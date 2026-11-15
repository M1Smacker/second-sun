"""Targeted regressions for paired cluster aggregation and no-op subtraction."""
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))


def main():
    H = importlib.import_module('024_harness')
    guard = H.Guard()
    guard.start()
    import numpy as np
    summary = importlib.import_module('024_summary')
    subtraction = importlib.import_module('024_subtract')
    result = subtraction.checks()
    rows = []
    for star in range(20):
        for b in range(5):
            values = [star % 2 == 0] * 4
            rows.append(dict(campaign='synthetic', star=star, bin=b, real=values, flip=values,
                             real_found=values, flip_found=values))
    metric = summary.metric(rows, np)
    assert metric['clusters'] == 20
    assert metric['n'] == [20] * 5
    assert np.array_equal(np.asarray(metric['delta_ci95']), 0 * np.asarray(metric['delta_ci95']))
    assert np.array_equal(np.asarray(metric['control_ci99']), 0 * np.asarray(metric['control_ci99']))
    assert np.allclose(metric['overall'], .5)
    # Duplicating all within-star trials must leave both point rates and intervals unchanged.
    doubled = summary.metric(rows + rows, np)
    assert np.array_equal(metric['ci95'], doubled['ci95'])
    # One common resample must preserve paired identity. Independently resampling arms would fail.
    rng = np.random.default_rng(8675309)
    star_values = np.array([star % 2 == 0 for star in range(20)], dtype=float)
    real_draws = star_values[rng.integers(0, 20, size=(1000, 20))].mean(axis=1)
    flip_draws = star_values[rng.integers(0, 20, size=(1000, 20))].mean(axis=1)
    mutation = real_draws - flip_draws
    assert np.std(mutation) > .05 and np.all(np.asarray(metric['control_ci99']) == 0)
    result.update(cluster_checks=6, duplicated_trials_leave_intervals_identical=True,
                  independently_resampled_arm_mutation_rejected=True)
    (H.OUT / 'checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('Six subtraction and six paired-cluster checks passed, two mutations rejected.')


if __name__ == '__main__':
    main()
