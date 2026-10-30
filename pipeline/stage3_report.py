"""Stage 3 report, PUBLISHABLE OUTPUT = AGGREGATES ONLY (no TIC, no event time). Works on any folder of group JSONs, including Stage 2's (events are enriched on
the fly), so it can be checked against Stage 2's published numbers. Differences from stage2_report.py: tiers (1A, 1L, 1B, 2, 3), the QLP-only share, the
share of the timeline C5 covers, class sizes derived from data, and the planning number is the REAL-curve tier-1 count (upside-down is only an upper bound).
Usage: python stage3_report.py <groups_dir> [label]   (writes research\\stage3\\aggregate_<label>.txt)"""
import sys, glob, json, pathlib
import numpy as np, pandas as pd
import stage3_core as C


SAP_BURST_D, SAP_BURST_N = 0.1, C.BURST_MIN     # v6: the same 0.1 d and 3 stars as the Stage 2 burst flag, counted on the SAP pass itself


def merge_sap(ev):
    """v6 union of the PDCSAP search (v5, unchanged) and the SAP-twin search. `ev` has the columns load() builds. A dip counts ONCE. If the best product's PDCSAP version has
    an event within the Stage 2 merge radius (0.5 x the longer box + 0.1 d) of a SAP-twin event of the same star-sector and kind, the dip keeps its v5 version (seen_by "both") and
    the SAP row stays non-primary; otherwise the SAP row becomes primary (seen_by "SAP only"). So v6 never changes a v5 event: it only adds dips PDCSAP missed.
    SAP-only dips also get the burst test on the SAP pass itself (the Stage 2 burst list is built from PDCSAP events and cannot know the scattered-light events only SAP has):
    flagged if upside-down SAP events of at least 3 other stars sit within 0.1 d at the same sector and camera. A newly flagged dip is re-tiered (tier 2). Only the SAP twin of the
    BEST product is eligible; twins of other products are searched only to confirm each other (rule C8) and stay non-primary."""
    ev = ev.copy()
    ev["seen_by"] = np.where(ev["primary"], "PDCSAP only", "")
    ev["sap_burst_n"] = 0
    twin = ev["product"] == ev["best"].astype(str) + "-SAP"
    if not twin.any():
        return ev
    pdc = {k: g for k, g in ev[ev["primary"]].groupby(["kind", "tic", "sector"])}
    sap_only = []
    for i, r in ev[twin].iterrows():
        g = pdc.get((r["kind"], r["tic"], r["sector"]))
        hit = None if g is None else next((j for j, c, d in zip(g.index, g.center, g.dur_h) if abs(c - r["center"]) <= 0.5 * max(d, r["dur_h"]) / 24 + 0.1), None)
        if hit is None:
            ev.at[i, "primary"] = True; ev.at[i, "seen_by"] = "SAP only"; sap_only.append(i)
        else:
            ev.at[hit, "seen_by"] = "both"
    flips = ev[ev["product"].str.endswith("-SAP") & (ev["kind"] == "flip")]
    where = {k: (g.center.values, g.tic.values) for k, g in flips.groupby(["sector", "camera"])}
    for i in sap_only:
        c, tics = where.get((ev.at[i, "sector"], ev.at[i, "camera"]), (np.array([]), np.array([])))
        n = len(set(tics[np.abs(c - ev.at[i, "center"]) < SAP_BURST_D]) - {ev.at[i, "tic"]})
        ev.at[i, "sap_burst_n"] = n
        if n >= SAP_BURST_N and not ev.at[i, "burst"]:
            ev.at[i, "burst"] = True; ev.at[i, "tier"] = C.tier_of(ev.loc[i].to_dict())
    return ev


