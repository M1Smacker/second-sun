"""Unit 4 plot and numbers, lesson 4.3 Measuring stars from their eclipses (Claude, 24 Nov 2026).

From OUR folded TESS 2-minute light of TIC 172900988 (sectors 44 to 47) we fit each eclipse with a trapezoid to get its total length
(first to last contact). Each eclipse happens at a known distance between the stars (lesson 4.2: Kepler's laws with the paper's P, e,
masses and our omega), where the stars cross the sky at the speed v = h / r (h = sqrt(G M a (1 - e^2)), the orbit's angular momentum
per unit mass). During an eclipse the stars' centres pass at a sky distance of r cos(i), so with S = R1 + R2:
    (v T / 2)^2 + (r cos i)^2 = S^2      at each eclipse.
Two eclipses give two equations: solve for cos(i) and S. Checks (a failure stops the plot): S within 15% of the paper's R1 + R2
(1.384 + 1.312 = 2.696 Sun radii, Kostov et al. 2021 Table 5) and i within 1.5 degrees of the paper's. A check that cannot fail is
not a check: the script also prints what a circular-orbit reading (one speed for both) would have given.
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u4c.py
"""
import glob, json, pathlib, sys
import numpy as np
from scipy.optimize import brentq, least_squares

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lesson_plots as LP

TIC, P, E, M1, M2 = 172900988, 19.658173, 0.44790, 1.2384, 1.2019
W_DEG = 70.6                                     # omega from lesson_plots_u4b.py (printed there; rerun it if inputs change)
GM_SUN, AU_M, RSUN_KM = 1.32712440018e20, 1.495978707e11, 695700.0
I_PAPER = None                                   # filled from the command line check below, see Sources in the lesson

T, F = [], []
for p in sorted(glob.glob(str(LP.ROOT / "data" / "known" / "172900988" / "tess2021*-s004[4-7]-*_lc.fits"))):
    t, f, _ = LP.load(p, TIC); T.append(t); F.append(f / np.median(f))
t, f = np.concatenate(T), np.concatenate(F)
tb, fb = LP.binned(t, f, 30); t1 = tb[np.argmin(fb)]
ph = ((t - t1 + 1) / P % 1.0) * P - 1                 # days from the primary eclipse, -1 to P - 1


def trapezoid(x, c, depth, t14, t23):
    t23 = min(abs(t23), abs(t14))
    y = np.ones_like(x)
    d = np.abs(x - c)
    flat = d <= t23 / 2
    slope = (d > t23 / 2) & (d < t14 / 2)
    y[flat] = 1 - depth
    y[slope] = 1 - depth * (t14 / 2 - d[slope]) / ((t14 - t23) / 2)
    return y


def fit(centre):
    m = np.abs(ph - centre) < 0.8
    x, y = ph[m], f[m]
    r = least_squares(lambda q: trapezoid(x, *q) - y, [centre, 0.4, 0.3, 0.02],
                      bounds=([centre - 0.2, 0.05, 0.02, 0.0], [centre + 0.2, 0.9, 1.0, 0.5]))
    c, depth, t14, t23 = r.x
    resid = trapezoid(x, *r.x) - y
    return c, depth, t14, min(abs(t23), t14), np.std(resid), len(x)


cp, dp, Tp, T23p, sp, np_ = fit(0.0)
cs, ds, Ts, T23s, ss, ns = fit(11.879)
print(f"primary:   centre {cp:+.4f} d, depth {dp*100:.1f}%, total length {Tp*24:.2f} h, flat part {T23p*24:.2f} h, scatter {sp*1e3:.2f} ppt, {np_} points")
print(f"secondary: centre {cs:.4f} d, depth {ds*100:.1f}%, total length {Ts*24:.2f} h, flat part {T23s*24:.2f} h, scatter {ss*1e3:.2f} ppt, {ns} points")

