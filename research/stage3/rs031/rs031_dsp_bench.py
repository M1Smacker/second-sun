"""RS-031 bench (Claude, 14 Nov 2026): B (repeater b + FIX 91 + OAE + K), B+DS, B+DSp (DS relief only after the dump). Rule in
MOMENTUM-DUMPS-RESEARCH-2026-11-14.md, written before running. Harness rs024_options.py imported; own output files (json next to this
script, trials csv to data/rs031)."""
import json, re, sys
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rs024")); sys.path.insert(0, str(HERE.parent / "rs029"))
import numpy as np, pandas as pd
from astropy.io import fits
import rs024_options as O
import rs029_bench as K                      # known-events touches() and its patched tier_under (we replace it below)

ROOT = O.PR.ROOT
tg = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
tg = tg[tg["list"].isin(["g2", "g3"]) & (tg.design_seen == 1)].drop_duplicates("tic")
files = defaultdict(list)
for tic, camp in zip(tg.tic.astype(int), tg["list"]):
    for p in (ROOT / "data" / camp / str(tic)).glob("*lc.fits"):
        if "qlp" in p.name:
            continue
        m = re.search(r"-s(\d{4})", p.name)
        if m and len(files[int(m.group(1))]) < 1:
            files[int(m.group(1))].append(p)
DUMPS = {}
for sec, ps in files.items():
    try:
        with fits.open(ps[0], memmap=False) as h:
            d = h[1].data; t = np.asarray(d["TIME"], float); q = np.asarray(d["QUALITY"], int)
        t = np.sort(t[((q & 32) > 0) & np.isfinite(t)])
        ev = [t[0]] if t.size else []
        for a, b in zip(t[:-1], t[1:]):
            if b - a > 0.05:
                ev.append(b)
        DUMPS[sec] = np.array(ev)
    except Exception as e:
        print("dump read failed", sec, type(e).__name__)
print("sectors with dump times:", len(DUMPS), flush=True)
DUMP_D, PRE_DUMP_D = 0.25, 0.5


def after_only(sec, c, dur_d):
    v = DUMPS.get(int(sec))
    if v is None or not v.size:
        return False                              # unknown dumps: no relief
    w = v[((v - c) > -DUMP_D) & ((v - c) < PRE_DUMP_D)]
    return bool(w.size) and bool(np.all(w <= c - dur_d / 2))


def tier_under(df, groups, idx, opt, C):
    row = df.loc[idx]
    d = row.to_dict(); d["dominated"] = O.dominated(row, idx, groups, "OAE")
    fl = str(d.get("flags") or "")
    c, dd = float(d["center"]), float(d.get("dur_h") or 0) / 24
    if opt in ("BDS", "BDSp"):
        lp, lq = d.get("lift_pre"), d.get("lift_post")
        uneven = any(l is None or l != l or abs(l) > 0.25 for l in (lp, lq))
        hold = uneven or (opt == "BDSp" and not after_only(d["sector"], c, dd))
        d["gap_dump"] = ("gap edge" in fl) or ("momentum dump" in fl and hold)
    if K.touches(d["sector"], c, dd):
        d["gap_dump"] = True
    return C.tier_of(d)


O.tier_under, O.OPTS = tier_under, ("B", "BDS", "BDSp")
if __name__ == "__main__":
    import argparse
    a = argparse.ArgumentParser(); a.add_argument("--limit", type=int); lim = a.parse_args().limit
    tag = f"-prefix{lim}" if lim else ""
    dd_ = ROOT / "data" / "rs031"; dd_.mkdir(exist_ok=True)
    O.__file__ = str(HERE / "rs024_options_shadow.py")
    _tc = pd.DataFrame.to_csv
    def to_csv(self, path=None, *a, **k):
        if path is not None and "options-trials" in str(path):
            path = dd_ / f"dsp-trials{tag}.csv"
        return _tc(self, path, *a, **k)
    pd.DataFrame.to_csv = to_csv
    O.main(lim)
    (HERE / f"options{tag}.json").replace(HERE / f"dsp{tag}.json")
