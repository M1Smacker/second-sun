"""RS-010 Q5 (night of 4 Nov 2026): how much did the 784 'no safe windows' G3 reads cost? Own data only, nothing in the search changes.
Counts and Horizon reach (the R0 rule, unchanged code of pipeline/horizon_reach.py), with and without the lost star-sectors.
Aggregates only: no star ID printed."""
import sys; sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import horizon_reach as H
R = "D:/second-sun"
au = pd.read_csv(f"{R}/data/g3/audit/audit_all.csv")
b = pd.read_csv(f"{R}/data/g3/audit/best_per_star_sector.csv")
tg = pd.read_csv(f"{R}/targets/g3_chain_targets.csv", comment="#").drop_duplicates("tic").set_index("tic")
P = print
unsafe = au.win_src.isin(["NONE (unsafe)", "ONE neighbour (weak)"])
P(f"audit reads {len(au)}; no-safe-window reads {int(unsafe.sum())} = {int((au.win_src=='NONE (unsafe)').sum())} with no neighbour + {int((au.win_src=='ONE neighbour (weak)').sum())} with one weak neighbour ({100*unsafe.mean():.1f}%)")
ss_all = au.drop_duplicates(["tic", "sector"])[["tic", "sector"]]
ss_ok = b[["tic", "sector"]]
lost = ss_all.merge(ss_ok, how="left", indicator=True).query("_merge=='left_only'")[["tic", "sector"]]
P(f"star-sectors in the audit {len(ss_all)}; with at least one safe-window product {len(ss_ok)}; with NONE {len(lost)} ({100*len(lost)/len(ss_all):.1f}%)")
stars_all = set(ss_all.tic); stars_ok = set(ss_ok.tic)
P(f"stars with files {len(stars_all)}; stars with at least one usable star-sector {len(stars_ok)}; stars with none at all {len(stars_all-stars_ok)}")
# by sector, camera, cadence of the lost ones
L = au.merge(lost, on=["tic", "sector"])
L1 = L.sort_values("n_searched", ascending=False).drop_duplicates(["tic", "sector"])
P("lost star-sectors by cadence (min): " + str(L1.cadence_min.value_counts().to_dict()))
tot_c = ss_all.merge(au.drop_duplicates(['tic','sector'])[['tic','sector','cadence_min']]).cadence_min.value_counts().to_dict()
P("all star-sectors by cadence: " + str(tot_c))
bysec = L1.groupby("sector").size().sort_values(ascending=False)
allsec = ss_all.groupby("sector").size()
P("lost share by sector (top 8 by count): " + "; ".join(f"S{s}: {n}/{allsec[s]}" for s, n in bysec.head(8).items()))
P(f"lost star-sectors in {L1.sector.nunique()} sectors; sectors with >30% lost: {int(((bysec/allsec[bysec.index])>0.3).sum())} of {allsec.size}")
P("neighbour counts (win_nn) of the lost reads: " + str(L.win_nn.value_counts().sort_index().to_dict()))
P("lost star-sectors by camera: " + str(L1.camera.value_counts().sort_index().to_dict()))
# brightness
tm = tg.tmag if "tmag" in tg.columns else tg.get("Tmag")
if tm is not None:
    P("median Tmag lost vs usable star-sectors: %.2f vs %.2f" % (tm.reindex(L1.tic).median(), tm.reindex(ss_ok.tic).median()))
P("median 8 h-ish noise (6.5 h ppm) lost vs usable: %.0f vs %.0f" % (L1["noise_6.5h_ppm"].median(), b["noise_6.5h_ppm"].median()))
# Horizon what-if
tabs = H.recovery_tables()
star, ss, nvalid, med = H.sector_table("g3")
S0, NS = H.reach(star, ss, tabs, 5.6, 1.0)
a = np.log(L1["noise_15h_ppm"] / L1["noise_6.5h_ppm"]) / np.log(15 / 6.5)
ex = L1[(L1.status == "ok") & (L1["noise_6.5h_ppm"] > 0) & (L1["noise_15h_ppm"] > 0)].copy()
a = np.log(ex["noise_15h_ppm"] / ex["noise_6.5h_ppm"]) / np.log(15 / 6.5)
ex["noise8"] = ex["noise_6.5h_ppm"] * (8 / 6.5) ** a
ex["covered_d"] = ex.n_searched * ex.cadence_min / 1440.0
ex["fam"] = ex["product"].isin(H.FAMILY)
ex = ex[ex.tic.isin(star.index)][["tic", "sector", "fam", "noise8", "covered_d"]]
P(f"lost star-sectors that can be scored: {len(ex)} of {len(lost)}")
ss2 = pd.concat([ss, ex], ignore_index=True)
S1, _ = H.reach(star, ss2, tabs, 5.6, 1.0)
P("Horizon sum of detection chance (main scenario, floor 5.6): rows R=3..15 step 2; columns P = " + ", ".join(f"{p:.0f}" for p in H.PER_C))
for nm, S in (("as searched", S0), ("if the lost ones were searched", S1)):
    P(nm); [P(f"  R={r:4.0f}: " + " ".join(f"{S[i,j]:6.2f}" for j in range(len(H.PER_C)))) for i, r in enumerate(H.RAD_C)]
i7 = list(H.RAD_C).index(min(H.RAD_C, key=lambda x: abs(x-7))); 
P("Kepler-16-size cell (R=7), sum for P=77,139: as searched %.2f, %.2f; with lost %.2f, %.2f; gain %.1f%%, %.1f%%" % (S0[i7,3], S0[i7,4], S1[i7,3], S1[i7,4], 100*(S1[i7,3]/S0[i7,3]-1), 100*(S1[i7,4]/S0[i7,4]-1)))
P("Largest relative gain over cells with sum>1: %.1f%%" % (100*np.nanmax(np.where(S0>1, S1/np.where(S0>0,S0,np.nan)-1, np.nan))))
