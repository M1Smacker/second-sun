"""Vesper benchmark scorecard on a G2 run (G2-SEALED-PLAN.md section 1, lines S1 to S8; preregistration sections 5 to 7 and Amendment 1). Aggregates only; no star ID and no event time is printed
except the one named star in S6 (TOI-1338, a known planet). The pass marks are WRITTEN HERE BEFORE the sealed run and are not edited afterwards: S1 chance 0.01 at bar 7 and real above expected at the other bars;
S2 8 or fewer upside-down tier-1 per 1,000 star-sectors; S3 mirror gap within 3 points; S4 report-only (a difference beyond both 95% intervals is labelled "did not generalise"); S5, S7, S8 report-only; S6 every transit accounted for.
Usage: SS_SET=g2 python benchmark_g2.py RUN_FOLDER LABEL [rows_pickle] [dev_rows_pickle]
  e.g. SS_SET=g2 python benchmark_g2.py dev_73f62615e365 dev ..\\data\\chain_recovery_g2\\rows_g2dev.pkl      (writes research\\stage3\\benchmark-g2-<LABEL>.txt)"""
import sys, json, subprocess, pathlib
import numpy as np, pandas as pd
from scipy.stats import chi2, binomtest
import stage3_core as C, stage3_report as R

T1 = ["1A", "1L", "1B"]
OUT = []
P = lambda s="": (OUT.append(s), print(s, flush=True))
CI = lambda k, n: tuple(np.array(binomtest(int(k), int(n)).proportion_ci(0.95, method="wilson")) * 100) if n else (np.nan, np.nan)


def pois(k, n):
    lo = chi2.ppf(.025, 2 * k) / 2 if k else 0.0
    return 1000 * lo / n, 1000 * chi2.ppf(.975, 2 * (k + 1)) / 2 / n


def s1(E):
    P("S1. Excess of real tier-1 dips over noise (preregistration section 5; PDCSAP half has the fair control, the SAP-only half is reported on its own line and is NEVER evidence)")
    t1 = E[E.tier.isin(T1)]; r1, f1 = R.pdc_half(t1[t1.kind == "real"]), R.pdc_half(t1[t1.kind == "flip"])
    ratios, src = R.asym_ratios()
    if not ratios:
        P("   asymmetry ratio file for this slice not found: S1 NOT COMPUTED (run asymmetry_test.py on this run first)"); return
    rows = []
    for thr in (7, 8, 10, 12):
        a, b = int((r1.snr >= thr).sum()), int((f1.snr >= thr).sum()); lam, p = R.noise_expected(a, b, ratios[max(k for k in ratios if k <= thr)])
        rows.append((thr, a, b, lam, p)); P(f"   bar {thr:2d}: real {a:3d}, upside-down {b:3d}, noise-expected real {lam:5.1f}, chance of at least the observed {p:.3f}")
    ex = rows[0][4] <= 0.01 and all(r[1] > r[3] for r in rows[1:])
    P(f"   VERDICT S1: {'EXCESS (opens two-key vetting only; not a discovery)' if ex else 'NO EXCESS'}   [rule: chance <= 0.01 at bar 7 and real above expected at bars 8, 10, 12]   asymmetry file: {src}")
    so = t1[t1.seen_by == "SAP only"] if "seen_by" in t1 else t1.iloc[0:0]
    P(f"   SAP-only half (no fair control, not evidence): real {int((so.kind == 'real').sum())}, upside-down {int((so.kind == 'flip').sum())}")


def s2(E, meta):
    ss = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"]); n = len(ss)
    k = int(((E.kind == "flip") & E.tier.isin(T1)).sum()); lo, hi = pois(k, n)
    P(f"S2. False alarms: upside-down tier-1 {k} in {n} star-sectors = {1000 * k / n:.2f} per 1,000 (95% interval {lo:.2f} to {hi:.2f}); mark 8 or fewer: {'PASS' if 1000 * k / n <= 8 else 'FAIL (v8 did not generalise)'}"
      f"{'' if hi <= 8 or 1000 * k / n > 8 else ' (interval reaches above 8)'}")


def rows_of(path):
    r = pd.read_pickle(path); r = r[r.K.notna() & r.error.isna()]
    return r[r.K.isin((8., 10., 12., 14.))].copy()


def s3_s4(rows, dev):
    d, b = rows[rows.sign == 1], rows[rows.sign == -1]
    gap = 100 * (d.tier1.astype(bool).mean() - b.tier1.astype(bool).mean())
    P(f"S3. Mirror test, planted dips against planted bumps through the whole chain (K 8 to 14): dips {100 * d.tier1.astype(bool).mean():.1f}%, bumps {100 * b.tier1.astype(bool).mean():.1f}%, gap {gap:+.1f} points; mark within 3: {'PASS' if abs(gap) <= 3 else 'FAIL'}")
    P("S4. Completeness, planted dips, tier-1 recovery by box length (K 8 to 14 pooled), 95% Wilson interval" + (" and the development slice beside it" if dev is not None else ""))
    for dur in sorted(d.dur.unique()):
        g = d[d.dur == dur]; k, n = int(g.tier1.astype(bool).sum()), len(g); lo, hi = CI(k, n); line = f"   {dur:g} h box: {100 * k / n:5.1f}% ({lo:.1f} to {hi:.1f}), n {n}"
        if dev is not None:
            h = dev[(dev.sign == 1) & (dev.dur == dur)]; k2, n2 = int(h.tier1.astype(bool).sum()), len(h); lo2, hi2 = CI(k2, n2)
            line += f"   | development {100 * k2 / n2:5.1f}% ({lo2:.1f} to {hi2:.1f})" + ("   DID NOT GENERALISE" if (lo > hi2 or lo2 > hi) else "")
        P(line)
    for dur in sorted(d.dur.unique()):                                           # depth in multiples of the 8 h noise at which half are recovered
        g = d[d.dur == dur].groupby("K").tier1.apply(lambda s: s.astype(bool).mean())
        P(f"   {dur:g} h box by K (depth in noise multiples): " + ", ".join(f"{k:g}: {100 * v:.0f}%" for k, v in g.items()))


