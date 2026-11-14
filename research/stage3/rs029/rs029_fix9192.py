"""RS-029 part 2 (Claude, 14 Nov 2026): FIX 91 (opposite-sign coincidence flag on both arms, or none) and FIX 92 (second product judged
only when it could see the event). Rules: FIX91-FIX92-RULE-2026-11-14.md, written before running. Harness rs024_options.py imported;
tier_under and prep replaced; outputs moved to rs029/fix9192.json and data/rs029/fix9192-trials.csv (rs024 files backed up, restored)."""
import json, math, shutil, sys
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rs024"))
import numpy as np
import rs024_options as O

FLIP_D, E_MIN = 0.3, 5.0
RATIO = defaultdict(list)          # (tic, sector, product A) -> [snr_B / snr_A for every other product B]
for camp in ("g2", "g3"):
    for kind in ("groups", "groups_sap"):
        for p in (O.PR.ROOT / "data" / f"stage3_{camp}" / f"r1dev_{camp}_seen_bcd29c7aabb0" / kind).glob("*.json"):
            for r in json.loads(p.read_text(encoding="utf-8")).get("inj") or []:
                a, b = r.get("snr_A"), r.get("snr_B")
                if a and b is not None and a == a and b == b and a > 0:
                    RATIO[int(r["tic"]), int(r["sector"]), r["A"]].append(float(b) / float(a))
RATIO = {k: max(v) for k, v in RATIO.items()}
_prep = O.prep


def prep(df):
    df, _ = _prep(df)
    groups = {k: (g.index.values, g.kind.values, g.snr.fillna(0).values.astype(float), g.center.values.astype(float), g._expl.values)
              for k, g in df.groupby(["tic", "sector", "product"])}
    return df, groups


def tier_under(df, groups, idx, opt, C):
    row = df.loc[idx]
    d = row.to_dict(); d["dominated"] = O.dominated(row, idx, groups, "OAE")
    if opt == "OAE91d":
        d["flipmatch"] = False
    elif opt == "OAE91m" and row.kind == "flip":
        ix, kind, snr, t, ex = groups[(row.tic, row.sector, row["product"])]
        d["flipmatch"] = bool(((kind == "real") & (np.abs(t - float(row.center)) < FLIP_D)).any())
    elif opt == "OAE92" and (d.get("c8_n") or 0) > 0:
        prod = str(row["product"]).replace("-SAP", "")
        r = RATIO.get((int(row.tic), int(row.sector), prod))
        if r is not None and float(row.snr) * r < E_MIN:
            d["c8_n"] = 0; d["c8_best"] = None
    return C.tier_of(d)


O.prep, O.tier_under, O.OPTS = prep, tier_under, ("OAE", "OAE91m", "OAE91d", "OAE92")
if __name__ == "__main__":
    # own output paths (so it can run beside rs029_bench.py, which uses the rs024 file names): the json goes next to this script via
    # the module's __file__, the trials csv is redirected by a to_csv wrapper in this process only
    import argparse, pandas as pd
    a = argparse.ArgumentParser(); a.add_argument("--limit", type=int); lim = a.parse_args().limit
    tag = f"-prefix{lim}" if lim else ""
    print("star-sector-product ratios:", len(RATIO), flush=True)
    dd = O.PR.ROOT / "data" / "rs029"; dd.mkdir(exist_ok=True)
    O.__file__ = str(HERE / "rs024_options_fix9192_shadow.py")
    _tc = pd.DataFrame.to_csv
    def to_csv(self, path=None, *a, **k):
        if path is not None and "options-trials" in str(path):
            path = dd / f"fix9192-trials{tag}.csv"
        return _tc(self, path, *a, **k)
    pd.DataFrame.to_csv = to_csv
    O.main(lim)
    oj = HERE / f"options{tag}.json"
    oj.replace(HERE / f"fix9192{tag}.json")
