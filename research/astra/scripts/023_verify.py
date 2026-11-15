"""Recount aggregate outputs by direct trial iteration, without pipeline imports."""
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('023_inputs')
H = D.H
O = importlib.import_module('023_outputs')


def main():
    guard = H.Guard()
    guard.start()
    summary = json.loads((H.OUT / 'summary.json').read_text(encoding='utf-8'))
    checks = []
    for bench in ('planets', 'T156'):
        rows = json.loads((H.OUT / f'combined-{bench}.json').read_text(encoding='utf-8'))
        if bench == 'planets':
            assert len(rows) == 1098
        else:
            assert len(rows) == 2000
        selections = [(bench, rows)]
        if bench == 'T156':
            selections.append(('reference', [r for r in rows if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]))
        for label, selected in selections:
            assert all(str(r['star']) in guard.seen[r['campaign']] for r in selected)
            metric = summary[label]
            bins = [[r for r in selected if r['bin'] == b] for b in range(5)]
            assert [len(group) for group in bins] == metric['n']
            for i in range(8):
                for a, arm in enumerate(('real', 'flip')):
                    rate = sum(sum(r[arm][i] for r in group) / len(group) for group in bins) / 5
                    assert abs(rate - metric['rates'][a][i]) < 1e-12
                    for b, group in enumerate(bins):
                        gained = sum(not r[arm][0] and r[arm][i] for r in group)
                        lost = sum(r[arm][0] and not r[arm][i] for r in group)
                        assert [gained, lost] == metric['moves'][b][a][i]
                if label == 'planets':
                    failed = [b for b in range(5) if metric['paired99'][b][i][0] > 0 or metric['paired99'][b][i][1] < 0]
                    assert failed == summary['configurations'][i]['failed_control_bins']
            checks.append(f'{label} denominator, rates, transitions and design membership')
    # The cap can only remove qualifying events. Planet detection excludes pre-existing events,
    # so its recovery metric need not be monotone when a baseline event itself is capped.
    for campaign in ('g2', 'g3'):
        base = json.loads((H.OUT / f'planets-{campaign}-V0.json').read_text(encoding='utf-8'))
        for event in base['background']:
            assert not event['options'][1] or event['options'][0]
            assert not event['options'][3] or event['options'][2]
        old = json.loads(D.read(guard, H.OUT.with_name('013') / f'planets-{campaign}.json', '013'))
        old_rows = {r['trial']: r for r in old['rows']}
        for row in base['rows']:
            for arm in ('real', 'flip'):
                assert [row[arm][0], row[arm][2]] == old_rows[row['trial']][arm][1:3]
    checks.append('full planet B and DS trial-wise historical identity')
    # Independently check vectorized resampling against explicit star multiplicities.
    import numpy as np
    rows = json.loads((H.OUT / 'combined-planets.json').read_text(encoding='utf-8'))
    keys = sorted({(r['campaign'], r['star']) for r in rows})
    by_star = {key: [r for r in rows if (r['campaign'], r['star']) == key] for key in keys}
    rng = np.random.default_rng(summary['bootstrap_seed'])
    weights = rng.multinomial(len(keys), np.full(len(keys), 1 / len(keys)), size=200)
    n = np.array([[sum(r['bin'] == b for r in by_star[key]) for b in range(5)] for key in keys])
    hit = np.array([[[sum(r['bin'] == b and r['real'][i] for r in by_star[key]) for i in range(8)]
                     for b in range(5)] for key in keys])
    for w in weights[:3]:
        den = w @ n
        vector = (w @ hit.reshape(len(keys), -1)).reshape(5, 8) / den[:, None]
        for b in range(5):
            for i in range(8):
                numerator = sum(int(weight) * sum(r['bin'] == b and r['real'][i] for r in by_star[key])
                                for key, weight in zip(keys, w))
                assert abs(vector[b, i] - numerator / den[b]) < 1e-12
    checks.append('three explicit whole-star resamples agree with vectorized aggregation')
    paths = list((H.ROOT / 'research/astra/scripts').glob('023_*.py'))
    paths += list((H.ROOT / 'research/astra/scripts/harness/sprint023').glob('*.py'))
    fingerprints = {str(p.relative_to(H.ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    O.write_json(H.OUT / 'verification.json', dict(checks=checks, source_sha256=fingerprints), indent=2)
    print(len(checks), 'aggregate and identity checks completed, three bootstrap draws independently recounted')


if __name__ == '__main__':
    main()
