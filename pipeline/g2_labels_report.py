"""G2 labels clause (G2-PREREGISTRATION.md section 7): the tier-1 counts of a G2 run split by (a) stars in the professionals' 591-star table, (b) stars not in it, (c) TOIs, (d) stars in none of the
three (not in the table, not a TOI, not a NASA-listed circumbinary host). Aggregates only: no star ID, no event time. Real minus upside-down per group and per SNR bar, with the noise-expected line
only when the run's own asymmetry ratio exists (stage3_report.asym_ratios). The label file data/g2/g2_labels_LOCAL.csv stays out of the repository (it holds a fact from their table).
Usage: SS_SET=g2 python g2_labels_report.py <run folder name, e.g. dev_73f62615e365> [label]   (writes research\\stage3\\g2-by-label-<label>.txt)"""
import sys, pathlib
import numpy as np, pandas as pd
import stage3_core as C, stage3_report as R

run, label = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "dev")
assert C.DS.NAME == "g2", "run with SS_SET=g2"
ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
lab = pd.read_csv(C.DS.DATA / "g2_labels_LOCAL.csv").drop_duplicates("tic").set_index("tic")
E = ev[ev.primary].copy()
E["inT"] = E.tic.map(lab.in_prof_table).fillna(False).astype(bool)
E["toi"] = E.tic.map(lab.toi).notna()
E["cbp"] = E.tic.map(lab.known_cbp_host).fillna(False).astype(bool)
pr = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"]).copy()
pr["inT"] = pr.tic.map(lab.in_prof_table).fillna(False).astype(bool)
pr["toi"] = pr.tic.map(lab.toi).notna()
pr["cbp"] = pr.tic.map(lab.known_cbp_host).fillna(False).astype(bool)
groups = {"(a) in the professionals' table": lambda d: d.inT, "(b) not in their table": lambda d: ~d.inT, "(c) TOI hosts": lambda d: d.toi,
          "(d) none of the three": lambda d: ~d.inT & ~d.toi & ~d.cbp, "all": lambda d: d.tic == d.tic}
T1 = ["1A", "1L", "1B"]
ratios, src = R.asym_ratios()
out = [f"G2 {label} run {run}: tier-1 events split by the labels clause (counts only; DEVELOPMENT USE; best product per star-sector; PDCSAP half and SAP half together as in the aggregate report)."]
out.append(f"Asymmetry ratio file used for the noise-expected line: {src or 'none yet'}")
out.append("group | stars | star-sectors | tier-1 real | tier-1 upside-down | by SNR bar 7 / 8 / 10 / 12: real - upside-down")
for name, f in groups.items():
    e, s = E[f(E)], pr[f(pr)]
    r, u = e[(e.kind == "real") & e.tier.isin(T1)], e[(e.kind == "flip") & e.tier.isin(T1)]
    bars = " / ".join(f"{int((r.snr >= t).sum())}-{int((u.snr >= t).sum())}" for t in (7, 8, 10, 12))
    out.append(f"{name:34s} | {s.tic.nunique():4d} | {len(s):5d} | {len(r):4d} | {len(u):4d} | {bars}")
if ratios:
    out.append("Noise-expected check on the PDCSAP half (upside-down tier-1 / measured ratio), SNR 7 bar:")
    thr = 7
    for name, f in groups.items():
        e = E[f(E)]
        r = R.pdc_half(e[(e.kind == "real") & e.tier.isin(T1) & (e.snr >= thr)]); u = R.pdc_half(e[(e.kind == "flip") & e.tier.isin(T1) & (e.snr >= thr)])
        lam, p = R.noise_expected(len(r), len(u), ratios[max(k for k in ratios if k <= thr)])
        out.append(f"  {name:34s} real {len(r):3d}, upside-down {len(u):3d}, noise-expected real {lam:5.1f}, chance {p:.2f}")
txt = "\n".join(out)
leaked = [str(t) for t in E.tic.unique() if str(t) in txt]
assert not leaked, f"star IDs leaked: {leaked[:3]}"
print(txt)
(C.ROOT / "research" / "stage3" / f"g2-by-label-{label}.txt").write_text(txt, encoding="utf-8")
