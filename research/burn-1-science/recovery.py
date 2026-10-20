"""Burn 1, task 2: does our wave-3 method recover TOI-1338 b's PUBLISHED transits?

Ground truth = Wang & Liu 2024 (arXiv:2404.18415) Table 1 midtimes (BTJD). S30 has no fitted midtime there
(damaged egress); we use the paper's predicted S30 time 2142.3991 as an approximate reference.
Same method as wave 3, run per sector (method.py). Match = event centre within 0.5 d of the published midtime.
"""
import json, pathlib, numpy as np, lightkurve as lk
from method import search

PUB = {3: 1391.2516, 6: 1483.9048, 10: 1579.0423, 27: 2049.9515, 30: 2142.3991, 34: 2238.2258,
       37: 2331.0148, 62: 2989.6356, 65: 3085.4243, 68: 3178.2853}
DL = pathlib.Path(r"D:\second-sun\data\burn-1\lk")
OUT = pathlib.Path(__file__).with_name("recovery_results.json")

rows, sizes = [], []
for s, tpub in PUB.items():
    sr = lk.search_lightcurve("TIC 260128333", author="SPOC", exptime=120, sector=s)
    if len(sr) == 0:
        rows.append(dict(sector=s, pub=tpub, status="no SPOC 2-min LC")); continue
    lc = sr[0].download(download_dir=str(DL), quality_bitmask="hard")
    sizes.append((s, pathlib.Path(lc.meta["FILENAME"]).stat().st_size, lc.meta["FILENAME"]))
    lc = lc.remove_nans().normalize()
    t, f = lc.time.value, lc.flux.value
    covered = bool(np.any(np.abs(t - tpub) < 0.1))
    events, mad, info = search(t, f)
    hits = [e for e in events if abs(e["center"] - tpub) < 0.5]
    best = min(hits, key=lambda e: abs(e["center"] - tpub)) if hits else None
    r = dict(sector=s, pub=tpub, n_cad=len(t), covered_after_mask=covered, mad_ppm=mad * 1e6,
             eclipse_depth=info["d1"], n_events=len(events), recovered=best is not None,
             found_center=best and best["center"], dt_h=best and (best["center"] - tpub) * 24,
             found_dur_h=best and best["dur_h"], found_depth_ppm=best and best["depth_ppm"],
             found_snr=best and best["snr"],
             others=[(round(e["center"], 3), round(e["depth_ppm"]), round(e["snr"], 1)) for e in events if e is not best])
    rows.append(r)
    print(json.dumps(r, default=float))

OUT.write_text(json.dumps(dict(rows=rows, sizes=sizes), default=float, indent=1))
