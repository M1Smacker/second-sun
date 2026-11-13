"""Counts-only summary and star-cluster bootstrap of frozen-design results."""
import argparse
import json
from pathlib import Path
import numpy as np
ROOT=Path(r'D:\second-sun-astra'); OUT=ROOT/'data/astra/003'

def main(args):
    rows=[]
    for path in sorted((OUT/'workers').glob('*/results-*.jsonl')):
        for line in path.read_text(encoding='utf-8').splitlines(): rows.append(json.loads(line))
    assert len({r['trial'] for r in rows})==len(rows), 'Duplicate trial records'
    rows.sort(key=lambda r:r['trial'])
    if not rows: print('No completed paired trials'); return
    n=len(rows); ref=np.array([3000<=r['depth_ppm']<=6000 and 6<=r['duration_h']<=12 for r in rows])
    b=np.array([r['bin'] for r in rows]); dip=np.array([r['dip']['recovered'] for r in rows],int)
    bump=np.array([r['bump']['recovered'] for r in rows],int)
    stars=list(dict.fromkeys((r['campaign'],r['star']) for r in rows)); index={s:i for i,s in enumerate(stars)}
    counts=np.zeros((len(stars),5)); successes=counts.copy(); diffs=counts.copy(); allcounts=counts.copy()
    allsuccess=counts.copy(); bumpdiff=counts.copy()
    for i,r in enumerate(rows):
        s=index[r['campaign'],r['star']]; k=r['bin']; allcounts[s,k]+=1; allsuccess[s,k]+=dip[i]; bumpdiff[s,k]+=dip[i]-bump[i]
        if ref[i]: counts[s,k]+=1; successes[s,k]+=dip[i]; diffs[s,k]+=dip[i]-bump[i]
    rng=np.random.default_rng(2026111304); distribution=[]; perbin=[]; difference=[]; invalid=0
    usable=bool(np.all(counts.sum(axis=0)>0))
    for _ in range(50):
        w=rng.multinomial(len(stars),np.full(len(stars),1/len(stars)),size=200)
        d=w@counts; ok=(d>0).all(axis=1); invalid+=int((~ok).sum())
        if usable:
            rates=(w@successes)[ok]/d[ok]; distribution.extend(rates.mean(axis=1)); perbin.extend(rates)
        da=w@allcounts; valid=(da>0).all(axis=1)
        difference.extend(((w@bumpdiff)[valid]/da[valid]).tolist())
    # Keep resampling only to replace reference-empty bootstrap realizations, not to change the estimator.
    while usable and len(distribution)<10000:
        w=rng.multinomial(len(stars),np.full(len(stars),1/len(stars)),size=200)
        d=w@counts; ok=(d>0).all(axis=1); invalid+=int((~ok).sum())
        rates=(w@successes)[ok]/d[ok]; distribution.extend(rates.mean(axis=1)); perbin.extend(rates)
        if invalid>100000: raise RuntimeError('Too few reference clusters for stable resampling')
    pooled=float(np.mean(successes.sum(axis=0)/counts.sum(axis=0))) if usable else None
    ci=np.quantile(distribution[:10000],[.025,.975]).tolist() if usable else None
    decision=None if not usable else 'GO' if pooled>=.5 and ci[0]>=.4 else 'CHAIN BROKEN' if pooled<.2 else 'FIX FIRST'
    result=dict(paired_trials=n,distinct_stars=len(stars),reference_trials=int(ref.sum()),R=pooled,ci95=ci,decision=decision,
        invalid_bootstrap_realizations=invalid,full_band_dip_rate=float(dip.mean()),full_band_bump_rate=float(bump.mean()),
        trial_seconds=dict(mean=float(np.mean([r['seconds'] for r in rows])),median=float(np.median([r['seconds'] for r in rows])),
                           total=float(sum(r['seconds'] for r in rows))),bins=[],splits={},cells=[])
    for k in range(5):
        sel=b==k; sr=sel&ref
        item=dict(bin=k,n=int(sel.sum()),dip=int(dip[sel].sum()),bump=int(bump[sel].sum()),reference_n=int(sr.sum()),
                  reference_dip=int(dip[sr].sum()),reference_R=float(dip[sr].mean()) if sr.any() else None,
                  dip_only=int(((dip==1)&(bump==0)&sel).sum()),bump_only=int(((dip==0)&(bump==1)&sel).sum()))
        item['loss_counts_dip']=[sum(r['bin']==k and r['dip']['stage']==j and not r['dip']['recovered'] for r in rows) for j in range(5)]
        item['diagnostic_inconsistencies']=sum(r['bin']==k and r['dip']['diagnostic_inconsistency'] for r in rows)
        if len(difference): item['paired_difference_ci99']=np.quantile(np.asarray(difference)[:,k],[.005,.995]).tolist()
        result['bins'].append(item)
    def split(key):
        values={}
        for i,r in enumerate(rows):
            label=key(r); entry=values.setdefault(label,dict(n=0,dip=0,bump=0,reference_n=0,reference_dip=0))
            entry['n']+=1; entry['dip']+=int(dip[i]); entry['bump']+=int(bump[i]); entry['reference_n']+=int(ref[i]); entry['reference_dip']+=int(ref[i]*dip[i])
        return values
    result['splits']['product']=split(lambda r:r['product'])
    result['splits']['campaign']=split(lambda r:r['campaign'])
    result['splits']['era']=split(lambda r:'<56' if r['sector']<56 else '56-93' if r['sector']<94 else '>=94')
    result['splits']['brightness']=split(lambda r:'<11' if r['tmag']<11 else '11-12' if r['tmag']<12 else '12-14' if r['tmag']<14 else '>=14')
    de=[1000,2000,3000,6000,10000]; du=[3,6,12,18]
    for a in range(4):
        for c in range(3):
            sel=np.array([de[a]<=r['depth_ppm']<de[a+1] and du[c]<=r['duration_h']<du[c+1] for r in rows])
            result['cells'].append(dict(depth_bin=a,duration_bin=c,n=int(sel.sum()),dip=int(dip[sel].sum()),bump=int(bump[sel].sum())))
    inside=np.array([r['dip']['flags'][1] for r in rows])
    result['conditional_window_rate']=float(dip[inside].mean()) if inside.any() else None
    result['conditional_window_reference_rate']=float(dip[inside&ref].mean()) if (inside&ref).any() else None
    (OUT/f'{args.label}-summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--label',default='recovery'); main(p.parse_args())
