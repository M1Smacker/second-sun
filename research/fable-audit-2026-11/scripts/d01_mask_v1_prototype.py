"""D-01 (Fable fix step, 10 Nov 2026): PROTOTYPE of the Petrova 1.0 eclipse mask ("repeat rule"), tested against the frozen 0.8.1 mask on real G2 SPOC light.
Scratch only: imports the frozen pipeline read-only, changes nothing in it. Counts only.

Repeat rule (per STAR, all its sectors together; phase = (t % P) / P as in the frozen code):
  1. Per sector: flatten (biweight 2 d), as the frozen mask does. Pool all sectors.
  2. Per phase bin (600 bins): folded median over ALL cycles (m_fold), number of distinct cycles that visit the bin (nvis; a visit = at least 3 points), and the median per cycle.
     Robust centre m0 and scatter sig from the folded medians, as the frozen code.
  3. A bin is an ECLIPSE bin if m_fold < m0 - 4 sig AND
       nvis >= 3 (a median over 3 or more cycles is low only if it repeats), or
       nvis == 2 and BOTH cycles are low (each cycle's median < m0 - max(2 sig, 0.3 x the folded depth)).
     A low bin with nvis == 1, or with 2 visits of which one is not low, is NOT masked: it is recorded as a "single" bin (an unconfirmed dip: second eclipse or planet).
  4. Eclipse runs are padded by 1.5 x their own width, as the frozen code.
The upside-down arm applies the same rule to 2 - f (mirror), in addition to the real-orientation eclipse mask, so the arms stay exchangeable.

Test, per period bin, N stars with at least 3 SPOC 2-min sectors (first 6 used), seed 2:
  A. No injection: events at SNR 7 (v5 grid) per star-sector on the real arm and the upside-down arm, frozen mask vs repeat rule; share of data kept.
  B. An 8 h box dip of K x the 8 h noise injected BEFORE masking into one sector: found share, frozen vs repeat rule.
Usage: python d01_mask_v1_prototype.py [stars_per_bin]"""
import sys, warnings
sys.path.insert(0, r"D:\second-sun\pipeline")
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from wotan import flatten
import detect_v2 as D
from audit_paths import noise

GRID = (3, 4, 5, 6.5, 8, 10, 12, 15, 20)
NB, NSIG, PAD = 600, 4.0, 1.5


def runs_of(low):
    runs, i = [], 0
    while i < NB:
        if low[i]:
            j = i
            while j + 1 < NB and low[j + 1]:
                j += 1
            runs.append([i / NB, (j + 1) / NB]); i = j + 1
        else:
            i += 1
    if len(runs) > 1 and runs[0][0] == 0 and runs[-1][1] == 1:
        runs[0][0] = runs[-1][0] - 1; runs.pop()
    return runs


def repeat_mask(ts, fs, P, flats=None):
    """ts, fs: lists per sector. Returns (list of keep arrays per sector, number of single bins, flats)."""
    if flats is None:
        flats = [flatten(t, f, method="biweight", window_length=2.0) for t, f in zip(ts, fs)]
    t = np.concatenate(ts); fl = np.concatenate(flats); ok = np.isfinite(fl)
    ph = (t % P) / P; cyc = np.floor(t / P).astype(int); k = np.clip((ph * NB).astype(int), 0, NB - 1)
    df = pd.DataFrame(dict(k=k[ok], c=cyc[ok], v=fl[ok]))
    fold = df.groupby("k").v.median().reindex(range(NB))
    pc = df.groupby(["k", "c"]).v.agg(["median", "size"]).reset_index(); pc = pc[pc["size"] >= 3]
    m0 = np.nanmedian(fold.values); sig = 1.4826 * np.nanmedian(np.abs(fold.values - m0))
    lowf = np.nan_to_num(fold.values < m0 - NSIG * sig).astype(bool)
    nvis = pc.groupby("k").size().reindex(range(NB)).fillna(0).values
    ecl = np.zeros(NB, bool); single = 0
    by = {kk: g["median"].values for kk, g in pc.groupby("k")}
    for i in np.where(lowf)[0]:
        if nvis[i] >= 3:
            ecl[i] = True
        elif nvis[i] == 2:
            thr = m0 - max(2 * sig, 0.3 * (m0 - fold.values[i]))
            if np.all(by[i] < thr):
                ecl[i] = True
            else:
                single += 1
        else:
            single += 1
    keeps = []
    for tt in ts:
        p = (tt % P) / P; keep = np.ones_like(tt, bool)
        for a, b in runs_of(ecl):
            w = b - a; lo, hi = a - PAD * w, b + PAD * w
            for sh in (-1, 0, 1):
                keep &= ~((p >= lo + sh) & (p <= hi + sh))
        keeps.append(keep)
    return keeps, single, flats


