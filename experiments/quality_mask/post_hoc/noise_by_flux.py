# EXPLORATORY follow-up 2 (not in SPEC): why does A0 (PDCSAP) miss transits that A1 (SAP) finds on the same cadences? Read-only.
import sys, json, numpy as np
sys.path.insert(0, r"D:\second-sun\experiments\quality_mask"); sys.path.insert(0, r"D:\second-sun\pipeline")
import qmask as q
from detect_v2 import load, detrend, bin10, box_scores
arms = json.load(open(r"D:\second-sun\experiments\quality_mask\results\20261020T215121Z_e40982b\arms.json"))
def at(t, f, tp, dur):
    tt, ff = detrend(t, f, 2.0); bt, bf = bin10(tt, ff)
    c, snr, m = box_scores(bt, bf, dur); g = np.isfinite(m)
    sig = 1.4826 * np.nanmedian(np.abs(m[g] - np.nanmedian(m[g]))); i = np.nanargmin(np.abs(c - tp) + np.where(g, 0, 9))
    med = np.nanmedian(bf)
    return sig * 1e6, (med - m[i]) * 1e6, snr[i], np.nanstd(bf[np.isfinite(bf)]) * 1e6
print("sector dur | PDCSAP: sigma_D  depth  SNR  | SAP: sigma_D  depth  SNR   (ppm; box of the published duration, centred on the published time)")
for s, dur in ((6, 6.5), (10, 10), (27, 6.5), (34, 8), (37, 5), (65, 10), (68, 6.5), (98, 5)):
    p = q.fits_path(s); tp = q.PUB[s]; T1 = arms["T1"][str(s)]
    t, f, _ = load(p); k = q.keep_from_T1(t, T1); a = at(t[k], f[k], tp, dur)
    ts, fs, rest, _ = q.load_sap(p, "hard"); ks = q.keep_from_T1(ts, T1); b = at(ts[ks], fs[ks], tp, dur)
    print(f"S{s:<4d} {dur:4.1f} | {a[0]:8.0f} {a[1]:6.0f} {a[2]:5.1f} | {b[0]:8.0f} {b[1]:6.0f} {b[2]:5.1f}   n kept {k.sum()} / {ks.sum()}")
