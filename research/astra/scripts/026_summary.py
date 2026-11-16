"""Fixed-population paired whole-star bootstrap and counts-only tables."""
from collections import Counter
import csv
import importlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('026_inputs')
H = D.H
CONFIGS = ('B', 'B+M2', 'B+M4', 'B+C96fallback', 'B+C96+DS+M4', 'cap+R2+M4')
INDICES = {'V0': (0, 3), 'V2': (1,), 'V4': (2, 4, 5)}
SEED = 2026111523


def metric(rows, np):
    keys = sorted({(r['campaign'], r['star']) for r in rows})
    index = {k: i for i, k in enumerate(keys)}
    den = np.zeros((len(keys), 5), dtype=int)
    hit = np.zeros((len(keys), 5, 2, 6), dtype=int)
    for r in rows:
        j, b = index[r['campaign'], r['star']], r['bin']
        den[j, b] += 1
        for arm, name in enumerate(('real', 'flip')):
            hit[j, b, arm] += r[name]
    n, k = den.sum(0), hit.sum(0)
    rates = k / n[:, None, None]
    rng = np.random.default_rng(SEED)
    samples = []
    while len(samples) < 10000:
        w = rng.multinomial(len(keys), np.full(len(keys), 1 / len(keys)), size=200)
        d = w @ den
        valid = (d > 0).all(1)
        count = (w[valid] @ hit.reshape(len(keys), -1)).reshape(-1, 5, 2, 6)
        samples.extend(count / d[valid, :, None, None])
    samples = np.asarray(samples[:10000])
    average = samples.mean(1)
    return dict(n=n.tolist(), counts=k.tolist(), per_bin=rates.tolist(), rates=rates.mean(0).tolist(),
                rate95=np.quantile(average, [.025, .975], axis=0).tolist(),
                per_bin95=np.quantile(samples, [.025, .975], axis=0).tolist(),
                gain95=np.quantile(average[:, 0] - average[:, 0, [0]], [.025, .975], axis=0).tolist(),
                paired99=np.quantile(samples[:, :, 0] - samples[:, :, 1], [.005, .995], axis=0).tolist())


def main():
    guard = H.Guard()
    guard.start()
    import numpy as np
    combined, background = {}, [[] for _ in CONFIGS]
    for bench in ('planets', 'T156'):
        rows = {}
        for campaign in ('g2', 'g3'):
            for mode, indices in INDICES.items():
                data = json.loads((H.OUT / f'{bench}-{campaign}-{mode}.json').read_text(encoding='utf-8'))
                for r in data['rows']:
                    assert str(r['star']) in guard.seen[campaign]
                    key = campaign, r['trial']
                    out = rows.setdefault(key, dict(r, real=[None] * 6, flip=[None] * 6))
                    for arm in ('real', 'flip'):
                        for i, value in zip(indices, r[arm]):
                            assert out[arm][i] is None
                            out[arm][i] = bool(value)
                if bench == 'planets':
                    for event in data['background']:
                        assert str(event['tic']) in guard.seen[campaign]
                        for i, yes in zip(indices, event['options']):
                            if yes:
                                background[i].append(event)
        combined[bench] = list(rows.values())
        assert all(None not in r['real'] + r['flip'] for r in rows.values())
        (H.OUT / f'combined-{bench}.json').write_text(json.dumps(combined[bench]), encoding='utf-8')
    assert len(combined['planets']) == 1098 and len(combined['T156']) == 2000
    radii = {}
    with (H.ROOT / 'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['set'] not in guard.seen or r['tic'] not in guard.seen[r['set']]:
                continue
            try:
                radius = float(r['radius_rsun'])
            except ValueError:
                continue
            if math.isfinite(radius) and radius > 0:
                radii[r['set'], int(r['tic'])] = radius
    depths = {}
    for campaign in ('g2', 'g3'):
        for path in sorted((H.DATA / 'astra/006').glob(f'planet-*-*-*-{campaign}/results.jsonl')):
            for line in D.read(guard, path, '006').splitlines():
                row = json.loads(line)
                assert str(row['star']) in guard.seen[campaign]
                depths[campaign, row['trial']] = row['depth_ppm']
    possible = []
    for r in combined['planets']:
        radius = radii.get((r['campaign'], r['star']))
        if radius is None or depths[r['campaign'], r['trial']] <= 1e6 * min(1., (.2009 / radius) ** 2):
            possible.append(r)
    assert len(possible) == 968
    reference = [r for r in combined['T156'] if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]
    assert len(reference) == 222
    metrics = {name: metric(rows, np) for name, rows in
               (('fixed1098', combined['planets']), ('possible968', possible), ('T156reference', reference))}
    assert round(metrics['fixed1098']['rates'][0][0] * 100, 2) == 48.11
    assert [sum(e['kind'] == arm for e in background[0]) for arm in ('real', 'flip')] == [174, 79]
    def same(a, b):
        return (a['campaign'], a['tic'], a['sector'], a['kind']) == (b['campaign'], b['tic'], b['sector'], b['kind']) and abs(a['center'] - b['center']) <= .1 + max(a['dur_h'], b['dur_h']) / 48
    b_hosts = set()
    for campaign in ('g2', 'g3'):
        for r in json.loads((H.OUT / f'inventory-{campaign}.json').read_text(encoding='utf-8')):
            if r['category'] == 'B':
                b_hosts.add((campaign, r['star']))
    counts = []
    for events in background:
        new = [e for e in events if (e['campaign'], e['tic']) in b_hosts and not any(same(e, old) for old in background[0])]
        nr, nf = [sum(e['kind'] == arm for e in new) for arm in ('real', 'flip')]
        counts.append(dict(real=sum(e['kind'] == 'real' for e in events), flip=sum(e['kind'] == 'flip' for e in events),
                           new_b_real=nr, new_b_flip=nf, control_d=nr <= 2.3 * nf + 5,
                           bins=dict(Counter(f"{e['campaign']}:{e['bin']}:{e['kind']}" for e in events))))
    out = dict(configs=CONFIGS, metrics=metrics, background=counts, bootstrap_seed=SEED, bootstrap_replicates=10000)
    (H.OUT / 'summary-m4.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    table = ['| Configuration | Fixed P % | Possible P % | T156 R % | Real | Upside-down | New B real / upside-down |',
             '|---|---:|---:|---:|---:|---:|---:|']
    for i, name in enumerate(CONFIGS):
        values = [f"{100 * metrics[key]['rates'][0][i]:.3f}" for key in ('fixed1098', 'possible968', 'T156reference')]
        b = counts[i]
        table.append(f"| {name} | {' | '.join(values)} | {b['real']} | {b['flip']} | {b['new_b_real']} / {b['new_b_flip']} |")
    (H.OUT / 'table.md').write_text('\n'.join(table) + '\n', encoding='utf-8')
    print('\n'.join(table))


if __name__ == '__main__':
    main()
