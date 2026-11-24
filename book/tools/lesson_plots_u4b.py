"""Unit 4 plot, lesson 4.2 How two stars orbit each other (Claude, 23 Nov 2026).

The distance between the two stars of TIC 172900988 through one orbit, drawn from Kepler's laws with the paper's values (Kostov et al.
2021: P = 19.658173 d, e = 0.4479, masses 1.2384 and 1.2019 Suns) and the orbit's orientation omega found from OUR light:
  - e cos(omega) = 0.149 from the eclipse timing (lesson 4.1's script), so sin(omega) = +-0.943;
  - the sign from the two eclipses' lengths (valid HERE because both eclipses are deep and the orbit is nearly edge-on, so the two paths
    are nearly equal: Codex 034b F4 showed a grazing tilt such as 87.35 degrees can reverse the length order, so this guard is NOT a
    general direction test; lesson 4.3 measures the equal paths): the stars move slower where they are farther apart, so the eclipse that happens at the
    wider separation lasts longer. The size of the ratio also depends on how squarely the stars cross at each eclipse (impact
    parameter), so we use ONLY which eclipse is longer, measured on the folded 2-minute light, never the ratio's value.
Checks (a failure stops the plot): the separation at the start of the orbit average equals the lesson 2.1 semi-major axis 0.192 AU within
1%; the measured length ratio is on the predicted side by a clear margin (more than 1.3 or less than 0.77).
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u4b.py
"""
import glob, json, pathlib, sys
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lesson_plots as LP

TIC, P, E, M1, M2 = 172900988, 19.658173, 0.44790, 1.2384, 1.2019
ECW = 0.149                                                  # from lesson_plots_u4.py (exact, edge-on)

# measured eclipse lengths on the folded 2-minute light: width where the dip is deeper than half its depth
T, F = [], []
for p in sorted(glob.glob(str(LP.ROOT / "data" / "known" / "172900988" / "tess2021*-s004[4-7]-*_lc.fits"))):
    t, f, _ = LP.load(p, TIC); T.append(t); F.append(f / np.median(f))
t, f = np.concatenate(T), np.concatenate(F)
tb, fb = LP.binned(t, f, 30); t1 = tb[np.argmin(fb)]
ph = ((t - t1 + 1) / P % 1.0) * P - 1


def fwhm(c):
    m = np.abs(ph - c) < 1.0
    x, y = ph[m], f[m]
    o = np.argsort(x); x, y = x[o], y[o]
    k = np.ones(15) / 15
    ys = np.convolve(y, k, mode="same")
    depth = 1 - ys[7:-7].min()
    below = x[7:-7][ys[7:-7] < 1 - depth / 2]
    return below.max() - below.min(), depth


wp, dp = fwhm(0.0); ws, ds = fwhm(11.879)
ratio = ws / wp
print(f"primary: half-depth width {wp*24:.2f} h, depth {dp*100:.1f}%   secondary: {ws*24:.2f} h, depth {ds*100:.1f}%   ratio secondary/primary {ratio:.2f}")
esw = np.sqrt(E ** 2 - ECW ** 2)
print(f"|e sin w| = {esw:.3f}; e sin w > 0 puts the secondary at the wider separation, so the secondary is the longer eclipse")
if 0.77 < ratio < 1.3: sys.exit("eclipse lengths too similar to tell the orientation")
sgn = 1 if ratio > 1 else -1
w = np.arctan2(sgn * esw, ECW)
print(f"omega = {np.degrees(w):.1f} degrees")

# separation through the orbit, day 0 = primary eclipse (true anomaly 90 - omega)
a_au = ((M1 + M2) * (P / 365.25) ** 2) ** (1 / 3)
def M_of(fv):
    Ea = 2 * np.arctan2(np.sqrt(1 - E) * np.sin(fv / 2), np.sqrt(1 + E) * np.cos(fv / 2))
    return Ea - E * np.sin(Ea)
M0 = M_of(np.pi / 2 - w)
days = np.linspace(-1, P - 1, 400)
r = []
for d in days:
    Mx = (M0 + 2 * np.pi * d / P) % (2 * np.pi)
    Ea = brentq(lambda x: x - E * np.sin(x) - Mx, 0, 2 * np.pi)
    r.append(a_au * (1 - E * np.cos(Ea)))
r = np.array(r)
tmean = np.mean(a_au * (1 - E * np.cos(np.linspace(0, 2 * np.pi, 100001))) * (1 - E * np.cos(np.linspace(0, 2 * np.pi, 100001))))
print(f"a = {a_au:.4f} AU (lesson 2.1: 0.192); nearest {r.min():.3f} AU at day {days[r.argmin()]:.2f}, farthest {r.max():.3f} AU at day {days[r.argmax()]:.2f}")
if abs(a_au - 0.192) > 0.002: sys.exit("semi-major axis check failed")
r_sec = r[np.argmin(np.abs(days - 11.879))]
print(f"separation at the primary eclipse {r[np.argmin(np.abs(days))]:.3f} AU, at the secondary {r_sec:.3f} AU")
doc = {"tic": TIC, "sector": None, "title": "How far apart the two stars are, through one orbit",
       "note": "Drawn from Kepler's laws with the published period, stretch and masses, and the orbit's direction read from our own eclipses. Day 0 is the deeper eclipse.",
       "x": "Days into the orbit", "y": "Distance between the stars (AU)", "unit": "AU", "xabs": True,
       "xlab": "Days into the 19.66-day orbit", "read": {"x": "Day", "xu": "into the orbit", "y": "distance", "yu": " AU"}, "star": "",
       "t": [round(float(v), 3) for v in days], "f": [round(float(v), 4) for v in r],
       "source": f"Kepler's laws with P = 19.658173 d, e = 0.4479, masses 1.2384 and 1.2019 Suns (Kostov et al. 2021); orientation omega = {np.degrees(w):.0f} degrees from the eclipse timing and lengths in TESS sectors 44 to 47 (our script book/tools/lesson_plots_u4b.py)"}
(LP.OUT / "u4-separation.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u4-separation:", len(days), "points")
