"""S6 of the sealed benchmark: which transits of the known circumbinary planet TOI-1338 b (TIC 260128333, a sealed star) should fall in the downloaded TESS sectors, from a PUBLISHED prediction and
FITS HEADER METADATA ONLY (TSTART and TSTOP of each file; no flux is read). Written BEFORE the sealed search, so the expectation cannot be shaped by what the search finds.
Source (CONFIRMED, read 30 Oct 2026): Kostov et al. 2020, "TOI-1338: TESS' First Transiting Circumbinary Planet", AJ 159, 253, arXiv:2004.07783, Table 6 "Times, durations, and impact parameters of
future planet transits" (photodynamical model; BJD - 2,455,000; 1-sigma uncertainty; duration; the share of model runs in which the transit happens). The prediction was made in 2020 from the first
12 TESS sectors plus radial velocities, so the later the epoch the less certain it is (sigma up to 1 d, transit share down to 20%): a late epoch is a weak test, an early one a strong test.
Usage: python toi1338b_expected.py   (writes research\\stage3\\toi1338b-expected.json)"""
import json, glob, pathlib
from astropy.io import fits

TIC = 260128333
T = [3861.1845, 3954.1353, 4049.6930, 4142.3991, 4237.9220, 4330.9984, 4425.7194, 4519.6951, 4708.3278, 4801.0174, 4896.7585, 4989.3540, 5084.8165, 5177.9790, 5272.3566, 5366.6770, 5459.7304,
     5555.2836, 5647.6474, 5743.6224, 5836.0445, 5931.4246, 6024.6162, 6118.5043, 6213.1325, 6305.7169, 6401.3824, 6493.7147, 6589.0498, 6682.0668, 6775.8467, 6870.3964, 6962.8655, 7058.3711,
     7150.8050, 7245.5142, 7339.0599, 7431.8295, 7527.1701]
S = [0.0161, 0.0214, 0.0196, 0.0224, 0.0236, 0.0264, 0.0319, 0.0328, 0.0389, 0.0461, 0.0461, 0.0509, 0.0693, 0.0600, 0.1296, 0.0742, 0.1788, 0.0967, 0.1677, 0.1383, 0.1543, 0.2222, 0.1615, 0.3348,
     0.1991, 0.3200, 0.2847, 0.2750, 0.4693, 0.2875, 0.7051, 0.3605, 0.5975, 0.5322, 0.4580, 0.8968, 0.4556, 1.0387, 0.5751]
D = [6.74, 9.80, 7.91, 7.46, 9.73, 6.31, 11.78, 5.94, 6.06, 8.44, 6.78, 6.04, 8.19, 4.93, 9.79, 4.79, 8.76, 5.26, 6.27, 6.35, 4.93, 8.39, 4.71, 9.86, 5.22, 7.40, 6.52, 5.53, 8.97, 5.11, 10.95, 5.65,
     7.74, 7.42, 5.64, 10.53, 5.33, 10.20, 6.19]
F = [100.0, 100.0, 100.0, 100.0, 99.9, 99.9, 99.6, 98.7, 92.9, 95.5, 82.4, 85.2, 72.6, 70.0, 64.5, 54.2, 55.7, 42.9, 44.5, 35.5, 34.2, 31.0, 27.7, 27.4, 23.9, 23.8, 22.4, 20.7, 21.5, 19.6, 20.4,
     20.7, 19.6, 23.1, 21.1, 26.0, 25.6, 27.5, 36.4]
assert len(T) == len(S) == len(D) == len(F) == 39, (len(T), len(S), len(D), len(F))

rng = {}
for f in glob.glob(rf"D:\second-sun\data\g2\{TIC}\*.fits"):
    for hdu in (1, 0):
        h = fits.getheader(f, hdu)
        if "TSTART" in h and "TSTOP" in h:
            sec = fits.getheader(f, 0).get("SECTOR"); lo, hi = rng.get(sec, (1e9, -1e9))
            rng[sec] = (min(lo, h["TSTART"]), max(hi, h["TSTOP"])); break
epochs = [dict(btjd=round(t - 2000, 4), sigma_d=s, dur_h=d, p_transit_pct=p, sector=sec) for t, s, d, p in zip(T, S, D, F) for sec, (lo, hi) in rng.items() if lo - 3 * s <= t - 2000 <= hi + 3 * s]
out = dict(source="Kostov et al. 2020, AJ 159, 253 (arXiv:2004.07783), Table 6, BJD-2455000 converted to BTJD (BJD-2457000) by subtracting 2000", tic=TIC, sectors_downloaded={str(k): [round(v[0], 2), round(v[1], 2)] for k, v in sorted(rng.items())},
           epochs=epochs, rule="S6 window per epoch: |event centre - predicted| < 3 x sigma + 0.1 d; epochs with a transit share under 50% are 'weak tests'")
pathlib.Path(r"D:\second-sun\research\stage3\toi1338b-expected.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
strong = [e for e in epochs if e["p_transit_pct"] >= 50]
print(f"sectors downloaded: {len(rng)}; predicted transits inside them: {len(epochs)} ({len(strong)} with a model transit share of 50% or more)")
for e in epochs:
    print(f"  BTJD {e['btjd']:.2f} +- {e['sigma_d']:.2f} d, {e['dur_h']:.1f} h, transit share {e['p_transit_pct']:.0f}%, sector {e['sector']}")
