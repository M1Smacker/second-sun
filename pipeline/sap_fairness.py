"""Is the upside-down copy a fair control for the SAP half, and what does the answer look like when it is made fair? (FIX-QUEUE 17, 18 and 19; learnings section 17.) POST-HOC on a frozen run,
aggregates only (no TIC, no time); nothing here changes an event or a tier.
A. CONTROL VALIDITY. If the upside-down curve were a fair null, every flag would hit real and upside-down events in equal shares (a flag that sees a mirror image the same way as the original).
   Share of each flag, real against upside-down, with Fisher's exact p, per half (PDCSAP half = dips PDCSAP found, SAP only = dips only the SAP twin found).
B. LADDER. Real | upside-down survivors as the flags are added one by one, so the step where the two sides part is visible.
C. EQUAL FLAG PASS RATES. The upside-down events are re-weighted (iterative proportional fitting) until each flag hits them in the same share as it hits the real events; the weighted number of upside-down
   events that then pass every check is what noise alone would leave among the real events, GIVEN the real events' flag shares. Observed real tier 1 against that, Poisson. Margins only, not the joint pattern: approximate.
D. PDCSAP CHECK (v7 runs). For SAP-only dips: the share that the PDCSAP flux of the same file also shows (SNR >= 3), real against upside-down. Systematics that PDC corrects do not survive it; the same operation
   is applied to the mirror image, so it needs no symmetry assumption.
E. VARIANTS of tier 1 (real | upside-down), so the effect of each rule is separate: v6 as frozen, no burst-type flag, the same-kind count (the FIX-QUEUE 17 wording), v7 pooled count, v7 with the PDCSAP check.
Usage: python sap_fairness.py [hash12]   (writes research\\stage3\\sap_fairness_<hash12>.txt)"""
import sys, pathlib
import numpy as np, pandas as pd
from scipy.stats import fisher_exact, poisson
import stage3_report as R, stage3_core as C

