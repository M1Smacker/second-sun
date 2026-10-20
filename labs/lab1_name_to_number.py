r"""Lab 1: from a star's name to its numbers. Run:  .\.venv\Scripts\python.exe labs\lab1_name_to_number.py "Kepler-16" """
import _env, sys
from astroquery.mast import Catalogs
import lightkurve as lk

name = sys.argv[1] if len(sys.argv) > 1 else "Kepler-16"
# 1. Ask the TESS Input Catalog (TIC) for every star within 2 arcminutes of that name's position.
near = Catalogs.query_object(name, radius=2 / 60, catalog="TIC")
near.sort("dstArcSec")
star = near[0]                                   # the closest one is our star
print(f"{name}  ->  TIC {star['ID']}   (KIC {star['KIC']}, Gaia DR3 {star['GAIA']})")
print(f"  position: RA {star['ra']:.5f} deg, Dec {star['dec']:.5f} deg")
print(f"  brightness: TESS magnitude {star['Tmag']:.2f} (smaller = brighter)")
print(f"  star: {star['Teff']:.0f} K, radius {star['rad']:.2f} Sun, distance {star['d']:.0f} parsecs")
# 2. Neighbours: TESS pixels are 21 arcseconds wide, so anything within ~1 arcminute can leak into our light.
close = near[(near["dstArcSec"] > 0) & (near["dstArcSec"] < 60)]
bright = close[close["Tmag"] < star["Tmag"] + 5]
print(f"  neighbours within 1 arcminute: {len(close)}, of which {len(bright)} are less than 5 magnitudes fainter")
# 3. Which ready-made light curves exist?
res = lk.search_lightcurve(f"TIC {star['ID']}")
print(f"\nReady-made light curves: {len(res)}")
for author in sorted(set(res.author)):
    rows = res[res.author == author]
    sectors = sorted({int(m.split()[-1]) for m in rows.mission})
    print(f"  {author:10s} {len(rows):3d} files, sectors {sectors}")