def apply_v7(ev):
    """v7 flags on the union (FIX-QUEUE 17 and 19; learnings section 17). (1) `common`: 3 or more other stars have an event of EITHER kind within 0.1 d at the same sector and camera
    (stage3_core.common_moment_n); it REPLACES the Stage 2 burst flag in the tiers, because that flag counts only upside-down events and so treats data and control differently. (2) `pdc_snr`: for a
    SAP-only dip, the SNR the PDCSAP flux of the same file shows at that time and box length (written by `stage3.py pdccheck`); under PDC_MIN the dip is tier 3. v5 events (PDCSAP only or both) are
    never judged by pdc_snr. Only primary events are re-tiered; the old `burst` column stays for the record."""
    ev = ev.copy()
    P = ev["primary"].values
    ev["common_n"], ev["common"] = 0, False
    n = C.common_moment_n(ev[P])
    ev.loc[P, "common_n"], ev.loc[P, "common"] = n, n >= C.COMMON_N
    if "pdc_snr" not in ev:
        ev["pdc_snr"] = np.nan
    ev["pdc_snr"] = pd.to_numeric(ev["pdc_snr"], errors="coerce").where(ev["seen_by"] == "SAP only")
    for i in ev.index[P]:
        ev.at[i, "tier"] = C.tier_of(ev.loc[i].to_dict())
    if "c6" in C.V.ON:                      # v8 candidate: orbit-locked flag, judged on the tiers above (partners must be tier 1)
        ep = C.Ephem(pd.read_csv(C.TARGETS, comment="#"), C.eb_widths())
        E = ev[P]; ev["orbit_lock"] = False
        ev.loc[P, "orbit_lock"] = C.orbit_locked(E, {int(t): [p for _, p, _ in ep.by.get(int(t), [])] for t in set(E.tic)})
        for i in ev.index[P & ev["orbit_lock"].values]:
            ev.at[i, "tier"] = C.tier_of(ev.loc[i].to_dict())
    return ev


def load(groups_dir, extra=True):
    """Events and star-sector meta of a run folder. If the folder has a sibling `groups_sap` (v6 and later) the SAP-twin events are read too and merged by merge_sap; if the run folder
    also holds v7.json (v7 and later) the v7 flags are applied on top (apply_v7)."""
    ephem, qlp = C.Ephem(pd.read_csv(C.TARGETS, comment="#"), C.eb_widths()), C.qlp_only_tics()
    dirs = [pathlib.Path(groups_dir)]
    if dirs[0].with_name("groups_sap").exists():
        dirs.append(dirs[0].with_name("groups_sap"))
    ev, meta = [], []
    for d in dirs:
        for p in glob.glob(str(d / "*.json")):
            g = json.load(open(p))
            ev += g["events"] if all("tier" in e for e in g["events"]) else C.enrich_group(g, ephem, qlp, extra)
            meta += [dict(m, tic=g["tic"], sector=g["sector"]) for m in g["meta"]]
    best = pd.read_csv(C.BEST)[["tic", "sector", "product"]].rename(columns={"product": "best"})
    ev = pd.DataFrame(ev).merge(best, on=["tic", "sector"], how="left")
    ev["primary"] = ev["product"] == ev["best"]
    ev["c8_best"] = pd.to_numeric(ev.c8_best, errors="coerce")
    if len(dirs) > 1:
        ev = merge_sap(ev)
        if dirs[0].with_name("v7.json").exists():
            ev = apply_v7(ev)
    return ev, pd.DataFrame(meta).merge(best, on=["tic", "sector"], how="left")


XM = C.ROOT / "data" / "xmatch"


def star_labels():
    """Catalogue labels per star from the tables saved in data/xmatch (NASA TOI table, NASA circumbinary hosts, TESS eclipsing binary catalogue of Prsa et al. 2022).
    Returns None if the tables are not on this machine. toi = TFOPWG disposition; eb = how the TESS period compares with the Kepler period."""
    if not all((XM / f).exists() for f in ("toi.csv", "cbp.csv", "ebs.csv")):
        return None
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic").set_index("tic")
    toi = pd.read_csv(XM / "toi.csv").drop_duplicates("tid").set_index("tid").tfopwg_disp
    cbp = set(pd.to_numeric(pd.read_csv(XM / "cbp.csv").tic_id.astype(str).str.replace("TIC ", ""), errors="coerce").dropna().astype(int))
    eb = pd.read_csv(XM / "ebs.csv").drop_duplicates("TIC").set_index("TIC").Per
    out = pd.DataFrame(index=tg.index)
    out["toi"] = out.index.map(toi)
    out["cbp_host"] = out.index.isin(cbp)
    r = out.index.map(eb) / tg.p_bin_d
    out["eb"] = np.select([r.isna(), (r - 1).abs() < .02, (r - .5).abs() < .01, (r - 2).abs() < .02], ["no", "same", "half", "double"], "other")
    return out


