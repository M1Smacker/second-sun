"""Counts-only comparison of saved, parity-checked replays."""
import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

OUT = Path(r'D:\second-sun-astra\data\astra\005')


def summarize(variant):
    results = [json.loads((OUT / f'{variant}-{c}.json').read_text(encoding='utf-8')) for c in ('g2', 'g3')]
    rows = sorted((r for result in results for r in result['trials']), key=lambda r: r['trial'])
    assert [r['trial'] for r in rows] == list(range(2000))
    keys = list(dict.fromkeys((r['campaign'], r['star']) for r in rows))
    index = {key: i for i, key in enumerate(keys)}
    all_n = np.zeros((len(keys), 5), dtype=int)
    ref_n = np.zeros_like(all_n)
    ref_dip = np.zeros((*all_n.shape, 2), dtype=int)
    diffs = np.zeros_like(ref_dip)
    bins = [dict(ref_n=0, dip=[0, 0], bump=[0, 0], ref_dip=[0, 0], ref_bump=[0, 0],
                 dip_gain=0, dip_loss=0, bump_gain=0, bump_loss=0, ref_dip_gain=0, ref_dip_loss=0,
                 ref_bump_gain=0, ref_bump_loss=0) for _ in range(5)]
    for row in rows:
        k = row['bin']
        i = index[row['campaign'], row['star']]
        ref = 3000 <= row['depth_ppm'] <= 6000 and 6 <= row['duration_h'] <= 12
        all_n[i, k] += 1
        diffs[i, k] += np.subtract(row['dip'], row['bump'], dtype=int)
        if ref:
            ref_n[i, k] += 1
            ref_dip[i, k] += row['dip']
            bins[k]['ref_n'] += 1
        for arm in ('dip', 'bump'):
            old, new = row[arm]
            for prefix in ('', 'ref_') if ref else ('',):
                b = bins[k]
                b[prefix + arm][0] += old
                b[prefix + arm][1] += new
                b[prefix + arm + '_gain'] += new and not old
                b[prefix + arm + '_loss'] += old and not new
    assert np.all(all_n.sum(axis=0) == 400)
    rng = np.random.default_rng(2026111304)
    ref_draws, diff_draws = [], []
    for _ in range(50):
        weights = rng.multinomial(len(keys), np.full(len(keys), 1 / len(keys)), size=200)
        ref_den = weights @ ref_n
        all_den = weights @ all_n
        assert (ref_den > 0).all() and (all_den > 0).all()
        ref_draws.extend(np.stack([weights @ ref_dip[:, :, j] / ref_den for j in range(2)], axis=2))
        diff_draws.extend(np.stack([weights @ diffs[:, :, j] / all_den for j in range(2)], axis=2))
    ref_draws = np.asarray(ref_draws)
    interval = np.quantile(ref_draws.mean(axis=1), [.025, .975], axis=0)
    bin_ci = np.quantile(ref_draws, [.025, .975], axis=0)
    paired = np.quantile(diff_draws, [.005, .995], axis=0)
    for k, b in enumerate(bins):
        b['ref_ci95'] = bin_ci[:, k].T.tolist()
        b['paired_ci99'] = paired[:, k].T.tolist()
    rates = (ref_dip.sum(axis=0) / ref_n.sum(axis=0)[:, None]).mean(axis=0)
    stored = json.loads((OUT.with_name('003') / 'recovery-summary.json').read_text(encoding='utf-8'))
    assert abs(rates[0] - stored['R']) < 1e-14
    assert np.allclose(interval[:, 0], stored['ci95'], rtol=0, atol=1e-14)
    old, new = Counter(), Counter()
    check = Counter()
    for result in results:
        old.update(result['background_old'])
        new.update(result['background_new'])
        check.update(result['check'])
    cap = old['flip'] + 2 * math.sqrt(old['flip'] + 1)
    verdict = [bool(rates[1] > rates[0] if variant == 'both' else rates[1] >= rates[0]),
               new['flip'] <= cap,
               bool((paired[0, :, 1] <= 0).all() and (paired[1, :, 1] >= 0).all())]
    result = dict(variant=variant, R=rates.tolist(), ci95=interval.T.tolist(), background_old=old,
                  background_new=new, flip_cap=cap, pass_conditions=verdict, check=check, bins=bins)
    (OUT / f'{variant}-summary.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('variant', choices=['both'])
    summarize(parser.parse_args().variant)
