"""Read guarded raw design light, then fit one disjoint shard."""
import argparse
from collections import Counter
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).parent))
S=importlib.import_module('014_eclipse_select')
F=importlib.import_module('014_eclipse_fit')
H=S.H
O=S.O


def main(slot,slots,stage):
    os.environ.update(SS_SET='g2',NUMBA_NUM_THREADS='2',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    guard=H.Guard()
    guard.start()
    guard.allow_machine_inputs('g2')
    import numpy as np
    import pandas as pd
    import detect_v2 as V
    import petrova_mask as PM
    import sap_twin as T

    samples=json.loads((H.OUT/'eclipse-samples.json').read_text(encoding='utf-8'))
    ids=sorted(samples['holdout'] if stage=='holdout' else samples['affected']+samples['controls'])
    assert len(ids)==len(set(ids))==(40 if stage=='holdout' else 172) and all(str(s) in guard.seen['g2'] for s in ids)
    best=pd.read_csv(H.DATA/'g2'/'audit'/'best_per_star_sector.csv')
    best={(r.tic,r.sector):r.product for r in best.itertuples() if r.tic in ids}
    products=('groups','groups_sap')
    cat=PM.cat()
    rows=[]
    counters=Counter()
    for star in ids[slot::slots]:
        entry=cat.get(star)
        result=dict(star=star,sample='holdout' if stage=='holdout' else 'control' if star in samples['controls'] else 'affected',catalogue=entry)
        rows.append(result)
        if not entry or not np.isfinite(entry['wp']) or entry['wp']<=0:
            result.update(fit={},reason='no catalogue primary width')
            counters['no catalogue width']+=1
            continue
        raw=[]
        folder=H.DATA/'g2'/str(star)
        seen=set()
        for kind in products:
            for file in sorted((S.SOURCE/kind).glob(f'{star}_*.json')):
                guard.allow_design_file(file)
                sec=int(file.stem.split('_')[1])
                for m in json.loads(file.read_text(encoding='utf-8'))['meta']:
                    name=m['file'].removesuffix(T.SUFFIX)
                    key=sec,kind,name
                    if key in seen:
                        continue
                    seen.add(key)
                    p=folder/Path(name).name
                    guard.allow_design_file(p)
                    loader=T.load_sap if kind=='groups_sap' else V.load
                    t,f,_,meta=loader(str(p),info=True)
                    product=meta['product']
                    valid=np.isfinite(t)&np.isfinite(f)
                    if valid.sum()<10:
                        counters['empty or short inputs']+=1
                        continue
                    t,f=t[valid],f[valid]
                    rank=0 if product==best.get((star,sec)) else 2 if kind=='groups_sap' else 1
                    raw.append((sec,rank,product,t,f))
                    counters['product curves loaded']+=1
        if result['sample']=='control' and raw:
            streams=F.streams_for_fit(raw)
            if streams:
                _,_,_,index,_,ff=max(streams,key=lambda x:len(x[-1]))
                dif=np.diff(ff)[np.diff(index)==1]/np.sqrt(2)
                if len(dif)>100:
                    scale=F.robust_sigma(dif)
                    result['noise']=(dif[abs(dif)<=5*scale][:2500]).tolist()
        width=entry['wp']
        ws=entry['ws'] if entry['ws']>0 else width
        result['input_curves']=len(raw)
        result['sectors']=sorted({s for s,*_ in raw})
        result['fit']=F.fit_star(raw,entry['P'],width,ws,entry.get('phs',float('nan')))
        if str(star) in samples['injections']:
            trial=samples['injections'][str(star)]
            result['injected']={str(sign):F.fit_star(raw,entry['P'],width,ws,entry.get('phs',float('nan')),trial,sign)
                                for sign in (1,-1)}
        counters['stars processed']+=1
    O.write_json(H.OUT/f'eclipse-{stage}-{slot}.json',dict(rows=rows,counts=counters))
    print('Completed shard',slot,'stars',len(rows),dict(counters),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('slot',type=int)
    p.add_argument('slots',type=int)
    p.add_argument('stage',choices=('calibrate','holdout'))
    args=p.parse_args()
    main(args.slot,args.slots,args.stage)
