"""Rows version of rs032_dumpmap_key.py (same method, also writes every tier-1 event with its dump bin to data/rs032/dumpmap-rows.csv) for the root-cause look at the pre-dump excess (RS-033 follow-up).
gap_dump OFF (gap-edge half and known events kept); signed time from box centre to the nearest dump (negative = before the dump), bins as
brief 014. Counts only, per campaign and arm, to dumpmap_key.json. Written before Codex reports; not shown to Codex."""
import json, math, os, sys, importlib
from collections import defaultdict, Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rs031"))
import numpy as np, pandas as pd
import rs031_dsp_bench as D
O, K, PR = D.O, D.K, D.O.PR
ROOT = PR.ROOT
import stage3_core as C, stage3_report as R
EDGES_H = [-12, -6, -3, -1, 0, 1, 3, 6, 12]
LAB = ["-12..-6", "-6..-3", "-3..-1", "-1..0", "contains", "0..1", "1..3", "3..6", "6..12", "far"]


def tier_nodump(df, groups, idx):
    row = df.loc[idx]; d = row.to_dict(); d["dominated"] = O.dominated(row, idx, groups, "OAE")
    d["gap_dump"] = "gap edge" in str(d.get("flags") or "")
    if K.touches(d["sector"], float(d["center"]), float(d.get("dur_h") or 0) / 24):
        d["gap_dump"] = True
    return C.tier_of(d)


def where(sec, c, dd):
    v = D.DUMPS.get(int(sec))
    if v is None or not v.size:
        return None
    if np.any(np.abs(v - c) <= dd / 2):
        return "contains"
    dt = (c - v[np.argmin(np.abs(v - c))]) * 24            # hours; negative = box before the dump
    if abs(dt) > 12:
        return "far"
    if dt < 0:
        return LAB[int(np.digitize(dt, [-6, -3, -1]))]
    return LAB[5 + int(np.digitize(dt, [1, 3, 6]))]


res = {}; rows = []
for camp in ("g2", "g3"):
    os.environ["SS_SET"] = camp
    import dataset as DSm
    importlib.reload(DSm); importlib.reload(C)
    best = pd.read_csv(C.BEST)[["tic", "sector", "product"]].rename(columns={"product": "best"})
    tg = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
    tg = tg[(tg["list"] == camp) & (tg.design_seen == 1)].drop_duplicates("tic")
    Pb = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
    src = ROOT / "data" / f"stage3_{camp}" / f"r1dev_{camp}_seen_bcd29c7aabb0"
    base = defaultdict(list)
    for kind in ("groups", "groups_sap"):
        for p in (src / kind).glob("*.json"):
            tic, sec = map(int, p.stem.split("_"))
            if tic in Pb:
                base[tic, sec].extend(json.loads(p.read_text(encoding="utf-8"))["events"])
    base = {k: PR.bench(v, Pb.get(k[0], math.nan), C) for k, v in base.items()}
    df = pd.DataFrame([e for v in base.values() for e in v]).merge(best, on=["tic", "sector"], how="left")
    df["primary"] = df["product"] == df["best"]
    df["c8_best"] = pd.to_numeric(df["c8_best"], errors="coerce")
    allb, ag = O.prep(R.apply_v7(R.merge_sap(df.reset_index(drop=True))))
    cnt = Counter(); allc = Counter(); t1 = []
    for idx in allb.index[allb.primary & (allb.snr >= 7)]:
        r = allb.loc[idx]; w = where(r.sector, float(r.center), float(r.dur_h or 0) / 24) or "no dump times"
        allc[r.kind, w] += 1
        if tier_nodump(allb, ag, idx) in PR.T1:
            t1.append(idx)
            cnt[r.kind, w] += 1
    res[camp] = {w: {"tier1_real": cnt["real", w], "tier1_flip": cnt["flip", w], "snr7_real": allc["real", w], "snr7_flip": allc["flip", w]}
                 for w in LAB + ["no dump times"]}
    rows += [dict(campaign=camp, kind=allb.loc[i].kind, tic=int(allb.loc[i].tic), sector=int(allb.loc[i].sector), product=allb.loc[i]["product"], dur_h=float(allb.loc[i].dur_h or 0), where=where(allb.loc[i].sector, float(allb.loc[i].center), float(allb.loc[i].dur_h or 0) / 24), flags=str(allb.loc[i].get("flags") or "")[:60]) for i in t1]
    print(camp, json.dumps({w: [v["tier1_real"], v["tier1_flip"]] for w, v in res[camp].items()}), flush=True)
pd.DataFrame(rows).to_csv(ROOT / "data" / "rs032" / "dumpmap-rows.csv", index=False)
