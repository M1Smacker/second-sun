"""Burn 1, task 2b: WHY does the wave-3 method miss published TOI-1338 b transits?

For each sector (files already downloaded by recovery.py): how much of the published transit window
(Wang & Liu 2024 Table 1 midtime +- duration/2) is removed by the eclipse mask or data gaps, and does the
method recover it with longer biweight windows (1, 2, 3 d)? Also tries S3 from FFI products (no SPOC 2-min).
"""
import json, pathlib, numpy as np, lightkurve as lk
from method import eclipse_mask, find_events

PUB = {3: (1391.2516, 8.5584), 6: (1483.9048, 5.9564), 10: (1579.0423, 11.5838), 27: (2049.9515, 7.1834),
       30: (2142.3991, np.nan), 34: (2238.2258, 9.5885), 37: (2331.0148, 5.8707), 62: (2989.6356, 7.6709),
       65: (3085.4243, 10.2463), 68: (3178.2853, 6.2203)}
DL = pathlib.Path(r"D:\second-sun\data\burn-1\lk")
rows = []
for s, (tp, dur) in PUB.items():
    sr = lk.search_lightcurve("TIC 260128333", author="SPOC", exptime=120, sector=s)
    prod = "SPOC 2-min"
    if len(sr) == 0:
        sr = lk.search_lightcurve("TIC 260128333", sector=s)
        print(f"S{s} products:", list(zip(sr.author, sr.exptime.value)) if len(sr) else "none")
        if len(sr) == 0:
            rows.append(dict(sector=s, note="no light curve")); continue
        prod = f"{sr.author[0]} {sr.exptime[0]}"
    lc = sr[0].download(download_dir=str(DL), quality_bitmask="hard").remove_nans().normalize()
    if prod != "SPOC 2-min":
        print(f"S{s}: downloaded {prod}, {pathlib.Path(lc.meta['FILENAME']).stat().st_size} B, {lc.meta['FILENAME']}")
        rows.append(dict(sector=s, product=prod, note="only 30-min FFI: method needs >=5 cadences per 30-min bin, not applicable"))
        continue
    t, f = lc.time.value, lc.flux.value
    half = (dur if np.isfinite(dur) else 7.0) / 48
    win = np.abs(t - tp) < half
    keep, info = eclipse_mask(t, f)
    cad = np.median(np.diff(t))
    r = dict(sector=s, product=prod, pub=tp, dur_h=dur, expected_cadences=int(2 * half / cad),
             in_data=int(win.sum()), after_mask=int((win & keep).sum()),
             eclipse_T1=info["T1"], eclipse_depth=info["d1"], eclipse_dur_h=info["D1"] * 24,
             secondary_T2=info["T2"], secondary_dur_h=info["D2"] * 24)
    for w in (1.0, 2.0, 3.0):
        ev, mad, bt, bf = find_events(t[keep], f[keep], window=w)
        hit = [e for e in ev if abs(e["center"] - tp) < 0.5]
        inb = np.abs(bt - tp) < half
        r[f"w{w:g}"] = dict(recovered=bool(hit), n_events=len(ev), mad_ppm=round(mad * 1e6),
                            depth_in_window_ppm=round((np.median(bf) - bf[inb].mean()) * 1e6) if inb.any() else None,
                            hit=[(round(e["center"], 3), round(e["dur_h"], 1), round(e["depth_ppm"]), round(e["snr"], 1)) for e in hit],
                            false=[(round(e["center"], 3), round(e["depth_ppm"]), round(e["snr"], 1)) for e in ev if e not in hit])
    rows.append(r)
    print(json.dumps(r, default=float))
pathlib.Path(__file__).with_name("diagnose_results.json").write_text(json.dumps(rows, default=float, indent=1))
