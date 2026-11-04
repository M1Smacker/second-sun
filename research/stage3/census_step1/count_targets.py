"""Census step 1: counts only. TESS 2-minute target lists (tess.mit.edu/public/target_lists), sectors 1-111.
No light curves read. Inputs: data/census_targets_2m/*.csv, data/xmatch/ebs.csv (Prsa 2022),
targets/g1,g2,g3 target lists, data/g3/catalog_ttc tables."""
import glob, os, re
import pandas as pd
R = r"D:\second-sun"
rows = []
for f in sorted(glob.glob(R + r"\data\census_targets_2m\all_targets_S*_v*.csv")):
    s = int(re.search(r"_S(\d+)_", f).group(1))
    d = pd.read_csv(f, comment="#")
    d.columns = [c.strip() for c in d.columns]
    d = d.rename(columns={"TICID": "TIC"})[["TIC", "Tmag"]]
    d["sector"] = s
    rows.append(d)
A = pd.concat(rows, ignore_index=True)
A["Tmag"] = pd.to_numeric(A.Tmag, errors="coerce")
P = print
OBS_LAST = 109  # sector 110 is running (to 26 Nov 2026), 111 is a plan only
old = A[A.sector <= 26]; new = A[(A.sector >= 27) & (A.sector <= OBS_LAST)]
P(f"rows (target-sectors): S1-26 {len(old):,}; S27-{OBS_LAST} {len(new):,}; S110-111 plan lists {len(A[A.sector>OBS_LAST]):,}")
P(f"unique stars: S1-26 {old.TIC.nunique():,}; S27-{OBS_LAST} {new.TIC.nunique():,}")
nS = new.groupby("TIC").sector.nunique()
tm = new.groupby("TIC").Tmag.min()
brk = [(0, 10), (10, 11), (11, 12), (12, 13), (13, 13.5), (13.5, 99)]
P("S27+ unique stars by Tmag, and by number of sectors:")
for lo, hi in brk:
    m = (tm > lo) & (tm <= hi) if lo > 0 else (tm <= hi)
    ids = tm.index[m]
    P(f"  Tmag {lo}-{hi}: {len(ids):,} stars; in 2+ sectors {int((nS[ids]>=2).sum()):,}; in 4+ sectors {int((nS[ids]>=4).sum()):,}; mean sectors {nS[ids].mean():.2f}")
newonly = set(new.TIC) - set(old.TIC)
P(f"stars with 2-minute data ONLY after sector 26 (never a 2-min target in S1-26): {len(newonly):,} of {new.TIC.nunique():,}")
bright = set(tm.index[tm <= 13.5])
P(f"  of those, Tmag <= 13.5: {len(newonly & bright):,}")
# known lists
ebs = pd.read_csv(R + r"\data\xmatch\ebs.csv"); pr = set(ebs.TIC.astype(int))
P(f"Prsa 2022 EBs {len(pr):,} (S1-26 2-min). Of them also 2-min targets in S27+: {len(pr & set(new.TIC)):,}")
fr = len(pr) / old.TIC.nunique()
P(f"EB share of S1-26 2-min unique stars: {len(pr):,}/{old.TIC.nunique():,} = {100*fr:.2f}%")
oldb = set(old.groupby('TIC').Tmag.min().index[old.groupby('TIC').Tmag.min() <= 13.5])
P(f"  same share for Tmag<=13.5: {len(pr & oldb):,}/{len(oldb):,} = {100*len(pr & oldb)/len(oldb):.2f}%")
def ticset(p):
    d = pd.read_csv(p, comment="#"); c = [x for x in d.columns if x.upper() in ("TIC", "TICID")][0]
    return set(d[c].astype(int))
srch = {}
for g in ("g1", "g2", "g3"):
    p = R + rf"\targets\{g}_targets.csv"
    if os.path.exists(p): srch[g] = ticset(p)
for g, s in srch.items(): P(f"searched {g}: {len(s):,} stars; also 2-min targets in S27+: {len(s & set(new.TIC)):,}")
# TTC (FFI binaries), table 3 new and 4 known: TIC column
import re as _re
for t in ("table3_new_ebs.txt", "table4_known_ebs.txt"):
    txt = open(R + rf"\data\g3\catalog_ttc\{t}", encoding="utf-8", errors="ignore").read().splitlines()
    ids = set()
    for ln in txt:
        m = _re.match(r"\s*(\d{4,12})\b", ln)
        if m: ids.add(int(m.group(1)))
    P(f"TTC {t}: {len(ids):,} TIC-like ids; also 2-min targets in S27+: {len(ids & set(new.TIC)):,}")
# what the simple EB-share would imply (rough, labelled estimate)
n_new_b = len(newonly & bright)
P(f"ROUGH (LIKELY at best, NOT measured): at the S1-26 EB share, {n_new_b:,} new bright stars would hold about {int(n_new_b*fr):,} EBs; of all S27+ stars not already listed about {int((new.TIC.nunique()-len(pr & set(new.TIC)))*fr):,}.")
sec = new.groupby("sector").agg(n=("TIC","size"), b=("Tmag", lambda x: int((x<=13.5).sum())))
P("per sector (rows, Tmag<=13.5): " + "; ".join(f"S{i}:{r.n}/{r.b}" for i, r in sec.iterrows()))
