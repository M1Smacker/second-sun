"""RS-025 Q5 (Claude, 14 Nov 2026): do the real TOI-1338 b transits fare better or worse under the OAE 'dominated' rule (adopted, not
frozen) than under the frozen rule? Same stored dev events, bench re-tier (repeater rule b) and apply_v7 path as T109's bench version
(t109_toi1338_bench.py); 'dominated' recomputed with rs024_options.dominated (O0 must reproduce the stored flag: identity check).
The mask timing variants of Codex 010 cannot change this star: its 3-sigma timing term is at most 0.005 d (data/rs026/offsets.csv) and
it is not among Codex's 112 affected stars. Published planet, so its name and transit times are public. Output: printed table and
data/t109/toi1338_q5.csv."""
import json, math, os, sys
from collections import defaultdict
from pathlib import Path
os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1", NUMBA_NUM_THREADS="2")
ROOT = Path(r"D:\second-sun")
sys.path.insert(0, str(ROOT / "pipeline")); sys.path.insert(0, str(ROOT / "research" / "stage3" / "rs024"))
sys.path.insert(0, str(ROOT / "research" / "stage3" / "006-check"))
import pandas as pd
import stage3_core as C, stage3_report as R
import rs024_options as O

TIC = 260128333
SRC = ROOT / "data" / "stage3_g2" / "r1dev_g2_seen_bcd29c7aabb0"
OBS = {3: (1391.2516, .0073), 6: (1483.9048, .0029), 10: (1579.0423, .0052), 27: (2049.9515, .0034), 34: (2238.2258, .0034),
       37: (2331.0148, .0024), 62: (2989.6356, .0047), 65: (3085.4243, .0044), 68: (3178.2853, .0077),
       89: (3744.4534, .0104), 93: (3836.9195, .0132), 96: (3932.7322, .0183), 98: (4025.5927, .0159)}
T1 = {"1A", "1L", "1B"}
tg = pd.read_csv(C.TARGETS, comment="#"); period = float(tg[tg.tic == TIC].p_bin_d.iloc[0])
best = pd.read_csv(C.BEST)[["tic", "sector", "product"]].rename(columns={"product": "best"})
import p_recount as PR
rows, ident = [], [0, 0]
for sec, (t, s) in sorted(OBS.items()):
    ev = []
    for kind in ("groups", "groups_sap"):
        p = SRC / kind / f"{TIC}_{sec}.json"
        if p.exists():
            ev.extend(json.loads(p.read_text(encoding="utf-8"))["events"])
    if not ev:
        rows.append(dict(sector=sec, status="no stored file")); continue
    ev = PR.bench(ev, period, C)
    df = pd.DataFrame(ev).merge(best, on=["tic", "sector"], how="left")
    df["primary"] = df["product"] == df["best"]; df["c8_best"] = pd.to_numeric(df["c8_best"], errors="coerce")
    df = R.apply_v7(R.merge_sap(df.reset_index(drop=True)))
    df, groups = O.prep(df)
    near = df[(df.kind == "real") & ((df.center - t).abs() <= 3 * s + 0.1) & df.primary & (df.snr >= 7)]
    res = {}
    for opt in ("O0", "OAE"):
        tiers = [O.tier_under(df, groups, i, opt, C) for i in near.index]
        res[opt] = ("tier1" if any(x in T1 for x in tiers) else ("held" if tiers else "not found"), ",".join(sorted(set(tiers))))
    for i in near.index:
        ident[0] += 1; ident[1] += int(O.dominated(df.loc[i], i, groups, "O0") == bool(O.truthy(df.loc[i].get("dominated"))))
    rows.append(dict(sector=sec, frozen=res["O0"][0], frozen_tiers=res["O0"][1], oae=res["OAE"][0], oae_tiers=res["OAE"][1],
                     dominated_frozen=bool(near.dominated.map(O.truthy).any()) if len(near) else None,
                     dominated_oae=any(O.dominated(df.loc[i], i, groups, "OAE") for i in near.index) if len(near) else None))
out = pd.DataFrame(rows); out.to_csv(ROOT / "data" / "t109" / "toi1338_q5.csv", index=False)
print(out.to_string()); print("identity: O0 dominated equals stored flag on", ident[1], "of", ident[0], "primary SNR 7+ transit events")
for c in ("frozen", "oae"):
    print(c, "tier1 transits:", int((out[c] == "tier1").sum()), "of", int(out[c].notna().sum()))
