"""G3 chain targets (Vesper 0.8.1 data path; research/stage3/G3-PREREGISTRATION.md). targets/g3_chain_targets.csv = the locked G3 list (targets/g3_targets.csv) plus the columns the Stage 3 code reads
from the G1 and G2 tables: kic (empty), tic, tmag, p_bin_d, bjd0, morph (empty), tic_radius_rsun, slice. It changes no star and no rule; it only supplies the ephemeris and eclipse lengths the C5 and
eclipse overlap flags need, from the catalogue the G3 list itself was drawn from (TESS Ten Thousand Catalog table 3, Kostov et al. 2025).
bjd0 = t0_btjd + 57000 (the BJD - 2400000 scale the G1 table uses; stage3_core.Ephem subtracts 57000). tic_radius_rsun = the TIC radius read from the FITS headers (targets/host_radii_g2_g3.csv, T107), 4 decimals;
empty where the headers have none. dur_pri_h, dur_sec_h = the catalogue's median eclipse durations in hours (generalized-Gaussian fit; empty where absent); stage3_core.eb_widths turns them into phase widths
for G3, the same rule as the Prsa widths for G1 and G2 ("the catalogue's measured width where the star has one, else physics from the radius").
Usage: python targets_g3_chain.py   (writes the file; prints counts and the sha256)"""
import hashlib, pathlib, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from astropy.io import ascii

ROOT = pathlib.Path(r"D:\second-sun")
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
T3 = ROOT / "data" / "g3" / "catalog_ttc" / "table3_new_ebs.txt"
g = pd.read_csv(ROOT / "targets" / "g3_targets.csv", comment="#")
t3 = ascii.read(T3, format="mrt").to_pandas().drop_duplicates("TIC").set_index("TIC").loc[g.tic]
assert np.allclose(t3.Per.values, g.p_bin_d.values, atol=1e-6) and np.allclose(t3["T0-pri"].values, g.t0_btjd.values, atol=1e-4), "the catalogue rows must be the ones the locked list was made from"
rad = pd.read_csv(ROOT / "targets" / "host_radii_g2_g3.csv")
rad = rad[rad["set"] == "g3"].drop_duplicates("tic").set_index("tic").radius_rsun.reindex(g.tic)
rad = rad.where(rad > 0)                                                  # the headers use -1 for "no radius"
f = lambda x, fmt: "" if not np.isfinite(x) else format(x, fmt)
rows = [f",{int(r.tic)},{r.tmag:.2f},{r.p_bin_d:.6f},{r.t0_btjd + 57000.0:.4f},,{f(rd, '.4f')},{f(t3['Dur-pri'][r.tic], '.1f')},{f(t3['Dur-sec'][r.tic], '.1f')},g3"
        for r, rd in zip(g.itertuples(), rad.values)]
head = (f"# G3 chain targets, made by pipeline/targets_g3_chain.py on 3 Nov 2026 from targets/g3_targets.csv (sha256 {sha(ROOT / 'targets' / 'g3_targets.csv')[:16]}), TTC table 3 (sha256 {sha(T3)[:16]}) "
        f"and targets/host_radii_g2_g3.csv (sha256 {sha(ROOT / 'targets' / 'host_radii_g2_g3.csv')[:16]}).\n"
        "# bjd0 = t0_btjd + 57000; tic_radius_rsun = TIC radius from the FITS headers (T107); dur_pri_h and dur_sec_h = TTC median eclipse durations in hours. No star, slice or rule differs from the locked G3 list.\n"
        "kic,tic,tmag,p_bin_d,bjd0,morph,tic_radius_rsun,dur_pri_h,dur_sec_h,slice\n")
path = ROOT / "targets" / "g3_chain_targets.csv"
path.write_bytes((head + "\n".join(rows) + "\n").encode("utf-8"))      # plain \n line ends, the same bytes on every machine
print("wrote", path, "| stars", len(rows), "| with radius:", int(np.isfinite(rad.values).sum()), "| with primary duration:", int(t3["Dur-pri"].notna().sum()),
      "| with secondary duration:", int(t3["Dur-sec"].notna().sum()), "| with neither duration nor radius:", int((t3["Dur-pri"].isna() & ~np.isfinite(rad.values)).sum()))
print("sha256", sha(path))
