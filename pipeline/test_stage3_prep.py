"""Phase E1 self-checks (Compass review 2026-10-27). Each check proves one claim the Stage 3 preparation rests on.
Run: .venv\\Scripts\\python.exe pipeline\\test_stage3_prep.py   (from D:\\second-sun; the dry-run check needs `python stage3.py dry` to have run first)"""
import re, glob, json, pathlib
import numpy as np, pandas as pd
import stage3_core as C
import stage3_report as R

D2 = C.ROOT / "data" / "stage2"
DRY = C.ROOT / "data" / "stage3_dry" / "groups"


def ev(**k):
    base = dict(tic=1, center=100.0, flags="", burst_n=0, c8_n=0, c8_best=None, gap_dump=False, flipmatch=False, burst=False, c5=False)
    return {**base, **k}


def test_tier_rules():
    assert C.tier_of(ev()) == "1B"                                        # no second product: unconfirmable, never a "candidate"
    assert C.tier_of(ev(c8_n=1, c8_best=5.0)) == "1A"
    assert C.tier_of(ev(c8_n=1, c8_best=4.0)) == "1A"
    assert C.tier_of(ev(c8_n=2, c8_best=3.5)) == "1L"
    assert C.tier_of(ev(c8_n=1, c8_best=2.0)) == "3"
    for k in ("gap_dump", "burst", "flipmatch", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated"):                    # any flag: tier 2, kept
        assert C.tier_of(ev(c8_n=1, c8_best=9.0, **{k: True})) == "2", k
    f = C.flags_of(dict(flags="gap edge; flipped", burst_n=3))
    assert f == dict(gap_dump=True, flipmatch=True, burst=True), f
    assert C.flags_of(dict(flags="", burst_n=2)) == dict(gap_dump=False, flipmatch=False, burst=False)


def test_ephemeris_matches_stage2_report():
    p = D2 / "events_real_LOCAL.csv"
    if not p.exists():
        print("  (skipped: no Stage 2 local events)"); return
    old = pd.read_csv(p); eph = C.Ephem(pd.read_csv(C.TARGETS, comment="#"))
    d = np.array([eph.dist(r.tic, r.center) for r in old.itertuples()])
    assert np.allclose(d, old.ph_d.values, atol=1e-9, equal_nan=True), "phase distance differs from stage2_report"
    assert ((d < C.PH_D) == old.c5.values).all(), "C5 flag differs from stage2_report"
    print(f"  {len(old)} Stage 2 real events: phase distance and C5 identical")


def test_campaign_class_sizes_are_what_stage2_hard_coded():
    sizes, total, nan = C.class_sizes()
    assert (sizes["bright<11"], sizes["mid11-12"], sizes["faint12+"]) == (801, 1067, 3196) and total == 5064 and nan == 0, (sizes, total, nan)


def parse(line):
    return [int(x) for x in re.findall(r"(\d+)\s*(?:\||$)", line.strip())]


def test_waterfall_reproduces_stage2():
    ev2, _ = R.load(D2 / "groups", extra=False)
    E = ev2[ev2.primary]
    txt = (C.ROOT / "research" / "stage2-2026-10-23" / "aggregate.txt").read_text(encoding="utf-8").splitlines()
    want = {l.split()[0]: parse(l) for l in txt if "no gap/dump flag" in l and "start" in l}
    got = {"real": list(R.waterfall(E[E.kind == "real"])), "upside-down": list(R.waterfall(E[E.kind == "flip"]))}
    assert got == want, (got, want)
    surv = E[(E.kind == "real") & E.tier.isin(["1A", "1L", "1B"])]
    assert len(surv) == got["real"][5], "tiers 1A+1L+1B must equal Stage 2's lenient survivors"
    print(f"  real {got['real']} | upside-down {got['upside-down']} (identical to the published Stage 2 aggregate)")


def test_v2_flags():
    tg = pd.DataFrame(dict(tic=[1, 2, 3], bjd0=[2457000.0 + 57000 - 2457000 + 0.0] * 3, p_bin_d=[67.7, 12.7, 67.7], tic_radius_rsun=[10.9, 0.48, np.nan]))
    tg["bjd0"] = 57000.0                                                  # eclipse centre at t = 0 in the Ephem's own frame (bjd0 - 57000)
    eph = C.Ephem(tg)
    assert eph.overlap(1, 0.8, 3), "giant: an event 0.8 d from the eclipse centre sits inside the physical eclipse"
    assert not eph.overlap(1, 20.0, 3), "far from both eclipses"
    assert eph.overlap(1, 67.7 / 2 + 0.9, 3), "secondary at phase 0.5 counts too"
    assert not eph.overlap(2, 1.3, 15), "dwarf pair: a 15 h event 1.3 d from a 0.13 d eclipse does not overlap"
    assert not eph.overlap(2, 3.0, 3), "dwarf pair, event 3 d from the eclipse: no overlap"
    assert not eph.overlap(3, 0.0, 3), "no TIC radius: never flagged by this rule"
    g = dict(events=[dict(tic=1, kind="real", product="QLP", center=20.0, dur_h=3, flags="", burst_n=0, c8_n=0, c8_best=None) for _ in range(3)]
             + [dict(tic=1, kind="flip", product="QLP", center=20.0, dur_h=3, flags="", burst_n=0, c8_n=0, c8_best=None) for _ in range(2)])
    out = C.enrich_group(g, eph, set())
    assert [e["repeater"] for e in out] == [True] * 3 + [False] * 2 and all(e["tier"] == "2" for e in out[:3]) and out[3]["tier"] == "1B", out
    assert not any(e["repeater"] or e["ecl_overlap"] for e in C.enrich_group(g, eph, set(), extra=False))


def test_step_test():
    bd = 1 / 144; bt = np.arange(0, 6, bd)
    def run(f, center=3.0, dur=4.0, depth=5000.0, t=bt):
        s = C.step_stats(t, f, bd, np.median(f), center, dur, depth)
        return s, C.step_flag(s)
    box = np.ones_like(bt); box[np.abs(bt - 3) < 2 / 24] -= 5000e-6
    s, fl = run(box); assert not fl and abs(s["lift_pre"]) < 0.05 and abs(s["lift_post"]) < 0.05 and s["cover_pre"] > 0.99, ("box must pass", s)
    step = np.ones_like(bt); step[bt > 3 - 2 / 24] -= 5000e-6                      # drops and stays down: an eclipse edge or a level shift
    assert run(step)[1], "step must be flagged"
    ring = box.copy(); ring[(bt > 3 + 2 / 24) & (bt < 3 + 6 / 24)] += 4000e-6      # overshoot after the dip: detrender ringing on a ramp
    assert run(ring)[1], "overshoot must be flagged"
    k = bt > 2.9                                                                    # event at the start of the data: nothing before it
    s, fl = run(box[k], t=bt[k], center=3.0); assert fl and s["cover_pre"] < C.STEP_COVER, ("no baseline", s)
    assert not C.step_flag(dict(tic=1)), "never measured: not flagged (Stage 2 data)"
    e = dict(**s, tic=1)                                                            # enrich: flagged in tier, and switched off for Stage 2 regressions
    ev_ = dict(tic=1, kind="real", product="QLP", center=3.0, dur_h=4, flags="", burst_n=0, c8_n=0, c8_best=None, **s)
    eph = C.Ephem(pd.DataFrame(dict(tic=[1], bjd0=[57000.0], p_bin_d=[67.7], tic_radius_rsun=[np.nan])))
    o = C.enrich_group(dict(events=[ev_]), eph, set())[0]; assert o["step"] and o["tier"] == "2"
    assert not C.enrich_group(dict(events=[ev_]), eph, set(), extra=False)[0]["step"]


def test_v4_flags():
    base = dict(tic=1, product="QLP", dur_h=3, flags="", burst_n=0, c8_n=0, c8_best=None)
    one = pd.DataFrame(dict(tic=[1], bjd0=[57000.0], p_bin_d=[10.0], tic_radius_rsun=[np.nan]))
    eph = C.Ephem(one, {1: (0.1, 0.05)})
    # measured widths: primary 1.0 d, secondary 0.5 d (works without a TIC radius)
    assert eph.overlap(1, 0.45, 3) and not eph.overlap(1, 0.7, 3) and eph.overlap(1, 5.3, 3) and not eph.overlap(1, 5.4, 3), "measured widths"
    assert not C.Ephem(one).overlap(1, 0.45, 3), "no width and no radius: never flagged"
    g = dict(events=[dict(base, kind="real", center=22.0, snr=8.0, ramp_d=0.5), dict(base, kind="flip", center=32.0, snr=9.0, ramp_d=3.0),
                     dict(base, kind="real", center=42.0, snr=12.0, ramp_d=None), dict(base, product="SPOC", kind="real", center=22.0, snr=8.0, ramp_d=2.0)])
    o = C.enrich_group(g, eph, set())
    assert [e["ramp"] for e in o] == [True, False, False, False], "ramp: 0.5 d after data resumed yes, 3 d no, unknown no"
    # QLP: real 8, flip 9, real 12. Real 8 and flip 9 are both dominated by a stronger event of the other kind (flip 9 by real 12; real 8 by flip 9); real 12 beats the flip 9; SPOC has no upside-down event
    assert [e["dominated"] for e in o] == [True, True, False, False], [e["dominated"] for e in o]
    assert [e["tier"] for e in o] == ["2", "2", "1B", "1B"], [e["tier"] for e in o]
    tie = dict(events=[dict(base, kind="real", center=2.0, snr=9.0, ramp_d=None), dict(base, kind="flip", center=3.0, snr=9.0, ramp_d=None)])
    assert all(e["dominated"] for e in C.enrich_group(tie, eph, set())), "a tie dominates both (symmetric)"
    assert not any(e["ramp"] or e["dominated"] for e in C.enrich_group(g, eph, set(), extra=False))


def test_grid_v5_sees_a_20_hour_dip():
    import stage2_search as S2
    rng = np.random.default_rng(3); t = np.arange(0, 27, 2 / 1440); f = 1 + rng.normal(0, 1000e-6, t.size)
    f[np.abs(t - 13.3) < 10 / 24] -= 3000e-6                                           # a 20 h box dip, 3000 ppm, in white noise (1000 ppm per 2 min)
    old = S2.DURS_H
    try:
        C.use_grid(S2, C.GRID_V4); e4 = S2.Prod(t, f).events()
        C.use_grid(S2, C.GRID_V5); e5 = S2.Prod(t, f).events()
    finally:
        S2.DURS_H = old
    assert C.GRID_V5 == C.GRID_V4 + (20,) and e4 and max(e["dur_h"] for e in e4) <= 15, "the old grid stops at 15 h"
    assert e5 and e5[0]["dur_h"] == 20 and e5[0]["snr"] > e4[0]["snr"], (e4[:1], e5[:1])
    assert S2.DURS_H == old, "use_grid must only change the module name it is given"


def test_noise_expected_and_ratio_table():
    lam, p = R.noise_expected(12, 33, 2.3)
    assert abs(lam - 33 / 2.3) < 1e-9 and 0.6 < p < 0.8, (lam, p)                        # 12 real against 14.3 expected: nothing unusual
    assert R.noise_expected(40, 33, 2.3)[1] < 1e-6 and R.noise_expected(0, 0, 2.0) == (0.0, 1.0)
    assert R.noise_expected(20, 33, 2.3)[1] < R.noise_expected(15, 33, 2.3)[1], "more real events must be less likely under noise alone"
    r, name = R.asym_ratios("v4-does-not-exist")                                         # falls back to the v4 file, whose bars are known
    assert name == "asymmetry.txt" and r[7.0] == 2.30 and r[10.0] == 2.07 and set(r) == {4.5, 5.0, 6.0, 7.0, 8.0, 10.0}, (name, r)


def test_settings_hash_changes_with_any_setting():
    s = dict(snr_threshold=7.0, durs_h=[3, 4], code=dict(a="x"))
    h = C.settings_hash(s)
    assert h == C.settings_hash(json.loads(json.dumps(s)))
    assert h != C.settings_hash({**s, "snr_threshold": 6.5})
    assert h != C.settings_hash({**s, "code": dict(a="y")})


def test_c5_timeline_cover_is_small_and_known():
    cov = C.c5_timeline_cover()
    assert len(cov) == 549 and cov.max() < 0.3 and int((cov >= 0.2).sum()) == 70, (cov.max(), int((cov >= 0.2).sum()))


def test_dry_runs_match_stage2():
    for d in (DRY, C.ROOT / "data" / "stage3_dry50" / "groups"):
        check_dry(d)


def check_dry(d):
    fs = sorted(glob.glob(str(d / "*.json")))
    if not fs:
        print(f"  (skipped: {d.parent.name} has no groups; run `python stage3.py dry` or `dry50` first)"); return
    n_ev = 0
    for p in fs:
        new = json.load(open(p)); old_p = D2 / "groups" / pathlib.Path(p).name
        old = json.load(open(old_p))
        assert new["meta"] == old["meta"] and new["inj"] == old["inj"], p
        assert len(new["events"]) == len(old["events"]), p
        for a, b in zip(old["events"], new["events"]):
            assert all(b[k] == v or (v != v and b[k] != b[k]) for k, v in a.items()), (p, a, b)     # NaN equals NaN here
            assert "tier" in b and "c5" in b and "ph_d" in b
        n_ev += len(old["events"])
    print(f"  {d.parent.name}: {len(fs)} groups, {n_ev} events: identical to Stage 2 on every old field, plus the new fields")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("pass:", name)
