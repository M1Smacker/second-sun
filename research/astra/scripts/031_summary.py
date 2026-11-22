"""Counts-only paired whole-star analysis. No pipeline imports or tuning."""
from collections import Counter
import csv
import json
import math
from pathlib import Path
import statistics

ROOT=Path(r'D:\second-sun-astra')
OUT=ROOT/'data/astra/031'
PHASES=('choosing','fresh_old','T156_old','fresh_new','T156_new')
VERSIONS=('B','N1','D1')
SEED=2026112230


def metric(rows, bootstrap=False):
    import numpy as np
    present=sorted({r['bin'] for r in rows})
    if not present:
        return dict(n=0,missing_bins=list(range(5)))
    hosts=sorted({r['star'] for r in rows})
    index={star:i for i,star in enumerate(hosts)}
    den=np.zeros((len(hosts),len(present)),int)
    hits=np.zeros((len(hosts),len(present),6),int)
    for r in rows:
        i,b=index[r['star']],present.index(r['bin'])
        den[i,b]+=1
        hits[i,b]+=[r[v][arm][0] for v in VERSIONS for arm in ('real','flip')]
    n=den.sum(0)
    rates=hits.sum(0)/n[:,None]
    result=dict(n=len(rows),hosts=len(hosts),bins=present,missing_bins=[b for b in range(5) if b not in present],
                n_by_bin=n.tolist(),counts_by_bin=hits.sum(0).tolist(),rates_by_bin=rates.tolist(),rates=rates.mean(0).tolist())
    result['crossings']={v:dict(total=sum(r[v]['n_crossings'] for r in rows),
                               real=sum(len(r[v]['real_crossings']) for r in rows),
                               flip=sum(len(r[v]['flip_crossings']) for r in rows)) for v in VERSIONS}
    if bootstrap:
        assert present==list(range(5)), 'Judging population has an empty period bin'
        rng=np.random.default_rng(SEED)
        draws=[]
        while len(draws)<10000:
            weights=rng.multinomial(len(hosts),np.full(len(hosts),1/len(hosts)),size=200)
            denom=weights@den
            valid=(denom>0).all(1)
            numer=(weights[valid]@hits.reshape(len(hosts),-1)).reshape(-1,5,6)
            draws.extend(numer/denom[valid,:,None])
        draws=np.asarray(draws[:10000])
        pooled=draws.mean(1)
        result.update(rate95=np.quantile(pooled,[.025,.975],axis=0).tolist(),
                      gain=float((rates[:,4]-rates[:,0]).mean()),
                      gain95=np.quantile(pooled[:,4]-pooled[:,0],[.025,.975]).tolist(),
                      control99=np.quantile(draws[:,:,4]-draws[:,:,5],[.005,.995],axis=0).tolist())
        lo,hi=result['control99']
        result['control_pass']=all(a<=0<=b for a,b in zip(lo,hi))
    return result


def same(a,b):
    return all(a[k]==b[k] for k in ('campaign','tic','sector','kind')) and abs(a['center']-b['center']) <= .1+max(a['dur_h'],b['dur_h'])/48


