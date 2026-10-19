"""Wave 3 practice target: did TESS catch a TOI-1338 b transit in Sectors 97-98 (Sep 2025 - Jan 2026)?

PRELIMINARY INTERNAL CHECK, NOT A DISCOVERY CLAIM.
Method (after Davies+ 2026, arXiv:2604.09435): find the binary's eclipses in the data with BLS, mask them,
detrend (wotan biweight, 1-d window), bin to 30 min, flag single events = >=3 consecutive bins below 3 x MAD.
Expected planet transit depth ~0.2% (6.85 R_E across a ~1.3 R_sun primary; Kostov+ 2020).
"""
import numpy as np, lightkurve as lk, pathlib
from astropy.timeseries import BoxLeastSquares
from wotan import flatten

DL = pathlib.Path(r"D:\second-sun\data\wave-3\lk")
lcs = []
for s in (97, 98):
    sr = lk.search_lightcurve("TIC 260128333", author="SPOC", exptime=120, sector=s)
    lc = sr[0].download(download_dir=str(DL), quality_bitmask="hard").remove_nans().normalize()
    lcs.append(lc)
    print(f"S{s}: {len(lc)} cadences, BTJD {lc.time.value.min():.2f}-{lc.time.value.max():.2f}")
lc = lk.LightCurveCollection(lcs).stitch().remove_nans()
t, f = lc.time.value, lc.flux.value

def bls_eclipse(t, f, pmin=14.5, pmax=14.7):
    m = BoxLeastSquares(t, f).power(np.linspace(pmin, pmax, 4000), [0.15, 0.2, 0.25, 0.3, 0.4])
    i = np.argmax(m.power)
    return m.period[i], m.transit_time[i], m.duration[i], m.depth[i]

P, T1, D1, d1 = bls_eclipse(t, f)
print(f"primary eclipse: P={P:.4f} d, T0={T1:.4f}, dur={D1*24:.1f} h, depth={d1*100:.2f}%")
ph = ((t - T1 + 0.5 * P) % P) - 0.5 * P
m1 = np.abs(ph) < 1.5 * D1
P2, T2, D2, d2 = bls_eclipse(t[~m1], f[~m1], P - 0.001, P + 0.001)
print(f"secondary eclipse: T={T2:.4f} (phase {((T2 - T1) / P) % 1:.3f}), dur={D2*24:.1f} h, depth={d2*100:.3f}%")
ph2 = ((t - T2 + 0.5 * P) % P) - 0.5 * P
keep = ~(m1 | (np.abs(ph2) < 1.5 * D2))

tt, ff = t[keep], f[keep]
flat = flatten(tt, ff, method="biweight", window_length=1.0)
ok = np.isfinite(flat)
tt, flat = tt[ok], flat[ok]
# 30-min bins
edges = np.arange(tt.min(), tt.max() + 1 / 48, 1 / 48)
idx = np.digitize(tt, edges)
bt = np.array([tt[idx == k].mean() for k in np.unique(idx) if np.sum(idx == k) >= 5])
bf = np.array([flat[idx == k].mean() for k in np.unique(idx) if np.sum(idx == k) >= 5])
med = np.median(bf); mad = 1.4826 * np.median(np.abs(bf - med))
low = bf < med - 3 * mad
print(f"30-min binned scatter (1.4826*MAD) = {mad*1e6:.0f} ppm; expected planet depth ~2200 ppm")

events, k = [], 0
while k < len(low):
    if low[k]:
        j = k
        while j + 1 < len(low) and low[j + 1] and bt[j + 1] - bt[j] < 0.03:
            j += 1
        if j - k + 1 >= 3:
            seg = slice(k, j + 1)
            depth = med - bf[seg].mean()
            snr = depth / mad * np.sqrt(j - k + 1)
            events.append((bt[k], bt[j], (bt[j] - bt[k]) * 24 + 0.5, depth * 1e6, snr))
        k = j + 1
    else:
        k += 1
print(f"\nsingle events (>=3 consecutive 30-min bins < 3 MAD): {len(events)}")
for e in events:
    print(f"  BTJD {e[0]:.3f}-{e[1]:.3f}  dur~{e[2]:.1f} h  depth~{e[3]:.0f} ppm  SNR~{e[4]:.1f}")
