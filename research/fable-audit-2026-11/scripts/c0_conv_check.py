"""C0 phase-convention check (10 Nov 2026, Sonnet 5.5 Extra): for G2 stars whose catalogue primary phase (Phip-pf, else Phip-2g) is NOT near 0 or 1, which window position sits on a real eclipse:
  'T0'   the primary at BJD0              (what C0 assumed)
  'phip' the primary at BJD0 + Phip * P   (the catalogue phase column added)
Per star: one SPOC-family file, light flattened by a running median (the larger of 1 d and 4 widths), z = (mean flux inside the primary window minus the median outside) / (robust sigma / sqrt(n)).
A real eclipse gives a large NEGATIVE z. COUNTS ONLY are printed, no star ids. Control: stars with Phip near 0 or 1 (both conventions agree there).
Usage: SS_SET=g2 python c0_conv_check.py"""
import os, sys, pathlib, warnings
os.environ.setdefault("NUMBA_NUM_THREADS", "1"); warnings.filterwarnings("ignore")
sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import dataset as DS, stage2_search as S2, audit_all as A

eb = pd.read_csv(r"D:\second-sun\data\xmatch\ebs.csv").drop_duplicates("TIC")
tg = pd.read_csv(r"D:\second-sun\targets\g2_chain_targets.csv", comment="#").drop_duplicates("tic")
e = eb[eb.TIC.isin(set(tg.tic.astype(int)))].copy()
e["wp"] = np.where(e["Wp-pf"] > 0, e["Wp-pf"], e["Wp-2g"] / 1.44); e["php"] = np.where(e["Wp-pf"] > 0, e["Phip-pf"], e["Phip-2g"])
e = e[(e.wp > 0) & e.php.notna()]
near = (e.php % 1.0 < 0.02) | (e.php % 1.0 > 0.98)
man = pd.read_csv(DS.MANIFEST).drop_duplicates("file"); man = man[man.author != "QLP"]
first = man.drop_duplicates("tic").set_index("tic")


def z_at(t, ff, centre, P, w):
    ph = ((t - centre) / P + 0.5) % 1.0 - 0.5
    k = np.abs(ph * P) <= w / 2
    o = np.abs(ph * P) > 1.5 * w
    if k.sum() < 5 or o.sum() < 50:
        return np.nan
    sig = 1.4826 * np.median(np.abs(ff[o] - np.median(ff[o])))
    return (np.mean(ff[k]) - np.median(ff[o])) / (sig / np.sqrt(k.sum()))


def zs(row):
    if row.TIC not in first.index:
        return None
    t, f, _, _ = S2.load(first.loc[row.TIC].path, info=True)
    if len(t) < 500:
        return None
    P, w = row.Per, row.wp * row.Per
    cad = np.median(np.diff(t)); n = int(max(1.0, 4 * w) / cad) | 1
    ff = f / pd.Series(f).rolling(n, center=True, min_periods=n // 3).median().values
    ok = np.isfinite(ff); t, ff = t[ok], ff[ok]
    return z_at(t, ff, row.BJD0, P, w), z_at(t, ff, row.BJD0 + row.php * P, P, w)


rng = np.random.default_rng(5)
for lab, sel in (("Phip NOT near 0/1 (pf)", e[~near & (e["Wp-pf"] > 0)]), ("Phip NOT near 0/1 (2g only)", e[~near & ~(e["Wp-pf"] > 0)]), ("control: Phip near 0/1", e[near])):
    idx = rng.choice(len(sel), min(30, len(sel)), replace=False); res = []
    for r in sel.iloc[idx].itertuples():
        try:
            z = zs(r)
        except Exception:
            z = None
        if z and np.isfinite(z[0]) and np.isfinite(z[1]):
            res.append(z)
    a = np.array(res)
    if not len(a):
        print(lab, "no usable stars"); continue
    print(f"{lab}: {len(sel)} stars in G2, {len(a)} tested | median z: T0 convention {np.median(a[:, 0]):.1f}, phip convention {np.median(a[:, 1]):.1f} | "
          f"eclipse seen (z < -5): T0 {int((a[:, 0] < -5).sum())}, phip {int((a[:, 1] < -5).sum())} | phip better by more than 5 sigma: {int((a[:, 1] < a[:, 0] - 5).sum())}, T0 better: {int((a[:, 0] < a[:, 1] - 5).sum())}")
