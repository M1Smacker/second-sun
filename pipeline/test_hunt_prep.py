"""Stage 0 self-checks for the hunt (2026-10-23): B3 (mask all periods), B4 (flip match as a flag), same-moment filter.
Each check shows the problem first, then the fix. Run: .venv\\Scripts\\python.exe pipeline\\test_hunt_prep.py"""
import numpy as np
from detect_v2 import find_events, mask_all_periods, eclipse_mask_auto, veto
from common_time import common_time_flags

STARS = [1683, 1711, 2390, 2419, 2743, 2770, 2797, 3311, 3338, 3474, 3502, 3529]


def two_binary_star(rng):
    """Like KIC 4150611: an 8.65 d binary plus a second 1.5223 d signal that the catalogue cut dropped."""
    t = np.concatenate([np.arange(s, s + 25, 200 / 86400) for s in STARS])
    f = 1 + rng.normal(0, 800e-6, t.size)
    for P, dur, dep, t0 in ((8.65, 5, 0.03, 1690.3), (1.5223, 2.5, 0.004, 1690.0)):
        ph = ((t - t0 + P / 2) % P) - P / 2
        f[np.abs(ph) < dur / 48] -= dep
    return t, f


def test_b3_mask_all_periods():
    t, f = two_binary_star(np.random.default_rng(5))
    keep, _ = eclipse_mask_auto(t, f, 8.65)                      # what the old pipeline did: only the kept period
    n_old = len(find_events(t[keep], f[keep]))
    t2, f2 = mask_all_periods(t, f, [8.65, 1.5223])
    n_new = len(find_events(t2, f2))
    assert n_old > 20, f"expected the unmasked 1.52 d binary to flood the search, got {n_old}"
    assert n_new <= 3, f"masking both periods should leave almost nothing, got {n_new}"
    assert len(t2) > 0.5 * len(t), "the double mask removed too much data"
    print(f"  B3: one period masked -> {n_old} events; both -> {n_new}")


def test_b4_flip_match_is_a_flag():
    ev = [dict(center=10.0, dur_h=6.5, snr=8.0, depth_ppm=1500)]
    flipped = [dict(center=10.1, dur_h=5, snr=7.5, depth_ppm=1000)]
    none = np.array([])
    k, r = veto(ev, none, none, flipped)                          # default: published behaviour, event deleted
    assert len(k) == 0 and len(r) == 1
    k, r = veto(ev, none, none, flipped, flip_action="flag")      # hunt behaviour: event kept and flagged
    assert len(k) == 1 and len(r) == 0 and any("flipped" in x for x in k[0]["flags"]), k
    k, r = veto(ev, none, none, [], flip_action="flag")
    assert len(k) == 1 and not k[0]["flags"]


def test_same_moment_filter():
    rng = np.random.default_rng(3)
    centers = []
    while len(centers) < 40:                                  # random events, kept at least 0.5 d from the burst below
        c = float(rng.uniform(1683, 1708))
        if abs(c - 1690.5) > 0.5:
            centers.append(c)
    evs = [dict(tic=1000 + i, sector=14, camera=1, center=c) for i, c in enumerate(centers)]
    evs += [dict(tic=2000 + i, sector=14, camera=1, center=1690.50 + 0.01 * i) for i in range(4)]   # 4 stars, same moment
    near = common_time_flags(evs + [dict(tic=4000, sector=14, camera=1, center=1690.45)])[-1]
    assert near["flags"], "an event inside a spacecraft burst must be flagged"
    evs += [dict(tic=3000, sector=14, camera=2, center=1690.50)]                                    # other camera: not a match
    out = common_time_flags(evs)
    flagged = {e["tic"] for e in out if e["flags"]}
    assert flagged >= {2000, 2001, 2002, 2003}, flagged
    assert 3000 not in flagged, "a different camera must not match"
    assert len([t for t in flagged if t < 2000]) <= 1, "random events should almost never be flagged"
    print(f"  same-moment: {len(flagged)} of {len(evs)} flagged ({sorted(flagged)[:6]}...)")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("pass:", name)
