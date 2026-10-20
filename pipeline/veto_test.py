"""Overnight task 8: does the systematics veto cut false alarms without losing TOI-1338 b?
Same sectors and ground truth as accept_v2.py. For each sector: real-flux events and flipped-flux events
(false alarms), before and after veto. Flipped events are only flagged (the flipped-match rule would be circular for them)."""
import glob, json, pathlib, numpy as np
from detect_v2 import load, eclipse_mask, find_events, systematics, veto

P, D1, D2, SEC = 14.6084, 4.7, 6.1, 0.454
PUB = {6: 1483.9048, 10: 1579.0423, 27: 2049.9515, 30: 2142.3991, 34: 2238.2258,
       37: 2331.0148, 62: 2989.6356, 65: 3085.4243, 68: 3178.2853, 98: 4025.5927}
path = lambda s: (glob.glob(rf"D:/second-sun/data/*/lk/mastDownload/TESS/*-s{s:04d}-0000000260128333-*-s/*_lc.fits") or [None])[0]
rows = []
for s, tp in PUB.items():
    p = path(s)
    t, f, _ = load(p)
    keep, _ = eclipse_mask(t, f, P, D1, D2, SEC)
    real = find_events(t[keep], f[keep])
    flip = find_events(t[keep], 2 - f[keep])
    edges, dumps = systematics(p)
    real_k, real_r = veto(real, edges, dumps, flip)
    flip_k, flip_r = veto(flip, edges, dumps, [])
    planet = lambda ev: any(abs(e["center"] - tp) < 0.3 for e in ev)
    r = dict(sector=s, planet_before=planet(real), planet_after=planet(real_k),
             other_real_before=sum(abs(e["center"] - tp) >= 0.3 for e in real),
             other_real_after=sum(abs(e["center"] - tp) >= 0.3 for e in real_k),
             flipped=len(flip), flipped_flagged=sum(bool(e["flags"]) for e in flip_k),
             rejected=[(round(e["center"], 2), e["veto"]) for e in real_r], flags_real=[(round(e["center"], 2), e["flags"]) for e in real_k if e["flags"]], flags_flipped=[(round(e["center"], 2), e["flags"]) for e in flip_k if e["flags"]])
    rows.append(r); print(r, flush=True)
tot = {k: sum(r[k] for r in rows) for k in ("planet_before", "planet_after", "other_real_before", "other_real_after", "flipped", "flipped_flagged")}
print("TOTALS", tot)
pathlib.Path(__file__).with_name("veto_results.json").write_text(json.dumps(dict(rows=rows, totals=tot), indent=1, default=float))
