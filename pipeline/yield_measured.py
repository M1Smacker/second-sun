"""Expected number of NEW detectable transiting circumbinary planets in G1, using each star's MEASURED noise from the Stage 1
audit instead of an assumed red-noise factor. Adapted from the outside review's yield.py (research/deep-review-2026-10-23/author-scripts/yield.py,
MIT, by the research Claude); inputs, logic and the precession table are theirs, so every number can be compared with section 4.3 of the review.
Per star and sector the noise at 3, 6.5 and 15 h comes from audit_all.csv (best usable product); other durations are interpolated in log-log.
Usage: python yield_measured.py"""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
OUT = r"D:\second-sun\research\audit-2026-10-23"
#            Tprec  f_prim  E     depth%  dur_d(lo,hi)  Pp(d)       (Martin 2017 Table 2; Davies et al. 2026 Table 2; periods standard)
SYS = {'K16': (41.4, .425, 0.9, 1.80, (.31, .43), 228.8), 'K34': (69.3, .169, 3.4, 0.28, (.16, .47), 288.8),
       'K35': (19.8, .360, 0.8, 0.40, (.18, .49), 131.4), 'K47c': (539.1, .197, 3.9, 0.17, (.18, .47), 303.2),
       'K64': (35.4, .284, 1.5, 0.11, (.45, .51), 138.5), 'K413': (11.1, .235, 0.7, 0.17, (.12, .39), 66.3),
       'K453': (102.9, .105, 6.0, 0.50, (.29, .57), 240.5), 'K1647': (7188.7, .070, 13.2, 0.22, (.2, .37), 1107.6)}
SECT = {14: (2019.545, 2019.619), 15: (2019.622, 2019.693), 16: (2019.697, 2019.764), 19: (2019.909, 2019.977), 26: (2020.437, 2020.505),
        40: (2021.477, 2021.557), 41: (2021.557, 2021.633), 53: (2022.447, 2022.518), 54: (2022.518, 2022.592), 55: (2022.592, 2022.666),
        56: (2022.666, 2022.748), 60: (2022.975, 2023.047), 73: (2023.934, 2024.008), 74: (2024.008, 2024.082), 75: (2024.082, 2024.156),
        76: (2024.156, 2024.235), 78: (2024.311, 2024.386), 80: (2024.462, 2024.536), 81: (2024.536, 2024.608), 82: (2024.608, 2024.679),
        83: (2024.679, 2024.751), 86: (2024.89, 2024.964)}
KEP, TESS = (2009.37, 2013.36), (2019.54, 2024.97)

best = pd.read_csv(rf"{OUT}\best_per_star_sector.csv")
stars = pd.read_csv(r"D:\second-sun\targets\g1_coverage.csv").tic.tolist()
noise = {}                                       # tic -> {sector: (n3, n6.5, n15)}
for tic, sec, n3, n65, n15 in zip(best.tic, best.sector, best["noise_3h_ppm"], best["noise_6.5h_ppm"], best["noise_15h_ppm"]):
    noise.setdefault(tic, {})[int(sec)] = (n3, n65, n15)
xs = np.log([3, 6.5, 15])
def noise_at(tic, sec, D_h):
    n = np.array(noise[tic][sec], float)
    return np.exp(np.interp(np.log(D_h), xs, np.log(n))) if np.isfinite(n).all() else np.inf


def run(rscale=1.0, ptrans=0.7, snr=7.0, nmc=4000, frac_g1=0.433):
    tot, rows = 0, []
    for k, (Tp, f, E, dep, dur, Pp) in SYS.items():
        w = f * Tp / 2; hits = n = 0
        for _ in range(nmc):
            ph = rng.uniform(0, Tp); st = np.array([ph, ph + Tp / 2]); st = np.r_[st - Tp, st, st + Tp] + 1990
            win = [(s, s + w) for s in st]
            ov = lambda a, b: any(s < b and e > a for s, e in win)
            if ov(*KEP):
                continue
            n += 1
            if not ov(*TESS):
                continue
            tic = stars[int(rng.integers(len(stars)))]
            secs = {s: SECT[s] for s in noise.get(tic, {}) if s in SECT}
            if not secs:
                continue
            t0 = rng.uniform(0, Pp / 365.25); D = rng.uniform(*dur) * 24 * rscale; d = dep / 100 / rscale**2
            seen = 0
            for tc in np.arange(TESS[0] - 1 + t0, TESS[1] + 1, Pp / 365.25):
                for s, (a0, b0) in secs.items():
                    if a0 <= tc <= b0 and any(x <= tc <= y for x, y in win):
                        if rng.random() < ptrans and d * 1e6 / noise_at(tic, s, D) >= snr:
                            seen += 1
            hits += seen > 0
        p = hits / max(n, 1); exp = E * frac_g1 * p; tot += exp; rows.append((k, E, round(p, 4), round(exp, 3)))
    return tot, rows


def parity(beta):
    """Fill `noise` the way the review did (Stassun et al. white noise x beta, QLP sectors of every star) to check this code against theirs."""
    c = [3.29685004771, 0.850021465753, -0.285041632435, 0.0395908321369, -0.0022308015894, 4.73508403525e-5]
    sig = lambda T: np.exp(sum(ci * T**i for i, ci in enumerate(c)))
    cov = pd.read_csv(r"D:\second-sun\targets\g1_coverage.csv")
    tm = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#").drop_duplicates("tic").set_index("tic").tmag
    noise.clear()
    for tic, qs in zip(cov.tic, cov.qlp_sectors):
        s = beta * sig(tm[tic])
        noise[tic] = {int(float(x)): (s / np.sqrt(3), s / np.sqrt(6.5), s / np.sqrt(15)) for x in str(qs).split()}


if __name__ == "__main__":
    import sys
    if "parity" in sys.argv:
        for beta in (1.0, 1.4):
            parity(beta); tot, rows = run(rscale=1.0)
            print(f"PARITY with the review's assumptions, beta {beta}: raw {tot:.2f} (review reported 0.47 to 0.71 over its settings)", rows[:3])
        raise SystemExit
    for rs in (1.0, 1.3):
        tot, rows = run(rscale=rs)
        lam = tot * 0.7 - 0.5 * 0.7 * rows[0][3]                    # vetting x0.7; the Kepler-16-like term halved (likely seen by eye already)
        print(f"hosts {rs}x the Kepler hosts: raw expected detectable switch-ons {tot:.2f} (review: 0.47 to 0.71)")
        print("   ", rows)
        print(f"    after vetting x0.7 and halving the Kepler-16 term: lambda {lam:.2f} -> P(at least one) {100 * (1 - np.exp(-lam)):.0f}%")
