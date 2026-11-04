"""Census step 1b (night of 4 Nov 2026): how does the share of eclipsing binaries among 2-minute stars depend on brightness and number of sectors? Own data: Prsa 2022 EBs (sectors 1-26) against the 2-minute target lists of sectors 1-26.
Then apply to the pilot pools of CENSUS-STEP2-RESEARCH (stars never 2-minute targets in S1-26, with S27+ coverage). Counts only."""
import glob, re, numpy as np, pandas as pd
R = r"D:\second-sun"
rows = []
for f in glob.glob(R + r"\data\census_targets_2m\all_targets_S*_v*.csv"):
    s = int(re.search(r"_S(\d+)_", f).group(1))
    d = pd.read_csv(f, comment="#"); d.columns = [c.strip() for c in d.columns]
    d = d.rename(columns={"TICID": "TIC"})[["TIC", "Tmag"]]; d["s"] = s; rows.append(d)
A = pd.concat(rows)
old = A[A.s <= 26].groupby("TIC").agg(T=("Tmag", "min"), n=("s", "nunique"))
new = A[(A.s >= 27) & (A.s <= 109)].groupby("TIC").agg(T=("Tmag", "min"), n=("s", "nunique"))
e = pd.read_csv(R + r"\data\xmatch\ebs.csv").drop_duplicates("TIC")
eb = set(e.TIC.astype(int)); g2type = set(e[(e.Per > 5) & (e.Morph < 0.7)].TIC.astype(int))
old["eb"] = old.index.isin(eb); old["g2"] = old.index.isin(g2type)
tb = [(0, 10), (10, 12), (12, 13.5)]
nb = [(1, 1), (2, 3), (4, 7), (8, 99)]
print("S1-26 2-minute stars: EB share (and G2-type share) by Tmag bin and number of sectors in S1-26")
tab = {}
for (tl, th) in tb:
    for (nl, nh) in nb:
        g = old[(old["T"] > tl if tl > 0 else True) & (old["T"] <= th) & (old.n >= nl) & (old.n <= nh)]
        if len(g) >= 50:
            tab[(tl, th, nl, nh)] = (g.eb.mean(), g.g2.mean(), len(g))
            print(f"  Tmag {tl}-{th}, sectors {nl}-{nh}: stars {len(g):6d}; EB {100*g.eb.mean():5.2f}%; G2-type {100*g.g2.mean():5.2f}%")
        else:
            print(f"  Tmag {tl}-{th}, sectors {nl}-{nh}: stars {len(g):6d} (too few)")
oldset = set(old.index)
new["new"] = ~new.index.isin(oldset)
print("\nPilot pools (stars new to 2-minute, S27-109 coverage) and expected EBs using the S1-26 shares of the same Tmag bin and the sector bin:")
def pool(nm, mask):
    g = new[mask]; ex = 0; ex2 = 0; used = 0
    for (tl, th) in tb:
        for (nl, nh) in nb:
            sel = g[(g["T"] > tl if tl > 0 else True) & (g["T"] <= th) & (g.n >= nl) & (g.n <= nh)]
            k = (tl, th, nl, nh)
            if len(sel) and k in tab:
                ex += len(sel) * tab[k][0]; ex2 += len(sel) * tab[k][1]; used += len(sel)
            elif len(sel):
                # fall back to the share of the same Tmag bin over all sector counts
                gg = old[(old["T"] > tl if tl > 0 else True) & (old["T"] <= th)]
                ex += len(sel) * gg.eb.mean(); ex2 += len(sel) * gg.g2.mean(); used += len(sel)
    print(f"  {nm:60s} stars {len(g):7,d}; expected EBs {ex:7.0f}; expected G2-type {ex2:6.0f}")
pool("new, Tmag<=13.5 (all)", new["new"] & (new["T"] <= 13.5))
pool("new, Tmag<=13.5, 8+ sectors (pilot pool)", new["new"] & (new["T"] <= 13.5) & (new.n >= 8))
pool("new, Tmag<=12, 6+ sectors", new["new"] & (new["T"] <= 12) & (new.n >= 6))
pool("new, Tmag<=10, 4+ sectors", new["new"] & (new["T"] <= 10) & (new.n >= 4))
pool("new, Tmag<=11, 4+ sectors", new["new"] & (new["T"] <= 11) & (new.n >= 4))
