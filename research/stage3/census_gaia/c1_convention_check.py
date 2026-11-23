"""Census builder step C1 (Claude, 23 Nov 2026, 10:46 am): can Gaia eclipsing-binary rows give the mask a correct ephemeris?
Test that can fail: Gaia DR3 slow EBs (data/ffi_door_2026-11-08/gaia_pool_p5.csv, P > 5 d) matched by position to the Prsa 2022
TESS EB catalogue (data/xmatch/ebs.csv, P > 5 d). For each pair:
  period ratio Gaia/Prsa (expect 1, or 2 / 0.5 for half/double period confusions);
  primary eclipse time from Gaia converted to BTJD, folded on Prsa's period against Prsa's BJD0: phase offset near 0 (or near the
  secondary phase if primary and secondary are swapped).
Time conversion: Gaia reference_time = BJD(TCB) - 2455197.5, so BTJD = reference_time - 1802.5 (TCB vs TDB: about a minute at most, LIKELY
negligible here). Two phase conventions are reported side by side: t_prim = ref + phase*P (A) and ref - phase*P (B); the doc check decides.
Width: Gaia derived_primary_ecl_duration is in phase units (x P = days); Prsa Wp-pf is in phase too. Ratio reported, conventions differ.
Position match: Gaia (epoch 2016.0) moved back to 2000.0 with its proper motion; Prsa RAJ2000/DEJ2000 are TIC J2000; radius 3 arcsec.
Prints aggregates only."""
import numpy as np, pandas as pd
from scipy.spatial import cKDTree

R = "D:/second-sun"
g = pd.read_csv(f"{R}/data/ffi_door_2026-11-08/gaia_pool_p5.csv")
p = pd.read_csv(f"{R}/data/xmatch/ebs.csv")
p = p[(p["Per"] > 5) & p["BJD0"].notna()].copy()
print("gaia rows", len(g), "prsa rows P>5", len(p))

dt = -16.0  # years, 2016.0 -> 2000.0
dec0 = g["dec"] + np.nan_to_num(g["pmdec"]) * dt / 3.6e6
ra0 = g["ra"] + np.nan_to_num(g["pmra"]) * dt / 3.6e6 / np.cos(np.radians(g["dec"]))


def xyz(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]


tree = cKDTree(xyz(ra0, dec0))
d, i = tree.query(xyz(p["RAJ2000"].values, p["DEJ2000"].values), distance_upper_bound=np.radians(3 / 3600) * 1.0001)
ok = np.isfinite(d)
m = p[ok].copy(); gi = g.iloc[i[ok]].reset_index(drop=True); m = m.reset_index(drop=True)
print("matched pairs within 3 arcsec", len(m), "| sep median arcsec", round(float(np.median(np.degrees(d[ok]) * 3600)), 2))

Pg = 1 / gi["frequency"]; ratio = Pg / m["Per"]
cls = np.select([abs(ratio - 1) < 0.002, abs(ratio - 2) < 0.004, abs(ratio - 0.5) < 0.001], ["same", "gaia_double", "gaia_half"], "other")
print("period ratio classes:", pd.Series(cls).value_counts().to_dict())
same = cls == "same"
bt_ref = gi["reference_time"] - 1802.5
for name, sgn in (("A: ref + phase*P", 1), ("B: ref - phase*P", -1)):
    tprim = bt_ref + sgn * gi["derived_primary_ecl_phase"] * Pg
    off = ((tprim - m["BJD0"]) / m["Per"]) % 1.0
    off = np.where(off > 0.5, off - 1, off)[same]
    a = np.abs(off)
    # how many land on the Prsa primary, and how many on 0.5 (swapped primary/secondary)
    print(f"{name}: n {same.sum()} | |offset| < 0.02: {np.mean(a < 0.02):.3f} | < 0.05: {np.mean(a < 0.05):.3f} | near 0.5 (+-0.05): {np.mean(a > 0.45):.3f} | median |offset| {np.median(a):.4f}")
    # in units of the Prsa primary width
    w = m["Wp-pf"].values[same]
    r = a / np.where(w > 0, w, np.nan)
    print(f"   offset in Prsa primary widths: median {np.nanmedian(r):.2f}; share within half a width {np.nanmean(r < 0.5):.3f} (n with width {np.isfinite(r).sum()})")
wr = (gi["derived_primary_ecl_duration"] / m["Wp-pf"])[same]
wr = wr[np.isfinite(wr) & (wr > 0)]
print("primary width ratio Gaia/Prsa (both phase units): n", len(wr), "median", round(float(wr.median()), 2), "IQR", [round(float(x), 2) for x in wr.quantile([.25, .75])])
# period precision: Gaia frequency_error -> period error in days, versus Prsa e_Per
pe = (gi["frequency_error"] / gi["frequency"] ** 2)[same]
print("period error days, Gaia median", f"{pe.median():.2e}", "| Prsa median", f"{m['e_Per'][same].median():.2e}")
print("drift after 2000 d at the Gaia period error, median, in days:", f"{(pe * 2000 / Pg[same]).median():.4f}")
