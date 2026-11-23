"""Brief 032: one capped robust pass and quadrature-scatter timing fit."""
import numpy as np
from scipy.optimize import brentq


def mad(values):
    return float(1.4826*np.median(np.abs(values-np.median(values))))


def fit_track(events, seed_period, epoch, width):
    if len(events) < 3:
        return None
    n = np.asarray([e['cycle'] for e in events], dtype=float)
    t = np.asarray([e['time'] for e in events], dtype=float)
    sig = np.asarray([e['error'] for e in events], dtype=float)
    assert np.all(np.isfinite(n)) and np.all(np.isfinite(t))
    assert np.all(np.isfinite(sig)) and np.all(sig > 0)
    if np.ptp(n) == 0:
        return None
    center = int(np.rint(np.average(n, weights=1/sig**2)))
    a = np.column_stack((np.ones(len(n)), n-center))
    y = t-epoch

    def solve(keep, extra):
        errors = np.hypot(sig[keep], extra)
        aw = a[keep]/errors[:, None]
        coeff = np.linalg.lstsq(aw, y[keep]/errors, rcond=None)[0]
        residual = y-a@coeff
        covariance = np.linalg.inv(aw.T@aw)
        chi2 = float(np.sum((residual[keep]/errors)**2))
        return coeff, residual, covariance, chi2/(sum(keep)-2)

    keep = np.ones(len(n), dtype=bool)
    _, first_residual, _, initial_chi2 = solve(keep, 0.)
    deviations = np.abs(first_residual-np.median(first_residual))
    # One pass only. Largest deviations first; stable order resolves exact ties.
    candidates = np.flatnonzero(deviations > 5*mad(first_residual))
    candidates = candidates[np.argsort(-deviations[candidates], kind='stable')]
    dropped = candidates[:min(len(n)//10, len(n)-3)]
    keep[dropped] = False
    if np.ptp(n[keep]) == 0:
        return None
    extra = 0.
    if solve(keep, 0.)[3] > 1:
        high = max(float(np.std(y[keep])), float(np.max(sig)), np.finfo(float).eps)
        while solve(keep, high)[3] > 1:
            high *= 2
        extra = float(brentq(lambda s: solve(keep, s)[3]-1, 0., high, xtol=1e-14))
    coeff, residual, covariance, chi2 = solve(keep, extra)
    scatter = mad(residual[keep])
    sectors = len({e['sector'] for e, k in zip(events, keep) if k})
    usable = sum(keep) >= 3 and sectors >= 2 and scatter <= .1*width
    return dict(period=float(coeff[1]), epoch=float(epoch+coeff[0]),
                period_error=float(np.sqrt(covariance[1,1])),
                epoch_error=float(np.sqrt(covariance[0,0])), covariance=float(covariance[0,1]),
                epoch_cycle=center, extra_scatter=extra, robust_scatter=scatter,
                reduced_chi2=chi2, initial_reduced_chi2=initial_chi2,
                n_input=len(n), n=int(sum(keep)), n_sectors=sectors,
                n_dropped=len(dropped), dropped_indices=dropped.tolist(),
                usable=bool(usable), seed_period=seed_period, residuals=residual.tolist())


def sector_agreement(fit, catalogue, midpoints):
    offsets = []
    for t in midpoints:
        ncat = round((t-catalogue['T0'])/catalogue['P'])
        cat_center = catalogue['T0']+ncat*catalogue['P']
        nfit = round((cat_center-fit['epoch'])/fit['period'])
        offsets.append(fit['epoch']+nfit*fit['period']-cat_center)
    return bool(offsets and all(abs(x) <= .25*catalogue['wp'] for x in offsets)), offsets


def rules(eligible_tracks, usable, agrees, trap):
    a1 = eligible_tracks > 0 and usable/eligible_tracks >= .8
    a2 = usable > 0 and agrees/usable >= .9
    a3 = trap == 30
    return dict(A1=a1, A2=a2, A3=a3, passed=a1 and a2 and a3)
