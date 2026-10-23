"""B3: G1 stars whose OTHER catalogue rows fail the cut (so those eclipses are never masked).
Uses research/wave-3-pipeline/g1_tmag.csv, the same input targets_g1.py selects from."""
import pandas as pd
m = pd.read_csv(r"D:\second-sun\research\wave-3-pipeline\g1_tmag.csv")
tg = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#")
g1 = set(tg.kic.astype(int))
mm = m[m.kic.astype(int).isin(g1)]
for kic, grp in mm.groupby("kic"):
    if len(grp) > 1:
        rows = [(r.p_bin, r.morph, bool(r.morph < 0.5 and r.p_bin > 5)) for r in grp.itertuples()]
        if not all(ok for *_, ok in rows):
            print(f"KIC {int(kic)}: (period, morph, passes cut) {rows}")
