"""Compass checks on the vetting-page research brief (2026-10-24). Everything here is pure arithmetic or a small simulation."""
import numpy as np
from scipy.stats import norm, binom

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); m = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - m) / d, (c + m) / d

print("== 1. Wilson intervals quoted in the brief (section 5.4)")
for k, n in [(16, 20), (18, 20), (45, 50), (90, 100)]:
    lo, hi = wilson(k, n); print(f"  {k}/{n}: {lo:.2f} to {hi:.2f}")

print("== 2. d-prime and criterion examples (section 5.3), and the zero-count problem")
def dprime(H, F): return norm.ppf(H) - norm.ppf(F), -(norm.ppf(H) + norm.ppf(F)) / 2
for H, F in [(0.8, 0.1), (0.9, 0.3)]:
    d, c = dprime(H, F); print(f"  H={H} F={F}: d'={d:.2f} c={c:.2f}")
with np.errstate(all="ignore"):
    print("  H=1.0 or F=0.0 ->", dprime(1.0, 0.1)[0], dprime(0.8, 0.0)[0], "(infinite: needs the log-linear correction, add 0.5 to each count)")
H = (17 + .5) / (20 + 1); F = (0 + .5) / (16 + 1); print(f"  corrected, 17/20 hits and 0/16 false alarms: d'={dprime(H, F)[0]:.2f}")

print("== 3. How easily does the CURRENT pass line (>=85% clear found, <=10% quiet called dip, min 60 curves) pass by luck?")
# first two test rounds: 20 clear dips, 16 quiet curves.  Meets = hits/20 >= .85 and falsealarms/16 <= .10  -> hits>=17, FA<=1
for ph, pf in [(0.95, 0.05), (0.90, 0.08), (0.80, 0.12), (0.75, 0.12), (0.70, 0.20), (0.60, 0.25)]:
    pass2 = (1 - binom.cdf(16, 20, ph)) * binom.cdf(1, 16, pf)
    print(f"  true hit {ph:.0%}, true false-alarm {pf:.0%}: chance the first two rounds 'meet the line' = {pass2:.0%}")
rng = np.random.default_rng(1)
def ever(ph, pf, rounds=6, trials=20000):
    ok = 0
    for _ in range(trials):
        h = f = 0
        for r in range(1, rounds + 1):
            h += rng.binomial(10, ph); f += rng.binomial(8, pf)
            if r >= 2 and h / (10 * r) >= .85 and f / (8 * r) <= .10: ok += 1; break
    return ok / trials
for ph, pf in [(0.75, 0.12), (0.70, 0.20)]:
    print(f"  true hit {ph:.0%}, FA {pf:.0%}: chance of 'meets the line' at least once in rounds 2..6 (looking after every round) = {ever(ph, pf):.0%}")

print("== 4. Lineup selection effect: random null windows vs flipped-style nulls")
# a sector of white noise, matched-filter dip statistic over 36 bins (6 h at 10 min)
N, WIN, BOX = 3900, 216, 36
def box_stat(x):                       # strongest box dip in a series, in sigma of the box mean
    c = np.cumsum(np.insert(x, 0, 0)); m = (c[BOX:] - c[:-BOX]) / BOX
    return (-m / (1 / np.sqrt(BOX))).max(), int(np.argmin(m))
def trial(proper):
    sector = rng.standard_normal(N); s, i = box_stat(sector)
    i0 = int(np.clip(i - WIN // 2, 0, N - WIN)); event = sector[i0:i0 + WIN]   # the event window = wherever the search found its biggest dip
    nulls = []
    for _ in range(4):
        other = rng.standard_normal(N)
        if proper:                                                              # same selection applied to a null series
            _, j = box_stat(other); j0 = int(np.clip(j - WIN // 2, 0, N - WIN)); nulls.append(other[j0:j0 + WIN])
        else:                                                                    # a random stretch of a null series
            j0 = rng.integers(0, N - WIN); nulls.append(other[j0:j0 + WIN])
    scores = [box_stat(w)[0] for w in [event] + nulls]
    return int(np.argmax(scores) == 0)
for proper in (False, True):
    r = np.mean([trial(proper) for _ in range(4000)])
    print(f"  {'nulls chosen like the event' if proper else 'nulls are random stretches'}: an ideal observer picks the 'real' window in {r:.0%} of 4000 pure-noise lineups (chance = 20%)")

print("== 5. Prevalence: the official test and the brief's planned mix")
print("  official test dips: 14 of 30 =", f"{14/30:.0%}", "; a real queue: a handful of true planets among hundreds of events")
