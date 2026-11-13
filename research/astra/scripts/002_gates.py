"""Count filed gate coverage and design-seen G3 metadata losses only."""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')

def main():
    gates = {}
    for path in sorted((ROOT/'research/stage3').glob('R1-GATE-RESULT-*.txt')):
        content = path.read_text(encoding='utf-8')
        gates[path.name] = dict(missing_injection_bins=content.count('d: no injections'),
            undefined_ratios=content.count('n/a (nothing found'),
            coverage_passes=re.findall(r'\(([ab])\) PASS',content),
            outside_bins=len(re.findall(r': OUTSIDE',content)))
    with (ROOT/'targets/r1_targets.csv').open(encoding='utf-8-sig') as stream:
        rows = list(csv.DictReader(x for x in stream if not x.startswith('#')))
    allowed = {r['tic']:r for r in rows if r['list']=='g3' and r['design_seen']=='1'}
    counts = {key:Counter() for key in ('status','brightness','product','sector','period','era')}
    groups = files = lost_groups = 0
    root = ROOT/'data/stage3_g3/r1dev_g3_seen_bcd29c7aabb0/groups'
    for path in sorted(root.glob('*.json')):
        star = path.stem.split('_')[0]
        if star not in allowed:
            continue
        # Only design-seen groups are opened; event fields are never inspected.
        meta = json.loads(path.read_text(encoding='utf-8'))['meta']
        groups += 1
        if meta and all(m.get('status')=='no safe windows' for m in meta):
            lost_groups += 1
        row = allowed[star]
        def number(keys):
            for key in keys:
                try:
                    return float(row[key])
                except (KeyError, ValueError):
                    pass
            return float('nan')
        mag = number(('tmag','Tmag'))
        period = number(('p_bin_d',))
        brightness = '<11' if mag<11 else '11-12' if mag<12 else '12-14' if mag<14 else '>=14' if mag==mag else 'unknown'
        pbin = next((f'{lo}-{hi}' for lo,hi in zip([5,10,14,20,27.4],[10,14,20,27.4,float('inf')]) if lo<=period<hi),'unknown')
        for m in meta:
            files += 1
            status = m.get('status','missing')
            sector = int(m.get('sector',path.stem.split('_')[1]))
            counts['status'][status] += 1
            labels = dict(brightness=brightness,product=m.get('product','unknown'),sector=str(sector),period=pbin,
                          era='<56' if sector<56 else '56-93' if sector<94 else '>=94')
            for key,label in labels.items():
                counts[key][label+'|total'] += 1
                if status=='no safe windows':
                    counts[key][label+'|no_safe_windows'] += 1
    result = dict(gates=gates,groups=groups,files=files,groups_all_no_safe_windows=lost_groups,
                  counts={k:dict(sorted(v.items())) for k,v in counts.items()})
    (ROOT/'data/astra/002/gates.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    sector_counts = result['counts']['sector']
    sector_rows = [(int(k.split('|')[0]),v,sector_counts.get(k.split('|')[0]+'|no_safe_windows',0))
                   for k,v in sector_counts.items() if k.endswith('|total')]
    assert sum(x[1] for x in sector_rows)==files
    assert sum(x[2] for x in sector_rows)==counts['status']['no safe windows']
    table = '# Part E: G3 design-seen file losses by sector\n\nStored development metadata only. Files are not independent stars or exposure time.\n\n| Sector | Files | No safe windows |\n|---:|---:|---:|\n'
    table += ''.join('| %s | %s | %s |\n' % x for x in sorted(sector_rows))
    (ROOT/'research/astra/reports/002-g3-sector-losses.md').write_text(table,encoding='utf-8')
    print(json.dumps({**result,'counts':{k:v for k,v in result['counts'].items() if k!='sector'}},indent=2))

if __name__=='__main__':
    main()
