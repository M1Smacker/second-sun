"""Counts-only flag attribution on matched injected events, without rerunning any light."""
import argparse
import importlib
import json
import os
from pathlib import Path
import sys
from collections import Counter
sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('003_harness')
def main(name):
    os.environ.update(SS_SET=name,VESPER_OPTS='c6,p1',NUMBA_NUM_THREADS='2')
    guard=H.Guard();guard.start();guard.allow_machine_inputs(name)
    import numpy as np
    import pandas as pd
    import stage3_core as C
    import stage3_report as R
    import stage3 as S3
    folder=H.OUT/'diagnosis'/name;folder.mkdir(parents=True,exist_ok=True)
    S3._init3(folder,name,C.GRID_V5)
    best=pd.read_csv(C.BEST)[['tic','sector','product']].rename(columns={'product':'best'})
    source=H.DATA/f'stage3_{name}'/f'r1dev_{name}_seen_{H.DEVELOPMENT_HASH}'
    events=[]
    for kind in ('groups','groups_sap'):
        for p in (source/kind).glob('*.json'):
            if p.stem.split('_')[0] not in guard.seen[name]:continue
            guard.allow_design_file(p);events.extend(json.loads(p.read_text(encoding='utf-8'))['events'])
    context=pd.DataFrame(events).merge(best,on=['tic','sector'],how='left')
    context['primary']=context['product']==context['best'];context['c8_best']=pd.to_numeric(context.c8_best,errors='coerce')
    flags=['gap_dump','common','flipmatch','c5','ecl_overlap','repeater','orbit_lock','step','ramp','dominated','p1_veto']
    counts=Counter();removal=Counter();checked=0
    for journal in (H.OUT/'workers').glob(f'{name}-*/results-*.jsonl'):
        for line in journal.read_text(encoding='utf-8').splitlines():
            trial=json.loads(line)
            if trial['dip']['recovered'] or trial['dip']['stage']!=4:continue
            checked+=1;star=trial['star'];sector=trial['sector'];evs=[]
            for kind in ('groups','groups_sap'):
                p=journal.parent/f'trial-{trial["trial"]}-1'/kind/f'{star}_{sector}.json'
                if p.exists():evs.extend(json.loads(p.read_text(encoding='utf-8'))['events'])
            cameras={e['camera'] for e in evs}
            sub=context[(context.tic==star)|((context.sector==sector)&context.camera.isin(cameras))].copy()
            new=pd.DataFrame(evs);new['best']=trial['product'];new['primary']=new['product']==new['best'];new['c8_best']=pd.to_numeric(new.c8_best,errors='coerce')
            combined=pd.concat([sub[~((sub.tic==star)&(sub.sector==sector))],new],ignore_index=True)
            scored=R.apply_v7(R.merge_sap(combined))
            near=scored[(scored.tic==star)&(scored.sector==sector)&(scored.kind=='real')&(np.abs(scored.center-trial['time'])<=trial['duration_h']/48)]
            primary=near[near.primary&(near.snr>=7)]
            if not len(primary):counts['no_primary_snr7']+=1;continue
            if trial['dip']['preexisting']:counts['preexisting']+=1;continue
            records=primary.to_dict('records')
            for flag in flags:
                if any(pd.notna(e.get(flag)) and bool(e.get(flag)) for e in records):counts[flag]+=1
                if any(C.tier_of({**e,flag:False}) in ('1A','1L','1B') for e in records):removal[flag]+=1
            if any(e['tier']=='3' for e in records):counts['second_product_disagreement']+=1
    result=dict(campaign=name,stage4_trials=checked,flags_present=dict(counts),single_flag_removal_static=dict(removal),
        limitation='Overlapping flags; removal holds all other event and cross-event features fixed, not an executable new filter or calibrated gain')
    (H.OUT/f'diagnosis-{name}.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--campaign',choices=['g2','g3'],required=True);main(p.parse_args().campaign)
