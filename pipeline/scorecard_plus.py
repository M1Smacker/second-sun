"""Scorecard plus (Amendment 2, 2 Nov 2026; research/stage3/SCORECARD-AMENDMENTS.md). Extra lines for a Vesper run, written AFTER the first sealed run (30 Oct 2026), so they are POST HOC for
that run and fixed BEFORE the run for every later one. Nothing here changes S1 to S8, their pass marks or benchmark_g2.py. Aggregates only: no star ID and no event time is printed, except TOI-1338 (a known planet).
  A  star-level counts; the control's ratio per bar with a star bootstrap, the upper limit AND the detectable excess; the heaviest stars trimmed      (T38, T39)
  B  price of every safety check: drop one alone, count planted dips regained against upside-down events let in                                       (T103)
  C  efficiency of one planet-bearing star, and the limit on (planets per star x geometry factor)                                                     (T105)
  D  wording rules: a borderline S2 is called borderline; S4 shows "found at all" beside "kept"; a difference is "better" or "worse"                  (T40, T41, T42)
  E  TOI-1338 b against the later published times, and the flags that cost each transit                                                                (T44, T102)
Usage: SS_SET=g2 VESPER_OPTS=c6 python scorecard_plus.py RUN_FOLDER LABEL NSTARS     (the options must be the ones the run used; writes research/stage3/scorecard-plus-<LABEL>.txt)"""
import os, sys, json, pathlib
os.environ.setdefault("SS_SET", "g2"); os.environ.setdefault("VESPER_OPTS", "c6")
import numpy as np, pandas as pd
from scipy import stats
import stage3_core as C, stage3_report as R

T1 = ["1A", "1L", "1B"]
BARS = (7, 8, 10, 12)
FLAGS = ["gap_dump", "flipmatch", "c5", "ecl_overlap", "repeater", "orbit_lock", "step", "ramp", "dominated"]
ROWS = C.ROOT / "data" / "chain_recovery_g2"


def load_events(run):
    ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
    E = R.pdc_half(ev[ev.primary]).copy()
    for c in ("snr", "dur_h", "depth_ppm", "cover_pre", "cover_post", "lift_pre", "lift_post"):
        E[c] = pd.to_numeric(E[c], errors="coerce")
    return E, meta


def planted(name):
    r = pd.read_pickle(ROWS / f"rows_{name}.pkl")
    return r[r.K.notna() & r.error.isna()].copy()


# ---------------------------------------------------------------- A: the unit is the star (T38, T39)
def star_table(E, nstars, B=20000, seed=7):
    stars = np.array(sorted(set(E.tic))); pad = nstars - len(stars)

    def vec(mask):
        c = E[mask].groupby("tic").size()
        return np.array([c.get(s, 0) for s in stars] + [0] * pad, dtype=np.int32)

    idx = np.random.default_rng(seed).integers(0, nstars, (B, nstars), dtype=np.int32)
    rows = []
    for b in BARS:
        ok = E.snr >= b
        rawR, rawF = vec(ok & (E.kind == "real")), vec(ok & (E.kind == "flip"))
        t1r, t1f = vec(ok & (E.kind == "real") & E.tier.isin(T1)), vec(ok & (E.kind == "flip") & E.tier.isin(T1))
        if rawR.sum() == 0 or rawF.sum() == 0:
            continue
        ratio = rawF.sum() / rawR.sum(); R1, F1 = int(t1r.sum()), int(t1f.sum()); exp = F1 / ratio
        rr, rf = rawR[idx].sum(1), rawF[idx].sum(1); good = rr > 0
        rb = np.where(good, rf / np.maximum(rr, 1), np.nan)
        exc = (t1r[idx].sum(1) - t1f[idx].sum(1) / rb)[good]
        sd = exc.std(); var = R1 + F1 / ratio ** 2
        trims = {}
        if b == 7:
            tot = rawR + rawF; order = np.argsort(-tot)
            for k in (1, 5, 10, 25):
                keep = np.ones(nstars, bool); keep[order[:k]] = False
                trims[k] = (rawF[keep].sum() / max(rawR[keep].sum(), 1), 100 * tot[order[:k]].sum() / tot.sum())
        rows.append(dict(bar=b, real=R1, real_stars=int((t1r > 0).sum()), flip=F1, flip_stars=int((t1f > 0).sum()), ratio=ratio,
                         ratio_lo=np.nanpercentile(rb, 2.5), ratio_hi=np.nanpercentile(rb, 97.5), expected=exp, diff=R1 - exp,
                         diff_lo=np.percentile(exc, 2.5), diff_hi=np.percentile(exc, 97.5), up95=np.percentile(exc, 95), sd=sd,
                         deff=sd ** 2 / var if var > 0 else np.nan, p_event=stats.poisson.sf(R1 - 1, exp) if exp > 0 else np.nan,
                         p_star=(exc <= 0).mean(), detectable=2.49 * sd, raw_real_stars=int((rawR > 0).sum()), raw_flip_stars=int((rawF > 0).sum()), trims=trims))
    return rows


