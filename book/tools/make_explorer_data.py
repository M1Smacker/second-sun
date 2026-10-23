"""Build book/docs/assets/data/toi1338-s98.json: a real TESS light curve for the Chapter 2 explorer.
TOI-1338 (TIC 260128333), sector 98, SPOC 2-minute PDCSAP flux, good cadences only (QUALITY == 0), divided by its median
and averaged into 10-minute bins. Values are stored as ppm away from 1 (null = no data). The planet crossing is the
event our detector found (claim F-040). Run once with the main Python (reads data/, which is not in git):
  .venv\\Scripts\\python.exe book\\tools\\make_explorer_data.py"""
import glob
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from astropy.io import fits

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "labs"))
import _env  # noqa: E402,F401

path = glob.glob(str(REPO / "data/wave-*/lk/mastDownload/TESS/*s0098-0000000260128333-0298-s/*_lc.fits"))[0]
with fits.open(path) as h:
    d = h[1].data
    t, f, q = np.array(d["TIME"], float), np.array(d["PDCSAP_FLUX"], float), np.array(d["QUALITY"])
ok = np.isfinite(t) & np.isfinite(f) & (q == 0)
t, f = t[ok], f[ok] / np.nanmedian(f[ok])
bin_d = 10 / 1440
t0 = float(np.floor(t.min() * 144) / 144)
idx = ((t - t0) / bin_d).astype(int)
n = idx.max() + 1
vals = [None] * n
for i in np.unique(idx):
    vals[i] = int(round((f[idx == i].mean() - 1) * 1e6))
arr = np.array([np.nan if v is None else v for v in vals])
# primary eclipse mid-times: runs of bins more than 2% below 1
low = np.where(np.nan_to_num(arr, nan=0) < -20000)[0]
runs = np.split(low, np.where(np.diff(low) > 12)[0] + 1) if len(low) else []
eclipses = [round(t0 + (r.mean() + 0.5) * bin_d, 3) for r in runs if len(r)]
print("bins", n, "valid", int(np.isfinite(arr).sum()), "t0", t0, "span", round(n * bin_d, 2), "d")
print("eclipse mid-times", eclipses, "deepest", int(np.nanmin(arr)), "ppm; median inside", int(np.median(arr[low])) if len(low) else None)
src = hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]
out = {"what": "TOI-1338 (TIC 260128333) TESS sector 98, SPOC 2-minute PDCSAP flux, QUALITY == 0, median-normalised, 10-minute bins, ppm from 1",
       "source_file": Path(path).name, "sha256_prefix": src, "t0_btjd": t0, "step_days": round(bin_d, 8),
       "planet_btjd": 4025.638, "eclipses_btjd": eclipses, "ppm": vals}
dest = REPO / "book/docs/assets/data/toi1338-s98.json"
dest.parent.mkdir(exist_ok=True)
dest.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
print("wrote", dest, dest.stat().st_size, "bytes")
