"""v6 injected-dip recovery for the SAP twin (FIX-QUEUE item 16, 'the same injected dips through both'). For random star-sectors whose best product is SPOC or TESS-SPOC, the SAME
trapezoid dip (20 percent ingress and egress; same time, same depth in ppm) is injected into the PDCSAP flux and into the SAP flux of the best file, in the middle of the longest data
segment. Depth unit = the 8 h box noise of the PDCSAP curve (the unit of faint_recovery_v5.txt), at graded depths 4 to 10 times that noise and four box lengths. For each cell: how often
PDCSAP finds the dip (SNR 7 or more, the search's own bar), how often SAP finds it, and the union. 'Found' only: the flags and the second-product check are NOT modelled (they act on
both halves). The SAP noise relative to PDCSAP is recorded per star-sector, so the gain can be split by which flux is quieter.
Usage: python sap_recovery.py [n_groups] [procs]   (writes research\\stage3\\sap_recovery_v6.txt)"""
import sys, pathlib, random, multiprocessing as mp
import numpy as np, pandas as pd
import stage2_search as S2, stage3_core as C, stage3 as S3, sap_twin as T
from audit_paths import noise

KS = (4.0, 5.0, 6.0, 7.0, 8.0, 10.0)
DURS = (4.0, 8.0, 14.0, 20.0)
BEST = None


def init():
    S2._init(); C.use_grid(S2, C.GRID_V5); T.install(S2)


def one(args):
    tic, sec, sp = args
    a, _ = S2.prepare(sp[:-len(T.SUFFIX)]); b, _ = S2.prepare(sp)
    if a is None or b is None:
        return []
    t = a["t"]
    seg = np.split(np.arange(len(t)), np.where(np.diff(t) > 0.25)[0] + 1)
    s = max(seg, key=lambda i: t[i[-1]] - t[i[0]]); t0, t1 = t[s[0]], t[s[-1]]; tc = 0.5 * (t0 + t1)
    n8, n8s = noise(t, a["f"], 8.0), noise(b["t"], b["f"], 8.0)
    if not (np.isfinite(n8) and np.isfinite(n8s)) or np.sum(np.abs(b["t"] - tc) < 0.5) < 100:
        return []
    out = []
    for dur in DURS:
        if tc - dur / 48 < t0 or tc + dur / 48 > t1:
            continue
        for k in KS:
            snr = []
            for d in (a, b):
                prof = np.clip((dur / 2 - np.abs(d["t"] - tc) * 24) / (0.2 * dur), 0, 1)
                snr.append(S2.Prod(d["t"], d["f"] - k * n8 * 1e-6 * prof).snr_near_any(tc))
            out.append((a["meta"]["product"], dur, k, snr[0], snr[1], n8s / n8))
    return out


def table(df, label):
    rows = [f"  {label}", "    box h | " + " | ".join(f"{k:g} x noise" for k in KS) + "     cells: PDCSAP / SAP / union, % found at SNR 7 or more"]
    for dur in DURS:
        cells = []
        for k in KS:
            h = df[(df.dur == dur) & (df.k == k)]
            cells.append(f"{h.p.mean() * 100:3.0f}/{h.s.mean() * 100:3.0f}/{h.u.mean() * 100:3.0f}" if len(h) else "    n/a    ")
        rows.append(f"    {dur:5.0f} | " + " | ".join(cells))
    return rows


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 240
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    S2.STARS = S3.STARS_ALL
    best = pd.read_csv(C.BEST, usecols=["tic", "sector", "file"]); bf = {(int(a), int(b)): c for a, b, c in zip(best.tic, best.sector, best.file)}
    gl = [(t, s, next((p for p in ps if pathlib.Path(p[:-len(T.SUFFIX)]).name == bf.get((int(t), int(s)))), None)) for t, s, ps in S3.sap_pass_groups(S2.groups())]
    gl = [g for g in gl if g[2]]
    random.Random(20261028).shuffle(gl)
    with mp.Pool(procs, initializer=init) as pool:
        rows = [r for rr in pool.imap_unordered(one, gl[:n]) for r in rr]
    df = pd.DataFrame(rows, columns=["product", "dur", "k", "snr_p", "snr_s", "noise_ratio"])
    df["p"], df["s"] = df.snr_p >= 7, df.snr_s >= 7
    df["u"] = df.p | df.s
    ng = int(((df.dur == DURS[0]) & (df.k == KS[0])).sum())
    txt = [f"SAP-twin recovery, v5 box lengths, {n} random star-sectors with a SPOC or TESS-SPOC best product (of {len(gl)}), {len(df)} injected dips (trapezoid, 20% ingress and egress), middle of the longest segment.",
           "The SAME dip (same time, same depth in ppm) goes into the PDCSAP flux and into the SAP flux of the best file. Depth unit = 8 h box noise of the PDCSAP curve. Found = SNR 7 or more.",
           "Flags and the second-product check are not modelled, so these are ceilings for both halves. Cells: PDCSAP / SAP / union, percent."]
    txt += table(df, "all star-sectors")
    for lab, m in (("SAP quieter than PDCSAP by more than 20 percent (SAP noise / PDCSAP noise < 0.8)", df.noise_ratio < 0.8), ("about equal (0.8 to 1.25)", (df.noise_ratio >= 0.8) & (df.noise_ratio <= 1.25)),
                   ("SAP noisier by more than 25 percent (> 1.25)", df.noise_ratio > 1.25)):
        sub = df[m]
        txt += table(sub, f"{lab}: {int(((sub.dur == DURS[0]) & (sub.k == KS[0])).sum())} star-sectors at 4 h") if len(sub) else [f"  {lab}: none"]
    s8 = df[df.dur == 8.0]
    txt.append("  8 h cells: dips found by SAP but not by PDCSAP / by PDCSAP but not by SAP (percent of all 8 h injections): " +
               ", ".join(f"{k:g}x {100 * ((g.s & ~g.p).mean()):.0f}/{100 * ((g.p & ~g.s).mean()):.0f}" for k, g in s8.groupby("k")))
    print("\n".join(txt))
    (pathlib.Path(r"D:\second-sun\research\stage3") / "sap_recovery_v6.txt").write_text("\n".join(txt), encoding="utf-8")
