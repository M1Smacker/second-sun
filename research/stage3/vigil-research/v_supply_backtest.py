"""RS-001 V-A1 and V-A2 (own data, MAST METADATA only, no light-curve file is downloaded): for the union of our three star lists (G1, G2, G3), which TESS sectors have a SPOC 2-min,
TESS-SPOC or QLP light curve on MAST, when was each released (t_obs_release) and how long after the sector's end. Aggregates only; no star IDs are written to the output.
Usage: python v_supply_backtest.py   (writes research/stage3/vigil-research/vigil-supply-backtest.txt)"""
import warnings, pathlib, sys, time
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from astroquery.mast import Observations
Observations.TIMEOUT = 120
R = pathlib.Path(r"D:\second-sun")
tics = set()
for g in ("g1", "g2", "g3"):
    tics |= set(pd.read_csv(R / "targets" / f"{g}_targets.csv", comment="#").tic.astype(int))
tics = sorted(tics); print(len(tics), "stars in the union of G1, G2, G3", flush=True)
frames = []
def run(kw, batch, label):
    for attempt in range(3):
        try:
            t = Observations.query_criteria(target_name=[str(x) for x in batch], **kw).to_pandas()
            t["prod"] = label; return t
        except Exception as e:
            print("retry", label, type(e).__name__, str(e)[:80], flush=True); time.sleep(20 * (attempt + 1))
    print("FAILED batch", label, flush=True); return None
for i in range(0, len(tics), 60):
    b = tics[i:i + 60]
    for kw, label in ((dict(obs_collection="TESS", dataproduct_type="timeseries", provenance_name="SPOC"), "SPOC"),
                      (dict(obs_collection="HLSP", provenance_name=["QLP", "TESS-SPOC"]), None)):
        t = run(kw, b, label or "HLSP")
        if t is not None and len(t):
            if label is None: t["prod"] = t.provenance_name
            frames.append(t[["target_name", "prod", "sequence_number", "t_min", "t_max", "t_exptime", "t_obs_release"]])
    print(f"batch {i // 60 + 1}/{-(-len(tics) // 60)} done, rows so far {sum(len(f) for f in frames)}", flush=True)
d = pd.concat(frames); d = d.dropna(subset=["sequence_number", "t_obs_release", "t_max"])
d["sector"] = d.sequence_number.astype(int); d["lag_d"] = d.t_obs_release - d.t_max
send = d.groupby("sector").t_max.median()                    # sector end (MJD) = median end of the files of that sector
d["lag_sector_end_d"] = d.t_obs_release - d.sector.map(send)
out = [f"MAST metadata backtest, {pd.Timestamp.now():%Y-%m-%d %H:%M} Kuwait. Stars in the union of G1, G2, G3: {len(tics)}. Rows: {len(d)}. Aggregates only.",
       "sector | product | stars with a file | share of union list | median days from sector end to release | 10th to 90th percentile"]
for (s, p), g in d.groupby(["sector", "prod"]):
    if s >= 85:
        q = g.lag_sector_end_d.quantile([.1, .5, .9]).values
        out.append(f"{s:3d} | {p:9s} | {g.target_name.nunique():5d} | {100 * g.target_name.nunique() / len(tics):4.1f}% | {q[1]:6.1f} | {q[0]:6.1f} to {q[2]:6.1f}")
out.append("")
out.append("All sectors (any year), median release lag by product in days from the sector end (first number: all sectors; second: sectors 70 and later):")
for p, g in d.groupby("prod"):
    out.append(f"  {p:9s}: {g.lag_sector_end_d.median():7.1f} | {g[g.sector >= 70].lag_sector_end_d.median():7.1f}   (files {len(g)})")
last = d.groupby("prod").sector.max()
out.append("Latest sector on MAST per product: " + ", ".join(f"{k} S{v}" for k, v in last.items()))
mjd = lambda x: (pd.Timestamp("1858-11-17") + pd.Timedelta(days=float(x))).strftime("%Y-%m-%d")
out.append("Sector end dates (UTC), latest 6 sectors: " + ", ".join(f"S{s} {mjd(send[s])}" for s in sorted(send.index)[-6:]))
out.append("Latest release date seen per product: " + ", ".join(f"{k} {mjd(g.t_obs_release.max())}" for k, g in d.groupby("prod")))
pathlib.Path(__file__).with_name("vigil-supply-backtest.txt").write_text("\n".join(out) + "\n", encoding="utf-8"); print("\n".join(out[:3]))
