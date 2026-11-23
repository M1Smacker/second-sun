"""Unit 4 plot, lesson 4.1 Eclipsing binaries (Claude, 23 Nov 2026).

TIC 172900988 (the published two-sun planet system of Kostov et al. 2021, AJ 162, 234; arXiv 2105.08614), TESS sectors 44 to 47, SPOC
2-minute PDCSAP light, quality flags removed, each sector divided by its median, folded on the paper's binary period 19.658173 d
(Table 5) with day 0 at our own measured primary eclipse.
Checks that could contradict the lesson (a failure stops the plot):
  1. primary eclipse depth within 8 percentage points of the paper's "about 40%", secondary within 8 of "about 35%" (TESS-only,
     preliminary values in its section 2.1);
  2. the secondary eclipse is NOT half an orbit after the primary (|offset| > 0.05 of the period), as an eccentric orbit requires;
  3. the exact two-eclipse timing (Kepler's equation, edge-on) with the paper's e = 0.4479 can reproduce the measured separation for
     some orientation omega; prints e cos(omega) from the exact solution and from the textbook first-order rule.
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u4.py
"""
import glob, json, pathlib, sys
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lesson_plots as LP

ROOT = LP.ROOT
TIC, P, E = 172900988, 19.658173, 0.44790
T, F = [], []
for p in sorted(glob.glob(str(ROOT / "data" / "known" / "172900988" / "tess2021*-s004[4-7]-*_lc.fits"))):
    t, f, _ = LP.load(p, TIC)
    T.append(t); F.append(f / np.median(f))
t, f = np.concatenate(T), np.concatenate(F)
print("points", len(t), "span", round(t.max() - t.min(), 1), "d")

# the deepest 30-minute point = a primary eclipse centre; refine every eclipse by a parabola through the bottom
tb, fb = LP.binned(t, f, 30)
c0 = tb[np.argmin(fb)]


def centre(c, half=0.25):
    m = np.abs(t - c) < half
    if m.sum() < 50: return None, None
    tt, ff = t[m], f[m]
    k = np.argsort(ff)[:40]
    a, b, _ = np.polyfit(tt[k] - c, ff[k], 2)
    tc = c - b / (2 * a)
    return tc, 1 - np.median(ff[np.abs(tt - tc) < 0.02])


prim, sec = [], []
for n in range(-8, 9):
    tc, d = centre(c0 + n * P)
    if tc: prim.append((tc, d))
# the secondary: deepest point between primaries, away from them
far = np.array([min(abs(((x - c0) / P - round((x - c0) / P)) * P), 99) for x in tb]) > 1.5
s0 = tb[far][np.argmin(fb[far])]
for n in range(-8, 9):
    tc, d = centre(s0 + n * P)
    if tc: sec.append((tc, d))
dp, ds = np.median([d for _, d in prim]), np.median([d for _, d in sec])
t1 = prim[0][0]
off = float(np.median([((tc - t1) / P) % 1.0 for tc, _ in sec]))   # phase of each secondary, then the median (a median of times mixes orbits)
print(f"primary eclipses {len(prim)}, depth {dp*100:.1f}%   secondary eclipses {len(sec)}, depth {ds*100:.1f}%   secondary at {off:.4f} of the orbit ({off*P:.3f} d after the primary)")
if abs(dp - 0.40) > 0.08 or abs(ds - 0.35) > 0.08: sys.exit("depth check failed")
if abs(off - 0.5) < 0.05: sys.exit("the secondary sits at half an orbit: not the eccentric orbit the paper describes")


def sep(omega, e=E):
    """time from primary to secondary conjunction, as a fraction of P, edge-on (primary: true anomaly pi/2 - omega)."""
    def M(fv):
        Ea = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(fv / 2), np.sqrt(1 + e) * np.cos(fv / 2))
        return Ea - e * np.sin(Ea)
    return ((M(1.5 * np.pi - omega) - M(0.5 * np.pi - omega)) / (2 * np.pi)) % 1.0


ws = np.linspace(0, 2 * np.pi, 20001)
vals = np.array([sep(w) for w in ws])
roots = [brentq(lambda w: sep(w) - off, ws[i], ws[i + 1]) for i in range(len(ws) - 1) if (vals[i] - off) * (vals[i + 1] - off) < 0 and abs(vals[i] - vals[i + 1]) < 0.5]
if not roots: sys.exit("no orientation reproduces the measured separation with e = 0.4479")
ecw_exact = [E * np.cos(w) for w in roots]
ecw_first = (off - 0.5) * np.pi / 2
print("exact e cos(omega) for the measured separation:", [round(x, 3) for x in ecw_exact], "| first-order rule (pi/2)(offset):", round(ecw_first, 3))

x = ((t - t1 + 1.0) / P % 1.0) * P - 1.0          # from day -1, so the primary eclipse at day 0 is drawn whole
xb, yb = [], []
for k in np.unique(np.floor(x / (30 / 1440)).astype(int)):
    m = np.floor(x / (30 / 1440)).astype(int) == k   # (bins are counted from day 0, so negative days bin the same way)
    if m.sum() >= 3: xb.append(x[m].mean()); yb.append(f[m].mean())
xb, yb = np.array(xb), np.array(yb)
doc = {"tic": TIC, "sector": 44, "title": "Two stars, two eclipses: four TESS sectors folded on 19.66 days",
       "note": "Each point averages 30 minutes of light, from about five orbits laid on top of each other. Day 0 is the middle of the deeper eclipse; the plot starts one day earlier so that dip shows whole.",
       "x": "Days into the binary's orbit", "y": "Brightness (1 = normal)", "unit": "share", "xabs": True,
       "xlab": "Days into the 19.66-day orbit", "read": {"x": "Day", "xu": "into the orbit", "y": "brightness", "yu": ""},
       "t": [round(float(v), 4) for v in xb], "f": [round(float(v), 4) for v in yb],
       "source": "TESS sectors 44 to 47, SPOC 2-minute light curves (PDCSAP), quality flags removed, each sector divided by its median, folded on the binary period of Kostov et al. 2021; MAST"}
(LP.OUT / "u4-eb-folded.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u4-eb-folded:", len(xb), "points")
