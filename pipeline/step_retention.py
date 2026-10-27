"""Completeness check for the v3 flag chain: how many INJECTED dips (box and trapezoid) survive the flags that can be computed from one injected light
curve: flat-baseline step test, eclipse overlap (physical eclipse length) and the 0.35 d eclipse rule. NOT modelled here: gap/dump, burst and matched
upside-down flags, the repeater flag, the second-product check, and planets that transit near a data-segment edge (injections sit in the middle of the
longest segment). Stage 2's injection recipe: depth = 12 x the 8 h noise clipped to 1500..40000 ppm; durations 4, 8 and 14 h; trapezoid = 20 percent
ingress and 20 percent egress. Random star-sectors from the v2 groups, seed 20261028.
Usage: python step_retention.py [n_groups]   (prints a summary and writes research\\stage3\\step_retention.txt)"""
import sys, glob, pathlib, random, multiprocessing as mp
import numpy as np, pandas as pd
import stage2_search as S2, stage3_core as C

G = pathlib.Path(r"D:\second-sun\data\stage3\14c896421028\groups")
DURS = (4.0, 8.0, 14.0)
EPH = C.Ephem(pd.read_csv(C.TARGETS, comment="#"))


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
        x = np.abs(d["t"] - tc) * 24                                     # hours from the middle of the injected dip
        for dur in DURS:
            for shape in ("box", "trap"):
                prof = (x < dur / 2).astype(float) if shape == "box" else np.clip((dur / 2 - x) / (0.2 * dur), 0, 1)
                P = S2.Prod(d["t"], d["f"] - depth * 1e-6 * prof)
                snr = P.snr_near(tc, dur) if dur in S2.DURS_H else P.snr_near_any(tc)
                st = C.step_stats(P.bt, P.bf, P.bd, P.med, tc, dur, depth)
                out.append((pn, f"{shape} {dur:.0f} h", snr, C.step_flag(st), min(st["cover_pre"], st["cover_post"]) < C.STEP_COVER,
                            EPH.overlap(tic, tc, dur), bool(EPH.dist(tic, tc) < C.PH_D)))
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 160
    names = sorted(G.glob("*.json")); random.Random(20261028).shuffle(names)
    with mp.Pool(8, initializer=S2._init) as pool:
        rows = [r for rr in pool.imap_unordered(one, [str(x) for x in names[:n]]) for r in rr]
    df = pd.DataFrame(rows, columns=["product", "kind", "snr", "step", "nocover", "overlap", "c5"])
    df["kept"] = ~(df.step | df.overlap | df.c5); det = df[df.snr >= 7]
    txt = [f"{n} random star-sectors, {len(df)} injected dips, {len(det)} detected at SNR 7 or more; shares below are among the detected"]
    for k, g in det.groupby("kind"):
        txt.append(f"  {k:9s}: {len(g):4d} detected | step test {g.step.mean()*100:4.1f}% (no data on a side {g.nocover.mean()*100:4.1f}%) | eclipse overlap "
                   f"{g.overlap.mean()*100:4.1f}% | 0.35 d rule {g.c5.mean()*100:4.1f}% | kept by all three {g.kept.mean()*100:5.1f}%")
    txt.append(f"  all: {len(det)} detected, kept by the three flags {det.kept.mean()*100:.1f}% (a ceiling: the other flags and the second-product check remove more)")
    print("\n".join(txt)); (pathlib.Path(r"D:\second-sun\research\stage3") / "step_retention.txt").write_text("\n".join(txt), encoding="utf-8")
