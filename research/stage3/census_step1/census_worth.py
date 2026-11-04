"""Is a Census of N G2-type stars worth it? Combines (a) Horizon-with-geometry sums per G2-sealed star from t138-geometry-probe.txt, (b) the value ratio of a 3 or 6 sector star against the G2 sealed set (q2-pool-value.txt: 88.5, 133.0, against 195.6 per 1,000 stars),
(c) the existing hunts' sums with geometry. Armstrong 2014 central rate 10%. Arithmetic on earlier outputs; LIKELY at best."""
import numpy as np
# mean cell sums WITH geometry from t138-geometry-probe.txt (rule A = all 30 cells, rule B = 15 stable cells), per R_sum factor
sealed = {1.5: {"A": 10.8, "B": 17.8}, 1.8: {"A": 7.5, "B": 12.8}}
dev    = {1.5: {"A": 4.6, "B": 7.6},   1.8: {"A": 3.3, "B": 5.5}}
g3     = {1.5: {"A": 7.1, "B": 11.0},  1.8: {"A": 1.8, "B": 2.8}}
ratio = {3: 88.5 / 195.6, 6: 133.0 / 195.6}
for f in (1.5, 1.8):
    for rule in "AB":
        past = sealed[f][rule] + dev[f][rule] + g3[f][rule]
        per = sealed[f][rule] / 594
        print(f"\nR_sum {f} x R_A, rule {rule}: existing hunts sum {past:.1f} (E at 10% = {0.1*past:.2f}); per G2-sealed star {per:.4f}")
        for sec in (3, 6):
            for N in (1400, 3000, 6000):
                sc = N * per * ratio[sec]
                tot = past + sc
                print(f"   Census {N:5d} G2-type stars, {sec} sectors each: Census sum {sc:6.1f}, E {0.1*sc:5.2f}; all hunts E {0.1*tot:5.2f}, chance of at least one {100*(1-np.exp(-0.1*tot)):3.0f}%, 95% ceiling on the total rate if none {100*3/tot:4.1f}%")
