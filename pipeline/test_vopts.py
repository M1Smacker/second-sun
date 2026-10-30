"""Tests for the study switches c1b and c2 (vopts.py, stage3_core.resmooth_stats / step_flag). Synthetic light curve, no data files.
1. A 20 h dip on a curve with slow stellar variability: with the 2 d smoothing the sides are lifted (shoulders) and the depth is understated; the re-smoothed measurement has small lifts and the true depth.
2. The guard stays: a real level step right after the dip is still flagged on the re-smoothed curve.
3. c2 ignores the data-cover rule and a missing side; default keeps it.
Usage: python test_vopts.py"""
import numpy as np
import stage2_search as S2, stage3_core as C, vopts as V


def curve(step=0.0, seed=3):
    rng = np.random.default_rng(seed)
    t = np.arange(0, 27, 10 / 1440)
    f = 1 + 3e-4 * rng.normal(size=t.size) + 8e-4 * np.sin(2 * np.pi * t / 4.3)
    tc, dur = 13.0, 20.0
    f -= 5e-3 * np.clip((dur / 2 - np.abs(t - tc) * 24) / (0.2 * dur), 0, 1)
    f[t > tc + dur / 48 + 0.1] += step
    return t, f, tc, dur


def test_shoulders():
    t, f, tc, dur = curve()
    P = S2.Prod(t, f)
    default = C.step_stats(P.bt, P.bf, P.bd, P.med, tc, dur, 3400.0)          # 2 d smoothing; depth as the search reports it (about 0.68 of 5,000)
    r = C.resmooth_stats(P.t, P.f, tc, dur, P.bd)
    assert r is not None
    new, depth = r
    assert 0.9 * 4000 < depth < 1.05 * 4000, f"re-smoothed depth should be the box mean of the trapezoid (0.8 x 5,000 = 4,000 ppm), got {depth:.0f}"
    print(f"PASS shoulders: default lifts {default['lift_pre']:+.2f} / {default['lift_post']:+.2f}, re-smoothed {new['lift_pre']:+.2f} / {new['lift_post']:+.2f}, depth {depth:.0f} ppm (injected 5000)")


def test_guard_stays():
    t, f, tc, dur = curve(step=2.5e-3)
    P = S2.Prod(t, f)
    new, depth = C.resmooth_stats(P.t, P.f, tc, dur, P.bd)
    old = C.step_stats(P.bt, P.bf, P.bd, P.med, tc, dur, 3400.0)
    e = dict(old, lift2_pre=new["lift_pre"], lift2_post=new["lift_post"])
    assert C.step_flag(e), f"a real level step must trip the re-smoothed step test: default {old}, re-smoothed {new}"
    assert not C.step_flag(dict(old)), "finding: the 2 d curve follows a sustained level step, so the default step test does NOT catch it (lift_post 0.07)"
    t0, f0, tc0, dur0 = curve()
    P0 = S2.Prod(t0, f0); n0, d0 = C.resmooth_stats(P0.t, P0.f, tc0, dur0, P0.bd)
    o0 = C.step_stats(P0.bt, P0.bf, P0.bd, P0.med, tc0, dur0, 3400.0)
    assert not C.step_flag(dict(o0, lift2_pre=n0["lift_pre"], lift2_post=n0["lift_post"])), "a clean dip must not be flagged"
    print(f"PASS guard: a +2,500 ppm level step after the dip is flagged (default lifts {old['lift_pre']:+.2f} / {old['lift_post']:+.2f}, re-smoothed {new['lift_pre']:+.2f} / {new['lift_post']:+.2f}); the clean dip is not")


