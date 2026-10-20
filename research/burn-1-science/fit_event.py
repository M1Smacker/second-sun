"""Burn 1, task 1: fit the S98 event and compare with Wang & Liu 2024's predicted TOI-1338 b transit.

Prediction (arXiv:2404.18415 Table 3, BJD-2455000 6025.5927 +- 0.0159 -> BTJD 4025.5927, 6.31 +- 0.15 h, b = 0.428).
Fit: batman single transit + linear baseline on SPOC PDCSAP 2-min (hard mask), window BTJD 4025.10-4026.20
(starts after the primary-eclipse mask). Free: t0, rp, a/rs, b, c0, c1. LD from the paper (q1 0.17, q2 0.478).
Also checks whether S97 covers the predicted 2025-09-14 transit (BTJD 3932.7322, 10.0 h).
"""
import json, pathlib, numpy as np, lightkurve as lk, batman
from scipy.optimize import curve_fit

DL = pathlib.Path(r"D:\second-sun\data\wave-3\lk")
lcs = {}
for s in (97, 98):
    sr = lk.search_lightcurve("TIC 260128333", author="SPOC", exptime=120, sector=s)
    lcs[s] = sr[0].download(download_dir=str(DL), quality_bitmask="hard").remove_nans().normalize()

t97 = lcs[97].time.value
s97 = dict(range=(float(t97.min()), float(t97.max())),
           n_within_5h_of_3932_73=int(np.sum(np.abs(t97 - 3932.7322) < 5 / 24)),
           nearest_cadence_gap_d=float(np.min(np.abs(t97 - 3932.7322))))
print("S97 coverage of predicted 3932.7322:", s97)

lc = lcs[98]
t, f, e = lc.time.value, lc.flux.value, lc.flux_err.value
w = (t > 4025.10) & (t < 4026.20)
t, f, e = t[w], f[w], e[w]
q1, q2 = 0.17, 0.478
u = [2 * np.sqrt(q1) * q2, np.sqrt(q1) * (1 - 2 * q2)]


def model(tt, t0, rp, ars, b, c0, c1):
    p = batman.TransitParams()
    p.t0, p.per, p.rp, p.a = t0, 95.4, rp, ars
    p.inc = np.degrees(np.arccos(min(b / ars, 1)))
    p.ecc, p.w, p.u, p.limb_dark = 0.0, 90.0, u, "quadratic"
    return batman.TransitModel(p, tt).light_curve(p) * (c0 + c1 * (tt - 4025.6))


results = {}
for label, bfix in (("free_b", None), ("b_fixed_0.428", 0.428)):
    fm = model if bfix is None else (lambda tt, t0, rp, ars, c0, c1: model(tt, t0, rp, ars, bfix, c0, c1))
    full = (lambda pp: pp) if bfix is None else (lambda pp: np.insert(pp, 3, bfix))
    p0 = [4025.62, 0.05, 60, 0.4, 1.0, 0.0]
    lo, hi = [4025.4, 0.01, 5, 0, 0.98, -0.1], [4025.8, 0.15, 400, 0.95, 1.02, 0.1]
    if bfix is not None:
        del p0[3], lo[3], hi[3]
    popt, pcov = curve_fit(fm, t, f, p0=p0, sigma=e, bounds=(lo, hi))
    perr = np.sqrt(np.diag(pcov))
    tf = np.linspace(t.min(), t.max(), 20000)
    def t14(pp):
        pp = full(np.array(pp, float)); pp[3] = np.clip(pp[3], 0, 0.95); pp[2] = max(pp[2], 5); pp[1] = max(pp[1], 0.005)
        m = model(tf, *pp) / (pp[4] + pp[5] * (tf - 4025.6)); ii = tf[m < 1 - 1e-6]
        return ((ii.max() - ii.min()) * 24 if len(ii) else np.nan), 1 - m.min()
    T14, dep = t14(popt)
    T14s = [t14(pp)[0] for pp in np.random.default_rng(1).multivariate_normal(popt, pcov, 300)]
    pf = full(popt)
    results[label] = dict(t0=popt[0], t0_err=perr[0], rp=popt[1], rp_err=perr[1], ars=popt[2], b=pf[3],
               depth_ppm=dep * 1e6, T14_h=T14, T14_err_h=float(np.nanstd(T14s)),
               dt_min=(popt[0] - 4025.5927) * 1440, dt_sigma=(popt[0] - 4025.5927) / np.hypot(perr[0], 0.0159),
               rp_RE=popt[1] * 1.313 * 109.08,
               chi2=float(np.sum(((f - fm(t, *popt)) / e) ** 2)), n_points=int(len(t)))
    if bfix is not None:
        np.savez(pathlib.Path(__file__).with_name("fit_event_data.npz"), t=t, f=f, e=e, tf=tf,
                 mf=model(tf, *pf), base=pf[4] + pf[5] * (t - 4025.6), basef=pf[4] + pf[5] * (tf - 4025.6))
# chi2 of the PREDICTED shape (t0, T14, b from the paper; only rp and baseline fitted)
from scipy.optimize import brentq
def ars_for(T14h, b=0.428, rp=0.045):
    def g(a):
        return (95.4 / np.pi * np.arcsin(np.sqrt((1 + rp) ** 2 - b ** 2) / a)) * 24 - T14h
    return brentq(g, 2, 2000)
a_pred = ars_for(6.31)
fp = lambda tt, rp, c0, c1: model(tt, 4025.5927, rp, a_pred, 0.428, c0, c1)
pp, _ = curve_fit(fp, t, f, p0=[0.045, 1, 0], sigma=e)
results["predicted_shape"] = dict(t0=4025.5927, T14_h=6.31, b=0.428, rp=pp[0], chi2=float(np.sum(((f - fp(t, *pp)) / e) ** 2)))
results["s97"] = s97
res = results
print(json.dumps(res, indent=1, default=float))
pathlib.Path(__file__).with_name("fit_event_results.json").write_text(json.dumps(res, indent=1, default=float))
