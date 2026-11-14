"""Re-search 1 readout (preregistration sections 6 and 7 with Amendments 1 and 2). COUNTS ONLY: no star id, no event time, no picture. Reads one run folder (a sealed run, or a development run for a smoke test)
and prints / writes the totals first, then S1 (Amendment 2: sealed recovered-light counts against the fixed seen-star reference counts, one-sided Fisher test), S1 as written in section 6 for the record, the control
(light both masks keep), S2 (false alarms in recovered light), the split by binary-period bin and the single-visit split (S3), and what was skipped.
Usage: SS_SET=g3 SS_RUN=r1_g3_unseen_<hash12> VESPER_OPTS=c6,p1 python r1_readout.py [--out FILE]
       (smoke test on a development run: SS_RUN=r1dev_g3_seen_<hash12>; the result of a seen run is NEVER a verdict.)"""
import os, sys, re, hashlib, pathlib, json, glob
import numpy as np, pandas as pd
from scipy.stats import fisher_exact
import benchmark_g2 as B, stage3_core as C, stage3_report as R

T1 = ["1A", "1L", "1B"]
BARS = (7, 8, 10, 12)
REF = C.ROOT / "research" / "stage3" / "R1-S1-REFERENCE-COUNTS.txt"
REF_SHA = "88ffd47484e0cf88c0977455e91412ac5af34210266eceab5c216abe98cd1c37"      # Amendment 2 (sha256 of the file with LF line endings)
ALPHA = 0.005                                                                       # Amendment 2: 0.01 shared between two lists
REF_BINS = C.ROOT / "research" / "stage3" / "R1-S1-REFERENCE-BINS.txt"
REF_BINS_SHA = "eba2b708884aa7f17dc73650d5d8eb62e2b2db2b017a0f1daf4fe9d1f6e17d20"   # Amendment 3 (sha256 of the file with LF line endings)
BINS = [(5, 10), (10, 14), (14, 20), (20, 27.4), (27.4, 1e9)]
OUT = []


def P(s=""):
    OUT.append(s); print(s, flush=True)


def ref_counts():
    b = REF.read_bytes().replace(b"\r\n", b"\n")
    if hashlib.sha256(b).hexdigest() != REF_SHA:
        sys.exit("REFUSED: the reference counts file does not hash to the value fixed in Amendment 2")
    d = {}
    for m in re.finditer(r"^REF (g\d) (recovered|kept) bar (\d+) real (\d+) flip (\d+)$", b.decode("utf-8"), re.M):
        d[(m[1], m[2], int(m[3]))] = (int(m[4]), int(m[5]))
    return d


def ref_bins():
    b = REF_BINS.read_bytes().replace(b"\r\n", b"\n")
    if hashlib.sha256(b).hexdigest() != REF_BINS_SHA:
        sys.exit("REFUSED: the per-bin reference counts file does not hash to the value fixed in Amendment 3")
    d = {}
    for m in re.finditer(r"^REFBIN (g\d) recovered bar (\d+) bin (\d) real (\d+) flip (\d+)$", b.decode("utf-8"), re.M):
        d[(m[1], int(m[2]), int(m[3]))] = (int(m[4]), int(m[5]))
    return d


def strat_exact(tables):
    """One-sided exact stratified test (Amendment 3): tables = [(real_sealed, flip_sealed, real_seen, flip_seen)] per binary-period bin. Under the null that the real share is the same in the sealed and the seen stars
    inside every bin, the real count of the sealed stars in a bin is hypergeometric; the bins are summed by convolution. Returns the chance of a total of real sealed events at least the observed one."""
    from scipy.stats import hypergeom
    pmf, obs = np.array([1.0]), 0
    for rs, fs, rr, fr in tables:
        ns, rt, n = rs + fs, rs + rr, rs + fs + rr + fr
        if ns == 0 or n == 0:
            continue
        obs += rs
        lo, hi = max(0, ns - (n - rt)), min(ns, rt)
        full = np.zeros(hi + 1)
        full[lo:hi + 1] = hypergeom.pmf(np.arange(lo, hi + 1), n, rt, ns)
        pmf = np.convolve(pmf, full)
    return float(pmf[obs:].sum()) if obs < len(pmf) else 0.0


