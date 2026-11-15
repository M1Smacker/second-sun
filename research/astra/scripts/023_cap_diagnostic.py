"""Diagnose cap losses using the fixed planted depths and independently read radii."""
from collections import Counter
import csv
import importlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('023_inputs')
H = D.H
O = importlib.import_module('023_outputs')


def main():
    guard = H.Guard()
    guard.start()
    radii = {}
    with (H.ROOT / 'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as source:
        for row in csv.DictReader(source):
            if row['set'] in guard.seen and row['tic'] in guard.seen[row['set']] and row['radius_rsun']:
                radius = float(row['radius_rsun'])
                if radius > 0 and math.isfinite(radius):
                    radii[row['set'], int(row['tic'])] = radius
    draws = {}
    for campaign in ('g2', 'g3'):
        for journal in sorted(H.OUT.with_name('006').glob(f'planet-*-*-*-{campaign}/results.jsonl')):
            for line in D.read(guard, journal, '006').splitlines():
                row = json.loads(line)
                assert str(row['star']) in guard.seen[campaign]
                if row['observed']:
                    draws[campaign, row['trial']] = row
    results = json.loads((H.OUT / 'combined-planets.json').read_text(encoding='utf-8'))
    summary = Counter()
    per_bin = [Counter() for _ in range(5)]
    private = []
    for row in results:
        key = row['campaign'], row['trial']
        draw = draws[key]
        radius = radii.get((row['campaign'], row['star']))
        cap = min(1., (.2009 / radius) ** 2) * 1e6 if radius is not None else None
        category = 'unknown radius' if cap is None else 'planted above cap' if draw['depth_ppm'] > cap else 'planted within cap'
        summary[category] += 1
        for arm in ('real', 'flip'):
            for base, guarded, name in ((0, 1, 'B'), (2, 3, 'DS')):
                if row[arm][base] and not row[arm][guarded]:
                    label = f'{name}:{arm}:lost:{category}'
                    summary[label] += 1
                    per_bin[row['bin']][label] += 1
                    private.append(dict(row, arm=arm, base=name, planted_depth_ppm=draw['depth_ppm'],
                                        maximum_depth_ppm=cap, category=category))
                if not row[arm][base] and row[arm][guarded]:
                    summary[f'{name}:{arm}:gained:{category}'] += 1
    assert len(draws) == len(results) == 1098
    t156 = json.loads((H.OUT / 'combined-T156.json').read_text(encoding='utf-8'))
    reference = [r for r in t156 if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]
    reference_losses = Counter()
    for row in reference:
        radius = radii.get((row['campaign'], row['star']))
        cap = min(1., (.2009 / radius) ** 2) * 1e6 if radius is not None else None
        category = 'unknown radius' if cap is None else 'planted above cap' if row['depth_ppm'] > cap else 'planted within cap'
        if row['real'][0] and not row['real'][1]:
            reference_losses[category] += 1
    # Examine original detector boxes for the physically allowed real-arm loss.
    ratios = []
    for loss in private:
        if loss['arm'] != 'real' or loss['base'] != 'B' or loss['category'] != 'planted within cap':
            continue
        campaign, trial = loss['campaign'], loss['trial']
        draw = draws[campaign, trial]
        folder = None
        for journal in sorted(H.OUT.with_name('006').glob(f'planet-*-*-*-{campaign}/results.jsonl')):
            if any(json.loads(line)['trial'] == trial for line in D.read(guard, journal, '006').splitlines()):
                folder = journal.parent / f'trial-{trial}' / '1'
                break
        assert folder is not None
        for sector in draw['changed']:
            for kind in D.KINDS:
                path = folder / kind / f"{loss['star']}_{sector}.json"
                if not path.is_file():
                    continue
                group = json.loads(D.read(guard, path, '006'))
                for event in group['events']:
                    if event['kind'] == 'real' and event['snr'] >= 7 and any(abs(event['center'] - t) <= d / 2 for t, d in draw['observed']):
                        ratios.append(event['depth_ppm'] / loss['maximum_depth_ppm'])
        loss['input_to_cap'] = draw['depth_ppm'] / loss['maximum_depth_ppm']
        loss['matching_box_depth_ratios'] = ratios[:]
    diagnostic = dict(counts=dict(summary), per_bin=list(map(dict, per_bin)),
                      reference_real_losses=dict(reference_losses),
                      within_cap_lost_real_matching_boxes=len(ratios),
                      within_cap_lost_real_measured_ratio_range=[min(ratios), max(ratios)] if ratios else None,
                      within_cap_lost_real_input_ratios=[r['input_to_cap'] for r in private if 'input_to_cap' in r])
    O.write_json(H.OUT / 'cap-diagnostic.json', diagnostic, indent=2)
    O.write_json(H.OUT / 'cap-loss-trials.json', private)
    print(json.dumps(diagnostic, indent=2))


if __name__ == '__main__':
    main()
