"""Different-method first-loss recount and fixed-bin recovery aggregation."""
from collections import Counter, defaultdict
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('025_harness')
SEED = 2026111525
NAMES = ['B', 'B+C96', 'B+admit4096', 'B+C96+admit4096']


def aggregate(rows, np):
    stars = sorted({(r['campaign'], r['star']) for r in rows})
    positions = {key: i for i, key in enumerate(stars)}
    denom = np.zeros((len(stars), 5), dtype=int)
    hits = np.zeros((len(stars), 5, 2, 4), dtype=int)
    found = np.zeros_like(hits)
    for row in rows:
        i, b = positions[row['campaign'], row['star']], row['bin']
        denom[i, b] += 1
        for arm, label in enumerate(('real', 'flip')):
            hits[i, b, arm] += row[label]
            found[i, b, arm] += row[label + '_found']
    n = denom.sum(0)
    counts = hits.sum(0)
    rates = counts / n[:, None, None]
    samples = []
    rng = np.random.default_rng(SEED)
    while sum(len(s) for s in samples) < 10000:
        w = rng.multinomial(len(stars), np.full(len(stars), 1 / len(stars)), size=200)
        d = w @ denom
        valid = (d > 0).all(1)
        samples.append(np.einsum('rs,sbac->rbac', w[valid], hits) / d[valid, :, None, None])
    draws = np.concatenate(samples)[:10000]
    gain, loss = [], []
    for j in range(4):
        gain.append(sum(bool(r['real'][j]) and not bool(r['real'][j % 2]) for r in rows))
        loss.append(sum(bool(r['real'][j % 2]) and not bool(r['real'][j]) for r in rows))
    return dict(n=n.tolist(), counts=counts.tolist(), found_counts=found.sum(0).tolist(),
                rates=rates.tolist(), overall=rates.mean(0).tolist(), gains=gain, losses=loss,
                overall_ci95=np.quantile(draws.mean(1), [.025, .975], axis=0).tolist(),
                delta_ci95=np.quantile(draws - draws[:, :, :, [0, 1, 0, 1]], [.025, .975], axis=0).tolist(),
                control_ci99=np.quantile(draws[:, :, 0] - draws[:, :, 1], [.005, .995], axis=0).tolist())


def first_loss(row):
    cause = row['cause']
    if cause == 'no recorded cadence':
        return 'archive gap'
    if cause.endswith('load'):
        return 'quality exclusion' if any(f['finite_near'] for f in row['files']) else 'nonfinite archived flux'
    if cause == 'recorded, no safe windows':
        return 'no safe windows'
    if cause == 'recorded outside safe windows':
        return next(f['window_detail'] for f in row['files'] if f['cause'] == cause)
    files = [f for f in row['files'] if f['cause'] == 'raw centre covered']
    if any(f.get('masked_near', 0) and f.get('preparation_status') == 'ok' for f in files):
        return 'retained to score input'
    if all(f.get('preparation_status') == 'too little data' for f in files):
        return 'under 200 points before mask'
    if any(f.get('FIX101_near_centre') for f in files):
        return 'catalogue drift mask'
    return 'other eclipse or repeat mask'


