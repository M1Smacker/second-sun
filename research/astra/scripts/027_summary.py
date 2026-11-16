"""Independent counts and paired whole-host bootstrap; never import the pipeline."""
from collections import Counter, defaultdict
import csv
import importlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('027_inputs')
H = D.H
NAMES = ('B', 'B+c1a', 'K2', 'K2+c1a')
SEED = 2026111523


def metric(rows, np):
    keys = sorted({(r['campaign'], r['star']) for r in rows})
    index = {k:i for i,k in enumerate(keys)}
    den = np.zeros((len(keys),5), dtype=int)
    hit = np.zeros((len(keys),5,2,4), dtype=int)
    moves = np.zeros((5,2,4,2), dtype=int)
    for r in rows:
        j,b = index[r['campaign'],r['star']], r['bin']
        den[j,b] += 1
        for arm,name in enumerate(('real','flip')):
            v = np.asarray(r[name], dtype=bool)
            base = v[[0,0,0,2]]
            hit[j,b,arm] += v
            moves[b,arm,:,0] += ~base & v
            moves[b,arm,:,1] += base & ~v
    n,k = den.sum(0), hit.sum(0)
    assert (n > 0).all()
    per = k/n[:,None,None]
    rng = np.random.default_rng(SEED)
    samples = []
    while len(samples)<10000:
        w = rng.multinomial(len(keys),np.full(len(keys),1/len(keys)),size=200)
        d = w @ den
        valid = (d>0).all(1)
        count = (w[valid] @ hit.reshape(len(keys),-1)).reshape(-1,5,2,4)
        samples.extend(count/d[valid,:,None,None])
    samples = np.asarray(samples[:10000])
    average = samples.mean(1)
    rate = per.mean(0)
    paired = np.quantile(samples[:,:,0]-samples[:,:,1],[.005,.995],axis=0)
    return dict(stars=len(keys), n=n.tolist(), counts=k.tolist(), per_bin=per.tolist(), rates=rate.tolist(),
        rate95=np.quantile(average,[.025,.975],axis=0).tolist(),
        change_B=(rate[0]-rate[0,0]).tolist(),
        change_B95=np.quantile(average[:,0]-average[:,0,[0]],[.025,.975],axis=0).tolist(),
        change_base=(rate[0]-rate[0,[0,0,0,2]]).tolist(),
        change_base95=np.quantile(average[:,0]-average[:,0,[0,0,0,2]],[.025,.975],axis=0).tolist(),
        paired99=paired.tolist(), paired_pass=((paired[0]<=0)&(paired[1]>=0)).all(0).tolist(), moves=moves.tolist())


def same(a,b):
    return (a['campaign'],a['tic'],a['sector'],a['kind']) == (b['campaign'],b['tic'],b['sector'],b['kind']) and abs(a['center']-b['center']) <= .1+max(a['dur_h'],b['dur_h'])/48


