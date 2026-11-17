"""Fix the floor from both complete null campaigns before planet orbit scores."""
import json
from pathlib import Path
OUT=Path(r'D:\second-sun-astra\data/astra/028')


def main():
    rows=[r for c in ('g2','g3') for r in json.loads((OUT/f'null-{c}.json').read_text(encoding='utf-8'))['rows']]
    assert len({(r['campaign'],r['star'],r['arm']) for r in rows})==len(rows)
    maximum=max(r['max_score'] for r in rows)
    summary=dict(floor=max(7.,maximum+1),max_null=maximum,host_arms=len(rows),
        sets=sum(len(r['sets']) for r in rows),mutation_sets=sum(r['mutant_sets'] for r in rows),
        templates=sum(r['templates'] for r in rows),missing_geometry_host_arms=sum(not r['geometry_valid'] for r in rows),strata=[])
    for c in ('g2','g3'):
        for arm in ('real','flip'):
            for b in range(5):
                sub=[r for r in rows if (r['campaign'],r['arm'],r['bin'])==(c,arm,b)]
                summary['strata'].append(dict(campaign=c,arm=arm,bin=b,hosts=len(sub),
                    sets=sum(len(r['sets']) for r in sub),hosts_with_set=sum(bool(r['sets']) for r in sub),
                    best=max((r['max_score'] for r in sub),default=0)))
    summary['mutation_sensitive']=summary['mutation_sets']!=summary['sets']
    p=OUT/'calibration.json'
    if p.exists(): assert json.loads(p.read_text(encoding='utf-8'))==summary, 'Frozen calibration changed'
    else: p.write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='strata'}))


if __name__=='__main__': main()
