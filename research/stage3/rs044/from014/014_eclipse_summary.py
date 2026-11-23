"""Summarize eclipse fits and independent validation without emitting identifiers."""
import argparse
from collections import Counter
import csv
import importlib
import json
import math
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0,str(Path(__file__).parent))
S=importlib.import_module('014_eclipse_select')
F=importlib.import_module('014_eclipse_fit')
H=S.H
O=S.O
KINDS=('primary','secondary')
CAL=importlib.import_module('014_eclipse_calibrate')


def quantiles(values):
    return [float(x) for x in np.quantile(values,[0,.1,.25,.5,.75,.9,1])] if len(values) else []


def write_csv(path,rows,fields=None):
    names=fields or list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=names)
        w.writeheader()
        w.writerows(rows)


def night_shift(time,fit,cat,kind):
    phase=0 if kind=='primary' else cat['phs']
    if not np.isfinite(phase):
        return None
    epoch=cat['T0']+phase*cat['P']
    reference=epoch+round((time-epoch)/cat['P'])*cat['P']
    return float(F.folded_distance(reference,fit['epoch'],fit['period'])*-1)


def injection_check(row):
    base=row['fit']
    originals={k:base[k] for k in KINDS if k in base and base[k]['fit'] and base[k]['fit']['usable']}
    if not originals:
        return dict(status='unusable baseline',max_shift=None)
    worst=0.
    for signed in row.get('injected',{}).values():
        for name,track in originals.items():
            candidate=signed.get(name,{})
            if not candidate.get('fit') or not candidate['fit']['usable']:
                return dict(status='missing usable injected fit',max_shift=None)
            for e in track['events']:
                nearby=[abs(q['time']-e['time'])/e['width'] for q in candidate['events']
                        if abs(q['time']-e['time'])<=e['width']]
                if not nearby:
                    return dict(status='missing timing event',max_shift=None)
                worst=max(worst,min(nearby))
    assert len(row['injected'])==2
    return dict(status='pass' if worst<=.1 else 'timing shift above one tenth width',max_shift=worst)


