"""Count eligibility/no-op cases without displaying private identifiers."""
from collections import Counter
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('024_harness')


def main():
    guard = H.Guard()
    guard.start()
    all_counts = {}
    for campaign in ('g2', 'g3'):
        data = json.loads((H.OUT / f'generated-{campaign}/counts.json').read_text(encoding='utf-8'))
        counts = Counter()
        uncertain = []
        empty_statuses = Counter()
        empty_uncertain = []
        for row in data['coverage']:
            if row['status'] != 'unchanged':
                continue
            products = row.get('products', [])
            if not products:
                own_statuses = set()
                for kind in ('groups', 'groups_sap'):
                    path = (H.DATA / f'stage3_{campaign}' / f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
                            / kind / f"{row['star']}_{row['sector']}.json")
                    if path.exists():
                        guard.allow_design_file(path)
                        group = json.loads(path.read_text(encoding='utf-8'))
                        empty_statuses.update(str(m.get('status')) for m in group['meta'])
                        own_statuses.update(str(m.get('status')) for m in group['meta'])
                if 'too little data after masking' in own_statuses:
                    empty_uncertain.append([row['star'], row['sector']])
            if any(p['status'] in ('applied', 'insufficient_cycle_coverage') for p in products):
                uncertain.append([row['star'], row['sector']])
                counts['coverage_dependent_noop_sectors'] += 1
                for p in products:
                    counts[f"{p['status']}_bins_{p['bins']}"] += 1
            else:
                counts['span_dependent_noop_sectors'] += 1
        counts['changed_above_ten_days'] = sum(r['status'] == 'changed' and r['period'] >= 10 for r in data['coverage'])
        counts['empty_mask_dependent_noop_sectors'] = len(empty_uncertain)
        output = dict(counts=dict(counts), uncertain=uncertain, empty_trace_statuses=dict(empty_statuses),
                      empty_mask_uncertain=empty_uncertain)
        target = H.OUT / f'coverage-audit-{campaign}.json'
        if target.exists():
            previous = json.loads(target.read_text(encoding='utf-8'))
            assert previous['uncertain'] == uncertain
        target.write_text(json.dumps(output, indent=2), encoding='utf-8')
        all_counts[campaign] = dict(counts=counts, empty_trace_statuses=empty_statuses)
    print(json.dumps(all_counts, indent=2))


if __name__ == '__main__':
    main()
