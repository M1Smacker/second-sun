"""T35 part 1 (report only): untouched design-light tier-1 background under B by box duration, arm and binary-period bin. Counts to box_split.json."""
import json, math, os, sys, importlib
from collections import defaultdict, Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rs031"))
import numpy as np, pandas as pd
import rs031_dsp_bench as D
O, PR = D.O, D.O.PR
ROOT = PR.ROOT
import stage3_core as C, stage3_report as R
res = {}
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
    cnt = Counter(); allbox = Counter()
    for idx in allb.index[allb.primary & (allb.snr >= 7)]:
        r = allb.loc[idx]; box = float(r.dur_h or 0)
        b = int(np.digitize(Pb.get(int(r.tic), np.nan), [10, 14, 20, 27.4]))
        allbox[r.kind, box] += 1
        if D.tier_under(allb, ag, idx, "B", C) in PR.T1:
            cnt[r.kind, box, b] += 1
    boxes = sorted({k[1] for k in cnt} | {k[1] for k in allbox})
    res[camp] = {f"{bx:g} h": {"tier1_real": sum(v for (k, x, b), v in cnt.items() if k == "real" and x == bx),
                               "tier1_flip": sum(v for (k, x, b), v in cnt.items() if k == "flip" and x == bx),
                               "tier1_by_bin_real_flip": [[cnt["real", bx, b], cnt["flip", bx, b]] for b in range(5)],
                               "snr7_primary_real_flip": [allbox["real", bx], allbox["flip", bx]]} for bx in boxes}
    print(camp, json.dumps(res[camp]), flush=True)
(HERE / "box_split.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
