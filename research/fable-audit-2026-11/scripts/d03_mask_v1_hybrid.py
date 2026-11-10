"""D-03 (Fable, 10 Nov 2026): Amendment A prototype. d02 showed the POOLED fold recovers planted dips but leaks on the real arm in every period bin (real over upside-down about 1.5 to 2.3 outside the lane),
because a fold over several years smears eclipses that the frozen per-sector fold catches. Hybrid rule tested here:
  1. Per sector, find low runs EXACTLY as the frozen mask does (detect_v2.eclipse_mask_auto).
  2. For every run and every binary cycle in that sector: the run is "low in that cycle" if the cycle has 3 or more points in the run and their median is below m0 - max(2 sig, 0.3 x run depth) (m0, sig from the
     sector's 600 folded bin medians, as the frozen code). Each such (sector, cycle) is one EPISODE at the run's phase.
  3. A run is a CONFIRMED eclipse if at least 2 episodes, in any sectors of the star, lie within phase tolerance (the larger run width + 0.02) of it. Confirmed runs are masked with the frozen padding (1.5 widths).
  4. An unconfirmed run is not masked: single-visit lane (events centred in it are counted apart).
  5. Upside-down arm: light kept by the confirmed real runs AND by confirmed runs of the same procedure on the flipped light; its lane = unconfirmed flipped runs.
Same test as d02 (G2 SPOC 2-min, seed 3 so the same stars). Scratch only, counts only.
Usage: python d03_mask_v1_hybrid.py [stars_per_bin] [max_sectors]"""
import sys, warnings
sys.path.insert(0, r"D:\second-sun\pipeline")
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from wotan import flatten
import detect_v2 as D
from audit_paths import noise
from d01_mask_v1_prototype import GRID, ev

NB, TOL = 600, 0.02


def pdist(a, b):
    return abs(((a - b + 0.5) % 1.0) - 0.5)


def in_run(ph, a, b):
    m = np.zeros_like(ph, bool)
    for sh in (-1, 0, 1):
        m |= (ph >= a + sh) & (ph <= b + sh)
    return m


def sector_runs(t, f, P):
    """Frozen runs of one sector plus, per run, the list of cycles in which it is low."""
    _, runs = D.eclipse_mask_auto(t, f, P)
    flat = flatten(t, f, method="biweight", window_length=2.0); ok = np.isfinite(flat)
    ph = (t % P) / P; cyc = np.floor(t / P).astype(int)
    k = np.clip(np.digitize(ph, np.linspace(0, 1, NB + 1)) - 1, 0, NB - 1)
    med = np.array([np.median(flat[ok & (k == i)]) if np.any(ok & (k == i)) else np.nan for i in range(NB)])
    m0 = np.nanmedian(med); sig = 1.4826 * np.nanmedian(np.abs(med - m0))
    out = []
    for a, b in runs:
        sel = in_run(ph, a, b) & ok
        if not sel.any():
            continue
        depth = m0 - np.median(flat[sel]); n_low = 0
        for c in np.unique(cyc[sel]):
            p = flat[sel & (cyc == c)]
            if len(p) >= 3 and np.median(p) < m0 - max(2 * sig, 0.3 * depth):
                n_low += 1
        out.append(dict(a=a, b=b, c=((a + b) / 2) % 1.0, w=b - a, n_low=n_low))
    return out


def confirm(all_runs):
    """all_runs: list (per sector) of run lists. Marks each run confirmed if 2 or more episodes lie within tolerance."""
    flat = [r for rs in all_runs for r in rs]
    for r in flat:
        r["conf"] = sum(o["n_low"] for o in flat if pdist(o["c"], r["c"]) <= max(o["w"], r["w"]) + TOL) >= 2
    return all_runs


def keep_of(t, P, runs, pad=1.5):
    ph = (t % P) / P; keep = np.ones_like(t, bool)
    for r in runs:
        if r["conf"]:
            keep &= ~in_run(ph, r["a"] - pad * r["w"], r["b"] + pad * r["w"])
    return keep


def lane_hit(center, P, runs):
    ph = (center % P) / P
    return any((not r["conf"]) and pdist(ph, r["c"]) <= r["w"] / 2 + 2 / NB for r in runs)


