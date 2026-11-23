"""Unit 3 plot, lesson 3.4 Doppler (Claude, 23 Nov 2026).

51 Pegasi's radial velocities from the 25-year Lick planet search (Fischer, Marcy and Spronck 2014, ApJS 210, 5; VizieR J/ApJS/210/5,
table 2, star HD 217014), downloaded 23 Nov 2026 (research/downloads.csv), 354 measurements.
Checks that could contradict the lesson (a failure stops the plot):
  1. a period search over 1 to 10 days finds the published period, 4.2307966 d (NASA Exoplanet Archive default, Cont et al. 2026),
     within 0.001 d;
  2. a sine fit at that period gives a semi-amplitude K within 2 m/s of the published 55.77 m/s;
  3. the planet's minimum mass from K, P and the star's mass (1.07 solar) is within 10% of the published 0.46 to 0.47 Jupiter masses.
The plot: every measurement folded on the period (x = days into the orbit, 0 to 4.23), y = velocity in m/s with the star's mean removed.
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u3c.py
"""
import json, pathlib, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "book" / "docs" / "assets" / "data" / "lessons"
SRC = ROOT / "data" / "learn-sources" / "lick-51peg-rv" / "fischer2014-table2-HD217014.tsv"
P_PUB, K_PUB, MSINI_PUB, MSTAR = 4.2307966, 55.77, 0.465, 1.07

rows = [l.split("\t") for l in SRC.read_text(encoding="latin-1").splitlines() if l.strip().startswith("217014")]
jd = np.array([float(r[1]) for r in rows]) + 2400000.0
rv = np.array([float(r[2]) for r in rows]); err = np.array([float(r[3]) for r in rows])
print("measurements", len(jd), "span", round((jd.max() - jd.min()) / 365.25, 1), "years")
if len(jd) != 354:
    sys.exit("unexpected row count")

# CCD dewars have different zero points (the paper's note 2); remove each dewar's own mean before anything else.
dew = np.array([int(r[5]) for r in rows])
for d in np.unique(dew):
    m = dew == d
    rv[m] -= np.average(rv[m], weights=1 / err[m] ** 2)
print("dewars", {int(d): int((dew == d).sum()) for d in np.unique(dew)})


def sine_fit(P):
    ph = 2 * np.pi * jd / P
    A = np.c_[np.sin(ph), np.cos(ph), np.ones_like(ph)]
    w = 1 / err
    coef, *_ = np.linalg.lstsq(A * w[:, None], rv * w, rcond=None)
    chi2 = float(np.sum(((A @ coef - rv) * w) ** 2))
    return coef, chi2


# 1. period search: chi-square of a sine at each trial frequency
freqs = np.linspace(1 / 10, 1 / 1, 200000)
chi = np.array([sine_fit(1 / f)[1] for f in freqs[::20]])
f0 = freqs[::20][chi.argmin()]
fine = np.linspace(f0 - 2e-4, f0 + 2e-4, 4001)
P_best = 1 / fine[np.argmin([sine_fit(1 / f)[1] for f in fine])]
print(f"period search best {P_best:.6f} d  published {P_PUB} d  difference {P_best - P_PUB:+.6f} d")
if abs(P_best - P_PUB) > 0.001:
    sys.exit("period check failed")

# 2. semi-amplitude at the published period
coef, chi2 = sine_fit(P_PUB)
K = float(np.hypot(coef[0], coef[1]))
print(f"K = {K:.2f} m/s  published {K_PUB}  reduced chi-square {chi2 / (len(jd) - 3):.2f}")
if abs(K - K_PUB) > 2:
    sys.exit("amplitude check failed")

# 3. minimum mass: m sin i = K (P / (2 pi G))^(1/3) M*^(2/3)  (planet mass << star mass, circular orbit)
G, MSUN, MJUP = 6.674e-11, 1.989e30, 1.898e27
msini = K * (P_PUB * 86400 / (2 * np.pi * G)) ** (1 / 3) * (MSTAR * MSUN) ** (2 / 3) / MJUP
print(f"m sin i = {msini:.3f} Jupiter masses  published about {MSINI_PUB}")
if abs(msini / MSINI_PUB - 1) > 0.10:
    sys.exit("mass check failed")

# the folded plot: day 0 = the moment the star moves fastest toward us (most negative velocity, a blueshift)
phase0 = np.arctan2(coef[1], coef[0])                       # model = K sin(2 pi t/P + phase0) + c
t_fast_toward = (P_PUB / (2 * np.pi)) * ((-np.pi / 2 - phase0) % (2 * np.pi))
x = ((jd - t_fast_toward) / P_PUB % 1.0) * P_PUB
y = rv - coef[2]
o = np.argsort(x)
doc = {"tic": None, "sector": None, "title": "51 Pegasi wobbles: 354 speed measurements over 16 years, folded on 4.23 days",
       "note": "Each dot is one measured speed of the star toward us (below zero) or away (above zero), placed by how far it was into the planet's 4.23-day orbit.",
       "x": "Days into the orbit", "y": "Star's speed (metres per second)", "unit": "m/s", "xabs": True,
       "xlab": "Days into the 4.23-day orbit", "read": {"x": "Day", "xu": "into the orbit", "y": "speed", "yu": " m/s"}, "star": "",
       "t": [round(float(v), 4) for v in x[o]], "f": [round(float(v), 2) for v in y[o]],
       "source": "Lick Observatory planet search, radial velocities of 51 Pegasi (HD 217014), Fischer, Marcy and Spronck 2014, ApJS 210, 5 (VizieR J/ApJS/210/5)"}
(OUT / "u3-51peg-rv.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u3-51peg-rv: written,", len(x), "points; folded, day 0 = fastest toward us")
