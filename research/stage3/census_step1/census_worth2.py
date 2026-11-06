"""Census worth, recomputed 6 Nov 2026 with the transit chance of R0 Amendment 4 (outputs of t138_g_reach.py, main scenario F = 5.6, no dilution).
Replaces census_worth.py (which used the withdrawn per-star-width probe). Existing hunts = G2 development + G2 sealed + G3 (G1 left out as before: older Vesper, approximate table; it would add E 0.2 to 0.4).
Per G2-sealed star mean cell sums come from t138-g-reach.txt; a Census star with 3 or 6 sectors is worth ratio x a G2-sealed star (q2-pool-value.txt: 88.5 and 133.0 against 195.6). Armstrong 2014 central rate 10% (UNCERTAIN per-binary meaning). Arithmetic on earlier outputs; LIKELY at best."""
import numpy as np
past_E = {(1.5, "A"): 1.88, (1.5, "B"): 2.89, (1.8, "A"): 1.57, (1.8, "B"): 2.41, (2.2, "A"): 1.28, (2.2, "B"): 1.97}   # three hunts, E at 10%
per = {(1.5, "A"): 0.0163, (1.5, "B"): 0.0251, (1.8, "A"): 0.0136, (1.8, "B"): 0.0209, (2.2, "A"): 0.0111, (2.2, "B"): 0.0171}  # per G2-sealed star
ratio = {3: 88.5 / 195.6, 6: 133.0 / 195.6}
for f in (1.5, 1.8, 2.2):
    for rule in "AB":
        E0 = past_E[(f, rule)]; p = per[(f, rule)]
        print(f"\nf {f}, rule {rule}: existing hunts E {E0:.2f} (sum {E0/0.1:.1f}); per G2-sealed star {p:.4f}; stars of the G2-sealed kind alone for a 10% ceiling: {3/(0.10*p):.0f}, for 5%: {3/(0.05*p):.0f}")
        for sec in (3, 6):
            for N in (1400, 3000, 6000):
                sc = N * p * ratio[sec]; tot = E0 + 0.1 * sc
                print(f"   Census {N:5d} G2-type stars, {sec} sectors each: Census E {0.1*sc:5.2f} (adds {100*0.1*sc/E0:3.0f}% to the existing E); all hunts E {tot:5.2f}, chance of at least one {100*(1-np.exp(-tot)):3.0f}%, 95% ceiling on the total rate if none {100*0.3/tot:4.1f}%")