if __name__ == "__main__":
    n_per = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    max_sec = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    tg = pd.read_csv(r"D:\second-sun\targets\g2_chain_targets.csv", comment="#").drop_duplicates("tic").set_index("tic")
    man = pd.read_csv(r"D:\second-sun\data\g2\manifest.csv").drop_duplicates("file")
    man = man[(man.author == "SPOC") & man.tic.isin(tg.index)]
    cnt = man.groupby("tic").size(); stars = pd.DataFrame(dict(tic=cnt.index, n=cnt.values)); stars["P"] = stars.tic.map(tg.p_bin_d); stars = stars[stars.n >= 3]
    rng = np.random.default_rng(3)
    print(f"HYBRID rule. stars per bin {n_per}, up to {max_sec} sectors, seed 3. Events per star-sector, real/upside-down.")
    print("A frozen | A hybrid outside the lane | A hybrid lane only | runs per star: frozen total -> unconfirmed | data kept frozen, hybrid")
    print("B planted 8 h dip before the mask: K12 found frozen / hybrid (share of hybrid finds in the lane); same for K25")
    for lo, hi in ((5, 10), (10, 14), (14, 20), (20, 27.4), (27.4, 1e4)):
        sub = stars[(stars.P >= lo) & (stars.P < hi)]
        pick = sub.sample(n=min(n_per, len(sub)), random_state=3)
        A = dict(ss=0, fr=0, ff=0, nr=0, nf=0, lr=0, lf=0, runs=0, unc=0, stars=0, kf=0.0, kh=0.0); B = {12: [], 25: []}
        for s in pick.itertuples():
            try:
                P = float(s.P); paths = man[man.tic == s.tic].path.tolist()[:max_sec]
                L = [D.load(p) for p in paths]; ts = [x[0] for x in L]; fs = [x[1] for x in L]
                R = confirm([sector_runs(t, f, P) for t, f in zip(ts, fs)])
                M = confirm([sector_runs(t, 2 - f, P) for t, f in zip(ts, fs)])
                A["stars"] += 1; A["runs"] += sum(len(r) for r in R); A["unc"] += sum(1 for rs in R for r in rs if not r["conf"])
                for t, f, rr, mm in zip(ts, fs, R, M):
                    k0, _ = D.eclipse_mask_auto(t, f, P); kh = keep_of(t, P, rr); kk = kh & keep_of(t, P, mm)
                    A["ss"] += 1; A["kf"] += k0.mean(); A["kh"] += kh.mean()
                    A["fr"] += len(ev(t[k0], f[k0])); A["ff"] += len(ev(t[k0], 2 - f[k0]))
                    for e in ev(t[kh], f[kh]):
                        A["lr" if lane_hit(e["center"], P, rr) else "nr"] += 1
                    for e in ev(t[kk], 2 - f[kk]):
                        A["lf" if lane_hit(e["center"], P, mm) else "nf"] += 1
                j = int(rng.integers(len(ts))); t, f = ts[j], fs[j]
                k0, _ = D.eclipse_mask_auto(t, f, P); tk = t[k0]; n8 = noise(tk, f[k0], 8.0)
                okc = [x for x in rng.choice(tk, 80) if x - tk.min() > 1.5 and tk.max() - x > 1.5 and np.sum(np.abs(tk - x) < 4 / 24) > 0.9 * 240]
                if not okc or not np.isfinite(n8):
                    continue
                tc = okc[0]; intr = np.abs(t - tc) < 4 / 24
                for K in B:
                    fa = f.copy(); fa[intr] -= K * n8 * 1e-6
                    ka, _ = D.eclipse_mask_auto(t, fa, P)
                    f_fro = any(abs(e["center"] - tc) < 0.3 for e in ev(t[ka], fa[ka]))
                    R2 = [list(map(dict, rs)) for rs in R]; R2[j] = sector_runs(t, fa, P); confirm(R2)
                    k2 = keep_of(t, P, R2[j])
                    hit = [e for e in ev(t[k2], fa[k2]) if abs(e["center"] - tc) < 0.3]
                    B[K].append((f_fro, bool(hit), bool(hit) and lane_hit(hit[0]["center"], P, R2[j])))
            except Exception as ex:
                print("   skip one star:", type(ex).__name__, str(ex)[:60], flush=True)
        n = max(A["ss"], 1); ns = max(A["stars"], 1)
        line = (f"P {lo} to {hi}: stars {A['stars']}, star-sectors {A['ss']} | A frozen {A['fr']/n:.2f}/{A['ff']/n:.2f} | hybrid outside lane {A['nr']/n:.2f}/{A['nf']/n:.2f} | lane {A['lr']/n:.2f}/{A['lf']/n:.2f}"
                f" | runs per star {A['runs']/ns:.1f} -> unconfirmed {A['unc']/ns:.1f} | kept {A['kf']/n:.3f}, {A['kh']/n:.3f}")
        for K, v in B.items():
            a = np.array(v, float)
            if len(a):
                line += f" | B K{K}: {a[:,0].mean():.2f} / {a[:,1].mean():.2f} (lane share {a[:,2].sum()/max(a[:,1].sum(),1):.2f}, n={len(a)})"
        print(line, flush=True)