def ev(t, f):
    return D.find_events(t, f, durs_h=GRID) if len(t) > 200 else []


if __name__ == "__main__":
    n_per = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    tg = pd.read_csv(r"D:\second-sun\targets\g2_chain_targets.csv", comment="#").drop_duplicates("tic")
    Pm = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
    man = pd.read_csv(r"D:\second-sun\data\g2\manifest.csv").drop_duplicates("file")
    man = man[(man.author == "SPOC") & man.tic.isin(Pm)]
    cnt = man.groupby("tic").size(); stars = pd.DataFrame(dict(tic=cnt.index, n=cnt.values)); stars["P"] = stars.tic.map(Pm); stars = stars[stars.n >= 3]
    rng = np.random.default_rng(2)
    print("columns A (no injection): events per star-sector real/upside-down, FROZEN mask | REPEAT rule (upside-down arm with the mirrored rule) | data kept frozen, repeat | single bins per star")
    print("columns B (8 h dip injected before the mask): K 12 found frozen / repeat ; K 25 found frozen / repeat")
    for lo, hi in ((5, 10), (10, 14), (14, 20), (20, 27.4), (27.4, 1e4)):
        sub = stars[(stars.P >= lo) & (stars.P < hi)]
        pick = sub.sample(n=min(n_per, len(sub)), random_state=2)
        A = dict(ss=0, fr=0, ff=0, rr=0, rf=0, kf=0.0, kr=0.0, single=0, stars=0); B = {12: [], 25: []}
        for s in pick.itertuples():
            try:
                paths = man[man.tic == s.tic].path.tolist()[:6]
                L = [D.load(p) for p in paths]; ts = [x[0] for x in L]; fs = [x[1] for x in L]; P = s.P
                keeps_r, single, flats = repeat_mask(ts, fs, P)
                keeps_m, _, _ = repeat_mask(ts, [2 - f for f in fs], P, flats=[2 - x for x in flats])          # mirrored rule on the upside-down light
                A["stars"] += 1; A["single"] += single
                for t, f, kr, km in zip(ts, fs, keeps_r, keeps_m):
                    k0, _ = D.eclipse_mask_auto(t, f, P)
                    A["ss"] += 1; A["kf"] += k0.mean(); A["kr"] += kr.mean()
                    A["fr"] += len(ev(t[k0], f[k0])); A["ff"] += len(ev(t[k0], 2 - f[k0]))
                    A["rr"] += len(ev(t[kr], f[kr])); kk = kr & km; A["rf"] += len(ev(t[kk], 2 - f[kk]))
                # B: inject into one sector
                j = int(rng.integers(len(ts))); t, f = ts[j], fs[j]
                k0, _ = D.eclipse_mask_auto(t, f, P); tk = t[k0]; n8 = noise(tk, f[k0], 8.0)
                okc = [x for x in rng.choice(tk, 80) if x - tk.min() > 1.5 and tk.max() - x > 1.5 and np.sum(np.abs(tk - x) < 4 / 24) > 0.9 * 240 and keeps_r[j][np.abs(t - x) < 4 / 24].mean() > 0.9]
                if not okc or not np.isfinite(n8):
                    continue
                tc = okc[0]; intr = np.abs(t - tc) < 4 / 24
                for K in B:
                    fa = f.copy(); fa[intr] -= K * n8 * 1e-6
                    ka, _ = D.eclipse_mask_auto(t, fa, P)
                    f_fro = any(abs(e["center"] - tc) < 0.3 for e in ev(t[ka], fa[ka]))
                    fl2 = list(flats); fl2[j] = flatten(t, fa, method="biweight", window_length=2.0)
                    fs2 = list(fs); fs2[j] = fa
                    kr2, _, _ = repeat_mask(ts, fs2, P, flats=fl2)
                    f_rep = any(abs(e["center"] - tc) < 0.3 for e in ev(t[kr2[j]], fa[kr2[j]]))
                    B[K].append((f_fro, f_rep))
            except Exception as ex:
                print("   skip one star:", type(ex).__name__, str(ex)[:60], flush=True)
        n = max(A["ss"], 1)
        b = {K: np.array(v, float) for K, v in B.items()}
        print(f"P {lo} to {hi}: stars {A['stars']}, star-sectors {A['ss']} | A: frozen {A['fr']/n:.2f}/{A['ff']/n:.2f} | repeat {A['rr']/n:.2f}/{A['rf']/n:.2f} | kept {A['kf']/n:.3f}, {A['kr']/n:.3f} | single bins per star {A['single']/max(A['stars'],1):.1f}"
              + "".join(f" | B K{K}: {v[:,0].mean():.2f} / {v[:,1].mean():.2f} (n={len(v)})" for K, v in b.items() if len(v)), flush=True)
