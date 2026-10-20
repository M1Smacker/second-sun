# EXPLORATORY follow-up (not in SPEC): is PDCSAP attenuating the known transits that SAP+HARD finds? Read-only.
import sys, json, numpy as np
sys.path.insert(0, r"D:\second-sun\experiments\quality_mask"); sys.path.insert(0, r"D:\second-sun\pipeline")
import qmask as q
from detect_v2 import load
arms = json.load(open(r"D:\second-sun\experiments\quality_mask\results\20261020T215121Z_e40982b\arms.json"))
dur = {6: 6.0, 10: 11.6, 27: 7.2, 34: 9.6, 37: 5.9, 65: 10.2, 68: 6.2}
print("A1 / A2 events matched to published times (centre offset h, box length h, depth ppm):")
for A in ("A1", "A2"):
    for s in arms[A]["sectors"]:
        h = s["hit"]
        if h: print(" ", A, "S%d" % s["sector"], "dt=%+.2f h" % ((h["center"] - q.PUB[s["sector"]]) * 24), "dur", h["dur_h"], "depth", h["depth_ppm"], "SNR", h["snr"])
print("\nLocal depth by simple line fit, same HARD cadences (published durations in h):")
print("sector  SAP_depth  PDCSAP_depth  ratio  SAP_noise  PDC_noise   (ppm; noise = scatter of 2-min residual outside transit)")
for s in (6, 10, 27, 34, 37, 65, 68, 98):
    p = q.fits_path(s); tp = q.PUB[s]
    t, pdc, _ = load(p)                                   # PDCSAP (HARD) as the baseline loads it
    ts, sap, rest, bkg = q.load_sap(p, "hard")
    keep_p = q.keep_from_T1(t, arms["T1"][str(s)]); keep_s = q.keep_from_T1(ts, arms["T1"][str(s)])
    out = []
    for tt, ff, kk in ((ts, sap, keep_s), (t, pdc, keep_p)):
        w = kk & (np.abs(tt - tp) < 1.6); x = tt[w] - tp; y = ff[w]
        side = (np.abs(x) > 0.5) & (np.abs(x) < 1.6)
        if side.sum() < 100: out += [np.nan, np.nan]; continue
        c = np.polyfit(x[side], y[side], 2); r = y - np.polyval(c, x)
        inn = np.abs(x) < 0.12
        out += [-np.median(r[inn]) * 1e6 if inn.sum() > 20 else np.nan, 1.4826 * np.median(np.abs(r[side] - np.median(r[side]))) * 1e6]
    print("S%-5d %9.0f %13.0f %7.2f %10.0f %10.0f   dur %.1f" % (s, out[0], out[2], out[0] / out[2] if out[2] else np.nan, out[1], out[3], dur.get(s, np.nan)))
