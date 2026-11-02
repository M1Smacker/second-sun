"""G3 star list (2 Nov 2026; research/stage3/G3-PREREGISTRATION.md). Rule, applied to table 3 of the TESS Ten Thousand Catalog (Kostov et al. 2025, ApJS 279, 50; data\\g3\\catalog_ttc\\table3_new_ebs.txt):
one row per TIC; binary period over 7 days; Tmag 13.5 or brighter; TIC not in targets\\g1_targets.csv, targets\\g2_targets.csv or the saved Prsa 2022 table (data\\xmatch\\ebs.csv).
No light curve is read. Writes targets\\g3_targets.csv (sorted by TIC, fixed number formats) and prints its sha256. Usage: python targets_g3.py"""
import hashlib, pathlib, warnings
warnings.filterwarnings("ignore")
import pandas as pd
from astropy.io import ascii

ROOT = pathlib.Path(r"D:\second-sun")
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
T3 = ROOT / "data" / "g3" / "catalog_ttc" / "table3_new_ebs.txt"
SRC = {"g1": ROOT / "targets" / "g1_targets.csv", "g2": ROOT / "targets" / "g2_targets.csv", "prsa": ROOT / "data" / "xmatch" / "ebs.csv"}
tic = lambda p, **kw: set(pd.read_csv(p, **kw).iloc[:, [c.lower() for c in pd.read_csv(p, nrows=0, **kw).columns].index("tic")].dropna().astype(int))
seen = tic(SRC["g1"], comment="#") | tic(SRC["g2"], comment="#") | tic(SRC["prsa"])
t = ascii.read(T3, format="mrt").to_pandas()
assert t.TIC.is_unique, "table 3 should have one row per TIC"
t = t[(t.Per > 7) & (t.Tmag <= 13.5) & ~t.TIC.isin(seen)].sort_values("TIC")
head = [
    "# G3 target list, 2 Nov 2026 (research/stage3/G3-PREREGISTRATION.md). Rule: TESS Ten Thousand Catalog table 3 (Kostov et al. 2025, ApJS 279, 50, https://arxiv.org/abs/2506.05631), one row per TIC, period over 7 d, Tmag 13.5 or brighter, TIC not in g1_targets, g2_targets or the saved Prsa 2022 table",
    f"# table 3 sha256 {sha(T3)}; g1_targets sha256 {sha(SRC['g1'])}; g2_targets sha256 {sha(SRC['g2'])}; data/xmatch/ebs.csv sha256 {sha(SRC['prsa'])}",
    "# t0_btjd = primary eclipse epoch in BTJD (BJD-2457000); dur_pri_h = primary eclipse duration in hours; sectors = number of TESS sectors the catalogue counts; ruwe = Gaia RUWE (a covariate, not a cut); slice = g3 for every star (no development split)",
    "tic,tmag,p_bin_d,t0_btjd,dur_pri_h,sectors,ruwe,slice"]
rows = [f"{int(r.TIC)},{r.Tmag:.2f},{r.Per:.6f},{r['T0-pri']:.4f},{r['Dur-pri']:.1f},{int(r.Sectors)},{'' if pd.isna(r.RUWE) else f'{r.RUWE:.2f}'},g3" for _, r in t.iterrows()]
out = ROOT / "targets" / "g3_targets.csv"
out.write_text("\n".join(head + rows) + "\n", encoding="utf-8", newline="\n")
print(f"{len(rows)} stars; sectors median {t.Sectors.median():.0f}, total star-sectors (upper bound for files) {int(t.Sectors.sum())}; Tmag median {t.Tmag.median():.1f}")
print("sha256", sha(out))
