"""Does the catalogue-ephemeris drift term make Petrova's eclipse windows cover most of the orbit at TESS times?"""
import os, sys, json, glob, numpy as np
os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1")
sys.path.insert(0, os.path.abspath("pipeline"))
import petrova_mask as PM
C = PM.cat()
print("catalogue stars:", len(C))
rows = []
for tic, c in C.items():
    if not np.isfinite(c.get("wp", np.nan)): continue
    P, T0 = c["P"], c["T0"]
    eT0 = c["eT0"] if np.isfinite(c.get("eT0", np.nan)) else 0.0; eP = c["eP"] if np.isfinite(c.get("eP", np.nan)) else 0.0
    for t in (1500.0, 2500.0, 3500.0):
        n = abs(np.round((t - T0) / P))
        drift = 3 * np.sqrt(eT0**2 + (n * eP)**2)
        sec_ok = np.isfinite(c["phs"]) and np.isfinite(c["ws"]); ws = c["ws"] if sec_ok else c["wp"]
        cover = min(1.0, (PM.PADF * c["wp"] + 2 * drift) / P) + min(1.0, (PM.PADF * ws + 2 * drift) / P)
        rows.append((int(tic), t, P, c["wp"], eP, eT0, drift, min(cover, 1.0), PM.PADF * c["wp"] / P + PM.PADF * ws / P))
r = np.array(rows, float)
for t in (1500, 2500, 3500):
    m = r[:, 1] == t
    x = r[m]
    print(f"t={t} BTJD: stars {m.sum()}; window share of orbit median {np.median(x[:,7]):.3f}, share of stars with windows over 50% of orbit {np.mean(x[:,7]>0.5):.3f}, over 90% {np.mean(x[:,7]>0.9):.3f}; width-only share median {np.median(x[:,8]):.3f}; drift median {np.median(x[:,6]):.3f} d, 90th pct {np.percentile(x[:,6],90):.2f} d")
x = r[r[:,1]==3500]
for lo, hi in ((0,7.5),(7.5,15),(15,30),(30,1e9)):
    k = (x[:,2]>=lo)&(x[:,2]<hi)
    if k.sum(): print(f"  t=3500, P {lo}-{hi}: n={k.sum()} cover median {np.median(x[k,7]):.2f}, over 50%: {np.mean(x[k,7]>0.5):.2f}, eP median {np.median(x[k,4]):.2e} d")
worst = x[np.argsort(-x[:,6])][:5]
print("largest drift at t=3500 (tic, P, wp, eP, eT0, drift d, cover):"); [print("  ", int(w[0]), round(w[2],3), round(w[3],3), w[4], w[5], round(w[6],2), round(w[7],2)) for w in worst]
