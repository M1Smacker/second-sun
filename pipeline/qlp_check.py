"""Does detector v2 find the S98 TOI-1338 b transit in QLP (an independent product, rule C8)?"""
from detect_v2 import load, eclipse_mask, find_events
Q = r"D:\second-sun\data\wave-3\lk\mastDownload\HLSP\hlsp_qlp_tess_ffi_s0098-0000000260128333_tess_v01_llc\hlsp_qlp_tess_ffi_s0098-0000000260128333_tess_v01_llc.fits"
t, f, _ = load(Q)
keep, _ = eclipse_mask(t, f, 14.6084, 4.7, 6.1, 0.454)
ev = find_events(t[keep], f[keep]); fl = find_events(t[keep], 2 - f[keep])
print("QLP S98 events:", [(round(e["center"], 3), e["dur_h"], round(e["snr"], 1), round(e["depth_ppm"])) for e in ev])
print("QLP S98 flipped (false alarms):", [(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in fl])
print("planet found:", any(abs(e["center"] - 4025.63) < 0.3 for e in ev))
