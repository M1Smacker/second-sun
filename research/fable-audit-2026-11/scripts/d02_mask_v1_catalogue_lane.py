"""D-02 (Fable, 10 Nov 2026): the Petrova 1.0 mask prototype with rules 6 and 7 of design/PETROVA-1.0-MASK-DESIGN.md added to d01.
Rule 6 (catalogue window): mask the catalogue primary and secondary eclipse (Prsa 2022 polyfit: phases Phip-pf, Phis-pf relative to BJD0, widths Wp-pf, Ws-pf in phase), half-width = 1.0 x the catalogue width, also when seen once.
Rule 7 (single-visit lane): a low bin seen in one cycle only and outside the catalogue windows stays in the light; an event whose centre falls in such a bin (plus or minus 2 bins) is labelled "lane" and counted apart.
The upside-down arm gets the mirror: repeat rule and lane computed on the flipped light, same catalogue windows.
Scratch only; counts only; the frozen pipeline is imported read-only.
Usage: python d02_mask_v1_catalogue_lane.py [stars_per_bin] [max_sectors]"""
import sys, warnings
sys.path.insert(0, r"D:\second-sun\pipeline")
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from wotan import flatten
import detect_v2 as D
from audit_paths import noise
from d01_mask_v1_prototype import runs_of, NB, NSIG, PAD, GRID, ev


def repeat_mask2(ts, flats, P):
    """Returns (ecl bins bool[NB], single bins bool[NB])."""
    t = np.concatenate(ts); fl = np.concatenate(flats); ok = np.isfinite(fl)
    ph = (t % P) / P; cyc = np.floor(t / P).astype(int); k = np.clip((ph * NB).astype(int), 0, NB - 1)
    df = pd.DataFrame(dict(k=k[ok], c=cyc[ok], v=fl[ok]))
    fold = df.groupby("k").v.median().reindex(range(NB)).values
    pc = df.groupby(["k", "c"]).v.agg(["median", "size"]).reset_index(); pc = pc[pc["size"] >= 3]
    m0 = np.nanmedian(fold); sig = 1.4826 * np.nanmedian(np.abs(fold - m0))
    lowf = np.nan_to_num(fold < m0 - NSIG * sig).astype(bool)
    nvis = pc.groupby("k").size().reindex(range(NB)).fillna(0).values
    by = {kk: g["median"].values for kk, g in pc.groupby("k")}
    ecl = np.zeros(NB, bool); single = np.zeros(NB, bool)
    for i in np.where(lowf)[0]:
        if nvis[i] >= 3 or (nvis[i] == 2 and np.all(by[i] < m0 - max(2 * sig, 0.3 * (m0 - fold[i])))):
            ecl[i] = True
        else:
            single[i] = True
    return ecl, single


def keep_from(t, P, ecl, cat):
    p = (t % P) / P; keep = np.ones_like(t, bool)
    for a, b in runs_of(ecl):
        w = b - a; lo, hi = a - PAD * w, b + PAD * w
        for sh in (-1, 0, 1):
            keep &= ~((p >= lo + sh) & (p <= hi + sh))
    if cat is not None:
        t0, wins = cat
        pc = ((t - t0) / P) % 1.0
        for c, w in wins:
            d = np.abs(((pc - c + 0.5) % 1.0) - 0.5)
            keep &= d > w
    return keep


def in_lane(center, P, single):
    k = int(((center % P) / P) * NB) % NB
    return bool(single[[(k + j) % NB for j in (-2, -1, 0, 1, 2)]].any())


def in_cat(center, P, cat):
    if cat is None:
        return False
    t0, wins = cat; pc = ((center - t0) / P) % 1.0
    return any(abs(((pc - c + 0.5) % 1.0) - 0.5) <= w for c, w in wins)


