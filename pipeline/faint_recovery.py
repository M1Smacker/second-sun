"""Faint-dip recovery (v5, FIX-QUEUE: the biggest open measurement). Until now only DEEP injected dips (12 x the 8 h noise) in the MIDDLE of a data segment were
tested (step_retention.py: 82.7 to 86.4 percent kept). Here a trapezoid dip (20 percent ingress and egress) is injected at graded depths from 4 to 10 times the
8 h box noise, at four box lengths (4, 8, 14 and 20 h) and at three places: the middle of the longest data segment, 1.5 d after data resumes (just outside the
1 d ramp flag) and 0.75 d after data resumes (inside it). One product per star-sector (the one with the longest span), the v5 box lengths, the search's own
threshold (SNR 7). For each cell: how often the dip is found, and how often a found dip also passes the computable flags (step test, eclipse overlap, 0.35 d
rule, dominance, 1 d ramp, 0.5 d gap edge). NOT modelled: burst, matched-upside-down and repeater flags, the second-product check. Random star-sectors from the
v4 groups, seed 20261028 (the same shuffle as step_retention.py).
Usage: python faint_recovery.py [n_groups] [procs]   (prints a summary and writes research\\stage3\\faint_recovery_v5.txt)"""
import sys, pathlib, glob, random, multiprocessing as mp
import numpy as np, pandas as pd
import stage2_search as S2, stage3_core as C
from audit_paths import noise

G = pathlib.Path(r"D:\second-sun\data\stage3\d5767e66c4d2\groups")
KS = (4.0, 5.0, 6.0, 7.0, 8.0, 10.0)                       # injected depth in units of the 8 h box noise
DURS = (4.0, 8.0, 14.0, 20.0)
PLACES = (("middle", None), ("1.5 d after data resumes", 1.5), ("0.75 d after data resumes", 0.75))
EPH = C.Ephem(pd.read_csv(C.TARGETS, comment="#"), C.eb_widths())


def init():
    S2._init(); C.use_grid(S2, C.GRID_V5)


def one(name):
    tic, sec = (int(x) for x in pathlib.Path(name).stem.split("_"))
    prods = {}
    for q in glob.glob(rf"D:\second-sun\data\g1\{tic}\*s{sec:04d}*.fits"):
        try:
            d, _ = S2.prepare(q)
        except Exception:
            continue
        if d is not None:
            prods[d["meta"]["product"]] = d
    if not prods:
        return []
    a = max(prods.values(), key=lambda d: d["t"].max() - d["t"].min())
    t = a["t"]
    seg = np.split(np.arange(len(t)), np.where(np.diff(t) > 0.25)[0] + 1)
    s = max(seg, key=lambda i: t[i[-1]] - t[i[0]]); t0, t1 = t[s[0]], t[s[-1]]
    n8 = noise(t, a["f"], 8.0)
    if not np.isfinite(n8):
        return []
    fmax = max([e["snr"] for e in S2.Prod(t, a["f"], -1).events()] or [0.0])        # strongest upside-down event of the untouched curve (v4 dominance)
    ed = np.sort(np.asarray(a["edges"], dtype=float)); out = []
    for pname, off in PLACES:
        tc = 0.5 * (t0 + t1) if off is None else t0 + off
        for dur in DURS:
            if tc - dur / 48 < t0 or tc + dur / 48 > t1:
                continue
            x = np.abs(t - tc) * 24
            prof = np.clip((dur / 2 - x) / (0.2 * dur), 0, 1)
            for k in KS:
                P = S2.Prod(t, a["f"] - k * n8 * 1e-6 * prof)
                snr = P.snr_near_any(tc)
                st = C.step_stats(P.bt, P.bf, P.bd, P.med, tc, dur, k * n8)
                step = C.step_flag(st); ovl = EPH.overlap(tic, tc, dur); c5 = bool(EPH.dist(tic, tc) < C.PH_D)
                ramp = off is not None and off < C.RAMP_D; gap = bool(ed.size and np.min(np.abs(ed - tc)) < 0.5)
                out.append((a["meta"]["product"], pname, dur, k, snr, step, ovl, c5, bool(fmax >= snr), ramp, gap))
    return out


def table(det_all, label):
    rows = [f"  {label}"]
    rows.append("    box h | " + " | ".join(f"{k:g} x noise" for k in KS))
    for dur in DURS:
        g = det_all[det_all.dur == dur]
        cells = []
        for k in KS:
            h = g[g.k == k]
            cells.append(f"{h.found.mean() * 100:4.0f}% ({h.kept.mean() * 100:3.0f}%)" if len(h) else "   n/a   ")
        rows.append(f"    {dur:5.0f} | " + " | ".join(cells))
    return rows


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 240
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    names = sorted(G.glob("*.json")); random.Random(20261028).shuffle(names)
    with mp.Pool(procs, initializer=init) as pool:
        rows = [r for rr in pool.imap_unordered(one, [str(x) for x in names[:n]]) for r in rr]
    df = pd.DataFrame(rows, columns=["product", "place", "dur", "k", "snr", "step", "overlap", "c5", "dom", "ramp", "gap"])
    df["found"] = df.snr >= 7
    df["kept"] = df.found & ~(df.step | df.overlap | df.c5 | df.dom | df.ramp | df.gap)
    txt = [f"Faint-dip recovery, v5 box lengths, {n} random star-sectors, {len(df)} injected dips (trapezoid, 20% ingress and egress), one product per star-sector.",
           "Cells: share FOUND at SNR 7 or more (share that is found AND passes the computable flags). Depth in units of the 8 h box noise of that light curve. Gap, burst, matched",
           "upside-down and repeater flags and the second-product check are not modelled, so 'kept' is a ceiling."]
    for pname, _ in PLACES:
        txt += table(df[df.place == pname], f"place: {pname} ({int(((df.place == pname) & (df.k == KS[0]) & (df.dur == DURS[0])).sum())} star-sectors at 4 h)")
    for pr, g in df[df.place == "middle"].groupby("product"):
        txt += table(g, f"middle, product {pr}")
    s8 = df[(df.place == "middle") & (df.dur == 8.0)].groupby("k").snr.median()
    txt.append("  median SNR actually reached by an 8 h dip in the middle: " + ", ".join(f"{k:g} x noise -> {v:.1f}" for k, v in s8.items()))
    print("\n".join(txt))
    (pathlib.Path(r"D:\second-sun\research\stage3") / "faint_recovery_v5.txt").write_text("\n".join(txt), encoding="utf-8")
