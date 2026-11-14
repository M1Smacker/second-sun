"""T109: TOI-1338 b (known CBP, design-seen g2 star) through Petrova 1.0.0 and through the T156 bench
(binary-locked repeater, rule b; FIX 91 only touches the upside-down arm, so it cannot change a real event's tier).
Re-tiers the STORED dev events exactly as Codex's 005_replay.py 'repeater' variant does, then the frozen
apply_v7(merge_sap). Published times: Wang & Liu 2024 (arXiv:2404.18415) Table 1 (BTJD) and Table 3 forecast.
Read-only use of pipeline code. Output: data/t109/ only. Run: .venv python -I -B this.py"""
import json, math, os, sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1", NUMBA_NUM_THREADS="2")
ROOT = Path(r"D:\second-sun")
sys.path.insert(0, str(ROOT / "pipeline"))
import pandas as pd
import stage3_core as C
import stage3_report as R

SRC = ROOT / "data" / "stage3_g2" / "r1dev_g2_seen_bcd29c7aabb0"
OUT = ROOT / "data" / "t109"; OUT.mkdir(exist_ok=True)
TIC = 260128333
OBS = {3: (1391.2516, .0073), 6: (1483.9048, .0029), 10: (1579.0423, .0052), 27: (2049.9515, .0034),
       34: (2238.2258, .0034), 37: (2331.0148, .0024), 62: (2989.6356, .0047), 65: (3085.4243, .0044),
       68: (3178.2853, .0077)}
PRED = {89: (3744.4534, .0104), 93: (3836.9195, .0132), 96: (3932.7322, .0183), 98: (4025.5927, .0159)}
TIERS = {"1A", "1L", "1B"}


def binary_members(events, period):  # copy of 005_replay.binary_members (rule b)
    if not math.isfinite(period) or period <= 0:
        return set(range(len(events))) if len(events) >= 3 else set()
    def locked(a, b):
        s = abs(a["center"] - b["center"]); c = round(s / period)
        return c >= 1 and abs(s - c * period) <= 1 / 24
    m = set()
    for tr in combinations(range(len(events)), 3):
        if all(locked(events[a], events[b]) for a, b in combinations(tr, 2)):
            m.update(tr)
    return m


tg = pd.read_csv(C.TARGETS, comment="#")
row = tg[tg.tic == TIC]
period = float(row.p_bin_d.iloc[0]) if "p_bin_d" in tg and len(row) else math.nan
print("binary period used", period)
best = pd.read_csv(C.BEST)[["tic", "sector", "product"]].rename(columns={"product": "best"})

groups = defaultdict(list); missing = []
for sec in sorted({**OBS, **PRED}):
    found = False
    for kind in ("groups", "groups_sap"):
        p = SRC / kind / f"{TIC}_{sec}.json"
        if p.exists():
            found = True; groups[sec].extend(json.loads(p.read_text(encoding="utf-8"))["events"])
    if not found:
        missing.append(sec)


def retier(events, bench):
    parts = defaultdict(list)
    for r in events:
        parts[r["kind"], r["product"]].append(r)
    out = {}
    for (kind, product), g in parts.items():
        mem = binary_members(g, period) if bench else None
        for i, r in enumerate(g):
            u = dict(r)
            if bench:
                u["repeater"] = i in mem
            ti = dict(u); ti.pop("pdc_snr", None)
            u["tier"] = C.tier_of(ti)
            out[id(r)] = u
    return [out[id(r)] for r in events]


def final(events):
    df = pd.DataFrame(events).merge(best, on=["tic", "sector"], how="left")
    df["primary"] = df["product"] == df["best"]
    if "c8_best" in df:
        df["c8_best"] = pd.to_numeric(df["c8_best"], errors="coerce")
    return R.apply_v7(R.merge_sap(df.reset_index(drop=True)))


rows = []
for label, bench in (("petrova_1_0_0", False), ("bench_repeater", True)):
    for sec, (t, s) in sorted({**OBS, **PRED}.items()):
        if sec not in groups:
            rows.append(dict(version=label, sector=sec, src="obs" if sec in OBS else "forecast", status="no stored file")); continue
        df = final(retier(groups[sec], bench))
        w = 3 * s + 0.1
        near = df[(df.kind == "real") & ((df.center - t).abs() <= w)]
        prim = near[near.primary]
        t1 = prim[prim.tier.isin(TIERS) & (prim.snr >= 7)]
        rows.append(dict(version=label, sector=sec, src="obs" if sec in OBS else "forecast",
                         status="tier1" if len(t1) else ("found, below tier 1" if len(prim) else ("other product only" if len(near) else "not found")),
                         best_tier=",".join(sorted(set(prim.tier))) if len(prim) else "",
                         snr=float(prim.snr.max()) if len(prim) else None,
                         repeater=bool(prim.repeater.any()) if len(prim) and "repeater" in prim else None,
                         n_events_sector=int((df.kind == "real").sum())))
res = pd.DataFrame(rows)
res.to_csv(OUT / "toi1338_bench.csv", index=False)
print(res.to_string())
for v, g in res.groupby("version"):
    o = g[g.src == "obs"]
    print(v, "observed transits:", len(o), "tier1:", int((o.status == "tier1").sum()),
          "| forecast:", int((g.src == "forecast").sum()), "tier1:", int(((g.src == "forecast") & (g.status == "tier1")).sum()))
print("missing sectors", missing)

# Which flags held each primary transit event below tier 1 (bench version)
FL = ["gap_dump", "burst", "common", "flipmatch", "c5", "ecl_overlap", "repeater", "orbit_lock", "step", "ramp", "dominated", "too_deep", "flare", "p1_veto"]
why = []
for sec, (t, s) in sorted({**OBS, **PRED}.items()):
    if sec not in groups:
        continue
    df = final(retier(groups[sec], True)); w = 3 * s + 0.1
    for _, e in df[(df.kind == "real") & ((df.center - t).abs() <= w)].iterrows():
        fired = [f for f in FL if f in e and isinstance(e[f], (bool,)) and e[f] or (f in e and e[f] is True)]
        why.append(dict(sector=sec, product=e["product"], primary=bool(e["primary"]), tier=e["tier"], snr=round(float(e["snr"]), 1),
                        dur_h=e["dur_h"], off_h=round(24 * (e["center"] - t), 1), fired=" ".join(fired), seen_by=e.get("seen_by"),
                        c8_best=e.get("c8_best"), pdc_snr=e.get("pdc_snr")))
W = pd.DataFrame(why); W.to_csv(OUT / "toi1338_flags.csv", index=False); print(W.to_string())
