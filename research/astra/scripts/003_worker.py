"""Guarded fixed-design recovery worker. Private detailed output; counts-only console."""
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys
import time
import traceback
from datetime import datetime, timezone
sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('003_harness')

class IdentityFailure(RuntimeError): pass

def canonical(events):
    return sorted(json.dumps(e,sort_keys=True,allow_nan=True) for e in events)

def run(args):
    os.environ.update(SS_SET=args.campaign,VESPER_OPTS='c6,p1',NUMBA_NUM_THREADS='2')
    guard=H.Guard(); guard.start(); refs=guard.allow_machine_inputs(args.campaign)
    import numpy as np
    import pandas as pd
    import stage3 as S3
    import stage2_search as S2
    import stage3_core as C
    import stage3_report as R
    import petrova_mask as PM
    import sap_twin as T
    name=args.campaign
    source=H.DATA/f'stage3_{name}'/f'r1dev_{name}_seen_{H.DEVELOPMENT_HASH}'
    ident=f'{name}-{args.slot}'
    study=getattr(args,'study_window',None)
    folder=H.OUT/('workers' if study is None else f'study-w{study:g}')/ident
    folder.mkdir(parents=True,exist_ok=True)
    progress=folder/'progress.json'
    def update(status,done,planned,**extra):
        progress.write_text(json.dumps(dict(worker=ident,status=status,trials_done=done,trials_planned=planned,
            last_update_utc=datetime.now(timezone.utc).isoformat(),**extra),indent=2),encoding='utf-8')
    trials=json.loads((H.OUT/'design.json').read_text(encoding='utf-8'))['trials']
    jobs=[r for r in trials[args.start:args.limit] if r['campaign']==name and r['trial']%args.slots==args.slot]
    if study is not None:
        selected=set(json.loads((H.OUT/'study-selection.json').read_text(encoding='utf-8'))['trials'])
        jobs=[r for r in jobs if r['trial'] in selected]
    update('context',0,len(jobs)); start=time.perf_counter()
    best=pd.read_csv(C.BEST)[['tic','sector','product']].rename(columns={'product':'best'})
    events=[]
    for kind in ('groups','groups_sap'):
        for p in sorted((source/kind).glob('*.json')):
            if p.stem.split('_')[0] not in guard.seen[name]: continue
            guard.allow_design_file(p)
            events.extend(json.loads(p.read_text(encoding='utf-8'))['events'])
    context=pd.DataFrame(events).merge(best,on=['tic','sector'],how='left')
    context['primary']=context['product']==context['best']
    context['c8_best']=pd.to_numeric(context.c8_best,errors='coerce')
    S3._init3(folder,'g3' if name=='g3' else 'g2',C.GRID_V5)
    S2.S['spoc_by_sector']={s:str(p) for s,p in refs.items()}
    original_load=S2.load; original_prepare=S2.prepare; original_mask=PM.mask_runs; original_windows=S2.in_windows
    original_detrend=S2.detrend
    def study_detrend(t,f,window_d=2.0):
        return original_detrend(t,f,window_d=study)
    active={}; raw_cache={}; prepared={}; tracing={}; traces={}
    def load(path,info=False):
        key=(str(path),bool(T.MODE['sap']),bool(T.MODE['pdc']),info)
        if key not in raw_cache: raw_cache[key]=original_load(path,info=info)
        r=raw_cache[key]; t,f=r[:2]
        tracing['raw']=t
        if not active: return r
        half=active['duration_h']/2
        shape=np.clip((half-np.abs(t-active['time'])*24)/(.1*active['duration_h']),0,1)
        return (t,f-active['sign']*active['depth_ppm']*1e-6*shape)+tuple(r[2:])
    def windows(t,w):
        keep=original_windows(t,w); tracing['windowed']=t[keep]; return keep
    def mask(t,f,periods,star):
        tracing['windowed']=t
        output=original_mask(t,f,periods,star); tracing['masked']=output[0]
        return output
    def prepare(path):
        key=str(path)
        if key in prepared: return prepared[key]
        tracing.clear(); d,m=original_prepare(path)
        if active:
            raw=tracing.get('raw',np.array([])); win=tracing.get('windowed',raw); kept=tracing.get('masked',np.array([]))
            cad=float(np.median(np.diff(raw))) if len(raw)>1 else np.nan
            safe=m.get('status')!='no safe windows' and not str(m.get('status','')).startswith('ERROR')
            inside=bool(len(win) and np.isfinite(cad) and np.min(np.abs(win-active['time']))<=1.5*cad)
            n=int((np.abs(kept-active['time'])<=active['duration_h']/48).sum())
            enough=bool(d is not None and np.isfinite(cad) and n>=max(3,.5*active['duration_h']/24/cad))
            traces[key]=dict(product=m.get('product','unknown'),safe=safe,inside=inside,mask=enough,status=m.get('status'))
        prepared[key]=(d,m); return d,m
    S2.load=load; S2.prepare=prepare; S2.in_windows=windows; PM.mask_runs=mask
    verified={}; journal=folder/f'results-{args.start}-{args.limit}.jsonl'
    if journal.exists(): raise RuntimeError('Existing result journal; explicit recovery needed')
    setup_seconds=time.perf_counter()-start
    for count,trial in enumerate(jobs):
        if (H.OUT/'STOP.json').exists(): update('stopped',count,len(jobs)); return
        tstart=time.perf_counter(); star,sector=trial['star'],trial['sector']; stem=f'{star}_{sector}.json'
        p=source/'groups'/stem; guard.allow_design_file(p)
        old=json.loads(p.read_text(encoding='utf-8'))
        oldsap_path=source/'groups_sap'/stem
        if oldsap_path.exists():
            guard.allow_design_file(oldsap_path); oldsap=json.loads(oldsap_path.read_text(encoding='utf-8'))
        else: oldsap=None
        paths=list(dict.fromkeys(H.DATA/name/str(star)/m['file'] for m in old['meta']))
        twin=[] if oldsap is None else list(dict.fromkeys(H.DATA/name/str(star)/m['file'].removesuffix(T.SUFFIX) for m in oldsap['meta']))
        for path in set(paths+twin): guard.allow_design_file(path)
        for path in (H.DATA/name/str(star)).glob('*.fits'): guard.allow_design_file(path)
        bp=best[(best.tic==star)&(best.sector==sector)]
        product=bp.iloc[0]['best'] if len(bp) else np.nan
        span_index=next((i for i,m in enumerate(old['meta']) if m.get('product')==product),0)
        span_path=H.DATA/name/str(star)/old['meta'][span_index]['file']
        active.clear(); tracing.clear()
        raw=load(str(span_path),info=True)[0]
        if not len(raw): raise RuntimeError('Empty raw span: input failure requires separate diagnosis')
        centre=float(raw.min()+trial['phase_fraction']*(raw.max()-raw.min()))
        expected_events=old['events']+([] if oldsap is None else oldsap['events'])
        camera_set=set(e['camera'] for e in expected_events)
        camera_set.update(m['camera'] for m in old['meta'] if 'camera' in m)
        sub=context[(context.tic==star)|((context.sector==sector)&context.camera.isin(camera_set))].copy()
        base=R.apply_v7(R.merge_sap(sub)).reset_index(drop=True)
        base=base[(base.tic==star)&(base.sector==sector)]
        def score(evs):
            new=pd.DataFrame(evs)
            if len(new):
                new['best']=product; new['primary']=new['product']==product; new['c8_best']=pd.to_numeric(new.c8_best,errors='coerce')
            combined=pd.concat([sub[~((sub.tic==star)&(sub.sector==sector))],new],ignore_index=True)
            out=R.apply_v7(R.merge_sap(combined))
            return out[(out.tic==star)&(out.sector==sector)]
        file_hash=hashlib.sha256(p.read_bytes()+(oldsap_path.read_bytes() if oldsap else b'')).hexdigest()
        key=(star,sector)
        signs=(0,1,-1) if key not in verified else (1,-1)
        if key in verified and verified[key]!=file_hash: raise IdentityFailure('Stored baseline changed')
        result=dict(trial,product=str(product),time=centre,setup_seconds=setup_seconds)
        for sign in signs:
            S2.detrend=study_detrend if study is not None and sign else original_detrend
            active.clear(); prepared.clear(); traces.clear()
            if sign: active.update(trial,sign=sign,time=centre)
            trial_dir=folder/f'trial-{trial["trial"]}-{sign}'
            if trial_dir.exists(): raise RuntimeError('Existing trial output; refuse cached search')
            S2.GROUPS=trial_dir/'groups'; S2.GROUPS.mkdir(parents=True)
            fresh=json.loads(Path(S3.do_group3((star,sector,list(map(str,paths))))).read_text(encoding='utf-8'))
            new_events=list(fresh['events']); metadata=list(fresh['meta'])
            if not sign and canonical(fresh['events'])!=canonical(old['events']): raise IdentityFailure('Primary zero-injection mismatch')
            if twin:
                S2.GROUPS=trial_dir/'groups_sap'; S2.GROUPS.mkdir()
                out=S3.do_group3((star,sector,[str(q)+T.SUFFIX for q in twin]))
                S3.add_pdc((out,list(map(str,twin)),product))
                sap=json.loads(Path(out).read_text(encoding='utf-8'))
                if not sign and canonical(sap['events'])!=canonical(oldsap['events']): raise IdentityFailure('SAP zero-injection mismatch')
                new_events+=sap['events']; metadata+=sap['meta']
            if any(str(m.get('status','')).startswith('ERROR') for m in metadata): raise RuntimeError('Recorded pipeline processing error')
            scored=score(new_events)
            if not sign:
                left=base.sort_values(['kind','product','center']).reset_index(drop=True)
                right=scored.sort_values(['kind','product','center']).reset_index(drop=True)
                try: pd.testing.assert_frame_equal(left,right,check_dtype=False,check_exact=True)
                except AssertionError as exc: raise IdentityFailure('Union zero-injection mismatch') from exc
                verified[key]=file_hash; continue
            arm='real' if sign==1 else 'flip'
            nearby=scored[(scored.kind==arm)&(np.abs(scored.center-centre)<=trial['duration_h']/48)]
            prior=base[(base.kind==arm)&base.primary&(np.abs(base.center-centre)<=trial['duration_h']/48)]
            eligible=[v for v in traces.values() if v['product'] in (product,str(product)+'-SAP')]
            if not eligible: eligible=list(traces.values())
            flags=[any(v['safe'] for v in eligible),any(v['safe'] and v['inside'] for v in eligible),
                   any(v['safe'] and v['inside'] and v['mask'] for v in eligible),len(nearby)>0,
                   bool((nearby.primary&nearby.tier.isin(['1A','1L','1B'])&(nearby.snr>=7)).any()) and not len(prior)]
            stage=0
            for flag in flags:
                if not flag: break
                stage+=1
            # Recovery itself follows the final event rule, even if a diagnostic cadence proxy disagrees.
            result['dip' if sign==1 else 'bump']=dict(stage=stage,flags=flags,recovered=flags[-1],preexisting=len(prior)>0,
                statuses=[v['status'] for v in eligible],diagnostic_inconsistency=bool(flags[-1] and stage<5))
        result['seconds']=time.perf_counter()-tstart
        with journal.open('a',encoding='utf-8') as stream: stream.write(json.dumps(result)+'\n')
        update('running',count+1,len(jobs),setup_seconds=setup_seconds,last_trial_seconds=result['seconds'])
        print(json.dumps(dict(worker=ident,done=count+1,planned=len(jobs),seconds=round(result['seconds'],2))),flush=True)
        raw_cache.clear()
    update('complete',len(jobs),len(jobs),setup_seconds=setup_seconds)

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--campaign',choices=['g2','g3'],required=True)
    parser.add_argument('--slot',type=int,default=0); parser.add_argument('--slots',type=int,default=1)
    parser.add_argument('--start',type=int,default=0); parser.add_argument('--limit',type=int,default=20)
    parser.add_argument('--study-window',type=float,choices=[1.0,3.0],default=None)
    args=parser.parse_args()
    try: run(args)
    except Exception as exc:
        traceback.print_exc()
        H.OUT.mkdir(parents=True,exist_ok=True)
        (H.OUT/'STOP.json').write_text(json.dumps(dict(kind='identity' if isinstance(exc,IdentityFailure) else 'tooling',
            worker=f'{args.campaign}-{args.slot}',error_type=type(exc).__name__,message=str(exc)[:120],
            last_update_utc=datetime.now(timezone.utc).isoformat()),indent=2),encoding='utf-8')
        sys.exit(1)
