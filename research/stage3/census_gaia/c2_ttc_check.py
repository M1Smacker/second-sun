"""Census builder step C2 (Claude, 23 Nov 2026, 10:47 am): the C1 test on a larger reference, the TESS Ten Thousand Catalog table 3
(Kostov et al. 2025; data/g3/catalog_ttc/table3_new_ebs.txt; T0 in BJD-2457000 = BTJD; durations in hours), plus Prsa 2022 again.
Convention A from C1 (t_prim = ref + phase*P, BTJD = ref - 1802.5). Reports period agreement and eclipse landing, binned by Gaia G,
period and Gaia global_ranking, so a usable subset (if any) can be named. Aggregates only."""
import numpy as np, pandas as pd
from scipy.spatial import cKDTree

R = "D:/second-sun"
g = pd.read_csv(f"{R}/data/ffi_door_2026-11-08/gaia_pool_p5.csv")
cols = [(0, 10, "TIC"), (11, 23, "ra"), (24, 36, "dec"), (37, 43, "Tmag"), (44, 53, "Per"), (54, 63, "T0"), (68, 72, "Dur")]
rows = []
for l in open(f"{R}/data/g3/catalog_ttc/table3_new_ebs.txt", encoding="utf-8"):
    if len(l) < 60 or not l[:10].strip().isdigit(): continue
    try: rows.append({n: float(l[a:b]) if l[a:b].strip() else np.nan for a, b, n in cols})
    except ValueError: pass
t = pd.DataFrame(rows); t["w_phase"] = t["Dur"] / 24 / t["Per"]; t["src"] = "TTC"
# Table 3 holds only EBs NEW to earlier catalogues (Gaia DR3 among them), so it should give ~0 pairs: a built-in negative control.
# Table 4 (known EBs, TESS period and T0, no width; width set to 0.04 phase, a typical value, for the landing test) adds pairs, and its
# published Gaia/TESS period ratio (Ratio1) is an independent check of the period agreement measured here.
c4 = [(0, 10, "TIC"), (11, 23, "ra"), (24, 36, "dec"), (37, 46, "Per"), (47, 58, "T0"), (59, 69, "PerGaia"), (70, 74, "Ratio1")]
r4 = []
for l in open(f"{R}/data/g3/catalog_ttc/table4_known_ebs.txt", encoding="utf-8"):
    if len(l) < 58 or not l[:10].strip().isdigit(): continue
    try: r4.append({n: float(l[a:b]) if l[a:b].strip() else np.nan for a, b, n in c4})
    except ValueError: pass
t4 = pd.DataFrame(r4); t4["w_phase"] = 0.04; t4["src"] = "TTC4"
k = t4[(t4.Per > 5) & t4.PerGaia.notna()]
print("TTC table 4, P>5 with a Gaia period: n", len(k), "| published ratio 1.0:", round(float((k.Ratio1.round(2) == 1.0).mean()), 3),
      "| 2.0:", round(float((k.Ratio1.round(2) == 2.0).mean()), 3), "| 0.5:", round(float((k.Ratio1.round(2) == 0.5).mean()), 3))
t = pd.concat([t, t4])
p = pd.read_csv(f"{R}/data/xmatch/ebs.csv").rename(columns={"RAJ2000": "ra", "DEJ2000": "dec", "BJD0": "T0", "Wp-pf": "w_phase"})
p["src"] = "Prsa"
ref = pd.concat([t[["ra", "dec", "Per", "T0", "w_phase", "src"]], p[["ra", "dec", "Per", "T0", "w_phase", "src"]]])
ref = ref[(ref["Per"] > 5) & ref["T0"].notna()].reset_index(drop=True)
print("reference rows P>5:", ref["src"].value_counts().to_dict())


def xyz(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]


dec0 = g["dec"] + np.nan_to_num(g["pmdec"]) * -16 / 3.6e6
ra0 = g["ra"] + np.nan_to_num(g["pmra"]) * -16 / 3.6e6 / np.cos(np.radians(g["dec"]))
d, i = cKDTree(xyz(ra0, dec0)).query(xyz(ref["ra"].values, ref["dec"].values), distance_upper_bound=np.radians(3 / 3600))
ok = np.isfinite(d)
m = ref[ok].reset_index(drop=True); gi = g.iloc[i[ok]].reset_index(drop=True)
print("pairs:", m["src"].value_counts().to_dict())
Pg = 1 / gi["frequency"]; ratio = Pg / m["Per"]
m["cls"] = np.select([abs(ratio - 1) < 0.002, abs(ratio - 2) < 0.004, abs(ratio - 0.5) < 0.001], ["same", "double", "half"], "other")
tprim = gi["reference_time"] - 1802.5 + gi["derived_primary_ecl_phase"] * Pg
off = ((tprim - m["T0"]) / m["Per"]) % 1.0
m["aoff"] = np.abs(np.where(off > 0.5, off - 1, off))
m["inw"] = m["aoff"] < 0.5 * m["w_phase"]          # lands within half a reference eclipse width
m["swap"] = np.abs(m["aoff"] - 0.5) < 0.5 * m["w_phase"]
m["G"] = gi["phot_g_mean_mag"]; m["rank"] = gi["global_ranking"]; m["P"] = m["Per"]
m["good"] = (m["cls"] == "same") & m["inw"]


def table(by, bins, labels):
    k = pd.cut(m[by], bins, labels=labels)
    s = m.groupby(k, observed=True).agg(n=("cls", "size"), same_period=("cls", lambda c: (c == "same").mean()),
                                        good=("good", "mean"), swapped=("swap", "mean"))
    print(f"\nby {by}:\n" + s.round(3).to_string())


print("\nall pairs: n", len(m), "| same period", round((m.cls == "same").mean(), 3), "| same period AND lands within half a width",
      round(m.good.mean(), 3), "| classes", m.cls.value_counts().to_dict())
s = m[m.cls == "same"]
print("among same-period pairs: lands within half a width", round(s.inw.mean(), 3), "| on the other eclipse (swap)", round(s.swap.mean(), 3),
      "| median offset in widths", round(float((s.aoff / s.w_phase).median()), 2))
table("G", [0, 11, 12, 13, 14, 16, 21], ["<11", "11-12", "12-13", "13-14", "14-16", ">16"])
table("P", [5, 7, 10, 15, 25, 60, 1e4], ["5-7", "7-10", "10-15", "15-25", "25-60", ">60"])
table("rank", [0, 0.3, 0.4, 0.5, 0.6, 1], ["<.3", ".3-.4", ".4-.5", ".5-.6", ">.6"])
print("same-period pairs, |phase offset| < 0.01 / 0.02 / 0.05:", [round(float((s.aoff < x).mean()), 3) for x in (0.01, 0.02, 0.05)])
for src in ("TTC", "TTC4", "Prsa"):
    q = m[m.src == src]
    print(f"{src}: n {len(q)}, same period {(q.cls=='same').mean():.3f}, good {q.good.mean():.3f}")
