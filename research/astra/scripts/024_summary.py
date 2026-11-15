"""Aggregate paired design-star recovery and whole-star uncertainty."""
from collections import Counter, defaultdict
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('024_harness')
NAMES = ('B', 'B+C96', 'B+subtraction', 'B+C96+subtraction')
SEED = 2026111524


def metric(rows, np):
    keys = sorted({(r['campaign'], r['star']) for r in rows})
    position = {key: i for i, key in enumerate(keys)}
    denominator = np.zeros((len(keys), 5), dtype=int)
    success = np.zeros((len(keys), 5, 2, 4), dtype=int)
    found = np.zeros_like(success)
    transitions = np.zeros((5, 4, 2), dtype=int)
    for row in rows:
        i, b = position[row['campaign'], row['star']], row['bin']
        denominator[i, b] += 1
        for arm, label in enumerate(('real', 'flip')):
            success[i, b, arm] += row[label]
            found[i, b, arm] += row[label + '_found']
        for j in range(4):
            baseline = j % 2
            transitions[b, j, 0] += row['real'][j] and not row['real'][baseline]
            transitions[b, j, 1] += row['real'][baseline] and not row['real'][j]
    totals = denominator.sum(0)
    counts = success.sum(0)
    found_counts = found.sum(0)
    samples, found_samples = [], []
    rng = np.random.default_rng(SEED)
    while sum(len(chunk) for chunk in samples) < 10000:
        weights = rng.multinomial(len(keys), np.full(len(keys), 1 / len(keys)), size=200)
        n = weights @ denominator
        valid = np.all(n > 0, axis=1)
        weights, n = weights[valid], n[valid]
        samples.append(np.einsum('rs,sbac->rbac', weights, success) / n[:, :, None, None])
        found_samples.append(np.einsum('rs,sbac->rbac', weights, found) / n[:, :, None, None])
    samples = np.concatenate(samples)[:10000]
    found_samples = np.concatenate(found_samples)[:10000]
    rates = counts / totals[:, None, None]
    found_rates = found_counts / totals[:, None, None]
    # Paired samples share the same whole-star draw for all configurations and arms.
    delta = samples - samples[:, :, :, [0, 1, 0, 1]]
    found_delta = found_samples - found_samples[:, :, :, [0, 1, 0, 1]]
    control = samples[:, :, 0] - samples[:, :, 1]
    return dict(n=totals.tolist(), clusters=len(keys), counts=counts.tolist(), found_counts=found_counts.tolist(),
                rates=rates.tolist(), found_rates=found_rates.tolist(), overall=rates.mean(0).tolist(),
                overall_ci95=np.quantile(samples.mean(1), [.025, .975], axis=0).tolist(),
                ci95=np.quantile(samples, [.025, .975], axis=0).tolist(),
                delta_ci95=np.quantile(delta, [.025, .975], axis=0).tolist(),
                delta_B_ci95=np.quantile(samples - samples[:, :, :, [0, 0, 0, 0]], [.025, .975], axis=0).tolist(),
                found_delta_ci95=np.quantile(found_delta, [.025, .975], axis=0).tolist(),
                control_ci99=np.quantile(control, [.005, .995], axis=0).tolist(),
                transitions=transitions.tolist())


