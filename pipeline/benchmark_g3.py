"""Vesper scorecard on the G3 run (G3-PREREGISTRATION.md sections 5 and 6 with Amendment 1). The lines S1, S2, S3, S4, S5 and S8 are the functions of benchmark_g2.py unchanged (their pass marks were written there before the
G2 sealed run and are not edited); S6 (TOI-1338 b) does not apply to G3, whose stars are not that star; S7 splits the tier-1 counts by the labels clause of section 6 (TOI hosts, NASA-listed circumbinary hosts, none of the two; the
G3 list excludes the professionals' table by rule). Aggregates only: no star ID and no event time is printed.
Usage: SS_SET=g3 VESPER_OPTS=c6 python benchmark_g3.py RUN_FOLDER LABEL [G3 planted rows pickle] [comparison rows pickle]     (writes research\stage3\benchmark-g3-<LABEL>.txt and g3-by-label-<LABEL>.txt)
The asymmetry ratio of this run must exist first: python asymmetry_test.py 1500 v5 RUN_FOLDER   (writes asymmetry_g3_v5.txt)."""
import sys, pathlib
import numpy as np, pandas as pd
import benchmark_g2 as B, stage3_core as C, stage3_report as R

T1 = ["1A", "1L", "1B"]


def labels_table():
    """data/g3/g3_labels_LOCAL.csv (kept out of the repository like the G2 one): tic, toi (TOI number or empty), known_cbp_host."""
    f = C.DS.DATA / "g3_labels_LOCAL.csv"
    if not f.exists():
        tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic")
        toi = pd.read_csv(C.ROOT / "data" / "xmatch" / "toi.csv").drop_duplicates("tid").set_index("tid")["toi"]
        cbp = pd.read_csv(C.ROOT / "data" / "xmatch" / "cbp.csv").tic_id.astype(str).str.extract(r"(\d+)")[0].dropna().astype(int)
        pd.DataFrame(dict(tic=tg.tic, toi=tg.tic.map(toi), known_cbp_host=tg.tic.isin(set(cbp)))).to_csv(f, index=False)
    return pd.read_csv(f).drop_duplicates("tic").set_index("tic")


def s7(E, meta, label, run):
    lab = labels_table()
    for d in (E, meta):
        d["toi"] = d.tic.map(lab.toi).notna(); d["cbp"] = d.tic.map(lab.known_cbp_host).fillna(False).astype(bool)
    pr = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"])
    groups = {"(a) TOI hosts": lambda d: d.toi, "(b) NASA-listed circumbinary hosts": lambda d: d.cbp, "(c) none of the two": lambda d: ~d.toi & ~d.cbp, "all": lambda d: d.tic == d.tic}
    out = [f"G3 {label} run {run}: tier-1 events split by the labels clause (counts only; best product per star-sector; PDCSAP half and SAP half together as in the aggregate report).",
           "group | stars | star-sectors | tier-1 real | tier-1 upside-down | by SNR bar 7 / 8 / 10 / 12: real - upside-down"]
    for name, f in groups.items():
        e, s = E[f(E)], pr[f(pr)]
        r, u = e[(e.kind == "real") & e.tier.isin(T1)], e[(e.kind == "flip") & e.tier.isin(T1)]
        out.append(f"{name:36s} | {s.tic.nunique():4d} | {len(s):5d} | {len(r):4d} | {len(u):4d} | " + " / ".join(f"{int((r.snr >= t).sum())}-{int((u.snr >= t).sum())}" for t in (7, 8, 10, 12)))
    txt = "\n".join(out)
    assert not [t for t in E.tic.unique() if str(t) in txt], "star IDs leaked"
    (C.ROOT / "research" / "stage3" / f"g3-by-label-{label}.txt").write_text(txt, encoding="utf-8")
    B.P(f"S7. Labels split (TOI hosts, NASA-listed circumbinary hosts, none): research/stage3/g3-by-label-{label}.txt"); B.P(txt)


if __name__ == "__main__":
    run, label = sys.argv[1], sys.argv[2]; B.LABEL = label
    assert C.DS.NAME == "g3", "run with SS_SET=g3"
    ev, meta = R.load(str(C.DS.RUNS / run / "groups")); E = ev[ev.primary].copy()
    rows = B.rows_of(sys.argv[3]) if len(sys.argv) > 3 else None
    cmp_rows = B.rows_of(sys.argv[4]) if len(sys.argv) > 4 else None
    B.P(f"VESPER BENCHMARK on G3 run {run} ({label})   Vesper options {sorted(C.V.ON)}")
    B.s1(E); B.s2(E, meta)
    if rows is not None:
        B.s3_s4(rows, cmp_rows); B.s5(E, rows)
    else:
        B.P("S3, S4, S5: planted-dip rows not given: NOT COMPUTED")
    B.P("S6. Not applicable to G3 (the known-planet line belongs to the G2 sealed star TOI-1338).")
    s7(E, meta, label, run); B.s8(meta, E)
    (C.ROOT / "research" / "stage3" / f"benchmark-g3-{label}.txt").write_text("\n".join(B.OUT) + "\n", encoding="utf-8")