def print_star_table(rows, label, P):
    P(f"A. STAR LEVEL (post hoc for the first sealed run): the unit is the star, not the event; events cluster on stars (deff = variance inflation from clustering)  [{label}]")
    P("   bar | tier-1 real (stars) | tier-1 upside-down (stars) | ratio, full run [95% star bootstrap] | expected real | real - expected [95%] | upper limit (95%, one-sided) | deff | detectable excess (80% power)")
    for r in rows:
        P(f"   {r['bar']:3d} | {r['real']} ({r['real_stars']}) | {r['flip']} ({r['flip_stars']}) | {r['ratio']:.2f} [{r['ratio_lo']:.2f} to {r['ratio_hi']:.2f}] | {r['expected']:.1f} | {r['diff']:+.1f} [{r['diff_lo']:+.1f} to {r['diff_hi']:+.1f}] | {r['up95']:+.1f} | {r['deff']:.1f} | {r['detectable']:.1f}")
    r7 = next((r for r in rows if r["bar"] == 7), None)
    if r7:
        P(f"   bar 7 raw events: real on {r7['raw_real_stars']} stars, upside-down on {r7['raw_flip_stars']} stars (star-level ratio {r7['raw_flip_stars'] / max(1, r7['raw_real_stars']):.2f}, event-level {r7['ratio']:.2f})")
        P("   ratio after dropping the heaviest stars: " + "; ".join(f"{k}: {v[0]:.2f} (they hold {v[1]:.0f}% of raw events)" for k, v in r7["trims"].items()))
    P("   read: the limit says what the data allow; the detectable excess says what this run could have shown. A result is never stated from the event count alone.")


# ---------------------------------------------------------------- B: what each check costs and buys (T103)
def _b(x):
    return pd.to_numeric(x, errors="coerce").fillna(0).ne(0)       # a missing flag is not set; any non-zero count is set


def price_table(E, Pl):
    E = E[E.snr >= 7].copy()
    for f in FLAGS + ["common", "burst"]:
        if f in E and f != "common":
            E[f] = _b(E[f])
    Pl = Pl[(Pl.K >= 8) & (Pl.K <= 14) & (Pl.sign == 1)].copy()
    for c in FLAGS + ["common"]:
        if c in Pl:
            Pl[c] = _b(Pl[c])

    def without(row, drop):
        e = row.to_dict()
        for f in drop:
            if f == "common":
                e["common"] = 0; e["burst"] = False
            else:
                e[f] = False
        return C.tier_of(e)

    out = []
    for f in FLAGS + ["common"]:
        if f not in E or f not in Pl:
            continue
        gains = []
        for sl in ("sealed", "dev"):
            d = Pl[Pl.sl == sl]; lost = d[d.found_any & ~d.tier1.astype(bool) & (d.tier == "2")]
            cols = [x for x in FLAGS if x in lost and x != "orbit_lock"] + ["common"]
            only = lost[cols]; others = [x for x in cols if x != f]
            gains.append(100 * (only[f] & ~only[others].any(axis=1)).sum() / len(d))
        cand = E[(E.tier == "2") & E[f].astype(bool)] if f != "common" else E[(E.tier == "2") & (E.common.fillna(0) > 0)]
        add = {"real": 0, "flip": 0}
        for _, row in cand.iterrows():
            if without(row, [f]) in T1:
                add[row.kind] += 1
        g = float(np.mean(gains))
        sh = (100 * E[E.kind == "real"][f].astype(bool).mean(), 100 * E[E.kind == "flip"][f].astype(bool).mean()) if f != "common" else None
        out.append(dict(check=f, gain_sealed=gains[0], gain_dev=gains[1], add_real=add["real"], add_flip=add["flip"], flips_per_point=(add["flip"] / g if g > 0 else np.inf), share=sh))
    return out


