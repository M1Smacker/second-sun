"""Paired whole-host bootstrap, independent of the search implementation."""
from collections import Counter
import csv
import json
import math
from pathlib import Path
import numpy as np

ROOT=Path(r'D:\second-sun-astra'); OUT=ROOT/'data/astra/028'
NAMES=('B','K2','B+A','B+A+B','K2+A','K2+A+B')
BASE=np.array([0,1,0,0,1,1])


def metric(rows):
    hosts=sorted({(r['campaign'],r['star']) for r in rows}); lookup={h:i for i,h in enumerate(hosts)}
    den=np.zeros((len(hosts),5),int); hit=np.zeros((len(hosts),5,2,6),int)
    moves=np.zeros((5,2,6,2),int)
    for r in rows:
        h,b=lookup[r['campaign'],r['star']],r['bin']; den[h,b]+=1
        for a,arm in enumerate(('real','flip')):
            v=np.asarray(r[arm],bool); hit[h,b,a]+=v
            moves[b,a,:,0]+=v&~v[BASE]; moves[b,a,:,1]+=~v&v[BASE]
    n=den.sum(0); counts=hit.sum(0); per=counts/n[:,None,None]; rates=per.mean(0)
    rng=np.random.default_rng(2026111523); samples=[]
    while len(samples)<10000:
        w=rng.multinomial(len(hosts),np.full(len(hosts),1/len(hosts)),size=200)
        d=w@den; ok=(d>0).all(1)
        c=(w[ok]@hit.reshape(len(hosts),-1)).reshape(-1,5,2,6)
        samples.extend(c/d[ok,:,None,None])
    s=np.asarray(samples[:10000]); avg=s.mean(1)
    control=np.quantile(s[:,:,0]-s[:,:,1],[.005,.995],axis=0)
    return dict(n=n.tolist(),hosts=len(hosts),counts=counts.tolist(),per_bin=per.tolist(),rates=rates.tolist(),
        rate95=np.quantile(avg,[.025,.975],axis=0).tolist(),
        gain=(rates[0]-rates[0,BASE]).tolist(),gain95=np.quantile(avg[:,0]-avg[:,0,BASE],[.025,.975],axis=0).tolist(),
        control99=control.tolist(),control_pass=((control[0]<=0)&(control[1]>=0)).all(0).tolist(),moves=moves.tolist())


def main():
    cal=json.loads((OUT/'calibration.json').read_text(encoding='utf-8'))
    radius={}
    magnitudes={}
    with (ROOT/'targets/r1_targets.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(line for line in f if not line.startswith('#')):
            if r['list'] not in ('g2','g3') or r['design_seen']!='1': continue
            try: value=float(r.get('tmag','nan'))
            except ValueError: value=math.nan
            magnitudes[r['list'],int(r['tic'])]=value
    with (ROOT/'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            try: v=float(r['radius_rsun'])
            except ValueError: continue
            if math.isfinite(v) and v>0: radius[r['set'],int(r['tic'])]=v
    combined={}
    for bench,total in (('planets',1098),('T156',2000)):
        rows=[r for c in ('g2','g3') for r in json.loads((OUT/f'{bench}-{c}.json').read_text(encoding='utf-8'))['rows']]
        assert len(rows)==len({(r['campaign'],r['trial']) for r in rows})==total
        combined[bench]=sorted(rows,key=lambda r:(r['campaign'],r['trial']))
        (OUT/f'combined-{bench}.json').write_text(json.dumps(combined[bench]),encoding='utf-8')
    def possible(r):
        v=radius.get((r['campaign'],r['star']))
        return v is None or r['depth_ppm']<=1e6*min(1.,(.2009/v)**2)
    pp=[r for r in combined['planets'] if possible(r)]; assert len(pp)==968
    ref=[r for r in combined['T156'] if 3000<=r['depth_ppm']<=6000 and 6<=r['duration_h']<=12]; assert len(ref)==222
    metrics={k:metric(v) for k,v in [('fixed1098',combined['planets']),('possible968',pp),('T156reference',ref),('T156all',combined['T156'])]}
    assert round(100*metrics['fixed1098']['rates'][0][0],3)==48.105
    assert round(100*metrics['possible968']['rates'][0][1],2)==51.02
    assert round(100*metrics['T156reference']['rates'][0][0],3)==34.207
    # Every searched null set falls below the chosen floor. No assumptions about
    # the underlying event rate are substituted for this explicit recount.
    null=[r for c in ('g2','g3') for r in json.loads((OUT/f'null-{c}.json').read_text(encoding='utf-8'))['rows']]
    qualifying=[s for r in null for s in r['sets'] if s['score']>=cal['floor']]
    assert not qualifying
    backgrounds=[]
    docs=[json.loads((OUT.with_name('027')/f'baseline-planets-{c}-V0.json').read_text(encoding='utf-8')) for c in ('g2','g3')]
    for i,name in enumerate(NAMES):
        col=0 if BASE[i]==0 else 3
        counts=Counter(e['kind'] for d in docs for e in d['background'] if e['options'][col])
        strata=Counter((e['campaign'],e['kind'],e['bin']) for d in docs for e in d['background'] if e['options'][col])
        other=Counter()
        for doc in docs:
            for e in doc['background']:
                if not e['options'][col]: continue
                mag=magnitudes.get((e['campaign'],e['tic']),math.nan)
                brightness='unknown' if not math.isfinite(mag) else ('<11','11-12','12-14','14+')[int(np.searchsorted([11,12,14],mag,side='right'))]
                era=('1-26','27-55','56-93','94+')[int(np.searchsorted([27,56,94],e['sector'],side='right'))]
                for category,value in (('brightness',brightness),('era',era),('product',e['product'])):
                    other[category+':'+value+':'+e['kind']]+=1
        backgrounds.append(dict(config=name,real=counts['real'],flip=counts['flip'],new_A_real=0,new_A_flip=0,
            new_B_real=0,new_B_flip=0,new_real=0,new_flip=0,rule4=0.,blindspots_required=0,
            strata=dict(other),
            period_campaign_counts=[dict(campaign=c,arm=a,bin=b,n=n) for (c,a,b),n in sorted(strata.items())]))
    rules={}
    p=metrics['possible968']; t=metrics['T156reference']
    for i in range(2,6):
        base=int(BASE[i]); bg=backgrounds[i]
        rules[NAMES[i]]=dict(a=p['gain'][i]>=.01 and p['gain95'][0][i]>0,
            b=bg['real']<=174 and bg['flip']<=backgrounds[base]['flip'],
            c=all(metrics[m]['control_pass'][i] for m in ('fixed1098','possible968')),
            d=t['rates'][0][i]>=t['rates'][0][base],e=bg['rule4']<=5)
        rules[NAMES[i]]['passes']=all(rules[NAMES[i]].values())
    summary=dict(configs=NAMES,metrics=metrics,background=backgrounds,rules=rules,calibration=cal,
        fresh_required=any(r['passes'] for r in rules.values()),bootstrap_seed=2026111523,replicates=10000)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (OUT/'new-real-events.json').write_text('[]',encoding='utf-8')
    print(json.dumps(dict(rules=rules,P=p['rates'][0],R=t['rates'][0])))


if __name__=='__main__': main()
