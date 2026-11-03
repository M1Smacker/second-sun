"""T107 (3 Nov 2026): TIC host radius, Teff, logg and Tmag for every G2 and G3 star, read from the primary FITS header (keywords RADIUS, TEFF, LOGG, TESSMAG, TICVER) of the first light-curve
file that carries them (SPOC, then TESS-SPOC, then QLP). Read-only on data; writes a NEW table targets/host_radii_g2_g3.csv (the hashed target lists are not touched). G1 already has tic_radius_rsun
in its own table. Usage: python t107_host_radii.py"""
import glob, os, warnings
warnings.filterwarnings("ignore")
import pandas as pd
from astropy.io import fits
R = r"D:\second-sun"
rows = []
for g, folder in (("g2", "g2"), ("g3", "g3")):
    t = pd.read_csv(f"{R}/targets/{g}_targets.csv", comment="#")
    for tic in t.tic.astype(int):
        rec = dict(tic=tic, set=g, radius_rsun=None, teff=None, logg=None, tmag=None, ticver=None, from_file=None)
        files = sorted(glob.glob(f"{R}/data/{folder}/{tic}/tess*_lc.fits")) + sorted(glob.glob(f"{R}/data/{folder}/{tic}/hlsp_tess-spoc*_lc.fits")) + sorted(glob.glob(f"{R}/data/{folder}/{tic}/hlsp_qlp*_llc.fits"))
        for f in files[:6]:
            try:
                h = fits.getheader(f, 0)
            except Exception:
                continue
            if h.get("RADIUS") not in (None, "") and str(h.get("RADIUS")).lower() != "nan":
                rec.update(radius_rsun=float(h["RADIUS"]), teff=h.get("TEFF"), logg=h.get("LOGG"), tmag=h.get("TESSMAG"), ticver=h.get("TICVER"), from_file=os.path.basename(f).split("-")[0].split("_")[1] if os.path.basename(f).startswith("hlsp") else "spoc")
                break
        rows.append(rec)
d = pd.DataFrame(rows)
d.to_csv(f"{R}/targets/host_radii_g2_g3.csv", index=False)
for g, x in d.groupby("set"):
    r = x.radius_rsun.dropna()
    print(f"{g}: {len(x)} stars, radius found for {len(r)}; median {r.median():.2f} Rsun, 10th to 90th percentile {r.quantile(.1):.2f} to {r.quantile(.9):.2f}; missing {len(x) - len(r)}")
