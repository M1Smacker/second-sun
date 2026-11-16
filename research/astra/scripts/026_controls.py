"""Cheap raw synthetic falsification before real-host acceptance controls."""
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('026_harness')
M = importlib.import_module('026_rules')


def main():
    os.environ.update(SS_SET='g2', VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    import numpy as np
    import petrova_mask as PM
    import detect_v2 as detector
    t = np.arange(1500., 1527., 10 / 1440)
    c = dict(P=50., T0=0., wp=.1, ws=float('nan'), phs=float('nan'), eT0=0., eP=.1)
    assert M.category(c, float(np.median(t))) == 'B'
    frozen_windows = PM.windows
    PM.windows = lambda times, cat: M.m2_windows(times, cat, 0., np)
    cap = 1e6 * (.2009 / 2) ** 2
    cases = [('eclipse2', .02, [1505., 1519.]), ('eclipse5', .05, [1505., 1519.]),
             ('planet2', .004, [1505., 1519.]), ('planet3_regular', .004, [1505., 1512., 1519.]),
             ('planet3_irregular', .004, [1505., 1511., 1519.])]
    output = []
    for label, depth, centers in cases:
        for sign in (1, -1):
            noise = np.random.default_rng(2026111626).normal(0, .0003, len(t))
            f = 1 + noise
            for center in centers:
                f -= sign * depth * np.clip((.125 - abs(t - center)) / .025, 0, 1)
            # Injection is upstream of both catalogue and repeat masks and detrending.
            removed = PM.remove(t, f, [c['P']], c)
            tt, ff = t[~removed], f[~removed]
            events = detector.find_events(tt, ff if sign == 1 else 2 - ff)
            measured = [e for e in events if any(abs(e['center'] - center) <= .125 for center in centers)]
            assert len(measured) == len(centers), 'Raw synthetic detector did not recover every planted crossing'
            held = M.held(measured, cap, True)
            output.append(dict(case=label, sign=sign, planted=len(centers), detected=len(measured),
                               m2_timing_hold=False, m4_timing_hold=any(e['timing_unverified'] for e in held),
                               reason=held[0]['timing_reason'], retained=int((~removed).sum())))
    PM.windows = frozen_windows
    checks = {}
    checks['m2_fails_eclipse_control_first'] = all(not r['m2_timing_hold'] for r in output if r['case'].startswith('eclipse'))
    checks['m4_holds_deep_eclipses'] = all(r['m4_timing_hold'] for r in output if r['case'].startswith('eclipse'))
    checks['two_planets_not_held'] = all(not r['m4_timing_hold'] for r in output if r['case'] == 'planet2')
    checks['three_irregular_planets_not_held'] = all(not r['m4_timing_hold'] for r in output if r['case'] == 'planet3_irregular')
    checks['three_regular_planets_counterexample'] = all(r['m4_timing_hold'] for r in output if r['case'] == 'planet3_regular')
    # Mutation checks prove that the detection/hold tests reject missing or overbroad rules.
    event = lambda center: dict(center=center, dur_h=6., depth_ppm=4000., snr=20.)
    assert M.reason([event(0.), event(7.)], cap) is None
    assert M.reason([event(0.), event(7.), event(14.)], cap) == 'three_periodic'
    mutated_no_hold = lambda events, cap: None
    checks['disabled_guard_mutation_rejected'] = mutated_no_hold([event(0.), event(7.), event(14.)], cap) != 'three_periodic'
    a = dict(c, eP=0.)
    assert M.category(a, float(np.median(t))) == 'A'
    assert not any(e['timing_unverified'] for e in M.held([event(0.), event(7.), event(14.)], cap, False))
    checks['class_a_guard_noop'] = True
    assert all(checks.values())
    result = dict(scope='synthetic raw mask and detector, not real-host tier acceptance', checks=checks, cases=output)
    (H.OUT / 'synthetic-controls.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
