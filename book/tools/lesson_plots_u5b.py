"""Unit 5 plot and numbers, lesson 5.2 How TESS watches the sky (Claude, 24 Nov 2026).

One sector (46) of TESS 2-minute light of TIC 172900988, binned to 30 minutes, with the gap where TESS sends its data home.
Also prints, from our own files, the facts the lesson quotes: sector spans, cadence, the downlink gap, 2-minute targets per sector,
the hemisphere of each year's targets and the number of distinct 2-minute stars (TESS Science Office target lists, data/census_targets_2m).
Checks (a failure stops): the cadence is 120 s; the raw largest gap is 0.5 to 2 days, between days 10 and 15; the usable (quality-masked) gap
contains it (first run, 24 Nov: raw 1.39 d, usable 2.74 d: flagged cadences around the downlink widen it).
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u5b.py
"""
import glob, json, pathlib, re, sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lesson_plots as LP

TIC = 172900988
p = glob.glob(str(LP.ROOT / "data" / "known" / "172900988" / "tess2021*-s0046-*_lc.fits"))[0]
t, f, _ = LP.load(p, TIC)
f = f / np.median(f)
d = np.diff(t)
cad, gi = np.median(d) * 86400, int(np.argmax(d))
print(f"sector 46: span {t[-1]-t[0]:.2f} d, cadence {cad:.1f} s, largest gap {d[gi]:.2f} d starting at day {t[gi]-t[0]:.2f}")
if abs(cad - 120) > 1: sys.exit("cadence check failed")
from astropy.io import fits
raw = fits.getdata(p, 1)["TIME"]; raw = raw[np.isfinite(raw)]; dr = np.diff(raw); ri = int(np.argmax(dr))
print(f"raw timestamps (before quality flags): largest gap {dr[ri]:.2f} d starting at day {raw[ri]-raw[0]:.2f}")
if not (0.5 < dr[ri] < 2 and 10 < raw[ri] - raw[0] < 15): sys.exit("raw gap check failed")
if not (d[gi] >= dr[ri] - 0.01 and 10 < t[gi] - t[0] < 15): sys.exit("usable gap check failed")

r = {}
for fn in glob.glob(str(LP.ROOT / "data" / "census_targets_2m" / "all_targets_S*_v1.csv")):
    s = int(re.search(r"S(\d+)", fn).group(1)); x = pd.read_csv(fn, comment="#"); r[s] = (len(x), float((x.Dec < 0).mean()), set(x.TICID))
for a, b in ((1, 13), (14, 26), (27, 39), (40, 55)):
    print(f"sectors {a} to {b}: share of 2-minute targets south of the equator {np.mean([r[s][1] for s in range(a, b + 1)]):.2f}")
print("2-minute targets in sectors 1, 13, 27, 56, 100:", [r[s][0] for s in (1, 13, 27, 56, 100)])
print("distinct 2-minute stars, sectors 1 to", max(r), ":", len(set().union(*[v[2] for v in r.values()])))

tb, fb = LP.binned(t, f, 30)
x0 = t[0]
doc = {"tic": TIC, "sector": 46, "title": "One TESS sector of our two-sun star",
       "note": "Sector 46, TESS 2-minute light averaged every 30 minutes. The deep drops are the stars' eclipses. The empty stretch in the middle is around the time TESS sends its data home.",
       "x": "Days since the sector began", "y": "Brightness (1 = normal)", "unit": "", "xabs": True,
       "xlab": "Days since the sector began", "read": {"x": "Day", "xu": "of the sector", "y": "brightness", "yu": ""}, "star": "",
       "t": [round(float(v - x0), 3) for v in tb], "f": [round(float(v), 4) for v in fb],
       "source": "TESS sector 46 SPOC 2-minute light of TIC 172900988 (MAST), averaged every 30 minutes by book/tools/lesson_plots_u5b.py"}
(LP.OUT / "u5-one-sector.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u5-one-sector:", len(tb), "points")
