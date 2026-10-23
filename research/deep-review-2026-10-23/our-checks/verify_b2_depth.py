"""How much does QLP's kspsap_flux shrink a real multi-hour dip? Kepler-16 S54 eclipses, SAP vs KSPSAP."""
import glob
import numpy as np
import lightkurve as lk

p = glob.glob(r"D:\second-sun\data\overnight\**\hlsp_qlp*s0054*.fits", recursive=True)[0]
lc = lk.read(p, quality_bitmask="none")
t = lc.time.value
sap = np.asarray(lc["sap_flux"].value, float)
ksp = np.asarray(lc["kspsap_flux"].value, float)
ok = np.isfinite(t) & np.isfinite(sap) & np.isfinite(ksp)
t, sap, ksp = t[ok], sap / np.nanmedian(sap[ok]), ksp / np.nanmedian(ksp[ok])
# find dips in SAP: points >0.5% below a 1-day running median
from scipy.ndimage import median_filter
cad = np.median(np.diff(t))
base = median_filter(sap, size=int(1.0 / cad) | 1)
low = sap < base - 0.005
idx = np.where(low)[0]
if not idx.size:
    print("no eclipse in S54 SAP"); raise SystemExit
groups = np.split(idx, np.where(np.diff(idx) > 3)[0] + 1)
for g in groups:
    if len(g) < 3:
        continue
    t0 = t[g].mean(); dur_h = (t[g[-1]] - t[g[0]]) * 24
    out = (np.abs(t - t0) > 0.4) & (np.abs(t - t0) < 1.0)
    inn = np.abs(t - t0) < (t[g[-1]] - t[g[0]]) / 4
    dsap = np.median(sap[out]) - np.min(sap[inn]) if inn.any() else np.nan
    dksp = np.median(ksp[out]) - np.min(ksp[inn]) if inn.any() else np.nan
    print(f"dip at {t0:.3f} BTJD, ~{dur_h:.1f} h: depth SAP {dsap*1e6:.0f} ppm, KSPSAP {dksp*1e6:.0f} ppm, "
          f"KSPSAP keeps {100*dksp/dsap:.0f}%")
