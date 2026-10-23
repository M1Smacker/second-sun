"""Does eclipse_mask_auto catch eclipses of long-period binaries? Synthetic test, G1-like sector coverage."""
import sys, types, numpy as np
sys.modules['lightkurve'] = types.ModuleType('lightkurve')
sys.path.insert(0, '/home/claude/second-sun/pipeline')
import detect_v2 as d
rng = np.random.default_rng(3)
# sector start times (BTJD, approx, 26 d each) for a typical Kepler-field star: S14,15,40,41,53,54,55,74,75,80,81,82
starts = [1683, 1711, 2390, 2419, 2743, 2770, 2797, 3311, 3338, 3474, 3502, 3529]
t = np.concatenate([np.arange(s, s+25, 200/86400) for s in starts])
for P, dur_h, depth in [(12, 5, 0.05), (60, 9, 0.05), (150, 10, 0.05), (300, 12, 0.05), (150, 10, 0.01)]:
    f = 1 + rng.normal(0, 800e-6, t.size)
    T0 = 1690.3
    ph = ((t - T0 + P/2) % P) - P/2
    ine = np.abs(ph) < dur_h/48
    f[ine] -= depth
    keep, runs = d.eclipse_mask_auto(t, f, P)
    n_ecl = len(np.unique(np.round((t[ine]-T0)/P)))
    print(f"P={P:4} d, {dur_h} h, {depth*100:.0f}%: eclipses in data {n_ecl}; in-eclipse points left UNMASKED: {int((ine & keep).sum())} of {int(ine.sum())}; runs {[(round(a,4),round(b,4)) for a,b in runs]}")
    if (ine & keep).sum():
        ev = d.find_events(t[keep], f[keep])
        print("   events from leaked eclipse points:", [(round(e['center'],2), e['dur_h'], round(e['snr'],1)) for e in ev[:4]])
