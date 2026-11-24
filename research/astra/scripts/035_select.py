"""Select catalogue metadata only; never opens light or event files."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'data/astra/035'


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(line for line in f if not line.startswith('#')))


def main():
    print('ROOT', ROOT, 'WRITE', OUT)
    sources = [ROOT/'targets/r1_targets.csv', ROOT/'targets/g1_targets.csv',
               ROOT/'data/census_union/eb_union.csv']
    r1, g1, union = map(rows, sources)
    blocked_a = {int(r['tic']) for r in r1 if r['list'] == 'g1'}
    blocked_a.update(int(r['tic']) for r in g1)
    blocked_b = {int(r['tic']) for r in r1
                 if r['list'] in ('g2', 'g3') and r['design_seen'] == '0'}
    bins = [{}, {}, {}]
    for r in union:
        try:
            star, p, mag = int(r['tic']), float(r['p_bin_d']), float(r['tmag'])
        except (ValueError, TypeError):
            continue
        if (r['source'] not in ('prsa2022', 'ttc_t3') or not 1 <= p <= 30 or
                not mag <= 13.5 or star in blocked_a | blocked_b):
            continue
        b = int(np.searchsorted([5, 10], p, side='right'))
        if star in bins[b] and bins[b][star] != r:
            raise RuntimeError('Conflicting duplicate catalogue rows')
        bins[b][star] = r
    rng = np.random.default_rng(2026112501)
    shuffled = [list(map(int, rng.permutation(sorted(b)))) for b in bins]
    chosen = [b[:50] for b in shuffled]
    # Prespecified equal allocation, round-robin shortfall redistribution.
    while sum(map(len, chosen)) < 150:
        added = False
        for i in range(3):
            if len(chosen[i]) < len(shuffled[i]) and sum(map(len, chosen)) < 150:
                chosen[i].append(shuffled[i][len(chosen[i])])
                added = True
        if not added:
            break
    selected = [dict(bins[b][s], band=b) for b in range(3) for s in chosen[b]]
    ids = {int(r['tic']) for r in selected}
    assert len(ids) == len(selected) and not ids & (blocked_a | blocked_b)
    sample = dict(seed=2026112501, band_edges=[1, 5, 10, 30],
                  eligible=[len(b) for b in bins], selected=selected,
                  selected_bins=list(map(len, chosen)), fence_a_overlap=0, fence_b_overlap=0,
                  source_hashes={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sources})
    output = OUT/'sample.json'
    serialized = json.dumps(sample, indent=2, sort_keys=True)
    if output.exists() and output.read_text(encoding='utf-8') != serialized:
        raise RuntimeError('Existing sample differs; no replacement authorized')
    output.write_text(serialized, encoding='utf-8')
    print(json.dumps({k: sample[k] for k in ('eligible', 'selected_bins',
                                           'fence_a_overlap', 'fence_b_overlap')}))


if __name__ == '__main__':
    main()
