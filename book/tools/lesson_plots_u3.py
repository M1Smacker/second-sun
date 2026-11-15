"""Unit 3 plots (non-time data). Lesson 3.1: the TESS response curve, v2.0 (Vanderspek, TESS POC; downloaded 15 Nov 2026, research/downloads.csv)."""
import json, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "book" / "docs" / "assets" / "data" / "lessons"
d = np.genfromtxt(ROOT / "data" / "learn-sources" / "tess-response" / "tess-response-function-v2.0.csv", delimiter=",", comments="#")
w, r = d[:, 0], d[:, 1]
m = (w >= 450) & (w <= 1150) & (w % 4 == 0)
doc = {"tic": None, "sector": None, "title": "What TESS's camera counts, colour by colour",
       "note": "For each wavelength, the share of the arriving light the camera records. Zero means TESS is blind there.",
       "x": "Wavelength (nanometres)", "y": "Share of light recorded", "unit": "share", "xabs": True,
       "xlab": "Wavelength (nanometres)", "read": {"x": "Wavelength", "xu": "nm", "y": "share recorded", "yu": ""}, "star": "",
       "t": [float(v) for v in w[m]], "f": [round(float(v), 3) for v in r[m]],
       "source": "TESS instrument response function v2.0 (R. Vanderspek, TESS Payload Operations Center, MIT), 2020; NASA TESS Science Support Center"}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "u3-tess-response.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
print("u3-tess-response:", m.sum(), "points; peak", w[r.argmax()], r.max())
