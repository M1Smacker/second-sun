"""RS-028 (Claude, 14 Nov 2026): how many of our events sit on KNOWN spacecraft events (known_events.csv, built from the HEASARC
TESS sector summaries, downloaded 14 Nov 2026 into data/heasarc_sector_notes_2026-11-14/)? Written before running.
An event 'touches' a known interval if its box [centre - dur/2, centre + dur/2] overlaps [start - 0.1 d, end + 0.1 d].
Counts: (1) all SNR 7+ dev events (g2, g3, both kinds); (2) Codex 011 V0+OAE tier-1 background, real and upside-down; (3) planted
crossings of the 1,098 planets (006 journals; the price of a flag = crossings that would be held). Output rs028/known.json."""
import json, glob
import pandas as pd, numpy as np
K = pd.read_csv("research/stage3/rs028/known_events.csv")
iv = {s: g[["start_tjd", "end_tjd", "kind"]].values for s, g in K.groupby("sector")}


def touch(sec, c, dur_d):
    if sec not in iv:
        return None
    for a, b, k in iv[sec]:
        if c + dur_d / 2 >= a - 0.1 and c - dur_d / 2 <= b + 0.1:
            return k
    return None


out = {}
dev = {"real": [0, 0], "flip": [0, 0]}; bykind = {}
for camp in ("g2", "g3"):
    for kind in ("groups", "groups_sap"):
        for p in glob.glob(f"data/stage3_{camp}/r1dev_{camp}_seen_bcd29c7aabb0/{kind}/*.json"):
            for e in json.load(open(p, encoding="utf-8"))["events"]:
                if (e.get("snr") or 0) < 7:
                    continue
                k = touch(int(e["sector"]), float(e["center"]), float(e.get("dur_h") or 0) / 24)
                dev[e["kind"]][0] += 1; dev[e["kind"]][1] += k is not None
                if k: bykind[k, e["kind"]] = bykind.get((k, e["kind"]), 0) + 1
out["dev_events_snr7"] = {k: dict(total=v[0], touching=v[1]) for k, v in dev.items()}
out["dev_by_kind"] = {f"{a} {b}": v for (a, b), v in sorted(bykind.items())}
B = pd.concat([pd.read_csv(f"D:/second-sun-astra/data/astra/011/background-{c}-V0.csv") for c in ("g2", "g3")])
B["k"] = [touch(int(s), float(c), float(d) / 24) for s, c, d in zip(B.sector, B.center, B.dur_h)]
out["tier1_background_V0_OAE"] = {k: dict(total=int((B.kind == k).sum()), touching=int(((B.kind == k) & B.k.notna()).sum())) for k in ("real", "flip")}
n = h = 0
for j in glob.glob("data/astra/006/planet-*-*-*-g*/results.jsonl"):
    for l in open(j, encoding="utf-8"):
        r = json.loads(l)
        for c, d in r["observed"]:
            n += 1
            h += any(touch(int(s), c, d) for s in r["changed"])
out["planted_crossings"] = dict(total=n, touching=h)
json.dump(out, open("research/stage3/rs028/known.json", "w"), indent=1); print(json.dumps(out, indent=1))
