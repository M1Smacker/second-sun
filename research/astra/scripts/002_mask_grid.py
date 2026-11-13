"""Predefined synthetic mask/arm and cross-sector veto audit."""
import importlib
import json
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('002_harness')

def main():
    os.environ['NUMBA_NUM_THREADS']='2'
    g=H.Guard(); g.start()
    import numpy as np
    import pandas as pd
    import petrova_mask as p
    rng=np.random.default_rng(20261113)
    results=[]
    for period in (5,10,14,20,30,50):
        for sectors in (1,2,4):
            row=dict(period=period,sectors=sectors,cadences=0,kept=0,mirror_differences=0,dip_total=0,dip_kept=0,bump_kept=0)
            c=dict(P=period,T0=1.,wp=.2,ws=.15,phs=.5,eT0=0.,eP=0.)
            for sector in range(sectors):
                t=np.arange(0,27.4,2/1440)+sector*29
                phase=(t-c['T0'])%period
                f=1+rng.normal(0,.001,len(t))
                f[np.minimum(phase,period-phase)<.1]-=.02
                f[np.abs(phase-period/2)<.075]-=.01
                # Fixed time relative to each sector, includes masked times by design.
                inj=np.abs(t-(sector*29+12.345))<4/24
                dip=f-.004*inj; bump=f+.004*inj
                mask=p.remove(t,dip,[period],c)
                mirror=p.remove(t,2-dip,[period],c)
                bm=p.remove(t,bump,[period],c)
                row['cadences']+=len(t); row['kept']+=int((~mask).sum())
                row['mirror_differences']+=int((mask!=mirror).sum())
                row['dip_total']+=int(inj.sum()); row['dip_kept']+=int((inj&~mask).sum()); row['bump_kept']+=int((inj&~bm).sum())
            results.append(row)
    veto=[]
    for period in (12.9,13.,20.):
        for phases in ((3.,),(3.,3.),(3.,3.,11.),(3.,3.,11.,15.),(3.,3.,3.,15.)):
            rows=[dict(tic=1,kind=kind,sector=i,center=period*i+ph,dur_h=2.,depth_ppm=4000.,p1_P=period,p1_T0=0.,p1_off=0.)
                  for kind in ('real','flip') for i,ph in enumerate(phases)]
            v=p.veto_events(pd.DataFrame(rows))
            n=len(phases)
            assert list(v[:n])==list(v[n:])
            veto.append(dict(period=period,sectors=n,pattern=list(phases),real_veto=int(v[:n].sum()),flip_veto=int(v[n:].sum())))
    output=dict(grid=results,veto=veto)
    (H.OUT/'mask-grid.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps(output,indent=2))

if __name__=='__main__':
    main()
