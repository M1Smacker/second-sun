"""RS-001 V-A4 (closed 3 Nov 2026 after Ahmed's yes to project downloads): how many of our 2,056 stars (union of G1, G2, G3) are on the TESS 2-minute target lists.
Inputs: data/tess_target_lists/all_targets_S107..S111_v1.txt (full 2-minute lists of the sectors already planned in detail) and GI_S108..S121.pri (guest-investigator priority lists; a star on a list has enhanced priority, not a guarantee).
Counts only, no star IDs printed. Run: python -I v_a4_cycle9_lists.py"""
import pathlib, re
import pandas as pd
R = pathlib.Path(r"D:\second-sun")
ours = set()
for g in ("g1", "g2", "g3"):
    ours |= set(pd.read_csv(R / "targets" / f"{g}_targets.csv", comment="#").tic.astype(int))
print(f"our stars: {len(ours)}")
D = R / "data" / "tess_target_lists"
print("sector | 2-minute list size | of our stars on it | share")
for s in range(107, 112):
    ids = set()
    for ln in open(D / f"all_targets_S{s}_v1.txt"):
        if ln.strip() and not ln.startswith("#"):
            ids.add(int(ln.split()[0]))
    k = len(ours & ids); print(f"S{s} | {len(ids):6d} | {k:4d} | {100 * k / len(ours):.1f}%")
print("GI priority lists: sector | stars on list | of our stars on it")
allgi = set()
for s in range(108, 122):
    ids = set()
    for ln in open(D / f"GI_S{s}.pri"):
        p = ln.split()
        if len(p) >= 2 and p[1].isdigit():
            ids.add(int(p[1]))
    allgi |= ids; print(f"S{s} | {len(ids):6d} | {len(ours & ids):4d}")
print(f"our stars on at least one GI priority list S108 to S121: {len(ours & allgi)}")
