"""Burn 1, task 1b: chi2 map over (mid-time, duration) for the S98 event, b fixed at the predicted 0.428.
At each grid point only rp and a linear baseline are fitted. Uses fit_event_data.npz (from fit_event.py).
Reports where Wang & Liu 2024's prediction (4025.5927, 6.31 h) sits in that map.
"""
import json, pathlib, numpy as np, batman
from scipy.optimize import curve_fit, brentq

here = pathlib.Path(__file__).parent
d = np.load(here / "fit_event_data.npz")
t, f, e = d["t"], d["f"], d["e"]
u = [2 * np.sqrt(0.17) * 0.478, np.sqrt(0.17) * (1 - 2 * 0.478)]
B = 0.428


def ars_for(T14h, rp=0.047):
    return brentq(lambda a: 95.4 / np.pi * np.arcsin(np.sqrt((1 + rp) ** 2 - B ** 2) / a) * 24 - T14h, 1.5, 5000)


def make(t0, ars):
    def m(tt, rp, c0, c1):
        p = batman.TransitParams()
        p.t0, p.per, p.rp, p.a, p.inc = t0, 95.4, rp, ars, np.degrees(np.arccos(B / ars))
        p.ecc, p.w, p.u, p.limb_dark = 0.0, 90.0, u, "quadratic"
        return batman.TransitModel(p, tt).light_curve(p) * (c0 + c1 * (tt - 4025.6))
    return m


def chi2(t0, T14):
    m = make(t0, ars_for(T14))
    pp, _ = curve_fit(m, t, f, p0=[0.047, 1, 0], sigma=e)
    return float(np.sum(((f - m(t, *pp)) / e) ** 2)), pp[0]


T0S = np.arange(4025.45, 4025.801, 0.01)
DURS = np.arange(4.0, 12.01, 0.5)
G = np.array([[chi2(a, b)[0] for b in DURS] for a in T0S])
i, j = np.unravel_index(G.argmin(), G.shape)
cpred, rpred = chi2(4025.5927, 6.31)
res = dict(best_t0=T0S[i], best_T14_h=DURS[j], chi2_min=G.min(), chi2_pred=cpred, dchi2_pred=cpred - G.min(),
           rp_pred=rpred,
           t0_1sigma_range=[float(T0S[(G - G.min() < 2.30).any(1)].min()), float(T0S[(G - G.min() < 2.30).any(1)].max())],
           T14_1sigma_range=[float(DURS[(G - G.min() < 2.30).any(0)].min()), float(DURS[(G - G.min() < 2.30).any(0)].max())],
           t0_2sigma_range=[float(T0S[(G - G.min() < 6.18).any(1)].min()), float(T0S[(G - G.min() < 6.18).any(1)].max())],
           T14_2sigma_range=[float(DURS[(G - G.min() < 6.18).any(0)].min()), float(DURS[(G - G.min() < 6.18).any(0)].max())])
print(json.dumps(res, indent=1, default=float))
(here / "chi2_grid_results.json").write_text(json.dumps(res, indent=1, default=float))
np.savez(here / "chi2_grid.npz", T0S=T0S, DURS=DURS, G=G)

# Fine grid around the minimum, flux errors scaled so the best fit has reduced chi2 = 1 (honest error bars).
scale = np.sqrt(G.min() / (len(t) - 5))
e = e * scale
T0F = np.arange(res["best_t0"] - 0.04, res["best_t0"] + 0.0401, 0.002)
DF = np.arange(5.0, 8.01, 0.1)
GF = np.array([[chi2(a, b)[0] for b in DF] for a in T0F])
i, j = np.unravel_index(GF.argmin(), GF.shape)
in1 = GF - GF.min() < 1.0   # 1-param 1-sigma projections
fine = dict(err_scale=scale, best_t0=T0F[i], best_T14_h=DF[j],
            t0_1sig=[float(T0F[in1.any(1)].min()), float(T0F[in1.any(1)].max())],
            T14_1sig=[float(DF[in1.any(0)].min()), float(DF[in1.any(0)].max())],
            dchi2_pred=chi2(4025.5927, 6.31)[0] - GF.min())
fine["t0_err"] = (fine["t0_1sig"][1] - fine["t0_1sig"][0]) / 2
fine["T14_err"] = (fine["T14_1sig"][1] - fine["T14_1sig"][0]) / 2
fine["dt_min"] = (fine["best_t0"] - 4025.5927) * 1440
fine["dt_sigma_combined"] = (fine["best_t0"] - 4025.5927) / np.hypot(fine["t0_err"], 0.0159)
print(json.dumps(fine, indent=1, default=float))
res["fine"] = fine
(here / "chi2_grid_results.json").write_text(json.dumps(res, indent=1, default=float))
np.savez(here / "chi2_grid.npz", T0S=T0S, DURS=DURS, G=G, T0F=T0F, DF=DF, GF=GF)
