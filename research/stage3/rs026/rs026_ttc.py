"""RS-026 Q3 (Claude, 14 Nov 2026): does the TESS Ten Thousand Catalog's TESS-era ephemeris (Kostov et al. 2025, table 4 for 2,065
known EBs, sectors 1 to 82 FFI; data/g3/catalog_ttc/table4_known_ebs.txt) cover our badly timed G2 stars, and does it predict the eclipse
offsets our own light curves measured (rs026_offsets.py, p1.off) better than the Prsa 2022 catalogue? Prediction of the offset: the TTC primary
time nearest the Prsa-predicted primary of that cycle, minus the Prsa prediction (wrapped to +-P/2). Only light curves where our own line fit
is clean are used as truth (scatter under a quarter of the eclipse width). Counts only to rs026/ttc.json."""
import json, os, sys
from pathlib import Path
os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1"); sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import petrova_mask as PM
ROOT = Path(r"D:\second-sun"); cat = PM.cat()
ttc = {}
for l in open(ROOT / "data/g3/catalog_ttc/table4_known_ebs.txt", encoding="latin-1"):
    if l[:10].strip().isdigit():
        try: ttc[int(l[0:10])] = (float(l[37:46]), float(l[47:58]))
        except ValueError: pass
D = pd.read_csv(ROOT / "data/rs026/offsets.csv")
big = set(D[D.term3 > 0.5].tic)
out = dict(ttc_known_rows=len(ttc), g2_design_stars=int(D.tic.nunique()), big_term_stars=len(big),
           big_term_in_ttc=len(big & set(ttc)), all_g2_design_in_ttc=len(set(D.tic) & set(ttc)))
rows = []
for r in D[D.tic.isin(big & set(ttc)) & (D.status == "ok")].itertuples():
    c = cat[r.tic]; Pt, Tt = ttc[r.tic]
    if not (abs(Pt / c["P"] - 1) < 0.02): rows.append(dict(tic=r.tic, period_mismatch=True)); continue
    # sector mid-time: Prsa prediction for this cycle
    tpred = c["T0"] + r.cycles * c["P"] * np.sign(1)
    for sgn in (1, -1):
        tp = c["T0"] + sgn * r.cycles * c["P"]
        if 1300 < tp < 4500: tpred = tp; break
    n = round((tpred - Tt) / Pt); tt = Tt + n * Pt
    d = ((tt - tpred + c["P"] / 2) % c["P"]) - c["P"] / 2
    rows.append(dict(tic=r.tic, period_mismatch=False, ttc_pred_off=d, measured_off=r.off, wp=r.wp, term3=r.term3))
R = pd.DataFrame(rows)
out["period_mismatch_stars"] = int(R[R.period_mismatch == True].tic.nunique()) if len(R) else 0
R = R[R.period_mismatch == False] if len(R) else R
if len(R):
    R["err_ttc"] = (R.ttc_pred_off - R.measured_off).abs(); R["err_prsa"] = R.measured_off.abs()
    out["light_curves_compared"] = int(len(R)); out["stars_compared"] = int(R.tic.nunique())
    out["median_abs_error_d"] = dict(prsa=round(float(R.err_prsa.median()), 3), ttc=round(float(R.err_ttc.median()), 3))
    out["ttc_error_under_quarter_width"] = int((R.err_ttc < R.wp / 4).sum()); out["prsa_error_under_quarter_width"] = int((R.err_prsa < R.wp / 4).sum())
    out["median_prsa_3sigma_term_d"] = round(float(R.term3.median()), 3)
(ROOT / "research/stage3/rs026/ttc.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
