"""RS-041 W1b (Claude, 22 Nov 2026, 11:12 pm): of the T156 stage-1 draws classed 'nodata' by W1 (no cadence kept by S2.load within
the dip), how many have cadences in the RAW file there (finite time and flux, any QUALITY) that the load's quality mask drops, and
which QUALITY bits do those cadences carry? Exploratory sizing, design stars only."""
import json, glob, os, collections
import numpy as np
from astropy.io import fits
ROOT = "D:/second-sun"
rows = [r for r in json.load(open(f"{ROOT}/data/rs041/w1_rows.json")) if r["cls"] == "nodata"]
out = collections.Counter(); bits = collections.Counter(); per = collections.Counter()
for r in rows:
    best = None
    for f in glob.glob(f"{ROOT}/data/{r['campaign']}/{r['star']}/*.fits"):
        n = os.path.basename(f).lower()
        fp = "QLP" if "qlp" in n else "TESS-SPOC" if "tess-spoc" in n else "SPOC"
        if (r["product"] in ("nan", fp)) and f"s{r['sector']:04d}" in n:
            best = f; break
    if best is None:
        out["nofile"] += 1; continue
    with fits.open(best) as h:
        d = h[1].data; cols = d.columns.names
        t = np.asarray(d["TIME"], float)
        fl = np.asarray(d["SAP_FLUX"] if "SAP_FLUX" in cols else d[cols[1]], float)
        q = np.asarray(d["QUALITY"], int) if "QUALITY" in cols else np.zeros(len(t), int)
    near = np.isfinite(t) & (np.abs(t - r["time"]) <= r["dur_h"] / 48)
    good = near & np.isfinite(fl)
    if near.sum() == 0:
        out[(r["product"], "true gap: no cadence in file")] += 1
    elif good.sum() == 0:
        out[(r["product"], "cadences, flux NaN")] += 1
    else:
        out[(r["product"], "cadences with flux, dropped at load")] += 1
        for b in range(32):
            if (q[good] & (1 << b)).any(): bits[(r["product"], b)] += 1
print("nodata draws", len(rows))
for k, v in sorted(out.items(), key=str): print(k, v)
print("QUALITY bits set on those cadences (draws per product and bit):")
for k, v in sorted(bits.items(), key=str): print(k, v)