def strat_block(name, E_rec, refb, label):
    """The Amendment 3 S1 block: sealed per-bin counts against the fixed per-bin reference. Returns (excess?, rows)."""
    t1 = E_rec[E_rec.tier.isin(T1)]
    r, f = R.pdc_half(t1[t1.kind == "real"]), R.pdc_half(t1[t1.kind == "flip"])
    P(f"   {label}: sealed counts split by binary period against the seen counts of the same bin (exact stratified test); events without a binary period: real {int(r.p1_P.isna().sum())}, upside-down {int(f.p1_P.isna().sum())}")
    rows = []
    for b in BARS:
        tabs, exp = [], 0.0
        for k, (lo, hi) in enumerate(BINS):
            rs = int(((r.snr >= b) & (r.p1_P >= lo) & (r.p1_P < hi)).sum()); fs = int(((f.snr >= b) & (f.p1_P >= lo) & (f.p1_P < hi)).sum())
            rr, fr = refb[(name, b, k)]
            tabs.append((rs, fs, rr, fr))
            exp += (rs + fs) * (rr / (rr + fr)) if rr + fr else 0.0
        R_s = sum(t[0] for t in tabs); F_s = sum(t[1] for t in tabs)
        p = strat_exact(tabs)
        rows.append((b, R_s, F_s, exp, p, tabs))
        P(f"   bar {b:2d}: sealed real {R_s:4d}, upside-down {F_s:4d}; real expected from the seen share of each bin {exp:6.1f}; chance {p:.4f}   per bin sealed real/upside-down: " + " ".join(f"{t[0]}/{t[1]}" for t in tabs))
    ex = rows[0][4] <= ALPHA and all(x[1] > x[3] for x in rows[1:])
    return ex, rows


def power_note(sealed, ref):
    """How big would an excess have to be? At bar 7: the smallest real count that the unstratified Fisher test would call an excess given the sealed upside-down count, against the count expected from the seen share."""
    rs, fs = sealed[7]; rr, fr = ref[7]
    if fs == 0 or rr + fr == 0 or fr == 0:
        return "power: not computable (a zero count at bar 7)"
    exp = fs * rr / fr
    for R_try in range(max(rs, 1), 100000):
        if fisher_exact([[R_try, fs], [rr, fr]], alternative="greater")[1] <= ALPHA:
            return f"power: at bar 7 with {fs} upside-down events the sealed real count would have to reach about {R_try} (expected from the seen share about {exp:.0f}), that is about {R_try / exp:.1f} times the expected count; the null excludes only an excess of that size or more"
    return "power: not reached below 100000"


def star_cluster_ci(k_by_star, n_by_star, B=100000, seed=20261114):
    """FIX 88: percentile 95% interval per 1,000 of sum(k)/sum(n), resampling stars with replacement (stars with exposure; k 0 when absent)."""
    stars = list(n_by_star)
    if not stars:
        return float("nan"), float("nan")
    k = np.array([k_by_star.get(s, 0) for s in stars], float); n = np.array([n_by_star[s] for s in stars], float)
    rng = np.random.default_rng(seed); idx = rng.integers(0, len(stars), size=(B, len(stars)))
    r = 1000 * k[idx].sum(1) / np.maximum(n[idx].sum(1), 1)
    return float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))


def t1_counts(E):
    t1 = E[E.tier.isin(T1)]
    r, f = R.pdc_half(t1[t1.kind == "real"]), R.pdc_half(t1[t1.kind == "flip"])
    return {b: (int((r.snr >= b).sum()), int((f.snr >= b).sum())) for b in BARS}


