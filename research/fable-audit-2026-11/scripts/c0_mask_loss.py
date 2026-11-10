"""C0 sanity test (10 Nov 2026, Opus 5.5): the WO-F01 Part A harness (wo_f01a_mask_loss.py, imported, NOT edited) with stage2_search.mask_runs swapped for the
catalogue mask C0 (c0_catalogue_mask.py). Per file it also counts, on REAL light without injection, real-arm and upside-down-arm events after the frozen mask and after C0,
the share of cadences each mask removes, and frozen-mask events whose centre lies inside a C0 catalogue window (counts only; nothing per star is printed).
Rows (private) -> data\\fable_audit_mask\\rows_<set>_c0.pkl.  Usage: SS_SET=g2 python c0_mask_loss.py run N_PER PROCS | summary"""
import os, sys, pathlib, time, multiprocessing as mp
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, pandas as pd
import wo_f01a_mask_loss as H
import c0_catalogue_mask as C0

FROZEN = H.S2.mask_runs
H.ROWS = H.OUT / f"rows_{H.SET}_c0{os.environ.get('C0_TAG', '')}.pkl"


def init():
    H.init(); H.S2.mask_runs = C0.mask_runs


def run_file(args):
    C0.CURRENT_TIC = args[1]
    rows = H.run_file(args)
    extra = dict(flags=",".join(sorted(C0.FLAGS.get(args[1], set()))))
    try:
        tf, meta, st = H.load_windowed(args[0])
        if tf is not None:
            t, f = tf; per = H.A.PER.get(args[1], [])
            for lab, fn in (("fz", FROZEN), ("c0", C0.mask_runs)):
                t2, f2, _ = fn(t, f, per)
                ev = H.S2.Prod(t2, f2).events(); eu = H.S2.Prod(t2, f2, -1).events()
                extra.update({f"{lab}_real": len(ev), f"{lab}_inv": len(eu), f"{lab}_cut": 1 - len(t2) / len(t)})
                if lab == "fz":
                    c = C0.cat().get(args[1])
                    if c is not None and np.isfinite(c["wp"]):
                        cc = C0.refit(t, f, c); cen = np.array([e["center"] for e in ev])
                        extra["fz_real_in_cat"] = int(C0.windows(cen, cc, padf=1.0)[0].sum()) if len(cen) else 0
    except Exception as e:
        extra["extra_err"] = type(e).__name__
    return [dict(r, **extra) for r in rows]


def run(n_per, procs):
    jobs, _ = H.sample(n_per); rows = []; t0 = time.time()
    with mp.Pool(procs, initializer=init) as pool:
        for r in pool.imap_unordered(run_file, jobs):
            rows += r
    pd.DataFrame(rows).to_pickle(H.ROWS); print("DONE", len(rows), f"{time.time() - t0:.0f} s", flush=True)


def summary():
    out = H.summary()
    df = pd.read_pickle(H.ROWS); f = df.drop_duplicates("file"); f = f[f.skip.isna()] if "skip" in f else f
    out += ["", "F. REAL LIGHT, no injection, per star-sector file (counts only): events real arm / upside-down arm, ratio, share of cadences removed; frozen vs C0"]
    for lo, hi in H.BINS:
        g = f[f.bin_lo == lo]
        if not len(g):
            continue
        r = lambda a, b: f"{g[a].sum():4.0f}/{g[b].sum():4.0f} = {g[a].sum() / max(g[b].sum(), 1):.2f}"
        out.append(f"  {lo:>4g} d n{len(g):3d} | frozen {r('fz_real', 'fz_inv')} cut {g.fz_cut.mean():.3f} | C0 {r('c0_real', 'c0_inv')} cut {g.c0_cut.mean():.3f} | "
                   f"frozen real events inside C0 windows {g.get('fz_real_in_cat', pd.Series(dtype=float)).sum():.0f}")
    fl = f["flags"].fillna("").str.split(",").explode(); fl = fl[fl != ""]
    out.append(f"  C0 fallback flags over {len(f)} files: {fl.value_counts().to_dict()}")
    return out


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("\n".join(summary()))
