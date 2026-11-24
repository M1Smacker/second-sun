"""Unit 5 plot and numbers, lesson 5.1 Telescopes: collecting light (Claude, 24 Nov 2026).

From sector 46 of TIC 172900988 (out of eclipse, quality flags removed): electrons per 2 minutes, the photon-noise limit sqrt(N)/N, and the
measured scatter of the corrected light, after dividing out a 12-hour running median (the star's own slow changes), as it is averaged over longer times (2 minutes to 4 hours). The plot: measured scatter (ppm)
against averaging time. Checks (a failure stops): the measured 2-minute scatter is at least the photon limit (noise cannot beat
photons), and the measured 1-hour scatter is within a factor 2 of the file's own CDPP 1-hour value.
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u5a.py
"""
import glob, json, pathlib, sys
import numpy as np
from astropy.io import fits

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lesson_plots as LP

TIC, P = 172900988, 19.658173
p = glob.glob(str(LP.ROOT / "data" / "known" / "172900988" / "tess2021*-s0046-*_lc.fits"))[0]
h0, h1 = fits.getheader(p, 0), fits.getheader(p, 1)
d = fits.getdata(p, 1)
q = (d["QUALITY"] == 0) & np.isfinite(d["PDCSAP_FLUX"]) & np.isfinite(d["SAP_FLUX"])
t, f, sap = d["TIME"][q], d["PDCSAP_FLUX"][q], d["SAP_FLUX"][q]
f = f / np.median(f)
# out of eclipse: drop 0.6 d around both eclipses (primary at the folded minimum, secondary 11.879 d later)
tb, fb = LP.binned(t, f, 30); t1 = tb[np.argmin(fb)]
ph = ((t - t1) / P) % 1.0 * P
keep = (np.abs(ph) > 0.6) & (np.abs(ph - P) > 0.6) & (np.abs(ph - 11.879) > 0.6)
t, f, sap = t[keep], f[keep], sap[keep]
raw_std = float(np.std(f) * 1e6)
# remove the star's own slow changes first, as every search does (lesson 6.1): divide by a 12-hour running median
trend = np.array([np.median(f[np.abs(t - x) < 0.25]) for x in t])
f = f / trend
print(f'scatter before removing slow changes {raw_std:.0f} ppm (the star varies slowly); after: see below')
N = np.median(sap) * 120.0
photon = 1e6 / np.sqrt(N)
print(f"Tmag {h0.get('TESSMAG')}; median SAP {np.median(sap):.0f} e/s; electrons per 2 minutes {N:.3g}; photon limit {photon:.0f} ppm per 2 minutes")
mins = [2, 4, 10, 20, 30, 60, 120, 240]
meas = []
for m in mins:
    k = m // 2
    edges = np.arange(t.min(), t.max() + k * 2 / 1440, k * 2 / 1440)
    idx = np.digitize(t, edges)
    v = [f[idx == i].mean() for i in np.unique(idx) if (idx == i).sum() == k]
    meas.append(float(np.std(v) * 1e6))
for m, s in zip(mins, meas):
    print(f"  {m:4d} min: measured {s:6.0f} ppm; photon limit {photon / np.sqrt(m / 2):6.0f} ppm; ratio {s / (photon / np.sqrt(m / 2)):.2f}")
print("file CDPP 1 hour:", h1.get("CDPP1_0"))
if meas[0] < photon: sys.exit("check failed: scatter below the photon limit")
if not 0.5 < meas[mins.index(60)] / h1["CDPP1_0"] < 2: sys.exit("check failed: 1-hour scatter far from the file's CDPP")
doc = {"tic": TIC, "sector": 46, "title": "Averaging longer, the scatter shrinks",
       "note": "The spread of our star's brightness outside the eclipses, after its own slow changes are divided out, when the 2-minute measurements are averaged in longer and longer blocks.",
       "x": "Averaging time (minutes)", "y": "Scatter (ppm)", "unit": "ppm", "xabs": True,
       "xlab": "Averaging time (minutes)", "read": {"x": "Averaging", "xu": "minutes", "y": "scatter", "yu": " ppm"}, "star": "",
       "t": [float(m) for m in mins], "f": [round(s, 0) for s in meas],
       "source": "TESS sector 46 SPOC 2-minute light of TIC 172900988 (MAST), PDCSAP flux outside the eclipses, quality flags removed; book/tools/lesson_plots_u5a.py"}
(LP.OUT / "u5-scatter.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u5-scatter:", len(mins), "points")
