"""Acceptance test for detect_v2 on TOI-1338 (TIC 260128333), same ground truth as burn 1.

1. Recovery: published TOI-1338 b mid-times (Wang & Liu 2024, arXiv:2404.18415, Table 1; S30 = their
   predicted time) in every cached SPOC 2-min sector. Match = event centre within 0.3 d.
2. False alarms: run the search on the flipped light curve (2 - flux) of every sector. A real transit
   flips into a bump, so any event found there is noise or systematics: an empirical false-alarm count.
3. Injection: S98 out-of-eclipse data with the real event removed; batman single transits of
   2-8 R_earth (6.4 h, b = 0.4) at 8 fixed times; recovered = event within 0.25 d. SNR recorded.
Uses only files already on D: (no downloads).
"""
import glob, json, pathlib, numpy as np, batman
from detect_v2 import load, eclipse_mask, find_events

P, D1, D2, SEC = 14.6084, 4.7, 6.1, 0.454  # binary, measured in wave 3 (claim P8)
PUB = {6: 1483.9048, 10: 1579.0423, 27: 2049.9515, 30: 2142.3991, 34: 2238.2258,
       37: 2331.0148, 62: 2989.6356, 65: 3085.4243, 68: 3178.2853, 98: 4025.5927}
OUT = pathlib.Path(__file__).with_name("accept_v2_results.json")


def path(s):
    hits = glob.glob(rf"D:\second-sun\data\*\lk\mastDownload\TESS\*-s{s:04d}-0000000260128333-*-s\*_lc.fits")
    return hits[0] if hits else None


res = dict(recovery=[], false_alarms=[], injection=[])
for s, tpub in PUB.items():
    p = path(s)
    if not p:
        res["recovery"].append(dict(sector=s, status="no cached SPOC 2-min file")); continue
    t, f, nfill = load(p)
    keep, T1 = eclipse_mask(t, f, P, D1, D2, SEC)
    in_data = int(np.sum(np.abs(t - tpub) < 3 / 24))
    in_kept = int(np.sum(keep & (np.abs(t - tpub) < 3 / 24)))
    ev = find_events(t[keep], f[keep])
    hit = [e for e in ev if abs(e["center"] - tpub) < 0.3]
    res["recovery"].append(dict(
        sector=s, pub=tpub, sap_filled=nfill, cad_near_transit=in_data, kept_near_transit=in_kept,
        recovered=bool(hit), dt_h=hit[0]["center"] * 24 - tpub * 24 if hit else None,
        dur_h=hit[0]["dur_h"] if hit else None, snr=hit[0]["snr"] if hit else None,
        depth_ppm=hit[0]["depth_ppm"] if hit else None,
        other_events=[(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in ev if e not in hit]))
    fa = find_events(t[keep], 2 - f[keep])
    res["false_alarms"].append(dict(sector=s, n=len(fa), events=[(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in fa]))
    print(res["recovery"][-1], "| flipped:", len(fa), flush=True)

# injection on S98
t, f, _ = load(path(98))
keep, _ = eclipse_mask(t, f, P, D1, D2, SEC)
keep &= ~((t > 4025.30) & (t < 4025.95))
t, f = t[keep], f[keep]
u = [2 * np.sqrt(0.17) * 0.478, np.sqrt(0.17) * (1 - 2 * 0.478)]
B, T14, PER = 0.4, 6.4 / 24, 95.4
ARS = np.sqrt(1.03 ** 2 - B ** 2) / np.sin(np.pi * T14 / PER)
times = [3997.6376, 3999.9, 4014.2876, 4017.1, 4028.0876, 4029.3876, 4037.2876, 4040.8876]
times = [x for x in times if np.sum(np.abs(t - x) < T14 / 2) >= 0.9 * T14 / (2 / 1440)]
base = find_events(t, f)
res["injection_base_events"] = [(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in base]
for re_ in (2, 3, 4, 5, 6, 7, 8):
    rp = re_ / (1.313 * 109.08)
    pr = batman.TransitParams()
    pr.per, pr.rp, pr.a, pr.inc, pr.ecc, pr.w, pr.u, pr.limb_dark = PER, rp, ARS, np.degrees(np.arccos(B / ARS)), 0.0, 90.0, u, "quadratic"
    rec, snrs = 0, []
    for t0 in times:
        pr.t0 = t0
        ev = find_events(t, f * batman.TransitModel(pr, t).light_curve(pr))
        h = [e for e in ev if abs(e["center"] - t0) < 0.25]
        rec += bool(h); snrs.append(round(h[0]["snr"], 1) if h else None)
    res["injection"].append(dict(R_earth=re_, depth_ppm=round(rp ** 2 * 1e6), recovered=rec, n=len(times), snr=snrs))
    print(res["injection"][-1], flush=True)

OUT.write_text(json.dumps(res, indent=1, default=float))
print("written", OUT)
