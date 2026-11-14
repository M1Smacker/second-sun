"""FIX 84 measurement (Claude, 15 Nov 2026): do QLP cadences flagged with the new bit (2^30, from sector 56) survive the frozen loader?
Design stars of G2 and G3 only. Step 1: raw count of flagged cadences per QLP file (all files). Step 2: for up to 60 files with flagged
cadences, call detect_v2.load (frozen, read only) and count flagged cadences whose time survives. Counts to fix84.json."""
import glob, json, os, re, sys
from pathlib import Path
import numpy as np, pandas as pd
from astropy.io import fits
ROOT = Path(r"D:\second-sun"); sys.path.insert(0, str(ROOT / "pipeline"))
B31, B13 = 1 << 30, 1 << 12
r1 = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
r1 = r1[r1["list"].isin(["g2", "g3"]) & (r1.design_seen == 1)].drop_duplicates("tic")
rows = []
for tic, camp in zip(r1.tic.astype(int), r1["list"]):
    for p in glob.glob(str(ROOT / "data" / camp / str(tic) / "hlsp_qlp*_llc.fits")):
        m = re.search(r"_s(\d{4})-", os.path.basename(p)); sec = int(m.group(1))
        with fits.open(p, memmap=False) as h:
            q = np.asarray(h[1].data["QUALITY"], np.int64); t = np.asarray(h[1].data["TIME"], float)
        rows.append(dict(camp=camp, tic=tic, sector=sec, path=p, n=len(q), b31=int(((q & B31) > 0).sum()), b13=int(((q & B13) > 0).sum())))
df = pd.DataFrame(rows); df["era"] = np.where(df.sector >= 56, "56+", "<56")
out = {"files": df.groupby("era").agg(files=("n", "size"), cadences=("n", "sum"), with_b31=("b31", lambda s: int((s > 0).sum())),
                                      b31=("b31", "sum"), b13=("b13", "sum")).to_dict("index")}
print(json.dumps(out, default=int), flush=True)
from detect_v2 import load
cand = df[df.b31 > 0].sort_values("sector").iloc[::max(1, int(np.ceil((df.b31 > 0).sum() / 60)))]
surv = []
for r in cand.itertuples():
    with fits.open(r.path, memmap=False) as h:
        q = np.asarray(h[1].data["QUALITY"], np.int64); t = np.asarray(h[1].data["TIME"], float)
    tf = t[((q & B31) > 0) & np.isfinite(t)]
    try:
        tl = np.asarray(load(r.path)[0], float)
    except Exception as e:
        surv.append(dict(sector=r.sector, flagged=len(tf), survived=None, err=type(e).__name__)); continue
    s = int(np.isin(np.round(tf, 6), np.round(tl, 6)).sum())
    surv.append(dict(sector=r.sector, flagged=len(tf), survived=s, kept=len(tl), n=r.n))
sv = pd.DataFrame(surv)
out["loaded_files"] = len(sv); out["flagged_in_loaded"] = int(sv.flagged.sum()); out["flagged_survived"] = int(sv.survived.fillna(0).sum())
out["files_with_survivors"] = int((sv.survived.fillna(0) > 0).sum()); out["share_of_kept_cadences_flagged"] = round(float(sv.survived.fillna(0).sum() / max(1, sv.kept.fillna(0).sum())), 4)
out["by_sector"] = sv.groupby("sector")[["flagged", "survived"]].sum().astype(int).to_dict("index")
(Path(__file__).parent / "fix84.json").write_text(json.dumps(out, indent=1, default=int), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "by_sector"}, default=int))
