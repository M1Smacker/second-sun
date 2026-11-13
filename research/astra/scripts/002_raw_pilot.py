"""Predeclared design-only raw injection pilot; full private context and identity checks."""
import csv
import importlib
import json
import os
from pathlib import Path
import sys
import traceback
import uuid
sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('002_harness')
canonical=importlib.import_module('002_replay').canonical

def main():
    os.environ.update(SS_SET='g3',VESPER_OPTS='c6,p1',NUMBA_NUM_THREADS='2')
    guard=H.Guard(); guard.start(); refs=guard.allow_machine_inputs('g3')
    import numpy as np
    import pandas as pd
    import stage3 as S3
    import stage2_search as S2
    import stage3_core as C
    import stage3_report as R
    import sap_twin as T
    source=max(H.OUT.glob('phase_g3_*'),key=lambda p:p.stat().st_mtime)
    with H.TARGETS.open(encoding='utf-8') as f:
        periods={r['tic']:float(r['p_bin_d']) for r in csv.DictReader(x for x in f if not x.startswith('#')) if r['list']=='g3' and r['design_seen']=='1'}
    edges=[5,10,14,20,27.4,np.inf]; selected={}
    for p in sorted((source/'groups').glob('*.json')):
        star=p.stem.split('_')[0]
        if star not in periods: raise RuntimeError('Fixture membership violation')
        b=next(i for i in range(5) if edges[i]<=periods[star]<edges[i+1])
        selected.setdefault(b,p)
    assert len(selected)==5
    raw=[]
    for folder in ('groups','groups_sap'):
        for p in (source/folder).glob('*.json'):
            if p.stem.split('_')[0] not in periods: raise RuntimeError('Fixture membership violation')
            raw.extend(json.loads(p.read_text(encoding='utf-8'))['events'])
    best=pd.read_csv(C.BEST)[['tic','sector','product']].rename(columns={'product':'best'})
    context=pd.DataFrame(raw).merge(best,on=['tic','sector'],how='left')
    context['primary']=context['product']==context['best']; context['c8_best']=pd.to_numeric(context.c8_best,errors='coerce')
    def final(frame): return R.apply_v7(R.merge_sap(frame)).reset_index(drop=True)
    base_final=final(context)
    dest=H.OUT/('raw_pilot_'+uuid.uuid4().hex[:8]); dest.mkdir()
    S3._init3(dest,'g3',C.GRID_V5); S2.S['spoc_by_sector']={s:str(p) for s,p in refs.items()}
    original_load=S2.load; active={}
    def load(path,info=False):
        loaded=original_load(path,info=info)
        if not active: return loaded
        t,f=loaded[:2]
        signal=-active['sign']*.004*np.clip((4-np.abs(t-active['time'])*24)/1.6,0,1)
        return (t,f+signal)+tuple(loaded[2:])
    S2.load=load
    rng=np.random.default_rng(2026111302); results=[]
    for b,path in sorted(selected.items()):
        old=json.loads(path.read_text(encoding='utf-8')); star,sector=map(int,path.stem.split('_'))
        paths=[H.DATA/'g3'/str(star)/m['file'] for m in old['meta']]
        for p in paths: guard.allow_design_file(p)
        sap_path=source/'groups_sap'/path.name
        sap=json.loads(sap_path.read_text(encoding='utf-8')) if sap_path.exists() else None
        twin=[] if sap is None else list(dict.fromkeys(H.DATA/'g3'/str(star)/m['file'].removesuffix(T.SUFFIX) for m in sap['meta']))
        for p in twin: guard.allow_design_file(p)
        product_rows=best[(best.tic==star)&(best.sector==sector)]
        product=product_rows.iloc[0]['best'] if len(product_rows) else np.nan
        times=[original_load(str(p))[0] for p in paths]
        times=[x for x in times if len(x)]
        if not times: raise RuntimeError('No loaded times in preselected group')
        tc=float(rng.uniform(min(x.min() for x in times),max(x.max() for x in times)))
        baseline=base_final[(base_final.tic==star)&(base_final.sector==sector)]
        for sign in (0,1,-1):
            active.clear()
            if sign: active.update(sign=sign,time=tc)
            folder=dest/f'{b}_{sign}'; folder.mkdir()
            S2.GROUPS=folder/'groups'; S2.GROUPS.mkdir()
            output=S3.do_group3((star,sector,list(map(str,paths))))
            primary=json.loads(Path(output).read_text(encoding='utf-8'))
            events=primary['events']; meta=list(primary['meta'])
            if sign==0 and canonical(events)!=canonical(old['events']): raise RuntimeError('Primary replay mismatch')
            if twin:
                S2.GROUPS=folder/'groups_sap'; S2.GROUPS.mkdir()
                output=S3.do_group3((star,sector,[str(p)+T.SUFFIX for p in twin]))
                S3.add_pdc((output,list(map(str,twin)),product))
                updated=json.loads(Path(output).read_text(encoding='utf-8'))
                if sign==0 and canonical(updated['events'])!=canonical(sap['events']): raise RuntimeError('SAP replay mismatch')
                events+=updated['events']; meta+=updated['meta']
            if any(str(m.get('status','')).startswith('ERROR') for m in meta): raise RuntimeError('Processing error')
            current=pd.DataFrame(events)
            if len(current):
                current['best']=product; current['primary']=current['product']==product
                current['c8_best']=pd.to_numeric(current.c8_best,errors='coerce')
            combined=pd.concat([context[~((context.tic==star)&(context.sector==sector))],current],ignore_index=True)
            scored=final(combined); scored=scored[(scored.tic==star)&(scored.sector==sector)]
            if sign==0:
                # Compare final columns with matching dtype-independent JSON serialization.
                left=baseline.sort_values(['kind','product','center']).reset_index(drop=True)
                right=scored.sort_values(['kind','product','center']).reset_index(drop=True)
                pd.testing.assert_frame_equal(left,right,check_dtype=False,check_exact=True)
                print(json.dumps(dict(bin=b,zero_identity=True)),flush=True); continue
            kind='real' if sign==1 else 'flip'
            def matched(frame):
                return frame[(frame.kind==kind)&frame.primary & (np.abs(frame.center-tc)<=.5*np.maximum(8,frame.dur_h)/24+.1)]
            near=matched(scored); prior=matched(baseline)
            results.append(dict(bin=b,sign=sign,preexisting=len(prior)>0,primary_match=len(near)>0,
                tier1=bool(near.tier.isin(['1A','1B','1L']).any()) and len(prior)==0))
            (dest/'summary.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
            print(json.dumps(results[-1]),flush=True)
    (H.OUT/'raw-pilot.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

if __name__=='__main__':
    try: main()
    except Exception: traceback.print_exc(); sys.exit(1)
