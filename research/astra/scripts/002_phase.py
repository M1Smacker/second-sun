"""Design-only catalogue phase diagnostic, bands fixed in report before reads."""
import importlib
import json
import os
from pathlib import Path
import shutil
import sys
import uuid
sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('002_harness')

def main(name):
    os.environ.update(SS_SET=name,VESPER_OPTS='c6,p1',NUMBA_NUM_THREADS='2')
    guard=H.Guard(); guard.start(); guard.allow_machine_inputs(name)
    import numpy as np
    import stage3_report as R
    import petrova_mask as PM
    source=H.DATA/f'stage3_{name}'/f'r1dev_{name}_seen_{H.DEVELOPMENT_HASH}'
    dest=H.OUT/f'phase_{name}_{uuid.uuid4().hex[:8]}'
    copied=0
    for group in ('groups','groups_sap'):
        (dest/group).mkdir(parents=True)
        for path in sorted((source/group).glob('*.json')):
            if path.stem.split('_')[0] not in guard.seen[name]:
                continue
            guard.allow_design_file(path); shutil.copyfile(path,dest/group/path.name); copied+=1
    (dest/'v7.json').write_text('{}',encoding='utf-8')
    ev,_=R.load(str(dest/'groups'))
    selected=ev[ev.primary & ev.tier.isin(['1A','1B','1L']) & (ev.snr>=7) & (ev.recovered==True) & ~ev['product'].str.endswith('-SAP')]
    cat=PM.cat(); counts={}; missing=0
    for _,e in selected.iterrows():
        c=cat.get(int(e.tic))
        if c is None or not np.isfinite(c['wp']):
            missing+=1; continue
        P=c['P']; sec_ok=np.isfinite(c['phs']) and np.isfinite(c['ws'])
        distances=[]
        for phase,width in ((0,c['wp']),(c['phs'] if sec_ok else .5,c['ws'] if sec_ok else c['wp'])):
            distance=abs(((e.center-c['T0']-phase*P+P/2)%P)-P/2)
            distances.append(distance/width)
        b=next((i for i,(lo,hi) in enumerate(zip([5,10,14,20,27.4],[10,14,20,27.4,np.inf])) if lo<=P<hi),-1)
        for k in (0,.75,1,1.5,2):
            if min(distances)>k:
                key=f'{b}|{k}|{e.kind}'; counts[key]=counts.get(key,0)+1
    result=dict(campaign=name,copied_groups=copied,selected=len(selected),missing_catalogue=missing,
                totals={kind:int((selected.kind==kind).sum()) for kind in ('real','flip')},counts=counts)
    (H.OUT/f'phase-{name}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    main(sys.argv[1])
