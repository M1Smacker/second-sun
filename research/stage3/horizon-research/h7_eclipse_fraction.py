"""RS-002 H-7 (own data): what share of a star's time is inside an eclipse of the binary, i.e. the chance that a random planted (or real) transit time lands on an eclipse (the ecl_overlap flag then fires).
G2: Prsa+ 2022 table data/xmatch/ebs.csv, phase widths Wp-pf and Ws-pf (primary and secondary, fraction of the period). G3: TTC table 3 durations (hours) over the period. Aggregates only."""
import pandas as pd, numpy as np
R = r"D:\second-sun"
ebs = pd.read_csv(R + r"\data\xmatch\ebs.csv", usecols=["TIC", "Per", "Wp-pf", "Ws-pf"]).drop_duplicates("TIC").set_index("TIC")
g2 = pd.read_csv(R + r"\targets\g2_targets.csv", comment="#")
for sl in ("dev", "sealed"):
    t = g2[g2.slice == sl].tic.values
    d = ebs.reindex(t).dropna(subset=["Wp-pf"])
    f = d["Wp-pf"].fillna(0) + d["Ws-pf"].fillna(0)
    print(f"G2 {sl}: {len(d)} of {len(t)} stars with a width; share of time inside eclipses: median {100 * f.median():.1f}%, 10th to 90th percentile {100 * f.quantile(.1):.1f}% to {100 * f.quantile(.9):.1f}%, mean {100 * f.mean():.1f}%")
rows = []
for ln in open(R + r"\data\g3\catalog_ttc\table3_new_ebs.txt", encoding="utf-8"):
    s = ln.rstrip("\n")
    if len(s) > 100 and s[:10].strip().isdigit():
        g = lambda a, b: s[a - 1:b].strip()
        rows.append((int(g(1, 10)), float(g(45, 53)), g(69, 72), g(96, 99)))
t3 = pd.DataFrame(rows, columns=["tic", "P", "dp", "ds"])
g3 = pd.read_csv(R + r"\targets\g3_targets.csv", comment="#")
d = t3[t3.tic.isin(g3.tic)].copy()
d["f"] = (pd.to_numeric(d.dp, errors="coerce").fillna(0) + pd.to_numeric(d.ds, errors="coerce").fillna(0)) / (24 * d.P)
print(f"G3: {len(d)} stars; share of time inside eclipses: median {100 * d.f.median():.1f}%, 10th to 90th percentile {100 * d.f.quantile(.1):.1f}% to {100 * d.f.quantile(.9):.1f}%, mean {100 * d.f.mean():.1f}%")
