"""Synthetic counterexample to arm parity, plus independent bootstrap arithmetic check."""
import importlib
import json
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('003_harness')
os.environ.update(SS_SET='g2',VESPER_OPTS='c6,p1',NUMBA_NUM_THREADS='2')
guard=H.Guard();guard.start()
import numpy as np
import detect_v2 as D
import stage3_core as C
# Reproduce the two call signatures at stage2_search.py:194-195 on synthetic events.
e=dict(center=0.0,dur_h=6,snr=9,depth_ppm=4000)
opposite=dict(center=.01,dur_h=6,snr=9,depth_ppm=4000)
real,_=D.veto([e],np.array([]),np.array([]),[opposite],flip_action='flag')
flip,_=D.veto([e],np.array([]),np.array([]),[],flip_action='flag')
def tier(event):
    row=dict(flags='; '.join(event['flags']),burst_n=0,c5=False,c8_n=0,c8_best=None,common=False)
    return C.tier_of({**row,**C.flags_of(row)})
assert tier(real[0])=='2' and tier(flip[0])=='1B'
# Cluster-matrix aggregation against explicit duplicated trial records, independent implementation.
toy=[(0,0,1),(0,1,0),(1,0,0),(1,1,1),(2,0,1),(2,1,1)]
cnt=np.zeros((3,2));win=cnt.copy()
for s,b,y in toy:cnt[s,b]+=1;win[s,b]+=y
rng=np.random.default_rng(17);passed=0
for _ in range(200):
    draw=rng.integers(0,3,size=3);w=np.bincount(draw,minlength=3)
    matrix=float(np.mean((w@win)/(w@cnt)))
    expanded=[(b,y) for s in draw for st,b,y in toy if st==s]
    explicit=sum(sum(y for b,y in expanded if b==k)/sum(b==k for b,y in expanded) for k in range(2))/2
    assert abs(matrix-explicit)<1e-14;passed+=1
result=dict(synthetic_opposite_match_real_tier=tier(real[0]),synthetic_opposite_match_flip_tier=tier(flip[0]),
    bootstrap_expansion_checks=passed,limitation='Synthetic control-path counterexample, not its frequency or net effect on real recovery')
(H.OUT/'checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
