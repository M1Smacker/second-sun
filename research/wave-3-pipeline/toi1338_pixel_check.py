"""Rule C6 for the TOI-1338 S98 event: difference image + centroid shift (PRELIMINARY INTERNAL CHECK)."""
import numpy as np, lightkurve as lk, glob, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
p = glob.glob("D:/second-sun/data/wave-2/lk/**/*0298-s_tp.fits", recursive=True)[0]
tpf = lk.read(p, quality_bitmask="hard")
t = tpf.time.value; flux = tpf.flux.value
EV = (4025.52, 4025.76)
inn = (t > EV[0]) & (t < EV[1])
out = ((t > EV[0] - 0.6) & (t < EV[0] - 0.1)) | ((t > EV[1] + 0.1) & (t < EV[1] + 0.6))
diff = np.nanmedian(flux[out], axis=0) - np.nanmedian(flux[inn], axis=0)   # positive = pixel dimmed in event
oot = np.nanmedian(flux[out], axis=0)
ap = tpf.pipeline_mask
r0, c0 = np.unravel_index(np.nanargmax(oot), oot.shape)
rd, cd = np.unravel_index(np.nanargmax(diff), diff.shape)
print(f"in-event cadences {inn.sum()}, out {out.sum()}")
print(f"brightest pixel (star) at row,col = {r0},{c0}; largest dimming pixel at {rd},{cd}")
print(f"fractional dimming summed over pipeline aperture: {diff[ap].sum()/oot[ap].sum()*1e6:.0f} ppm")
# centroid shift
cr, cc = tpf.estimate_centroids(aperture_mask="pipeline")
cr, cc = cr.value, cc.value
dr = np.nanmedian(cr[inn]) - np.nanmedian(cr[out]); dc = np.nanmedian(cc[inn]) - np.nanmedian(cc[out])
sr = np.nanstd(cr[out]) / np.sqrt(inn.sum()); sc = np.nanstd(cc[out]) / np.sqrt(inn.sum())
print(f"centroid shift in event: d_row={dr*21.0:.2f}\" ({dr/sr:.1f} sigma), d_col={dc*21.0:.2f}\" ({dc/sc:.1f} sigma)  [1 px ~ 21\"]")
fig, ax = plt.subplots(1, 2, figsize=(8, 3.6))
im0 = ax[0].imshow(oot, origin="lower"); ax[0].set_title("out-of-event flux"); plt.colorbar(im0, ax=ax[0])
im1 = ax[1].imshow(diff, origin="lower", cmap="RdBu_r"); ax[1].set_title("difference (out - in): dimmed pixels"); plt.colorbar(im1, ax=ax[1])
for a in ax:
    a.contour(ap, levels=[0.5], colors="k", linewidths=0.8)
fig.suptitle("TOI-1338 S98 event: pixel check (black outline = SPOC aperture)", fontsize=9)
fig.tight_layout(); fig.savefig("D:/second-sun/research/wave-3-pipeline/toi1338_pixel_check.png", dpi=110)
print("saved png")
