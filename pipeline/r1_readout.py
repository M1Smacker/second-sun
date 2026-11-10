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
    plan = json.load(open(folder / "watch_plan.json"))
    nfile = len(glob.glob(str(folder / "groups" / "*.json"))); nsap = len(glob.glob(str(folder / "groups_sap" / "*.json")))
    ref = ref_counts()
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
    P("S1 (Amendment 2): recovered light, tier-1, PDCSAP half, against the fixed seen-star reference counts")
    sealed, kept = t1_counts(E[E.rec]), t1_counts(E[~E.rec])
    r_ref = {b: ref[(name, "recovered", b)] for b in BARS}; k_ref = {b: ref[(name, "kept", b)] for b in BARS}
    ex, rows = fisher_block(name, sealed, r_ref, "recovered light")
    P(f"   VERDICT S1 for {name.upper()}: {'EXCESS (opens private two-key checks only; not a discovery)' if ex else 'NO EXCESS'}   [rule: chance <= {ALPHA} at bar 7 and sealed real share above the seen real share at bars 8, 10, 12]")
    P("   power note: with these counts the smallest excess that could have reached the mark is large; the null excludes only a large excess. Wording fixed in Amendment 2: no excess beyond the imbalance measured on the 704 design stars.")
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
    P(f"S2. False alarms in recovered light (no pass mark, Ahmed's decision of 10 Nov): upside-down tier-1 {k} in {n} star-sectors with recovered light = {1000 * k / max(n, 1):.2f} per 1,000 (95 percent interval {lo:.2f} to {hi:.2f}); stars are correlated, so the interval is a floor")
    txt = "\n".join(OUT)
    assert not re.search(r"\b\d{8,9}\b", txt), "a long number (possible star id) in the readout"
    f = out_file or (C.ROOT / "research" / "stage3" / (f"R1-RESULT-{name}.txt" if sealed_run else f"R1-READOUT-smoketest-{name}.txt"))
    pathlib.Path(f).write_text(txt + "\n", encoding="utf-8")
    P(f"(written to {f})")


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None)