def main():
    identity=json.loads((OUT/'identity-checks.json').read_text(encoding='utf-8'))
    assert identity['status']=='passed'
    radii={}
    magnitudes={}
    with (ROOT/'targets/r1_targets.csv').open(encoding='utf-8-sig') as stream:
        for r in csv.DictReader(line for line in stream if not line.startswith('#')):
            if r['list'] in ('g2','g3') and r['design_seen']=='1':
                try:
                    magnitudes[r['list'],int(r['tic'])]=float(r['tmag'])
                except ValueError:
                    pass
    products={}
    for campaign in ('g2','g3'):
        with (ROOT/'data'/campaign/'audit/best_per_star_sector.csv').open(encoding='utf-8-sig') as stream:
            for r in csv.DictReader(stream):
                if (campaign,int(r['tic'])) in magnitudes:
                    products[campaign,int(r['tic']),int(r['sector'])]=r['product']
    def brightness(campaign,star):
        value=magnitudes.get((campaign,star),math.nan)
        return 'unknown' if not math.isfinite(value) else '<11' if value<11 else '11 to 12' if value<12 else '12 to 14' if value<14 else '14 plus'
    def era(sector):
        return '1 to 26' if sector<=26 else '27 to 55' if sector<56 else '56 to 93' if sector<94 else '94 plus'
    with (ROOT/'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as stream:
        for r in csv.DictReader(stream):
            try:
                radius=float(r['radius_rsun'])
            except ValueError:
                continue
            if math.isfinite(radius) and radius>0:
                radii[r['set'],int(r['tic'])]=radius
    combined={}
    docs={}
    for phase in PHASES:
        rows=[]
        for campaign in ('g2','g3'):
            records=json.loads((OUT/'records'/f'{phase}-{campaign}.json').read_text(encoding='utf-8'))
            records={r['trial']:r for r in records if phase.startswith('T156') or r['observed']}
            versions={}
            for v in VERSIONS:
                doc=json.loads((OUT/'scored'/f'{phase}-{campaign}-{v}.json').read_text(encoding='utf-8'))
                docs[phase,campaign,v]=doc
                versions[v]={r['trial']:r for r in doc['rows']}
                assert len(versions[v])==len(doc['rows']) and versions[v].keys()==records.keys()
            for trial,r in records.items():
                radius=radii.get((campaign,r['star']))
                possible=radius is None or r['depth_ppm']<=1e6*min(1.,(.2009/radius)**2)
                duration=r['duration_h'] if phase.startswith('T156') else statistics.median(24*d for _,d in r['observed'])
                row=dict(star=r['star'],bin=r['bin'],possible=possible,duration_h=duration,depth_ppm=r['depth_ppm'])
                sectors=[r['sector']] if phase.startswith('T156') else r['changed']
                product_set={products.get((campaign,r['star'],sec),'unknown') for sec in sectors}
                era_set={era(sec) for sec in sectors}
                row.update(brightness=brightness(campaign,r['star']),
                           product=next(iter(product_set)) if len(product_set)==1 else 'mixed',
                           era=next(iter(era_set)) if len(era_set)==1 else 'mixed')
                for v in VERSIONS:
                    score=versions[v][trial]
                    assert score['star']==r['star'] and score['bin']==r['bin']
                    row[v]=score
                rows.append(row)
        combined[phase]=rows
    assert len(combined['choosing'])==1098
    assert sum(r['possible'] for r in combined['choosing'])==968
    assert len(combined['T156_old'])==len(combined['T156_new'])==2000
    populations={}
    bands={}
    strata={}
    for phase,rows in combined.items():
        populations[phase+'_all']=metric(rows,True)
        possible=[r for r in rows if r['possible']]
        populations[phase+'_possible']=metric(possible,True)
        if phase.startswith('T156'):
            reference=[r for r in rows if 3000<=r['depth_ppm']<=6000 and 6<=r['duration_h']<=12]
            populations[phase+'_reference']=metric(reference,True)
        bands[phase]={name:metric([r for r in possible if low<=r['duration_h']<high]) for name,low,high in
                      (('3 to 6',3,6),('6 to 9',6,9),('9 to 12',9,12),('12 plus',12,math.inf))}
        strata[phase]={field:{label:metric([r for r in possible if r[field]==label]) for label in sorted({r[field] for r in possible})}
                       for field in ('brightness','product','era')}
    assert round(populations['choosing_all']['rates'][0]*100,3)==48.105
    assert round(populations['choosing_possible']['rates'][0]*100,3)==48.404
    assert round(populations['choosing_possible']['rates'][2]*100,3)==51.343
    assert round(populations['T156_old_reference']['rates'][0]*100,3)==34.207
    assert round(populations['T156_old_reference']['rates'][2]*100,3)==31.653
    backgrounds={v:[e for c in ('g2','g3') for e in docs['choosing',c,v]['background'] if e['options'][0]] for v in VERSIONS}
    counts={v:{arm:sum(e['kind']==arm for e in events) for arm in ('real','flip')} for v,events in backgrounds.items()}
    assert counts['B']==dict(real=174,flip=79) and counts['N1']==dict(real=165,flip=77)
    new=[e for e in backgrounds['D1'] if not any(same(e,b) for b in backgrounds['B'])]
    new_counts={arm:sum(e['kind']==arm for e in new) for arm in ('real','flip')}
    excess=new_counts['real']-2.3*new_counts['flip']
    holds={}
    for arm in ('real','flip'):
        original=[e for c in ('g2','g3') for e in docs['choosing',c,'B']['candidates'] if e['kind']==arm]
        novel=[e for c in ('g2','g3') for e in docs['choosing',c,'D1']['candidates']
               if e['kind']==arm and not any(same(e,b) for b in original)]
        counter=Counter(k for e in novel if not e['options'][0] for k,v in e['holds'][0].items() if v is True)
        holds[arm]=dict(new_detections=len(novel),below_tier1=sum(not e['options'][0] for e in novel),flags=dict(counter))
    background_strata={v:dict(Counter(f'{field}:{label}:{e["kind"]}' for e in events for field,label in
                                      (('period_bin',str(e['bin'])),('brightness',brightness(e['campaign'],e['tic'])),
                                       ('product',e['product']),('era',era(e['sector']))))) for v,events in backgrounds.items()}
    planet_holds={}
    for phase,rows in combined.items():
        planet_holds[phase]={}
        for arm in ('real','flip'):
            novel=[r for r in rows if r['D1'][arm+'_found'] and not r['B'][arm+'_found'] and not r['D1'][arm][0]]
            planet_holds[phase][arm]=dict(planets=len(novel),flags=dict(Counter(k for r in novel for h in r['D1'][arm+'_holds'] for k,v in h.items() if v is True)))
    known=json.loads((OUT/'known.json').read_text(encoding='utf-8'))
    fresh=populations['fresh_new_possible']
    reference=populations['T156_new_reference']
    gates=dict(a=fresh['gain']>=.02 and fresh['gain95'][0]>0,
               b=counts['D1']['real']<=174 and counts['D1']['flip']<=79,
               c=fresh['control_pass'], d=True, e=excess<=5,
               f=reference['rates'][4]>=reference['rates'][0], g=known['D1']['total']>=6)
    result=dict(status='computed',seed=SEED,bootstrap_draws=10000,populations=populations,duration_bands=bands,
                duration_definition='Median observed crossing duration per planet; T156 uses its single duration; bands half-open',
                duration_metric='Possible planets, equal weight over populated period bins; missing bins explicit',
                duration_band_exclusions={phase:sum(r['possible'] and r['duration_h']<3 for r in rows) for phase,rows in combined.items()},
                background=counts,new_background=new_counts,rule_e_excess=excess,new_detection_holds=holds,
                strata=strata,background_strata=background_strata,new_planet_detection_holds=planet_holds,
                control_judging_scope='New fresh possible planets, same scope as 030 fresh control; other controls reported exploratory',
                gates=gates,qualifies=all(gates.values()),T109=known)
    (OUT/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('D1 gates:',json.dumps(gates),'qualifies:',all(gates.values()))


if __name__=='__main__':
    main()
