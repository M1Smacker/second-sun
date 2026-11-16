"""Unit 3 plots, lessons 3.2 and 3.3 (Claude, 17 Nov 2026).

3.2: two glow curves from Planck's law (the Sun 5,772 K, a red dwarf 3,300 K), computed here from the exact SI constants. The script checks
     that the peak of each curve sits where Wien's law says (the checks print; a mismatch stops the build of the plot).
3.3: one real star's spectrum, SDSS DR17 plate 2938, MJD 54526, fibre 518 (an A0 star, redshift 2.6e-6, i.e. no measurable motion),
     downloaded 17 Nov 2026 (research/downloads.csv). The script checks that the dark lines sit where the Balmer formula puts them.
Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots_u3b.py
"""
import json, pathlib, sys
import numpy as np
from astropy.io import fits

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "book" / "docs" / "assets" / "data" / "lessons"
OUT.mkdir(parents=True, exist_ok=True)

# ---- 3.2: Planck glow curves -------------------------------------------------------------
h, c, k = 6.62607015e-34, 299792458.0, 1.380649e-23          # exact SI values
B_WIEN = 2.897771955e6                                       # nm K (CODATA 2018 Wien constant, 2.897771955e-3 m K)


def planck(lam_nm, T):
    lam = lam_nm * 1e-9
    return (2 * h * c ** 2 / lam ** 5) / np.expm1(h * c / (lam * k * T))


def glow(name, T, title, note, lo=200, hi=2500, step=10):
    lam = np.arange(lo, hi + 1, step, dtype=float)
    fine = np.arange(lo, hi + 0.01, 0.1)
    peak_fine = fine[np.argmax(planck(fine, T))]
    wien = B_WIEN / T
    if abs(peak_fine - wien) > 0.5:                           # the check that could contradict the lesson
        sys.exit(f"{name}: numeric peak {peak_fine:.1f} nm differs from Wien {wien:.1f} nm")
    y = planck(lam, T)
    y = y / y.max()
    doc = {"tic": None, "sector": None, "title": title, "note": note,
           "x": "Wavelength (nanometres)", "y": "Glow at each colour (1 = the brightest)", "unit": "share", "xabs": True,
           "xlab": "Wavelength (nanometres)", "read": {"x": "Wavelength", "xu": "nm", "y": "glow", "yu": ""}, "star": "",
           "t": [float(v) for v in lam], "f": [round(float(v), 4) for v in y],
           "source": f"Planck's law at {T:,} K, computed with the exact SI constants h, c and k (our own script, book/tools/lesson_plots_u3b.py)"}
    (OUT / f"{name}.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
    print(f"{name}: T={T} K  numeric peak {peak_fine:.1f} nm  Wien {wien:.1f} nm  OK")


glow("u3-glow-reddwarf", 3300, "The glow of a red dwarf, colour by colour",
     "A star at 3,300 K, drawn from Planck's law. The height is how much light it sends out at each wavelength, scaled so the brightest colour is 1.")
glow("u3-glow-sun", 5772, "The glow of the Sun, colour by colour",
     "A star at 5,772 K, the Sun's surface temperature, drawn from Planck's law and scaled the same way.")

# ---- 3.3: a real spectrum ----------------------------------------------------------------
SRC = ROOT / "data" / "learn-sources" / "sdss-a0-spectrum" / "spec-2938-54526-0518.fits"
f = fits.open(SRC)
d, sp = f[1].data, f[2].data
if sp["SUBCLASS"][0].strip() != "A0" or sp["ZWARNING"][0] != 0:
    sys.exit("unexpected spectrum class")
lam = 10 ** d["loglam"] / 10.0                                # angstrom to nm (SDSS wavelengths are in vacuum)
fl, ok = d["flux"].astype(float), (d["and_mask"] == 0) & (d["ivar"] > 0)
z = float(sp["Z"][0])
R_H = 1.0967758e7                                             # Rydberg constant for hydrogen, per metre
print("redshift", z, "-> speed", round(z * 299792.458, 2), "km/s")
for n in range(3, 10):
    pred = 1e9 / (R_H * (0.25 - 1 / n ** 2))
    m = ok & (lam > pred - 3) & (lam < pred + 3)
    s = np.convolve(fl[m], np.ones(5) / 5, mode="same")
    obs = lam[m][3:-3][s[3:-3].argmin()]
    print(f"  n={n}: formula {pred:7.2f} nm   darkest point in the file {obs:7.2f} nm   gap {obs - pred:+.2f} nm")
    if abs(obs - pred) > 0.3:
        sys.exit("a Balmer line is not where the formula puts it")
sel = ok & (lam >= 380) & (lam <= 700)
x, y = lam[sel], fl[sel]
y = y / np.max(y)
doc = {"tic": None, "sector": None, "title": "One real star, split into its colours",
       "note": "The light of an A0 star spread out by wavelength. Height is brightness, scaled so the brightest colour is 1. The narrow dark gaps are lines.",
       "x": "Wavelength (nanometres)", "y": "Brightness (1 = the brightest colour)", "unit": "share", "xabs": True,
       "xlab": "Wavelength (nanometres)", "read": {"x": "Wavelength", "xu": "nm", "y": "brightness", "yu": ""}, "star": "",
       "t": [round(float(v), 2) for v in x], "f": [round(float(v), 3) for v in y],
       "source": "Sloan Digital Sky Survey DR17, spectrum of an A0 star (plate 2938, MJD 54526, fibre 518), SDSS Collaboration; vacuum wavelengths"}
(OUT / "u3-a0-spectrum.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u3-a0-spectrum:", sel.sum(), "points", round(float(x.min()), 1), "to", round(float(x.max()), 1), "nm")
