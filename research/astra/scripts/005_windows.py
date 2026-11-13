"""Inspect recorded and quality-selected time support on the fixed reference losses."""
import importlib,json,os,sys
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('005_harness')
name=sys.argv[1]
os.environ.update(SS_SET=name,VESPER_OPTS='c6,p1',NUMBA_NUM_THREADS='2')
guard=H.Guard();guard.start();refs=guard.allow_machine_inputs(name)
import numpy as np
from astropy.io import fits
import audit_all as A
import stage2_search as S
from detect_v2 import intersect_windows
S._init(); S.S['spoc_by_sector']={k:str(v) for k,v in refs.items()}
old=H.OUT.with_name('003');assert old.resolve()==guard.data/'astra'/'003'
def saved(path):
    resolved=path.resolve(strict=True)
    if resolved!=guard.data/path.relative_to(H.DATA) or not resolved.is_relative_to(old.resolve()):raise PermissionError('T156 path escape')
    guard.reads.add(resolved);return path.read_text(encoding='utf-8')
counts=Counter();sources=Counter();reasons=Counter(); bybin=Counter()
for journal in (old/'workers').glob(f'{name}-*/results-*.jsonl'):
    for line in saved(journal).splitlines():
        trial=json.loads(line)
        if not (3000<=trial['depth_ppm']<=6000 and 6<=trial['duration_h']<=12 and trial['dip']['stage']<2 and not trial['dip']['recovered']):continue
        star,sector=trial['star'],trial['sector'];centre=trial['time'];stem=f'{star}_{sector}.json'
        if str(star) not in guard.seen[name] or trial['campaign']!=name:raise PermissionError('Non-design trial')
        folder=H.DATA/name/str(star)
        meta=json.loads(saved(journal.parent/f'trial-{trial["trial"]}-1'/'groups'/stem))['meta']
        selected=[m for m in meta if m.get('product')==trial['product']] or meta
        states=set(); details=set()
        for m in selected:
            path=guard.allow_design_file(folder/m['file'])
            times,flux,_,info=S.load(str(path),info=True)
            with fits.open(path,memmap=False) as hdul:
                table=hdul[1].data
                all_times=np.asarray(table['TIME'],float)
                recorded=all_times[np.isfinite(all_times)]
                finite_flux=np.isfinite(table[info['column']])
                if info['column']=='pdcsap_flux':finite_flux |= np.isfinite(table['SAP_FLUX'])
                usable_recorded=all_times[finite_flux & np.isfinite(all_times)]
            cad=np.median(np.diff(times)) if len(times)>1 else np.nan
            if not np.isfinite(cad):states.add('no cadence estimate');continue
            has=lambda t:bool(len(t) and np.min(np.abs(t-centre))<=1.5*cad)
            if not has(recorded):states.add('no recorded cadence');continue
            if not has(times):
                states.add('recorded but lost at quality/finite-flux load')
                details.add('finite archived flux excluded at load' if has(usable_recorded) else 'no finite archived flux')
                continue
            if not info['needs_windows']:
                states.add('raw centre covered');continue
            own=next(folder.glob(f'tess*-s{sector:04d}-{star:016d}-*_lc.fits'),None)
            windows,nn=A.neighbour_windows(sector,m['camera'],m['ccd'],star)
            if own is not None:
                guard.allow_design_file(own);windows=S.good_windows(str(own));details.add('own SPOC')
            elif nn>=2:
                lists=[w for tic,w in A.DB.get((sector,m['camera'],m['ccd']),{}).items() if tic!=star and w]
                untrimmed=intersect_windows(lists,trim_start_d=0)
                if has(times[S.in_windows(times,untrimmed)]) and not has(times[S.in_windows(times,windows)]):details.add('half-day start trim')
                else:details.add('neighbour intersection')
            else:
                states.add('recorded, no safe windows');details.add('too few neighbours');continue
            if has(times[S.in_windows(times,windows)]):states.add('raw centre covered')
            else:
                states.add('recorded outside safe windows')
                if len(S.dumps_for(sector)) and np.min(np.abs(S.dumps_for(sector)-centre))<.5:details.add('near momentum dump (0.5 d)')
        order=['raw centre covered','recorded outside safe windows','recorded, no safe windows','recorded but lost at quality/finite-flux load','no recorded cadence','no cadence estimate']
        category=next((k for k in order if k in states),'missing input')
        counts[category]+=1
        bybin[f'{trial["bin"]}: {category}']+=1
        reasons.update(details)
        sources.update({f'{trial["dip"]["stage"]}: '+next((k for k in order if k in states),'missing input'):1})
result=dict(counts=counts,reasons=reasons,original_stage_crosscheck=sources,bybin=bybin)
(H.OUT/f'window-{name}.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
