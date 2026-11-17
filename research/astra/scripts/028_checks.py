"""Independent forward-root geometry and mutation checks, synthetic only."""
import importlib
import json
import math
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
O=importlib.import_module('028_orbits')
from scipy.optimize import brentq
import numpy as np


def main():
    pb,p,tb,epoch = 10.,61.,2.,5.
    a=O.MU
    ap=(p/pb)**(2/3)
    def sep(t):
        return ap*math.sin(2*math.pi*(t-epoch)/p)-a*math.sin(2*math.pi*(t-tb)/pb)
    ev=[]
    for n in range(6):
        anchor=epoch+n*p
        t=brentq(sep,anchor-3,anchor+3)
        # Independent finite-difference derivative for duration consistency.
        v=abs((sep(t+1e-5)-sep(t-1e-5))/2e-5)
        ev.append(dict(center=t,dur_h=.025/v*24,snr=6.,sector=n))
    result=O.search(ev,pb,tb)
    assert any(len(r['events'])==6 and abs(r['period']-p)<1e-6 for r in result['sets'])
    assert not O.search(ev[:2],pb,tb)['sets']
    assert not O.search([ev[0]]*5,pb,tb)['sets']
    off=[dict(e,center=e['center']+1234) for e in ev]
    assert abs(O.search(off,pb,tb+1234)['max_score']-result['max_score'])<1e-10
    broken=[dict(e,center=e['center']+(.73 if i==2 else 0)) for i,e in enumerate(ev[:3])]
    normal=O.search(broken,pb,tb)
    mutant=O.search(broken,pb,tb,mutation=True)
    assert len(mutant['sets'])>len(normal['sets']), 'Timing mutation was not detected'
    assert len(O.members(result,7,promotion=True))==0
    assert len(O.members(result,7))==6
    # Analytic timing bound tested against independently solved coordinates.
    bound=p/(2*math.pi)*math.asin(a/ap)
    assert all(abs(e['center']-(epoch+n*p))<=bound for n,e in enumerate(ev))
    summary=dict(passed=True,checks=8,stability_period_ratio=O.stability_ratio(),
        synthetic_sets=len(result['sets']),mutation_before=len(normal['sets']),mutation_after=len(mutant['sets']))
    out=Path(r'D:\second-sun-astra\data/astra/028')
    (out/'checks.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary))


if __name__=='__main__': main()
