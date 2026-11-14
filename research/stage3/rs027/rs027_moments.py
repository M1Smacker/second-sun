"""FIX 95 pricing (Claude, 14 Nov 2026). Written before running.
Question: how many tier-1 background events, and how many planted planet crossings, sit at a 'sector-wide moment': a time when events
(SNR 7+, any tier, either kind, best or other product) on at least K other stars in the SAME SECTOR, ANY camera, fall within 0.1 d?
The frozen common-moment flag asks for 3 other stars on the SAME camera; a spacecraft event (pointing shift, reset) touches every camera.
K = 3 (the frozen BURST_MIN, not tuned); also reported for K = 5 and 8 as a sensitivity line, not a choice.
Background: Codex 011 V0+OAE tier-1 rows (both campaigns). Planets: every observed crossing of the 1,098 planets (006 journals);
a crossing 'sits at a moment' if a moment lies within half its duration + 0.1 d. Pool of moments: untouched dev events (g2, g3).
Counts only; output rs027/moments.json."""
import json, glob
from collections import defaultdict
import numpy as np, pandas as pd

pool = defaultdict(list)  # sector -> (time, tic)
for camp in ("g2", "g3"):
    for kind in ("groups", "groups_sap"):
        for p in glob.glob(f"data/stage3_{camp}/r1dev_{camp}_seen_bcd29c7aabb0/{kind}/*.json"):
            for e in json.load(open(p, encoding="utf-8"))["events"]:
                if (e.get("snr") or 0) >= 7:
                    pool[int(e["sector"])].append((float(e["center"]), int(e["tic"])))
pool = {s: (np.array([x[0] for x in v]), np.array([x[1] for x in v])) for s, v in pool.items()}


def others(sec, t, tic, w=0.1):
    if sec not in pool:
        return 0
    c, ti = pool[sec]
    return len(set(ti[np.abs(c - t) < w]) - {tic})


out = {}
B = pd.concat([pd.read_csv(f"D:/second-sun-astra/data/astra/011/background-{c}-V0.csv") for c in ("g2", "g3")])
B["n_other"] = [others(int(s), float(t), int(i)) for s, t, i in zip(B.sector, B.center, B.tic)]
for K in (3, 5, 8):
    out[f"background_K{K}"] = {k: dict(total=int((B.kind == k).sum()), at_moment=int(((B.kind == k) & (B.n_other >= K)).sum())) for k in ("real", "flip")}
n = hit = {3: 0, 5: 0, 8: 0}
n, hit = 0, {3: 0, 5: 0, 8: 0}
for j in glob.glob("data/astra/006/planet-*-*-*-g*/results.jsonl"):
    for l in open(j, encoding="utf-8"):
        r = json.loads(l)
        for c, d in r["observed"]:
            n += 1
            secs = [int(s) for s in r["changed"]]
            best = 0
            for s in secs:
                if s in pool:
                    cc, ti = pool[s]
                    best = max(best, len(set(ti[np.abs(cc - c) < d / 2 + 0.1]) - {r["star"]}))
            for K in hit:
                hit[K] += best >= K
out["planet_crossings"] = dict(total=n, **{f"at_moment_K{K}": v for K, v in hit.items()})
json.dump(out, open("research/stage3/rs027/moments.json", "w"), indent=1)
print(json.dumps(out, indent=1))
