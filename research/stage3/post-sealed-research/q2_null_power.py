# Q2 (31 Oct 2026): what does a null of this power rule out?  Own-data part: noise per box from the planted dips (sigma = depth / K), tier-1 completeness against K, and the single-sector window.
# Exploratory; no outside number is used here (occurrence and geometry are read from papers in the literature file).
import pandas as pd, numpy as np
P = pd.concat([pd.read_pickle(r"D:\second-sun\data\chain_recovery_g2\rows_sealed.pkl").assign(sl="sealed"), pd.read_pickle(r"D:\second-sun\data\chain_recovery_g2\rows_g2dev.pkl").assign(sl="dev")])
P = P[P.K.notna() & P.error.isna() & (P.sign == 1)].copy()
P["sigma_ppm"] = P.depth_ppm / P.K
print("planted dips with K:", len(P), "K values:", sorted(P.K.unique()))
print("noise per box (sigma, ppm) = depth / K, by box length: median, 25%, 75% | tier-1 completeness by K (all stars)")
for d, g in P.groupby("dur"):
    c = {int(k): round(100 * v.tier1.astype(bool).mean(), 0) for k, v in g.groupby("K")}
    print(f"  {d:4.0f} h box: sigma median {g.sigma_ppm.median():6.0f}  [{g.sigma_ppm.quantile(.25):6.0f}, {g.sigma_ppm.quantile(.75):6.0f}]  tier-1 % by K {c}")
cK = P[P.dur == 8].groupby("K").apply(lambda v: v.tier1.astype(bool).mean())
Ks, Cs = np.array(cK.index, float), cK.values
def comp(K): return float(np.interp(K, Ks, Cs, left=Cs[0] * max(K, 0) / Ks[0] if Ks[0] > 0 else 0.0))
sig8 = P[P.dur == 8].sigma_ppm
print("\nWindow: one sector has ~26 d of data; a planet of period P puts at least one transit in it with probability min(1, 26/P) (random phase).")
print("Efficiency eps = P(window) x tier-1 completeness at K = depth/sigma (8 h box, median sigma %.0f ppm; terciles %.0f / %.0f). Depth = (Rp/R*)^2, no dilution, R* = 1 Rsun.\n" % (sig8.median(), sig8.quantile(1/3), sig8.quantile(2/3)))
print("Rp (Re) | depth ppm | K at median sigma | tier-1 completeness | eps at P = 30 / 60 / 95 / 150 / 300 d")
for rp in (2, 4, 6.85, 11):
    dep = (rp / 109.2) ** 2 * 1e6; K = dep / sig8.median(); C = comp(K)
    eps = [min(1, 26 / p) * C for p in (30, 60, 95, 150, 300)]
    print(f"  {rp:5.2f} | {dep:7.0f} | {K:5.1f} | {100*C:4.0f}% | " + " / ".join(f"{100*e:4.1f}%" for e in eps))
print("\nUpper limit on (planets per star) x (geometry factor g): N_ul / (594 stars x eps); N_ul = 8.3 (preregistered-ratio cluster interval upper end) or 1.0 (full-run ratio) kept dips above expectation, 95%.")
for rp in (4, 6.85, 11):
    dep = (rp / 109.2) ** 2 * 1e6; C = comp(dep / sig8.median())
    for p in (95, 300):
        e = min(1, 26 / p) * C
        print(f"  Rp {rp} Re, P {p} d: eps {100*e:.1f}%; N_ul 8.3 -> eta*g <= {8.3/(594*e):.2f}; N_ul 1.0 -> {1.0/(594*e):.2f}  (values above 1 mean no constraint)")
