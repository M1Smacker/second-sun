"""Why does v2 miss some published TOI-1338 b transits? Box SNR at the published time, best duration,
versus the strongest flipped-flux (false-alarm) peak in the same sector."""
import json, numpy as np
from detect_v2 import load, eclipse_mask, detrend, bin10, box_scores, DURS_H
import glob
P, D1, D2, SEC = 14.6084, 4.7, 6.1, 0.454
PUB = {6: 1483.9048, 10: 1579.0423, 27: 2049.9515, 34: 2238.2258, 37: 2331.0148, 65: 3085.4243, 68: 3178.2853, 98: 4025.5927}
path = lambda s: (glob.glob(rf"D:/second-sun/data/*/lk/mastDownload/TESS/*-s{s:04d}-0000000260128333-*-s/*_lc.fits") or [None])[0]
rows = []
for s, tp in PUB.items():
    p = path(s)
    if not p: continue
    t, f, _ = load(p)
    keep, _ = eclipse_mask(t, f, P, D1, D2, SEC)
    tt, ff = detrend(t[keep], f[keep])
    bt, bf = bin10(tt, ff)
    best, fa = (0, None), 0
    for d in DURS_H:
        c, snr, _ = box_scores(bt, bf, d)
        near = np.abs(c - tp) < 0.3
        if np.any(np.isfinite(snr[near])):
            v = np.nanmax(snr[near]); best = max(best, (v, d), key=lambda x: x[0])
        c2, snr2, _ = box_scores(bt, 2 - bf, d)
        fa = max(fa, np.nanmax(snr2))
    sig1h = 1.4826*np.nanmedian(np.abs(bf-np.nanmedian(bf)))/np.sqrt(6)
    rows.append(dict(sector=s, snr_at_pub=round(best[0], 1), dur=best[1], max_flipped_snr=round(fa, 1), white_1h_ppm=round(sig1h*1e6)))
    print(rows[-1], flush=True)
json.dump(rows, open("diag_v2_results.json", "w"), indent=1)
