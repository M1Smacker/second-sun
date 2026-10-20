"""The wave-3 single-event search (toi1338_s97_98.py), unchanged, wrapped as a function so burn-1 can reuse it.

Method (after Davies+ 2026, arXiv:2604.09435): BLS the binary's eclipses, mask +-1.5 durations,
wotan biweight 1-d window, 30-min bins, event = >=3 consecutive bins below 3 x MAD.
"""
import numpy as np
from astropy.timeseries import BoxLeastSquares
from wotan import flatten


def bls_eclipse(t, f, pmin=14.5, pmax=14.7):
    m = BoxLeastSquares(t, f).power(np.linspace(pmin, pmax, 4000), [0.15, 0.2, 0.25, 0.3, 0.4])
    i = np.argmax(m.power)
    return m.period[i], m.transit_time[i], m.duration[i], m.depth[i]


def eclipse_mask(t, f):
    """Return (keep mask, info dict) with both eclipses masked +-1.5 durations."""
    P, T1, D1, d1 = bls_eclipse(t, f)
    ph = ((t - T1 + 0.5 * P) % P) - 0.5 * P
    m1 = np.abs(ph) < 1.5 * D1
    P2, T2, D2, d2 = bls_eclipse(t[~m1], f[~m1], P - 0.001, P + 0.001)
    ph2 = ((t - T2 + 0.5 * P) % P) - 0.5 * P
    keep = ~(m1 | (np.abs(ph2) < 1.5 * D2))
    return keep, dict(P=P, T1=T1, D1=D1, d1=d1, T2=T2, D2=D2, d2=d2)


def find_events(tt, ff, window=1.0):
    """Detrend + bin + flag. tt, ff = out-of-eclipse time and flux. Returns (events, mad, bt, bf)."""
    flat = flatten(tt, ff, method="biweight", window_length=window)
    ok = np.isfinite(flat)
    tt, flat = tt[ok], flat[ok]
    edges = np.arange(tt.min(), tt.max() + 1 / 48, 1 / 48)
    idx = np.digitize(tt, edges)
    u = [k for k in np.unique(idx) if np.sum(idx == k) >= 5]
    bt = np.array([tt[idx == k].mean() for k in u])
    bf = np.array([flat[idx == k].mean() for k in u])
    med = np.median(bf); mad = 1.4826 * np.median(np.abs(bf - med))
    low = bf < med - 3 * mad
    events, k = [], 0
    while k < len(low):
        if low[k]:
            j = k
            while j + 1 < len(low) and low[j + 1] and bt[j + 1] - bt[j] < 0.03:
                j += 1
            if j - k + 1 >= 3:
                seg = slice(k, j + 1)
                depth = med - bf[seg].mean()
                events.append(dict(t0=bt[k], t1=bt[j],                                    center=0.5 * (bt[k] + bt[j]), dur_h=(bt[j] - bt[k]) * 24 + 0.5,
                                   depth_ppm=depth * 1e6, snr=depth / mad * np.sqrt(j - k + 1)))
            k = j + 1
        else:
            k += 1
    return events, mad, bt, bf


def search(t, f):
    keep, info = eclipse_mask(t, f)
    events, mad, bt, bf = find_events(t[keep], f[keep])
    return events, mad, info