def repeater_labels(X):
    """Label star-sectors with 3 or more events of one kind in one product (never a deletion) by how much the event depths scatter (std / mean):
    uniform-depth (<= 0.25), scattered (> 0.5), mixed. A period test was tried and dropped: with thousands of trial periods any 3 or more events fit
    some period by chance, so it cannot tell a regular pattern from noise (it would need a significance test against the upside-down control).
    Thresholds are a priori label choices, not used in any flag."""
    lab = {}
    for key, g in X.groupby(["kind", "tic", "sector", "product"]):
        if len(g) >= C.REPEAT_N:
            cv = float(g.depth_ppm.std() / g.depth_ppm.mean())
            lab[key] = "uniform-depth" if cv <= 0.25 else ("scattered" if cv > 0.5 else "mixed")
    return pd.Series(lab, dtype=object)


def asym_ratios(label="v5"):
    """({SNR bar: upside-down dips / real dips}, file name) from research/stage3/asymmetry_<label>.txt (written by asymmetry_test.py), or the v4 file
    asymmetry.txt if there is no v5 one; ({}, None) if neither exists."""
    import re
    for name in ((f"asymmetry_{label}.txt", "asymmetry.txt") if C.DS.NAME == "g1" else (f"asymmetry_{C.DS.NAME}_{label}.txt",)):   # G2: only its own ratio (prereg section 5), never the G1 file
        p = C.ROOT / "research" / "stage3" / name
        if p.exists():
            out = {float(m[0]): float(m[3]) for m in re.findall(r"^\s*([\d.]+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s*$", p.read_text(encoding="utf-8"), re.M)}
            if out:
                return out, name
    return {}, None


def pdc_half(X):
    """The dips PDCSAP found (v5 events, seen by PDCSAP alone or by both); runs without a SAP twin are returned whole. The v5 asymmetry ratio belongs to this half."""
    return X[X.seen_by != "SAP only"] if "seen_by" in X else X


def noise_expected(real, flip, ratio):
    """(real events expected from noise alone = upside-down / ratio, chance of seeing at least `real` if the real curves held noise only). Poisson."""
    from scipy.stats import poisson
    lam = flip / ratio
    return lam, float(poisson.sf(real - 1, lam)) if lam > 0 else (1.0 if real == 0 else 0.0)


def waterfall(X):
    """Same order and rules as stage2_report.waterfall: start, no gap/dump, no burst, not matched upside-down, not at an eclipse phase (C5),
    second product >= 3 (lenient), >= 4 (lenient), >= 4 (strict)."""
    b = X[~X.gap_dump]; c = b[~(b.common if "common" in b else b.burst)]; d0 = c[~c.flipmatch]; d = d0[~d0.c5]      # v7: "burst" means the common-moment flag
    has = d.second_product
    return (len(X), len(b), len(c), len(d0), len(d), len(d[(d.c8_best.fillna(99) >= 3) | ~has]), len(d[(d.c8_best.fillna(99) >= 4) | ~has]),
            len(d[has & (d.c8_best >= 4)]))


