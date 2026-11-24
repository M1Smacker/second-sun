"""Census: TIC ids for the Gaia DR3 slow pool binaries that are in none of our lists (Claude, 24 Nov 2026).

Input: data/census_union/gaia_dr3_matched.csv (to exclude matched ones) and data/ffi_door_2026-11-08/gaia_pool_p5.csv.
Selection: Gaia P over 5 d, G 13.5 or brighter, not matched to the union (the 5,382 of the T139 note).
Query: MAST TIC v8.2 by GAIA id (TIC's GAIA column holds Gaia DR2 ids; most DR3 ids are the same; misses are counted, not guessed).
Output (new folder): data/census_tic_xmatch/gaia_slow_bright_tic.csv, summary.json. Then: how many are 2-minute targets from sector 27 on.
Usage: python gaia_tic_xmatch.py [batch_limit]   (batch_limit = number of 500-id batches; omit for all)
"""
import json, pathlib, sys, time, glob, re
import pandas as pd
from astroquery.mast import Catalogs

D = pathlib.Path(r"D:\second-sun\data")
OUT = D / "census_tic_xmatch"
OUT.mkdir(exist_ok=True)
g = pd.read_csv(D / "ffi_door_2026-11-08/gaia_pool_p5.csv", dtype={"source_id": str})
m = pd.read_csv(D / "census_union/gaia_dr3_matched.csv", dtype={"gaia_source_id": str})
sel = g[(1 / g.frequency > 5) & (g.phot_g_mean_mag <= 13.5) & ~g.source_id.isin(set(m.gaia_source_id))].copy()
print("selected", len(sel))
ids = sel.source_id.tolist()
limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
rows = []
for k, i in enumerate(range(0, len(ids), 500)):
    if limit is not None and k >= limit: break
    chunk = ids[i:i + 500]
    for attempt in range(3):
        try:
            t = Catalogs.query_criteria(catalog="Tic", GAIA=chunk)
            break
        except Exception as e:
            print("retry", k, attempt, type(e).__name__); time.sleep(10)
    else:
        print("batch failed", k); continue
    if len(t):
        rows.append(t[["ID", "GAIA", "Tmag", "ra", "dec", "objType", "disposition"]].to_pandas())
    print("batch", k, "asked", len(chunk), "got", len(t), flush=True)
x = pd.concat(rows) if rows else pd.DataFrame(columns=["ID", "GAIA", "Tmag"])
x = x.rename(columns={"ID": "tic", "GAIA": "source_id"})
x = x[x.disposition.fillna("") != "ARTIFACT"] if "disposition" in x else x
x["tic"] = x.tic.astype("int64")
out = sel.merge(x[["tic", "source_id", "Tmag"]], on="source_id", how="left")
late = set()
for f in glob.glob(str(D / "census_targets_2m/all_targets_S*_v1.csv")):
    if int(re.search(r"S(\d+)", f).group(1)) >= 27:
        late |= set(pd.read_csv(f, comment="#").iloc[:, 0].astype("int64"))
out["twomin_s27plus"] = out.tic.isin(late)
asked = len(ids) if limit is None else min(len(ids), 500 * limit)
s = dict(selected=len(sel), asked=asked, with_tic=int(out.tic.notna().sum()), duplicates=int(out.source_id.duplicated().sum()),
         twomin_s27plus=int(out.twomin_s27plus.sum()), tmag_le_13_5=int((out.Tmag <= 13.5).sum()))
out.to_csv(OUT / "gaia_slow_bright_tic.csv", index=False)
json.dump(s, open(OUT / "summary.json", "w"), indent=1)
print(json.dumps(s, indent=1))
