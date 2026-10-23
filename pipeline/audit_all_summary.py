"""Summarise the Stage 1 audit (research/audit-2026-10-23/audit_all.csv). NOT a search: no real-data events are in the input.
Writes best_per_star_sector.csv and per_star.csv next to the audit, prints the report. Usage: python audit_all_summary.py"""
import numpy as np, pandas as pd
from common_time import common_time_flags

OUT = r"D:\second-sun\research\audit-2026-10-23"
c = [3.29685004771, 0.850021465753, -0.285041632435, 0.0395908321369, -0.0022308015894, 4.73508403525e-5]
sig1h = lambda T: np.exp(sum(ci * T**i for i, ci in enumerate(c)))          # white-noise ppm in 1 h (Stassun et al. 2018, as in ticgen)

a = pd.read_csv(rf"{OUT}\audit_all.csv")
tm = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#").drop_duplicates("tic")[["tic", "tmag"]]
print(f"files audited: {len(a)} | status: {a.status.value_counts().to_dict()}")
print("by product:", a["product"].value_counts().to_dict())
err = a[a.status.astype(str).str.startswith("ERROR")]
if len(err):
    print("ERROR examples:", err[["file", "status"]].head(5).values.tolist())

ok = a[a.status == "ok"].merge(tm, on="tic", how="left")
ok["eligible"] = ~((ok["product"] == "QLP") & ~ok.win_src.isin(["own SPOC", "neighbours"]))
print(f"\nQLP star-sectors with no safe windows (not usable): {int((~ok.eligible).sum())} "
      f"{ok[~ok.eligible].win_src.value_counts().to_dict()}")
el = ok[ok.eligible].copy()
el["beta"] = el["noise_6.5h_ppm"] / (sig1h(el.tmag) / np.sqrt(6.5))
el["pri"] = el.inj_found.astype(int)
best = (el.sort_values(["tic", "sector", "pri", "noise_6.5h_ppm"], ascending=[True, True, False, True])
          .drop_duplicates(["tic", "sector"]))
best.to_csv(rf"{OUT}\best_per_star_sector.csv", index=False)
total_ss = a.drop_duplicates(["tic", "sector"]).shape[0]               # sector column comes from the FITS header (a filename regex picks up "s2019" from "tess2019...")
print(f"\nstar-sectors with any product: {total_ss} | with a usable audited product: {len(best)} "
      f"| best product chosen: {best['product'].value_counts().to_dict()}")

bins = [0, 4, 6, 10, 15, 25, 1e9]; lab = ["<4", "4-6", "6-10", "10-15", "15-25", ">25"]
cut = pd.cut(best.rmin7_rearth.astype(float), bins, labels=lab)
print("\nsmallest planet (Earth radii) that reaches SNR 7 in ONE 6.5 h crossing, per best star-sector (TIC radius, no dilution):")
print(cut.value_counts().reindex(lab).to_dict(), "| no value:", int(best.rmin7_rearth.isna().sum()))
print("injected 8 h, 3,000 ppm dip recovered:", f"{best.inj_found.mean():.1%} of best star-sectors")

best["tbin"] = pd.cut(best.tmag, [0, 11, 12, 13, 14], labels=["<11", "11-12", "12-13", "13-13.5"])
g = best.groupby("tbin", observed=True)
print("\nby brightness (best product): star-sectors, median noise at 6.5 h (ppm), median noise factor beta, median min planet R_earth, % injected recovered")
print(pd.DataFrame({"n": g.size(), "noise_ppm": g["noise_6.5h_ppm"].median().round(0), "beta": g.beta.median().round(2),
                    "rmin": g.rmin7_rearth.median().round(1), "inj%": (g.inj_found.mean() * 100).round(0)}).to_string())
print(f"overall beta median {best.beta.median():.2f} (quartiles {best.beta.quantile(.25):.2f} to {best.beta.quantile(.75):.2f})")

print("\nproduct noise ratios on the SAME star-sector (median of QLP or TESS-SPOC noise / SPOC noise):")
piv = ok.pivot_table(index=["tic", "sector"], columns="product", values="noise_6.5h_ppm", aggfunc="min")
q = ok[ok["product"] == "QLP"].drop_duplicates(["tic", "sector"]).set_index(["tic", "sector"]).column
piv = piv.join(q.rename("qcol"))
for col, name in (("TESS-SPOC", "TESS-SPOC"), ("QLP", "QLP")):
    for qc in ((None,) if col == "TESS-SPOC" else ("sap_flux", "sys_rm_flux")):
        d = piv if qc is None else piv[piv.qcol == qc]
        r = (d[col] / d["SPOC"]).dropna()
        print(f"  {name}{'' if qc is None else ' ' + qc}: {len(r)} pairs, median {r.median():.2f}x, quartiles {r.quantile(.25):.2f} to {r.quantile(.75):.2f}")