def print_price_table(rows, P):
    P("B. PRICE OF EVERY SAFETY CHECK (post hoc for the first sealed run): drop one check alone; planted dips regained (tier-1 points, sealed / development) against events let into tier 1 on the sealed run")
    P("   check | planted points regained (sealed / dev) | real events added | upside-down events added | upside-down added per planted point | share of all raw events carrying it (real, upside-down)")
    for r in rows:
        fp = f"{r['flips_per_point']:.1f}" if np.isfinite(r["flips_per_point"]) else "no gain"
        sh = f"{r['share'][0]:.0f}%, {r['share'][1]:.0f}%" if r["share"] else "-"
        P(f"   {r['check']:11s} | {r['gain_sealed']:+.1f} / {r['gain_dev']:+.1f} | +{r['add_real']} | +{r['add_flip']} | {fp} | {sh}")
    P("   read: a check is cheap to keep when it lets few upside-down events in per planted point it would give back. The step check is the biggest single cost and the largest source of kept false alarms if dropped.")


# ---------------------------------------------------------------- C: efficiency of one planet-bearing star (T105)
def efficiency(Pl, sectors_mean, nstars, window=26.0):
    Pl = Pl[(Pl.sign == 1) & (Pl.dur == 8)].copy(); Pl["sig"] = Pl.depth_ppm / Pl.K
    cK = Pl.assign(t=Pl.tier1.astype(bool)).groupby("K").t.mean(); Ks, Cs = np.array(cK.index, float), cK.values
    comp = lambda K: float(np.interp(K, Ks, Cs, left=Cs[0] * max(K, 0) / Ks[0]))
    sg = float(Pl.sig.median()); rows = []
    for dep, name in ((1000, "about 4 Earth radii, 1 solar radius"), (2300, "TOI-1338 b as seen (median depth of its events)"), (4000, "6.85 Earth radii, undiluted"), (10000, "Jupiter, 1 solar radius")):
        K = dep / sg; c = comp(K); det = [sectors_mean * window / p * c for p in (60, 95, 150, 300)]
        lim = lambda n, d: n / (nstars * d) if d > 0 else np.inf
        rows.append(dict(depth=dep, name=name, K=K, comp=c, det=det, lim95=(lim(8.3, det[1]), lim(1.0, det[1])), lim300=(lim(8.3, det[3]), lim(1.0, det[3]))))
    return dict(sigma=sg, rows=rows, comp_by_K={int(k): float(v) for k, v in zip(Ks, Cs)}, sectors_mean=sectors_mean)


def print_efficiency(e, nstars, P):
    P(f"C. EFFICIENCY (post hoc for the first sealed run): noise per 8 h box median {e['sigma']:.0f} ppm; tier-1 completeness (8 h box) by K: " + ", ".join(f"K{k} {100 * v:.0f}%" for k, v in e["comp_by_K"].items()))
    P(f"   one planet-bearing star with {e['sectors_mean']:.1f} sectors of data on average; expected tier-1 detections at P = 60 / 95 / 150 / 300 d, and the limit on (planets per binary x geometry factor g) at P = 95 and 300 d for the two excess limits (8.3 = preregistered-ratio upper end, 1.0 = full-run ratio)")
    for r in e["rows"]:
        P(f"   {r['depth']:6d} ppm ({r['name']}): K {r['K']:.1f}, completeness {100 * r['comp']:.0f}% | " + " / ".join(f"{d:.2f}" for d in r["det"])
          + f" | P95: {100 * r['lim95'][0]:.1f}% | {100 * r['lim95'][1]:.2f}%   P300: {100 * r['lim300'][0]:.1f}% | {100 * r['lim300'][1]:.2f}%")
    P(f"   caveat: depth = (Rp/R*)^2 with R* = 1 solar radius, no dilution, window = 26 d per sector; the real host radii are not used yet (task T107). Limits above 100% mean no constraint. Stars searched: {nstars}.")


