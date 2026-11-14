"""RS-025 Q3 (Claude, 14 Nov 2026): how much light does Petrova's mask remove, and how many design light curves does it blank
(status 'too little data after masking', fewer than 200 points left)? Per light curve: status, product, cadence, points removed and the share
removed; plus the catalogue ephemeris-uncertainty term of the window half-width (3 x sqrt(eT0^2 + (n eP)^2), petrova_mask.windows) at the
sector's mid-time. Design stars only. Counts only to rs025/masklost.json."""
import json, os, sys
from collections import Counter
from pathlib import Path
os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1")
sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
ROOT = Path(r"D:\second-sun")
import petrova_mask as PM
cat = PM.cat()
tg = pd.read_csv(ROOT / "targets/r1_targets.csv", comment="#"); tg = tg[tg["list"].isin(["g2", "g3"]) & (tg.design_seen == 1)].drop_duplicates("tic")
pb = dict(zip(tg.tic.astype(int), tg.p_bin_d)); BINS = [5, 10, 14, 20, 27.4, 1e9]; LAB = ["5-10", "10-14", "14-20", "20-27.4", "27.4+"]
rows = []
for camp in ("g2", "g3"):
    for p in (ROOT / f"data/stage3_{camp}/r1dev_{camp}_seen_bcd29c7aabb0/groups").glob("*.json"):
        tic, sec = map(int, p.stem.split("_"))
        if tic not in pb: continue
        for m in json.loads(p.read_text(encoding="utf-8"))["meta"]:
            p1 = m.get("p1") or {}
            c = cat.get(tic)
            unc = None
            if c is not None and p1.get("T0") is not None:
                tmid = p1["T0"] + 0  # placeholder replaced below
            rows.append(dict(camp=camp, tic=tic, sector=sec, product=m.get("product"), status=m.get("status"), cad=m.get("cadence_min"),
                             n_removed=p1.get("n_removed"), n_searched=m.get("n_searched"), cat=bool(p1.get("cat")),
                             eT0=(c or {}).get("eT0"), eP=(c or {}).get("eP"), P=(c or {}).get("P"), T0=(c or {}).get("T0"), wp=(c or {}).get("wp")))
D = pd.DataFrame(rows); D["bin"] = pd.cut(D.tic.map(pb), BINS, labels=LAB, right=False).astype(str)
D["share_removed"] = D.n_removed / (D.n_removed + D.n_searched)
out = dict(light_curves=int(len(D)), status=dict(Counter(D.status)))
out["blanked_by_mask_by_bin"] = {b: dict(n=int(len(g)), blanked=int((g.status == "too little data after masking").sum())) for b, g in D.groupby("bin")}
ok = D[D.status == "ok"]
out["share_removed_ok_curves_quantiles"] = {b: [round(float(x), 3) for x in g.share_removed.quantile([0.5, 0.9, 0.99])] for b, g in ok.groupby("bin")}
bl = D[D.status == "too little data after masking"]
out["blanked_products"] = dict(Counter(bl["product"])); out["blanked_cadence_min"] = dict(Counter(bl.cad.round(1)))
out["blanked_with_catalogue_entry"] = int(bl.cat.sum())
# window half-width from ephemeris uncertainty at a typical TESS time of that sector (sector mid-time approximated from the star's events is not stored; use T0 offset by cycles to BTJD 2500)
def unc(r, t=2500.0):
    if not (r.P and r.P == r.P and r.T0 == r.T0): return np.nan
    n = abs(round((t - r.T0) / r.P)); a = r.eT0 if r.eT0 == r.eT0 else 0; b = r.eP if r.eP == r.eP else 0
    return 3 * np.sqrt(a * a + (n * b) ** 2)
u = D.drop_duplicates("tic").copy(); u["unc_d"] = u.apply(unc, axis=1); u["frac_of_P"] = 4 * u.unc_d / u.P   # two windows, each 2 x unc wide
out["ephemeris_term_at_BTJD2500"] = {b: dict(stars=int(len(g)), median_unc_d=round(float(g.unc_d.median()), 3), stars_unc_over_0p5d=int((g.unc_d > 0.5).sum()), stars_windows_cover_half_orbit=int((g.frac_of_P > 0.5).sum())) for b, g in u.groupby("bin")}
bt = set(bl.tic); out["blanked_stars"] = len(bt); out["blanked_stars_unc_over_0p5d"] = int(u[u.tic.isin(bt)].unc_d.gt(0.5).sum())
(ROOT / "research/stage3/rs025/masklost.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