def main():
    guard = H.Guard()
    guard.start()
    import numpy as np
    subtraction = importlib.import_module('024_subtract')
    combined = {}
    background = [[] for _ in NAMES]
    for bench in ('planets', 'T156'):
        rows = []
        for campaign in ('g2', 'g3'):
            sources = [json.loads((H.OUT / f'{prefix}{bench}-{campaign}-V0.json').read_text(encoding='utf-8'))
                       for prefix in ('baseline-', '')]
            mappings = [{row['trial']: row for row in source['rows']} for source in sources]
            assert mappings[0].keys() == mappings[1].keys()
            for trial in sorted(mappings[0]):
                original, revised = (m[trial] for m in mappings)
                row = {k: original[k] for k in ('trial', 'star', 'bin', 'campaign')}
                assert str(row['star']) in guard.seen[campaign]
                if bench == 'T156':
                    row.update(depth_ppm=original['depth_ppm'], duration_h=original['duration_h'])
                for label in ('real', 'flip'):
                    row[label] = original[label][:2] + revised[label][:2]
                    row[label + '_found'] = [original[label + '_found']] * 2 + [revised[label + '_found']] * 2
                rows.append(row)
            if bench == 'planets':
                for offset, source in zip((0, 2), sources):
                    for event in source['background']:
                        for j in range(2):
                            if event['options'][j]:
                                background[offset + j].append(event)
        combined[bench] = rows
        assert len(rows) == (1098 if bench == 'planets' else 2000)
        (H.OUT / f'combined-{bench}.json').write_text(json.dumps(rows), encoding='utf-8')
    reference = [r for r in combined['T156'] if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]
    assert len(reference) == 222
    measurements = {name: metric(rows, np) for name, rows in
                    (('planets', combined['planets']), ('reference', reference), ('all_T156', combined['T156']))}
    assert abs(measurements['planets']['overall'][0][0] - .4810499792381308) < 1e-5
    counts = [Counter((r['campaign'], r['bin'], r['kind']) for r in events) for events in background]
    background_table = [dict(real=sum(r['kind'] == 'real' for r in events),
                             flip=sum(r['kind'] == 'flip' for r in events),
                             bins=[dict(real=sum(counts[j][c, b, 'real'] for c in ('g2', 'g3')),
                                        flip=sum(counts[j][c, b, 'flip'] for c in ('g2', 'g3'))) for b in range(5)])
                        for j, events in enumerate(background)]
    assert [(r['real'], r['flip']) for r in background_table[:2]] == [(174, 79), (124, 53)]
    coverage, scatter, controls, identities = [], [], [], []
    for campaign in ('g2', 'g3'):
        data = json.loads((H.OUT / f'generated-{campaign}/counts.json').read_text(encoding='utf-8'))
        for name, destination in (('coverage', coverage), ('scatter', scatter), ('controls', controls), ('identity', identities)):
            destination.extend(dict(row, campaign=campaign) for row in data[name])
        extra = H.OUT / f'coverage-{campaign}/counts.json'
        if extra.exists():
            recovered = json.loads(extra.read_text(encoding='utf-8'))
            identities.extend(dict(row, campaign=campaign) for row in recovered['identity'])
        empty = H.OUT / f'empty-{campaign}/counts.json'
        if empty.exists():
            recovered = json.loads(empty.read_text(encoding='utf-8'))
            identities.extend(dict(row, campaign=campaign) for row in recovered['identity'])
    controls = controls[:20]
    assert len(controls) == 20
    per_star = defaultdict(list)
    periods = {(r['campaign'], r['star']): r['period'] for r in coverage}
    for row in scatter:
        key = row['campaign'], row['star']
        if 5 <= periods[key] < 10:
            per_star[key].append(row)
    star_scatter = [dict(campaign=c, star=star, products=len(records),
                         before_ppm=float(np.median([r['before'] for r in records]) * 1e6),
                         after_ppm=float(np.median([r['after'] for r in records]) * 1e6),
                         changed=any(r['status'] == 'applied' and r['bins'] > 1 for r in records))
                    for (c, star), records in sorted(per_star.items())]
    (H.OUT / 'per-star-scatter.json').write_text(json.dumps(star_scatter, indent=2), encoding='utf-8')
    (H.OUT / 'periodic-controls.json').write_text(json.dumps(controls, indent=2), encoding='utf-8')
    # Keep complete private identifiers and crossing details inside the data directory.
    (H.OUT / 'background.json').write_text(json.dumps(background), encoding='utf-8')
    gates = []
    for j in (2, 3):
        tests = {}
        for bench in ('planets', 'reference'):
            value = measurements[bench]
            tests[bench + '_short_tier1_gain'] = value['delta_B_ci95'][0][0][0][j] > 0
            tests[bench + '_short_detection_gain'] = value['found_delta_ci95'][0][0][0][j] > 0
            tests[bench + '_other_bins'] = all(value['delta_B_ci95'][1][b][0][j] >= 0 for b in range(1, 5))
            tests[bench + '_paired_control'] = all(value['control_ci99'][0][b][j] <= 0 <= value['control_ci99'][1][b][j]
                                                  for b in range(5))
        tests['upside_down_background'] = background_table[j]['flip'] <= 79
        gates.append(dict(configuration=NAMES[j], tests=tests, passes=all(tests.values())))
    control_summary = {name: dict(median=float(np.median([r[name] for r in controls if r[name] is not None])),
                                  minimum=float(min(r[name] for r in controls if r[name] is not None)),
                                  maximum=float(max(r[name] for r in controls if r[name] is not None)))
                       for name in ('after_mask', 'after_subtraction', 'after_detrending')}
    coverage_counts = Counter(r['status'] for r in coverage)
    span_skips = [r for r in coverage if r['status'] == 'fewer_than_three_cycles'
                  or (r.get('products') and all(p['status'] == 'fewer_than_three_cycles' for p in r['products']))]
    span_skip_keys = {(r['campaign'], r['star'], r['sector']) for r in span_skips}
    per_star_coverage = defaultdict(list)
    for row in coverage:
        per_star_coverage[row['campaign'], row['star']].append(row)
    all_span_skipped_stars = sum(all((r['campaign'], r['star'], r['sector']) in span_skip_keys for r in rows)
                                 for rows in per_star_coverage.values())
    summary = dict(configurations=NAMES, seed=SEED, bootstraps=10000, measurements=measurements,
                   background=background_table, gates=gates, coverage=dict(coverage_counts),
                   total_star_sectors=len(coverage), total_stars=len({(r['campaign'], r['star']) for r in coverage}),
                   changed_stars=len({(r['campaign'], r['star']) for r in coverage if r['status'] == 'changed'}),
                   fewer_than_three_cycles_sectors=len(span_skips),
                   fewer_than_three_cycles_all_sectors_stars=all_span_skipped_stars,
                   controls=control_summary, identity_groups=len(identities),
                   symmetry_max_error=max(r.get('symmetry_error') or 0 for r in scatter),
                   synthetic=subtraction.checks(),
                   scatter=dict(stars=len(star_scatter), before_median_ppm=float(np.median([r['before_ppm'] for r in star_scatter])),
                                after_median_ppm=float(np.median([r['after_ppm'] for r in star_scatter]))))
    (H.OUT / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print('Summary complete', [(g['configuration'], g['passes']) for g in gates])


if __name__ == '__main__':
    main()