# separations and sky speeds at the two eclipses
a_m = (GM_SUN * (M1 + M2) * (P * 86400 / (2 * np.pi)) ** 2) ** (1 / 3)
w = np.radians(W_DEG)
r_at = lambda fv: a_m * (1 - E ** 2) / (1 + E * np.cos(fv))
rp, rs = r_at(np.pi / 2 - w), r_at(3 * np.pi / 2 - w)  # primary: true anomaly 90 - omega; secondary: 270 - omega
h = np.sqrt(GM_SUN * (M1 + M2) * a_m * (1 - E ** 2))
vp, vs = h / rp, h / rs
print(f"a = {a_m/AU_M:.4f} AU; at the primary r = {rp/AU_M:.4f} AU, sky speed {vp/1e3:.1f} km/s; at the secondary r = {rs/AU_M:.4f} AU, {vs/1e3:.1f} km/s")

hp, hs = vp * Tp * 86400 / 2, vs * Ts * 86400 / 2       # half of each path, metres: R1 + R2 can be no smaller than this
Sp, Ss = hp / 1e3 / RSUN_KM, hs / 1e3 / RSUN_KM
print(f"lower bounds on R1 + R2 (centres crossing dead centre): primary {Sp:.3f}, secondary {Ss:.3f} Sun radii; length ratio {Ts/Tp:.3f}, speed ratio {vp/vs:.3f}")
# the paper's tilt and sizes (Kostov et al. 2021 Table 5: i1 = 89.4182 deg, R1 = 1.3846, R1/R2 = 1.0527): predicted first-to-last-contact lengths
I_P, R1_P, Q_P = 89.4182, 1.3846, 1.0527
S_P = R1_P * (1 + 1 / Q_P)
ci = np.cos(np.radians(I_P))
for nm, r, v, T in (("primary", rp, vp, Tp), ("secondary", rs, vs, Ts)):
    d = r * ci / 1e3 / RSUN_KM
    Tpred = 2 * np.sqrt(S_P ** 2 - d ** 2) * RSUN_KM * 1e3 / v / 3600
    print(f"{nm}: sky offset at mid-eclipse {d:.3f} Sun radii; predicted length {Tpred:.2f} h; ours {T*24:.2f} h = {T*24/Tpred:.3f} of it")
for tilt in (88.0, 85.0):
    c = np.cos(np.radians(tilt))
    print(f"if tilted to {tilt} deg: offsets {rp*c/1e3/RSUN_KM:.2f} and {rs*c/1e3/RSUN_KM:.2f} Sun radii (eclipse needs under {S_P:.2f})")
print(f"paper R1 + R2 = {S_P:.3f} Sun radii; ours as a lower bound is {Sp/S_P:.3f} of it")
if abs(Sp - Ss) / S_P > 0.05: sys.exit("check failed: the two eclipses' bounds differ by more than 5%")
if not (0.75 < Sp / S_P < 1.0): sys.exit("check failed: lower bound not between 75% and 100% of the paper's size")
# the plot: the folded light around each eclipse with the fitted trapezoids, hours from mid-eclipse
out = {}
for name, c, d, T14, T23 in (("u4-eclipse-primary", cp, dp, Tp, T23p), ("u4-eclipse-secondary", cs, ds, Ts, T23s)):
    m = np.abs(ph - c) < 0.5
    x = (ph[m] - c) * 24; y = f[m]
    o = np.argsort(x); x, y = x[o], y[o]
    xb = np.arange(-12, 12.01, 0.25); yb = [float(np.median(y[np.abs(x - v) < 0.125])) if np.any(np.abs(x - v) < 0.125) else None for v in xb]
    keep = [k for k, v in enumerate(yb) if v is not None]
    doc = {"tic": TIC, "sector": None, "title": ("The deeper eclipse" if "primary" in name else "The shallower eclipse") + ", hour by hour",
           "note": f"TESS 2-minute light, sectors 44 to 47, folded and averaged every 15 minutes. The fitted shape lasts {T14*24:.1f} hours from first to last touch.",
           "x": "Hours from mid-eclipse", "y": "Brightness (1 = normal)", "unit": "", "xabs": True,
           "xlab": "Hours from mid-eclipse", "read": {"x": "Hour", "xu": "h", "y": "brightness", "yu": ""}, "star": "",
           "t": [round(float(xb[k]), 2) for k in keep], "f": [round(yb[k], 4) for k in keep],
           "source": "TESS sectors 44 to 47 SPOC 2-minute light of TIC 172900988, folded on 19.658173 d; trapezoid fit by book/tools/lesson_plots_u4c.py"}
    (LP.OUT / f"{name}.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
    out[name] = len(keep)
print("plots:", out)
