"""Census worth, FORWARD-LOOKING version (8 Nov 2026). Written after the outside review (research/handoff-2026-11-07, WO-1).
census_worth2.py counted the three finished null hunts (G2 development, G2 sealed, G3) inside 'chance of at least one'. They are finished and found nothing, so for the future only Census counts, and the nulls pull the believed rate down.
Inputs are the same outputs as census_worth2.py (t138_g_reach.py main scenario, Amendment 4). Nothing here changes a search setting.
Method (reviewer's, re-derived here): rate r on a grid; prior A lognormal, median 10%, factor-2 spread (Kepler-like); prior B log-uniform 1% to 20% (broad).
Likelihood of the null from the three hunts = exp(-c * E0 * r / 0.1), c = 0.9 or 1.0 (FIX 28: quoted completeness about 3 points, about 10% relative, generous).
Forecast for Census = posterior mean of 1 - exp(-c * Ec * r / 0.1). Also printed: Census alone at exactly 10% with no null update, and the old all-hunts number for comparison.
Labels: arithmetic on earlier outputs; the priors are a choice, not data (UNCERTAIN). The ceilings in census_worth2 are unchanged and correct as a combined limit."""
import numpy as np

past_E = {(1.5, "A"): 1.88, (1.5, "B"): 2.89, (1.8, "A"): 1.57, (1.8, "B"): 2.41, (2.2, "A"): 1.28, (2.2, "B"): 1.97}
per = {(1.5, "A"): 0.0163, (1.5, "B"): 0.0251, (1.8, "A"): 0.0136, (1.8, "B"): 0.0209, (2.2, "A"): 0.0111, (2.2, "B"): 0.0171}
ratio = 88.5 / 195.6          # a 3-sector Census star vs a G2-sealed star
r = np.logspace(-3, np.log10(0.4), 4000)
w = np.gradient(np.log(r))
priors = {"A Kepler-like (lognormal, median 10%, x2)": np.exp(-0.5 * (np.log(r / 0.10) / np.log(2)) ** 2),
          "B broad (log-uniform 1% to 20%)": ((r >= 0.01) & (r <= 0.20)).astype(float)}


def forward(E0, Ec, p, c):
    post = p * np.exp(-c * E0 * r / 0.1) * w
    post /= post.sum()
    P = (post * (1 - np.exp(-c * Ec * r / 0.1))).sum()
    med = r[np.searchsorted(np.cumsum(post), 0.5)]
    return P, med


for c in (0.9, 1.0):
    print(f"\n=== completeness factor c = {c} ({'FIX 28 trim' if c < 1 else 'as quoted'}) ===")
    for (f, rule), E0 in sorted(past_E.items()):
        for N in (1400, 3000):
            Ec = 0.1 * N * per[(f, rule)] * ratio
            old = 1 - np.exp(-(E0 + Ec))
            naive = 1 - np.exp(-Ec)
            line = f"f {f} rule {rule} N {N}: E0 {E0:.2f} Census E {Ec:.2f} | old all-hunts {100*old:3.0f}% | Census alone at 10%, no update {100*naive:3.0f}%"
            for pn, p in priors.items():
                P, med = forward(E0, Ec, p, c)
                line += f" | {pn[:1]}: {100*P:3.0f}% (rate median {100*med:.1f}%)"
            print(line)

print("\n=== sensitivity: add G1 (about E 0.3 to the existing hunts, approximate), c 0.9 ===")
for (f, rule) in ((2.2, "A"), (1.8, "A"), (1.5, "B")):
    for N in (1400, 3000):
        E0 = past_E[(f, rule)] + 0.3
        Ec = 0.1 * N * per[(f, rule)] * ratio
        s = " | ".join(f"{pn[:1]}: {100*forward(E0, Ec, p, 0.9)[0]:3.0f}%" for pn, p in priors.items())
        print(f"f {f} rule {rule} N {N}: {s}")