ROOT = r"D:\second-sun\data\stage3"
BASE_FLAGS = ["gap_dump", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated"]      # the flags that act on both kinds alike in rule; burst-type flags and flipmatch are handled apart


def same_kind_n(E):
    """The FIX-QUEUE 17 wording, kept as a sensitivity row: other stars with an event of the SAME kind within COMMON_D, same sector and camera."""
    out = np.zeros(len(E), int); pos = {ix: n for n, ix in enumerate(E.index)}
    for _, g in E.groupby(["kind", "sector", "camera"]):
        c, t = g.center.values, g.tic.values
        for ix, ci, ti in zip(g.index, c, t):
            out[pos[ix]] = len(set(t[np.abs(c - ci) < C.COMMON_D]) - {ti})
    return out


def passes(E, burst, pdc):
    """Boolean Series: an event is tier 1 under the given rule set. burst = the column that plays the burst role (bool Series) or None; pdc = apply the v7 PDCSAP check."""
    ok = ~E[["flipmatch"] + BASE_FLAGS].any(axis=1)
    if burst is not None:
        ok &= ~burst
    ok &= ~((E.c8_n.fillna(0) > 0) & (E.c8_best < C.C8_LENIENT))               # second product disagrees: tier 3
    if pdc:
        ok &= ~(E.pdc_snr < C.PDC_MIN)                                           # NaN compares False: not measurable means no judgement
    return ok


def rake(flags, target, total, iters=500):
    """Weights on rows (bool matrix n x k) so that each column's weighted share equals target and the weights sum to total. Columns whose target is 0 or 1, or that are empty, are skipped."""
    w = np.full(len(flags), total / len(flags)); use = [j for j in range(flags.shape[1]) if 0 < target[j] < 1 and 0 < flags[:, j].sum() < len(flags)]
    for _ in range(iters):
        for j in use:
            f = flags[:, j]; wf, wn = w[f].sum(), w[~f].sum()
            w[f] *= target[j] * total / wf; w[~f] *= (1 - target[j]) * total / wn
    gap = max((abs(w[flags[:, j]].sum() / total - target[j]) for j in use), default=0.0)
    return w, gap


def fisher(a, na, b, nb):
    return fisher_exact([[a, na - a], [b, nb - b]])[1]


def report(h):
    ev, _ = R.load(rf"{ROOT}\{h}\groups")
    E = ev[ev.primary].copy()
    v7 = "common" in E
    E["common_same"] = same_kind_n(E) >= C.COMMON_N
    burst_col = "common" if v7 else "burst"
    E["half"] = np.where(E.seen_by == "SAP only", "SAP only", "PDCSAP half")
    out = [f"SAP FAIRNESS on run {h} ({'v7: common-moment flag and PDCSAP check applied' if v7 else 'v6: Stage 2 burst flag'}). Aggregates only; post-hoc; changes no tier.",
           "Real = the dip on the real curve, upside-down = its mirror image on the flipped curve (the control). SNR 7 or more, one row per dip (primary).", ""]
    flags = ["burst"] + (["common"] if v7 else []) + ["flipmatch"] + BASE_FLAGS
    out.append("A. DOES THE CONTROL TREAT THE FLAGS ALIKE? Share of events carrying each flag (real | upside-down), Fisher exact p for equal shares; p < 0.01 marks an unfair flag. flipmatch can only fire on real events.")
    for half, G in E.groupby("half"):
        r, f = G[G.kind == "real"], G[G.kind == "flip"]
        out.append(f"  {half}: {len(r)} real, {len(f)} upside-down")
        for fl in flags:
            a, b = int(r[fl].sum()), int(f[fl].sum())
            p = fisher(a, len(r), b, len(f))
            out.append(f"    {fl:12s} {100 * a / len(r):5.1f}% | {100 * b / len(f):5.1f}%   p = {p:.1e}" + ("   UNFAIR" if p < 0.01 and fl != "flipmatch" else ""))
        if "pdc_snr" in G:
            m = G.pdc_snr.notna()
            if half == "SAP only":
                a, b = int((r.pdc_snr < C.PDC_MIN).sum()), int((f.pdc_snr < C.PDC_MIN).sum())
                out.append(f"    {'fails PDC bar':12s} {100 * a / len(r):5.1f}% | {100 * b / len(f):5.1f}%   p = {fisher(a, len(r), b, len(f)):.1e}   (PDCSAP of the same file shows under SNR {C.PDC_MIN:g})")
    out += ["", "B. LADDER: survivors (real | upside-down, real / upside-down) as flags are added in order; ratios far from the raw one show where the sides part."]
    steps = ["gap_dump", burst_col, "flipmatch", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated"]
    for half, G in E.groupby("half"):
        r, f = G[G.kind == "real"], G[G.kind == "flip"]; keep_r, keep_f = np.ones(len(r), bool), np.ones(len(f), bool)
        line = [f"all {len(r)} | {len(f)}"]
        for s in steps:
            keep_r &= ~r[s].values; keep_f &= ~f[s].values
            line.append(f"+{s} {keep_r.sum()} | {keep_f.sum()}")
        pr, pf = passes(r, None, False).values & keep_r, passes(f, None, False).values & keep_f
        line.append(f"+second product {pr.sum()} | {pf.sum()}")
        if v7 and half == "SAP only":
            qr, qf = pr & ~(r.pdc_snr < C.PDC_MIN).values, pf & ~(f.pdc_snr < C.PDC_MIN).values
            line.append(f"+PDCSAP check {qr.sum()} | {qf.sum()}")
        out.append(f"  {half}: " + "; ".join(line))
    out += ["", "C. EQUAL FLAG PASS RATES (upside-down re-weighted to the real events' flag shares; sum of weights = number of real events). Expected = what noise would leave among the real events."]
    rk = [burst_col] + BASE_FLAGS
    for half, G in E.groupby("half"):
        r, f = G[G.kind == "real"], G[G.kind == "flip"]
        tgt = np.array([r[x].mean() for x in rk]); w, gap = rake(f[rk].values.astype(bool), tgt, len(r))
        for lab, pdc in (("tier 1", False),) + ((("tier 1 with the PDCSAP check", True),) if (v7 and half == "SAP only") else ()):
            ok_r, ok_f = passes(r, r[burst_col], pdc), passes(f, f[burst_col], pdc)
            obs, exp = int(ok_r.sum()), float(w[ok_f.values].sum())
            out.append(f"  {half}, {lab}: real {obs}, upside-down {int(ok_f.sum())} unweighted, {exp:.1f} when it is made to share the real flag shares; chance of {obs} or more from noise at {exp:.1f}: {poisson.sf(obs - 1, exp) if exp > 0 else float('nan'):.3f}   (fit gap {gap:.3f})")
    out.append("  Margins only: the joint pattern of the flags is the control's own, and real planets, if any, are part of the target shares. Approximate, not a proof of either direction.")
    if v7:
        out += ["", "D. PDCSAP CHECK: share of SAP-only dips that the PDCSAP flux of the same file also shows (SNR >= %g at the dip's own box length)." % C.PDC_MIN]
        G = E[E.half == "SAP only"]
        r, f = G[G.kind == "real"], G[G.kind == "flip"]
        for lab, rr, ff in (("all SAP-only dips", r, f), ("those that pass every flag", r[passes(r, r["common"], False) & ~(r.c8_n.fillna(0) > 0)], f[passes(f, f["common"], False) & ~(f.c8_n.fillna(0) > 0)]),
                            ("tier 1 before the PDCSAP check", r[passes(r, r["common"], False)], f[passes(f, f["common"], False)])):
            a, b = int((rr.pdc_snr >= C.PDC_MIN).sum()), int((ff.pdc_snr >= C.PDC_MIN).sum())
            out.append(f"  {lab:34s}: pass {a} of {len(rr)} real | {b} of {len(ff)} upside-down" + (f"   (shares {100 * a / len(rr):.1f}% | {100 * b / len(ff):.1f}%, p = {fisher(a, len(rr), b, len(ff)):.2f})" if len(rr) and len(ff) else ""))
        out.append(f"  median PDCSAP SNR at the dip: real {r.pdc_snr.median():.2f}, upside-down {f.pdc_snr.median():.2f}   (a dip PDC left alone would show about its SAP SNR, 7 or more, in the same pixels)")
    out += ["", "E. TIER 1 BY RULE SET (real | upside-down), per half and whole union"]
    sets = [("v6 as frozen (Stage 2 burst flag, plus the SAP burst test on SAP-only dips)", E["burst"], False), ("no burst-type flag at all", None, False),
            ("same-kind common moment instead of burst (FIX-QUEUE 17 wording; sensitivity)", E["common_same"], False)]
    if v7:
        sets += [("v7 pooled common moment instead of burst", E["common"], False), ("v7 pooled common moment and the PDCSAP check (= the v7 tiers)", E["common"], True)]
    for lab, b, pdc in sets:
        cells = []
        for half, G in list(E.groupby("half")) + [("whole union", E)]:
            ok = passes(G, b.loc[G.index] if b is not None else None, pdc)
            cells.append(f"{half}: {int(ok[G.kind == 'real'].sum())} | {int(ok[G.kind == 'flip'].sum())}")
        out.append(f"  {lab:80s} " + "   ".join(cells))
    if v7:
        t = E.groupby("kind").tier.apply(lambda s: int(s.isin(['1A', '1L', '1B']).sum()))
        out.append(f"  (check: tier column of this run, whole union: {t.get('real', 0)} | {t.get('flip', 0)})")
        ok = passes(E, E["common"], True)
        assert int(ok[E.kind == "real"].sum()) == t.get("real", 0) and int(ok[E.kind == "flip"].sum()) == t.get("flip", 0), "the rule-set rebuild must equal the tier column"
    else:
        t = E.groupby("kind").tier.apply(lambda s: int(s.isin(['1A', '1L', '1B']).sum()))
        ok = passes(E, E["burst"], False)
        assert int(ok[E.kind == "real"].sum()) == t.get("real", 0) and int(ok[E.kind == "flip"].sum()) == t.get("flip", 0), "the rule-set rebuild must equal the tier column"
    txt = "\n".join(out)
    leaked = [str(x) for x in ev.tic.unique() if str(x) in txt]
    assert not leaked, f"star IDs leaked: {leaked[:3]}"
    return txt


if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else "f366d3682843"
    txt = report(h); print(txt)
    (pathlib.Path(r"D:\second-sun\research\stage3") / f"sap_fairness_{h}.txt").write_text(txt, encoding="utf-8")