def report(groups_dir):
    ev, meta = load(groups_dir)
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic").set_index("tic")
    ok = meta[meta.status == "ok"]; pr = ok[ok["product"] == ok["best"]].drop_duplicates(["tic", "sector"])
    pr = pr.assign(tb=pd.cut(pr.tic.map(tg.tmag), C.TBINS, right=False, labels=C.TLABELS)); nss = pr.groupby("tb", observed=True).size()
    E = ev[ev.primary].assign(tb=lambda x: pd.cut(x.tic.map(tg.tmag), C.TBINS, right=False, labels=C.TLABELS))
    R, F = E[E.kind == "real"], E[E.kind == "flip"]
    out = []
    P = out.append
    P(f"STAGE 3 aggregate report (no star IDs, no event times). Groups: {len(glob.glob(str(pathlib.Path(groups_dir) / '*.json')))}; star-sectors with a best product searched: {len(pr)}")
    P("\n1. CUTS in order (real | upside-down): start, no gap/dump, no burst, not matched upside-down, not at an eclipse phase (C5), second product >=3 lenient, >=4 lenient, >=4 strict")
    for lab, X in (("real", R), ("upside-down", F)):
        P(f"  {lab:12s} " + " | ".join(str(v) for v in waterfall(X)))
    P("\n2. TIERS of the best-product events (1A second product agrees >=4; 1L 3 to 4; 1B no second product; 2 flagged; 3 second product disagrees)")
    for lab, X in (("real", R), ("upside-down", F)):
        t = X.tier.value_counts().reindex(["1A", "1L", "1B", "2", "3"]).fillna(0).astype(int)
        P(f"  {lab:12s} " + "  ".join(f"{k} {v}" for k, v in t.items()))
    t1 = R[R.tier.isin(["1A", "1L", "1B"])]
    P(f"  real tier-1 events on QLP-only stars: {int(t1.qlp_only_star.sum())} of {len(t1)} (no second product is possible there)")
    P("\n3. HOW MUCH TIMELINE C5 COVERS (windows of 0.35 d around the primary and phase 0.5): stars with at least 5% / 10% / 20% / 30% of the timeline")
    cov = C.c5_timeline_cover()
    P("  " + " | ".join(f">= {int(q * 100)}%: {int((cov >= q).sum())} of {len(cov)}" for q in (0.05, 0.1, 0.2, 0.3)))
    P("\n4. PROJECTION TO THE CAMPAIGN (class sizes derived from data; rates per brightness class from this sample; REAL-curve tier-1 is the planning number, upside-down is an upper bound)")
    camp, nsec, nan = C.class_sizes()
    P(f"  campaign star-sectors by class: {camp} (total {nsec}, without a magnitude class {nan})")
    for lab, X in (("real tier-1", R[R.tier.isin(['1A', '1L', '1B'])]), ("real tier-1 + tier 2 (all real)", R), ("upside-down tier-1 (upper bound)", F[F.tier.isin(['1A', '1L', '1B'])])):
        tot = sum((X.tb == b).sum() / nss[b] * camp[b] for b in camp if b in nss.index)
        P(f"  {lab:34s}: about {tot:6.0f} events across the campaign")
    P("\n5. SIGNAL EXCESS: real minus upside-down (positive = more real dips than the control; the control is an upper bound on false alarms)")
    for lab, tiers in (("tier 1 (1A+1L+1B)", ["1A", "1L", "1B"]), ("tier 1A (second product agrees)", ["1A"]), ("tier 2 (flagged)", ["2"])):
        r, f = int(R.tier.isin(tiers).sum()), int(F.tier.isin(tiers).sum())
        P(f"  {lab:34s}: real {r:4d}, upside-down {f:4d}, excess {r - f:+5d}")
    t1r, t1f = R[R.tier.isin(["1A", "1L", "1B"])], F[F.tier.isin(["1A", "1L", "1B"])]
    for thr in (7, 8, 10, 12):
        a, b = int((t1r.snr >= thr).sum()), int((t1f.snr >= thr).sum())
        P(f"  tier 1 with SNR >= {thr:2d}: real {a:3d}, upside-down {b:3d}, excess {a - b:+4d}")
    if "step" in E:
        P("  v3 flat-baseline flag (real | upside-down): " + f"{int(R.step.sum())} | {int(F.step.sum())} of {len(R)} | {len(F)} best-product events")
    ratios, src = asym_ratios()
    if ratios:                                                    # v5: the control overstates dip false alarms, so judge real against upside-down / ratio
        u1r, u1f = pdc_half(t1r), pdc_half(t1f)                   # v6 and later: the ratio was measured on PDCSAP flux, so it is applied to the PDCSAP half only (sap_fairness.py shows why not to the SAP half)
        P(f"\n5b. NOISE-EXPECTED REAL{' (PDCSAP half only: dips PDCSAP found; the SAP-only half has no valid ratio)' if 'seen_by' in R else ''}: upside-down tier-1 divided by the measured asymmetry ratio ({src}); chance = P(real >= observed | noise alone, Poisson)")
        P("  Assumes the flags act equally on both sides and the ratio measured on raw dips holds for tier 1 (NOT TESTED for the PDCSAP half; for the SAP half it is known to FAIL, see sap_fairness); a SNR bar above the table uses its last ratio.")
        for thr in (7, 8, 10, 12):
            a, b = int((u1r.snr >= thr).sum()), int((u1f.snr >= thr).sum())
            r = ratios[max(k for k in ratios if k <= thr)]
            lam, p = noise_expected(a, b, r)
            P(f"  tier 1 with SNR >= {thr:2d}: real {a:3d}, upside-down {b:3d}, ratio {r:.2f}, noise-expected real {lam:5.1f}, chance {p:.2f}")
    P("\n6. LABELS (aggregate only; labels never remove an event)")
    sl = star_labels()
    if sl is None:
        P("  catalogue tables not on this machine: star labels skipped")
    else:
        for lab, X in (("real tier-1", t1r), ("upside-down tier-1", t1f)):
            tt = sl.reindex(X.tic.values)
            P(f"  {lab:20s} {len(X):3d} events: on a TOI {int(tt.toi.notna().sum())}, on a known circumbinary host {int(tt.cbp_host.sum())}, "
              f"in the TESS eclipsing binary catalogue {int((tt.eb != 'no').sum())} (period same {int((tt.eb == 'same').sum())}, half {int((tt.eb == 'half').sum())}, other {int((tt.eb == 'other').sum())})")
    for lab, X in (("real", R), ("upside-down", F)):
        rl = repeater_labels(X)
        P(f"  repeater star-sectors, {lab}: {len(rl)} " + ", ".join(f"{k} {int(v)}" for k, v in rl.value_counts().items()))
    if "seen_by" in ev:
        P("\n7. SAP TWIN (v6; sections 1 to 6 above already count each dip ONCE, the union). The PDCSAP half is the frozen v5 run; the SAP search of the same files adds dips PDCSAP missed")
        tw = meta[meta["product"].astype(str) == meta["best"].astype(str) + "-SAP"]
        P(f"  star-sectors whose best product has a SAP twin searched: {len(tw[tw.status == 'ok'].drop_duplicates(['tic', 'sector']))} of {len(pr)} star-sectors with a best product ({len(pr[pr['product'].isin(['SPOC', 'TESS-SPOC'])])} have a SPOC or TESS-SPOC best product)")
        t1 = ["1A", "1L", "1B"]
        for lab, X in (("real", R), ("upside-down", F)):
            c = X.seen_by.value_counts()
            P(f"  {lab:12s} dips by who found them: PDCSAP only {int(c.get('PDCSAP only', 0))}, both {int(c.get('both', 0))}, SAP only {int(c.get('SAP only', 0))}; "
              f"tier 1 of those: " + ", ".join(f"{k} {int(X[(X.seen_by == k) & X.tier.isin(t1)].shape[0])}" for k in ('PDCSAP only', 'both', 'SAP only')))
        a, b = int(((R.seen_by == "SAP only") & R.tier.isin(t1)).sum()), int(((F.seen_by == "SAP only") & F.tier.isin(t1)).sum())
        P(f"  tier-1 dips ADDED by the SAP twin: real {a}, upside-down {b}, excess {a - b:+d}   (judge the SAP half by this line: real minus upside-down)")
        for lab, X in (("real", R), ("upside-down", F)):
            both, only = int((X.seen_by == "both").sum()), int((X.seen_by == "PDCSAP only").sum())
            P(f"  {lab:12s} PDCSAP dips that SAP also found: {both} of {both + only}; SAP-only dips flagged by the SAP burst test: {int(((X.seen_by == 'SAP only') & (X.sap_burst_n >= SAP_BURST_N)).sum())} of {int((X.seen_by == 'SAP only').sum())}")
        P("  NOT measured for the SAP half: its own real-to-upside-down asymmetry ratio (section 5b uses the PDCSAP ratio), and injected-dip recovery with every check (see sap_recovery).")
    if "common" in ev:
        P("\n8. v7 FLAGS (the common-moment flag replaces the Stage 2 burst flag in the tiers; SAP-only dips must also show in the PDCSAP flux of the same file)")
        for lab, X in (("real", R), ("upside-down", F)):
            so = X[X.seen_by == "SAP only"]
            P(f"  {lab:12s} flagged by the common moment {int(X.common.sum())} of {len(X)} (the old burst flag: {int(X.burst.sum())}); SAP-only dips: {len(so)}, PDCSAP shows them (SNR {C.PDC_MIN:g} or more) {int((so.pdc_snr >= C.PDC_MIN).sum())}, "
              f"does not {int((so.pdc_snr < C.PDC_MIN).sum())}, not measurable {int(so.pdc_snr.isna().sum())}")
        P("  Is the upside-down copy a fair control for the SAP half, and what is left when it is made fair: sap_fairness_<run hash>.txt (flag shares, ladder, equal-pass-rate null, PDCSAP check, rule-set variants).")
    txt = "\n".join(out)
    leaked = [str(t) for t in ev.tic.unique() if str(t) in txt]
    assert not leaked, f"star IDs leaked into the published text: {leaked[:3]}"
    return txt


if __name__ == "__main__":
    txt = report(sys.argv[1]); print(txt)
    if len(sys.argv) > 2:
        d = C.ROOT / "research" / "stage3"; d.mkdir(exist_ok=True)
        (d / f"aggregate_{sys.argv[2]}.txt").write_text(txt, encoding="utf-8")
