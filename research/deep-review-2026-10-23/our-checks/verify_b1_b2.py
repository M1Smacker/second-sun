"""Independent re-check of the research review's B1 (30-min cadence) and B2 (QLP column before S56)."""
import sys, glob
import numpy as np
sys.path.insert(0, r"D:\second-sun\pipeline")
import detect_v2 as d
import lightkurve as lk

print("== B1: same 8 h, 1500 ppm dip at four cadences (noise per unit time held fixed) ==")
rng = np.random.default_rng(1)
for cad in (2, 200 / 60, 10, 30):
    t = np.arange(0, 27, cad / 1440)
    f = 1 + rng.normal(0, 1000e-6 * np.sqrt(2 / cad), t.size)
    f[np.abs(t - 13.3) < 4 / 24] -= 1500e-6
    ev = d.find_events(t, f)
    bt, bf = d.bin10(*d.detrend(t, f))
    print(f"  {cad:5.2f} min: finite 10-min bins {np.isfinite(bf).mean():.2f}; top event "
          f"{(round(ev[0]['center'],2), ev[0]['dur_h'], round(ev[0]['snr'],1)) if ev else 'NONE'}")

print("== B2: which flux column does load() pick for real QLP files? ==")
for p in sorted(glob.glob(r"D:\second-sun\data\**\hlsp_qlp*.fits", recursive=True)):
    lc = lk.read(p, quality_bitmask="hard")
    cols = sorted(c for c in lc.colnames if "flux" in c.lower())
    chosen = next((c for c in ("sys_rm_flux", "det_flux", "kspsap_flux") if c in {x.lower() for x in lc.colnames}), "flux")
    sec = lc.meta.get("SECTOR")
    cad = np.nanmedian(np.diff(lc.time.value)) * 1440
    print(f"  S{sec} ({cad:.1f} min): flux columns {cols} -> load() uses '{chosen}'")
