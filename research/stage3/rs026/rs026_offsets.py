"""RS-026 Q1/Q2 (Claude, 14 Nov 2026): G2 catalogue timing errors (Prsa 2022, data/xmatch/ebs.csv) against what our own light curves show.
Each design light curve's group meta stores Petrova's per-sector primary offset (p1.off, `petrova_mask.refit`: the shift of the deepest primary
position within +-D of the catalogue prediction, D = min(max(3 x timing error, 0.5 x width), P/4)). For G2 design stars: the catalogue 3-sigma
timing term at each sector against the measured |offset|, and whether one star's offsets follow a straight line in cycle number (a period
correction) with small scatter. Counts only to rs026/offsets.json; private rows to data/rs026/offsets.csv."""
import json, os, sys
from pathlib import Path
os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1"); sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import petrova_mask as PM
ROOT = Path(r"D:\second-sun"); cat = PM.cat()
tg = pd.read_csv(ROOT / "targets/r1_targets.csv", comment="#"); tg = tg[(tg["list"] == "g2") & (tg.design_seen == 1)].drop_duplicates("tic")
pb = dict(zip(tg.tic.astype(int), tg.p_bin_d)); BINS = [5, 10, 14, 20, 27.4, 1e9]; LAB = ["5-10", "10-14", "14-20", "20-27.4", "27.4+"]
rows = []
for p in (ROOT / "data/stage3_g2/r1dev_g2_seen_bcd29c7aabb0/groups").glob("*.json"):
    tic, sec = map(int, p.stem.split("_"))
    c = cat.get(tic)
    if tic not in pb or c is None: continue
    for m in json.loads(p.read_text(encoding="utf-8"))["meta"]:
        p1 = m.get("p1") or {}
        if "off" not in p1 or not m.get("file"): continue
        rows.append(dict(tic=tic, sector=sec, product=m.get("product"), status=m.get("status"), off=p1["off"], n_removed=p1.get("n_removed"), n_searched=m.get("n_searched")))
D = pd.DataFrame(rows)
sec_mid = {}  # sector mid-time from the first catalogue-cycle estimate is not stored; use the median of the star's own events instead
for p in (ROOT / "data/stage3_g2/r1dev_g2_seen_bcd29c7aabb0/groups").glob("*.json"):
    tic, sec = map(int, p.stem.split("_"))
    ev = json.loads(p.read_text(encoding="utf-8"))["events"]
    if ev: sec_mid.setdefault(sec, []).append(np.median([e["center"] for e in ev]))
sec_mid = {s: float(np.median(v)) for s, v in sec_mid.items()}
def term(r):
    c = cat[r.tic]; t = sec_mid.get(r.sector, np.nan)
    if not (np.isfinite(t) and np.isfinite(c["T0"]) and np.isfinite(c["P"])): return np.nan, np.nan
    n = abs(round((t - c["T0"]) / c["P"])); a = c["eT0"] if np.isfinite(c["eT0"]) else 0; b = c["eP"] if np.isfinite(c["eP"]) else 0
    return 3 * np.hypot(a, n * b), n
D[["term3", "cycles"]] = D.apply(lambda r: pd.Series(term(r)), axis=1)
D["P"] = D.tic.map(lambda t: cat[t]["P"]); D["wp"] = D.tic.map(lambda t: cat[t]["wp"]); D["bin"] = pd.cut(D.tic.map(pb), BINS, labels=LAB, right=False).astype(str)
D["absoff"] = D.off.abs(); D["blanked"] = D.status == "too little data after masking"
D.to_csv(ROOT / "data/rs026/offsets.csv", index=False)
out = dict(light_curves=int(len(D)), stars=int(D.tic.nunique()))
big = D[D.term3 > 0.5]; small = D[D.term3 <= 0.5]
for name, g in (("term over 0.5 d", big), ("term 0.5 d or less", small)):
    out[name] = dict(light_curves=int(len(g)), stars=int(g.tic.nunique()), blanked=int(g.blanked.sum()),
                     median_term_d=round(float(g.term3.median()), 3), median_abs_offset_d=round(float(g.absoff.median()), 3),
                     abs_offset_quantiles_50_90_99=[round(float(x), 3) for x in g.absoff.quantile([0.5, 0.9, 0.99])],
                     offset_over_width=int((g.absoff > g.wp).sum()))
# per star with 3+ unblanked light curves (best product only would be cleaner; use all): straight-line fit of offset against cycles
fit = []
for tic, g in D[~D.blanked & D.cycles.notna()].groupby("tic"):
    g = g.drop_duplicates("sector")
    if len(g) < 3: continue
    A = np.vstack([g.cycles, np.ones(len(g))]).T; coef, *_ = np.linalg.lstsq(A, g.off, rcond=None)
    resid = g.off - A @ coef
    fit.append(dict(tic=tic, n=len(g), slope_d_per_cycle=coef[0], scatter_d=float(np.std(resid)), wp=g.wp.iloc[0], term3_max=float(g.term3.max())))
F = pd.DataFrame(fit)
out["per_star_line_fit"] = dict(stars=int(len(F)), median_scatter_d=round(float(F.scatter_d.median()), 3),
                                scatter_under_quarter_width=int((F.scatter_d < F.wp / 4).sum()),
                                stars_term_over_0p5d=int((F.term3_max > 0.5).sum()),
                                of_those_scatter_under_quarter_width=int(((F.term3_max > 0.5) & (F.scatter_d < F.wp / 4)).sum()))
(ROOT / "research/stage3/rs026/offsets.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
