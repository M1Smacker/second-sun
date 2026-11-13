"""Three design-seen SAP replays, with PDCSAP checking, private detail only."""
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
    import pandas as pd
    import stage3 as S3
    import stage2_search as S2
    import stage3_core as C
    import sap_twin as T
    source=H.DATA/'stage3_g3'/f'r1dev_g3_seen_{H.DEVELOPMENT_HASH}'/'groups_sap'
    selected=[p for p in sorted(source.glob('*.json')) if p.stem.split('_')[0] in guard.seen['g3']][:3]
    best=pd.read_csv(C.BEST).set_index(['tic','sector'])['product'].to_dict()
    dest=H.OUT/('sap_replay_'+uuid.uuid4().hex[:8]); dest.mkdir()
    summary=[]
    for index,path in enumerate(selected,1):
        guard.allow_design_file(path); old=json.loads(path.read_text(encoding='utf-8'))
        star,sector=map(int,path.stem.split('_'))
        raw=list(dict.fromkeys(H.DATA/'g3'/str(star)/m['file'].removesuffix(T.SUFFIX) for m in old['meta']))
        for p in raw: guard.allow_design_file(p)
        folder=dest/str(index); folder.mkdir()
        S3._init3(folder,'g3',C.GRID_V5)
        S2.S['spoc_by_sector']={s:str(p) for s,p in refs.items()}
        fresh=S3.do_group3((star,sector,[str(p)+T.SUFFIX for p in raw]))
        S3.add_pdc((fresh,list(map(str,raw)),best[star,sector]))
        new=json.loads(Path(fresh).read_text(encoding='utf-8'))
        equal=canonical(old['events'])==canonical(new['events'])
        errors=sum(str(m.get('status','')).startswith('ERROR') for m in new['meta'])
        row=dict(group=index,expected=len(old['events']),actual=len(new['events']),equal=equal,errors=errors)
        summary.append(row); print(json.dumps(row),flush=True)
        (dest/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
        if not equal or errors:
            raise RuntimeError('SAP replay mismatch' if not equal else 'SAP processing error')
    assert len(summary)==3

if __name__=='__main__':
    try: main()
    except Exception: traceback.print_exc(); sys.exit(1)