# ---------------------------------------------------------------- D: wording rules (T40, T41, T42)
def s2_reading(k, n, mark=8.0):
    """The sentence for S2 given upside-down tier-1 count k in n star-sectors, against a mark in events per 1,000."""
    lo = 1000 * (stats.chi2.ppf(.025, 2 * k) / 2 if k else 0.0) / n; hi = 1000 * stats.chi2.ppf(.975, 2 * (k + 1)) / 2 / n; r = 1000 * k / n
    if hi <= mark:
        word = "below the mark"
    elif lo > mark:
        word = "above the mark"
    else:
        word = "BORDERLINE: the 95% interval includes the mark, so neither a pass nor a fail is claimed"
    return f"S2 reading: {r:.2f} per 1,000 (95% interval {lo:.2f} to {hi:.2f}) against a mark of {mark:g}: {word}"


def wilson(k, n):
    return tuple(100 * np.array(stats.binomtest(int(k), int(n)).proportion_ci(0.95, method="wilson"))) if n else (np.nan, np.nan)


def compare_word(lo, hi, lo2, hi2):
    """Sealed interval (lo, hi) against development (lo2, hi2): better, worse, or no clear difference. Intervals that overlap are not a difference."""
    return "better in this slice" if lo > hi2 else "worse in this slice" if hi < lo2 else "no clear difference"


def s4_table(rows, dev):
    d = rows[(rows.sign == 1) & rows.K.isin((8., 10., 12., 14.))]; h = dev[(dev.sign == 1) & dev.K.isin((8., 10., 12., 14.))]
    out = []
    for dur in sorted(d.dur.unique()):
        g, g2 = d[d.dur == dur], h[h.dur == dur]
        fk, fn = int(g.found_any.astype(bool).sum()), len(g); kk = int(g.tier1.astype(bool).sum())
        f2, k2, n2 = int(g2.found_any.astype(bool).sum()), int(g2.tier1.astype(bool).sum()), len(g2)
        out.append(dict(dur=dur, n=fn, found=wilson(fk, fn) + (100 * fk / fn,), kept=wilson(kk, fn) + (100 * kk / fn,), dev_found=wilson(f2, n2) + (100 * f2 / n2,), dev_kept=wilson(k2, n2) + (100 * k2 / n2,)))
    return out


def print_wording(E, meta, rows, dev, P):
    ss = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"]); n = len(ss)
    k = int(((E.kind == "flip") & E.tier.isin(T1)).sum())
    P("D. WORDING RULES (post hoc for the first sealed run)")
    P("   " + s2_reading(k, n))
    P("   pooled rate over all 895 stars: NOT COMPUTED until the development slice has been re-run with this version (census run, task T43)")
    P("   S4 with 'found at all' beside 'kept' (planted dips, K 8 to 14, sealed | development; 95% Wilson intervals); the gap between the two is what the safety checks cost")
    for r in s4_table(rows, dev):
        f, kp, df, dk = r["found"], r["kept"], r["dev_found"], r["dev_kept"]
        P(f"   {r['dur']:g} h box: found {f[2]:.1f}% ({f[0]:.1f} to {f[1]:.1f}), kept {kp[2]:.1f}% ({kp[0]:.1f} to {kp[1]:.1f}), n {r['n']} | development found {df[2]:.1f}%, kept {dk[2]:.1f}% | kept, sealed against development: {compare_word(kp[0], kp[1], dk[0], dk[1])}")


# ---------------------------------------------------------------- E: TOI-1338 b against the later published times (T44, T102)
TOI1338 = 260128333
# Kostov 2020 forecast (preregistered epochs); Wang and Liu 2024 (arXiv:2404.18415): Table 1 observed mid-transit times (BJD - 2457000 = BTJD), Table 3 photodynamical forecast (BJD - 2455000, so minus 2000), published 29 Apr 2024, before sectors 89 to 98 were observed.
KOS = {27: 2049.69, 30: 2142.40, 34: 2237.92, 37: 2331.00, 62: 2989.35, 65: 3084.82, 68: 3177.98, 89: 3743.62, 93: 3836.04, 96: 3931.42, 98: 4024.62}
OBS = {27: (2049.9515, .0034), 34: (2238.2258, .0034), 37: (2331.0148, .0024), 62: (2989.6356, .0047), 65: (3085.4243, .0044), 68: (3178.2853, .0077)}
PRED = {89: (5744.4534 - 2000, .0104), 93: (5836.9195 - 2000, .0132), 96: (5932.7322 - 2000, .0183), 98: (6025.5927 - 2000, .0159)}
RANK = {"1A": 0, "1L": 1, "1B": 2, "2": 3, "3": 4}