def main():
    guard = H.Guard()
    guard.start()
    import numpy as np
    combined, docs, backgrounds = {}, {}, [[] for _ in NAMES]
    for bench in ('planets','T156'):
        rows = {}
        for c in ('g2','g3'):
            for baseline in (True,False):
                doc = json.loads((H.OUT/f'{"baseline-" if baseline else ""}{bench}-{c}-V0.json').read_text(encoding='utf-8'))
                docs[bench,c,baseline] = doc
                inds = (0,2) if baseline else (1,3)
                for r in doc['rows']:
                    assert str(r['star']) in guard.seen[c]
                    out = rows.setdefault((c,r['trial']),dict(r,real=[None]*4,flip=[None]*4))
                    for arm in ('real','flip'):
                        for dest,source in zip(inds,(0,3)):
                            assert out[arm][dest] is None
                            out[arm][dest] = bool(r[arm][source])
                if bench=='planets':
                    for e in doc['background']:
                        assert str(e['tic']) in guard.seen[c]
                        for dest,source in zip(inds,(0,3)):
                            if e['options'][source]:
                                backgrounds[dest].append(e)
        combined[bench] = sorted(rows.values(),key=lambda r:(r['campaign'],r['trial']))
        assert len(rows)==(1098 if bench=='planets' else 2000)
        assert all(None not in r['real']+r['flip'] for r in rows.values())
        (H.OUT/f'combined-{bench}.json').write_text(json.dumps(combined[bench]),encoding='utf-8')
    radii,tmag = {},{}
    with (H.ROOT/'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['set'] not in guard.seen or r['tic'] not in guard.seen[r['set']]:
                continue
            try:
                v = float(r['radius_rsun'])
            except ValueError:
                continue
            if math.isfinite(v) and v>0:
                radii[r['set'],int(r['tic'])] = v
    with H.TARGETS.open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(line for line in f if not line.startswith('#')):
            if r['list'] in guard.seen and r['tic'] in guard.seen[r['list']]:
                try:
                    tmag[r['list'],int(r['tic'])] = float(r.get('tmag','nan'))
                except ValueError:
                    pass
    depths = {}
    for c in ('g2','g3'):
        for p in sorted((H.DATA/'astra/006').glob(f'planet-*-*-*-{c}/results.jsonl')):
            for line in D.read(guard,p,'006').splitlines():
                r=json.loads(line)
                assert str(r['star']) in guard.seen[c]
                depths[c,r['trial']]=r['depth_ppm']
    def possible(r,depth):
        v=radii.get((r['campaign'],r['star']))
        return v is None or depth<=1e6*min(1.,(.2009/v)**2)
    pp = [r for r in combined['planets'] if possible(r,depths[r['campaign'],r['trial']])]
    assert len(pp)==968
    ref = [r for r in combined['T156'] if 3000<=r['depth_ppm']<=6000 and 6<=r['duration_h']<=12]
    assert len(ref)==222
    populations = dict(fixed1098=combined['planets'],possible968=pp,T156all=combined['T156'],T156reference=ref,
        T156possible=[r for r in combined['T156'] if possible(r,r['depth_ppm'])],
        T156reference_possible=[r for r in ref if possible(r,r['depth_ppm'])])
    metrics = {name:metric(rows,np) for name,rows in populations.items()}
    assert round(metrics['fixed1098']['rates'][0][0]*100,3)==48.105
    assert round(metrics['T156reference']['rates'][0][0]*100,3)==34.207
    assert round(metrics['possible968']['rates'][0][2]*100,2)==51.02
    # Summary reads saved dump starts and catalogue columns only, never any fenced light.
    refs=json.loads(D.read(guard,H.OUT.with_name('014')/'dump-references.json','014'))
    dumps={int(s):np.asarray(r['starts']) for s,r in refs.items()}
    # Catalogue parser is a redirected copy, used for geometry only.
    import os
    os.environ.update(SS_SET='g2',VESPER_OPTS='c6,p1',NUMBA_NUM_THREADS='2')
    import petrova_mask as PM
    catalogues={c:{star:r for star,r in PM.load_catalogue(c,H.ROOT/f'targets/{c}_chain_targets.csv').items() if str(star) in guard.seen[c]} for c in ('g2','g3')}
    def screen(e):
        times=dumps.get(e['sector'],np.asarray([]))
        hours=float(24*(e['center']-times[np.argmin(abs(times-e['center']))])) if len(times) else None
        cat=catalogues[e['campaign']].get(e['tic'])
        distances=None
        if cat is not None and all(math.isfinite(cat[k]) for k in ('P','T0','wp')) and cat['wp']>0:
            phase=((e['center']-cat['T0'])/cat['P'])%1
            dist=lambda p:abs((phase-p+.5)%1-.5)*cat['P']
            secondary=math.isfinite(cat['phs']) and math.isfinite(cat['ws']) and cat['ws']>0
            distances=[dist(0)/cat['wp'],dist(cat['phs'] if secondary else .5)/(cat['ws'] if secondary else cat['wp'])]
        return dict(dump_hours=hours, eclipse_width_distances=distances,
            dump12h=hours is not None and (abs(hours)<=12 or abs(hours)<=e['dur_h']/2),
            eclipse=distances is not None and min(distances)<=1,
            unknown=hours is None or distances is None)
    bg,private,held = [],[],[]
    for i,events in enumerate(backgrounds):
        row=dict(real=sum(e['kind']=='real' for e in events),flip=sum(e['kind']=='flip' for e in events),
                 by_campaign_bin=dict(Counter(f"{e['campaign']}:{e['bin']}:{e['kind']}" for e in events)))
        for label,j in (('B',0),('base',0 if i<2 else 2)):
            new=[e for e in events if not any(same(e,old) for old in backgrounds[j])]
            nr,nf=[sum(e['kind']==arm for e in new) for arm in ('real','flip')]
            geometry=Counter()
            for e in new:
                if e['kind']=='real':
                    g=screen(e)
                    geometry.update(new=1,dump12h=int(g['dump12h']),eclipse=int(g['eclipse']),unknown=int(g['unknown']))
                    private.append(dict(e,configuration=NAMES[i],reference=label,geometry=g))
            row[label]=dict(new_real=nr,new_flip=nf,excess=nr-2.3*nf,pass_f1=nr-2.3*nf<=5,screen=dict(geometry))
        strata=Counter()
        for e in events:
            m=tmag.get((e['campaign'],e['tic']),math.nan)
            bright='unknown' if not math.isfinite(m) else ('<11','11-12','12-14','14+')[int(np.searchsorted([11,12,14],m,side='right'))]
            era=('1-26','27-55','56-93','94+')[int(np.searchsorted([27,56,94],e['sector'],side='right'))]
            for kind,value in (('brightness',bright),('product',e['product']),('era',era)):
                strata[kind+':'+value+':'+e['kind']]+=1
        row['strata']=dict(strata)
        bg.append(row)
        if i not in (1,3):
            continue
        for c in ('g2','g3'):
            old=docs['planets',c,True]['candidates']
            new=[e for e in docs['planets',c,False]['candidates'] if not any(same(e,o) for o in old)]
            for arm in ('real','flip'):
                subset=[e for e in new if e['kind']==arm]
                col=0 if i==1 else 3
                hcol=0 if i==1 else 1
                held2=[e for e in subset if not e['options'][col] and (e['holds'][hcol]['tier']=='2' or e['holds'][hcol]['cap'])]
                flags=Counter(f for e in held2 for f,v in e['holds'][hcol].items() if f!='tier' and v)
                held.append(dict(config=NAMES[i],campaign=c,arm=arm,new_candidates=len(subset),held_tier2=len(held2),
                    tier1=sum(e['options'][col] for e in subset),flags=dict(flags)))
    assert [bg[0]['real'],bg[0]['flip']]==[174,79]
    assert [bg[2]['real'],bg[2]['flip']]==[158,63]
    rules={}
    for i,base in ((1,0),(3,2)):
        p=metrics['possible968']
        rule=dict(a=p['change_base'][i]>=.02 and p['change_base95'][0][i]>0,
            b=bg[i]['flip']<=79 and bg[i]['real']<=174,
            c=metrics['fixed1098']['paired_pass'][i] and p['paired_pass'][i],
            d=metrics['T156reference']['rates'][0][i]>=metrics['T156reference']['rates'][0][base],
            e=bg[i]['B']['pass_f1'])
        rule['passes']=all(rule.values())
        rule['equal_alarm_eligible']=not rule['b'] and all(rule[k] for k in ('a','c','d','e'))
        rules[NAMES[i]]=rule
    summary=dict(configs=NAMES,metrics=metrics,background=bg,holds=held,rules=rules,bootstrap_seed=SEED,bootstrap_replicates=10000)
    (H.OUT/'new-real-events.json').write_text(json.dumps(private),encoding='utf-8')
    (H.OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(dict(rules=rules,background=[(r['real'],r['flip']) for r in bg],P=metrics['possible968']['rates'][0])))


if __name__=='__main__':
    main()
