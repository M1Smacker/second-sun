"""Independent arithmetic recount from saved times, without the v3 fitter."""
from collections import Counter, defaultdict
import csv
import importlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('032_harness')


def main():
    guard = H.Guard()
    guard.start()
    import numpy as np
    sample = json.loads((H.OUT/'fresh-controls.json').read_text(encoding='utf-8'))
    result = json.loads((H.OUT/'summary.json').read_text(encoding='utf-8'))
    with (H.OUT/'ephemerides-v3.csv').open(encoding='utf-8', newline='') as stream:
        tracks = list(csv.DictReader(stream))
    with (H.OUT/'eclipse-times-v3.csv').open(encoding='utf-8', newline='') as stream:
        events = list(csv.DictReader(stream))
    grouped = defaultdict(list)
    for e in events:
        assert e['star'] in guard.seen['g2']
        grouped[e['star'],e['type']].append(e)
    assert len(tracks) == 2*len(sample['selected'])
    assert {int(r['star']) for r in tracks} == set(sample['selected'])
    counts = Counter()
    binned = defaultdict(Counter)
    fits_checked = 0
    for row in tracks:
        star = row['star']
        points = grouped[star,row['type']]
        assert len(points) == int(row['n_measured'])
        raw = json.loads((H.OUT/'tracks'/f'{star}.json').read_text(encoding='utf-8'))
        original = raw['fit'].get(row['type'],{}).get('events', [])
        assert len(original) == len(points)
        for stored, source in zip(points, original):
            assert float(stored['time']) == source['time']
            assert float(stored['uncalibrated_error']) == source['error']
            scale = result['error_scales'].get(source['product'].removesuffix('-SAP'), 1.)
            assert math.isclose(float(stored['error']), source['error']*scale, rel_tol=1e-13)
        usable = agree = sigma_ok = False
        if row['period']:
            kept = [e for e in points if e['retained'] == 'True']
            drop = len(points)-len(kept)
            assert drop == int(row['n_dropped']) and drop <= len(points)//10
            assert len(kept) == int(row['n']) >= 3
            x = np.array([float(e['cycle'])-int(row['epoch_cycle']) for e in kept])
            y = np.array([float(e['time']) for e in kept])
            err = np.array([float(e['error']) for e in kept])
            extra = float(row['extra_scatter'])
            weights = 1/(err**2+extra**2)
            xm, ym = np.average(x,weights=weights), np.average(y,weights=weights)
            sxx = np.sum(weights*(x-xm)**2)
            period = np.sum(weights*(x-xm)*(y-ym))/sxx
            epoch = ym-period*xm
            residual = y-epoch-period*x
            chi = np.sum(weights*residual**2)/(len(x)-2)
            scatter = 1.4826*np.median(np.abs(residual-np.median(residual)))
            assert abs(period-float(row['period'])) < 1e-9
            assert abs(epoch-float(row['epoch'])) < 1e-8
            assert math.isclose(1/sxx, float(row['period_error'])**2, rel_tol=1e-8)
            assert math.isclose(1/weights.sum()+xm*xm/sxx, float(row['epoch_error'])**2, rel_tol=1e-8)
            assert abs(-xm/sxx-float(row['covariance'])) < 1e-12
            assert abs(chi-float(row['reduced_chi2'])) < 1e-5
            assert (abs(chi-1) < 1e-5) if extra else (chi <= 1+1e-5)
            assert abs(scatter-float(row['robust_scatter'])) < 1e-8
            sectors = len({e['sector'] for e in kept})
            usable = len(kept)>=3 and sectors>=2 and scatter <= .1*float(row['width'])
            assert usable == (row['usable']=='True')
            fits_checked += 1
            counts[f"{row['type']}:dropped"] += drop
            if usable and row['type']=='primary':
                cat = raw['catalogue']
                differences = []
                for sec in sample['sectors'][star]:
                    midpoint = sample['sector_midpoints'][str(sec)]
                    reference = cat['T0']+round((midpoint-cat['T0'])/cat['P'])*cat['P']
                    # Circular distance, independently of the fitter's nearest-cycle formula.
                    delta = (reference-epoch+period/2)%period-period/2
                    differences.append(abs(delta))
                agree = all(d <= cat['wp']/4 for d in differences) and bool(differences)
                sigma_ok = abs(period-cat['P']) <= 3*math.sqrt(1/sxx+cat['eP']**2)
        if row['type'] == 'primary':
            assert agree == (row['agrees']=='True') and sigma_ok == (row['period_3sigma']=='True')
            values = dict(selected=1, three_times=int(len(points)>=3), usable=int(usable), agrees=int(agree), period_3sigma=int(sigma_ok))
            counts.update(values)
            binned[row['period_bin']].update(values)
    for key, value in counts.items():
        assert result['counts'][key] == value, key
    assert {k:dict(v) for k,v in binned.items()} == result['period_bins']
    a1 = counts['three_times']>0 and 5*counts['usable']>=4*counts['three_times']
    a2 = counts['usable']>0 and 10*counts['agrees']>=9*counts['usable']
    a3 = result['trap_pass']==30
    assert result['rules'] == dict(A1=a1,A2=a2,A3=a3,passed=a1 and a2 and a3)
    evidence = dict(fits_recomputed=fits_checked, counts=dict(counts), rules=result['rules'],
                    limitation='Different arithmetic by the producer; not independent review.')
    (H.OUT/'recount.json').write_text(json.dumps(evidence,indent=2), encoding='utf-8')
    print(json.dumps(evidence,indent=2))


if __name__ == '__main__':
    main()
