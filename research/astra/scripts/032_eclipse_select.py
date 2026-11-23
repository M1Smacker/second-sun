"""Freeze design-only control and injection samples before fitting any flux."""
import importlib
import json
import os
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('032_harness')
O=importlib.import_module('032_outputs')
SOURCE=H.DATA/'stage3_g2'/f'r1dev_g2_seen_{H.DEVELOPMENT_HASH}'


def saved(guard,path,brief):
    if not path.resolve().is_relative_to(guard.data/'astra'/brief):
        raise PermissionError('Saved input path escape')
    guard.reads.add(path.resolve())
    return path.read_text(encoding='utf-8')


def midpoint(path):
    from astropy.io import fits
    with fits.open(path,memmap=False,lazy_load_hdus=True) as hdus:
        for hdu in hdus[:2]:
            h=hdu.header
            if 'TSTART' in h and 'TSTOP' in h:
                t=(float(h['TSTART'])+float(h['TSTOP']))/2
                t+=float(h.get('BJDREFI',2457000))+float(h.get('BJDREFF',0))-2457000
                if 1300<t<10000:
                    return t
    return None


def stratified(items,periods,per_bin,seed=12):
    bins=[[] for _ in range(5)]
    rng=np.random.default_rng(seed)
    for s in sorted(items):
        bins[np.searchsorted([10,14,20,27.4],periods[s],side='right')].append(s)
    shuffled=[list(map(int,rng.permutation(b))) for b in bins]
    selected=[b[:per_bin] for b in shuffled]
    while sum(map(len,selected))<5*per_bin:
        missing=5*per_bin-sum(map(len,selected))
        for i,b in enumerate(shuffled):
            if missing and len(selected[i])<len(b):
                selected[i].append(b[len(selected[i])])
                missing-=1
        if missing==5*per_bin-sum(map(len,selected)) and not any(len(a)<len(b) for a,b in zip(selected,shuffled)):
            if missing:raise RuntimeError('Too few eligible stars')
    return [s for b in selected for s in b],[len(b) for b in selected]


def main():
    os.environ['SS_SET']='g2'
    guard=H.Guard()
    guard.start()
    guard.allow_machine_inputs('g2')
    import pandas as pd
    import petrova_mask as PM
    periods={int(r.tic):r.p_bin_d for r in pd.read_csv(H.TARGETS,comment='#').itertuples()
             if r.list=='g2' and r.design_seen==1}
    affected={int(s) for s in json.loads(saved(guard,H.OUT.with_name('010')/'affected-g2.json','010'))}
    assert len(affected)==112 and affected<=periods.keys()
    sectors={}
    times={}
    for path in sorted((SOURCE/'groups').glob('*.json')):
        star,sec=map(int,path.stem.split('_'))
        if star not in periods:continue
        guard.allow_design_file(path)
        sectors.setdefault(star,set()).add(sec)
        if sec not in times:
            for m in json.loads(path.read_text(encoding='utf-8'))['meta']:
                file=H.DATA/'g2'/str(star)/Path(m['file']).name
                guard.allow_design_file(file)
                t=midpoint(file)
                if t is not None:
                    times[sec]=t
                    break
    assert set.union(*sectors.values())<=times.keys()
    cat=PM.cat()
    eligible=set()
    for s in periods.keys()-affected:
        c=cat.get(s)
        if not c or not sectors.get(s) or not all(np.isfinite(c[k]) and c[k]>0 for k in ('P','T0','eP','eT0')):
            continue
        if all(3*np.hypot(c['eT0'],round((times[k]-c['T0'])/c['P'])*c['eP'])<.05 for k in sectors[s]):
            eligible.add(s)
    old=json.loads(saved(guard,H.OUT.with_name('012')/'samples.json','012'))
    controls=old['controls']
    assert set(controls)<=eligible and old['affected']==sorted(affected)
    holdout,hb=stratified(eligible-set(controls),periods,8,14)
    assert len(set(holdout+controls))==100
    old['holdout']=holdout
    old['holdout_bins']=hb
    O.write_json(H.OUT/'eclipse-samples.json',old)
    print('Fixed seed-14 holdout by bin',hb,flush=True)



if __name__=='__main__':
    main()
