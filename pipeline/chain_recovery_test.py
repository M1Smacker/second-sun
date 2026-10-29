"""Tests for chain_recovery.py (29 Oct 2026). Needs the real v7 run on this machine (data\\stage3\\fd788be04650) and takes a few minutes.
1. signal(): shape, sign and depth of the injected trapezoid (pure).
2. identity: with nothing injected, the harness gives EXACTLY the real run's events, tiers and flags for the same star-sectors (SPOC family with a SAP twin, QLP only, and star-sectors with no event).
3. deep dips come back as primary events, in both signs; a harness that ignores the injection or flips its sign fails (two mutations, run in this file).
Usage: python chain_recovery_test.py   (prints PASS lines and the time one injection takes)"""
import time, numpy as np, pandas as pd
import chain_recovery as X
import stage3_report as R
import sap_twin as T


def test_signal():
    t = np.linspace(0, 2, 2001)
    s = X.signal(t, 1.0, 8.0, 1000.0, 1)
    assert abs(s.min() + 1e-3) < 1e-9 and s.max() == 0 and abs(t[np.argmin(s)] - 1.0) < 0.2, "dip: 1000 ppm deep, below the baseline, centred"
    assert np.all(X.signal(t, 1.0, 8.0, 1000.0, -1) == -s), "a bump is the mirror of a dip"
    w = t[s < -0.5e-3]; assert 0.75 * 8 / 24 < w.max() - w.min() < 0.85 * 8 / 24, "width at half depth is 0.8 of the base (20 percent ingress and egress), the base is the box length"
    print("PASS signal")


def key(ev):
    return sorted((r.kind, r.product, round(float(r.center), 3), round(float(r.snr), 2), str(r.tier), bool(r.primary), str(r.seen_by), bool(r.common)) for r in ev.itertuples())


def pick_groups(real):
    """Deterministic: 3 SPOC-family groups with events, 2 QLP-best with events, 2 with no event at all."""
    g = real.groupby(["tic", "sector"]).agg(best=("best", "first"), n=("kind", "size")).reset_index()
    fam, qlp = g[g.best.isin(T.FAMILY)].sort_values(["n", "tic", "sector"]), g[~g.best.isin(T.FAMILY)].sort_values(["n", "tic", "sector"])
    pick = list(fam.iloc[[len(fam) // 4, len(fam) // 2, 3 * len(fam) // 4]].itertuples(index=False)) + list(qlp.iloc[[len(qlp) // 3, 2 * len(qlp) // 3]].itertuples(index=False))
    return [(int(r.tic), int(r.sector)) for r in pick]


def test_identity(real):
    n = 0
    for tic, sec in pick_groups(real):
        _, best, base, _ = X.baseline(tic, sec)
        want = real[(real.tic == tic) & (real.sector == sec)]
        assert key(base) == key(want), (tic, sec, key(base)[:3], key(want)[:3])
        n += len(want)
    print(f"PASS identity: harness == real run on 5 star-sectors, {n} events (flags, tiers, union, common-moment pool all equal)")


def test_deep():
    hits, t0 = 0, time.time()
    for tic, sec in X.W["deep"]:
        paths, best, base, prods = X.baseline(tic, sec)
        a = max(prods.values(), key=lambda d: d["t"].max() - d["t"].min()); n8 = X.noise(a["t"], a["f"], 8.0)
        bc = base[["center", "dur_h"]].values if len(base) else np.empty((0, 2)); tc = X.pick_tc(a["t"], bc, 8.0, np.random.default_rng(1))
        for sign in (1, -1):
            X.INJ.update(tc=tc, dur_h=8.0, depth_ppm=25 * n8, sign=sign)
            evs, _ = X.chain(tic, sec, paths, best)
            r = X.row_of(X.merged(evs, tic, sec, best), "real" if sign == 1 else "flip", tc, 8.0)
            hits += r["found_primary"]
        X.INJ.clear()
    return hits, (time.time() - t0) / (2 * len(X.W["deep"]) + len(X.W["deep"]))


if __name__ == "__main__":
    test_signal()
    X.PREP.mkdir(parents=True, exist_ok=True); X.TMP.mkdir(parents=True, exist_ok=True)
    raw = X.PREP / f"raw_{X.RUN.name}.pkl"
    if not raw.exists():
        X.build_raw(raw)
    X.init(str(raw))
    real, _ = R.load(str(X.RUN / "groups"))
    test_identity(real)
    X.W["deep"] = [g for g in pick_groups(real)[:2] + pick_groups(real)[3:4]]
    hits, per = test_deep()
    assert hits >= 5, f"deep dips (25 x noise, 8 h) should come back as primary events in nearly every case: {hits} of 6"
    print(f"PASS deep: {hits} of 6 deep injections (3 star-sectors x 2 signs) are primary events; about {per:.1f} s per chain run")
    # mutation 1: the injection is ignored -> nothing is found, the test must fail
    orig = X.signal; X.signal = lambda t, **k: np.zeros_like(t)
    h1, _ = test_deep(); X.signal = orig
    assert h1 < hits, f"mutation 'injection ignored' should lose the dips: {h1} vs {hits}"
    # mutation 2: the sign is flipped -> real-path dips become bumps and vice versa; with the kind check this loses every recovery
    X.signal = lambda t, tc, dur_h, depth_ppm, sign: orig(t, tc, dur_h, depth_ppm, -sign)
    h2, _ = test_deep(); X.signal = orig
    assert h2 < hits, f"mutation 'sign flipped' should lose the dips: {h2} vs {hits}"
    print(f"PASS mutations: ignored injection {h1} of 6, flipped sign {h2} of 6 (against {hits} of 6)")
