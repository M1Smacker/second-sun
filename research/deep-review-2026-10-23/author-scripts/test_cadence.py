"""Does detect_v2.find_events work on 30-min (S14-26 FFI) and 10-min cadence? Stub out lightkurve (only used by load())."""
import sys, types, numpy as np
sys.modules['lightkurve'] = types.ModuleType('lightkurve')
sys.path.insert(0, '/home/claude/second-sun/pipeline')
import detect_v2 as d
rng = np.random.default_rng(1)
for cad_min in (2, 200/60, 10, 30):
    t = np.arange(0, 27, cad_min/1440)
    sig = 1000e-6*np.sqrt(2/cad_min)          # same noise per unit time as the 2-min self-check
    f = 1 + rng.normal(0, sig, t.size)
    f[np.abs(t-13.3) < 4/24] -= 1500e-6       # 8-h, 1500 ppm box: expected SNR ~ 1500/(1000/sqrt(4*60)) ~ 23
    ev = d.find_events(t, f)
    bt, bf = d.bin10(*d.detrend(t, f))
    print(f"cadence {cad_min:5.2f} min: finite 10-min bins {np.isfinite(bf).mean():.2f}; events: {[(round(e['center'],2), e['dur_h'], round(e['snr'],1)) for e in ev[:2]]}")