def test_c2_rules():
    base = dict(lift_pre=0.1, lift_post=-0.1, cover_pre=0.2, cover_post=0.9)
    assert C.step_flag(base) is True, "default: under half the data on a side flags"
    none_side = dict(lift_pre=None, lift_post=0.1, cover_pre=0.0, cover_post=0.9)
    assert C.step_flag(none_side) is True
    V.ON = frozenset({"c2"})
    try:
        assert C.step_flag(base) is False and C.step_flag(none_side) is False, "c2: cover and missing sides are not judged"
        assert C.step_flag(dict(lift_pre=0.9, lift_post=0.0, cover_pre=0.0, cover_post=1.0)) is True, "c2 still flags a measured lift"
    finally:
        V.ON = frozenset()
    print("PASS c2 rules: default flags a thin side, c2 ignores it but still flags a measured lift")





def test_c1a_window():
    """c1a: a 4 h dip on a star that varies on 2.5 d: the 2 d window leaves the variability, the 3 x box (0.5 d) window removes more of it, so the dip stands out more."""
    rng = np.random.default_rng(5)
    t = np.arange(0, 27, 2 / 1440)
    f = 1 + 3e-4 * rng.normal(size=t.size) + 1.2e-3 * np.sin(2 * np.pi * t / 2.5)
    f -= 2e-3 * (np.abs(t - 13.0) * 24 < 2)
    P = S2.Prod(t, f); s0 = P.snr_near(13.0, 4.0)
    V.ON = frozenset({"c1a"})
    try:
        P1 = S2.Prod(t, f); s1 = P1.snr_near(13.0, 4.0)
        c, snr, m = P1.scores(4.0); i = np.nanargmax(np.where(np.abs(c - 13.0) < 0.2, snr, np.nan)); depth = (P1.meds[4.0] - m[i]) * 1e6
    finally:
        V.ON = frozenset()
    assert s1 > s0 + 3, f"c1a should raise the SNR of the short dip on a variable star: default {s0:.1f}, c1a {s1:.1f}"
    assert 0.8 * 2000 < depth < 1.2 * 2000, depth
    assert S2.Prod(t, f).snr_near(13.0, 4.0) == s0, "default must be unchanged"
    print(f"PASS c1a: 4 h dip SNR {s0:.1f} with the 2 d window, {s1:.1f} with the 0.5 d window; depth {depth:.0f} ppm (injected 2000)")


def test_c1c_window():
    """c1c: a 20 h dip on a quiet star keeps ~100% of its depth with the 5 x box window (62% with the 2 d window); boxes up to 8 h give bit-identical scores."""
    rng = np.random.default_rng(7)
    t = np.arange(0, 30, 2 / 1440)
    f = 1 + 3e-4 * rng.normal(size=t.size); f -= 1e-3 * (np.abs(t - 15.0) * 24 < 10)
    P0 = S2.Prod(t, f); s0 = P0.snr_near(15.0, 20.0); c0, snr0, m0 = P0.scores(8.0)
    V.ON = frozenset({"c1c"})
    try:
        P1 = S2.Prod(t, f); s1 = P1.snr_near(15.0, 20.0)
        c, snr, m = P1.scores(20.0); i = np.nanargmax(np.where(np.abs(c - 15.0) < 0.3, snr, np.nan)); depth = (P1.meds[20.0] - m[i]) * 1e6
        c8, snr8, m8 = P1.scores(8.0)
    finally:
        V.ON = frozenset()
    assert s1 > 1.1 * s0, f"c1c should raise the SNR of the long dip: default {s0:.1f}, c1c {s1:.1f}"
    assert 0.9 * 1000 < depth < 1.1 * 1000, depth
    assert np.array_equal(snr0, snr8, equal_nan=True) and np.array_equal(m0, m8, equal_nan=True), "8 h box must be bit-identical"
    print(f"PASS c1c: 20 h dip SNR {s0:.1f} with the 2 d window, {s1:.1f} with the 4.2 d window; depth {depth:.0f} ppm (injected 1000); 8 h scores identical")


