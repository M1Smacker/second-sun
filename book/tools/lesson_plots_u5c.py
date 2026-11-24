"""Unit 5 plot and numbers, lesson 5.3 From pixels to light curves (Claude, 24 Nov 2026).

Sector 46 of TIC 172900988: the RAW aperture sum (SAP_FLUX), binned to 30 minutes, to set beside lesson 5.2's corrected light (PDCSAP).
Prints the file's own numbers: stamp size, aperture and background pixels, CROWDSAP, FLFRCSAP, PDC method, median SAP and PDCSAP, background.
Checks (a failure stops): median PDCSAP / median SAP equals CROWDSAP / FLFRCSAP within 0.5% (the PDC crowding and flux-fraction
correction, Stumpe et al. 2012 section 2.3.11: y' = (y - (1 - c) median(y)) / f, whose median is c median(y) / f).
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u5c.py
"""
import glob, json, pathlib, sys
import numpy as np
from astropy.io import fits

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lesson_plots as LP

TIC = 172900988
p = glob.glob(str(LP.ROOT / "data" / "known" / "172900988" / "tess2021*-s0046-*_lc.fits"))[0]
h1 = fits.getheader(p, 1)
ap = fits.getdata(p, 2)
d = fits.getdata(p, 1)
if int(fits.getheader(p, 0)["TICID"]) != TIC: sys.exit("wrong star")
q = (d["QUALITY"] == 0) & np.isfinite(d["SAP_FLUX"]) & np.isfinite(d["PDCSAP_FLUX"])
t, sap, pdc, bkg = d["TIME"][q], d["SAP_FLUX"][q], d["PDCSAP_FLUX"][q], d["SAP_BKG"][q]
c, fr = h1["CROWDSAP"], h1["FLFRCSAP"]
ratio = np.median(pdc) / np.median(sap)
print(f"stamp {ap.shape[0]} x {ap.shape[1]} pixels; aperture {int(((ap & 2) > 0).sum())} pixels; background {int(((ap & 4) > 0).sum())} pixels")
print(f"CROWDSAP {c:.5f}; FLFRCSAP {fr:.5f}; PDC method {h1.get('PDCMETHD')}; CDPP 1 h {h1.get('CDPP1_0'):.0f} ppm")
print(f"median SAP {np.median(sap):.1f} e/s; median PDCSAP {np.median(pdc):.1f} e/s; ratio {ratio:.5f}; c / f {c / fr:.5f}")
print(f"median background (summed over the aperture) {np.median(bkg):.1f} e/s = {np.median(bkg) / np.median(sap):.3f} of the star's SAP")
if abs(ratio / (c / fr) - 1) > 0.005: sys.exit("check failed: PDCSAP / SAP does not equal CROWDSAP / FLFRCSAP")
s = sap / np.median(sap)
print(f"raw SAP range over the sector outside eclipses (5th to 95th percentile of 30-min bins): ", end="")
tb, fb = LP.binned(t, s, 30)
out = fb[fb > 0.9]
print(f"{np.percentile(out, 5):.4f} to {np.percentile(out, 95):.4f}")
doc = {"tic": TIC, "sector": 46, "title": "The same sector, raw",
       "note": "The plain sum of the 20 aperture pixels minus the background (SAP), sector 46, averaged every 30 minutes, before any correction. Compare lesson 5.2's plot of the corrected light.",
       "x": "Days since the sector began", "y": "Raw brightness (1 = median)", "unit": "", "xabs": True,
       "xlab": "Days since the sector began", "read": {"x": "Day", "xu": "of the sector", "y": "raw brightness", "yu": ""}, "star": "",
       "t": [round(float(v - t[0]), 3) for v in tb], "f": [round(float(v), 4) for v in fb],
       "source": "TESS sector 46 SPOC 2-minute light of TIC 172900988 (MAST), SAP_FLUX column, quality flags removed, averaged every 30 minutes by book/tools/lesson_plots_u5c.py"}
(LP.OUT / "u5-raw-sector.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u5-raw-sector:", len(tb), "points")
