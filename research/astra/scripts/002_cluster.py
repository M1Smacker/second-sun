"""Anonymous star-cluster percentile bootstrap. No pipeline imports."""
import csv
import json
from pathlib import Path
import numpy as np

ROOT = Path(r'D:\second-sun-astra')

def main():
    rng = np.random.default_rng(2026111301)
    output = {}
    for campaign, target in [('g3', (311, 1152, 6)), ('g2', (446, 2381, 13))]:
        path = ROOT / f'research/astra/inbox/002-s2-cluster-table-{campaign}.csv'
        with path.open(encoding='utf-8-sig') as stream:
            rows = list(csv.DictReader(x for x in stream if not x.startswith('#')))
        exposure, flips, stars = (np.array([int(r[k]) for r in rows]) for k in ('exposure','flips','stars'))
        totals = (int(stars.sum()), int(stars @ exposure), int(stars @ flips))
        assert totals == target
        # Multinomial counts resample whole stars, preserving exposure/flip pairs.
        batches = []
        for _ in range(100):
            weights = rng.multinomial(totals[0], stars / stars.sum(), size=1000)
            batches.append(1000 * (weights @ flips) / (weights @ exposure))
        samples = np.concatenate(batches)
        output[campaign] = dict(stars=totals[0], exposure=totals[1], flips=totals[2],
            positive_stars=int(stars[flips>0].sum()), rate=1000*totals[2]/totals[1],
            percentile95=np.quantile(samples,[.025,.975]).tolist(),
            zero_fraction=float(np.mean(samples==0)), draws=len(samples))
    print(json.dumps(output, indent=2))
    (ROOT/'data/astra/002/cluster.json').write_text(json.dumps(output,indent=2),encoding='utf-8')

if __name__ == '__main__':
    main()
