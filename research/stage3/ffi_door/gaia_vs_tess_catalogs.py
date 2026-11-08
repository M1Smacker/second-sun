"""FFI door stage B: how good are the Gaia DR3 slow-EB periods and eclipse times, tested against TESS-based published ephemerides (own data, catalogue values only; NO light curve is read).

References: Prsa 2022 (data\\xmatch\\ebs.csv: Per, BJD0 = BJD-2457000, Tmag) and TTC (data\\g3\\catalog_ttc: Per, T0-pri = BJD-2457000, Tmag).
Gaia: the pool of all P>5 d rows (data\\ffi_door_2026-11-08\\gaia_pool_p5.csv). Match 3 arcsec after moving Gaia to J2000 with pm; sanity -0.3 <= G - Tmag <= 1.8.
Prints COUNTS ONLY (no ids) to research/stage3/ffi_door/gaia-vs-tess-counts.txt
Questions: (1) recall: of TESS-known EBs with P_TESS > 5 d and Tmag <= 13.5, how many are in the Gaia slow pool? (2) period agreement P_Gaia/P_TESS. (3) does the Gaia ephemeris (reference_time, frequency, derived phases) predict the TESS primary or secondary eclipse time within 0.25 d, and are the formal errors honest?
"""
import os, re
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

ROOT = r"D:\second-sun"; D = os.path.join(ROOT, "data", "ffi_door_2026-11-08")
pool = pd.read_csv(os.path.join(D, "gaia_pool_p5.csv"))
dec = pool["dec"].values; cosd = np.cos(np.radians(dec))
pool["ra0"] = pool["ra"] + np.where(pool["pmra"].notna(), -pool["pmra"].fillna(0) * 16 / (3.6e6 * cosd), 0)
pool["dec0"] = pool["dec"] + np.where(pool["pmdec"].notna(), -pool["pmdec"].fillna(0) * 16 / 3.6e6, 0)
def xyz(ra, de):
    r, d = np.radians(ra), np.radians(de)
    return np.column_stack([np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)])
tree = cKDTree(xyz(pool["ra0"].values, pool["dec0"].values))
ASEC = np.radians(1 / 3600)

def read_ttc(fn, cols):
    rows = []
    for ln in open(fn, encoding="utf-8", errors="replace"):
        m = re.match(r"^\s*(\d{3,10})\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", ln)
        if m and len(ln) > 40:
            if cols == 3:
                rows.append((int(m.group(1)), float(m.group(2)), float(m.group(3)), float(ln[37:43]) if ln[37:43].strip() else np.nan,
                             float(ln[44:53]), float(ln[54:63])))
            else:
                rows.append((int(m.group(1)), float(m.group(2)), float(m.group(3)), np.nan, float(ln[37:46]), float(ln[47:58])))
    return pd.DataFrame(rows, columns=["tic", "ra", "dec", "tmag", "per", "t0"])
t3 = read_ttc(os.path.join(ROOT, "data", "g3", "catalog_ttc", "table3_new_ebs.txt"), 3)
t4 = read_ttc(os.path.join(ROOT, "data", "g3", "catalog_ttc", "table4_known_ebs.txt"), 4)
pr = pd.read_csv(os.path.join(ROOT, "data", "xmatch", "ebs.csv"))
prs = pd.DataFrame({"tic": pr["TIC"], "ra": pr["RAJ2000"], "dec": pr["DEJ2000"], "tmag": pr["Tmag"], "per": pr["Per"], "t0": pr["BJD0"], "src": "prsa"})
t3["src"] = "ttc3"; t4["src"] = "ttc4"
ref = pd.concat([prs, t3, t4], ignore_index=True)
ref = ref.drop_duplicates("tic").reset_index(drop=True)          # Prsa first, then TTC
ref = ref[(ref["per"] > 5) & ref["per"].notna()].reset_index(drop=True)

out = []
def say(s=""):
    print(s); out.append(s)
say("TESS-known EBs (Prsa 2022 first, then TTC tables 3 and 4), unique TIC, P_TESS > 5 d: %d (Prsa %d, TTC3 %d, TTC4 %d)" % (len(ref), (ref.src == "prsa").sum(), (ref.src == "ttc3").sum(), (ref.src == "ttc4").sum()))
bright = ref[ref["tmag"] <= 13.5]
say("  with Tmag <= 13.5 (TTC4 has no Tmag in the table; those are counted separately): %d; TTC4 rows without Tmag: %d" % (len(bright), ref["tmag"].isna().sum()))

# match
rx = xyz(ref["ra"].values, ref["dec"].values)
d, idx = tree.query(rx, distance_upper_bound=3 * ASEC)
ok = np.isfinite(d)
m = ref[ok].copy(); mi = idx[ok]
m["g"] = pool["phot_g_mean_mag"].values[mi]
m["sep"] = d[ok] / ASEC
dg = m["g"] - m["tmag"]
m["ok"] = (m["tmag"].isna() | ((dg >= -0.3) & (dg <= 1.8))) | (m["sep"] <= 1.0)
m = m[m["ok"]].copy(); mi = idx[ok][m.index.map(lambda i: list(ref[ok].index).index(i))] if False else None
# recompute the pool row for the kept ones
kept_idx = []
for i, r in m.iterrows():
    j = tree.query(xyz(np.array([r["ra"]]), np.array([r["dec"]])))[1][0]
    kept_idx.append(j)
