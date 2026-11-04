"""Gap fill (night of 4 Nov 2026): Horizon reach for G1 (549 Kepler-field binaries, searched with an OLDER Vesper than 0.8, so the 0.8 recovery table is an approximation: UNCERTAIN, probably generous).
Same code path as horizon_reach.sector_table for g3: star table from targets/g1_targets.csv, usable star-sectors from the G1 audit (research/audit-2026-10-23).
No eclipse widths exist for G1 (Villanova catalogue), so geometry uses the mean effective g of G2 sealed (t138-geometry-probe.txt) instead of a per-star g. Aggregates only."""
import sys; sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import horizon_reach as H
R = "D:/second-sun"
tabs = H.recovery_tables()
tg = pd.read_csv(f"{R}/targets/g1_targets.csv", comment="#").drop_duplicates("tic")
star = pd.DataFrame(dict(tic=tg.tic.values, rad=tg.tic_radius_rsun.values, pbin=tg.p_bin_d.values)).set_index("tic")
med = float(star.rad[star.rad > 0].median()); nvalid = int((star.rad > 0).sum()); star["rad"] = star.rad.where(star.rad > 0, med)
b = pd.read_csv(f"{R}/research/audit-2026-10-23/best_per_star_sector.csv"); b = b[b.tic.isin(star.index)][["tic", "sector", "product"]]
au = pd.read_csv(f"{R}/research/audit-2026-10-23/audit_all.csv")
au = au[(au.status == "ok") & (au["noise_6.5h_ppm"] > 0) & (au["noise_15h_ppm"] > 0)].copy()
a = np.log(au["noise_15h_ppm"] / au["noise_6.5h_ppm"]) / np.log(15 / 6.5)
au["noise8"] = au["noise_6.5h_ppm"] * (8 / 6.5) ** a
au["covered_d"] = au.n_searched * au.cadence_min / 1440.0
au = au.sort_values("covered_d", ascending=False).drop_duplicates(["tic", "sector"])[["tic", "sector", "noise8", "covered_d"]]
ss = b.merge(au, on=["tic", "sector"], how="inner"); ss["fam"] = ss["product"].isin(H.FAMILY)
ss = ss[["tic", "sector", "fam", "noise8", "covered_d"]]
print(f"G1: {len(star)} stars ({nvalid} with a TIC radius, median {med:.2f}), {ss.tic.nunique()} with a usable star-sector, {len(ss)} star-sectors")
S, NS = H.reach(star, ss, tabs, 5.6, 1.0)
ri = [i for i, r in enumerate(H.RAD_C) if r > 6]; pi = [j for j, p in enumerate(H.PER_C) if p < 300]
cA = [(i, j) for i in ri for j in pi]; cB = [(i, j) for i in ri for j in pi if NS[i, j] >= 0.5 * len(star)]
mA = np.mean([S[i, j] for i, j in cA]); mB = np.mean([S[i, j] for i, j in cB])
print(f"G1 mean cell sum without geometry: rule A {mA:.1f}, rule B {mB:.1f}; Kepler-16 cell (R=7, P 77/139): {S[2,3]:.1f}, {S[2,4]:.1f}")
# effective g from the G2 sealed probe (R_sum 1.5 and 1.8): 0.15 and 0.11
for f, g in ((1.5, 0.15), (1.8, 0.11)):
    past = {1.5: (22.5, 36.4), 1.8: (12.6, 21.1)}[f]       # G2 dev + G2 sealed + G3 mean sums with geometry (t138-geometry-probe.txt)
    for rule, m, p in (("A", mA, past[0]), ("B", mB, past[1])):
        g1 = g * m; tot = p + g1
        print(f"  R_sum {f}, rule {rule}: G1 with g = {g}: sum {g1:.1f} (E {0.1*g1:.2f}); all four hunts E {0.1*tot:.2f}, chance of none {100*np.exp(-0.1*tot):.0f}%, 95% ceiling on the total rate {100*3/tot:.1f}%")
