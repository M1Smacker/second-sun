"""N-01 (Fable audit): independent re-derivation of (1) the forward Census odds and (2) the S2 interval. No project code imported.
(1) Different method from census_worth3.py: Monte Carlo draws from the prior, importance-weighted by the null likelihood, instead of a grid sum.
    Inputs copied from census_worth3.py (past_E, per, ratio); they are Horizon outputs, not re-derived here.
    Then a sensitivity the project has not done: the eclipse-mask loss (finding F-01) as a factor m on E (m = share of expected detections that survive the mask).
    Case X: Census run with the mask unfixed (m on past E and on Census E). Case Y: mask fixed for Census (m on past E only).
(2) Exact (Clopper-Pearson / Garwood) intervals for 115 in 13,412, 32 in 3,425 and the chance that a true rate of 8 per 1,000 gives at least the observed count.
Usage: python n01_census_odds_and_s2.py"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(7)
past_E = {(1.5, "A"): 1.88, (1.5, "B"): 2.89, (1.8, "A"): 1.57, (1.8, "B"): 2.41, (2.2, "A"): 1.28, (2.2, "B"): 1.97}
per = {(1.5, "A"): 0.0163, (1.5, "B"): 0.0251, (1.8, "A"): 0.0136, (1.8, "B"): 0.0209, (2.2, "A"): 0.0111, (2.2, "B"): 0.0171}
ratio = 88.5 / 195.6
M = 400_000
draws = {"A": np.exp(np.log(0.10) + np.log(2) * rng.standard_normal(M)),            # lognormal, median 10%, factor 2 (untruncated; the project's grid stops at 0.1% and 40%)
         "B": np.exp(rng.uniform(np.log(0.01), np.log(0.20), M))}                   # log-uniform 1% to 20%


def forward(E0, Ec, r, c):
    w = np.exp(-c * E0 * r / 0.1)
    return float((w * (1 - np.exp(-c * Ec * r / 0.1))).sum() / w.sum()), float(np.average(r, weights=w))


print("(1) Forward Census odds, c = 0.9: mine (Monte Carlo) per prior; the project's ranges are 36-52% (A) and 21-31% (B) at 1,400; 59-76% and 37-52% at 3,000")
for N in (1400, 3000):
    for pn in "AB":
        v = [forward(E0, 0.1 * N * per[k] * ratio, draws[pn], 0.9)[0] for k, E0 in past_E.items()]
        print(f"   N {N} prior {pn}: {100*min(v):.0f}% to {100*max(v):.0f}%")
print("\n    With the mask loss (F-01), factor m on E. X = Census also run with the unfixed mask; Y = mask fixed before Census. N 1,400, c 0.9:")
for m in (1.0, 0.8, 0.6, 0.4):
    out = []
    for pn in "AB":
        x = [forward(m * E0, m * 0.1 * 1400 * per[k] * ratio, draws[pn], 0.9)[0] for k, E0 in past_E.items()]
        y = [forward(m * E0, 0.1 * 1400 * per[k] * ratio, draws[pn], 0.9)[0] for k, E0 in past_E.items()]
        rm = [forward(m * E0, 0, draws[pn], 0.9)[1] for k, E0 in past_E.items()]
        out.append(f"prior {pn}: X {100*min(x):.0f}-{100*max(x):.0f}%, Y {100*min(y):.0f}-{100*max(y):.0f}%, believed rate (mean) {100*min(rm):.1f}-{100*max(rm):.1f}%")
    print(f"   m {m}: " + " | ".join(out))

print("\n(2) S2 intervals (exact binomial, 95%), per 1,000 star-sectors; mark 8")
for k, n, lab in ((115, 13412, "pooled"), (32, 3425, "G3"), (83, 9987, "pooled minus G3 (115-32 in 13,412-3,425)")):
    lo, hi = stats.beta.ppf(0.025, k, n - k + 1), stats.beta.ppf(0.975, k + 1, n - k)
    p_ge = stats.binom.sf(k - 1, n, 0.008)
    print(f"   {lab}: {k} in {n} = {1000*k/n:.2f} ({1000*lo:.2f} to {1000*hi:.2f}); chance of {k} or more if the true rate is exactly 8: {p_ge:.3f}")
print("   Note: star-sectors of one star are not independent (the G3 note gives a star-level ratio with the 25 heaviest stars), so the true interval is wider than binomial.")
