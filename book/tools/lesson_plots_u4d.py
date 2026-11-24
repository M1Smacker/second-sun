"""Unit 4 plot and numbers, lesson 4.5 The stability limit, and why they are rare (Claude, 24 Nov 2026).

Holman & Wiegert 1999 (AJ 117, 621) fit, for a planet circling both stars of a binary, the smallest stable orbit:
    a_crit / a_bin = 1.60 + 5.10 e - 2.22 e^2 + 4.12 mu - 4.27 e mu - 5.09 mu^2 + 4.61 e^2 mu^2,   mu = M2 / (M1 + M2).
The plot: a_crit / a_bin against the binary's stretch e, for TIC 172900988's mass share. Checks (a failure stops the plot):
  - our a_planet / a_crit reproduces Kostov et al. 2021's 1.34 (within 0.01);
  - Kepler's third law at a_crit gives Kostov's P_stab = 129.7 days (within 1 day) (a figure caption in their section on the planet's orbit, HTML read 24 Nov 2026).
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u4d.py
"""
import json, pathlib, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lesson_plots as LP

P_BIN, E, M1, M2, A_PL = 19.658173, 0.44790, 1.2384, 1.2019, 0.901


def hw(e, mu):
    return 1.60 + 5.10 * e - 2.22 * e ** 2 + 4.12 * mu - 4.27 * e * mu - 5.09 * mu ** 2 + 4.61 * e ** 2 * mu ** 2


mu = M2 / (M1 + M2)
a_bin = ((M1 + M2) * (P_BIN / 365.25) ** 2) ** (1 / 3)
k = hw(E, mu)
a_crit = k * a_bin
p_crit = np.sqrt(a_crit ** 3 / (M1 + M2)) * 365.25
print(f"mu {mu:.4f}; a_bin {a_bin:.4f} AU; a_crit / a_bin {k:.3f}; a_crit {a_crit:.3f} AU; planet a / a_crit {A_PL / a_crit:.3f}; P_crit {p_crit:.1f} d")
print(f"equal stars, circular orbit: {hw(0, 0.5):.3f}; our mass share, circular: {hw(0, mu):.3f}; e = 0.8: {hw(0.8, mu):.3f}")
if abs(A_PL / a_crit - 1.34) > 0.01: sys.exit("check failed: a / a_crit does not reproduce Kostov's 1.34")
if abs(p_crit - 129.7) > 1.0: sys.exit("check failed: P_crit does not reproduce Kostov's 129.7 days")

es = np.round(np.linspace(0, 0.8, 81), 3)
doc = {"tic": None, "sector": None, "title": "How far out a planet must be to survive",
       "note": "The closest stable orbit around both stars, in units of the stars' own orbit size, for a pair whose masses are nearly equal like TIC 172900988's. The more stretched the stars' orbit, the farther out the edge.",
       "x": "Stretch of the stars' orbit (e)", "y": "Closest stable planet orbit / stars' orbit", "unit": "", "xabs": True,
       "xlab": "Stretch of the stars' orbit, e", "read": {"x": "e =", "xu": "", "y": "edge at", "yu": " times the stars' orbit"}, "star": "",
       "t": [float(v) for v in es], "f": [round(float(hw(v, mu)), 3) for v in es],
       "source": "Holman & Wiegert 1999 (AJ 117, 621) stability fit with mass share mu = 0.4925 (Kostov et al. 2021 masses); our script book/tools/lesson_plots_u4d.py reproduces the paper's a / a_crit = 1.34 and P_crit = 129.7 d"}
(LP.OUT / "u4-stability.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u4-stability:", len(es), "points")
