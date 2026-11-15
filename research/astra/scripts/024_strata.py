"""Descriptive recovery splits for brightness, product and observing era."""
from collections import defaultdict
import csv
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('024_harness')


def main():
    guard = H.Guard()
    guard.start()
    generator = importlib.import_module('024_generate')
    magnitudes = {}
    with H.TARGETS.open(encoding='utf-8-sig') as stream:
        for row in csv.DictReader(line for line in stream if not line.startswith('#')):
            if row['list'] in guard.seen and row['tic'] in guard.seen[row['list']]:
                magnitudes[row['list'], int(row['tic'])] = float(row['tmag'] or 'nan')
    product_map = {}
    original = {}
    for campaign in ('g2', 'g3'):
        guard.allow_machine_inputs(campaign)
        path = H.DATA / campaign / 'audit/best_per_star_sector.csv'
        with path.open(encoding='utf-8-sig') as stream:
            for row in csv.DictReader(stream):
                if row['tic'] in guard.seen[campaign]:
                    product_map[campaign, int(row['tic']), int(row['sector'])] = row['product']
        for bench, rows in generator.records(guard, campaign).items():
            for row in rows:
                original[bench, campaign, row['trial']] = row
    tables = []
    for bench in ('planets', 'T156'):
        rows = json.loads((H.OUT / f'combined-{bench}.json').read_text(encoding='utf-8'))
        if bench == 'T156':
            rows = [r for r in rows if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]
        groups = defaultdict(list)
        for row in rows:
            record = original[bench, row['campaign'], row['trial']]
            mag = magnitudes[row['campaign'], row['star']]
            brightness = 'under 11' if mag < 11 else '11 to 12' if mag < 12 else '12+' if mag == mag else 'unknown'
            sectors = [record['sector']] if bench == 'T156' else record['changed']
            products = {product_map.get((row['campaign'], row['star'], int(s)), 'unknown') for s in sectors}
            product = next(iter(products)) if len(products) == 1 else 'mixed'
            eras = {'1 to 26' if s <= 26 else '27 to 55' if s <= 55 else '56 to 93' if s <= 93 else '94+'
                    for s in map(int, sectors)}
            era = next(iter(eras)) if len(eras) == 1 else 'mixed'
            for dimension, label in (('campaign', row['campaign']), ('brightness', brightness), ('product', product), ('era', era)):
                groups[dimension, label].append(row)
        for (dimension, label), selected in sorted(groups.items()):
            tables.append(dict(bench=bench, dimension=dimension, label=label, n=len(selected),
                               real=[sum(bool(r['real'][j]) for r in selected) for j in range(4)],
                               flip=[sum(bool(r['flip'][j]) for r in selected) for j in range(4)]))
    (H.OUT / 'strata.json').write_text(json.dumps(tables, indent=2), encoding='utf-8')
    print('Descriptive subgroup tables', len(tables))


if __name__ == '__main__':
    main()
