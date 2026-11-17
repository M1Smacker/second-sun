"""Recount archived baselines and inventory captures without using planted scores."""
from collections import Counter
import csv
import importlib
import json
import math
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
D=importlib.import_module('028_inputs')
H=D.H


def main():
    guard=H.Guard(); guard.start()
    result={}
    for bench in ('planets','T156'):
        docs=[json.loads(D.read(guard,H.OUT.with_name('027')/f'baseline-{bench}-{c}-V0.json','027')) for c in ('g2','g3')]
        rows=[r for doc in docs for r in doc['rows']]
        assert len(rows)==(1098 if bench=='planets' else 2000)
        assert all(str(r['star']) in guard.seen[r['campaign']] for r in rows)
        sample=rows if bench=='planets' else [r for r in rows if 3000<=r['depth_ppm']<=6000 and 6<=r['duration_h']<=12]
        rate=lambda col: sum(sum(r['real'][col] for r in sample if r['bin']==b)/sum(r['bin']==b for r in sample) for b in range(5))/5
        result[bench]=dict(n=len(sample),B=rate(0),K2=rate(3))
        assert round(100*rate(0),3)==(48.105 if bench=='planets' else 34.207)
        if bench=='planets':
            result['background']={name:[sum(e['kind']==arm and e['options'][i] for doc in docs for e in doc['background']) for arm in ('real','flip')] for name,i in (('B',0),('K2',3))}
            assert result['background']=={'B':[174,79],'K2':[158,63]}
    # Count available capture centres; never summarize amplitudes before calibration.
    refs={}
    for c in ('g2','g3'):
        p=H.OUT.with_name('027')/f'baseline-planets-{c}-V0.json'
        refs.update({(c,r['trial']):r for r in json.loads(D.read(guard,p,'027'))['rows']})
    bins=[Counter() for _ in range(5)]
    seen=set()
    radii={}
    with (H.ROOT/'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            if row['set'] not in guard.seen or row['tic'] not in guard.seen[row['set']]: continue
            try: radius=float(row['radius_rsun'])
            except ValueError: continue
            if math.isfinite(radius) and radius>0: radii[row['set'],int(row['tic'])]=radius
    possible=[]
    for c in ('g2','g3'):
        for journal in sorted(H.OUT.with_name('006').glob(f'planet-*-*-*-{c}/results.jsonl')):
            for line in D.read(guard,journal,'006').splitlines():
                r=json.loads(line); key=(c,r['trial'])
                assert str(r['star']) in guard.seen[c]
                if key not in refs: continue
                assert key not in seen; seen.add(key)
                radius=radii.get((c,r['star']))
                if radius is None or r['depth_ppm']<=1e6*min(1.,(.2009/radius)**2): possible.append(refs[key])
                sc=journal.parent/f'trial-{r["trial"]}/scores.json'
                b=bins[r['bin']]; b['total']+=1
                if not sc.is_file(): b['missing_capture']+=1; continue
                values=json.loads(D.read(guard,sc,'006'))
                centres={round(row[3],8) for row in values['1'] if row[1]==1 and row[2]==r['trial']}
                b['captured']+=1; b['three_scored']+=len(centres)>=3
                for name,col in (('B',0),('K2',3)):
                    missed=not refs[key]['real'][col]
                    b[name+'_missed']+=missed
                    b[name+'_missed_three_scored']+=missed and len(centres)>=3
                    found=bool(refs[key].get('real_found'))
                    b[name+'_detected_missed']+=missed and found
                    b[name+'_detected_missed_three_scored']+=missed and found and len(centres)>=3
    assert len(seen)==1098
    assert len(possible)==968
    possible_rate=lambda col: sum(sum(r['real'][col] for r in possible if r['bin']==b)/sum(r['bin']==b for r in possible) for b in range(5))/5
    result['possible968']=dict(B=possible_rate(0),K2=possible_rate(3))
    assert round(result['possible968']['K2']*100,2)==51.02
    result['capture_coverage_by_bin']=[dict(b) for b in bins]
    (H.OUT/'inventory.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__': main()
