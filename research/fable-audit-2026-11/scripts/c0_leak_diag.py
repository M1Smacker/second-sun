"""C0 diagnosis (10 Nov 2026, Opus 5.5). Counts only.
1. m split by the C0 fallback flag (no_cat files use the frozen mask) from data\\fable_audit_mask\\rows_<set>_c0.pkl.
2. Where do C0's real-arm events on real light sit? For each sampled file (same sample as c0_mask_loss.py, N_PER 8): events after C0, classed by distance from the
   catalogue primary / secondary centre (after the refit) in primary widths, and by phase for stars with no catalogue secondary. Same for the upside-down arm.
Usage: SS_SET=g2|g3 python c0_leak_diag.py"""
import os, sys, pathlib, multiprocessing as mp
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, pandas as pd
import wo_f01a_mask_loss as H
import c0_catalogue_mask as C0


def classify(args):
    path, tic = args[0], args[1]
    try:
        tf, meta, st = H.load_windowed(path)
        c = C0.cat().get(tic)
        if tf is None or c is None or not np.isfinite(c["wp"]):
            return []
        t, f = tf; t2, f2, _ = C0.mask_runs(t, f, H.A.PER.get(tic, []), tic=tic)
        cc = C0.refit(t, f, c) if C0.REFIT else c
        sec_ok = np.isfinite(cc["phs"]) and np.isfinite(cc["ws"])
        out = []
        for arm in (1, -1):
            for e in H.S2.Prod(t2, f2, arm).events():
                ph = ((e["center"] - cc["T0"]) / cc["P"]) % 1.0
                dp = min(ph, 1 - ph) * cc["P"] / cc["wp"]                                   # distance from primary centre, in primary widths
                s = cc["phs"] if sec_ok else 0.5; ws = cc["ws"] if sec_ok else cc["wp"]
                ds = min(abs(ph - s), 1 - abs(ph - s)) * cc["P"] / ws
                out.append(dict(arm=arm, sec_ok=sec_ok, ecc=bool(sec_ok and abs(cc["phs"] - 0.5) > 0.02), dp=dp, ds=ds, ph=ph, P=cc["P"], dur=e["dur_h"],
                                wp_h=cc["wp"] * 24, bin_lo=args[4], file=pathlib.Path(path).name))
        return out
    except Exception as ex:
        return [dict(err=type(ex).__name__)]


def init():
    H.init()


if __name__ == "__main__":
    lines = []
    rows = pd.read_pickle(H.OUT / f"rows_{H.SET}_c0.pkl")
    d = rows[(rows.get("sign") == 1) & rows.K.isin((12.0, 25.0))].copy()
    d["nocat"] = d["flags"].fillna("").str.contains("no_cat")
    lines.append(f"1. m split by fallback ({H.SET}, K 12 and 25, all durations; before/after, files)")
    for nc, g in d.groupby("nocat"):
        cells = [f"{x.found_before.mean():.2f}/{x.found_after.mean():.2f} n{x.file.nunique()}" for _, x in g.groupby("bin_lo")]
        lines.append(f"  {'no_cat (frozen fallback)' if nc else 'catalogue window       '} | " + " | ".join(cells) + f" | all {g.found_before.sum() / max(g.found_after.sum(), 1):.2f}")
    jobs, _ = H.sample(8)
    with mp.Pool(6, initializer=init) as pool:
        ev = pd.DataFrame([r for rr in pool.map(classify, jobs) for r in rr])
    if "err" in ev:
        lines.append(f"  errors: {ev.err.notna().sum()}"); ev = ev[ev.err.isna()]
    lines.append(f"\n2. C0 events on real light ({H.SET}, {len(jobs)} files sampled): where they sit (counts; real arm / upside-down arm)")
    for lab, sel in (("within 1.5 primary widths of the primary centre (edge leak)", lambda x: x.dp < 1.5),
                     ("within 1.5 secondary widths of the catalogue secondary", lambda x: (x.dp >= 1.5) & x.sec_ok & (x.ds < 1.5)),
                     ("within 1.5 widths of phase 0.5, star with NO catalogue secondary", lambda x: (x.dp >= 1.5) & ~x.sec_ok & (x.ds < 1.5)),
                     ("elsewhere, star with no catalogue secondary", lambda x: (x.dp >= 1.5) & ~x.sec_ok & (x.ds >= 1.5)),
                     ("elsewhere, star with catalogue secondary", lambda x: (x.dp >= 1.5) & x.sec_ok & (x.ds >= 1.5))):
        k = sel(ev)
        lines.append(f"  {lab:66s}: {int((k & (ev.arm == 1)).sum()):3d} / {int((k & (ev.arm == -1)).sum()):3d}")
    r = ev[ev.arm == 1]
    lines.append(f"  real-arm events, phase from primary, histogram in 10 bins: {np.histogram(r.ph, bins=10, range=(0, 1))[0].tolist()}")
    lines.append(f"  real-arm events: share whose duration exceeds 0.5 x primary width {np.mean(r.dur > 0.5 * r.wp_h):.2f}; eccentric-secondary stars {int(r.ecc.sum())}")
    # repeats: real-arm events of one file that sit at the same binary phase (within 1.5 primary widths) = a recurring eclipse the windows miss
    rep = tot = 0; files_rep = set()
    for fn, g in r.groupby("file"):
        ph = g.ph.values; tol = 1.5 * g.wp_h.iloc[0] / 24 / g.P.iloc[0]
        for i in range(len(ph)):
            tot += 1
            if any(min(abs(ph[i] - ph[j]), 1 - abs(ph[i] - ph[j])) < tol for j in range(len(ph)) if j != i):
                rep += 1; files_rep.add(fn)
    u = ev[ev.arm == -1]; urep = 0
    for fn, g in u.groupby("file"):
        ph = g.ph.values; tol = 1.5 * g.wp_h.iloc[0] / 24 / g.P.iloc[0]
        urep += sum(any(min(abs(ph[i] - ph[j]), 1 - abs(ph[i] - ph[j])) < tol for j in range(len(ph)) if j != i) for i in range(len(ph)))
    lines.append(f"  real-arm events that REPEAT at the same binary phase in their file: {rep} of {tot} (in {len(files_rep)} files of {r.file.nunique()} with events); upside-down arm: {urep} of {len(u)}")
    print("\n".join(lines))
