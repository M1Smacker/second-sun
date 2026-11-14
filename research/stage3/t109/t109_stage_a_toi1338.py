"""T109 stage A: what did the stored Petrova 1.0.0 dev run (g2, design-seen) see at the
published TOI-1338 b transits? Reads only stored outputs; writes data\t109\. Run -I.
Transit mid-times and durations: Wang & Liu 2024 (arXiv:2404.18415) Table 1, BJD-2457000 (= BTJD)."""
import json
from pathlib import Path

D = Path(r"D:\second-sun\data\stage3_g2\r1dev_g2_seen_bcd29c7aabb0")
OUT = Path(r"D:\second-sun\data\t109"); OUT.mkdir(exist_ok=True)
TIC = 260128333
TRANSITS = [(3, 1391.2516, 8.5584), (6, 1483.9048, 5.9564), (10, 1579.0423, 11.5838),
            (27, 2049.9515, 7.1834), (34, 2238.2258, 9.5885), (37, 2331.0148, 5.8707),
            (62, 2989.6356, 7.6709), (65, 3085.4243, 10.2463), (68, 3178.2853, 6.2203)]
rows = []
for sector, mid, dur_h in TRANSITS:
    for kind in ("groups", "groups_sap"):
        f = D / kind / f"{TIC}_{sector}.json"
        if not f.exists():
            rows.append(dict(sector=sector, kind=kind, file="missing")); continue
        g = json.loads(f.read_text(encoding="utf-8"))
        meta = [{k: m.get(k) for k in ("product", "status", "file") if k in m} for m in g.get("meta", [])]
        near = []
        for e in g.get("events", []):
            t = e.get("t") or e.get("t0") or e.get("time") or e.get("center")
            if t is None:
                continue
            if abs(float(t) - mid) <= max(1.0, dur_h / 24):
                near.append(e)
        rows.append(dict(sector=sector, kind=kind, file="ok", n_events=len(g.get("events", [])),
                         meta=meta, near=near, keys=sorted(g.keys()),
                         event_keys=sorted(g["events"][0].keys()) if g.get("events") else []))
(OUT / "stage_a_toi1338.json").write_text(json.dumps(rows, indent=1, default=str), encoding="utf-8")
for r in rows:
    if r["file"] == "missing":
        print(r["sector"], r["kind"], "MISSING"); continue
    print(r["sector"], r["kind"], "events", r["n_events"], "near", len(r["near"]),
          [m.get("status") for m in r["meta"]], [m.get("product") for m in r["meta"]])
    for e in r["near"]:
        print("    ", {k: e[k] for k in list(e)[:14]})
print("keys", rows[1].get("keys"), rows[1].get("event_keys"))
