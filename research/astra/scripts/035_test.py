"""Synthetic-only checks; no validation star light is opened."""
import importlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
P = importlib.import_module('035_period')
np = P.np


def raw(t, f):
    return [(1, 0, 'SPOC', t, f)]


def main():
    checks = []
    assert len(P.NAMES) == 7
    checks.append('seven inherited function AST identities against 032b')
    t = np.arange(0, 27, 1/720)
    rng = np.random.default_rng(35)
    f = 1 + rng.normal(0, .0002, len(t))
    for centers, expected in [([], 'no_eclipse'), ([4], 'single_eclipse'),
                              ([4, 21], 'two_eclipses')]:
        y = f.copy()
        for center in centers:
            y[abs(t-center) < .12] -= .02
        result = P.find_period(raw(t, y))
        assert result['period'] is None and result['quality'] == expected, result
    checks.append('zero, one and two injected raw eclipses never yield period')
    # Unequal primary/secondary depths give a falsifiable parity control.
    phase = (t-1) % 4
    y = f.copy()
    y[np.minimum(phase, 4-phase) < .12] -= .02
    y[abs(phase-2) < .12] -= .01
    normal = P.find_period(raw(t, y))
    broken = P.find_period(raw(t, y), mutate_alias=True)
    measured = dict(normal_period=normal['period'], mutation_period=broken['period'])
    # Record evidence even when the requested mutation does not distinguish.
    correct = normal['period'] is not None and abs(normal['period']/4-1) <= .001
    half = broken['period'] is not None and abs(broken['period']/2-1) <= .001
    evidence = dict(checks=checks, synthetic_correct=correct,
                    alias_mutation_increases_half_errors=bool(correct and half),
                    synthetic=measured, alias_source_sha256=P.ALIAS_SOURCE_SHA256)
    (P.OUT/'synthetic-tests.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
    print(json.dumps(evidence))
    assert correct, 'Synthetic binary not recovered'
    assert half, 'Alias mutation did not demonstrate increased half-period errors'


if __name__ == '__main__':
    main()
