"""P-01 (Fable audit): does detect_v2.eclipse_mask_auto cut planet dips out of slow binaries before the search?
Synthetic, no real data. White noise, 27.4 d of 2-min data with a 1 d mid-sector gap, a toy binary with box eclipses at period P.
A box dip (the "planet") is injected BEFORE masking at a random time outside the eclipses. Chain as in stage2_search.prepare/do_group:
mask_runs (eclipse_mask_auto per period) -> Prod(real) and Prod(flip) -> events at SNR >= 7 on the v5 grid.
Reported per binary period and injected strength: share of the dip's points the mask removes, share of dips found with the mask,
share found with a perfect mask (true eclipse phases only). The same for a BUMP of the same size read on the upside-down arm.
Usage: python p01_mask_eats_transits.py [n_trials]"""
import sys, warnings
sys.path.insert(0, r"D:\second-sun\pipeline")
warnings.filterwarnings("ignore")
import numpy as np
import detect_v2 as D

GRID = (3, 4, 5, 6.5, 8, 10, 12, 15, 20)
SIG = 1000e-6            # per 2-min point
DUR_H = 8.0


def events(t, f):
    return D.find_events(t, f, thr=7.0, durs_h=GRID)


def make(P, rng):
    t = np.arange(0, 27.4, 2 / 1440)
    t = t[(t < 13.2) | (t > 14.2)]
    f = 1 + rng.normal(0, SIG, t.size)
    t0 = rng.uniform(0, P)
    w1 = 0.15 * (P / 10) ** (1 / 3)                      # eclipse length in days, grows slowly with period
    ph = ((t - t0 + P / 2) % P) - P / 2
    ph2 = ((t - t0 - 0.5 * P + P / 2) % P) - P / 2
    ecl = (np.abs(ph) < w1 / 2) | (np.abs(ph2) < w1 / 2)
    f[np.abs(ph) < w1 / 2] -= 0.10
    f[np.abs(ph2) < w1 / 2] -= 0.04
    return t, f, ecl, (t0, w1)


def trial(P, snr_target, sign, rng):
    t, f, ecl, (t0, w1) = make(P, rng)
    n_in = DUR_H * 30
    depth = snr_target * SIG / np.sqrt(n_in)
    for _ in range(200):                                  # a dip time well away from eclipses, gap and ends
        tc = rng.uniform(1.5, 25.9)
        if abs(tc - 13.7) < 1.5:
            continue
        d1 = abs(((tc - t0 + P / 2) % P) - P / 2); d2 = abs(((tc - t0 - 0.5 * P + P / 2) % P) - P / 2)
        if min(d1, d2) > 1.0:
            break
    else:
        return None
    intr = np.abs(t - tc) < DUR_H / 48
    f = f.copy(); f[intr] -= sign * depth
    keep, runs = D.eclipse_mask_auto(t, f, P)
    cut = 1 - keep[intr].mean()
    cut_all = 1 - keep[~ecl].mean()
    def found(tt, ff):
        ff = ff if sign == 1 else 2 - ff
        return any(abs(e["center"] - tc) < 0.3 for e in events(tt, ff))
    perfect = ~(np.abs(((t - t0 + P / 2) % P) - P / 2) < 1.5 * w1) & ~(np.abs(((t - t0 - 0.5 * P + P / 2) % P) - P / 2) < 1.5 * w1)
    return cut, found(t[keep], f[keep]), found(t[perfect], f[perfect]), cut_all


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    rng = np.random.default_rng(20261110)
    print(f"trials per cell: {n}; dip {DUR_H} h; columns: share of dip points cut by the mask | found with pipeline mask | found with perfect mask | out-of-eclipse data cut")
    for sign, name in ((1, "DIP on the real arm"), (-1, "BUMP on the upside-down arm")):
        print(f"\n== {name} ==")
        for P in (5.5, 7.5, 10, 14, 20, 30, 50):
            for s in (9, 12, 20):
                r = [x for x in (trial(P, s, sign, rng) for _ in range(n)) if x]
                a = np.array(r, float)
                print(f"P={P:5.1f} d  injected SNR {s:2d}:  cut {a[:,0].mean():.2f} | found {a[:,1].mean():.2f} | perfect {a[:,2].mean():.2f} | data cut {a[:,3].mean():.3f}  (n={len(r)})", flush=True)