def test_bf4_floor():
    """bf4: a 3 h dip is found with the 3 h box by default; with the floor no event has a box under 4 h; the grid is restored afterwards."""
    import stage3_core as C
    rng = np.random.default_rng(11)
    t = np.arange(0, 27, 2 / 1440)
    f = 1 + 3e-4 * rng.normal(size=t.size); f -= 2e-3 * (np.abs(t - 13.0) * 24 < 1.5)
    old = S2.DURS_H
    try:
        C.use_grid(S2, C.GRID_V5); d0 = [e["dur_h"] for e in S2.Prod(t, f).events()]
        V.ON = frozenset({"bf4"}); C.use_grid(S2, C.GRID_V5); g = S2.DURS_H; d1 = [e["dur_h"] for e in S2.Prod(t, f).events()]
    finally:
        V.ON = frozenset(); S2.DURS_H = old
    assert d0 and min(d0) == 3, d0
    assert d1 and min(d1) >= 4 and 3 not in g and g == (4, 5, 6.5, 8, 10, 12, 15, 20), (d1, g)
    print(f"PASS bf4: default finds the 3 h dip with box {min(d0)} h; with the floor the boxes are {g} and the event box is {min(d1)} h")


def test_c6_lock():
    """c6: two tier-1 dips on one star, other sectors, 3 binary periods apart, same box and depth, are locked; off by 0.3 period, other kind, depth x3, same sector or a tier-2 partner are not."""
    import pandas as pd
    P = 7.3
    def E(rows):
        return pd.DataFrame([dict(tic=1, kind=k, sector=s, center=c, dur_h=8.0, depth_ppm=dp, tier=t) for k, s, c, dp, t in rows])
    lock = lambda rows: list(C.orbit_locked(E(rows), {1: [P]}))
    assert lock([("real", 10, 100.0, 900, "1A"), ("real", 11, 100.0 + 3 * P, 1000, "1B")]) == [True, True]
    assert lock([("real", 10, 100.0, 900, "1A"), ("real", 11, 100.0 + 3.3 * P, 1000, "1B")]) == [False, False]
    assert lock([("real", 10, 100.0, 900, "1A"), ("flip", 11, 100.0 + 3 * P, 1000, "1B")]) == [False, False]
    assert lock([("real", 10, 100.0, 300, "1A"), ("real", 11, 100.0 + 3 * P, 1000, "1B")]) == [False, False]
    assert lock([("real", 10, 100.0, 900, "1A"), ("real", 10, 100.0 + 3 * P, 1000, "1B")]) == [False, False]
    assert lock([("real", 10, 100.0, 900, "1A"), ("real", 11, 100.0 + 3 * P, 1000, "2")]) == [False, False]
    odd = pd.DataFrame([dict(tic=1, kind="real", sector=10, center=100.0, dur_h=8.0, depth_ppm=900, tier="1A"), dict(tic=1, kind="real", sector=11, center=100.0 + 3 * P, dur_h=20.0, depth_ppm=1000, tier="1B")])
    assert list(C.orbit_locked(odd, {1: [P]})) == [False, False], "box lengths 8 h and 20 h differ by more than 1.6: not a match"
    same = pd.DataFrame([dict(tic=1, kind="real", sector=10, center=100.0, dur_h=8.0, depth_ppm=900, tier="1A"), dict(tic=1, kind="real", sector=11, center=100.0, dur_h=8.0, depth_ppm=1000, tier="1B")])
    assert list(C.orbit_locked(same, {1: [P]})) == [False, False], "zero periods apart is not a lock"
    assert C.tier_of(dict(gap_dump=False, burst=False, flipmatch=False, c5=False, orbit_lock=True)) == "2"
    print("PASS c6: a locked pair is found; off-period, other kind, depth x3, same sector and tier-2 partners are not; a locked event is tier 2")


if __name__ == "__main__":
    test_shoulders(); test_guard_stays(); test_c2_rules(); test_c1a_window(); test_c1c_window(); test_bf4_floor(); test_c6_lock()
