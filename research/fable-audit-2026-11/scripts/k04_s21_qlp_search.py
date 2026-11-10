"""K-04: the QLP S21 light of TIC 172900988 through the frozen mask and the Prod search (no borrowed windows: the star has no SPOC 2-minute file in S21, so this is the best case for QLP)."""
import os; os.environ.setdefault("NUMBA_NUM_THREADS", "1")
import sys, warnings; sys.path.insert(0, r"D:\second-sun\pipeline"); warnings.filterwarnings("ignore")
import numpy as np
import stage2_search as S2, stage3_core as C
from detect_v2 import load
S2._init(); C.use_grid(S2, C.GRID_V5)
t, f, _, info = load(r"D:\second-sun\data\known\172900988\hlsp_qlp_tess_ffi_s0021-0000000172900988_tess_v01_llc.fits", info=True)
tm, fm, runs = S2.mask_runs(t, f, [19.658])
print("cadences", len(t), "after the frozen mask", len(tm), "mask runs (phase)", [[round(a, 3), round(b, 3)] for a, b in runs[0][1]])
for tc, dur in ((1883.37, 0.40), (1888.30, 0.27)):
    n_all = int(np.sum(np.abs(t - tc) < dur / 2)); n_kept = int(np.sum(np.abs(tm - tc) < dur / 2))
    out = []
    for lab, (tt, ff) in (("frozen mask", (tm, fm)), ("no mask", (t, f))):
        pr = S2.Prod(tt, ff); b = (np.nan, np.nan, np.nan)
        for d in S2.DURS_H:
            c, snr, m = pr.scores(d); sel = (np.abs(c - tc) < 1.5) & np.isfinite(snr)
            if sel.any():
                i = np.argmax(np.where(sel, snr, -np.inf))
                if not np.isfinite(b[0]) or snr[i] > b[0]: b = (float(snr[i]), float(c[i]), d)
        out.append(f"{lab}: best SNR {b[0]:.1f} @ {b[1]:.2f} ({b[2]:g} h)")
    print(f"transit {tc}: cadences in window {n_all}, removed by the mask {1 - n_kept / max(n_all, 1):.0%}; " + "; ".join(out))
