"""Synthetic duration routing, merging, diagnostic-curve and mutation checks."""
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('031_harness')
M = importlib.import_module('031_detector')
N = importlib.import_module('031_notch')


def main():
    os.environ.update(SS_SET='g2', VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    import numpy as np
    import stage2_search as S2
    import stage3 as S3
    import stage3_core as C
    C.use_grid(S2, C.GRID_V5)
    original = S2.Prod, S2.veto, S2.do_group, S3.add_step
    rng = np.random.default_rng(2026112231)
    t = np.arange(0, 8, 10/1440)
    f = 1 + rng.normal(0, .001, len(t)) + .002*np.sin(t*2)
    f[abs(t-2) < .08] -= .008
    f[abs(t-5) < .3] -= .006
    baseline = S2.Prod(t, f)
    assert M.install(S2, S3, 0.) == 'B'
    assert original == (S2.Prod, S2.veto, S2.do_group, S3.add_step)
    assert S2.Prod(t, f).events() == baseline.events()
    N.install(S2, True, floor=4.5)
    reference = S2.Prod(t, f)
    reference_events = reference.events()
    S2.Prod, S2.veto, S2.do_group, S3.add_step = original
    assert M.install(S2, S3, 21.) == 'N1'
    assert S2.Prod(t, f).events() == reference_events
    S2.Prod, S2.veto, S2.do_group, S3.add_step = original
    assert M.install(S2, S3, 8.) == 'D1'
    hybrid = S2.Prod(t, f)
    candidates = []
    for duration in C.GRID_V5:
        reference_product = reference if duration <= 8 else baseline
        for actual, expected in zip(hybrid.scores(duration), reference_product.scores(duration)):
            np.testing.assert_array_equal(actual, expected)
        centers, significance, mean = reference_product.scores(duration)
        threshold = 6.5 if duration <= 8 else 7.
        for i, snr in enumerate(significance):
            if np.isfinite(snr) and snr >= threshold:
                depth = (reference_product.depths[duration][i] if duration <= 8 else reference_product.med-mean[i])*1e6
                candidates.append(dict(center=float(centers[i]), dur_h=duration, snr=float(snr), depth_ppm=float(depth)))
    def oracle(normalize):
        ordered = sorted(candidates, key=lambda e: (e['snr']/(6.5 if e['dur_h'] <= 8 else 7.) if normalize else e['snr'],
                         e['center'], e['dur_h'], e['depth_ppm']), reverse=True)
        result = []
        while ordered:
            selected = ordered.pop(0)
            result.append(selected)
            ordered = [e for e in ordered if abs(e['center']-selected['center']) > max(e['dur_h'], selected['dur_h'])/48+.1]
        return result
    assert hybrid.events() == oracle(True)
    # Deliberately close scores expose a wrong raw-SNR sorting implementation.
    candidates = [dict(center=1., dur_h=6., snr=6.8, depth_ppm=1.), dict(center=1., dur_h=10., snr=7.1, depth_ppm=1.)]
    assert oracle(True) != oracle(False)
    # Feed controlled score arrays through the actual hybrid candidate merger.
    actual_grid=S2.DURS_H
    S2.DURS_H=(8.,10.)
    short=type('Short',(),{'depths':{8.:np.array([.001,.001])},
                         'scores':lambda self,d:(np.array([1.,4.]),np.array([6.8,6.49]),np.ones(2))})()
    long=type('Long',(),{'med':1.,'meds':{},
                       'scores':lambda self,d:(np.array([1.,5.]),np.array([7.1,6.99]),np.ones(2)-.001)})()
    hybrid.for_duration=lambda d:short if d<=8 else long
    chosen=hybrid.events()
    assert len(chosen)==1 and chosen[0]['dur_h']==8., 'Actual normalized merge or thresholds failed'
    S2.DURS_H=actual_grid
    # The two sides of a mixed short/long pair intentionally use different mirrors.
    short_event=dict(center=1.,dur_h=8.,snr=8.,depth_ppm=1.)
    long_event=dict(center=1.2,dur_h=10.,snr=8.,depth_ppm=1.)
    kept,_=S2.veto([short_event],np.array([]),np.array([]),[long_event],flip_action='flag')
    reverse,_=S2.veto([long_event],np.array([]),np.array([]),[short_event],flip_action='flag')
    assert not kept[0]['flags'] and any('matched in flipped' in flag for flag in reverse[0]['flags'])
    # Exercise the actual step wrapper and record the curve selected per event.
    calls = []
    S2.prepare = lambda _: (dict(t=t, f=f, meta={'product':'synthetic'}, edges=np.array([])), {})
    C.step_stats = lambda bt, bf, bd, med, center, duration, depth: calls.append((duration, bf.copy())) or {}
    group = {'events':[dict(product='synthetic', kind='real', center=2., dur_h=d, depth_ppm=1.) for d in (8., 10.)]}
    S3.add_step(group, ['synthetic'])
    assert len(calls) == 2
    np.testing.assert_array_equal(calls[0][1], reference.bf)
    np.testing.assert_array_equal(calls[1][1], baseline.bf)
    assert not np.array_equal(reference.bf, baseline.bf), 'Wrong-curve mutation must be detectable'
    e = dict(center=1., dur_h=8.)
    assert N.mirrored(e, [{'center':1.+8/96}])
    assert not N.mirrored(e, [{'center':1.2}])
    result = dict(status='passed', grid=list(C.GRID_V5), short_boxes=[d for d in C.GRID_V5 if d <= 8],
                  long_boxes=[d for d in C.GRID_V5 if d > 8], score_array_identities=len(C.GRID_V5)*3,
                  endpoint_event_identities=2, merge_oracle=True, diagnostic_curves=2,
                  actual_controlled_merge=True,actual_mixed_mirrors=True,
                  mutations_rejected=['raw-SNR ordering', 'one diagnostic curve for both statistics'],
                  scope='synthetic producer checks; full historical tier identities still required')
    (H.OUT/'detector-checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
