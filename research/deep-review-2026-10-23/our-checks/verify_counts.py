"""Re-count the review's numbers from our own target files."""
import pandas as pd, numpy as np
cov = pd.read_csv(r"D:\second-sun\targets\g1_coverage.csv")
tg = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#")
sec = lambda s: [int(float(x)) for x in str(s).split()] if isinstance(s, str) else []
q = [x for s in cov.qlp_sectors for x in sec(s)]
ts = [x for s in cov.tess_spoc_sectors for x in sec(s)]
FFI30 = {x for x in q if x <= 26}
print("QLP star-sectors:", len(q), "| 30-min (S<=26):", sum(x <= 26 for x in q), "| pre-56 (27..55):",
      sum(27 <= x <= 55 for x in q), "| all pre-56:", sum(x < 56 for x in q))
print("TESS-SPOC star-sectors at S<=26:", sum(x <= 26 for x in ts))
# star-sectors at S<=26 with QLP but no SPOC 2-min in that sector
n = 0
for _, r in cov.iterrows():
    sp = set(sec(r.spoc_sectors))
    n += sum(1 for x in sec(r.qlp_sectors) if x <= 26 and x not in sp)
print("S<=26 QLP star-sectors with no SPOC 2-min that sector:", n)
print("QLP sectors seen <=26:", sorted(FFI30))
print("stars with no SPOC and no TESS-SPOC:", ((cov.n_spoc == 0) & (cov.n_tess_spoc == 0)).sum())
print("median Tmag:", tg.drop_duplicates("tic").tmag.median(), "| median n_qlp:", cov.n_qlp.median())
print("stars with <=1 SPOC sector:", (cov.n_spoc <= 1).sum(), "of", len(cov))
hosts = {"Kepler-16": 299096355, "Kepler-38": 158316612, "Kepler-64": 170348142, "Kepler-453": 164457525,
         "Kepler-1647": 170344769, "Kepler-34": 271164763, "Kepler-35": 0}
for k, v in hosts.items():
    m = tg[tg.tic == v]
    print(f"  {k} TIC {v}: in G1 = {len(m) > 0}", m[["kic", "tmag", "p_bin_d"]].values.tolist())
print("TIC radius > 3 Rsun rows:", (tg.tic_radius_rsun > 3).sum())
