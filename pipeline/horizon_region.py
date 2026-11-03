"""Horizon: integrate the reach over a region of cells and put an error band on it (research/stage3/HORIZON-R0-RULE.md, Amendment 2 of 3 Nov 2026). The region of Armstrong et al. 2014's coplanar occurrence is planets above
6 Earth radii inside about 300 days (here: radius bins 6 to 16, period bins 1 to 6, i.e. 10 to 334 days). Assumption, stated: a star's planet, if it has one, falls uniformly (per bin: uniform in radius, log-uniform in period) among
the cells of the region where that star is allowed (period at least F x binary period). Expected detections for an occurrence f per star: f x D, D = sum over stars of the mean chance over the star's allowed cells in the region.
95% ceiling for zero found: 3.0 / D; with k = 1 (the known planet counted): 4.74 / D. Error band: the recovery table is re-made from 200 resamples of the development star-sectors (the dominant error; the host radii, noise and windows are held).
Usage: python horizon_region.py [set] [n_boot]    (default g2sealed, 200; writes research\stage3\horizon-region-<set>.txt; aggregates only)"""
import sys, numpy as np, pandas as pd
import horizon_reach as H

RMASK = H.RAD_C >= 6          # radius bins 6-16 (centres 7 to 15)
PMASK = np.arange(len(H.PER_C)) <= 5   # period bins 10 to 334 d


def region_D(store, nstars_total):
    D, n = 0.0, 0
    for tic, P in store.items():
        sub = P[np.ix_(RMASK, PMASK)]
        ok = np.isfinite(sub)
        if ok.any():
            D += float(np.nanmean(sub)); n += 1
    return D, n


_CACHE = {}


def run(sset, floor, dil, tabs):
    star, ss, nv, med = _CACHE.setdefault(sset, H.sector_table(sset)); store = {}
    H.reach(star, ss, tabs, floor, dil, store)
    return region_D(store, len(star))


if __name__ == "__main__":
    sset = sys.argv[1] if len(sys.argv) > 1 else "g2sealed"; B = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    base = pd.read_pickle(f"{H.ROOT}/data/chain_recovery_g2/rows_v9base.pkl"); base = base[base.K.notna() & (base.sign == 1)]
    key = base.groupby(["tic", "sector"]).ngroup().values; ng = key.max() + 1; groups = [np.where(key == k)[0] for k in range(ng)]
    rng = np.random.default_rng(20261103)
    out = [f"Horizon region integral, star set {sset}: planets above 6 Earth radii, 10 to 334 days (Armstrong 2014 region: R > 6 Earth radii, P < 300 d). Assumptions in the file header of pipeline/horizon_region.py. Aggregates only.", ""]
    for name, fl, dl in (("main (F 5.6, no dilution)", 5.6, 1.0), ("F 3", 3.0, 1.0), ("F 6.9", 6.9, 1.0), ("dilution 0.5", 5.6, 0.5)):
        D0, n0 = run(sset, fl, dl, H.recovery_tables(base))
        Ds = []
        if name.startswith("main") or B <= 0 or True:
            for b in range(B if name.startswith("main") else min(B, 40)):
                pick = rng.integers(0, ng, ng); idx = np.concatenate([groups[k] for k in pick])
                Ds.append(run(sset, fl, dl, H.recovery_tables(base.iloc[idx].reset_index(drop=True)))[0])
        lo, hi = (np.percentile(Ds, 2.5), np.percentile(Ds, 97.5)) if Ds else (np.nan, np.nan)
        out.append(f"{name}: stars with an allowed cell in the region {n0}; D = {D0:.1f} stars-equivalent (95% band {lo:.1f} to {hi:.1f}, {len(Ds)} resamples)")
        out.append(f"   95% ceiling on the occurrence, zero found: {100 * 3.0 / D0:.1f}% (band {100 * 3.0 / hi:.1f}% to {100 * 3.0 / lo:.1f}%); with the known planet counted (k = 1): {100 * 4.74 / D0:.1f}% (band {100 * 4.74 / hi:.1f}% to {100 * 4.74 / lo:.1f}%)")
        print(out[-2]); print(out[-1], flush=True)
    out += ["", "Read: Armstrong 2014 reports about 10% for this region (coplanar, from Kepler eclipsing binaries; UNCERTAIN how it maps onto our TESS binaries). A ceiling below 10% would be in tension with it; a ceiling above 10% is no constraint.",
            "Caveats: UNCERTAIN window function and independent epochs (R0 Amendment 1); depth uses the TIC radius with no dilution unless stated; recovery table from the development split only; band covers the table only."]
    open(f"{H.ROOT}/research/stage3/horizon-region-{sset}.txt", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
