r"""Lab 7: is the dip on our star? Run:  .\.venv\Scripts\python.exe labs\lab7_pixels.py
Uses the TOI-1338 sector 98 pixel file (target pixel file, ~50 MB, already on D:) and the planet crossing at BTJD 4025.64."""
import _env, glob
import numpy as np, lightkurve as lk, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from astroquery.mast import Catalogs

p = glob.glob(str(_env.ROOT / "data/wave-2/lk/mastDownload/TESS/*s0098-0000000260128333-0298-s/*_tp.fits"))[0]
tpf = lk.read(p, quality_bitmask="hard")
t, flux = tpf.time.value, tpf.flux.value
print(f"Pixel file: {flux.shape[1]} x {flux.shape[2]} pixels, {len(t)} pictures, aperture of {tpf.pipeline_mask.sum()} pixels")
EV, W = 4025.64, 0.12                              # centre and half-length (days) of the crossing
inn = np.abs(t - EV) < W
out = (np.abs(t - EV) > W + 0.1) & (np.abs(t - EV) < W + 0.6)
oot = np.nanmedian(flux[out], axis=0)
diff = oot - np.nanmedian(flux[inn], axis=0)       # positive = this pixel got dimmer during the crossing
ap = tpf.pipeline_mask
print(f"Dimming summed over the aperture: {diff[ap].sum() / oot[ap].sum() * 1e6:.0f} ppm")
r0, c0 = np.unravel_index(np.nanargmax(oot), oot.shape); rd, cd = np.unravel_index(np.nanargmax(diff), diff.shape)
print(f"Brightest pixel (the star): row {r0}, col {c0}. Most-dimmed pixel: row {rd}, col {cd}")

# Centroid shift, with an honest error bar: slide the same-length window over quiet times and see how much
# the centroid moves by chance (this includes slow, red noise; dividing by sqrt(N) would not).
cr, cc = (x.value for x in tpf.estimate_centroids(aperture_mask="pipeline"))
def shift(c0_):
    i = np.abs(t - c0_) < W; o = (np.abs(t - c0_) > W + 0.1) & (np.abs(t - c0_) < W + 0.6)
    if i.sum() < 50 or o.sum() < 200: return None
    return (np.nanmedian(cr[i]) - np.nanmedian(cr[o])) * 21, (np.nanmedian(cc[i]) - np.nanmedian(cc[o])) * 21
dr, dc = shift(EV)
null = []
for x in np.arange(t.min() + 1, t.max() - 1, 0.25):     # every quarter day, away from the real crossing
    s = shift(x) if abs(x - EV) > 1 else None
    if s: null.append(s)
sr, sc = (1.4826 * np.median(np.abs(np.array(v) - np.median(v))) for v in zip(*null))
print(f"Centroid shift during the crossing: {dr:+.3f}\" in row ({dr / sr:+.1f} x the chance spread), {dc:+.3f}\" in column ({dc / sc:+.1f} x)")
print(f"Chance spread measured from {len(null)} fake windows: {sr:.3f}\" (row), {sc:.3f}\" (column)")

# Neighbours from the TESS Input Catalog, placed on the pixels with the file's sky map (WCS).
cat = Catalogs.query_object("TIC 260128333", radius=2.5 / 60, catalog="TIC")
cat = cat[cat["Tmag"] < 16]
xs, ys = tpf.wcs.world_to_pixel_values(cat["ra"], cat["dec"])
on = (xs > -0.5) & (xs < flux.shape[2] - 0.5) & (ys > -0.5) & (ys < flux.shape[1] - 0.5)
print(f"Catalogued stars brighter than Tmag 16 on these pixels: {on.sum()}")
for row in cat[on][np.argsort(cat[on]["Tmag"])][:6]:
    print(f"  TIC {row['ID']}: Tmag {row['Tmag']:.1f}, {row['dstArcSec']:.0f}\" from our star")

fig, ax = plt.subplots(1, 2, figsize=(9, 4))
for a, img, title in ((ax[0], oot, "Normal light"), (ax[1], diff, "Dimming during the crossing")):
    im = a.imshow(img, origin="lower", cmap="viridis"); a.set_title(title); plt.colorbar(im, ax=a, shrink=0.8)
    a.contour(ap, levels=[0.5], colors="w", linewidths=1)
    a.scatter(xs[on], ys[on], s=np.clip(200 - 10 * cat["Tmag"][on], 10, 120), facecolors="none", edgecolors="C3")
fig.suptitle("White outline: aperture. Red circles: catalogued stars (bigger = brighter)"); fig.tight_layout()
out_png = _env.OUT / "lab7_toi1338_pixels.png"; fig.savefig(out_png, dpi=110); print("Picture saved:", out_png)
