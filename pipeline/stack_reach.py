"""Vesper study phase D, question 1 (own data first): how many transits of a planet of period P does our data cover per star, so how much can stacking ever add?
For each star, the sectors it has (best-product star-sectors of the frozen run, no events read) are laid out as 25.5-day windows from the sector number (BTJD 1325.3 + 27.3 x (sector - 1); an upper bound,
real good-data cover is lower). A planet of period P and random phase is placed; N = transits that fall in a window (400 phases per star). Stacking N dips at equal depth gains N**0.25 in smallest detectable radius
(SNR ~ sqrt(N) x depth, depth ~ radius**2). N >= 2 is needed to link anything at all. TTVs, duration changes and gaps make every number here an upper bound.
Usage: python stack_reach.py   (aggregates only; writes research/stage3/stack-reach.txt)"""
import os
import numpy as np

SETS = {"g1": "fd788be04650", "g2": "dev_73f62615e365"}
PERIODS = (20, 30, 50, 75, 100, 150, 200, 300)


def load(name):
    os.environ["SS_SET"] = name
    import dataset as DS; import importlib; importlib.reload(DS)
    import stage3_core as C, stage3_report as R
    importlib.reload(C); importlib.reload(R)
    ev, meta = R.load(str(C.DS.RUNS / SETS[name] / "groups"))
    ss = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"])
    return {int(t): np.sort(g.sector.values.astype(int)) for t, g in ss.groupby("tic")}


def reach(secs, P, rng, draws=400):
    lo = 1325.3 + 27.3 * (secs - 1); hi = lo + 25.5
    span0, span1 = lo.min(), hi.max()
    n = np.zeros(draws, int)
    for i in range(draws):
        t = span0 + rng.uniform(0, P) + P * np.arange(int((span1 - span0) / P) + 2)
        n[i] = int(((t[:, None] >= lo) & (t[:, None] <= hi)).any(axis=1).sum())
    return n


if __name__ == "__main__":
    rng = np.random.default_rng(20261030); out = []
    for name in SETS:
        stars = load(name); ns = np.array([len(v) for v in stars.values()])
        out.append(f"{name}: {len(stars)} stars, sectors per star: median {np.median(ns):.0f}, 10th to 90th percentile {np.percentile(ns, 10):.0f} to {np.percentile(ns, 90):.0f}, share with 1 sector {100 * (ns == 1).mean():.0f}%")
        out.append("   period d | median transits covered | share of star-phases with N>=2 / >=3 / >=5 / >=9 | median radius gain where N>=2 | share with gain >= 1.3 (N>=3)")
        for P in PERIODS:
            N = np.concatenate([reach(v, P, rng) for v in stars.values()])
            g = N[N >= 2] ** 0.25
            out.append(f"   {P:7d} | {np.median(N):.0f} | {100 * (N >= 2).mean():.0f}% / {100 * (N >= 3).mean():.0f}% / {100 * (N >= 5).mean():.0f}% / {100 * (N >= 9).mean():.0f}% | "
                       f"{np.median(g) if len(g) else float('nan'):.2f} | {100 * (N >= 3).mean():.0f}%")
    txt = chr(10).join(out); print(txt)
    open("../research/stage3/stack-reach.txt", "w", encoding="utf-8").write(txt + chr(10))
