"""Is the noise lopsided? Count RAW dips (real curve) and RAW bumps-seen-as-dips (upside-down curve) at several signal-to-noise levels, no flags, in
random star-sectors. Real planets are rare and mostly strong, so at LOW levels (4.5 to 6) the ratio upside-down / real is the noise's own asymmetry.
If the ratio at 7 and above equals that low-level ratio, the real dips at our threshold are what noise alone makes: no excess.
Usage: python asymmetry_test.py [n_groups]   (writes research\\stage3\\asymmetry.txt; nothing else is saved)"""
import sys, glob, pathlib, random, multiprocessing as mp
import numpy as np, pandas as pd
import stage2_search as S2

G = pathlib.Path(r"D:\second-sun\data\stage3\d5767e66c4d2\groups")
THR = (4.5, 5.0, 6.0, 7.0, 8.0, 10.0)


def one(name):
    tic, sec = (int(x) for x in pathlib.Path(name).stem.split("_"))
    out = []
    for q in glob.glob(rf"D:\second-sun\data\g1\{tic}\*s{sec:04d}*.fits"):
        try:
            d, _ = S2.prepare(q)
        except Exception:
            continue
        if d is None:
            continue
        for kind, sign in (("real", 1), ("flip", -1)):
            P = S2.Prod(d["t"], d["f"], sign)
            ev = P.events(thr=min(THR))
            for t in THR:
                out.append((kind, t, sum(1 for e in ev if e["snr"] >= t), d["meta"]["product"]))
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    names = sorted(G.glob("*.json")); random.Random(20261028).shuffle(names)
    with mp.Pool(8, initializer=S2._init) as pool:
        rows = [r for rr in pool.imap_unordered(one, [str(x) for x in names[:n]]) for r in rr]
    df = pd.DataFrame(rows, columns=["kind", "thr", "n", "product"])
    tab = df.groupby(["thr", "kind"]).n.sum().unstack()
    tab["ratio upside-down / real"] = tab["flip"] / tab["real"]
    txt = [f"{n} random star-sectors, all products, RAW events (no flags). Counts of dips found in the real curve and in the upside-down curve:"]
    txt.append(tab.rename(columns={"real": "real dips", "flip": "upside-down dips"}).round(2).to_string())
    print("\n".join(txt)); (pathlib.Path(r"D:\second-sun\research\stage3") / "asymmetry.txt").write_text("\n".join(txt), encoding="utf-8")
