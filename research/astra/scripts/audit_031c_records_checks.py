"""Exercise the actual records loop without pipeline imports or real light.

Run with the project Python, -I -B. Writes counts only under data/astra/031.
"""
import ast
from collections import Counter
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/031'
SOURCE = ROOT / 'research/astra/scripts/031_records.py'


def check(source):
    tree = ast.parse(source)
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    loop = next(n for n in main.body if isinstance(n, ast.For)
                and ast.unparse(n.iter) == "t156['trials']")
    # Two empty products in distinct bins, one nonempty product, one other campaign.
    trials = [dict(star=1, sector=i, campaign='g2', bin=b,
                   phase_fraction=.25, duration_h=6)
              for i, b in enumerate((0, 3, 4))]
    trials.append(dict(trials[0], campaign='g3'))
    groups = {(1, i): [('groups', dict(meta=[dict(product='test', slot=i)], events=[]))]
              for i in range(3)}
    frame = pd.DataFrame(columns=['tic', 'sector', 'camera', 'kind', 'primary', 'center'])
    env = dict(t156=dict(trials=trials), campaign='g2',
               guard=SimpleNamespace(seen={'g2': {'1'}}), groups=groups,
               bestmap={}, times=lambda star, m: np.array([] if m['slot'] < 2 else [10., 14.]),
               context=frame, R=SimpleNamespace(apply_v7=lambda x: x, merge_sap=lambda x: x),
               newt156=[], excluded=Counter(), raw={})
    exec(compile(ast.Module(body=[loop], type_ignores=[]), str(SOURCE), 'exec'), env)
    assert dict(env['excluded']) == {0: 1, 3: 1}
    assert len(env['newt156']) == 1
    row = env['newt156'][0]
    assert row['time'] == 11. and row['bin'] == 4
    assert row['dip'] == row['bump'] == dict(preexisting=False)
    # The fresh path already excludes no-time draws through observed=[], identically
    # to a nonempty span with no observed crossing. Test the actual function body.
    fresh = next(n for n in main.body if isinstance(n, ast.FunctionDef) and n.name == 'fresh_record')
    fresh_env = dict(guard=SimpleNamespace(seen={'g2': {'1'}}), campaign='g2',
                     Orbit=lambda **kw: SimpleNamespace(crossings=lambda lo, hi: [(12., 1.)]),
                     bestmap={}, groups={(1, 0): [('groups', dict(meta=[dict(file='test')]))]},
                     times=lambda *args: np.array([]), raw={}, np=np)
    exec(compile(ast.Module(body=[fresh], type_ignores=[]), str(SOURCE), 'exec'), fresh_env)
    job = dict(star=1, sectors=[0], binary_period=1, binary_epoch=0,
               planet_period=10, planet_epoch=0)
    empty = fresh_env['fresh_record'](job)
    assert empty['observed'] == empty['changed'] == []
    fresh_env['times'] = lambda *args: np.array([10., 14.])
    assert fresh_env['fresh_record'](job) == empty
    fresh_env['times'] = lambda *args: np.array([10., 12., 14.])
    seen = fresh_env['fresh_record'](job)
    assert seen['observed'] == [(12., 1.)] and seen['changed'] == [0]


def main():
    source = SOURCE.read_text(encoding='utf-8')
    check(source)
    mutant = source.replace('if not len(t):', 'if False:', 1)
    assert mutant != source
    try:
        check(mutant)
    except (AssertionError, ValueError):
        pass
    else:
        raise AssertionError('Disabled-exclusion mutation survived')
    result = dict(status='passed', t156_empty_exclusions=2, nonempty_center_unchanged=True,
                  other_campaign_ignored=True, fresh_cases=3, disabled_exclusion_rejected=True,
                  scope='Synthetic execution of extracted actual records code; no pipeline imports')
    (OUT/'031c-records-checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
