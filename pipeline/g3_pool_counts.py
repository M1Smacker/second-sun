"""G3 star list, step T111b (2 Nov 2026): COUNT the candidate rule pools from the TESS Ten Thousand Catalog tables (data\\g3\\catalog_ttc) and their overlap with the stars already searched (G1, G2) and with
the saved Prsa 2022 table. Counts only: no rule is chosen here and no light curve is read or downloaded (the G3 rule, number and hash are written afterwards in T112, before any download).
Usage: python g3_pool_counts.py    (writes research\\stage3\\g3-pool-counts-2026-11-02.txt)"""
import warnings; warnings.filterwarnings("ignore")
import pathlib
import numpy as np, pandas as pd
from astropy.io import ascii

ROOT = pathlib.Path(r"D:\second-sun")
D = ROOT / "data" / "g3" / "catalog_ttc"
OUT, P = [], None
P = lambda s="": (OUT.append(s), print(s))

t3 = ascii.read(D / "table3_new_ebs.txt", format="mrt").to_pandas()
t4 = ascii.read(D / "table4_known_ebs.txt", format="mrt").to_pandas()
tic = lambda df: set(pd.to_numeric(df[[c for c in df.columns if c.lower() == "tic"][0]], errors="coerce").dropna().astype(int))
g1 = tic(pd.read_csv(ROOT / "targets" / "g1_targets.csv", comment="#"))
g2 = tic(pd.read_csv(ROOT / "targets" / "g2_targets.csv", comment="#"))
prsa = tic(pd.read_csv(ROOT / "data" / "xmatch" / "ebs.csv"))
P(f"G3 pool counts from the TESS Ten Thousand Catalog (Kostov et al. 2025): table 3 {len(t3)} new eclipsing binaries, table 4 {len(t4)} known ones. Searched before: G1 {len(g1)} stars, G2 {len(g2)} stars; saved Prsa 2022 table {len(prsa)} stars.")
a, b = tic(t3), tic(t4)
P(f"overlap of table 3 with G1 {len(a & g1)}, G2 {len(a & g2)}, Prsa {len(a & prsa)}; table 4 with G1 {len(b & g1)}, G2 {len(b & g2)}, Prsa {len(b & prsa)}; table 3 with table 4 {len(a & b)}")
P(f"table 3 Tmag quantiles (5, 25, 50, 75, 95%): " + ", ".join(f"{x:.1f}" for x in t3.Tmag.quantile([.05, .25, .5, .75, .95])) + f"; period quantiles (d): " + ", ".join(f"{x:.2f}" for x in t3.Per.quantile([.05, .25, .5, .75, .95, .99])))
P(f"table 4 periods (TESS): over 7 d {int((t4['Per-TESS'] > 7).sum())} of {len(t4)}; no Tmag in this table (a TIC join would be needed)")
P("")
t = t3.copy()
t["frac"] = t["Dur-pri"] / (t.Per * 24)                                     # eclipse duration as a share of the orbit: a rough detachedness proxy (the table has no morphology column)
t["new"] = ~t.TIC.isin(g1 | g2 | prsa)
P("Pools of table 3 (all stars, then the part NOT in G1, G2 or the saved Prsa table):")
P("   rule | all | not searched before | of those: RUWE <= 1.4 | 2 or more sectors | 4 or more sectors | duration share of orbit <= 0.1 (detached proxy)")
for name, m in [("P > 7 d, Tmag <= 13.5", (t.Per > 7) & (t.Tmag <= 13.5)), ("P > 7 d, Tmag <= 13.0", (t.Per > 7) & (t.Tmag <= 13.0)), ("P > 7 d, Tmag <= 12.5", (t.Per > 7) & (t.Tmag <= 12.5)),
                ("P > 7 d, Tmag <= 14.0", (t.Per > 7) & (t.Tmag <= 14.0)), ("P > 7 d, Tmag <= 14.5", (t.Per > 7) & (t.Tmag <= 14.5)), ("P > 7 d, any Tmag", (t.Per > 7)),
                ("P > 5 d, Tmag <= 13.5", (t.Per > 5) & (t.Tmag <= 13.5)), ("P > 10 d, Tmag <= 13.5", (t.Per > 10) & (t.Tmag <= 13.5)), ("P > 15 d, Tmag <= 14.0", (t.Per > 15) & (t.Tmag <= 14.0))]:
    n = t[m & t.new]
    P(f"   {name} | {int(m.sum())} | {len(n)} | {int((n.RUWE <= 1.4).sum())} | {int((n.Sectors >= 2).sum())} | {int((n.Sectors >= 4).sum())} | {int((n.frac <= 0.1).sum())}")
P("")
m = (t.Per > 7) & (t.Tmag <= 13.5) & t.new
P(f"For the main candidate rule (P > 7 d, Tmag <= 13.5, not searched before): {int(m.sum())} stars; sectors observed quantiles (25, 50, 75, max): " + ", ".join(f"{x:.0f}" for x in list(t[m].Sectors.quantile([.25, .5, .75])) + [t[m].Sectors.max()])
  + f"; Tmag median {t[m].Tmag.median():.1f}; period median {t[m].Per.median():.1f} d, max {t[m].Per.max():.1f} d; duration share of orbit median {t[m].frac.median():.3f}; Comments filled {int(t[m].Com.notna().sum())}")
(ROOT / "research" / "stage3" / "g3-pool-counts-2026-11-02.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
