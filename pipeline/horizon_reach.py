"""Horizon R1/R2 (research/stage3/HORIZON-R0-RULE.md, locked 3 Nov 2026): the reach map and the zero-found ceiling per cell, in the unchanged rules of R0.
Recovery table S(K, duration) = tier-1 share of PLANTED dips (sign +1) from data/chain_recovery_g2/rows_v9base.pkl: the whole frozen chain with VESPER_OPTS=c6 (Vesper 0.8.0 rules, identical in 0.8.1)
on the G2 DEVELOPMENT run dev_428c5fb454cd (asserted: every star is slice dev), K = 6..18 x the 8 h box noise, durations 4, 8, 14, 20 h, one table for the SPOC family and one for QLP.
For each usable star-sector of a star set (its Stage 1 audit best-product table): noise at 8 h of its longest-covered product (log-log between the audited 6.5 h and 15 h values; the planting used the same product), covered days (cadences searched), host radius, binary period.
Per cell (radius bin centre x period bin centre): depth = (Rp / R_star)^2 (no dilution unless asked), K = depth / noise8, duration from Kepler's third law (total mass 2 Msun, as the frozen eclipse-length rule), spread by a factor
0.7 to 1.4 (averaged over five log-spaced factors) and clipped to 3..20 h; window function W = min(1, covered days / planet period) (UNCERTAIN: an approximation to folding the real windows); chance of a star-sector
= W x S; a star's chance = 1 - product over its star-sectors (independent epochs: UNCERTAIN); a cell counts a star only if P_planet >= F x P_binary. Ceiling for zero found = -ln(0.05) / sum of the star chances.
Aggregates only: no star ID, no event. Usage: python horizon_reach.py   (writes research/stage3/horizon-reach-<set>-<scenario>.txt)"""
import sys, os, numpy as np, pandas as pd
from scipy.interpolate import RegularGridInterpolator

ROOT = "D:/second-sun"
RAD_EDGES = np.linspace(2, 16, 8); RAD_C = 0.5 * (RAD_EDGES[:-1] + RAD_EDGES[1:])
PER_EDGES = 10 * 60 ** (np.arange(8) / 7); PER_C = np.sqrt(PER_EDGES[:-1] * PER_EDGES[1:])
KS, DURS = (6.0, 8.0, 10.0, 12.0, 14.0, 18.0), (4.0, 8.0, 14.0, 20.0)
SPREAD = np.exp(np.linspace(np.log(0.7), np.log(1.4), 5))
R_E = 109.076                                                    # Earth radii per solar radius
FAMILY = ("SPOC", "TESS-SPOC")                                   # the products a second 2-minute or FFI SPOC file backs up (sap_twin.FAMILY)


def recovery_tables():
    d = pd.read_pickle(f"{ROOT}/data/chain_recovery_g2/rows_v9base.pkl"); d = d[d.K.notna() & (d.sign == 1)]
    tg = pd.read_csv(f"{ROOT}/targets/g2_chain_targets.csv", comment="#").drop_duplicates("tic").set_index("tic")
    assert set(tg.loc[d.tic.unique(), "slice"]) == {"dev"}, "R1 uses the development split only"
    d = d.assign(fam=d.best.isin(FAMILY), tier1=d.tier1.astype(bool))
    out = {}
    for fam, g in d.groupby("fam"):
        m = g.groupby(["dur", "K"]).tier1.mean().unstack().reindex(index=DURS, columns=KS)
        out[bool(fam)] = (RegularGridInterpolator((np.log(DURS), np.log(KS)), m.values, bounds_error=False, fill_value=None), m, g.groupby(["dur", "K"]).size().unstack().reindex(index=DURS, columns=KS))
    return out


def sector_table(sset):
    """One row per usable star-sector: tic, fam, noise8 (ppm), covered_d; plus per-star radius and binary period."""
    if sset in ("g2sealed", "g2dev"):
        tg = pd.read_csv(f"{ROOT}/targets/g2_chain_targets.csv", comment="#").drop_duplicates("tic")
        tg = tg[tg["slice"] == ("sealed" if sset == "g2sealed" else "dev")]
        b = pd.read_csv(f"{ROOT}/data/g2/audit/best_per_star_sector.csv"); audit_path = f"{ROOT}/data/g2/audit/audit_all.csv"
        hr = pd.read_csv(f"{ROOT}/targets/host_radii_g2_g3.csv"); hr = hr[hr["set"] == "g2"].drop_duplicates("tic").set_index("tic").radius_rsun
        rad = tg.tic.map(hr)
    else:
        tg = pd.read_csv(f"{ROOT}/targets/g3_chain_targets.csv", comment="#").drop_duplicates("tic")
        b = pd.read_csv(f"{ROOT}/data/g3/audit/best_per_star_sector.csv"); audit_path = f"{ROOT}/data/g3/audit/audit_all.csv"
        rad = tg.tic_radius_rsun
    star = pd.DataFrame(dict(tic=tg.tic.values, rad=rad.values, pbin=tg.p_bin_d.values)).set_index("tic")
    nvalid = int((star.rad > 0).sum()); med = float(star.rad[star.rad > 0].median()); star["rad"] = star.rad.where(star.rad > 0, med)
    b = b[b.tic.isin(star.index)][["tic", "sector", "product"]]                        # usable star-sectors and their best product (the recovery table is split by it)
    au = pd.read_csv(audit_path)
    au = au[(au.status == "ok") & (au["noise_6.5h_ppm"] > 0) & (au["noise_15h_ppm"] > 0)].copy()
    a = np.log(au["noise_15h_ppm"] / au["noise_6.5h_ppm"]) / np.log(15 / 6.5)
    au["noise8"] = au["noise_6.5h_ppm"] * (8 / 6.5) ** a
    au["covered_d"] = au.n_searched * au.cadence_min / 1440.0
    # the planting used the 8 h noise of the star-sector's LONGEST-covered product (chain_recovery._run_group), so K here is measured on the same product; checked on 284 dev star-sectors:
    # interpolated / measured 8 h noise has median 0.98 and 16 to 84% range 0.94 to 1.04 (the best product alone gave 0.93 with 0.64 to 1.00)
    au = au.sort_values("covered_d", ascending=False).drop_duplicates(["tic", "sector"])[["tic", "sector", "noise8", "covered_d"]]
    b = b.merge(au, on=["tic", "sector"], how="inner")
    b["fam"] = b["product"].isin(FAMILY)
    return star, b[["tic", "sector", "fam", "noise8", "covered_d"]], nvalid, med