def s5(E, rows):
    ol = E[E.orbit_lock.fillna(False)] if "orbit_lock" in E else E.iloc[0:0]
    P(f"S5. Orbit-locked flag (c6): {len(ol)} events moved to tier 2 ({int((ol.kind == 'real').sum())} real, {int((ol.kind == 'flip').sum())} upside-down) on {ol.tic.nunique()} stars")
    eph = C.Ephem(pd.read_csv(C.TARGETS, comment="#"), C.eb_widths()); real = E[(E.kind == "real") & E.tier.isin(T1 + ["2"])]
    by = {t: g for t, g in real[real.tier.isin(T1) | real.orbit_lock.fillna(False)].groupby("tic")} if "orbit_lock" in real else {}
    r1 = rows[(rows.sign == 1) & rows.tier1.astype(bool) & rows.tc.notna()]; hit = 0
    for r in r1.itertuples():
        g = by.get(int(r.tic)); Ps = [p for _, p, _ in eph.by.get(int(r.tic), [])]
        if g is None or not Ps:
            continue
        for c, d_, dp, s_ in zip(g.center, g.dur_h, g.depth_ppm, g.sector):
            if s_ != r.sector and 1 / C.LOCK_BOX <= r.dur / d_ <= C.LOCK_BOX and 1 / C.LOCK_DEPTH <= r.depth_ppm / dp <= C.LOCK_DEPTH and any(C.lock_pair(r.tc, r.dur, c, d_, p) for p in Ps):
                hit += 1; break
    P(f"   cost on planted dips (offline, the harness cannot see other sectors): {hit} of {len(r1)} tier-1 planted dips would be flagged by chance = {100 * hit / max(1, len(r1)):.2f}% (development slice: 0.81%)")


def s6(E, tic=260128333):
    f = pathlib.Path(C.ROOT / "research" / "stage3" / "toi1338b-expected.json")
    if not f.exists():
        P("S6. TOI-1338 b: expected-transit file not written yet (research/stage3/toi1338b-expected.json): NOT COMPUTED"); return
    ex = json.load(open(f)); g = E[(E.tic == tic) & (E.kind == "real")]
    P(f"S6. TOI-1338 b (known circumbinary planet; ephemeris from {ex['source']}): {len(ex['epochs'])} expected transits fall in the downloaded sectors")
    for e in ex["epochs"]:
        near = g[(g.center - e["btjd"]).abs() < 0.3]
        P(f"   epoch BTJD {e['btjd']:.2f} (sector {e['sector']}): " + ("; ".join(f"found, box {r.dur_h:g} h, SNR {r.snr:.1f}, tier {r.tier}" + (f", flags {[k for k in ('gap_dump','common','flipmatch','c5','ecl_overlap','repeater','step','ramp','dominated','orbit_lock') if r.get(k)]}" if r.tier == "2" else "") for r in near.itertuples()) if len(near) else "no event within 0.3 d (missed, or inside an eclipse or a gap: look up why)"))


def s8(meta, ev):
    P(f"S8. Machine health: {meta[['tic', 'sector']].drop_duplicates().shape[0]} star-sectors read; file statuses: {meta.status.value_counts().to_dict()}; {len(ev)} events written; products: {meta['product'].value_counts().to_dict()}")


if __name__ == "__main__":
    run, label = sys.argv[1], sys.argv[2]
    assert C.DS.NAME == "g2", "run with SS_SET=g2"
    ev, meta = R.load(str(C.DS.RUNS / run / "groups")); E = ev[ev.primary]
    rows = rows_of(sys.argv[3]) if len(sys.argv) > 3 else None
    dev = rows_of(sys.argv[4]) if len(sys.argv) > 4 else None
    P(f"VESPER BENCHMARK on G2 run {run} ({label})   Vesper options {sorted(C.V.ON)}")
    s1(E); s2(E, meta)
    if rows is not None:
        s3_s4(rows, dev); s5(E, rows)
    else:
        P("S3, S4, S5: planted-dip rows not given: NOT COMPUTED")
    s6(E)
    r = subprocess.run([sys.executable, str(pathlib.Path(__file__).with_name("g2_labels_report.py")), run, label], capture_output=True, text=True)
    P(f"S7. Labels split (professionals' table, not in it, TOIs, none): research/stage3/g2-by-label-{label}.txt" + ("" if r.returncode == 0 else f"  [labels script failed: {r.stderr[-150:]}]"))
    s8(meta, E)
    (C.ROOT / "research" / "stage3" / f"benchmark-g2-{label}.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
