"""Red-noise-aware error on the TOI-1338 b mid-time in sector 98 (overnight queue item 3).

Shape held at Wang & Liu 2024's prediction (T14 = 6.31 h, b = 0.428, quadratic LD q1 0.17, q2 0.478);
free: mid-time t0, radius ratio rp, linear baseline. Error from (a) the fit covariance (white noise) and
(b) residual permutation ("prayer bead"): add the best-fit model to cyclically shifted residuals and refit,
which keeps the real correlated noise. Prediction: BTJD 4025.5927 +- 0.0159 d (+-23 min).
Uses the cached SPOC 2-min file (no download).
"""
import json, pathlib, numpy as np, lightkurve as lk, batman
from scipy.optimize import curve_fit, brentq

F = r"D:\second-sun\data\wave-3\lk\mastDownload\TESS\tess2025312202959-s0098-0000000260128333-0298-s\tess2025312202959-s0098-0000000260128333-0298-s_lc.fits"
PRED, PRED_ERR = 4025.5927, 0.0159
lc = lk.read(F, quality_bitmask="hard").remove_nans().normalize()
t, f, e = lc.time.value, lc.flux.value, lc.flux_err.value
w = (t > 4025.10) & (t < 4026.20)
t, f, e = t[w], f[w], e[w]
u = [2 * np.sqrt(0.17) * 0.478, np.sqrt(0.17) * (1 - 2 * 0.478)]
B = 0.428
ARS = brentq(lambda a: 95.4 / np.pi * np.arcsin(np.sqrt(1.045 ** 2 - B ** 2) / a) * 24 - 6.31, 2, 2000)


def model(tt, t0, rp, c0, c1):
    p = batman.TransitParams()
    p.t0, p.per, p.rp, p.a, p.inc = t0, 95.4, rp, ARS, np.degrees(np.arccos(B / ARS))
    p.ecc, p.w, p.u, p.limb_dark = 0.0, 90.0, u, "quadratic"
    return batman.TransitModel(p, tt).light_curve(p) * (c0 + c1 * (tt - 4025.6))


p0, lo, hi = [4025.62, 0.045, 1.0, 0.0], [4025.40, 0.01, 0.98, -0.1], [4025.85, 0.12, 1.02, 0.1]
popt, pcov = curve_fit(model, t, f, p0=p0, sigma=e, bounds=(lo, hi))
best = model(t, *popt)
res = f - best
step = max(len(t) // 150, 1)
t0s = []
for k in range(step, len(t), step):
    pk, _ = curve_fit(model, t, best + np.roll(res, k), p0=popt, sigma=e, bounds=(lo, hi))
    t0s.append(pk[0])
t0s = np.array(t0s)
err_white = float(np.sqrt(pcov[0, 0]))
err_rp = float(np.std(t0s))
err = max(err_white, err_rp)
out = dict(t0=float(popt[0]), err_white_min=err_white * 1440, err_prayer_bead_min=err_rp * 1440, n_shifts=len(t0s),
           offset_min=(popt[0] - PRED) * 1440, combined_err_min=float(np.hypot(err, PRED_ERR)) * 1440,
           offset_sigma=float((popt[0] - PRED) / np.hypot(err, PRED_ERR)), rp=float(popt[1]), ars=ARS)
print(json.dumps(out, indent=1))
pathlib.Path(__file__).with_name("timing_s98_results.json").write_text(json.dumps(out, indent=1))
