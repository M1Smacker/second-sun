"""Unit 6 plot and numbers, lesson 6.1 Smoothing out slow changes (Claude, 24 Nov 2026).

Sector 46 of TIC 172900988 (corrected light, quality flags removed): divide by a running median of width w (centred, in days) and measure
how much of each eclipse's depth survives, for w = 0.25, 0.5, 1, 2 and 3 days. Depth = 1 minus the median of the 30 lowest 2-minute points
within 0.1 d of the eclipse centre, after dividing; compared with the same measure on the undivided light.
The plot: the light after a 0.5-day running median (the eclipses partly eaten). Checks (a failure stops): the kept share rises with w for
both eclipses (wider windows eat less), and the longer secondary loses more than the primary at every w.
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u6a.py
"""
import glob, json, pathlib, sys
import numpy as np
from astropy.io import fits

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lesson_plots as LP

TIC, P = 172900988, 19.658173
p = glob.glob(str(LP.ROOT / "data" / "known" / "172900988" / "tess2021*-s0046-*_lc.fits"))[0]
d = fits.getdata(p, 1)
q = (d["QUALITY"] == 0) & np.isfinite(d["PDCSAP_FLUX"])
t, f = d["TIME"][q], d["PDCSAP_FLUX"][q]
f = f / np.median(f)
tb, fb = LP.binned(t, f, 30); tp = tb[np.argmin(fb)]
cands = [tp + k * P for k in range(-2, 3)] + [tp + 11.879 + k * P for k in range(-2, 3)]
ecl = [(c, "primary" if abs(((c - tp) / P) % 1) < 0.01 or abs(((c - tp) / P) % 1 - 1) < 0.01 else "secondary") for c in cands
       if t.min() + 0.3 < c < t.max() - 0.3 and np.sum(np.abs(t - c) < 0.1) > 60]
print("eclipses in sector 46:", [(round(c - t.min(), 2), k) for c, k in ecl])


def depth(flux, c):
    m = np.abs(t - c) < 0.1
    return 1 - np.median(np.sort(flux[m])[:30])


def runmed(w):
    return np.array([np.median(f[np.abs(t - x) < w / 2]) for x in t])


base = {c: depth(f, c) for c, _ in ecl}
rows = {}
for w in (0.25, 0.5, 1.0, 2.0, 3.0):
    g = f / runmed(w)
    rows[w] = {k: np.mean([depth(g, c) / base[c] for c, kk in ecl if kk == k]) for k in ("primary", "secondary")}
    print(f"window {w:4.2f} d: primary keeps {rows[w]['primary']:.2f} of its depth, secondary keeps {rows[w]['secondary']:.2f}")
ws = sorted(rows)
for k in ("primary", "secondary"):
    if any(rows[ws[i + 1]][k] < rows[ws[i]][k] - 0.02 for i in range(len(ws) - 1)): sys.exit(f"check failed: {k} kept share does not rise with window")
if any(rows[w]["secondary"] > rows[w]["primary"] + 0.02 for w in ws): sys.exit("check failed: the longer eclipse lost less")
g = f / runmed(0.5)
tb, fb = LP.binned(t, g, 30)
doc = {"tic": TIC, "sector": 46, "title": "Smoothed with a half-day window",
       "note": "Sector 46 after dividing by a running median half a day wide. Slow changes are gone, and so is part of each eclipse: the window could not tell them apart.",
       "x": "Days since the sector began", "y": "Brightness after smoothing", "unit": "", "xabs": True,
       "xlab": "Days since the sector began", "read": {"x": "Day", "xu": "of the sector", "y": "brightness", "yu": ""}, "star": "",
       "t": [round(float(v - t.min()), 3) for v in tb], "f": [round(float(v), 4) for v in fb],
       "source": "TESS sector 46 SPOC 2-minute light of TIC 172900988 (MAST), divided by a 0.5-day running median by book/tools/lesson_plots_u6a.py"}
(LP.OUT / "u6-smoothed.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u6-smoothed:", len(tb), "points")
