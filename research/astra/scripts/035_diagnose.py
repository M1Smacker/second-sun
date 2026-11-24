"""Bounded synthetic root-cause study after two failed precision checks.

Compare BLS objectives at the same periods and durations. No real light,
no thresholds changed, and no production correction is made by this script.
"""
import importlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
P = importlib.import_module('035_period')
np = P.np


def main():
    t = np.arange(0, 27, 1/720)
    f = 1 + np.random.default_rng(35).normal(0, .0002, len(t))
    phase = (t-1) % 4
    f[np.minimum(phase, 4-phase) < .12] -= .02
    f[abs(phase-2) < .12] -= .01
    streams = P.OLD['streams_for_fit']([(1, 0, 'SPOC', t, f)])
    tt, ff = P.OLD['combined'](streams)
    bls = P.BoxLeastSquares(tt, ff, dy=P.OLD['robust_sigma'](ff))
    grid = np.linspace(3.98, 4.02, 4001)
    evidence = []
    for objective in ('snr', 'likelihood'):
        for durations in ([.192, .32], [.24]):
            power = bls.power(grid, durations, objective=objective, oversample=20)
            i, truth = int(np.argmax(power.power)), int(np.argmin(abs(grid-4)))
            evidence.append(dict(objective=objective, durations=durations,
                                 selected_period=float(grid[i]),
                                 fractional_error=float(abs(grid[i]/4-1)),
                                 selected_score=float(power.power[i]),
                                 truth_score=float(power.power[truth]),
                                 selected_duration=float(power.duration[i])))
    result = dict(cases=evidence, real_light_opened=False,
                  inference='Diagnostic only; full finder still fails its synthetic precision test')
    (P.OUT/'diagnostic.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
