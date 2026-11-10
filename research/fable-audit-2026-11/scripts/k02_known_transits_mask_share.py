"""K-02 (WO-F01 Part A step 6 and the known-planet check, 10 Nov 2026): for every PUBLISHED or PREDICTED transit of the two known TESS circumbinary planets that falls in our light, how much of the transit window does the frozen
mask remove, and what is the best SNR near it with and without the mask? Public, published stars, so times are printed.
Sources (opened 10 Nov 2026, text extracted from the arXiv PDFs saved in data\\known_papers_2026-11-10):
  TOI-1338 b : Kostov et al. 2020, arXiv 2004.07783, Table 6 (predicted transit times, BJD - 2,455,000 -> BTJD = value - 2000; duration in the table). Predictions, not observations.
  TIC 172900988 b : Kostov et al. 2021, arXiv 2105.08614, section 2: two transits in Sector 21 at BTJD 1883.37 (about 0.4 d) and 1888.30 (about 0.27 d), 'just before and right after the downlink data gap'.
Frozen mask = stage2_search.mask_runs with the star's catalogue period list (as the hunts do). 'unmasked' = no eclipse mask at all (detrend and search only).
Usage (SS_SET=g2): python k02_known_transits_mask_share.py"""
import os
os.environ.setdefault("NUMBA_NUM_THREADS", "1")
import sys, glob, warnings
sys.path.insert(0, r"D:\second-sun\pipeline")
warnings.filterwarnings("ignore")
import numpy as np
import stage2_search as S2, stage3_core as C, audit_all as A
from detect_v2 import load

S2._init(); C.use_grid(S2, C.GRID_V5)
T1338 = [(3861.1845, 6.74), (3954.1353, 9.80), (4049.6930, 7.91), (4142.3991, 7.46), (4237.9220, 9.73), (4330.9984, 6.31), (4425.7194, 11.78), (4519.6951, 5.94), (4708.3278, 6.06), (4801.0174, 8.44),
         (4896.7585, 6.78), (4989.3540, 6.04), (5084.8165, 8.19), (5177.9790, 4.93), (5272.3566, 9.79), (5366.6770, 4.79), (5459.7304, 8.76), (5555.2836, 5.26), (5647.6474, 6.27), (5743.6224, 6.35),
         (5836.0445, 4.93), (5931.4246, 8.39), (6024.6162, 4.71), (6118.5043, 9.86)]
PRED = [(t - 2000.0, h) for t, h in T1338]
SYS = [("TOI-1338 b (predicted, Kostov 2020 Table 6)", 260128333, sorted(glob.glob(r"D:\second-sun\data\g2\260128333\tess*_lc.fits")), PRED, A.PER.get(260128333) or [14.608559]),
       ("TIC 172900988 b (published S21 transits, Kostov 2021)", 172900988, sorted(glob.glob(r"D:\second-sun\data\known\172900988\hlsp_tess-spoc*s0021*_lc.fits")), [(1883.37, 9.6), (1888.30, 6.5)], [19.658])]
WIN = 1.5     # search window around the published/predicted time, days (prediction error of the model grows with time)


def best(prod, tc, win=WIN):
    out = (np.nan, np.nan, np.nan)
    for d in S2.DURS_H:
        c, snr, m = prod.scores(d)
        sel = (np.abs(c - tc) < win) & np.isfinite(snr)
        if sel.any():
            i = np.argmax(np.where(sel, snr, -np.inf))
            if not np.isfinite(out[0]) or snr[i] > out[0]:
                out = (float(snr[i]), float(c[i]), d)
    return out


for name, tic, paths, trs, periods in SYS:
    print(f"\n===== {name}: {len(paths)} files, catalogue periods used by the mask {periods}")
    print("  columns: transit time (BTJD) | sector | cadences in the window (+-dur/2) | share removed by the frozen mask | best SNR within +-1.5 d: frozen mask (SNR @ time, box h) | no mask | note")
    L = []
    for p in paths:
        t, f, _, info = load(p, info=True)
        L.append((t, f, info["sector"], info["cadence_min"]))
    for tc, dur in trs:
        hit = [(t, f, s, cad) for t, f, s, cad in L if t.min() - 1 < tc < t.max() + 1]
        if not hit:
            continue
        t, f, s, cad = hit[0]
        n_all = int(np.sum(np.abs(t - tc) < dur / 48))
        tm, fm, _ = S2.mask_runs(t, f, periods)
        n_kept = int(np.sum(np.abs(tm - tc) < dur / 48))
        near = np.sum(np.abs(t - tc) < WIN)
        if len(tm) < 200 or near < 20:
            print(f"  {tc:9.2f} | S{s} | {n_all} cad in window | not testable (data near it: {near} cadences)")
            continue
        bm = best(S2.Prod(tm, fm), tc) if np.sum(np.abs(tm - tc) < WIN) > 20 else (np.nan,) * 3
        bu = best(S2.Prod(t, f), tc)
        exp = dur / 24 / (cad / 1440)
        share = f"{1 - n_kept / n_all:.0%}" if n_all else "n/a"
        note = "" if n_all >= 0.8 * exp else f"window only {n_all / exp:.0%} covered by data"
        print(f"  {tc:9.2f} | S{s} | {n_all:4d} of {exp:.0f} expected | removed {share:>4s} | masked {bm[0]:5.1f} @ {bm[1]:.2f} ({bm[2]:g} h) | unmasked {bu[0]:5.1f} @ {bu[1]:.2f} ({bu[2]:g} h) | {note}")
