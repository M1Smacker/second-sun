"""G2 chain targets: targets/g2_chain_targets.csv = the locked G2 list (targets/g2_targets.csv) plus the columns the Stage 3 code reads from the G1 table, taken from the same TESS eclipsing
binary catalogue (Prsa et al. 2022, data/xmatch/ebs.csv, first row per TIC as in coverage_g2.py). It changes no star, no slice and no rule; it only supplies the ephemeris the C5 and eclipse
overlap flags need. Columns as in g1_targets.csv: kic (empty), tic, tmag, p_bin_d, bjd0, morph, tic_radius_rsun, plus slice.
bjd0 is the catalogue BJD0 (BJD - 2457000) + 57000, i.e. on the BJD - 2400000 scale the G1 table uses (stage3_core.Ephem subtracts 57000). The TESS catalogue has no stellar radius, so tic_radius_rsun is
nan: stars with a catalogue eclipse width use it, the others are never flagged by the overlap rule (the 0.35 d C5 rule still applies to them).
Usage: python targets_g2_chain.py   (writes the file; prints counts)"""
import hashlib, pathlib
import numpy as np, pandas as pd

ROOT = pathlib.Path(r"D:\second-sun")
g = pd.read_csv(ROOT / "targets" / "g2_targets.csv", comment="#")
e = pd.read_csv(ROOT / "data" / "xmatch" / "ebs.csv").drop_duplicates("TIC").set_index("TIC").loc[g.tic]
assert np.allclose(e.Per.values, g.p_bin_d.values, atol=1e-6) and np.allclose(e.Tmag.values, g.tmag.values, atol=1e-3), "the catalogue rows must be the ones the locked list was made from"
out = pd.DataFrame(dict(kic="", tic=g.tic.values, tmag=g.tmag.values, p_bin_d=g.p_bin_d.values, bjd0=(pd.to_numeric(e.BJD0, errors="coerce").values + 57000.0),
                        morph=g.morph.values, tic_radius_rsun=np.nan, slice=g["slice"].values))
head = (f"# G2 chain targets, made by pipeline/targets_g2_chain.py on 29 Oct 2026 from targets/g2_targets.csv (sha256 {hashlib.sha256((ROOT / 'targets' / 'g2_targets.csv').read_bytes()).hexdigest()[:16]}) "
        f"and data/xmatch/ebs.csv (sha256 {hashlib.sha256((ROOT / 'data' / 'xmatch' / 'ebs.csv').read_bytes()).hexdigest()[:16]}).\n"
        "# bjd0 = catalogue BJD0 (BJD-2457000) + 57000; tic_radius_rsun = nan (the TESS catalogue has none). No star, slice or rule differs from the locked G2 list.\n")
path = ROOT / "targets" / "g2_chain_targets.csv"
path.write_bytes((head + out.to_csv(index=False, lineterminator="\n")).encode("utf-8"))   # plain \n line ends, the same bytes on every machine
print("wrote", path, "| stars", len(out), "| slices", out["slice"].value_counts().to_dict(), "| no BJD0:", int(out.bjd0.isna().sum()),
      "| with eclipse widths:", int(pd.to_numeric(e["Wp-pf"], errors="coerce").gt(0).sum()))