r30 = ok[(ok.cadence_min > 20)]
print(f"30-minute star-sectors audited: {len(r30)} ({r30['product'].value_counts().to_dict()}), injected dip recovered {r30.inj_found.mean():.1%}")

lo = ok[ok.win_loo_cover.notna() & (ok["product"] == "QLP")]
print(f"\nborrowed-window leave-one-out check ({len(lo)} QLP star-sectors that also have their own SPOC windows):")
print(f"  share of the star's own good time kept: median {lo.win_loo_cover.median():.2f}, 10th percentile {lo.win_loo_cover.quantile(.1):.2f}")
print(f"  share of borrowed time that SPOC itself would reject: median {lo.win_loo_extra.median():.3f}, 90th percentile {lo.win_loo_extra.quantile(.9):.3f}, "
      f"share with more than 5% bad time: {(lo.win_loo_extra > .05).mean():.1%}")

pc = best.groupby("tic").agg(n_sectors=("sector", "size"), best_rmin=("rmin7_rearth", "min"),
                             med_rmin=("rmin7_rearth", "median"), n_usable15=("rmin7_rearth", lambda s: int((s <= 15).sum())),
                             tmag=("tmag", "first"))
allt = pd.read_csv(r"D:\second-sun\targets\g1_coverage.csv").tic
pc = pc.reindex(allt).assign(n_sectors=lambda d: d.n_sectors.fillna(0).astype(int))
pc.to_csv(rf"{OUT}\per_star.csv")
print(f"\nper star (549): stars with a usable sector {int((pc.n_sectors > 0).sum())}; "
      f"best sector reaches <=6 R_earth: {int((pc.best_rmin <= 6).sum())}, <=10: {int((pc.best_rmin <= 10).sum())}, "
      f"<=15: {int((pc.best_rmin <= 15).sum())}, never below 15: {int((pc.best_rmin > 15).sum())}, no usable data: {int((pc.n_sectors == 0).sum())}")
print("median usable sectors per star:", int(pc.n_sectors.median()))
print(f"stars with no TIC radius (min planet size not computed): {int(pc.best_rmin.isna().sum())}")
inj = best.groupby("tic").inj_found.agg(["sum", "size"])
print(f"stars where the injected 3,000 ppm dip came back in at least 1 / 3 / 5 sectors: "
      f"{int((inj['sum'] >= 1).sum())} / {int((inj['sum'] >= 3).sum())} / {int((inj['sum'] >= 5).sum())} of {len(pc)}")
print(f"search exposure: {len(best)} usable star-sectors; those where a 15 R_earth planet could be seen: {int((best.rmin7_rearth <= 15).sum())}; "
      f"10 R_earth: {int((best.rmin7_rearth <= 10).sum())}; 6 R_earth: {int((best.rmin7_rearth <= 6).sum())}")

fl = best[best.flipped_events > 0]
evs = []
for r in fl.itertuples():
    for item in str(r.flipped_centers).split():
        evs.append(dict(tic=r.tic, sector=r.sector, camera=r.camera, center=float(item.split(":")[0]), snr=float(item.split(":")[1])))
print(f"\nupside-down (false-alarm proxy) on best star-sectors: {best.flipped_events.sum()} events in {len(best)} star-sectors "
      f"= {best.flipped_events.sum() / len(best):.2f} per star-sector; strongest SNR {best.flipped_max_snr.max()}")
if evs:
    out = common_time_flags(evs)
    n_flag = sum(bool(e["flags"]) for e in out)
    print(f"same-moment filter on those fake events: {n_flag} of {len(out)} flagged ({n_flag / len(out):.1%}); "
          f"largest burst: {max(e['same_moment_stars'] for e in out)} other stars within 0.1 d")
    print("false-alarm load for a person (upside-down events across all best star-sectors) by threshold:")
    for thr in (7, 8, 9, 10, 12):
        left = [e for e in out if e["snr"] >= thr]
        print(f"  SNR >= {thr:>2}: {len(left):4d} events, {sum(not e['flags'] for e in left):4d} not flagged by the same-moment filter")
    big = sorted({(e["sector"], e["camera"], round(e["center"], 1)) for e in out if e["same_moment_stars"] >= 3})
    print("  bursts (sector, camera, BTJD):", big[:12], "..." if len(big) > 12 else "")
