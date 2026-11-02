"""Vesper 0.9 study analysis (2 Nov 2026). Applies the accept rules of research/stage3/V9-STUDY-PLAN.md mechanically to the DEVELOPMENT slice. The sealed slice is never read here.
Usage: SS_SET=g2 python v9_study_analysis.py      (writes research\\stage3\\v9-study-results.txt; aggregates only, no star IDs, no event times)

READING OF THE PLAN FIXED BEFORE ANY NUMBER WAS LOOKED AT (the plan says "no development event of depth 30% or less changes tier because of dg and nd"; for nd that is ambiguous, because
releasing real events from a broken light curve's dominance IS its purpose):
  dg: accepted only if no event of depth 30% or less and with a finite depth changes tier because of it, and no planted dip is lost.
  nd: accepted only if every event whose `dominated` flag changes (a) sits in a light curve that holds an unphysical event, and (b) changes in one direction only, dominated -> not dominated.
      Events released that way may move to tier 1; they are listed as a count (real and upside-down), never judged by how many real ones appear.
  both: the mirror gap of the planted dips and bumps stays within 3 points.
fl is judged exactly as written in the plan (four conditions, threshold = the largest fall among 0.5, 1.0, 1.5 that still meets 2 to 4); upside-down events removed are counted on the
development run itself (the plan does not ask for a rescale to the sealed slice size; a per-1,000-star-sector figure is printed beside it for information).
The 'alone' variants are recomputed with the very same tier code (stage3_core.tier_of and the orbit-lock pass of stage3_report.apply_v7) and checked against the two real runs first."""
import os, sys, pathlib
os.environ.setdefault("SS_SET", "g2")
import numpy as np, pandas as pd
import stage3_core as C, stage3_report as R, vopts

ROOT = C.ROOT
RUNS = C.DS.RUNS
# The 0.8.0 baseline is a fresh run (options c6 only) under TODAY'S manifest: the 29 Oct development run (dev_73f62615e365) is not like for like, because a QLP-only star-sector borrows its good-time
# windows from neighbouring stars in the manifest, and the manifest grew after the sealed download (77 of 583 such groups changed events on 2 Nov; own-SPOC groups never did).
BASE_RUN, NEW_RUN = "dev_428c5fb454cd", "dev_8bbb1568d6a3"
BASE_ROWS, NEW_ROWS = ROOT / "data" / "chain_recovery_g2" / "rows_v9base.pkl", ROOT / "data" / "chain_recovery_g2" / "rows_v9dev.pkl"
T1 = ("1A", "1L", "1B")
THR = (0.5, 1.0, 1.5)
PRICE_STEP = 6.8                    # upside-down events per planted tier-1 point, the step check (31 Oct 2026); the plan's bar for fl
OUT = []
P = lambda s="": (OUT.append(s), print(s, flush=True))


def load(run, opts):
    vopts.ON = frozenset(opts)                                  # read at call time by stage3_core and stage3_report
    ev, meta = R.load(str(RUNS / run / "groups"))
    return ev[ev.primary].copy(), meta


def key(E):
    return E.tic.astype(int).astype(str) + "|" + E.sector.astype(int).astype(str) + "|" + E.kind + "|" + E["product"] + "|" + E.center.round(4).astype(str) + "|" + E.dur_h.astype(str)


def periods_of(E):
    ep = C.Ephem(pd.read_csv(C.TARGETS, comment="#"), C.eb_widths())
    return {int(t): [p for _, p, _ in ep.by.get(int(t), [])] for t in set(E.tic)}


def retier(E, dom, deep, flare, per):
    """The tier of every event under the given flag columns: the order of apply_v7 (tiers without orbit_lock, then the orbit-lock pass, then re-tier those)."""
    base = E.drop(columns=[c for c in ("dominated", "too_deep", "flare", "orbit_lock", "tier") if c in E]).to_dict("records")
    mk = lambda r, d, td, fl, ol: C.tier_of({**r, "dominated": bool(d), "too_deep": bool(td), "flare": bool(fl), "orbit_lock": bool(ol)})
    t0 = [mk(r, d, td, fl, False) for r, d, td, fl in zip(base, dom, deep, flare)]
    ol = C.orbit_locked(E.assign(tier=t0), per)
    return np.array([mk(r, d, td, fl, True) if o else t for r, d, td, fl, o, t in zip(base, dom, deep, flare, ol, t0)])


