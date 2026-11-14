import sys
sys.path.insert(0, r"D:\second-sun\research\stage3\rs032")
import numpy as np, pandas as pd
from astropy.io import fits
import rs032_wobble as W
dumps = W.DUMPS[11]; ASEC = 206264.806
Q = fits.open(r"D:\second-sun\data\tess_quat_2026-11-14\tess2019140185400_sector11-quat.fits", memmap=True)
for cam in (1, 4):
    d = Q[cam].data; t = np.asarray(d["TIME"], float)
    q = np.stack([np.asarray(d[f"C{cam}_Q{i}"], float) for i in (1, 2, 3)], 1) * 2 * ASEC
    ok = np.isfinite(t) & np.all(np.isfinite(q), 1); t, q = t[ok], q[ok]
    w = np.floor((t - t[0]) / (30 / 1440)).astype(int)
    m = pd.DataFrame(q).groupby(w).mean(); tw = pd.Series(t).groupby(w).mean().values
    # offset of each 30-min mean from the mean over the 2 h right after the previous dump (fresh pointing)
    rel = np.array([(x - dumps[np.argmin(np.abs(dumps - x))]) * 24 for x in tw])
    prev = np.array([dumps[dumps <= x].max() if (dumps <= x).any() else np.nan for x in tw])
    off = np.full(len(tw), np.nan)
    for dv in np.unique(prev[np.isfinite(prev)]):
        sel = prev == dv; base = m.values[sel & (tw - dv > 0.05) & (tw - dv < 0.15)]
        if len(base): off[sel] = np.sqrt(((m.values[sel] - base.mean(0)) ** 2).sum(1))
    prof = {h: round(float(np.nanmedian(off[(rel >= h) & (rel < h + 1)])), 2) for h in (-24, -18, -12, -8, -6, -4, -2, -1, 1, 2, 6) if ((rel >= h) & (rel < h + 1)).any()}
    print("camera", cam, "drift from fresh pointing (arcsec) by hour to nearest dump:", prof)
