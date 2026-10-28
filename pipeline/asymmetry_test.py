"""Is the noise lopsided? Count RAW dips (real curve) and RAW bumps-seen-as-dips (upside-down curve) at several signal-to-noise levels, no flags, in
random star-sectors. Real planets are rare and mostly strong, so at LOW levels (4.5 to 6) the ratio upside-down / real is the noise's own asymmetry.
If the ratio at 7 and above equals that low-level ratio, the real dips at our threshold are what noise alone makes: no excess.
Usage: python asymmetry_test.py [n_groups] [label] [hash]   (no label: the v4 box lengths on the v4 groups, writes research\\stage3\\asymmetry.txt; label v5: the v5 box
lengths on the groups of the given settings hash, writes asymmetry_v5.txt; label v6sap: the v5 box lengths on the SAP twins of the star-sectors in that run's groups_sap folder
(SPOC and TESS-SPOC files read as SAP), writes asymmetry_v6sap.txt; nothing else is saved)"""
import sys, glob, pathlib, random, multiprocessing as mp
import numpy as np, pandas as pd
import stage2_search as S2, stage3_core as C, sap_twin as T

G = pathlib.Path(r"D:\second-sun\data\stage3\d5767e66c4d2\groups")
THR = (4.5, 5.0, 6.0, 7.0, 8.0, 10.0)
SAP = False


def one(name):
    tic, sec = (int(x) for x in pathlib.Path(name).stem.split("_"))
    out = []
    for q in glob.glob(rf"D:\second-sun\data\g1\{tic}\*s{sec:04d}*.fits"):
        if SAP:
            if "qlp" in pathlib.Path(q).name.lower():
                continue
            q += T.SUFFIX
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


def init(grid, sap=False):
    global SAP
    SAP = sap
    S2._init(); C.use_grid(S2, grid); T.install(S2)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    label = sys.argv[2] if len(sys.argv) > 2 else ""
    if len(sys.argv) > 3:
        G = pathlib.Path(rf"D:\second-sun\data\stage3\{sys.argv[3]}\{'groups_sap' if label == 'v6sap' else 'groups'}")
    grid = C.GRID_V5 if label in ("v5", "v6sap") else C.GRID_V4
    names = sorted(G.glob("*.json")); random.Random(20261028).shuffle(names)
    with mp.Pool(8, initializer=init, initargs=(grid, label == "v6sap")) as pool:
        rows = [r for rr in pool.imap_unordered(one, [str(x) for x in names[:n]]) for r in rr]
    df = pd.DataFrame(rows, columns=["kind", "thr", "n", "product"])
    tab = df.groupby(["thr", "kind"]).n.sum().unstack()
    tab["ratio upside-down / real"] = tab["flip"] / tab["real"]
    txt = [f"{n} random star-sectors, all products, RAW events (no flags). Counts of dips found in the real curve and in the upside-down curve:"]
    txt.append(tab.rename(columns={"real": "real dips", "flip": "upside-down dips"}).round(2).to_string())
    print("\n".join(txt)); (pathlib.Path(r"D:\second-sun\research\stage3") / (f"asymmetry_{label}.txt" if label else "asymmetry.txt")).write_text("\n".join(txt), encoding="utf-8")
