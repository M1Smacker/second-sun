"""Independent direct-window oracle, reference parity, and mutation tests for N1."""
import ast
import importlib
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('030_harness')
N = importlib.import_module('030_notch')


def main():
    os.environ.update(SS_SET='g2', VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    import numpy as np
    import stage2_search as S2
    import stage3_core as C
    C.use_grid(S2, C.GRID_V5)
    objects = S2.Prod, S2.veto, S2.do_group
    N.install(S2, False)
    assert objects == (S2.Prod, S2.veto, S2.do_group)
    reference = H.DATA / 'rs039/a8b_notchmin.py'
    guard.reads.add(reference.resolve())
    tree = ast.parse(reference.read_text(encoding='utf-8'))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'notch_scores')
    scope = dict(X=SimpleNamespace(G=dict(np=np, S2=S2)))
    exec(compile(ast.Module(body=[function], type_ignores=[]), '<isolated reference function>', 'exec'), scope)
    rng = np.random.default_rng(2026111830)
    checked, mutations = 0, 0
    N.install(S2, True)
    for cadence in (2., 10., 30.):
        t = np.arange(0, 6., cadence / 1440)
        f = 1 + rng.normal(0, .001, len(t)) + .002 * np.sin(t * 4)
        f[abs(t - 2.4) < .15] -= .006
        keep = ~((t > 3.1) & (t < 3.4))
        t, f = t[keep], f[keep]
        product = S2.Prod(t, f)
        for duration in C.GRID_V5:
            centers, snr, _ = product.scores(duration)
            refc, refs = scope['notch_scores'](t, f, duration)
            np.testing.assert_allclose(centers, refc, rtol=0, atol=0)
            np.testing.assert_allclose(snr, refs, rtol=1e-11, atol=1e-11, equal_nan=True)
            # Different implementation: slice each window directly, no prefix sums.
            w = max(round(duration / 24 / product.bd), 1)
            gap, flank = max(round(w * .25), 1), max(round(w * 1.5), 1)
            expected = np.full(len(product.bf), np.nan)
            for i in range(len(expected)):
                windows = [product.bf[max(0, a):min(len(expected), b)] if b > 0 else np.array([])
                           for a, b in ((i, i+w), (i-gap-flank, i-gap), (i+w+gap, i+w+gap+flank))]
                clean = [a[np.isfinite(a)] for a in windows]
                if len(clean[0]) >= .8*w and len(clean[1]) >= .6*flank and len(clean[2]) >= .6*flank:
                    expected[i] = min(clean[1].mean(), clean[2].mean()) - clean[0].mean()
                    mutant = max(clean[1].mean(), clean[2].mean()) - clean[0].mean()
                    mutations += abs(mutant - expected[i]) > 1e-6
            np.testing.assert_allclose(product.depths[duration], expected, rtol=0, atol=2e-12, equal_nan=True)
            checked += 1
        low = product.events(4.5)
        for floor in (5., 5.5, 6., 6.5, 7.):
            assert product.events(floor) == [e for e in low if e['snr'] >= floor]
    assert mutations > 0
    e = dict(center=1., dur_h=12.)
    assert N.mirrored(e, [dict(center=1.125)])
    assert not N.mirrored(e, [dict(center=1.125001)])
    assert not N.mirrored(e, [dict(center=1.2)])  # old .3 d mirror must be rejected
    # Degenerate constant data cannot emit infinite-significance events.
    _, degenerate, _ = N.scores(np, np.arange(1000.) / 144, np.ones(1000), 1/144, 6.)
    assert not np.isfinite(degenerate).any()
    # Exercise the actual scorer's nested retier function, without importing main.
    scorer = ast.parse((Path(__file__).parent / '030_n1_score.py').read_text(encoding='utf-8'))
    main_node = next(n for n in scorer.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    retier = next(n for n in main_node.body if isinstance(n, ast.FunctionDef) and n.name == 'retier')
    from collections import defaultdict
    rules = importlib.import_module('023_scoring_rules')
    scope2 = dict(defaultdict=defaultdict, S=rules, N=N, periods={1: 10.}, floor=4.5,
                  C=SimpleNamespace(tier_of=lambda e: '2' if e['flipmatch'] else '1B'))
    exec(compile(ast.Module(body=[retier], type_ignores=[]), '<actual scorer retier>', 'exec'), scope2)
    events = [dict(tic=1, kind=kind, product='synthetic', center=2., dur_h=6., snr=snr,
                   flags='', flipmatch=False) for kind, snr in (('real', 8.), ('flip', 4.75))]
    low = scope2['retier'](events)
    assert len(low) == 2 and all(e['flipmatch'] for e in low)
    scope2['floor'] = 5.
    high = scope2['retier'](events)
    assert len(high) == 1 and not high[0]['flipmatch'] and high[0]['tier'] == '1B'
    # A mutation that filters only after flagging retains the spurious mirror.
    mutant = [e for e in low if e['snr'] >= 5.]
    assert mutant != high
    select = importlib.import_module('030_choose')
    alarm_rows = [dict(floor=f, real=175, upside_down=79) for f in select.FLOORS]
    alarm_rows[1].update(real=174, upside_down=80)
    alarm_rows[2].update(real=174, upside_down=79)
    assert select.choose(alarm_rows) == 5.5
    assert select.choose([dict(r, real=175) for r in alarm_rows]) is None
    assert next(r['floor'] for r in alarm_rows if r['real'] <= 174 or r['upside_down'] <= 79) != select.choose(alarm_rows)
    result = dict(passed=True, cadence_duration_cases=checked, lower_flank_mutation_detections=int(mutations),
                  mirror_boundary_checks=3, threshold_nested_checks=15, off_switch_objects_unchanged=True,
                  reference_function_only=True, constant_data_no_detections=True,
                  threshold_context_mutation_rejected=True, both_arm_choice_mutation_rejected=True)
    (H.OUT / 'notch-checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
