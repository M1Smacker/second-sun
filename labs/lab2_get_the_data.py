r"""Lab 2: download one sector and look inside. Run:  .\.venv\Scripts\python.exe labs\lab2_get_the_data.py "Kepler-16" 82"""
import _env, sys
import numpy as np, lightkurve as lk
from astropy.io import fits

name = sys.argv[1] if len(sys.argv) > 1 else "Kepler-16"
sector = int(sys.argv[2]) if len(sys.argv) > 2 else 82
res = lk.search_lightcurve(name, sector=sector, author="SPOC", exptime=120)
print(res)
lc = res[0].download(download_dir=str(_env.DATA))     # about 2 MB; skipped if already downloaded
path = lc.meta["FILENAME"]
print("\nSaved to:", path)
with fits.open(path) as h:
    hd = h[0].header
    print(f"Header: OBJECT={hd['OBJECT']}  TICID={hd['TICID']}  SECTOR={hd['SECTOR']}  CAMERA={hd['CAMERA']}  CCD={hd['CCD']}  TESSMAG={hd['TESSMAG']}")
    cols = h[1].columns.names
    print("Columns:", ", ".join(cols))
    d = h[1].data
    t, q = d["TIME"], d["QUALITY"]
    print(f"Cadences: {len(t)}, from BTJD {np.nanmin(t):.2f} to {np.nanmax(t):.2f} ({np.nanmax(t) - np.nanmin(t):.1f} days)")
    print(f"Every {np.nanmedian(np.diff(t)) * 1440:.1f} minutes")
    print(f"Flagged by quality bits: {np.sum(q > 0)} cadences; momentum dumps (bit 32): {np.sum((q & 32) > 0)}")
    good = np.isfinite(d["PDCSAP_FLUX"])
    print(f"PDCSAP flux present on {good.sum()} cadences; median {np.nanmedian(d['PDCSAP_FLUX']):.0f} electrons per second")
