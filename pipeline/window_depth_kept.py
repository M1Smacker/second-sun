"""Vesper study C1: how much of a dip the biweight detrend keeps, by window length. Synthetic white-noise star (300 ppm per 2 min), 1000 ppm box dip, 30 runs per cell; window = max(2 d, k x box). Usage: python window_depth_kept.py (writes research/stage3/window-depth-kept.txt)"""
import numpy as np, sys
sys.path.insert(0, ".")
from detect_v2 import detrend
rng = np.random.default_rng(2)
t = np.arange(0, 30, 2/1440)
OUT = ["kept share of a 1000 ppm dip (white noise, 30 runs); window = max(2 d, k x box)"]
for dur in (8, 14, 20):
    row = []
    for k in (0, 3, 4, 5, 6, 8):
        w = 2.0 if k == 0 else max(2.0, k * dur / 24)
        dep = []
        for _ in range(30):
            f = 1 + rng.normal(0, 300e-6, t.size); tc = 15.0
            f[np.abs(t - tc) < dur/48] -= 1000e-6
            tt, ff = detrend(t, f, window_d=w)
            inb = np.abs(tt - tc) < dur/48; ob = (np.abs(tt - tc) > dur/24) & (np.abs(tt - tc) < 2.5)
            dep.append((np.nanmedian(ff[ob]) - np.nanmean(ff[inb])) * 1e6)
        row.append("k=%s w=%.2fd: %.0f%%" % (k or "base", w, np.mean(dep) / 10))
    OUT.append(str(dur) + " h | " + " | ".join(row))
print(chr(10).join(OUT)); open("../research/stage3/window-depth-kept.txt", "w", encoding="utf-8").write(chr(10).join(OUT) + chr(10))
