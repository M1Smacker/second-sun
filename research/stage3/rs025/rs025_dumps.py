"""RS-025 Q2 (Claude, 14 Nov 2026): where do the dips held only by the momentum-dump rule sit relative to the dump itself?
Dump times are spacecraft-wide, so one SPOC or TESS-SPOC file per sector gives them (QUALITY bit value 32, 'reaction wheel
desaturation'); a second file of the same sector is read as a check. Design stars only (g2, g3, design_seen == 1).
A: untouched light, SNR 7+ events whose only hold is the dump part of gap_dump (no gap edge, no other stored flag), real against
   upside-down: offset from the nearest dump in hours, and whether the box [centre - dur/2, centre + dur/2] contains the dump.
B: planted crossings freed when the dump half is switched off (rs025_gapsplit trial rows): the same numbers.
Counts only to rs025/dumps.json."""
import json, re
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np, pandas as pd
from astropy.io import fits

ROOT = Path(__file__).resolve().parents[3]
tg = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
tg = tg[tg["list"].isin(["g2", "g3"]) & (tg.design_seen == 1)].drop_duplicates("tic")
camp_of = dict(zip(tg.tic.astype(int), tg["list"]))

# 1. dump times per sector
files = defaultdict(list)
for tic, camp in camp_of.items():
    for p in (ROOT / "data" / camp / str(tic)).glob("*lc.fits"):
        n = p.name
        if "qlp" in n:
            continue
        m = re.search(r"-s(\d{4})", n)
        if m:
            files[int(m.group(1))].append(p)
dumps, check = {}, Counter()
for sec, ps in files.items():
    got = []
    for p in ps[:2]:
        try:
            with fits.open(p, memmap=False) as h:
                d = h[1].data
                t = np.asarray(d["TIME"], float); q = np.asarray(d["QUALITY"], int)
                got.append(np.sort(t[((q & 32) > 0) & np.isfinite(t)]))
        except Exception:
            check["file read failed"] += 1
    if not got:
        continue
    # merge cadence runs into dump events (a dump spans a few cadences)
    t = got[0]
    ev = [t[0]] if t.size else []
    for a, b in zip(t[:-1], t[1:]):
        if b - a > 0.05:
            ev.append(b)
    dumps[sec] = np.array(ev)
    if len(got) == 2 and got[1].size and t.size:
        check["sectors with two files"] += 1
        check["... median |difference| of dump starts under 0.01 d"] += int(np.median([np.min(np.abs(got[1] - x)) for x in ev]) < 0.01)
check["sectors with dump times"] = len(dumps)
check["median dumps per sector"] = float(np.median([len(v) for v in dumps.values()])) if dumps else 0


def where(sec, c, dur_h):
    v = dumps.get(sec)
    if v is None or not v.size:
        return None
    k = np.argmin(np.abs(v - c)); off = (c - v[k]) * 24
    return off, abs(c - v[k]) * 24 <= dur_h / 2


# 2A. untouched light
A = defaultdict(list)
other = ("step", "ramp", "dominated", "c5", "ecl_overlap", "repeater", "flipmatch")
for camp in ("g2", "g3"):
    for p in (ROOT / "data" / f"stage3_{camp}" / f"r1dev_{camp}_seen_bcd29c7aabb0" / "groups").glob("*.json"):
        tic, sec = map(int, p.stem.split("_"))
        if tic not in camp_of:
            continue
        for e in json.loads(p.read_text(encoding="utf-8"))["events"]:
            fl = str(e.get("flags") or "")
            if (e.get("snr") or 0) >= 7 and "momentum dump" in fl and "gap edge" not in fl and not any(e.get(o) for o in other):
                w = where(sec, float(e["center"]), float(e.get("dur_h") or 0))
                if w:
                    A[e["kind"]].append(w)


def summ(lst):
    if not lst:
        return {}
    off = np.array([x[0] for x in lst]); inside = np.array([x[1] for x in lst])
    return dict(n=len(lst), box_contains_dump=int(inside.sum()), share_inside=round(float(inside.mean()), 3),
                offset_h_hist={f"{a} to {b} h": int(((off >= a) & (off < b)).sum()) for a, b in ((-6, -3), (-3, -1), (-1, 1), (1, 3), (3, 6), (6, 12))},
                median_abs_offset_h=round(float(np.median(np.abs(off))), 2))


out = dict(check=dict(check), A_untouched={k: summ(v) for k, v in A.items()})
# 2B. planted crossings freed by switching the dump half off
tr = pd.read_csv(ROOT / "data" / "rs024" / "rs025-gap-split-trials.csv")
gain = tr[(tr.edge_only_real_new == True) & (tr.base_real_new == False)]
B = []
for r in gain.itertuples():
    for j in (ROOT / "data" / "astra" / "006").glob(f"planet-*-*-*-{r.campaign}/results.jsonl"):
        for line in j.read_text(encoding="utf-8").splitlines():
            x = json.loads(line)
            if x["trial"] == r.trial and x["star"] == r.star:
                best = None
                for c, d in x["observed"]:
                    for sec in x["changed"]:
                        w = where(int(sec), float(c), float(d) * 24)
                        if w and (best is None or abs(w[0]) < abs(best[0])):
                            best = w
                if best:
                    B.append(best)
out["B_planted_freed"] = summ(B)
out["B_note"] = "observed crossing nearest a dump, per freed trial; duration in the journal is in days"
(ROOT / "research/stage3/rs025/dumps.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