def reach(star, ss, tabs, floor=5.6, dilution=1.0):
    """Sum over stars of the chance of a tier-1 detection, per (radius, period) cell. Returns (sum, number of stars allowed in the cell)."""
    S = np.zeros((len(RAD_C), len(PER_C))); NS = np.zeros_like(S)
    sec = {t: g for t, g in ss.groupby("tic")}
    for tic, g in sec.items():
        r_star, pbin = star.rad[tic], star.pbin[tic]
        for j, P in enumerate(PER_C):
            if P < floor * pbin:
                continue
            NS[:, j] += 1
            a_rsun = 215.03 * (2.0 * (P / 365.25) ** 2) ** (1 / 3)
            for i, Rp in enumerate(RAD_C):
                depth = dilution * (Rp / (R_star_e := r_star * R_E)) ** 2 * 1e6
                dur0 = 24 * P / np.pi * (r_star + Rp / R_E) / a_rsun
                miss = 1.0
                for fam, gg in g.groupby("fam"):
                    K = depth / gg.noise8.values
                    s = np.zeros(len(gg))
                    for f in SPREAD:
                        d = np.clip(dur0 * f, 3.0, 20.0)
                        pts = np.column_stack([np.full(len(gg), np.log(np.clip(d, DURS[0], DURS[-1]))), np.log(np.clip(K, KS[0], KS[-1]))])
                        s += np.clip(tabs[bool(fam)][0](pts), 0, 1) * (K >= KS[0])
                    s /= len(SPREAD)
                    w = np.minimum(1.0, gg.covered_d.values / P)
                    miss *= float(np.prod(1 - w * s))
                S[i, j] += 1 - miss
    return S, NS


def table_text(S, NS, title):
    lines = [title, "rows: planet radius bin centre (Earth radii); columns: period bin centre (days)", "sum of detection chance over stars  |  95% ceiling for zero found = 3.0 / sum, as a share of stars (blank: no star allowed)"]
    lines.append("      R \\ P | " + " | ".join(f"{p:6.0f}" for p in PER_C))
    for i, R in enumerate(RAD_C):
        lines.append(f"  {R:6.0f}    | " + " | ".join(f"{S[i, j]:6.2f}" for j in range(len(PER_C))))
    lines.append("      ceiling | " + " | ".join(f"{p:6.0f}" for p in PER_C))
    for i, R in enumerate(RAD_C):
        lines.append(f"  {R:6.0f}    | " + " | ".join((f"{min(3.0 / S[i, j], 9.99):6.3f}" if S[i, j] > 0.05 else "   >10") if NS[i, j] else "      -" for j in range(len(PER_C))))
    lines.append("      stars allowed | " + " | ".join(f"{int(NS[0, j]):6d}" for j in range(len(PER_C))))
    return lines


if __name__ == "__main__":
    tabs = recovery_tables()
    head = ["Horizon reach and zero-found ceiling (R0 rule locked 3 Nov 2026, commit cc6604e). An UPPER BOUND on what the frozen search could have seen, not a measurement of how common planets are.",
            "Recovery table: planted dips on the G2 development split, 0.8.0 rules (c6), rows_v9base.pkl; share of planted dips that end as tier 1, by product family (K = depth / 8 h box noise)."]
    for fam, (_, m, n) in tabs.items():
        head += [f"  {'SPOC family' if fam else 'QLP'} (injections per cell {int(n.values.min())} to {int(n.values.max())}); rows duration 4, 8, 14, 20 h; columns K = 6, 8, 10, 12, 14, 18:"] + ["    " + " ".join(f"{v:5.2f}" for v in row) for row in m.values]
    scen = [("main", 5.6, 1.0), ("floor3", 3.0, 1.0), ("floor6.9", 6.9, 1.0), ("dilute0.5", 5.6, 0.5)]
    sets = sys.argv[1:] or ["g2sealed", "g3", "g2dev"]
    for sset in sets:
        star, ss, nvalid, med = sector_table(sset)
        for name, fl, dl in scen:
            S, NS = reach(star, ss, tabs, fl, dl)
            txt = head + ["", f"STAR SET {sset}: {len(star)} stars, {ss.groupby('tic').ngroups} with a usable star-sector, {len(ss)} star-sectors; positive TIC radius for {nvalid} stars, the rest use the set median {med:.2f} Rsun.",
                          f"Scenario {name}: stability floor F = {fl}, dilution (share of light from the crossed star) = {dl}."] + table_text(S, NS, "")
            path = f"{ROOT}/research/stage3/horizon-reach-{sset}-{name}.txt"
            open(path, "w", encoding="utf-8", newline="\n").write("\n".join(txt) + "\n")
            print(path, "| max sum %.1f | cells with sum > 3: %d of 49" % (S.max(), int((S > 3).sum())), flush=True)
