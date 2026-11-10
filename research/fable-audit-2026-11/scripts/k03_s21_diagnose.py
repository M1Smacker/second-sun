"""K-03: why are the two published S21 transits of TIC 172900988 b (Kostov 2021: BTJD 1883.37 and 1888.30) not found? Local checks on the TESS-SPOC 30-min S21 file; no mask involved."""
import os; os.environ.setdefault("NUMBA_NUM_THREADS", "1")
import sys, warnings; sys.path.insert(0, r"D:\second-sun\pipeline"); warnings.filterwarnings("ignore")
import numpy as np
from detect_v2 import load, detrend
p = r"D:\second-sun\data\known\172900988\hlsp_tess-spoc_tess_phot_0000000172900988-s0021_tess_v1_lc.fits"
t, f, _, info = load(p, info=True)
print("product", info["product"], "column", info["column"], "cadence min", info["cadence_min"], "n", len(t), "range", round(t.min(), 2), round(t.max(), 2))
gi = np.where(np.diff(t) > 0.2)[0]
print("gaps over 0.2 d:", [(round(t[i], 2), round(t[i + 1], 2), round(t[i + 1] - t[i], 2)) for i in gi])
s = 1.4826 * np.median(np.abs(f - np.median(f)))
print("per-cadence robust scatter (all data incl. eclipses) ppm", round(s * 1e6))
for tc, dur_d in ((1883.37, 0.40), (1888.30, 0.27)):
    inw = np.abs(t - tc) < dur_d / 2
    out = (np.abs(t - tc) < 1.5) & (np.abs(t - tc) > dur_d / 2 + 0.1)
    # exclude the eclipses (primary 1878.3 +- 0.3, secondaries 1870.57 and 1890.23 +- 0.3) from the local baseline
    for e in (1870.57, 1878.3, 1890.23):
        out &= np.abs(t - e) > 0.5
    base = np.median(f[out]); sc = 1.4826 * np.median(np.abs(f[out] - base))
    d = (base - np.mean(f[inw])) * 1e6
    print(f"transit {tc}: cadences in window {inw.sum()}, baseline cadences {out.sum()}, depth {d:.0f} ppm, baseline scatter {sc * 1e6:.0f} ppm/cadence, naive SNR {d / (sc * 1e6 / np.sqrt(max(inw.sum(), 1))):.1f}; "
          f"nearest gap edge {min(abs(t[gi] - tc).min(), abs(t[gi + 1] - tc).min()):.2f} d; data within +-0.5 d: {(np.abs(t - tc) < 0.5).sum()}")
tt, ff = detrend(t, f)
print("after 2-d biweight detrend: cadences", len(tt), "of", len(t))
for tc, dur_d in ((1883.37, 0.40), (1888.30, 0.27)):
    inw = np.abs(tt - tc) < dur_d / 2
    print(f"  detrended in-window mean {1e6 * (1 - np.mean(ff[inw])):.0f} ppm below 1 (the real depth is about 3000)" if inw.any() else f"  no detrended data in the window at {tc}")
