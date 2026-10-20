r"""Lab 3: plot a light curve and measure its noise. Run:  .\.venv\Scripts\python.exe labs\lab3_plot_and_read.py
Optional: a path to any SPOC _lc.fits file (default: the Kepler-16 sector 82 file from Lab 2)."""
import _env, sys, glob, csv
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from astropy.io import fits
sys.path.insert(0, str(_env.ROOT / "pipeline"))
from detect_v2 import detrend, eclipse_mask_auto

path = sys.argv[1] if len(sys.argv) > 1 else glob.glob(str(_env.DATA / "mastDownload/TESS/*s0082-0000000299096355*/*_lc.fits"))[0]
h = fits.open(path); tic = h[0].header["TICID"]; d = h[1].data
t, sap, pdc, q = d["TIME"], d["SAP_FLUX"], d["PDCSAP_FLUX"], d["QUALITY"]
# The binary's period comes from our G1 list (Kepler's catalogue), looked up by TIC number.
rows = [r for r in csv.DictReader(l for l in open(_env.ROOT / "targets/g1_targets.csv") if not l.startswith("#")) if int(r["tic"]) == tic]
P = float(rows[0]["p_bin_d"]) if rows else None
print(f"TIC {tic}, sector {h[0].header['SECTOR']}, binary period from G1 list: {P} d")

fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ok = np.isfinite(t) & np.isfinite(sap)
ax[0].plot(t[ok], sap[ok] / np.nanmedian(sap), ".", ms=1, color="0.4"); ax[0].set_ylabel("SAP (raw)")
ax[1].plot(t, pdc / np.nanmedian(pdc), ".", ms=1, color="C0"); ax[1].set_ylabel("PDCSAP (cleaned)")
for a in ax:
    for td in t[(q & 32) > 0]:
        a.axvline(td, color="C3", lw=0.6, alpha=0.6)
ax[1].set_xlabel("Time (BTJD days)"); ax[0].set_title("Red lines: momentum dumps (quality bit 32)")
fig.tight_layout(); out = _env.OUT / f"lab3_tic{tic}.png"; fig.savefig(out, dpi=110); print("Picture saved:", out)

# Noise: keep good data, flatten slow wiggles, remove the binary's eclipses, then measure the scatter.
good = (q == 0) & np.isfinite(pdc)
tt, ff = detrend(t[good], pdc[good] / np.nanmedian(pdc[good]))
if P:
    keep, _ = eclipse_mask_auto(tt, ff, P); tt, ff = tt[keep], ff[keep]
    print(f"Eclipses masked: {100 * (1 - keep.mean()):.1f}% of the good data")
robust = lambda x: 1.4826 * np.median(np.abs(x - np.median(x)))
s1 = robust(ff)
print(f"\n{'bin':>7} {'points':>6} {'measured':>9} {'if white':>9}   (scatter in ppm)")
for n, label in ((1, "2 min"), (5, "10 min"), (30, "1 h"), (90, "3 h"), (180, "6 h")):
    m = len(ff) // n * n
    binned = ff[:m].reshape(-1, n).mean(axis=1)       # ponytail: ignores gaps inside a bin; fine for a lesson
    print(f"{label:>7} {n:6d} {robust(binned) * 1e6:9.0f} {s1 / np.sqrt(n) * 1e6:9.0f}")
