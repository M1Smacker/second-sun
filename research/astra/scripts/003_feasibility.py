"""Count design-only multi-sector availability using stored group filenames, not events."""
import csv
import json
from collections import defaultdict
from pathlib import Path
ROOT=Path(r'D:\second-sun-astra')
seen=defaultdict(set)
with (ROOT/'targets/r1_targets.csv').open(encoding='utf-8') as f:
    for r in csv.DictReader(x for x in f if not x.startswith('#')):
        if r['design_seen']=='1' and r['list'] in ('g2','g3'): seen[r['list']].add(r['tic'])
result={}; total=defaultdict(set)
for name,allowed in seen.items():
    groups=defaultdict(set)
    candidates=list((ROOT/'data'/f'stage3_{name}').glob(f'r1dev_{name}_seen_*/groups'))
    assert len(candidates)==1
    for p in candidates[0].glob('*.json'):
        star,sector=p.stem.split('_')
        if star in allowed: groups[star].add(int(sector)); total[star].add(int(sector))
    result[name]=dict(allowed_stars=len(allowed),with_groups=len(groups),multi_sector=sum(len(v)>=2 for v in groups.values()),
        sectors_ge_5=sum(len(v)>=5 for v in groups.values()),groups=sum(map(len,groups.values())))
result['unique_across_campaigns']=dict(with_groups=len(total),multi_sector=sum(len(v)>=2 for v in total.values()))
(ROOT/'data/astra/003/feasibility.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
