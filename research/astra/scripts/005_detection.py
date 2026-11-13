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
H=importlib.import_module('005_harness')

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

    import petrova_mask as PM
    import sap_twin as T
    name=args.campaign
    source=H.DATA/f'stage3_{name}'/f'r1dev_{name}_seen_{H.DEVELOPMENT_HASH}'
    ident=f'{name}-{args.slot}'
    study=getattr(args,'study_window',None)
    folder=H.OUT/'blindspot'/ident
    folder.mkdir(parents=True,exist_ok=True)
    progress=folder/'progress.json'
    def update(status,done,planned,**extra):
        progress.write_text(json.dumps(dict(worker=ident,status=status,trials_done=done,trials_planned=planned,
            last_update_utc=datetime.now(timezone.utc).isoformat(),**extra),indent=2),encoding='utf-8')
    from collections import Counter
    old_out=H.OUT.with_name('003')
    if old_out.resolve() != guard.data/'astra'/'003':raise PermissionError('T156 source path escape')
    def read_saved(path):
        resolved=path.resolve(strict=True)
        if resolved != guard.data/path.relative_to(H.DATA) or not resolved.is_relative_to(old_out.resolve()):
            raise PermissionError('T156 input path escape')
        guard.reads.add(resolved)
        return json.loads(path.read_text(encoding='utf-8'))
    jobs=[]
    for old_journal in sorted((old_out/'workers').glob(f'{name}-*/results-*.jsonl')):
        resolved=old_journal.resolve(strict=True)
        if resolved != guard.data/old_journal.relative_to(H.DATA):raise PermissionError('Journal path escape')
        guard.reads.add(resolved)
        for line in old_journal.read_text(encoding='utf-8').splitlines():
            row=json.loads(line)
            if row['bin'] in (0,3) and row['trial']//5%args.slots==args.slot:
                if str(row['star']) not in guard.seen[name] or row['campaign']!=name:raise PermissionError('Trial outside design')
                jobs.append((row,old_journal.parent))
    jobs.sort(key=lambda pair:pair[0]['trial'])
    update('context',0,len(jobs)); start=time.perf_counter()
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
    original_prod=S2.Prod
    measurements=[]
    def fit(t,f):
        dt=np.abs(t-active['time'])*24
        select=(dt<=active['duration_h'])&np.isfinite(f)
        x=np.clip((active['duration_h']/2-dt[select])/(.1*active['duration_h']),0,1)
        y=f[select]
        if len(y)<5 or np.var(x)==0:return None,None
        ratio=-float(np.mean((x-x.mean())*(y-y.mean()))/np.var(x))/(active['depth_ppm']*1e-6)
        return ratio,float(1.4826*np.median(np.abs(y-np.median(y)))*1e6)
    detrended=[]
    def trace_detrend(t,f,window_d=2.0):
        output=original_detrend(t,f,window_d=window_d)
        detrended[:]=[fit(*output)]
        return output
    class TracedProd(original_prod):
        def __init__(self,t,f,sign=1):
            super().__init__(t,f,sign)
            self.trace_sign=sign
            self.before=fit(t,f)
            self.after=detrended[0]
        def events(self,thr=7.0):
            found=super().events(thr)
            if self.trace_sign!=1:return found
            radius=active['duration_h']/48
            scores=[]
            for duration in S2.DURS_H:
                centres,snr,_=self.scores(duration)
                select=(np.abs(centres-active['time'])<=radius)&np.isfinite(snr)
                scores.extend(snr[select].tolist())
            nearest=min((abs(e['center']-active['time']) for e in found),default=None)
            measurements.append(dict(before=self.before,after=self.after,best_snr=max(scores,default=None),
                above=sum(x>=thr for x in scores),matched=nearest is not None and nearest<=radius,
                shift_duration=None if nearest is None else nearest/(2*radius)))
            return found
    S2.detrend=trace_detrend; S2.Prod=TracedProd
    journal=folder/'diagnostic.jsonl'
    if journal.exists():raise RuntimeError('Existing diagnostic journal')
    for count,(trial,old_folder) in enumerate(jobs):
        if (H.OUT/'STOP.json').exists():update('stopped',count,len(jobs));return
        star,sector=trial['star'],trial['sector']; stem=f'{star}_{sector}.json'
        prior=old_folder/f'trial-{trial["trial"]}-1'
        active.clear();active.update(trial,sign=1)
        raw_cache.clear();prepared.clear();traces.clear()
        for p in (H.DATA/name/str(star)).glob('*.fits'):guard.allow_design_file(p)
        result={k:trial[k] for k in ('trial','bin','depth_ppm','duration_h','product','dip')}
        result['paths']=[]
        for kind in ('groups','groups_sap'):
            previous=prior/kind/stem
            if not previous.exists():continue
            expected=read_saved(previous)
            metadata=[m for m in expected['meta'] if 'product' in m]
            suffix=T.SUFFIX if kind=='groups_sap' else ''
            paths=list(dict.fromkeys(str(H.DATA/name/str(star)/m['file'].removesuffix(T.SUFFIX))+suffix for m in metadata))
            for p in paths:guard.allow_design_file(Path(p.removesuffix(T.SUFFIX)))
            measurements.clear(); S2.GROUPS=folder/f'trial-{trial["trial"]}'/kind
            S2.GROUPS.mkdir(parents=True)
            output=S3.do_group3((star,sector,paths))
            if kind=='groups_sap':S3.add_pdc((output,[p.removesuffix(T.SUFFIX) for p in paths],trial['product']))
            actual=json.loads(Path(output).read_text(encoding='utf-8'))
            if canonical(actual['events'])!=canonical(expected['events']):raise IdentityFailure('Saved injected event mismatch')
            # S2 builds and iterates one prepared object per surviving product, in metadata order.
            products=list(dict.fromkeys(m['product'] for m in actual['meta'] if m.get('status')=='ok'))
            if len(products)!=len(measurements):raise RuntimeError('Measurement-to-product count mismatch')
            for product,metrics in zip(products,measurements):
                if product not in (trial['product'],trial['product']+'-SAP'):continue
                cat=PM.cat().get(star)
                phase_width=None
                if cat and np.isfinite(cat['wp']) and cat['wp']>0:
                    P=cat['P']; phase=(trial['time']-cat['T0'])/P
                    phs=cat['phs'] if np.isfinite(cat['phs']) and np.isfinite(cat['ws']) and cat['ws']>0 else .5
                    ws=cat['ws'] if np.isfinite(cat['ws']) and cat['ws']>0 else cat['wp']
                    phase_width=min(abs(phase-round(phase))*P/cat['wp'],abs(phase-phs-round(phase-phs))*P/ws)
                result['paths'].append(dict(product=product,phase_width=phase_width,**metrics))
        with journal.open('a',encoding='utf-8') as stream:stream.write(json.dumps(result)+'\n')
        update('running',count+1,len(jobs))
    update('complete',len(jobs),len(jobs))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--campaign',choices=['g2','g3'],required=True)
    parser.add_argument('--slot',type=int,default=0)
    parser.add_argument('--slots',type=int,default=1)
    try:run(parser.parse_args())
    except Exception as exc:
        (H.OUT/'STOP.json').write_text(json.dumps(dict(kind=type(exc).__name__)),encoding='utf-8')
        traceback.print_exc();sys.exit(1)