def tail(ps, k):
    dp = [1.0]
    for p in ps:
        dp = [(dp[i] * (1 - p) if i < len(dp) else 0) + (dp[i - 1] * p if i > 0 else 0) for i in range(len(dp) + 1)]
    return sum(dp[k:])


def toi1338(run_dir):
    upd = {**OBS, **PRED}; rows = []
    for sec in sorted(upd):
        ev = []
        for sub in ("groups", "groups_sap"):
            p = pathlib.Path(run_dir) / sub / f"{TOI1338}_{sec}.json"
            if p.exists():
                ev += json.load(open(p))["events"]
        t, s = upd[sec]; w = 3 * s + 0.1
        inw = [e for e in ev if abs(e["center"] - t) <= w]
        n = len({round(e["center"] * 4) for e in ev}); real = [e for e in inw if e["kind"] == "real"]
        best = min((RANK.get(e["tier"], 9) for e in real), default=None)
        rows.append(dict(sector=sec, src="observed" if sec in OBS else "forecast", shift=t - KOS[sec], hit=bool(inw), best=best, p=min(1.0, n * 2 * w / 27.4),
                         events=[dict(kind=e["kind"], product=e["product"], tier=e["tier"], off_h=24 * (e["center"] - t), dur=e["dur_h"], snr=e["snr"],
                                      flags=[f for f in FLAGS + ["common", "burst"] if e.get(f)]) for e in sorted(inw, key=lambda e: (RANK.get(e["tier"], 9), e["product"]))]))
    return rows


def print_toi1338(rows, P):
    hits = sum(r["hit"] for r in rows); oos = [r for r in rows if r["src"] == "forecast"]
    P("E. TOI-1338 b (known circumbinary planet) against the LATER published times (post hoc; the preregistered S6 line, Kostov 2020 epochs, 1 of 7 strong, is unchanged)")
    P("   sector | source | shift from the Kostov 2020 time (d) | events within 3 sigma + 0.1 d of the updated time: kind, product, tier, offset (h), length (h), SNR, flags that fired")
    for r in rows:
        d = "; ".join(f"{e['kind']} {e['product']} tier {e['tier']} {e['off_h']:+.1f} h {e['dur']} h snr {e['snr']:.1f} flags [{', '.join(e['flags']) or 'none'}]" for e in r["events"]) or "none"
        P(f"   {r['sector']} | {r['src']} | {r['shift']:+.3f} | {d}")
    P(f"   sectors with an updated time: {len(rows)}; with an event in the window: {hits} (chance {tail([r['p'] for r in rows], hits):.1e}); forecast sectors {sum(r['hit'] for r in oos)} of {len(oos)} (chance {tail([r['p'] for r in oos], sum(r['hit'] for r in oos)):.1e}); real event at tier 1: {sum(1 for r in rows if r['best'] is not None and r['best'] <= 2)}, tier 2 only: {sum(1 for r in rows if r['best'] == 3)}, none: {sum(1 for r in rows if r['best'] is None)}")


# ---------------------------------------------------------------- main
def main(run, label, nstars):
    out = []
    P = lambda s="": (out.append(s), print(s, flush=True))
    P(f"VESPER SCORECARD PLUS on {run} ({label}), options {sorted(C.V.ON)}. Post hoc for the first sealed run (written 2 Nov 2026, Amendment 2); S1 to S8 are in benchmark-g2-{label}.txt and are not changed.")
    E, meta = load_events(run)
    print_star_table(star_table(E, nstars), label, P)
    pl = pd.concat([planted("sealed").assign(sl="sealed"), planted("g2dev").assign(sl="dev")])
    print_price_table(price_table(E, pl), P)
    ss = meta[meta.status == "ok"].drop_duplicates(["tic", "sector"]).groupby("tic").size()
    print_efficiency(efficiency(pl, float(ss.mean()), nstars), nstars, P)
    sealed, dev = planted("sealed"), planted("g2dev")
    print_wording(E, meta, sealed, dev, P)
    print_toi1338(toi1338(C.DS.RUNS / run), P)
    (C.ROOT / "research" / "stage3" / f"scorecard-plus-{label}.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