G = pool.iloc[kept_idx].reset_index(drop=True)
m = m.reset_index(drop=True)
say("matched to the Gaia slow pool (3 arcsec + sanity): %d of %d (any Tmag); pool rows are P_Gaia > 5 d by construction" % (len(m), len(ref)))
mb = m[m["tmag"] <= 13.5]
say("  of the %d TESS-known with Tmag <= 13.5: %d matched = recall of the Gaia slow-EB list %.1f%%" % (len(bright), len(mb), 100 * len(mb) / max(len(bright), 1)))
# period ratio
ratio = G["P"].values / m["per"].values
def share(lo, hi): return int(((ratio >= lo) & (ratio <= hi)).sum())
say("period ratio P_Gaia / P_TESS over the %d matched: within 1%% of 1: %d; within 5%% of 1: %d; within 2%% of 2: %d; within 2%% of 0.5: %d; within 2%% of 3: %d; within 2%% of 1/3: %d; other: %d" % (
    len(m), share(0.99, 1.01), share(0.95, 1.05), share(1.96, 2.04), share(0.49, 0.51), share(2.94, 3.06), share(0.327, 0.34), len(m) - sum([share(0.95, 1.05), share(1.9, 2.1), share(0.45, 0.55), share(2.9, 3.1), share(0.31, 0.36)])))
for lo, hi in ((5, 10), (10, 30), (30, 1e9)):
    sel = (m["per"] > lo) & (m["per"] <= hi)
    say("  P_TESS %s to %s d: n=%d, within 1%%: %d, factor 2 either way (+-3%%): %d" % (lo, hi if hi < 1e8 else "inf", sel.sum(),
        int(((ratio >= 0.99) & (ratio <= 1.01) & sel).sum()), int((((ratio >= 1.94) & (ratio <= 2.06)) | ((ratio >= 0.485) & (ratio <= 0.515))) [sel].sum())))
# ephemeris test: only where the periods agree within 1% (the ephemeris is meaningless otherwise)
good = (ratio >= 0.99) & (ratio <= 1.01)
f = G["frequency"].values; fe = G["frequency_error"].values
tref = G["reference_time"].values + 2455197.5 - 2457000.0
ph1 = G["derived_primary_ecl_phase"].values; ph2 = G["derived_secondary_ecl_phase"].values
P = G["P"].values
t_obs = m["t0"].values
res = np.full(len(m), np.nan); which = np.full(len(m), -1)
for i in range(len(m)):
    if not good[i] or not np.isfinite(ph1[i]):
        continue
    best = None
    for k, ph in enumerate((ph1[i], ph2[i])):
        if not np.isfinite(ph): continue
        tp = tref[i] + ph * P[i]
        n = np.round((t_obs[i] - tp) / P[i])
        r = t_obs[i] - (tp + n * P[i])
        if best is None or abs(r) < abs(best[0]):
            best = (r, k)
    if best is not None:
        res[i], which[i] = best
ok2 = np.isfinite(res)
say("")
say("Gaia ephemeris vs TESS catalogue T0 (stars with period within 1%%: %d; with Gaia eclipse phases: %d)" % (good.sum(), ok2.sum()))
ar = np.abs(res[ok2])
say("  |T_TESS - T_Gaia| (nearest Gaia primary or secondary eclipse): median %.3f d; share <= 0.1 d: %.1f%%; <= 0.25 d: %.1f%%; <= 0.5 d: %.1f%%; <= 1 d: %.1f%%" % (
    np.median(ar), 100 * (ar <= 0.1).mean(), 100 * (ar <= 0.25).mean(), 100 * (ar <= 0.5).mean(), 100 * (ar <= 1.0).mean()))
prim = which[ok2] == 0
say("  nearest eclipse is the Gaia PRIMARY in %.1f%% (so TESS T0 and Gaia primary agree on which eclipse is deeper in %.1f%% of the cases)" % (100 * prim.mean(), 100 * prim.mean()))
# chance level: for random timing the share within 0.25 d of one of two eclipses is about 4*0.25/P
chance = np.mean(np.minimum(1.0, 4 * 0.25 / P[ok2]))
say("  chance level for a random time to land within 0.25 d of either eclipse: %.1f%%" % (100 * chance))
# formal error
tgt = t_obs - tref
dtt = np.abs(t_obs - tref)
formal = np.sqrt((fe * dtt / f) ** 2 + (G["derived_primary_ecl_phase_error"].fillna(0).values * P) ** 2)
fz = formal[ok2]
z = ar / np.maximum(fz, 1e-6)
say("  formal Gaia ephemeris error at the TESS time: median %.3f d; share of stars with |residual| <= 3 x formal error: %.1f%% (honest errors would give about 99.7%%)" % (np.median(fz), 100 * (z <= 3).mean()))
say("  residual in units of formal error: median %.2f; 90th percentile %.1f" % (np.median(z), np.percentile(z, 90)))
for lo, hi in ((5, 10), (10, 30), (30, 1e9)):
    sel = ((m["per"] > lo) & (m["per"] <= hi)).values[ok2]
    if sel.sum():
        say("  P_TESS %s to %s d: n=%d, share <= 0.25 d: %.1f%%, median |res| %.3f d" % (lo, hi if hi < 1e8 else "inf", sel.sum(), 100 * (ar[sel] <= 0.25).mean(), np.median(ar[sel])))
# TESS epoch coverage of the test (how far the T0 values are from the Gaia reference)
say("  mean offset between Gaia reference time and the TESS T0 used: %.0f d" % np.mean(np.abs(tgt[ok2])))
open(os.path.join(ROOT, "research", "stage3", "ffi_door", "gaia-vs-tess-counts.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
