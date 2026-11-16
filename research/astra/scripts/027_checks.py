"""Rule boundary and deliberate-mutation checks, using synthetic events only."""
import ast
import importlib
import itertools
import json
import math
import os
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('027_harness')


def main():
    os.environ.update(SS_SET='g2',VESPER_OPTS='c6,p1',NUMBA_NUM_THREADS='2')
    guard=H.Guard()
    guard.start()
    import stage3_core as C
    new=importlib.import_module('027_score')
    # Extract only pure rule functions from X10; never execute its imports or main.
    src=H.DATA/'fable/f4/x10_score.py'
    guard.reads.add(src.resolve())
    tree=ast.parse(src.read_text(encoding='utf-8'))
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('finite','truth','decision')]
    assert len(funcs)==3
    scope=dict(math=math,S=new.S,LABELS=new.LABELS)
    exec(compile(ast.Module(body=funcs,type_ignores=[]),'<extracted X10 pure rules>','exec'),scope)
    count,mutation=0,0
    base=dict(center=100.,dur_h=6.,sector=1,snr=12.,depth_ppm=3000.,gap_dump=False,burst=False,
        flipmatch=False,c5=False,ecl_overlap=False,repeater=False,orbit_lock=False,step=False,ramp=False,
        dominated=False,c8_n=0,c8_best=None,p1_veto=False,lift_pre=.1,lift_post=.1,flags='')
    for flag,lift,step,ramp,known,cap in itertools.product(('', 'gap edge', 'momentum dump', 'momentum dump; gap edge'),
            (.25,.250001,None), (False,True),(False,True),(False,True),(None,2999.,3000.)):
        e=dict(base,flags=flag,gap_dump=bool(flag),lift_pre=lift,step=step,ramp=ramp)
        intervals={1:[(99.9,100.1)]} if known else {}
        old=scope['decision'](e,0,{0:e},intervals,cap,C.tier_of)
        actual=new.decision(e,0,{0:e},intervals,cap,C.tier_of)
        assert actual==[old[0],old[1],old[2],old[29]], 'Rule mismatch'
        # Mutation: omit C96 for K2. At least one synthetic case must reject it.
        mutant=new.decision(e,0,{0:e},intervals,None,C.tier_of)
        mutation+=actual[3]!=mutant[3]
        count+=1
    assert mutation>0
    result=dict(rule_cases=count,cap_mutation_rejections=mutation,passed=True)
    (H.OUT/'rule-checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':
    main()
