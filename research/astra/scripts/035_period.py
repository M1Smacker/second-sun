"""Draft blind binary-period finder. No catalogue arguments, pipeline imports or I/O.

CLI reads one prepared NPZ (time, flux, sector) only inside data/astra/035.
The validation runner must separately verify FITS identity, cadence and fences.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import sys

os.environ['NUMBA_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np
from astropy.timeseries import BoxLeastSquares
from scipy.ndimage import median_filter

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'data/astra/035'
NAMES = ('robust_sigma', 'folded_distance', 'streams_for_fit', 'combined',
         'support', 'primary', 'secondary')


def inherited():
    """Execute only unchanged, AST-compared pure functions, never old harness code."""
    source = Path(__file__).with_name('032_eclipse_fit.py')
    other = source.with_name('032b_eclipse_fit.py')
    a = ast.parse(source.read_text(encoding='utf-8'))
    b = ast.parse(other.read_text(encoding='utf-8'))
    aa = {n.name: n for n in a.body if isinstance(n, ast.FunctionDef)}
    bb = {n.name: n for n in b.body if isinstance(n, ast.FunctionDef)}
    for name in NAMES:
        if ast.dump(aa[name]) != ast.dump(bb[name]):
            raise RuntimeError('Inherited function AST differs: ' + name)
    ns = dict(np=np, BoxLeastSquares=BoxLeastSquares, median_filter=median_filter,
              EPS=np.finfo(float).eps)
    exec(compile(ast.Module(body=[aa[n] for n in NAMES], type_ignores=[]),
                 str(source), 'exec'), ns)
    return ns, hashlib.sha256(source.read_bytes()).hexdigest()


OLD, ALIAS_SOURCE_SHA256 = inherited()


def episodes(t, f):
    """Conservative isolated-dip screen, independent of any candidate period."""
    sigma = OLD['robust_sigma'](f)
    hit = np.flatnonzero(f < np.median(f) - 5*sigma)
    if not len(hit):
        return []
    groups = np.split(hit, np.flatnonzero((np.diff(hit) > 1) |
                                        (np.diff(t[hit]) > 2/48)) + 1)
    return [float(np.mean(t[g])) for g in groups if len(g) >= 2]


def count_support(t, f, p, e, w):
    dt = OLD['folded_distance'](t, e, p)
    inside = abs(dt) <= w/2
    cycles = np.rint((t[inside]-e)/p).astype(int)
    sigma = OLD['robust_sigma'](f)
    return sum(int(np.count_nonzero(cycles == c) >= 2 and
                   np.sum(np.median(f)-f[inside][cycles == c]) >
                   2*sigma*np.sqrt(np.count_nonzero(cycles == c)))
               for c in np.unique(cycles))


def odd_even(t, f, p, e, w):
    stats = []
    for parity in (0, 1):
        phase = OLD['folded_distance'](t, e + parity*p, 2*p)
        core = abs(phase) <= w/2
        shoulder = (abs(phase) >= .75*w) & (abs(phase) <= 1.5*w)
        if core.sum() < 5 or shoulder.sum() < 5:
            return None
        depth = np.median(f[shoulder]) - np.mean(f[core])
        err = OLD['robust_sigma'](f[shoulder])*np.sqrt(1/core.sum()+1/shoulder.sum())
        stats.append((float(depth), float(err)))
    return stats


def find_period(raw, mutate_alias=False):
    """raw: (sector, rank, product, BTJD array, normalized flux array) tuples.

    Rank/product exist only for unchanged 032 preprocessing. Use one SPOC
    120-second product per sector. No catalogue epoch, width or period enters.
    """
    clean = []
    for sec, rank, product, t, f in raw:
        t, f = np.asarray(t, float), np.asarray(f, float)
        if t.shape != f.shape or t.ndim != 1:
            raise ValueError('Time and flux must be equal one-dimensional arrays')
        good = np.isfinite(t) & np.isfinite(f)
        t, f = t[good], f[good]
        order = np.argsort(t)
        t, f = t[order], f[order]
        keep = np.r_[True, np.diff(t) > 0] if len(t) else np.array([], bool)
        if keep.sum() >= 10:
            clean.append((sec, rank, product, t[keep], f[keep]))
    streams = OLD['streams_for_fit'](clean)
    result = dict(period=None, epoch_btjd=None, primary_width_d=None,
                  secondary_phase=None, n_eclipses=0, quality='insufficient_data')
    if not streams:
        return result
    t, f = OLD['combined'](streams)
    order = np.argsort(t)
    t, f = t[order], f[order]
    dips = episodes(t, f)
    result['isolated_dip_count'] = len(dips)
    if len(dips) < 3:
        result.update(n_eclipses=len(dips), quality={0: 'no_eclipse', 1: 'single_eclipse',
                                                  2: 'two_eclipses'}[len(dips)])
        return result
    # Sector-local broad searches avoid a huge dense grid over years of gaps.
    # Retain three separated peaks per sector; refine across all supplied light.
    seeds = []
    grid = 1/np.linspace(1/30, 1/.5, 24000)
    for _, _, _, _, tt, ff in streams:
        base = float(tt[0])
        power = BoxLeastSquares(tt-base, ff, dy=OLD['robust_sigma'](ff)).power(
            grid, [.04, .08, .16, .32], objective='snr')
        chosen = []
        for i in np.argsort(power.power)[::-1]:
            p = float(grid[i])
            if all(abs(p/x-1) > .01 for x in chosen):
                chosen.append(p)
                seeds.append((float(power.power[i]), p, float(power.duration[i])))
                if len(chosen) == 3:
                    break
    candidates = []
    unique = []
    for score, p, w in sorted(seeds, reverse=True):
        if any(abs(p/x-1) < .005 for x in unique):
            continue
        unique.append(p)
        # Unchanged check treats this blind BLS seed as its reference period.
        found, reason = OLD['primary'](t, f, p, w, np.nan)
        if found:
            candidates.append((found, reason))
        if len(unique) == 8:
            break
    if not candidates:
        result['quality'] = 'no_supported_period'
        return result
    found, reason = max(candidates, key=lambda x: x[0][0])
    score, p, e, w, alias = found
    stats = odd_even(t, f, p, e, w)
    if not mutate_alias and stats is not None:
        a, b = stats
        if abs(a[0]-b[0]) > 3*np.hypot(a[1], b[1]):
            # Data-derived orbital seed, never the answer from the catalogue.
            doubled, why = OLD['primary'](t, f, 2*p, w, np.nan)
            if doubled:
                score, p, e, w, alias = doubled
                reason = 'odd/even split; ' + why
    # Resolve box-grid discretization before quoting 0.1-percent accuracy.
    # This refinement is identical for the normal and deliberately broken arm.
    base = float(t[0])
    ngrid = max(1001, int(np.ceil(.01*p*8*np.ptp(t)/(w*p)))+1)
    grid = np.linspace(.995*p, 1.005*p, ngrid)
    refined = BoxLeastSquares(t-base, f, dy=OLD['robust_sigma'](f)).power(
        grid, [.6*w, w], objective='snr', oversample=20)
    i = int(np.argmax(refined.power))
    p, e, w = float(grid[i]), float(refined.transit_time[i]+base), float(refined.duration[i])
    n = count_support(t, f, p, e, w)
    if n < 3:
        result.update(quality='fewer_than_three_supported', n_eclipses=n)
        return result
    sec = OLD['secondary'](t, f, p, e, w, w)
    result.update(period=float(p), epoch_btjd=float(e), primary_width_d=float(w),
                  secondary_phase=None if sec is None else float((sec-e)/p % 1),
                  n_eclipses=n, quality='candidate', alias_reason=reason,
                  odd_even_depths=stats)
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input_npz')
    parser.add_argument('output_json')
    args = parser.parse_args()
    paths = [Path(x).resolve() for x in (args.input_npz, args.output_json)]
    if not all(p.is_relative_to(OUT.resolve()) for p in paths):
        raise PermissionError('CLI input and output must be inside data/astra/035')
    print('ROOT', ROOT, 'WRITE', OUT, flush=True)
    with np.load(paths[0], allow_pickle=False) as z:
        raw = [(int(s), 0, 'SPOC', z['time'][z['sector'] == s],
                z['flux'][z['sector'] == s]) for s in np.unique(z['sector'])]
    result = find_period(raw)
    paths[1].write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print('Result saved; quality:', result['quality'])


if __name__ == '__main__':
    main()
