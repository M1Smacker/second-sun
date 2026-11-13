"""Freeze catalogue/file-name-only draws before any recovery numbers."""
import csv
import hashlib
import json
import random
from pathlib import Path
ROOT=Path(r'D:\second-sun-astra'); OUT=ROOT/'data/astra/003'
SEED=2026111303
def main():
    with (ROOT/'targets/r1_targets.csv').open(encoding='utf-8') as f:
        rows=list(csv.DictReader(x for x in f if not x.startswith('#')))
    targets={}
    for r in rows:
        if r['list'] in ('g2','g3') and r['design_seen']=='1': targets.setdefault((r['list'],r['tic']),r)
    bins=[[] for _ in range(5)]; edges=[5,10,14,20,27.4,float('inf')]
    for name in ('g2','g3'):
        folder=ROOT/'data'/f'stage3_{name}'/f'r1dev_{name}_seen_bcd29c7aabb0'/'groups'
        for p in sorted(folder.glob('*.json')):
            star,sector=p.stem.split('_'); row=targets.get((name,star))
            if row is None: continue
            period=float(row['p_bin_d'])
            b=next(i for i in range(5) if edges[i]<=period<edges[i+1])
            bins[b].append(dict(campaign=name,star=int(star),sector=int(sector),period=period,tmag=float(row['tmag'])))
    rng=random.Random(SEED); trials=[]
    for repeat in range(400):
        for b in range(5):
            group=rng.choice(bins[b])
            trials.append(dict(**group,trial=len(trials),bin=b,phase_fraction=rng.random(),
                depth_ppm=1000*10**rng.random(),duration_h=3*6**rng.random()))
    payload=json.dumps(dict(seed=SEED,pool_counts=list(map(len,bins)),trials=trials),indent=2)
    path=OUT/'design.json'
    if path.exists(): assert path.read_text(encoding='utf-8')==payload, 'Do not overwrite a different design'
    else: path.write_text(payload,encoding='utf-8')
    print('Pool groups by bin:',list(map(len,bins)),'planned paired trials:',len(trials),'design SHA256:',hashlib.sha256(payload.encode()).hexdigest())
if __name__=='__main__': main()
