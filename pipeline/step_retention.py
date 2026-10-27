"""v3 check: how many INJECTED box dips does the flat-baseline step test wrongly flag? (retention = 1 - flagged). Stage 2's injection recipe: depth =
12 x the 8 h noise clipped to 1500..40000 ppm, middle of the longest segment; boxes of 4, 8 and 14 h. Random star-sectors, seed 20261028.
Usage: python step_retention.py [n_groups]  (prints a summary; nothing is saved but research\stage3\step_retention.txt)"""
import sys, glob, pathlib, random, multiprocessing as mp
import numpy as np
import stage2_search as S2, stage3_core as C

G = pathlib.Path(r"D:\second-sun\data\stage3\14c896421028\groups")
DURS = (4.0, 8.0, 14.0)


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
    seg = np.split(np.arange(len(a["t"])), np.where(np.diff(a["t"]) > 0.25)[0] + 1)
    s = max(seg, key=lambda i: a["t"][i[-1]] - a["t"][i[0]]); tc = 0.5 * (a["t"][s[0]] + a["t"][s[-1]])
    n8 = S2.noise(a["t"], a["f"], 8.0)
    if not np.isfinite(n8):
        return []
    depth = float(np.clip(12 * n8, 1500, 40000)); out = []
    for pn, d in prods.items():
        for dur in DURS:
            fi = d["f"].copy(); fi[np.abs(d["t"] - tc) < dur / 48] -= depth * 1e-6
            P = S2.Prod(d["t"], fi)
            snr = P.snr_near(tc, dur) if dur in S2.DURS_H else P.snr_near_any(tc)
            st = C.step_stats(P.bt, P.bf, P.bd, P.med, tc, dur, depth)
            out.append((pn, dur, snr, C.step_flag(st), min(st["cover_pre"], st["cover_post"]) < C.STEP_COVER))
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 160
    names = sorted(G.glob("*.json")); random.Random(20261028).shuffle(names)
    with mp.Pool(8, initializer=S2._init) as pool:
        rows = [r for rr in pool.imap_unordered(one, [str(x) for x in names[:n]]) for r in rr]
    import pandas as pd
    df = pd.DataFrame(rows, columns=["product", "dur", "snr", "flag", "nocover"]); det = df[df.snr >= 7]
    txt = [f"{n} random star-sectors, {len(df)} injected boxes, {len(det)} detected at SNR 7 or more (flagged share below is among the detected)"]
    for k, g in det.groupby("dur"):
        txt.append(f"  {k:4.0f} h box: {len(g):4d} detected, step test flags {g.flag.mean()*100:5.1f}%  (of which no data on a side: {g.nocover.mean()*100:4.1f}%)")
    txt.append(f"  all: {len(det)} detected, flagged {det.flag.mean()*100:.1f}%, so {100 - det.flag.mean()*100:.1f}% of injected dips are kept")
    print("\n".join(txt)); (pathlib.Path(r"D:\second-sun\research\stage3") / "step_retention.txt").write_text("\n".join(txt), encoding="utf-8")
