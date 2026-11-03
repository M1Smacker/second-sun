import sys, numpy as np, pandas as pd
sys.path.insert(0, "D:/second-sun/pipeline")
import os
def phys(P, R):                      # the frozen eclipse-length rule: P/pi x 2R/a, a from Kepler 3 with 2 Msun, capped at 0.4 P (days)
    a = 215.03 * (2.0 * (P / 365.25) ** 2) ** (1 / 3)
    return np.minimum(P / np.pi * 2 * R / a, 0.4 * P)
# G1: Prsa full widths where the Kepler period matches
os.environ.pop("SS_SET", None)
import stage3_core as C, dataset as DS
tg = pd.read_csv(DS.TARGETS, comment="#").drop_duplicates("tic").set_index("tic"); w = C.eb_widths()
g1 = pd.DataFrame([dict(tic=t, P=tg.p_bin_d[t], R=tg.tic_radius_rsun[t], T=w[t][0] * tg.p_bin_d[t], Ts=w[t][1] * tg.p_bin_d[t]) for t in w if t in tg.index])
g1 = g1[(g1.R > 0) & (g1.P > 7)]; g1["ratio"] = g1["T"] / phys(g1.P, g1.R)
print("G1 Prsa full width / physics, P>7 d, radius known: n=%d median %.2f IQR %.2f..%.2f" % (len(g1), g1.ratio.median(), g1.ratio.quantile(.25), g1.ratio.quantile(.75)))
# G3: TTC median duration
g3 = pd.read_csv("D:/second-sun/targets/g3_chain_targets.csv", comment="#").drop_duplicates("tic")
g3 = g3[(g3.tic_radius_rsun > 0) & g3.dur_pri_h.notna()].copy(); g3["T"] = g3.dur_pri_h / 24
g3["ratio"] = g3["T"] / phys(g3.p_bin_d, g3.tic_radius_rsun)
print("G3 TTC duration / physics, radius known: n=%d median %.2f IQR %.2f..%.2f" % (len(g3), g3.ratio.median(), g3.ratio.quantile(.25), g3.ratio.quantile(.75)))
for lo, hi in ((7, 10), (10, 15), (15, 40)):
    a, b = g1[(g1.P >= lo) & (g1.P < hi)], g3[(g3.p_bin_d >= lo) & (g3.p_bin_d < hi)]
    print("  P %d-%d d: G1 n=%d median %.2f | G3 n=%d median %.2f" % (lo, hi, len(a), a.ratio.median() if len(a) else np.nan, len(b), b.ratio.median()))
# the G1 stars' TIC radius is the same kind of number as G3's; duration vs period slope
print("G3 median duration (h) by period bin:", {f"{lo}-{hi}": round(float(g3[(g3.p_bin_d>=lo)&(g3.p_bin_d<hi)].dur_pri_h.median()),1) for lo,hi in ((7,10),(10,15),(15,40))})
print("G1 median full width (h) by period bin:", {f"{lo}-{hi}": round(float(g1[(g1.P>=lo)&(g1.P<hi)]["T"].median()*24),1) for lo,hi in ((7,10),(10,15),(15,40))})
# U03: sector range of the downloaded G3 files
a = pd.read_csv("D:/second-sun/data/g3/audit/audit_all.csv", usecols=["sector", "product"])
print("G3 files sector min %d max %d; sectors above 120: %d" % (a.sector.min(), a.sector.max(), int((a.sector > 120).sum())), "| distinct sectors", a.sector.nunique())
