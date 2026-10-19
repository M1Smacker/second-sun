"""Vet the TOI-1338 S98 event near BTJD 4025.6 against wave-4 rules C2, C5, C7, C8 (+ SAP/PDCSAP).
PRELIMINARY INTERNAL CHECK. Writes toi1338_event_check.png for visual inspection.
"""
import numpy as np, lightkurve as lk, pathlib, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from wotan import flatten
from lightkurve.utils import TessQualityFlags as Q

DL = pathlib.Path(r"D:\second-sun\data\wave-3\lk"); OUT = pathlib.Path(r"D:\second-sun\research\wave-3-pipeline")
EV = (4025.50, 4025.78)           # event window (BTJD)
P, T1, D1 = 14.6084, 3937.1450, 4.7 / 24
T2, D2 = 3943.7750, 6.1 / 24

raw = lk.search_lightcurve("TIC 260128333", author="SPOC", exptime=120, sector=98)[0].download(download_dir=str(DL), quality_bitmask="none")
t = raw.time.value; q = raw.quality.value
near = (t > 4024.6) & (t < 4026.6)
flags = {}
for b in np.unique(q[near]):
    if b: flags[int(b)] = (Q.decode(int(b)), int(np.sum(q[near] == b)))
print("quality flags in BTJD 4024.6-4026.6:", flags)
dumps = t[(q & 32) > 0]
print("momentum dumps (bit 32) in S98 at BTJD:", np.round(np.unique(np.round(dumps, 2)), 2))
print("nearest dump to event:", np.round(dumps[np.argmin(np.abs(dumps - 4025.6))], 3) if len(dumps) else None)
print("nearest primary eclipse:", round(T1 + P * round((4025.6 - T1) / P), 3), "| nearest secondary:", round(T2 + P * round((4025.6 - T2) / P), 3))

def ecl_mask(t):
    p1 = ((t - T1 + 0.5 * P) % P) - 0.5 * P; p2 = ((t - T2 + 0.5 * P) % P) - 0.5 * P
    return (np.abs(p1) < 1.5 * D1) | (np.abs(p2) < 1.5 * D2)

def depth_in_window(tt, ff, win):
    m = (tt > EV[0]) & (tt < EV[1]); o = (tt > EV[0] - 1.0) & (tt < EV[1] + 1.0) & ~m
    return (np.nanmedian(ff[o]) - np.nanmedian(ff[m])) * 1e6, np.nanstd(ff[o]) * 1e6

# C2: detrending robustness (21 biweight windows 1.0-3.0 d, like Davies) on HARD-masked PDCSAP
lc = raw.copy(); lc = lc[(lc.quality.value & Q.HARD_BITMASK) == 0].remove_nans().normalize()
tt, ff = lc.time.value, lc.flux.value; k = ~ecl_mask(tt); tt, ff = tt[k], ff[k]
hits = 0; depths = []
for w in np.linspace(1.0, 3.0, 21):
    fl = flatten(tt, ff, method="biweight", window_length=w)
    d, s = depth_in_window(tt, fl, EV); depths.append(d)
    hits += d > 3 * s / np.sqrt(max(1, np.sum((tt > EV[0]) & (tt < EV[1])) / 15))
print(f"C2 detrending robustness: depth>3sigma in {hits}/21 windows; depths ppm min/med/max = {min(depths):.0f}/{np.median(depths):.0f}/{max(depths):.0f}")

# SAP vs PDCSAP
sap = raw.copy(); sap.flux = sap.sap_flux; sap.flux_err = sap.sap_flux_err
sap = sap[(sap.quality.value & Q.HARD_BITMASK) == 0].remove_nans().normalize()
ts, fs = sap.time.value, sap.flux.value; k = ~ecl_mask(ts)
fls = flatten(ts[k], fs[k], method="biweight", window_length=1.5)
print("SAP depth in window (ppm): %.0f (scatter %.0f)" % depth_in_window(ts[k], fls, EV))

# C8: independent products
prods = {}
for label, kw in [("SPOC 20-s", dict(author="SPOC", exptime=20)), ("QLP", dict(author="QLP")), ("TESS-SPOC", dict(author="TESS-SPOC"))]:
    try:
        sr = lk.search_lightcurve("TIC 260128333", sector=98, **kw)
        if len(sr) == 0: prods[label] = "not available"; continue
        x = sr[0].download(download_dir=str(DL), quality_bitmask="hard").remove_nans().normalize()
        if label == "SPOC 20-s": x = x.bin(time_bin_size=2 / 1440)
        a, b = x.time.value, x.flux.value; k = ~ecl_mask(a)
        fl = flatten(a[k], b[k], method="biweight", window_length=1.5)
        prods[label] = "depth %.0f ppm (scatter %.0f)" % depth_in_window(a[k], fl, EV)
        prods[label + "_series"] = (a[k], fl)
    except Exception as e:
        prods[label] = f"ERROR {type(e).__name__}: {str(e)[:100]}"
for kx, v in prods.items():
    if not kx.endswith("_series"): print(f"C8 {kx}: {v}")

# picture
fig, ax = plt.subplots(4, 1, figsize=(7, 11), sharex=True)
fl = flatten(tt, ff, method="biweight", window_length=1.5)
for a_, (lab, ser) in zip(ax, [("SPOC 2-min PDCSAP (hard mask, eclipses masked)", (tt, fl)), ("SPOC 2-min SAP", (ts[~ecl_mask(ts)], fls))]
                         + [(l, prods[l + "_series"]) for l in ("QLP", "TESS-SPOC") if l + "_series" in prods][:2]):
    x, y = ser; m = (x > 4023.5) & (x < 4027.5)
    a_.plot(x[m], y[m], ".", ms=1.5, color="0.6")
    xb = np.arange(4023.5, 4027.5, 1 / 48); yb = [np.nanmean(y[m][(x[m] >= u) & (x[m] < u + 1 / 48)]) for u in xb]
    a_.plot(xb + 1 / 96, yb, "-", color="C0", lw=1.2)
    a_.axvspan(*EV, color="C3", alpha=0.15); a_.set_title(lab, fontsize=9); a_.set_ylim(0.996, 1.003)
    for d in dumps[(dumps > 4023.5) & (dumps < 4027.5)]: a_.axvline(d, color="k", ls=":", lw=0.8)
    pe = T1 + P * round((4025.6 - T1) / P); a_.axvspan(pe - 1.5 * D1, pe + 1.5 * D1, color="C2", alpha=0.15)
ax[-1].set_xlabel("BTJD"); fig.suptitle("TOI-1338 S98: event check (red = event, green = masked primary eclipse, dotted = momentum dumps)", fontsize=8)
fig.tight_layout(); fig.savefig(OUT / "toi1338_event_check.png", dpi=110)
print("saved png")
