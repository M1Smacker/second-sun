"""Distances (days) from each event to the nearest gap edge and nearest momentum dump, real and flipped."""
import glob, numpy as np
from detect_v2 import load, eclipse_mask, find_events, systematics
P, D1, D2, SEC = 14.6084, 4.7, 6.1, 0.454
PUB = {6: 1483.9048, 10: 1579.0423, 27: 2049.9515, 30: 2142.3991, 34: 2238.2258, 65: 3085.4243, 68: 3178.2853, 98: 4025.5927}
path = lambda s: glob.glob(rf"D:/second-sun/data/*/lk/mastDownload/TESS/*-s{s:04d}-0000000260128333-*-s/*_lc.fits")[0]
for s, tp in PUB.items():
    t, f, _ = load(path(s)); keep, _ = eclipse_mask(t, f, P, D1, D2, SEC)
    edges, dumps = systematics(path(s))
    med_dump_gap = np.median(np.diff(np.sort(dumps))) if dumps.size > 1 else None
    for kind, ff in (("real", f[keep]), ("flip", 2 - f[keep])):
        for e in find_events(t[keep], ff):
            c = e["center"]; tag = "PLANET" if kind == "real" and abs(c - tp) < 0.3 else kind
            print(s, tag, round(c, 2), "dur", e["dur_h"], "snr", round(e["snr"], 1),
                  "gap", round(float(np.min(np.abs(edges - c))), 2), "dump", round(float(np.min(np.abs(dumps - c))), 2) if dumps.size else None,
                  "dump spacing", round(med_dump_gap, 2) if med_dump_gap else None)
