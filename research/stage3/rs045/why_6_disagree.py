"""RS-045 (Claude, 23 Nov 2026, 11:25 am): why do 6 of 53 usable fresh-control primary tracks of Codex 032 (eclipse times v3) disagree
with the catalogue? Question tied to a decision: is the v3 fit wrong (no Part B, rethink), or is the catalogue wrong for those stars
(then the judge, not the method, failed; a NEW preregistered judge and a NEW hold-out are needed; the filed FAIL stands).
Test that can decide: compare the catalogue prediction with the eclipse times MEASURED directly in the light (not with our fit).
  - catalogue wrong: measured times sit more than 0.25 width from the catalogue prediction, while the v3 fit's residuals are small;
  - fit wrong: measured times agree with the catalogue but the fit's prediction does not.
Reads Codex's v3 tables (data/astra/032) and the frozen catalogue through petrova_mask.cat() (read-only). Aggregates only."""
import os, sys
import numpy as np, pandas as pd
os.environ["SS_SET"] = "g2"
sys.path.insert(0, "D:/second-sun/pipeline")
import petrova_mask as PM

H = "D:/second-sun/data/astra/032"
e = pd.read_csv(f"{H}/ephemerides-v3.csv"); t = pd.read_csv(f"{H}/eclipse-times-v3.csv")
cat = PM.cat()
p = e[(e.type == "primary") & (e.usable == True)]
print("usable primary tracks", len(p), "agree", int(p.agrees.sum()))
rows = []
for _, r in p.iterrows():
    c = cat[int(r.star)]
    m = t[(t.star == r.star) & (t.type == "primary") & (t.retained == True)]
    n = np.round((m.time - c["T0"]) / c["P"])
    off_cat = (m.time - (c["T0"] + n * c["P"])) / r.width          # measured minus catalogue, in eclipse widths
    nf = np.round((m.time - r.epoch) / r.period)
    off_fit = (m.time - (r.epoch + nf * r.period)) / r.width        # measured minus our fit, in widths
    late = m.sector == m.sector.max()
    rows.append(dict(star=int(r.star), agrees=bool(r.agrees), n=len(m), sectors=int(m.sector.nunique()), bin=int(r.period_bin),
                     cat_med=float(np.median(off_cat)), cat_late=float(np.median(off_cat[late])), cat_max=float(np.max(np.abs(off_cat))),
                     fit_med=float(np.median(np.abs(off_fit))), fit_max=float(np.max(np.abs(off_fit))),
                     dP_sigma=float((r.period - c["P"]) / np.hypot(r.period_error, c["eP"])), cat_pad_late=float(3 * np.hypot(c["eT0"], n.max() * c["eP"]) / r.width)))
R = pd.DataFrame(rows)
pd.set_option("display.width", 200)
for k, g in R.groupby("agrees"):
    print(f"\nagrees={k}: n {len(g)}")
    print(g.drop(columns=["star"]).describe().loc[["50%", "max"]].round(3).to_string())
print("\nthe disagreeing tracks, one row each (offsets in eclipse widths; star ids are design-star ids, not leads):")
print(R[~R.agrees].round(3).to_string(index=False))
print("\nverdict per disagreeing track: catalogue off (|measured - catalogue| late-sector median > 0.25 width) while fit residuals small (median < 0.1):",
      int(((R.cat_late.abs() > 0.25) & (R.fit_med < 0.1))[~R.agrees].sum()), "of", int((~R.agrees).sum()))
