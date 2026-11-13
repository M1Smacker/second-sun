"""Run identical three design groups with pinned old or current p1-off sources."""
import importlib
import hashlib
import json
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('002_harness')

def main(mode):
    os.environ.update(SS_SET='g3',VESPER_OPTS='c6',NUMBA_NUM_THREADS='2')
    guard=H.Guard(); guard.start(); refs=guard.allow_machine_inputs('g3')
    if mode=='v81':
        base=H.OUT/'v81'
        for name,p in json.loads((base/'provenance.json').read_text(encoding='utf-8')).items():
            assert hashlib.sha256((base/name).read_bytes()).hexdigest()==p['adapted_sha256']
        sys.path.insert(0,str(base))
    import stage3 as S3
    import stage2_search as S2
    import stage3_core as C
    source=H.DATA/'stage3_g3'/f'r1dev_g3_seen_{H.DEVELOPMENT_HASH}'/'groups'
    selected=[p for p in sorted(source.glob('*.json')) if p.stem.split('_')[0] in guard.seen['g3']][:3]
    output=[]
    for i,path in enumerate(selected):
        guard.allow_design_file(path); old=json.loads(path.read_text(encoding='utf-8'))
        star,sector=map(int,path.stem.split('_'))
        paths=[H.DATA/'g3'/str(star)/m['file'] for m in old['meta']]
        for p in paths: guard.allow_design_file(p)
        dest=H.OUT/f'off_{mode}'/str(i); dest.mkdir(parents=True,exist_ok=True)
        S3._init3(dest,'g3',C.GRID_V5); S2.S['spoc_by_sector']={s:str(p) for s,p in refs.items()}
        fresh=S3.do_group3((star,sector,list(map(str,paths))))
        value=json.loads(Path(fresh).read_text(encoding='utf-8'))
        if any(str(m.get('status','')).startswith('ERROR') for m in value['meta']): raise RuntimeError('Processing error')
        output.append(value['events'])
    (H.OUT/f'off-{mode}.json').write_text(json.dumps(output),encoding='utf-8')
    print('Completed',mode,'three primary groups')

if __name__=='__main__': main(sys.argv[1])