if __name__ == "__main__":
    n_per = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    max_sec = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    tg = pd.read_csv(r"D:\second-sun\targets\g2_chain_targets.csv", comment="#").drop_duplicates("tic").set_index("tic")
    eb = pd.read_csv(r"D:\second-sun\data\xmatch\ebs.csv").drop_duplicates("TIC").set_index("TIC")
    man = pd.read_csv(r"D:\second-sun\data\g2\manifest.csv").drop_duplicates("file")
    man = man[(man.author == "SPOC") & man.tic.isin(tg.index)]
    cnt = man.groupby("tic").size(); stars = pd.DataFrame(dict(tic=cnt.index, n=cnt.values)); stars["P"] = stars.tic.map(tg.p_bin_d); stars = stars[stars.n >= 3]
    rng = np.random.default_rng(3)
    print(f"stars per bin {n_per}, up to {max_sec} sectors each, seed 3. Events per star-sector, real/upside-down.")
    print("A frozen | A new mask, outside the lane | A new mask, lane only | single bins per star: before the catalogue window -> left after it | stars with catalogue widths")
    print("B planted 8 h dip before the mask: K12 found frozen / new (of the new finds, share labelled lane) ; same for K25")
    for lo, hi in ((5, 10), (10, 14), (14, 20), (20, 27.4), (27.4, 1e4)):
        sub = stars[(stars.P >= lo) & (stars.P < hi)]
        pick = sub.sample(n=min(n_per, len(sub)), random_state=3)
        A = dict(ss=0, fr=0, ff=0, nr=0, nf=0, lr=0, lf=0, s0=0, s1=0, stars=0, cat=0); B = {12: [], 25: []}
        for s in pick.itertuples():
            try:
                P = float(s.P); paths = man[man.tic == s.tic].path.tolist()[:max_sec]
                L = [D.load(p) for p in paths]; ts = [x[0] for x in L]; fs = [x[1] for x in L]
                cat = None
                if s.tic in eb.index:
                    r = eb.loc[s.tic]; wins = []
                    if np.isfinite(r["Wp-pf"]) and r["Wp-pf"] > 0:
                        wins.append((float(r["Phip-pf"]) % 1.0 if np.isfinite(r["Phip-pf"]) else 0.0, float(r["Wp-pf"])))
                        ws = float(r["Ws-pf"]) if np.isfinite(r["Ws-pf"]) and r["Ws-pf"] > 0 else float(r["Wp-pf"])
                        wins.append((float(r["Phis-pf"]) % 1.0 if np.isfinite(r["Phis-pf"]) else (wins[0][0] + 0.5) % 1.0, ws))
                        cat = (float(tg.bjd0[s.tic]) - 57000.0, wins)
                flats = [flatten(t, f, method="biweight", window_length=2.0) for t, f in zip(ts, fs)]
                ecl, single = repeat_mask2(ts, flats, P)
                eclm, singlem = repeat_mask2(ts, [2 - x for x in flats], P)
                # single bins that the catalogue window covers are no longer in the light: drop them from the lane
                centres = (np.arange(NB) + 0.5) / NB * P
                cov = np.array([in_cat(c, P, cat) for c in centres]) if cat is not None else np.zeros(NB, bool)
                A["stars"] += 1; A["cat"] += int(cat is not None); A["s0"] += int(single.sum()); single = single & ~cov; singlem = singlem & ~cov; A["s1"] += int(single.sum())
                for t, f in zip(ts, fs):
                    k0, _ = D.eclipse_mask_auto(t, f, P)
                    kr = keep_from(t, P, ecl, cat); kk = kr & keep_from(t, P, eclm, None)
                    A["ss"] += 1
                    A["fr"] += len(ev(t[k0], f[k0])); A["ff"] += len(ev(t[k0], 2 - f[k0]))
                    for e in ev(t[kr], f[kr]):
                        A["lr" if in_lane(e["center"], P, single) else "nr"] += 1
                    for e in ev(t[kk], 2 - f[kk]):
                        A["lf" if in_lane(e["center"], P, singlem) else "nf"] += 1
                j = int(rng.integers(len(ts))); t, f = ts[j], fs[j]
                k0, _ = D.eclipse_mask_auto(t, f, P); tk = t[k0]; n8 = noise(tk, f[k0], 8.0); krj = keep_from(t, P, ecl, cat)
                okc = [x for x in rng.choice(tk, 80) if x - tk.min() > 1.5 and tk.max() - x > 1.5 and np.sum(np.abs(tk - x) < 4 / 24) > 0.9 * 240 and krj[np.abs(t - x) < 4 / 24].mean() > 0.9]
                if not okc or not np.isfinite(n8):
                    continue
                tc = okc[0]; intr = np.abs(t - tc) < 4 / 24
                for K in B:
                    fa = f.copy(); fa[intr] -= K * n8 * 1e-6
                    ka, _ = D.eclipse_mask_auto(t, fa, P)
                    f_fro = any(abs(e["center"] - tc) < 0.3 for e in ev(t[ka], fa[ka]))
                    fl2 = list(flats); fl2[j] = flatten(t, fa, method="biweight", window_length=2.0)
                    e2, s2 = repeat_mask2(ts, fl2, P); k2 = keep_from(t, P, e2, cat)
                    hit = [e for e in ev(t[k2], fa[k2]) if abs(e["center"] - tc) < 0.3]
                    B[K].append((f_fro, bool(hit), bool(hit) and in_lane(hit[0]["center"], P, s2 & ~cov)))
            except Exception as ex:
                print("   skip one star:", type(ex).__name__, str(ex)[:60], flush=True)
        n = max(A["ss"], 1); ns = max(A["stars"], 1)
        line = (f"P {lo} to {hi}: stars {A['stars']}, star-sectors {A['ss']} | A frozen {A['fr']/n:.2f}/{A['ff']/n:.2f} | new outside lane {A['nr']/n:.2f}/{A['nf']/n:.2f} | lane {A['lr']/n:.2f}/{A['lf']/n:.2f}"
                f" | single bins per star {A['s0']/ns:.1f} -> {A['s1']/ns:.1f} | catalogue widths for {A['cat']} of {A['stars']}")
        for K, v in B.items():
            a = np.array(v, float)
            if len(a):
                line += f" | B K{K}: {a[:,0].mean():.2f} / {a[:,1].mean():.2f} (lane share {a[:,2].sum()/max(a[:,1].sum(),1):.2f}, n={len(a)})"
        print(line, flush=True)