def diagnostic(injected=False):
    prefix = 'injected-trace' if injected else 'trace'
    trace = sum((json.loads((H.OUT / f'{prefix}-{c}.json').read_text(encoding='utf-8'))['rows']
                 for c in ('g2', 'g3')), [])
    roster = json.loads((H.OUT / 'roster.json').read_text(encoding='utf-8'))
    keys = {(r['campaign'], r['trial']) for r in roster}
    original = [r for r in trace if (r['campaign'], r['trial']) in keys]
    assert len(trace) == 2000 and len(original) == 52
    assert Counter(r['cause'] for r in original) == Counter(r['cause'] for r in roster)
    load = [r for r in original if r['cause'].endswith('load')]
    usable = [r for r in original if r['cause'] in ('recorded outside safe windows', 'recorded, no safe windows')]
    assert len(load) == 21 and len(usable) == 16
    causes, by_bin, blocking, overlaps = Counter(), defaultdict(Counter), Counter(), Counter()
    for row in trace:
        cause = first_loss(row)
        causes[cause] += 1
        by_bin[str(row['bin'])][cause] += 1
        if cause == 'quality exclusion':
            bits = set()
            for f in row['files']:
                for bit in f['rejected_bits']:
                    if int(bit) & f['effective_quality_mask']:
                        bits.add(bit)
            blocking.update(bits)
        for field in ('FIX101_whole_sector', 'FIX101_near_centre', 'FIX101_zero_drift_restores_200'):
            overlaps[field] += any(f.get(field, False) for f in row['files'])
    load_table = Counter()
    for row in load:
        if not any(f['finite_near'] for f in row['files']):
            load_table['nonfinite archived flux'] += 1
            continue
        bits = {int(bit) for f in row['files'] for bit in f['rejected_bits']
                if int(bit) & f['effective_quality_mask']}
        load_table['+'.join(map(str, sorted(bits)))] += 1
    def alternatives(rows):
        return sum(any(f.get('preparation_status') == 'ok' and f.get('masked_near', 0)
                       for f in r.get('alternatives', [])) for r in rows)
    result = dict(total=2000, injected_before_mask=injected,
                  original_counts=dict(Counter(r['cause'] for r in original)),
                  all_first_loss=dict(causes), by_bin={k: dict(v) for k, v in by_bin.items()},
                  all_quality_bits=dict(blocking), original_load_bits=dict(load_table),
                  usable_window_rules=dict(Counter(first_loss(r) for r in usable)),
                  all_drift_overlap=dict(overlaps),
                  load_whole_sector_drift=sum(any(f.get('FIX101_whole_sector') for f in r['files']) for r in load),
                  load_no_safe_windows=sum(any(f.get('preparation_status') == 'no safe windows' for f in r['files']) for r in load),
                  load_alternative_product_keeps=alternatives(load), window_alternative_product_keeps=alternatives(usable),
                  missing_manifest=sum(any(not f['manifest'] for f in r['files']) for r in trace),
                  missing_files=sum(any(f['cause'] == 'missing file' for f in r['files']) for r in trace))
    (H.OUT / f'{"injected-" if injected else ""}diagnostic-summary.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    return result


def main():
    guard = H.Guard()
    guard.start()
    import numpy as np
    diag = diagnostic(injected='--diagnostic-only' not in sys.argv or '--injected' in sys.argv)
    if '--diagnostic-only' in sys.argv:
        return
    combined, background = {}, [[] for _ in NAMES]
    for bench in ('planets', 'T156'):
        rows = []
        for campaign in ('g2', 'g3'):
            sources = [json.loads((H.OUT / f'{prefix}{bench}-{campaign}-V0.json').read_text(encoding='utf-8'))
                       for prefix in ('baseline-', '')]
            maps = [{r['trial']: r for r in source['rows']} for source in sources]
            assert maps[0].keys() == maps[1].keys()
            for trial in sorted(maps[0]):
                a, b = (m[trial] for m in maps)
                row = {key: a[key] for key in ('trial', 'star', 'bin', 'campaign')}
                if bench == 'T156':
                    row.update(depth_ppm=a['depth_ppm'], duration_h=a['duration_h'])
                for label in ('real', 'flip'):
                    row[label] = a[label][:2] + b[label][:2]
                    row[label + '_found'] = [a[label + '_found']] * 2 + [b[label + '_found']] * 2
                rows.append(row)
            if bench == 'planets':
                for offset, source in zip((0, 2), sources):
                    for event in source['background']:
                        for j in range(2):
                            if event['options'][j]:
                                background[offset + j].append(event)
        assert len(rows) == (1098 if bench == 'planets' else 2000)
        combined[bench] = rows
        (H.OUT / f'combined-{bench}.json').write_text(json.dumps(rows), encoding='utf-8')
    reference = [r for r in combined['T156'] if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]
    assert len(reference) == 222
    metrics = {name: aggregate(rows, np) for name, rows in
               (('planets', combined['planets']), ('all_T156', combined['T156']), ('reference', reference))}
    import csv
    inputs = importlib.import_module('025_inputs')
    original = {(c, r['trial']): r for c in ('g2', 'g3') for r, _ in inputs.t156_rows(guard, c)}
    with H.TARGETS.open(encoding='utf-8-sig') as source:
        target_rows = list(csv.DictReader(line for line in source if not line.startswith('#')))
    magnitude = {}
    for target in target_rows:
        if target['list'] in guard.seen and target['tic'] in guard.seen[target['list']]:
            try:
                magnitude[target['list'], int(target['tic'])] = float(target.get('tmag', 'nan'))
            except ValueError:
                continue
    strata = defaultdict(lambda: dict(n=0, real=[0] * 4, flip=[0] * 4))
    for row in combined['T156']:
        source = original[row['campaign'], row['trial']]
        mag = magnitude.get((row['campaign'], row['star']), float('nan'))
        brightness = 'unknown' if not np.isfinite(mag) else '<11' if mag < 11 else '11to12' if mag < 12 else '12plus'
        sec = source['sector']
        era = '1to26' if sec <= 26 else '27to55' if sec < 56 else '56to93' if sec < 94 else '94plus'
        for dimension, value in (('product', source['product']), ('era', era), ('brightness', brightness)):
            cell = strata[f'{dimension}/{value}']
            cell['n'] += 1
            for arm in ('real', 'flip'):
                cell[arm] = [a + int(b) for a, b in zip(cell[arm], row[arm])]
    bg = [dict(real=sum(e['kind'] == 'real' for e in events),
               flip=sum(e['kind'] == 'flip' for e in events),
               bins=[dict(real=sum(e['bin'] == b and e['kind'] == 'real' for e in events),
                          flip=sum(e['bin'] == b and e['kind'] == 'flip' for e in events)) for b in range(5)])
          for events in background]
    assert [(r['real'], r['flip']) for r in bg[:2]] == [(174, 79), (124, 53)]
    ids = 0
    support = {}
    for campaign in ('g2', 'g3'):
        counts = json.loads((H.OUT / f'generated-{campaign}/counts.json').read_text(encoding='utf-8'))
        ids += counts['identity_sectors']
        support.update({(campaign, r['trial']): any(f['searched'] for f in r['support']) for r in counts['support']})
    roster = json.loads((H.OUT / 'roster.json').read_text(encoding='utf-8'))
    original_load = [r for r in roster if r['cause'].endswith('load')]
    restored = sum(support.get((r['campaign'], r['trial']), False) for r in original_load)
    new_events = []
    def key(e):
        return tuple(e.get(k) for k in ('campaign', 'tic', 'sector', 'kind', 'product', 'center', 'dur_h'))
    old_keys = {key(e) for e in background[0]}
    for event in background[2]:
        if key(event) not in old_keys:
            new_events.append(event)
    # Historical RS-027's diagnostic marks, fixed before candidate scoring.
    residue = dict(new_real=sum(e['kind'] == 'real' for e in new_events),
                   new_flip=sum(e['kind'] == 'flip' for e in new_events),
                   new_real_deep_or_high_snr=sum(e['kind'] == 'real' and
                       (e['depth_ppm'] >= 8000 or e['snr'] >= 50) for e in new_events))
    checks = dict(restores_half=restored >= 11,
                  reference_gain=metrics['reference']['overall'][0][2] > metrics['reference']['overall'][0][0],
                  upside_down_ceiling=bg[2]['flip'] <= bg[0]['flip'], identity_50=ids >= 50)
    summary = dict(configurations=NAMES, seed=SEED, bootstraps=10000, measurements=metrics,
                   background=bg, restored_load_centres=restored, identity_star_sectors=ids,
                   tests=checks, passes=all(checks.values()), residue=residue, diagnostic=diag,
                   descriptive_T156_strata=dict(strata))
    (H.OUT / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    (H.OUT / 'background.json').write_text(json.dumps(background), encoding='utf-8')
    (H.OUT / 'new-background.json').write_text(json.dumps(new_events, indent=2), encoding='utf-8')
    print('Candidate gates', checks, 'passes', summary['passes'])


if __name__ == '__main__':
    main()
