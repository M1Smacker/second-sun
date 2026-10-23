import sys, types, numpy as np
sys.modules['lightkurve'] = types.ModuleType('lightkurve')
sys.path.insert(0, '/home/claude/second-sun/pipeline')
import detect_v2 as d
rng = np.random.default_rng(5)
starts = [1683, 1711, 2390, 2419, 2743, 2770, 2797, 3311, 3338, 3474, 3502, 3529]
t = np.concatenate([np.arange(s, s+25, 200/86400) for s in starts])
def run(P, dP, dur_h, d1, d2, sep, noise, label):
    f = 1 + rng.normal(0, noise, t.size)
    Pt = P + dP; T0 = 1690.3
    ine = np.zeros(t.size, bool)
    for dep, off in ((d1, 0), (d2, sep)):
        ph = ((t - T0 - off*Pt + Pt/2) % Pt) - Pt/2
        m = np.abs(ph) < dur_h/48; f[m] -= dep; ine |= m
    keep, runs = d.eclipse_mask_auto(t, f, P)
    leak = ine & keep
    ev = d.find_events(t[keep], f[keep]) if leak.sum() else []
    evl = [e for e in ev if np.any(np.abs(t[leak]-e['center']) < 0.3)]
    print(f"{label}: unmasked in-eclipse points {int(leak.sum())}/{int(ine.sum())}; SNR>=7 events caused by leakage: {len(evl)} {[(round(e['center'],2),e['dur_h'],round(e['snr'],1)) for e in evl[:3]]}")
run(12, 0, 5, 0.05, 0.002, 0.5, 800e-6, "P12 bright, shallow 0.2% secondary")
run(12, 0, 5, 0.05, 0.002, 0.5, 3000e-6, "P12 faint (3000 ppm/200s), 0.2% secondary")
run(12, 0, 5, 0.05, 0.003, 0.37, 3000e-6, "P12 faint, eccentric 0.3% secondary at phase 0.37")
run(12, 0.0005, 5, 0.05, 0.01, 0.5, 800e-6, "P12, catalogue period off by 0.0005 d")
run(12, 0.002, 5, 0.05, 0.01, 0.5, 800e-6, "P12, catalogue period off by 0.002 d")
run(40, 0.005, 8, 0.05, 0.01, 0.5, 800e-6, "P40, catalogue period off by 0.005 d")
run(12, 0.01, 5, 0.05, 0.01, 0.5, 800e-6, "P12, catalogue period off by 0.01 d (1.5 d drift)")
run(5.5, 0.004, 4, 0.05, 0.01, 0.5, 800e-6, "P5.5, catalogue period off by 0.004 d")
# un-catalogued second binary (like KIC 4150611's 1.52 d signal dropped by the P>5 cut)
f = 1 + rng.normal(0, 800e-6, t.size)
for P, dur, dep in ((8.65, 5, 0.03), ):
    ph = ((t - 1690.3 + P/2) % P) - P/2; f[np.abs(ph) < dur/48] -= dep
P2=1.5223; ph2 = ((t - 1690.0 + P2/2) % P2) - P2/2; m2 = np.abs(ph2) < 2.5/48; f[m2] -= 0.004
keep, runs = d.eclipse_mask_auto(t, f, 8.65)
ev = d.find_events(t[keep], f[keep])
print("second (1.52 d, 0.4%) binary not in target list: events per star:", len(ev), "first:", [(round(e['center'],2),e['dur_h'],round(e['snr'],1)) for e in ev[:3]])
