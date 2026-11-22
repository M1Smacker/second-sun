"""Exercise actual mixed retier definitions without opening any light curves."""
import ast
from collections import defaultdict
import importlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

sys.path.insert(0,str(Path(__file__).parent))
ROOT=Path(r'D:\second-sun-astra')
OUT=ROOT/'data/astra/031'


def main():
    tree=ast.parse((Path(__file__).parent/'031_mixed_score.py').read_text(encoding='utf-8'))
    outer=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    fn=next(n for n in outer.body if isinstance(n,ast.FunctionDef) and n.name=='retier')
    scope=dict(defaultdict=defaultdict,version='D1',strict=False,FLIP_D=.3,periods={1:10.},
               S=importlib.import_module('023_scoring_rules'),N=importlib.import_module('031_notch'),
               C=SimpleNamespace(tier_of=lambda e:'2' if e['flipmatch'] else '1B'))
    exec(compile(ast.Module(body=[fn],type_ignores=[]),'<actual mixed retier>','exec'),scope)
    def event(kind,center,duration,snr,mirror=False):
        return dict(tic=1,kind=kind,product='synthetic',center=center,dur_h=duration,snr=snr,flipmatch=mirror,flags='')
    sample=[event('real',1.,8.,6.6),event('flip',1.2,10.,7.1,True),event('real',4.,10.,6.9)]
    result=scope['retier'](sample)
    assert len(result)==2 and not result[0]['flipmatch'] and result[1]['flipmatch']
    assert result[0]['tier']=='1B' and result[1]['tier']=='2'
    # Mirror threshold filtering occurs before re-tiering, not after.
    sample=[event('real',1.,8.,6.6),event('flip',1.,8.,6.4)]
    assert len(scope['retier'](sample))==1 and not scope['retier'](sample)[0]['flipmatch']
    sample[1]['snr']=6.5
    assert all(e['flipmatch'] for e in scope['retier'](sample))
    # A deliberate long-box threshold mutation must be rejected.
    assert not scope['retier']([event('real',2.,10.,6.9)])
    scope['version']='N1'
    assert len(scope['retier']([event('real',2.,10.,6.9)]))==1
    (OUT/'retier-checks.json').write_text(json.dumps(dict(status='passed',checks=5,
        mutation='long box at N1 threshold detected',scope='actual retier AST; synthetic events')),encoding='utf-8')
    print('Five synthetic mixed-tier checks passed, including threshold mutation.')


if __name__=='__main__':
    main()