def fisher_block(name, sealed, ref, label):
    P(f"   {label}: sealed real/upside-down against seen real/upside-down, one-sided Fisher chance that the sealed real share is this much larger")
    rows = []
    for b in BARS:
        rs, fs = sealed[b]; rr, fr = ref[b]
        p = float(fisher_exact([[rs, fs], [rr, fr]], alternative="greater")[1])
        sh_s = rs / (rs + fs) if rs + fs else float("nan"); sh_r = rr / (rr + fr) if rr + fr else float("nan")
        rows.append((b, rs, fs, rr, fr, sh_s, sh_r, p))
        P(f"   bar {b:2d}: sealed {rs:4d} / {fs:4d} (real share {sh_s:.2f}), seen {rr:4d} / {fr:4d} (real share {sh_r:.2f}), chance {p:.4f}")
    ex = rows[0][7] <= ALPHA and all(r[5] > r[6] for r in rows[1:])
    return ex, rows


def main(out_file=None):
    name, run = C.DS.NAME, os.environ["SS_RUN"]
    sealed_run = run.startswith("r1_") and "unseen" in run
    folder = C.DS.RUNS / run
    plan = json.load(open(folder / "watch_plan.json", encoding="utf-8"))
    nfile = len(glob.glob(str(folder / "groups" / "*.json"))); nsap = len(glob.glob(str(folder / "groups_sap" / "*.json")))
    ref, refb = ref_counts(), ref_bins()
    ev, meta = R.load(str(folder / "groups"))
    E = ev[ev.primary].copy()
    E["rec"] = E.recovered.fillna(False).astype(bool)
    ok = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"])
    rec_ss = ok[ok["p1"].apply(lambda d: bool(isinstance(d, dict) and d.get("recovered")))]
    P(f"RE-SEARCH 1 READOUT, list {name.upper()}, run {run} ({'SEALED RUN' if sealed_run else 'NOT a sealed run: smoke test, no verdict'}), options {sorted(C.V.ON)}. Counts only.")
    P("")
    P("TOTALS FIRST")
    P(f"   star-sectors searched (best product ok): {len(ok)}, of them with any recovered light: {len(rec_ss)}; stars: {ok.tic.nunique()}")
    P(f"   group files: search {nfile} of {plan['groups']}, raw-light twins {nsap} of {plan['sap']}")
    st = meta.status.value_counts().to_dict(); tot = sum(st.values()); sk = tot - st.get("ok", 0)
    P(f"   files by status: {st}; skipped {sk} of {tot} = {100 * sk / max(tot, 1):.1f} percent")
    P(f"   primary events: real {int((E.kind == 'real').sum())}, upside-down {int((E.kind == 'flip').sum())}; vetoed by the cross-sector veto: real {int(((E.kind == 'real') & E.p1_veto.fillna(False).astype(bool)).sum())}, upside-down {int(((E.kind == 'flip') & E.p1_veto.fillna(False).astype(bool)).sum())}")
    rec = E[E.rec]
    P(f"   events in recovered light: real {int((rec.kind == 'real').sum())}, upside-down {int((rec.kind == 'flip').sum())}; tier-1: real {int(((rec.kind == 'real') & rec.tier.isin(T1)).sum())}, upside-down {int(((rec.kind == 'flip') & rec.tier.isin(T1)).sum())}")
    P("")
    P("S1 (Amendments 2 and 3): recovered light, tier-1, PDCSAP half, against the fixed seen-star reference counts, stratified by binary-period bin (Amendment 3: the unseen stars have a different mix of periods)")
    sealed, kept = t1_counts(E[E.rec]), t1_counts(E[~E.rec])
    r_ref = {b: ref[(name, "recovered", b)] for b in BARS}; k_ref = {b: ref[(name, "kept", b)] for b in BARS}
    ex, rows = strat_block(name, E[E.rec], refb, "recovered light, stratified")
    P(f"   VERDICT S1 for {name.upper()}: {'EXCESS (opens private two-key checks only; not a discovery)' if ex else 'NO EXCESS'}   [rule (Amendment 3): stratified chance <= {ALPHA} at bar 7 and sealed real count above the count expected from the seen share of each bin at bars 8, 10, 12]")
    import s1_sensitivity as SENS                # FIX 86 (14 Nov 2026): the full stratified rule, Codex 002 part B design; replaces power_note (unstratified, worded as an exclusion)
    P("   " + SENS.note({r[0]: r[5] for r in rows}, strat_exact, ALPHA))
    P("   Wording: a null means no excess beyond the real-over-upside-down imbalance measured on the design stars; the sensitivity line is conditional on its stated assumptions and is not an exclusion.")
    P("   The unweighted test of Amendment 2, for the record:")
    exu, rowsu = fisher_block(name, sealed, r_ref, "recovered light, unweighted")
    P("")
    P("CONTROL (light both masks keep; the old filter already judged it; this tells whether the seen and sealed stars behave alike)")
    exk, _ = fisher_block(name, kept, k_ref, "light both masks keep")
    P(f"   control reads: {'a surplus of real events too: the seen-star reference may not transfer to this list, label its null NOT COVERED' if exk else 'no surplus: nothing against the transfer'}")
    P("")
    P("S1 AS WRITTEN IN SECTION 6, FOR THE RECORD (noise-expected from the all-light asymmetry file; superseded by Amendment 2 for the verdict)")
    B.LABEL = "v5"
    B.OUT.clear(); B.s1(E[E.rec])                                   # B.s1 prints its own lines; they are kept for the file below
    OUT.extend(B.OUT)
    P("")
    P("SPLIT BY BINARY PERIOD (tier-1 in recovered light, all bars at 7 and up; counts only, no mark). S3 note: above 13.7 d a binary phase is visited at most about twice per sector, so the last three rows are the near single-visit lane.")
    t1 = E[E.rec & E.tier.isin(T1) & E.p1_P.notna()]
    t1 = R.pdc_half(t1[t1.kind == "real"]), R.pdc_half(t1[t1.kind == "flip"])
    for lo, hi in BINS:
        r = int(((t1[0].p1_P >= lo) & (t1[0].p1_P < hi) & (t1[0].snr >= 7)).sum()); f = int(((t1[1].p1_P >= lo) & (t1[1].p1_P < hi) & (t1[1].snr >= 7)).sum())
        P(f"   {('%g-%g' % (lo, hi)) if hi < 1e8 else 'over %g' % lo:>9} d: real {r:4d}, upside-down {f:4d}")
    P("")
    k = int(((rec.kind == "flip") & rec.tier.isin(T1) & (rec.snr >= 7)).sum()); n = len(rec_ss)
    lo, hi = B.pois(k, max(n, 1))
    fl = rec[(rec.kind == "flip") & rec.tier.isin(T1) & (rec.snr >= 7)]           # FIX 88 (14 Nov 2026): star-clustered bootstrap beside the Poisson interval; "floor" was wrong (Codex 002 part B)
    kb = fl.groupby("tic").size().to_dict(); nb = rec_ss.groupby("tic").size().to_dict()
    clo, chi = star_cluster_ci(kb, nb)
    P(f"S2. False alarms in recovered light (no pass mark, Ahmed's decision of 10 Nov): upside-down tier-1 {k} in {n} star-sectors with recovered light = {1000 * k / max(n, 1):.2f} per 1,000 (Poisson 95 percent interval {lo:.2f} to {hi:.2f}, which ignores that events cluster on stars; a star-clustered bootstrap over {len(nb)} stars gives {clo:.2f} to {chi:.2f}; its coverage is not tested, with only {len(kb)} stars carrying events)")
    txt = "\n".join(OUT)
    assert not re.search(r"\b\d{8,9}\b", txt), "a long number (possible star id) in the readout"
    f = out_file or (C.ROOT / "research" / "stage3" / (f"R1-RESULT-{name}.txt" if sealed_run else f"R1-READOUT-smoketest-{name}.txt"))
    pathlib.Path(f).write_text(txt + "\n", encoding="utf-8")
    P(f"(written to {f})")


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None)
