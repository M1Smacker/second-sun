"""Fixed phase-median subtraction, applied after the unchanged eclipse mask."""
import numpy as np


def correct(t, flux, period, origin, span):
    if not np.isfinite(period) or period <= 0:
        return flux.copy(), dict(status='invalid_period', bins=0)
    if span < 3 * period:
        return flux.copy(), dict(status='fewer_than_three_cycles', bins=0)
    phase_cycles = (t - origin) / period
    cycles = np.floor(phase_cycles).astype(int)
    phase = phase_cycles % 1
    bins = min(200, max(20, int(np.floor(period / .1))))
    while True:
        index = np.minimum((phase * bins).astype(int), bins - 1)
        occupied = np.unique(index)
        counts = [len(np.unique(cycles[index == b])) for b in occupied]
        if counts and min(counts) >= 3:
            break
        if bins == 1:
            return flux.copy(), dict(status='insufficient_cycle_coverage', bins=0)
        bins = max(1, bins // 2)
    model = np.empty_like(flux)
    for b in occupied:
        selected = index == b
        model[selected] = np.median(flux[selected])
    result = flux - model + np.median(flux)
    return result, dict(status='applied', bins=bins, min_cycles=min(counts),
                        model_scatter=float(np.std(model)))


def checks():
    rng = np.random.default_rng(2026111524)
    t = np.arange(0., 32., 1 / 720)
    flux = 1 + .01 * np.sin(2 * np.pi * t / 6) + rng.normal(0, .001, len(t))
    result, meta = correct(t, flux, 6., 0., 32.)
    mirrored, _ = correct(t, 2 - flux, 6., 0., 32.)
    error = float(np.max(np.abs(result + mirrored - 2)))
    assert error < 2e-15
    assert np.std(result) < .002 and meta['min_cycles'] >= 3
    unchanged, skip = correct(t, flux, 14., 0., 32.)
    assert np.array_equal(unchanged, flux) and skip['status'] == 'fewer_than_three_cycles'
    flat, _ = correct(t, np.ones(len(t)), 6., 0., 32.)
    assert np.array_equal(flat, np.ones(len(t)))
    # A deliberately asymmetric operator must fail the same symmetry assertion.
    bad = lambda f: f - np.minimum(f - 1, 0)
    assert np.max(np.abs(bad(flux) + bad(2 - flux) - 2)) > .001
    phase = ((t / 6 - .3 + .5) % 1) - .5
    shape = np.clip((.15 - np.abs(phase) * 6) / .03, 0, 1)
    injected, _ = correct(t, flux - .004 * shape, 6., 0., 32.)
    attenuation = float(np.sum(shape * (result - injected)) / np.sum(shape ** 2) / .004)
    assert attenuation < .3
    return dict(symmetry_max_error=error, periodic_depth_fraction=attenuation,
                checks=6, asymmetric_mutation_rejected=True)


if __name__ == '__main__':
    print(checks())
