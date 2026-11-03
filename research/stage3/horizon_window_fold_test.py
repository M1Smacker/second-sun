"""H1 of the uncertainty audit (RS-006, 3 Nov 2026): is W = min(1, covered days / P) a good stand-in for folding the real good-time windows?
For a random sample of G2 DEVELOPMENT stars (seed 11), per star-sector take the product with the most good cadences (as the reach calculator does), mark the
good times, fold them modulo each Horizon period-bin centre and count the share of epochs T0 (a planet crossing at T0 + k P) with at least one crossing inside good time.
Compare per star-sector: fold W vs min(1, covered/P); per star: fold coverage of all its sectors together vs 1 - prod(1 - W_i) (the 'independent epochs' step).
Pure coverage (recovery S = 1); eclipse masks are not applied, so the covered days here are slightly larger than the calculator's. Aggregates only.
Usage: D:/second-sun/.venv/Scripts/python.exe -I horizon_window_fold_test.py"""
import glob, re, random, numpy as np, pandas as pd
from astropy.io import fits

ROOT = "D:/second-sun"
PER_EDGES = 10 * 60 ** (np.arange(8) / 7); PER_C = np.sqrt(PER_EDGES[:-1] * PER_EDGES[1:])
BIN = 0.05                                                       # day; phase resolution of the fold
tg = pd.read_csv(f"{ROOT}/targets/g2_chain_targets.csv", comment="#").drop_duplicates("tic")
dev = tg[tg["slice"] == "dev"].tic.tolist()
random.seed(11); sample = random.sample(dev, 80)


def good_times(f):
    with fits.open(f) as h:
        d = h[1].data; cols = d.columns.names
        t = np.asarray(d["TIME"], float); q = np.asarray(d["QUALITY"])
        fl = next((np.asarray(d[c], float) for c in ("PDCSAP_FLUX", "KSPSAP_FLUX", "SAP_FLUX") if c in cols), None)
        ok = np.isfinite(t) & (q == 0) & (np.isfinite(fl) if fl is not None else True)
        cad = np.nanmedian(np.diff(t[np.isfinite(t)])) if np.isfinite(t).sum() > 2 else np.nan
    return t[ok], cad


def covered(tg_, P):
    """boolean array over epochs T0 on a grid of BIN days in [0, P): True if some crossing T0 + kP is inside good time."""
    n = int(np.ceil(P / BIN)); c = np.zeros(n, bool)
    b = np.unique(np.floor(tg_ / BIN).astype(np.int64))
    c[(b * BIN % P / BIN).astype(int) % n] = True
    return c


rows_s, rows_star = [], []
for tic in sample:
    secs = {}
    for f in glob.glob(f"{ROOT}/data/g2/{tic}/*.fits"):
        m = re.search(r"s(\d{4})", f)
        if not m: continue
        try: t, cad = good_times(f)
        except Exception: continue
        if len(t) < 100: continue
        cov = len(t) * cad
        if int(m.group(1)) not in secs or cov > secs[int(m.group(1))][1]:
            secs[int(m.group(1))] = (t, cov)
    if not secs: continue
    for P in PER_C:
        cs = [covered(t, P) for t, _ in secs.values()]
        w_fold = [c.mean() for c in cs]
        w_app = [min(1.0, cov / P) for _, cov in secs.values()]
        for a, b in zip(w_fold, w_app): rows_s.append((P, a, b))
        star_fold = np.logical_or.reduce(cs).mean()
        indep_from_fold = 1 - np.prod([1 - x for x in w_fold])
        indep_from_app = 1 - np.prod([1 - x for x in w_app])
        rows_star.append((P, len(secs), star_fold, indep_from_fold, indep_from_app))
s = pd.DataFrame(rows_s, columns=["P", "fold", "approx"]); st = pd.DataFrame(rows_star, columns=["P", "nsec", "fold", "indep_fold", "indep_app"])
out = [f"H1 window-function test: {st.groupby('P').ngroups and len(st)//len(PER_C)} G2 development stars (seed 11), {len(s)//len(PER_C)} star-sectors; coverage only (S = 1); aggregates only.",
       "Per star-sector: mean of fold coverage W_fold and of the approximation min(1, covered/P); ratio approx/fold of the means.",
       "P centre (d) | W_fold | W_approx | approx/fold"]
for P, g in s.groupby("P"):
    out.append(f"{P:10.1f}   | {g.fold.mean():.3f}  | {g.approx.mean():.3f}   | {g.approx.mean() / g.fold.mean():.2f}")
out += ["", "Per star (all its sectors together): coverage by folding all windows vs 1 - prod(1 - W_i) from fold W and from approximate W; stars with 2 or more sectors only (n shown).",
        "P centre (d) | n | star fold | independent (fold W) | independent (approx W) | approx/star-fold"]
m2 = st[st.nsec >= 2]
for P, g in m2.groupby("P"):
    out.append(f"{P:10.1f}   | {len(g):2d} | {g.fold.mean():.3f}     | {g.indep_fold.mean():.3f}                | {g.indep_app.mean():.3f}                  | {g.indep_app.mean() / g.fold.mean():.2f}")
txt = "\n".join(out); print(txt)
open(f"{ROOT}/research/stage3/horizon-window-fold-test.txt", "w", encoding="utf-8", newline="\n").write(txt + "\n")
