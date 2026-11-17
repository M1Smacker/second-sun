"""Blind orbit search of the complete SNR4 bank; historical baseline preserved."""
import argparse
from collections import defaultdict
import csv
import importlib
import json
import math
import os
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).parent))
D=importlib.import_module('028_inputs'); H=D.H
S=importlib.import_module('023_scoring_rules')
O=importlib.import_module('028_orbits')
J=importlib.import_module('028_outputs')


def truth(v): return bool(v) and v==v


def main(campaign,bench,pilot=False):
    os.environ.update(SS_SET=campaign,VESPER_OPTS='c6,p1',NUMBA_NUM_THREADS='2')
    guard=H.Guard(); guard.start(); guard.allow_machine_inputs(campaign)
    import numpy as np
    import pandas as pd
    import stage3_core as C
    import stage3_report as R
    from detect_v2 import FLIP_D
    target_frame=pd.read_csv(C.TARGETS,comment='#')
    ephemeris=C.Ephem(target_frame,C.eb_widths())
    original_csv=pd.read_csv
    pd.read_csv=lambda p,*a,**kw: target_frame.copy() if p==C.TARGETS else original_csv(p,*a,**kw)
    C.eb_widths=lambda: None
    C.Ephem=lambda *_: ephemeris
    strict=bench=='T156'
    intervals=defaultdict(list)
    with (H.ROOT/'research/stage3/rs028/known_events.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f): intervals[int(r['sector'])].append((float(r['start_tjd'])-.1,float(r['end_tjd'])+.1))
    assert sum(map(len,intervals.values()))==19
    targets=pd.read_csv(H.TARGETS,comment='#')
    allowed=targets[(targets['list']==campaign)&(targets.design_seen==1)].drop_duplicates('tic')
    periods=allowed.set_index('tic').p_bin_d.to_dict()
    epochs={}
    for r in pd.read_csv(C.TARGETS,comment='#').itertuples():
        if r.tic in periods: epochs.setdefault(r.tic,float(r.bjd0)-57000)
    best=pd.read_csv(C.BEST)[['tic','sector','product']].rename(columns={'product':'best'})
    radii={}
    with (H.ROOT/'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['set']==campaign and r['tic'] in guard.seen[campaign] and r['radius_rsun']:
                v=float(r['radius_rsun'])
                if math.isfinite(v) and v>0: radii[int(r['tic'])]=min(1.,(.2009/v)**2)*1e6
    def retier(events):
        buckets=defaultdict(list)
        for e in events: buckets[e['kind'],e['product']].append(e)
        out=[]
        for (kind,product),group in buckets.items():
            repeats=S.binary_members(group,periods[group[0]['tic']])
            real=buckets.get(('real',product),[])
            flips=set()
            if kind=='flip' and strict:
                flips,uncertain=S.symmetric_matches(real,group,FLIP_D)
                if uncertain: raise RuntimeError('Unresolved rounded coincidence')
            for i,e in enumerate(group):
                mirrored=(i in flips if strict else any(abs(e['center']-r['center'])<FLIP_D for r in real))
                q=dict(e,repeater=i in repeats,flipmatch=mirrored if kind=='flip' else e['flipmatch'])
                tmp=dict(q); tmp.pop('pdc_snr',None); q['tier']=C.tier_of(tmp); out.append(q)
        return out
    def frame(events):
        if not events: return pd.DataFrame()
        f=pd.DataFrame(events).merge(best,on=['tic','sector'],how='left')
        f['primary']=f['product']==f['best']
        f['c8_best']=pd.to_numeric(f['c8_best'],errors='coerce')
        return f
    def tiers(events): return R.apply_v7(R.merge_sap(events.reset_index(drop=True))) if not events.empty else events
    source=H.DATA/f'stage3_{campaign}'/f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
    assert not pilot or bench=='null'
    generated=H.OUT/f'{"pilot-" if pilot else ""}generated-{campaign}'
    coverage=json.loads((generated/'counts.json').read_text(encoding='utf-8'))
    expected={tuple(k) for k in coverage['affected']}
    assert all(str(k[0]) in guard.seen[campaign] for k in expected)
    groups=defaultdict(list); cameras=defaultdict(set)
    for star,sec in sorted(expected):
        for kind in D.KINDS:
            old=source/kind/f'{star}_{sec}.json'
            p=generated/'background'/kind/old.name
            assert p.is_file()==old.is_file(), 'Incomplete lower-threshold background'
            if not p.is_file(): continue
            g=json.loads(p.read_text(encoding='utf-8'))
            assert (g['tic'],g['sector'])==(star,sec)
            assert not any(str(m.get('status')).startswith('ERROR') for m in g['meta'])
            groups[star,sec].extend(g['events'])
            cameras[star,sec].update(m['camera'] for m in g['meta'] if 'camera' in m)
    context=frame([e for g in groups.values() for e in retier(g)])
    ranked=tiers(context)
    def eligible(events,star=None,arm=None):
        if events.empty: return []
        candidates=events[events.primary & (events.snr>=4)]
        if star is not None: candidates=candidates[candidates.tic==star]
        if arm is not None: candidates=candidates[candidates.kind==arm]
        result=[]
        for e in candidates.to_dict('records'):
            cap=radii.get(e['tic'])
            if cap is not None and e['depth_ppm']>cap: continue
            if any(e['center']+e['dur_h']/48>=a and e['center']-e['dur_h']/48<=b for a,b in intervals[e['sector']]): continue
            clean=dict(e,gap_dump=False,ramp=False,dominated=False)
            if C.tier_of(clean) not in S.TIERS: continue
            result.append({k:e[k] for k in ('tic','sector','kind','product','center','dur_h','depth_ppm','snr')})
        return result
    def run_star(events,star,arm,mutation=False):
        return O.search(eligible(events,star,arm),periods[star],epochs.get(star,math.nan),mutation)
    output=H.OUT/f'{"pilot-" if pilot else ""}{bench}-{campaign}.json'
    if bench=='null':
        rows=[]
        for number,star in enumerate(sorted({k[0] for k in expected}),1):
            own=ranked[ranked.tic==star]
            for arm in ('real','flip'):
                res=run_star(own,star,arm)
                mutant=run_star(own,star,arm,True)
                rows.append(dict(campaign=campaign,star=star,arm=arm,bin=int(np.searchsorted([10,14,20,27.4],periods[star],side='right')),
                    **res,mutant_sets=len(mutant['sets']),geometry_valid=math.isfinite(epochs.get(star,math.nan))))
            if number%25==0: print(campaign,'null hosts',number,flush=True)
        J.write_json(output,dict(rows=rows,sector_groups=len(expected)),default=lambda x:x.item() if isinstance(x,np.generic) else str(x))
        print(campaign,'null complete',len(rows),'host-arms',flush=True)
        return
    calibration=json.loads((H.OUT/'calibration.json').read_text(encoding='utf-8'))
    floor=calibration['floor']
    baseline=json.loads(D.read(guard,H.OUT.with_name('027')/f'baseline-{bench}-{campaign}-V0.json','027'))
    base={r['trial']:r for r in baseline['rows']}
    records=list(D.t156_rows(guard,campaign)) if strict else []
    if not strict:
        for p in sorted(H.OUT.with_name('006').glob(f'planet-*-*-*-{campaign}/results.jsonl')):
            for line in D.read(guard,p,'006').splitlines():
                r=json.loads(line)
                if r['observed']: records.append((r,p.parent))
    assert {r['trial'] for r,_ in records}==set(base)
    rows=[]; last=time.monotonic()
    cache=H.OUT/f'scored-{bench}-{campaign}'; cache.mkdir(exist_ok=True)
    for number,(record,_) in enumerate(records,1):
        star,trial=record['star'],record['trial']; assert str(star) in guard.seen[campaign]
        mark=cache/f'trial-{trial}.json'
        if mark.exists(): rows.append(json.loads(mark.read_text(encoding='utf-8'))); continue
        observed=[(record['time'],record['duration_h']/24)] if strict else record['observed']
        sectors={record['sector']} if strict else set(record['changed'])
        near=np.logical_or.reduce([(context.sector==sec)&context.camera.isin(cameras[star,sec]) for sec in sectors])
        own=context.tic==star; in_sector=context.sector.isin(sectors)
        keep=context[(own|near)&~(own&in_sector)]
        result={k:record[k] for k in ('campaign','star','trial','bin','depth_ppm')}
        if strict: result['duration_h']=record['duration_h']
        for sign,arm,label in ((1,'real','dip'),(-1,'flip','bump')):
            revised=[]
            for sec in sectors:
                for kind in D.KINDS:
                    p=generated/bench/f'trial-{trial}'/str(sign)/kind/f'{star}_{sec}.json'
                    assert p.is_file()==(source/kind/p.name).is_file(), 'Incomplete injection replay'
                    if p.is_file():
                        g=json.loads(p.read_text(encoding='utf-8'))
                        assert (g['tic'],g['sector'])==(star,sec)
                        assert not any(str(m.get('status')).startswith('ERROR') for m in g['meta'])
                        revised.extend(g['events'])
            filtered=frame(retier(revised))
            after=tiers(pd.concat([keep,filtered] if not filtered.empty else [keep],ignore_index=True))
            res=run_star(after,star,arm)
            hits=[]
            for promotion in (True,False):
                members=O.members(res,floor,promotion)
                novel=any(abs(e['center']-t)<=dur/2 for e in members for t,dur in observed)
                # Calibration excludes all background orbit sets at this floor.
                # T156's older broad preexisting exclusion is additionally retained.
                if strict and record[label]['preexisting']: novel=False
                hits.append(novel)
            b,k=base[trial][arm][0],base[trial][arm][3]
            result[arm]=[b,k,b or hits[0],b or hits[1],k or hits[0],k or hits[1]]
            result[arm+'_orbit']=hits
            result[arm+'_max']=res['max_score']
            result[arm+'_soft_candidates']=res['candidates']
        J.write_json(mark,result,default=lambda x:x.item() if isinstance(x,np.generic) else str(x))
        rows.append(result)
        if time.monotonic()-last>=60:
            print(campaign,bench,number,'/',len(records),flush=True); last=time.monotonic()
    J.write_json(output,dict(rows=rows),default=lambda x:x.item() if isinstance(x,np.generic) else str(x))
    print(campaign,bench,'complete',len(rows),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('campaign',choices=('g2','g3')); p.add_argument('bench',choices=('null','planets','T156'))
    p.add_argument('--pilot',action='store_true')
    a=p.parse_args(); main(a.campaign,a.bench,a.pilot)
