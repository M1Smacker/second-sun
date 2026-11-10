"""C1 tuning on PLANTED material only (10 Nov 2026, Opus 5.5). For each sampled file: a synthetic recurring eclipse (trapezoid, width 3 to 8 h, depth Ke x 8 h noise,
Ke in 6 / 15 / 40, random binary phase at least 3 widths from the catalogue windows) is pasted into this sector AND every other sector of the star (SYNTH hook), plus
ONE planted single dip (8 h, K 12) in this sector. For each threshold Z: share of the synthetic eclipse cadences C1 removes (C0 for reference), real-arm events left at
the synthetic eclipses, share of the planted dip removed, planted dip found. Counts only. Usage: SS_SET=g2|g3 python c1_synth_test.py N_PER"""
import os, sys, pathlib, multiprocessing as mp
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, pandas as pd
import wo_f01a_mask_loss as H
import c0_catalogue_mask as C0
import c1_mask as C1

ZS = (3.0, 4.0, 5.0, 6.0); KES = (6.0, 15.0, 40.0)


def one(args):
    path, tic, P, fam, lo, i = args
    try:
        tf, meta, st = H.load_windowed(path)
        c = C0.cat().get(tic)
        if tf is None or c is None or not np.isfinite(c["wp"]):
            return []
        t, f = tf; win = C0.windows(t, c)[0]
        n8 = H.noise(t[~win], f[~win], 8.0)
        if not np.isfinite(n8):
            return []
        rng = np.random.default_rng([tic, i, 77]); Ke = KES[i % 3]; ws = rng.uniform(3, 8); depth = Ke * n8
        for _ in range(50):
            phs = rng.uniform(0, 1); probe = c["T0"] + phs * c["P"] + c["P"] * np.arange(-2, 3)
            if not C0.windows(probe, c, padf=1.5 + 6 * c["wp"] / max(c["wp"], 1e-9) / 1.5)[0].any():
                break
        def synth(tc_, tt):
            dt = ((tt - c["T0"] - phs * c["P"] + c["P"] / 2) % c["P"]) - c["P"] / 2
            return H.signal(dt, 0.0, ws, depth, 1)
        C1.SYNTH = synth
        fs = f + synth(tic, t)
        dt = ((t - c["T0"] - phs * c["P"] + c["P"] / 2) % c["P"]) - c["P"] / 2; core = np.abs(dt) < ws / 48
        ok = ~win & ~core & (np.abs(dt) > 1.0) & (t - t.min() > 1.5) & (t.max() - t > 1.5)
        if ok.sum() < 10 or core.sum() < 5:
            return []
        tp = float(rng.choice(t[ok])); fsp = fs + H.signal(t, tp, 8.0, 12 * n8, 1); dip = np.abs(t - tp) < 8 / 48
        cen = c["T0"] + (np.round((t - c["T0"]) / c["P"] - phs) + phs) * c["P"]; cens = np.unique(np.round(cen[core], 3))
        def leak(keep):
            ev = H.S2.Prod(t[keep], fsp[keep]).events()
            return sum(any(abs(e["center"] - x) < ws / 48 + 0.1 for x in cens) for e in ev)
        def fnd(keep):
            return any(abs(e["center"] - tp) <= 0.5 * max(8, e["dur_h"]) / 24 + 0.1 for e in H.S2.Prod(t[keep], fsp[keep]).events())
        base = dict(bin_lo=lo, slow=P >= C1.PSLOW, Ke=Ke, catch_c0=float(win[core].mean()), leak_c0=leak(~win), found_c0=fnd(~win))
        rows = []
        for z in ZS:
            C1.Z = z; C1._OTHER.clear(); C1.STATS.clear()
            rm = C1.remove(t, fsp, H.A.PER.get(tic, []), tic)
            s = C1.STATS.get(tic, {})
            rows.append(dict(base, Z=z, catch=float(rm[core].mean()), dipcut=float(rm[dip].mean()), leak=leak(~rm), found=fnd(~rm), cut=float(rm.mean()),
                             rec=s.get("rec", 0), single=s.get("single", 0)))
        return rows
    except Exception as e:
        return [dict(err=f"{type(e).__name__}: {str(e)[:60]}")]


if __name__ == "__main__":
    jobs, _ = H.sample(int(sys.argv[1]))
    with mp.Pool(6, initializer=H.init) as pool:
        df = pd.DataFrame([r for rr in pool.map(one, jobs) for r in rr])
    if "err" in df:
        print("errors:", df.err.notna().sum(), df.err.dropna().unique()[:3]); df = df[df.err.isna()]
    print(f"C1 synthetic test, set {H.SET}: {df.groupby('Z').size().iloc[0]} files with a synthetic eclipse and a planted dip")
    print("Z  speed  Ke | eclipse cadences removed C1 (C0) | real-arm events at the synthetic eclipse C1 (C0) | planted dip: share removed, found C1 (C0) | cadences removed | runs recurring/single")
    for (z, slow, ke), g in df.groupby(["Z", "slow", "Ke"]):
        print(f"{z:3g} {'slow' if slow else 'fast'} {ke:4g} n{len(g):3d} | {g.catch.mean():.2f} ({g.catch_c0.mean():.2f}) | {int(g.leak.sum()):3d} ({int(g.leak_c0.sum()):3d}) | "
              f"{g.dipcut.mean():.3f}, {g.found.astype(float).mean():.2f} ({g.found_c0.astype(float).mean():.2f}) | {g.cut.mean():.3f} | {int(g.rec.sum())}/{int(g.single.sum())}")
    for (z, slow), g in df.groupby(["Z", "slow"]):
        print(f"Z {z:g} {'slow' if slow else 'fast'}: eclipse removed {g.catch.mean():.2f}; leak events {int(g.leak.sum())} (C0 {int(g.leak_c0.sum())}); planted dip removed {g.dipcut.mean():.3f}, found {g.found.astype(float).mean():.2f} (C0 {g.found_c0.astype(float).mean():.2f})")
