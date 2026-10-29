"""Vesper study phase A2: WHY the flat-baseline (step) flag fires on injected planet-shaped dips. Injects one dip (K x the 8 h box noise, box 8 h and 20 h, dip only) into random star-sectors through the whole
0.7.1 chain (chain_recovery harness) and records the step measurements of the recovered primary event: data cover before and after (rule: under 0.5 flags) and the lift before and after in units of the
dip depth (rule: |lift| over 0.5 flags; a positive lift means the side sits ABOVE the median, as a smoothing shoulder would). Aggregates only.
Usage: SS_SET=g2 SS_RUN=dev_73f62615e365 python step_causes.py [n_groups] [procs]   (writes research\\stage3\\step-causes-0.7.1.txt)"""
import sys, random, multiprocessing as mp
import numpy as np, pandas as pd
import chain_recovery as X, stage3_core as C

K = 12.0


def one(args):
    tic, sec = args
    try:
        paths, best, base, prods = X.baseline(tic, sec)
        if not prods:
            return []
        a = max(prods.values(), key=lambda d: d["t"].max() - d["t"].min()); n8 = X.noise(a["t"], a["f"], 8.0)
        bc = base[["center", "dur_h"]].values if len(base) else np.empty((0, 2))
        rng = np.random.default_rng([20261029, tic, sec]); out = []
        for dur in (8.0, 20.0):
            tc = X.pick_tc(a["t"], bc, dur, rng)
            if tc is None or not np.isfinite(n8):
                continue
            X.INJ.update(tc=tc, dur_h=dur, depth_ppm=K * n8, sign=1)
            ev = X.merged(X.chain(tic, sec, paths, best)[0], tic, sec, best)
            X.INJ.clear()
            if not len(ev):
                continue
            near = ev[(ev.kind == "real") & ev.primary & (np.abs(ev.center - tc) <= 0.5 * np.maximum(dur, ev.dur_h) / 24 + 0.1)]
            if not len(near):
                continue
            r = near.sort_values("snr", ascending=False).iloc[0]
            out.append(dict(dur=dur, step=bool(r.get("step")), tier=r["tier"], box=r["dur_h"], cover_pre=r.get("cover_pre"), cover_post=r.get("cover_post"),
                            lift_pre=r.get("lift_pre"), lift_post=r.get("lift_post"), depth_ratio=r["depth_ppm"] / (K * n8)))
        return out
    except Exception as e:
        return [dict(error=f"{type(e).__name__}: {str(e)[:80]}")]


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    X.PREP.mkdir(parents=True, exist_ok=True); X.TMP.mkdir(parents=True, exist_ok=True)
    raw = X.PREP / f"raw_{X.RUN.name}.pkl"
    if not raw.exists():
        X.build_raw(raw)
    gl = [tuple(int(x) for x in p.stem.split("_")) for p in sorted((X.RUN / "groups").glob("*.json"))]
    random.Random(20261030).shuffle(gl)
    rows = []
    with mp.Pool(procs, initializer=X.init, initargs=(str(raw),)) as pool:
        for r in pool.imap_unordered(one, gl[:n]):
            rows += r
    d = pd.DataFrame(rows)
    txt = [f"Why the step flag fires on injected dips (Vesper 0.7.1, {C.DS.NAME}, {n} random star-sectors, depth {K:g} x the 8 h box noise, one 8 h and one 20 h dip each). Errors: {int(d.get('error', pd.Series(dtype=str)).notna().sum())}."]
    d = d[d.get("dur").notna()] if "dur" in d else d
    for dur, g in d.groupby("dur"):
        s = g[g.step]
        cov = (s[["cover_pre", "cover_post"]].min(axis=1) < C.STEP_COVER)
        lp, lq = s.lift_pre.abs() > C.STEP_LIFT, s.lift_post.abs() > C.STEP_LIFT
        lifts = pd.concat([s.lift_pre, s.lift_post]).dropna()
        txt.append(f"  box {dur:4.0f} h: recovered as primary {len(g)}; step flag {len(s)} ({100 * len(s) / max(len(g), 1):.0f}%); of those: too little data on a side {int(cov.sum())}, lift over 0.5 before {int(lp.sum())}, after {int(lq.sum())}, lift only (data fine) {int((~cov & (lp | lq)).sum())}")
        txt.append(f"    lift values on flagged events (units of the dip depth; + = side above the median): quartiles {np.percentile(lifts, [25, 50, 75]).round(2).tolist() if len(lifts) else []}, share positive {100 * (lifts > 0).mean():.0f}%")
        txt.append(f"    lift on NOT-flagged events: quartiles {np.percentile(pd.concat([g[~g.step].lift_pre, g[~g.step].lift_post]).dropna(), [25, 50, 75]).round(2).tolist() if (~g.step).any() else []}")
        txt.append(f"    recovered depth / injected depth: median {g.depth_ratio.median():.2f} (smoothing and box fit together); box length found: median {g.box.median():.1f} h")
    print("\n".join(txt))
    (C.ROOT / "research" / "stage3" / f"step-causes-0.7.1-{C.DS.NAME}.txt").write_text("\n".join(txt), encoding="utf-8")
