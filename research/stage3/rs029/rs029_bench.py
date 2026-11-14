"""RS-029 (Claude, 14 Nov 2026, 9:02 pm Kuwait): FIX 95 known-events hold and the combined OAE + known + DS test on the planet bench.
Rules: FIX95-AND-COMBINED-RULE-2026-11-14.md (written before running). Harness: rs024_options.py imported unchanged; only tier_under is
replaced and OPTS set. O.main writes rs024/options.json and data/rs024/options-trials.csv, so both are backed up first and restored after;
this run's numbers are moved to rs029/bench.json and data/rs029/bench-trials.csv."""
import json, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rs024"))
import pandas as pd
import rs024_options as O

K = pd.read_csv(HERE.parent / "rs028" / "known_events.csv")
IV = {int(s): g[["start_tjd", "end_tjd"]].values.astype(float) for s, g in K.groupby("sector")}


def touches(sec, c, dur_d):
    v = IV.get(int(sec))
    if v is None:
        return False
    return bool(((c + dur_d / 2 >= v[:, 0] - 0.1) & (c - dur_d / 2 <= v[:, 1] + 0.1)).any())


def tier_under(df, groups, idx, opt, C):
    row = df.loc[idx]
    d = row.to_dict(); d["dominated"] = O.dominated(row, idx, groups, "OAE")
    fl = str(d.get("flags") or "")
    if opt in ("OAED", "OAEkD"):
        lp, lq = d.get("lift_pre"), d.get("lift_post")
        uneven = any(l is None or l != l or abs(l) > 0.25 for l in (lp, lq))
        d["gap_dump"] = ("gap edge" in fl) or ("momentum dump" in fl and uneven)
    if opt in ("OAEk", "OAEkD") and touches(d["sector"], float(d["center"]), float(d.get("dur_h") or 0) / 24):
        d["gap_dump"] = True
    return C.tier_of(d)


O.tier_under, O.OPTS = tier_under, ("OAE", "OAEk", "OAED", "OAEkD")
if __name__ == "__main__":
    import argparse
    a = argparse.ArgumentParser(); a.add_argument("--limit", type=int); lim = a.parse_args().limit
    tag = f"-prefix{lim}" if lim else ""
    oj = Path(O.__file__).parent / f"options{tag}.json"; oc = O.PR.ROOT / "data" / "rs024" / f"options-trials{tag}.csv"
    bk = [(p, p.with_name(p.name + ".rs029-backup")) for p in (oj, oc) if p.exists()]
    for p, b in bk:
        shutil.copy2(p, b)
    try:
        O.main(lim)
        (HERE / f"bench{tag}.json").write_text(oj.read_text(encoding="utf-8"), encoding="utf-8")
        dd = O.PR.ROOT / "data" / "rs029"; dd.mkdir(exist_ok=True); shutil.copy2(oc, dd / f"bench-trials{tag}.csv")
    finally:
        for p, b in bk:
            shutil.move(b, p)
