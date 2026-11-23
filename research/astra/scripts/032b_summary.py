"""Score the fixed held-out judge; all details stay under data/astra/032b."""
import argparse
from collections import Counter, defaultdict
import importlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
S = importlib.import_module('032b_eclipse_select')
J = importlib.import_module('032b_holdout')
CAL = importlib.import_module('032b_eclipse_calibrate')
H, O = S.H, S.O


def score(label, sample, rows, scales):
    counts, bins, records = Counter(), defaultdict(Counter), []
    assert len(rows) == len({r['star'] for r in rows}) == len(sample['selected'])
    assert {r['star'] for r in rows} == set(sample['selected'])
    for row in rows:
        star, cat = row['star'], row['catalogue']
        period = sample['periods'][str(star)]
        b = next((i for i, edge in enumerate([10,14,20,27.4]) if period < edge), 4)
        counts['selected'] += 1; bins[b]['selected'] += 1
        for kind in ('primary', 'secondary'):
            track = row['fit'].get(kind, {})
            result = J.judge(track, row['fit'].get('search_period'), scales)
            full = result['all_fit']
            all_usable = bool(full and full['usable'])
            agree, sigma = False, None
            if kind == 'primary' and all_usable:
                midpoints = [sample['sector_midpoints'][str(sec)] for sec in sample['sectors'][str(star)]]
                agree, _ = J.M.sector_agreement(full, cat, midpoints)
                if math.isfinite(cat['eP']):
                    sigma = abs(full['period']-cat['P']) <= 3*math.hypot(full['period_error'], cat['eP'])
            events = J.calibrated(track, scales)
            record = dict(star=star, sample=label, type=kind, period_bin=b,
                          width=track.get('width'), seed_period=row['fit'].get('search_period'),
                          epoch_seed=track.get('epoch_seed'), events=events,
                          catalogue=cat, catalogue_midpoints=[sample['sector_midpoints'][str(sec)] for sec in sample['sectors'][str(star)]],
                          all_usable=all_usable, catalogue_agrees=agree, period_3sigma=sigma, **result)
            records.append(record)
            values = dict(eligible=result['eligible'], usable=result['usable'], predicts=result['predicts'],
                          measured=result['n_measured'], all_usable=all_usable, catalogue_agrees=agree,
                          train_dropped=result['train']['n_dropped'] if result['train'] else 0,
                          all_dropped=full['n_dropped'] if full else 0,
                          period_3sigma_available=sigma is not None, period_3sigma=sigma is True)
            for k, v in values.items():
                counts[f'{kind}:{k}'] += int(v)
                bins[b][f'{kind}:{k}'] += int(v)
    O.write_json(H.OUT/f'judged-{label}.json', records)
    result = dict(counts=dict(counts), bins=dict(bins))
    O.write_json(H.OUT/f'counts-{label}.json', result, indent=2)
    return result


def main(cached_only=False):
    guard = H.Guard(); guard.start()
    samples = json.loads((H.OUT/'samples.json').read_text(encoding='utf-8'))
    calibration = json.loads(S.saved(guard,H.OUT.with_name('014')/'timing-calibration.json','014'))
    old = [r for i in range(3) for r in json.loads(S.saved(guard,H.OUT.with_name('014')/f'eclipse-calibrate-{i}.json','014'))['rows']]
    assert all(str(r['star']) in guard.seen['g2'] for r in old)
    trap_path = H.OUT/'trap.json'
    if trap_path.exists():
        trap = json.loads(trap_path.read_text(encoding='utf-8'))['passed']
    else:
        trap = CAL.trap(old)
        O.write_json(trap_path, dict(passed=trap, total=30))
    results = {}
    for label, sample in samples['sets'].items():
        if label == 'g3' and cached_only:
            continue
        if label == 'affected':
            rows = [r for r in old if r['star'] in sample['selected']]
        elif label == 'seen':
            rows = [json.loads(S.saved(guard,H.OUT.with_name('032')/'tracks'/f'{star}.json','032')) for star in sample['selected']]
        else:
            rows = [json.loads((H.OUT/'tracks'/f'g3-{star}.json').read_text(encoding='utf-8')) for star in sample['selected']]
        assert all(str(r['star']) in guard.seen[sample['campaign']] for r in rows)
        results[label] = score(label, sample, rows, calibration['scales'])
        c = results[label]['counts']
        results[label]['rules'] = J.rules(c['primary:eligible'], c['primary:usable'], c['primary:predicts'], trap)
        print(label, 'eligible', c['primary:eligible'], 'usable', c['primary:usable'],
              'predicts', c['primary:predicts'], 'rules', results[label]['rules'], flush=True)
    result = dict(sets=results, trap_pass=trap, trap_n=30, cached_only=cached_only,
                  passed=not cached_only and all(results[k]['rules']['passed'] for k in ('affected','g3')),
                  seen_is_not_judging=True)
    O.write_json(H.OUT/('cached-summary.json' if cached_only else 'summary.json'), result, indent=2)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--cached-only', action='store_true')
    main(p.parse_args().cached_only)
