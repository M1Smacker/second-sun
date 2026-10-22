"""Build book/data/sky.json: the real sky behind the home-page constellation map.

Run once (needs the network for VizieR); the result is committed, so the book build stays offline.
  bright : Bright Star Catalogue (VizieR V/50, Hoffleit & Warren 1991), stars V < 5.6 within 30 deg of Cygnus
  names  : HR numbers of the stars we label, checked against the catalogue's own Bayer names below
  field  : positions of our 549 G1 stars (Villanova Kepler EB rev 3 galactic coordinates -> ICRS)
  plane  : the galactic plane (b = 0) as RA/Dec points, for the Milky Way band
"""
import csv, json, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "labs"))
import _env  # noqa: F401  caches go to D:, never C:

import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.vizier import Vizier

CENTER = SkyCoord(ra=20.0 * 15 * u.deg, dec=40 * u.deg)
LABEL = {"AlpCyg": "Deneb", "GamCyg": "Sadr", "EpsCyg": "Gienah", "DelCyg": "Delta Cygni", "EtaCyg": "Eta Cygni",
         "Bet1Cyg": "Albireo", "AlpLyr": "Vega", "AlpAql": "Altair"}

v = Vizier(columns=["HR", "Name", "RAJ2000", "DEJ2000", "Vmag", "SpType"], column_filters={"Vmag": "<5.6"}, row_limit=-1)
t = v.query_region(CENTER, radius=32 * u.deg, catalog="V/50/catalog")[0]
bright, named = [], {}
for r in t:
    c = SkyCoord(str(r["RAJ2000"]), str(r["DEJ2000"]), unit=(u.hourangle, u.deg))
    nm = str(r["Name"]).replace("\xa0", " ")
    key = re.sub(r"[\s\d]*(?=[A-Z])", "", nm, count=1).replace(" ", "")
    key = key if key in LABEL else None
    row = [round(c.ra.deg, 4), round(c.dec.deg, 4), float(r["Vmag"]), str(r["SpType"]).strip()[:1] or "?"]
    if key:
        named[LABEL[key]] = {"hr": int(r["HR"]), "bsc_name": nm.strip(), "i": len(bright)}
    bright.append(row)
missing = sorted(set(LABEL.values()) - set(named))
assert not missing, f"not found in the catalogue: {missing}; names seen: {[str(r['Name']) for r in t][:5]}"

g1 = {int(r["kic"]) for r in csv.DictReader(l for l in open(REPO / "targets/g1_targets.csv", encoding="utf-8") if not l.startswith("#"))}
ebfile = REPO / "data/wave-1/villanova_kepler-ebs_live/keplerebs_live.csv"
rows = [l for l in open(ebfile, encoding="utf-8") if not l.startswith("##")]
rows[0] = rows[0].lstrip("#")
glon, glat, seen = [], [], set()
for r in csv.DictReader(rows):
    k = int(r["KIC"])
    if k in g1 and k not in seen and float(r["GLat"]) > -0.5:
        seen.add(k); glon.append(float(r["GLon"])); glat.append(float(r["GLat"]))
fc = SkyCoord(l=glon * u.deg, b=glat * u.deg, frame="galactic").icrs
field = [[round(a, 3), round(b, 3)] for a, b in zip(fc.ra.deg, fc.dec.deg)]

pl = SkyCoord(l=np.arange(0, 360, 2.0) * u.deg, b=np.zeros(180) * u.deg, frame="galactic").icrs
plane = [[round(a, 3), round(b, 3)] for a, b in zip(pl.ra.deg, pl.dec.deg)]

out = {"source": {"bright": "Bright Star Catalogue 5th ed., VizieR V/50 (Hoffleit & Warren 1991)",
                  "field": "Villanova Kepler EB catalog rev 3 (2019-08-08) galactic coordinates of the G1 stars, converted with astropy",
                  "made": "2026-10-23"},
       "center": [300.0, 40.0], "named": named, "bright": bright, "field": field, "plane": plane,
       "g1_with_position": len(field), "g1_total": len(g1)}
(REPO / "book/data/sky.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
print(len(bright), "bright stars;", len(field), "of", len(g1), "G1 stars placed;", named)
