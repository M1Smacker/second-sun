"""RS-024 Q2 (Claude, 14 Nov 2026): do strong off-eclipse dips recur at the same BINARY phase in other sectors of the same star
(mono-cbp's test for unmasked secondary eclipses: 3+ events at one binary phase)? Bumps (upside-down events) are the control.
Design stars only (g2, g3, design_seen == 1). Catalogue period p_bin_d. Counts only to rs024/phase.json."""
import json
from collections import Counter
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[3]
LAB = ["5-10", "10-14", "14-20", "20-27.4", "27.4+"]; BINS = [5, 10, 14, 20, 27.4, 1e9]
tg = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
tg = tg[tg["list"].isin(["g2", "g3"]) & (tg.design_seen == 1)].drop_duplicates("tic")
Pb = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
rows = []
for camp in ("g2", "g3"):
    src = ROOT / "data" / f"stage3_{camp}" / f"r1dev_{camp}_seen_bcd29c7aabb0" / "groups"
    for p in src.glob("*.json"):
        tic, sec = map(int, p.stem.split("_"))
        if tic not in Pb: continue
        for e in json.loads(p.read_text(encoding="utf-8"))["events"]:
            if (e.get("snr") or 0) >= 7:
                rows.append(dict(tic=tic, sector=sec, kind=e["kind"], product=e["product"], t=float(e["center"]), snr=float(e["snr"]),
                                 off=not (e.get("c5") or e.get("ecl_overlap")), flagged=bool(e.get("step") or e.get("gap_dump") or e.get("ramp"))))
E = pd.DataFrame(rows).drop_duplicates(["tic", "sector", "kind", "t"])
E["P"] = E.tic.map(Pb); E["bin"] = pd.cut(E.P, BINS, labels=LAB, right=False)
out = {}
for tol in (0.01, 0.02):
    res = {}
    for kind in ("real", "flip"):
        c = Counter()
        for tic, s in E[E.kind == kind].groupby("tic"):
            P = s.P.iloc[0]; t = s.t.values; sec = s.sector.values
            d = np.abs(((t[:, None] - t[None, :]) / P + 0.5) % 1 - 0.5)
            other = sec[:, None] != sec[None, :]
            nmatch = ((d < tol) & other).sum(1)          # events in OTHER sectors at the same binary phase
            for i, r in enumerate(s.itertuples()):
                if not r.off: continue
                key = f"{r.bin} {'clean' if not r.flagged else 'flagged'}"
                c[key + " n"] += 1; c[key + " recurs (1+ other sector)"] += int(nmatch[i] >= 1); c[key + " recurs 2+ (mono-cbp 3 events)"] += int(nmatch[i] >= 2)
        res[kind] = dict(sorted(c.items()))
    out[f"tol {tol}"] = res
(ROOT / "research/stage3/rs024/phase.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
for tol, r in out.items():
    print("==", tol)
    for b in LAB:
        for f in ("clean", "flagged"):
            line = []
            for kind in ("real", "flip"):
                n = r[kind].get(f"{b} {f} n", 0); a = r[kind].get(f"{b} {f} recurs (1+ other sector)", 0); m = r[kind].get(f"{b} {f} recurs 2+ (mono-cbp 3 events)", 0)
                line.append(f"{kind}: {a}/{n} ({(a/n if n else 0):.2f}), 2+ {m}")
            print(b, f, " | ".join(line))
