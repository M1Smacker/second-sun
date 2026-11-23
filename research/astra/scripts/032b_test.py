"""Synthetic leakage, prediction-boundary, source identity and guard checks."""
import ast
import copy
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
J = importlib.import_module('032b_holdout')
H = importlib.import_module('032b_harness')
S = Path(__file__).parent


def main():
    checks = []
    events = [dict(cycle=n, time=2000.+7*n, error=.01, sector=1+n//4, product='SPOC') for n in range(12)]
    track = dict(events=events, epoch_seed=2000., width=1.)
    a = J.judge(track, 7., {})
    assert a['eligible'] and a['usable'] and a['predicts']
    assert a['held_sector'] == 3 and a['n_train'] == 8 and a['n_held'] == 4
    shifted = copy.deepcopy(track)
    for e in shifted['events']:
        if e['sector'] == 3:
            e['time'] += .75
    b = J.judge(shifted, 7., {})
    assert a['train'] == b['train'] and b['usable'] and not b['predicts']
    checks.append('held-out timing mutation leaves training fit identical and changes verdict')
    assert J.predicts([0., .25, .5]) and not J.predicts([0., .25, .500001])
    assert not J.predicts([.250001, .250001]) and not J.predicts([])
    checks.append('median and every-eclipse limits including exact boundaries')
    short = copy.deepcopy(track)
    short['events'] = [e for e in events if e['sector'] < 3]
    assert not J.judge(short, 7., {})['eligible']
    bad_train = copy.deepcopy(track)
    for e in bad_train['events']:
        if e['sector'] < 3:
            e['time'] += .4*(-1)**e['cycle']
    assert not J.judge(bad_train, 7., {})['usable']
    checks.append('three measured sectors required and usability based on training only')
    assert J.rules(50,40,36,30)['passed']
    for args in [(50,39,39,30),(50,40,35,30),(50,40,36,29),(0,0,0,30)]:
        assert not J.rules(*args)['passed']
    checks.append('H1 H2 H3 and empty denominator failures')
    for name, names in [('eclipse_fit',None),('eclipse_calibrate',['trap','family']),('eclipse_select',['stratified','midpoint'])]:
        def functions(prefix):
            tree = ast.parse((S/f'{prefix}_{name}.py').read_text(encoding='utf-8'))
            return {n.name:ast.dump(n) for n in tree.body if isinstance(n,ast.FunctionDef)}
        old, new = functions('032'), functions('032b')
        for n in names or old:
            assert old[n] == new[n]
    checks.append('032 measurement alias trap and allocation function identity')
    guard = H.Guard(); provenance = guard.start()
    for path, flags in [(H.OUT.with_name('032')/'probe',os.O_WRONLY),
                        (H.DATA/'g1/probe.fits',os.O_RDONLY),
                        (H.ROOT/'AGENTS.md',os.O_WRONLY),
                        (H.OUT/'../probe',os.O_WRONLY)]:
        try:
            sys.audit('open',str(path),None,flags)
        except PermissionError:
            continue
        raise AssertionError('Forbidden path allowed')
    checks.append('four simulated forbidden accesses rejected without opening targets')
    files = sorted(S.glob('032b_*.py'))+sorted((S/'032b_harness').glob('*.py'))
    for path in files:
        ast.parse(path.read_text(encoding='utf-8'))
    evidence = dict(checks=checks, parsed_files=len(files), copied_module_hashes=len(provenance),
                    hashes={p.relative_to(S).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
    (H.OUT/'tests.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    print('Six runtime/source verification groups passed; held-out mutation rejected; four guarded accesses rejected.')


if __name__ == '__main__':
    main()
