"""P-01c (Fable audit): F-01 on REAL light, counts only. G2 SPOC 2-min files (no windows needed), random sample per binary-period bin (seed 1).
For each file: load() as Petrova does; pick a time in the out-of-eclipse data (after the pipeline's own mask, so both arms of the test use a time the search keeps);
inject an 8 h box dip of K x the 8 h noise (a) BEFORE the mask (what a real planet does) and (b) AFTER the mask (what every recovery test does);
search with find_events on the v5 grid at SNR 7. Reports found share for (a) and (b), and the share of the dip's cadences the mask removed in (a).
Usage: python p01c_real_light_premask_injection.py [files_per_bin]"""
import sys, warnings
sys.path.insert(0, r"D:\second-sun\pipeline")
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import detect_v2 as D
from audit_paths import noise

GRID = (3, 4, 5, 6.5, 8, 10, 12, 15, 20)
n_per = int(sys.argv[1]) if len(sys.argv) > 1 else 25
tg = pd.read_csv(r"D:\second-sun\targets\g2_chain_targets.csv", comment="#").drop_duplicates("tic")
P = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
man = pd.read_csv(r"D:\second-sun\data\g2\manifest.csv").drop_duplicates("file")
man = man[(man.author == "SPOC") & man.tic.isin(P)]
man["P"] = man.tic.map(P)
rng = np.random.default_rng(1)
print(f"files per period bin: {n_per}; dip 8 h; columns: K | found when injected BEFORE the mask | found when injected AFTER the mask | share of dip cadences cut")
for lo, hi in ((5, 10), (10, 14), (14, 20), (20, 27.4), (27.4, 1e4)):
    sub = man[(man.P >= lo) & (man.P < hi)]
    pick = sub.sample(n=min(n_per, len(sub)), random_state=1)
    res = {12: [], 25: []}
    for r in pick.itertuples():
        try:
            t, f, _ = D.load(r.path)
            keep0, _ = D.eclipse_mask_auto(t, f, r.P)
            n8 = noise(t[keep0], f[keep0], 8.0)
            if not np.isfinite(n8) or keep0.sum() < 2000:
                continue
            tk = t[keep0]
            ok = [x for x in rng.choice(tk, 60) if x - tk.min() > 1.5 and tk.max() - x > 1.5 and np.sum(np.abs(tk - x) < 4 / 24) > 0.9 * 240]
            if not ok:
                continue
            tc = ok[0]
            for K in res:
                depth = K * n8 * 1e-6
                intr = np.abs(t - tc) < 4 / 24
                fa = f.copy(); fa[intr] -= depth                          # (a) before the mask
                ka, _ = D.eclipse_mask_auto(t, fa, r.P)
                cut = 1 - ka[intr].mean()
                found_a = any(abs(e["center"] - tc) < 0.3 for e in D.find_events(t[ka], fa[ka], durs_h=GRID))
                fb = f[keep0].copy(); fb[np.abs(tk - tc) < 4 / 24] -= depth  # (b) after the mask
                found_b = any(abs(e["center"] - tc) < 0.3 for e in D.find_events(tk, fb, durs_h=GRID))
                res[K].append((found_a, found_b, cut))
        except Exception as e:
            continue
    for K, v in res.items():
        a = np.array(v, float)
        if len(a):
            print(f"P {lo:>5} to {hi:<6}: K {K:2d} | before {a[:,0].mean():.2f} | after {a[:,1].mean():.2f} | cut {a[:,2].mean():.2f} | files {len(a)} of {len(sub)} in bin", flush=True)