def main(slots):
    guard=H.Guard()
    guard.start()
    samples=json.loads((H.OUT/'eclipse-samples.json').read_text(encoding='utf-8'))
    rows=CAL.load('calibrate',slots)+CAL.load('holdout',slots)
    calibration=json.loads((H.OUT/'timing-calibration.json').read_text())
    for row in rows: CAL.apply(row,calibration['scales'])
    counters={}
    assert sorted(r['star'] for r in rows)==sorted(samples['affected']+samples['controls']+samples['holdout'])
    assert all(str(r['star']) in guard.seen['g2'] for r in rows)
    ephem=[]
    events=[]
    sector_offsets=[]
    usable=Counter()
    status=Counter()
    control=Counter()
    aliases=Counter()
    observed=Counter()
    period_deltas=[]
    standardized=[]
    shift_days={k:[] for k in KINDS}
    shift_widths={k:[] for k in KINDS}
    phases=[]
    phase_offsets=[]
    injection=[]
    by={r['star']:r for r in rows}
    for row in rows:
        cat=row['catalogue'] or {}
        star=row['star']
        sample=row['sample']
        outputs=row['fit']
        fits={k:outputs.get(k,{}).get('fit') for k in KINDS}
        passed={k for k,fit in fits.items() if fit and fit['usable']}
        usable[sample,','.join(sorted(passed)) or 'none']+=1
        aliases[sample,str(outputs.get('alias','none'))]+=1
        if sample in ('control','holdout'):
            primary=fits['primary']
            p_ok=t_ok=width_ok=period_width_ok=False
            if 'primary' in passed:
                p_ok=abs(primary['period']-cat['P'])<=3*math.hypot(primary['period_error'],cat['eP'])
                n=round((cat['T0']-primary['epoch'])/primary['period'])
                diff=primary['epoch']+n*primary['period']-cat['T0']
                var=primary['epoch_error']**2+(n*primary['period_error'])**2+2*n*primary['covariance']
                width_ok=abs(diff)<=outputs['primary']['width']/4
                period_width_ok=abs(primary['period']-cat['P'])<=outputs['primary']['width']/4
                t_ok=abs(diff)<=3*math.sqrt(max(0,var)+cat['eT0']**2)
            for key,value in [('period',p_ok),('epoch',t_ok),('both',p_ok and t_ok),('quarter_width',width_ok),('period_quarter_width',period_width_ok)]:
                control[f'{sample}:{key}']+=int(value)
        if str(star) in samples['injections']:
            injection.append(injection_check(row))
        phase=None
        if fits['primary'] and fits['secondary']:
            t=fits['primary']['epoch']
            secondary=fits['secondary']
            e=secondary['epoch']+round((t-secondary['epoch'])/secondary['period'])*secondary['period']
            phase=(e-t)%fits['primary']['period']/fits['primary']['period']
            if sample=='affected' and len(passed)==2:
                phases.append(phase)
                if np.isfinite(cat['phs']):
                    phase_offsets.append(float(F.folded_distance(phase,cat['phs'],1)))
        for k in KINDS:
            component=outputs.get(k,{})
            fit=fits[k]
            n=len(component.get('events',[]))
            observed[sample,k,n]+=1
            reason=('usable' if k in passed else 'timing variations' if fit else 'fewer than three times' if n<3 else 'insufficient cycle span')
            status[sample,k,reason]+=1
            rec=dict(star=star,sample=sample,type=k,status=reason,width=component.get('width'),
                     catalogue_period=cat.get('P'),catalogue_period_error=cat.get('eP'),catalogue_epoch=cat.get('T0'),
                     catalogue_secondary_phase=cat.get('phs'),measured_secondary_phase=phase,
                     alias=outputs.get('alias'),alias_reason=outputs.get('alias_reason'),input_curves=row.get('input_curves',0),measured_events=n)
            if fit:rec.update(fit)
            ephem.append(rec)
            events.extend(dict(star=star,sample=sample,type=k,**e) for e in component.get('events',[]))
            if sample!='affected' or k not in passed:continue
            if k=='primary':
                delta=fit['period']-cat['P']
                period_deltas.append(delta)
                if np.isfinite(cat['eP']) and cat['eP']>0:
                    standardized.append(delta/cat['eP'])
            for sec in row['sectors']:
                diff=night_shift(samples['sector_midpoints'][str(sec)],fit,cat,k)
                if diff is not None and np.isfinite(diff):
                    width=component['width']
                    shift_days[k].append(diff)
                    shift_widths[k].append(diff/width)
                    sector_offsets.append(dict(star=star,type=k,sector=sec,days=diff,widths=diff/width))
    assert len(injection)==20 and len(ephem)==424
    event_tests=Counter()
    path=H.OUT.with_name('011')/'new-events.csv'
    source=S.saved(guard,path,'011').splitlines()
    for e in csv.DictReader(source):
        if e['kind']!='real':continue
        star=int(e['tic'])
        t=float(e['center'])
        assert str(star) in guard.seen['g2']
        group=(e['variant'],'deep' if float(e['depth_ppm'])>=8000 or float(e['snr'])>=50 else 'shallow')
        event_tests[group+('total',)]+=1
        matches=[]
        diagnostic_match=False
        usable_count=0
        for k in KINDS:
            rec=by.get(star,{}).get('fit',{}).get(k,{})
            fit=rec.get('fit')
            if fit:
                hit=abs(F.folded_distance(t,fit['epoch'],fit['period']))<=rec['width']
                diagnostic_match|=hit
                if fit['usable']:
                    usable_count+=1
                    if hit:
                        matches.append(k)
        if diagnostic_match:
            event_tests[group+('matched including flagged',)]+=1
        if usable_count:
            event_tests[group+('has usable fit',)]+=1
        if matches:
            event_tests[group+('matched',)]+=1
            event_tests[group+('+'.join(matches),)]+=1
    assert event_tests['V1','deep','total']==21 and event_tests['V2','deep','total']==18
    write_csv(H.OUT/'ephemerides-v2.csv',ephem)
    write_csv(H.OUT/'eclipse-times-v2.csv',events)
    write_csv(H.OUT/'sector-offsets-v2.csv',sector_offsets)
    fmt=lambda counter:{':'.join(map(str,k)):v for k,v in counter.items()}
    result=dict(worker_counts=counters,usable=fmt(usable),status=fmt(status),aliases=fmt(aliases),
                observed=fmt(observed),control=control,event_tests=fmt(event_tests),
                injection=Counter(r['status'] for r in injection),
                injection_max_shift=quantiles([r['max_shift'] for r in injection if r['max_shift'] is not None]),
                period_delta_days=quantiles(period_deltas),period_delta_catalogue_sigma=quantiles(standardized),
                period_n=len(period_deltas),period_sigma_n=len(standardized),
                sector_shift_days={k:quantiles(v) for k,v in shift_days.items()},
                sector_shift_widths={k:quantiles(v) for k,v in shift_widths.items()},
                sector_shift_n={k:len(v) for k,v in shift_days.items()},
                measured_secondary_phase=quantiles(phases),phase_offset=quantiles(phase_offsets),
                measured_secondary_n=len(phases),phase_offset_n=len(phase_offsets),events=len(events),
                calibration=calibration,control_primary_median_chi2={sample:float(np.median([
                    r['fit']['primary']['fit']['reduced_chi2'] for r in rows
                    if r['sample']==sample and r['fit'].get('primary',{}).get('fit')]))
                    for sample in ('control','holdout')},
                affected_timing_variation_stars=sum(r['sample']=='affected' and any(
                    r['fit'].get(k,{}).get('fit') and not r['fit'][k]['fit']['usable'] for k in KINDS) for r in rows))
    O.write_json(H.OUT/'eclipse-summary.json',result,indent=2)
    print('Usable',result['usable'],'control',control,'injection',result['injection'])
    print('Event tests',result['event_tests'],flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('slots',type=int)
    main(p.parse_args().slots)