def counts(E, tier):
    t1 = np.isin(tier, T1)
    return dict(real=int(((E.kind == "real") & t1).sum()), flip=int(((E.kind == "flip") & t1).sum()))


def rows_of(path):
    r = pd.read_pickle(path); r = r[r.K.notna() & r.error.isna()]
    r = r[r.K.isin((6., 8., 10., 12., 14., 18.))].copy()
    r["tier1"] = r.tier1.astype(bool)
    return r


def k_at(g, level, KS=(6.0, 8.0, 10.0, 12.0, 14.0, 18.0)):
    r = g.groupby("K").tier1.mean().reindex(KS)
    if r.isna().all():
        return np.nan
    if r.iloc[0] >= level:
        return KS[0]
    for (k0, r0), (k1, r1) in zip(r.items(), list(r.items())[1:]):
        if r0 < level <= r1:
            return k0 + (k1 - k0) * (level - r0) / (r1 - r0)
    return np.inf


def main():
    P("VESPER 0.9 STUDY RESULTS (development slice only; rules fixed in V9-STUDY-PLAN.md; reading of the guard rule written in this script's header before any number was read)")
    Eb, meta_b = load(BASE_RUN, ["c6"]); En, meta_n = load(NEW_RUN, ["c6", "dg", "nd", "fl"])
    per = periods_of(pd.concat([Eb, En]))
    Eb["k"], En["k"] = key(Eb), key(En)
    P(f"events (primary): baseline run {len(Eb)}, new run {len(En)}; unique keys {Eb.k.is_unique and En.k.is_unique}")
    j = En.merge(Eb[["k", "dominated", "tier"]].rename(columns={"dominated": "dom_base", "tier": "tier_base"}), on="k", how="outer", indicator=True)
    P(f"same events in both runs: {int((j._merge == 'both').sum())}; only in baseline {int((j._merge == 'right_only').sum())}; only in new {int((j._merge == 'left_only').sum())}")
    X = j[j._merge == "both"].copy().reset_index(drop=True)
    tf = lambda s: pd.to_numeric(s, errors="coerce").fillna(0).ne(0)       # a missing flag is not set
    for c in ("too_deep", "flare", "dom_base", "dominated"):
        X[c] = tf(X[c])
    no = np.zeros(len(X), bool)
    # machinery check: reproduce both real runs exactly
    t_base = retier(X, X.dom_base.values, no, no, per); t_new = retier(X, X.dominated.values, X.too_deep.values, X.asym.gt(1.0).fillna(False).values, per)
    P(f"machinery check: tier recomputed for the baseline run agrees on {int((t_base == X.tier_base.values).sum())} of {len(X)}; for the all-on run on {int((t_new == X.tier.values).sum())} of {len(X)}")
    ok_machine = (t_base == X.tier_base.values).all() and (t_new == X.tier.values).all()
    P(f"   {'OK' if ok_machine else 'MISMATCH: the offline variants below are NOT trusted until this is explained'}")

    n_ss = len(meta_n[(meta_n.status == "ok") & (meta_n["product"] == meta_n["best"])].drop_duplicates(["tic", "sector"]))
    P(f"star-sectors in the development run: {n_ss}")
    cb = counts(X, X.tier_base.values); cn = counts(X, X.tier.values)
    P("")
    P(f"1. FULL DEVELOPMENT RUN, tier-1 events (primary).  0.8.0: real {cb['real']}, upside-down {cb['flip']} ({1000 * cb['flip'] / n_ss:.2f} per 1,000 star-sectors).  All switches on (fl 1.0): real {cn['real']}, upside-down {cn['flip']} ({1000 * cn['flip'] / n_ss:.2f} per 1,000)")

    # --- dg
    unph = X.depth_ppm.isna() | ~np.isfinite(X.depth_ppm.astype(float)) | (X.depth_ppm > C.DEPTH_MAX_PPM)
    t_dg = retier(X, X.dom_base.values, X.too_deep.values, no, per)
    ch = t_dg != X.tier_base.values
    P("")
    P(f"2. dg (depth guard): events over 30% or not finite: {int(unph.sum())} ({int((unph & (X.kind == 'real')).sum())} real, {int((unph & (X.kind == 'flip')).sum())} upside-down); flagged too_deep: {int(X.too_deep.sum())} (must equal the first number: {'yes' if int(X.too_deep.sum()) == int(unph.sum()) else 'NO'})")
    P(f"   events whose tier changes because of dg alone: {int(ch.sum())}; of them with depth 30% or less and finite: {int((ch & ~unph.values).sum())} (must be 0)")
    P(f"   tier-1 events removed by dg alone: real {int((np.isin(X.tier_base.values, T1) & ch & (X.kind == 'real')).sum())}, upside-down {int((np.isin(X.tier_base.values, T1) & ch & (X.kind == 'flip')).sum())}")
    dg_ok = int((ch & ~unph.values).sum()) == 0 and int(X.too_deep.sum()) == int(unph.sum())

    # --- nd
    dch = X.dominated.values != X.dom_base.values
    rel = dch & X.dom_base.values & ~X.dominated.values
    rev = dch & ~X.dom_base.values & X.dominated.values
    inlc = unph.groupby([X.tic, X.sector, X["product"]]).transform("any").values        # the light curve (star, sector, product) holds an unphysical event
    t_nd = retier(X, X.dominated.values, no, no, per)
    tch = t_nd != X.tier_base.values
    P("")
    P(f"3. nd (unphysical events leave the dominance comparison): events whose dominated flag changes {int(dch.sum())}: released {int(rel.sum())}, newly dominated {int(rev.sum())} (must be 0); in a light curve with an unphysical event: {int((dch & inlc).sum())} of {int(dch.sum())}")
    P(f"   tier changes from nd alone: {int(tch.sum())}; real {int((tch & (X.kind == 'real')).sum())}, upside-down {int((tch & (X.kind == 'flip')).sum())}; to tier 1: {int((np.isin(t_nd, T1) & tch).sum())}")
    nd_ok = int(rev.sum()) == 0 and int((dch & ~inlc).sum()) == 0

    # --- planted dips
    pb, pn = rows_of(BASE_ROWS), rows_of(NEW_ROWS)
    kk = lambda d: d.tic.astype(int).astype(str) + "|" + d.sector.astype(int).astype(str) + "|" + d.K.astype(str) + "|" + d.dur.astype(str) + "|" + d.sign.astype(int).astype(str) + "|" + d.tc.round(3).astype(str)
    pb["k"], pn["k"] = kk(pb), kk(pn)
    pj = pn.merge(pb[["k", "tier1"]].rename(columns={"tier1": "t1_base"}), on="k", how="outer", indicator=True)
    P("")
    P(f"4. PLANTED DIPS AND BUMPS (same 300 star-sectors, same seed): rows in both {int((pj._merge == 'both').sum())}; only baseline {int((pj._merge == 'right_only').sum())}; only new {int((pj._merge == 'left_only').sum())}")
    pj = pj[pj._merge == "both"].copy()
    for c in ("t1_base", "tier1", "found_primary", "step", "too_deep"):        # the outer merge left these as object columns (bitwise ~ on objects is wrong)
        pj[c] = tf(pj[c])
    pj["asym"] = pd.to_numeric(pj.asym, errors="coerce")
    agree = int(((pj.t1_base & ~pj.asym.gt(1.0)) == pj.tier1).sum())
    P(f"   machinery check: 0.8.0 tier-1 minus the flare flag at 1.0 equals the all-on tier-1 on {agree} of {len(pj)} planted rows ({'OK' if agree == len(pj) else 'MISMATCH: the planted variants below are NOT trusted until this is explained'})")
    pooled = pj[pj.K.isin((8., 10., 12., 14.))]
    d_, b_ = pooled[pooled.sign == 1], pooled[pooled.sign == -1]
    P(f"   deep planted events (too_deep) in the new run: {int(pj.too_deep.sum())}; planted tier-1 points lost that the flare flag at 1.0 does not explain (dg, nd or anything else): {int((pj.t1_base & ~pj.tier1 & ~(pj.asym > 1.0)).sum())} (must be 0)")
    gap_b = 100 * (d_.t1_base.mean() - b_.t1_base.mean())
    P(f"   K 8 to 14 pooled, tier-1 recovery: 0.8.0 dips {100 * d_.t1_base.mean():.1f}% bumps {100 * b_.t1_base.mean():.1f}% gap {gap_b:+.1f} points; all on (fl 1.0): dips {100 * d_.tier1.mean():.1f}% bumps {100 * b_.tier1.mean():.1f}% gap {100 * (d_.tier1.mean() - b_.tier1.mean()):+.1f}")

    # --- fl thresholds
    P("")
    P("5. fl (flare shape) by threshold, each ALONE against 0.8.0 on the development slice (the plan's four conditions)")
    P("   thr | upside-down tier-1 removed (of 0.8.0 total) = fall | real tier-1 removed | planted dips lost (points, K 8-14) | flips removed per planted point | K50 8 h (0.8.0 -> fl) | K50 14-20 h (0.8.0 -> fl) | mirror gap | 1 fall>=20% | 2 price>=6.8 | 3 K50 within 10% | 4 mirror")
    verdicts = []
    for thr in THR:
        t_fl = retier(X, X.dom_base.values, no, X.asym.gt(thr).fillna(False).values, per)
        was = np.isin(X.tier_base.values, T1); now = np.isin(t_fl, T1)
        rm = was & ~now
        rm_flip, rm_real = int((rm & (X.kind == "flip")).sum()), int((rm & (X.kind == "real")).sum())
        fall = 100 * rm_flip / max(cb["flip"], 1)
        flare_p = pj.asym.gt(thr).fillna(False)
        pj["t1_fl"] = pj.t1_base & ~flare_p
        dd = pj[pj.K.isin((8., 10., 12., 14.)) & (pj.sign == 1)]; bb = pj[pj.K.isin((8., 10., 12., 14.)) & (pj.sign == -1)]
        lost_pts = 100 * (dd.t1_base.mean() - dd.t1_fl.mean())
        price = rm_flip / lost_pts if lost_pts > 0 else np.inf
        gap = 100 * (dd.t1_fl.mean() - bb.t1_fl.mean())
        def c3_of(durs):
            g = pj[(pj.sign == 1) & pj.dur.isin(durs)]
            kb, kf = k_at(g.assign(tier1=g.t1_base), .5), k_at(g.assign(tier1=g.t1_fl), .5)
            if np.isfinite(kb):
                return bool(np.isfinite(kf) and kf <= 1.1 * kb), f"K50 {kb:.1f} -> {kf:.1f}"
            r0, r1 = g.t1_base.mean(), g.t1_fl.mean()               # K50 is not reached by K 18 on the baseline: fall back to the relative loss of tier-1 recovery over all K (at most 10%)
            return bool(r1 >= 0.9 * r0), f"K50 not reached; recovery {100 * r0:.1f}% -> {100 * r1:.1f}% (fallback rule: at most 10% lost)"
        ok8, t8 = c3_of((8.,)); okl, tl = c3_of((14., 20.))
        c1, c2, c3, c4 = fall >= 20, price >= PRICE_STEP, ok8 and okl, abs(gap) <= 3
        verdicts.append((thr, fall, c1, c2, c3, c4))
        fmt = lambda x: "inf" if x == np.inf else f"{x:.1f}"
        P(f"   {thr:.1f} | {rm_flip} of {cb['flip']} = {fall:.0f}% | {rm_real} of {cb['real']} | {lost_pts:.2f} | {fmt(price)} (per 1,000 star-sectors: {1000 * rm_flip / n_ss:.1f} flips) | 8 h: {t8} | 14-20 h: {tl} | {gap:+.1f} | {'yes' if c1 else 'NO'} | {'yes' if c2 else 'NO'} | {'yes' if c3 else 'NO'} | {'yes' if c4 else 'NO'}")
    good = [v for v in verdicts if v[2] and v[3] and v[4] and v[5]]
    pick = max(good, key=lambda v: v[1])[0] if good else None

    # --- T34 step parts and T35 box split (report only)
    P("")
    P("6. T34 STEP CHECK, its two parts priced on the development run (report only; no switch). A part is 'dropped alone' for events where the step flag is set and that part is the only reason; planted points regained / upside-down events let in")
    E = X.copy()
    def parts(r):
        cov = min(r.cover_pre, r.cover_post) < C.STEP_COVER
        lift = any(l is None or l != l or abs(l) > C.STEP_LIFT for l in (r.lift_pre, r.lift_post))
        return cov, lift
    pc = [parts(r) for r in E.itertuples()]
    E["cov_rule"], E["lift_rule"] = [p[0] for p in pc], [p[1] for p in pc]
    for name, only in (("coverage rule (too little data beside the event)", lambda r: r.cov_rule and not r.lift_rule), ("lift rule (flux beside the event is lifted)", lambda r: r.lift_rule and not r.cov_rule)):
        add = {"real": 0, "flip": 0}
        for r in E[(E.tier_base == "2") & E.step.fillna(False).astype(bool)].itertuples():
            if only(r):
                e = {**r._asdict(), "step": False, "dominated": r.dom_base, "too_deep": False, "flare": False, "orbit_lock": False}
                if C.tier_of(e) in T1:
                    add[r.kind] += 1
        pl = pj[pj.K.isin((8., 10., 12., 14.)) & (pj.sign == 1) & pj.found_primary.astype(bool) & (pj.tier == "2") & pj.step.astype(bool)]
        cov = pl.apply(lambda r: min(r.cover_pre, r.cover_post) < C.STEP_COVER, axis=1); lif = pl.apply(lambda r: any(l is None or l != l or abs(l) > C.STEP_LIFT for l in (r.lift_pre, r.lift_post)), axis=1)
        sel = (cov & ~lif) if name.startswith("coverage") else (lif & ~cov)
        flags = [c for c in ("gap_dump", "flipmatch", "c5", "ecl_overlap", "repeater", "ramp", "dominated", "common") if c in pl]
        only_step = ~pl[flags].apply(lambda c: pd.to_numeric(c, errors="coerce").fillna(0).ne(0)).any(axis=1)
        reg = 100 * int((sel & only_step).sum()) / max(len(pj[pj.K.isin((8., 10., 12., 14.)) & (pj.sign == 1)]), 1)
        P(f"   {name}: planted points regained {reg:.2f}; upside-down let in {add['flip']}, real let in {add['real']}; flips per point {add['flip'] / reg:.1f}" if reg > 0 else f"   {name}: planted points regained 0.00; upside-down let in {add['flip']}, real let in {add['real']}")
    P("")
    P("7. T35 BOX LENGTH: tier-1 events of the development run by box length (0.8.0 tiers; report only; the planted rows do not record which box found them, so no planted split)")
    t = pd.crosstab(X.dur_h[np.isin(X.tier_base.values, T1)], X.kind[np.isin(X.tier_base.values, T1)])
    for dur, r in t.iterrows():
        P(f"   box {dur:g} h: real {int(r.get('real', 0))}, upside-down {int(r.get('flip', 0))}")

    P("")
    P("DECISION BY THE PLAN'S OWN RULES (mechanical; the numbers above are the evidence)")
    P(f"   dg: {'ACCEPT' if dg_ok and abs(100 * (d_.tier1.mean() - b_.tier1.mean())) <= 3 else 'REJECT or investigate'} (no event of 30% or less changed tier: {dg_ok}; mirror gap within 3)")
    P(f"   nd: {'ACCEPT' if nd_ok and abs(100 * (d_.tier1.mean() - b_.tier1.mean())) <= 3 else 'REJECT or investigate'} (every changed event in a light curve with an unphysical event, released only: {nd_ok})")
    P(f"   fl: {'ACCEPT at threshold ' + str(pick) if pick is not None else 'REJECT (no threshold meets all four conditions): record as a negative result'}")
    (ROOT / "research" / "stage3" / "v9-study-results.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
