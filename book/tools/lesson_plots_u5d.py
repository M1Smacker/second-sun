"""Unit 5 plot and numbers, lesson 5.4 What goes wrong (Claude, 24 Nov 2026).

Sector 46 of TIC 172900988: the sky background in the aperture (SAP_BKG), binned to 30 minutes, showing scattered-light surges.
Prints the quality flags set in the file, by bit, with lightkurve's own descriptions (TessQualityFlags), and the momentum-dump days.
Checks (a failure stops): the flagged share is between 5% and 30%; the Earth-point cadences carry no flux; the background's highest
30-minute value falls inside or next to (within 1 day of) a stretch flagged for scattered light.
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u5d.py
"""
import glob, json, pathlib, sys
import numpy as np
from astropy.io import fits
from lightkurve.utils import TessQualityFlags as Q

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lesson_plots as LP

TIC = 172900988
p = glob.glob(str(LP.ROOT / "data" / "known" / "172900988" / "tess2021*-s0046-*_lc.fits"))[0]
d = fits.getdata(p, 1)
q, t, b, s = d["QUALITY"], d["TIME"], d["SAP_BKG"], d["SAP_FLUX"]
t0 = np.nanmin(t)
share = (q > 0).mean()
print(f"cadences {len(q)}; flagged {int((q > 0).sum())} ({share:.3f})")
for bit in range(20):
    v = 1 << bit; k = int(((q & v) > 0).sum())
    if k: print(f"  value {v}: {k} cadences ({k * 2 / 60:.1f} h) | {Q.STRINGS.get(v, '?')}")
earth = (q & 8) > 0
print("Earth-point cadences with flux:", int(np.isfinite(s[earth]).sum()), "of", int(earth.sum()))
print("momentum-dump days:", sorted(set(np.round(t[(q & 32) > 0] - t0, 1))))
if not 0.05 < share < 0.30: sys.exit("flag share check failed")
if np.isfinite(s[earth]).any(): sys.exit("Earth-point flux check failed")
ok = np.isfinite(t) & np.isfinite(b)
tb, bb = LP.binned(t[ok], b[ok], 30)
peak = tb[int(np.argmax(bb))]
stray = t[((q & 4096) > 0) & np.isfinite(t)]
gap = np.min(np.abs(stray - peak))
print(f"background: median {np.median(bb):.0f} e/s, highest {bb.max():.0f} at day {peak - t0:.2f}; nearest scattered-light flag {gap:.2f} d away")
if gap > 1.0: sys.exit("check failed: the background peak is not near a scattered-light flag")
doc = {"tic": TIC, "sector": 46, "title": "The sky behind our star, sector 46",
       "note": "The background light in the star's 20 aperture pixels, averaged every 30 minutes. Most of the time it is steady; the surges are scattered light from Earth and the Moon.",
       "x": "Days since the sector began", "y": "Background (electrons per second)", "unit": "", "xabs": True,
       "xlab": "Days since the sector began", "read": {"x": "Day", "xu": "of the sector", "y": "background", "yu": " e/s"}, "star": "",
       "t": [round(float(v - t0), 3) for v in tb], "f": [round(float(v), 1) for v in bb],
       "source": "TESS sector 46 SPOC 2-minute light of TIC 172900988 (MAST), SAP_BKG column, averaged every 30 minutes by book/tools/lesson_plots_u5d.py; flag names from lightkurve 2.6 TessQualityFlags"}
(LP.OUT / "u5-background.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u5-background:", len(tb), "points")
