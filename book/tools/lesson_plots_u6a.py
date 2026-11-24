"""Unit 6 plot and numbers, lesson 6.1 Smoothing out slow changes (Claude, 24 Nov 2026).

Sector 46 of TIC 172900988 (corrected light, quality flags removed): divide by a running median of width w (centred, in days) and measure
how much of each eclipse's depth survives, for w = 0.25, 0.5, 1, 2 and 3 days. Depth = 1 minus the median of the 30 lowest 2-minute points
within 0.1 d of the eclipse centre, after dividing; compared with the same measure on the undivided light.
The plot: the light after a 0.5-day running median (the eclipses partly eaten). Checks (a failure stops): the kept share rises with w for
every eclipse found (wider windows eat less); a 6-hour window keeps under half of a 13-hour eclipse and a 2-day window over 90%.
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
# Eclipses found by their depth, never assumed (24 Nov 2026, 11:54 pm: the first version took the deepest dip as the primary, but in
# sector 46 the primary falls inside the data-sending hole, so both visible dips are secondaries; the "secondary" it then measured was
# plain starlight). A dip is any 30-minute bin below 0.80; its kind comes from its depth (primary about 43.5%, secondary about 35.8%).
tb, fb = LP.binned(t, f, 30)
low = tb[fb < 0.80]
groups = np.split(low, np.where(np.diff(low) > 0.5)[0] + 1) if len(low) else []
ecl = []
for gr in groups:
    m = np.abs(t - gr.mean()) < 0.6
    c = t[m][np.argmin(f[m])]
    dep = 1 - f[m].min()
    ecl.append((c, "primary" if dep > 0.40 else "secondary"))
print("eclipses in sector 46:", [(round(c - t.min(), 2), k) for c, k in ecl])
if not ecl: sys.exit("no eclipse found")

def depth(flux, c):
    m = np.abs(t - c) < 0.1
    return 1 - np.median(np.sort(flux[m])[:30])


def runmed(w):
    return np.array([np.median(f[np.abs(t - x) < w / 2]) for x in t])


base = {c: depth(f, c) for c, _ in ecl}
rows = {}
for w in (0.25, 0.5, 1.0, 2.0, 3.0):
    g = f / runmed(w)
    rows[w] = {k: float(np.mean([depth(g, c) / base[c] for c, kk in ecl if kk == k])) for k in {kk for _, kk in ecl}}
    print(f"window {w:4.2f} d (= {w*24:.0f} h):", ", ".join(f"{k} keeps {v:.2f} of its depth" for k, v in rows[w].items()))
ws = sorted(rows)
for k in rows[ws[0]]:
    if any(rows[ws[i + 1]][k] < rows[ws[i]][k] - 0.02 for i in range(len(ws) - 1)): sys.exit(f"check failed: {k} kept share does not rise with window")
for k in rows[ws[0]]:
    if not (rows[0.25][k] < 0.5 and rows[2.0][k] > 0.9): sys.exit(f"check failed: {k}: a window shorter than the eclipse should eat most of it, a 2-day one almost none")
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
