"""Detector v2 on QLP S98 of TOI-1338 (independent product, rule C8), restricted to SPOC good-time windows."""
from detect_v2 import load, eclipse_mask, find_events, good_windows, in_windows
Q = r"D:\second-sun\data\wave-3\lk\mastDownload\HLSP\hlsp_qlp_tess_ffi_s0098-0000000260128333_tess_v01_llc\hlsp_qlp_tess_ffi_s0098-0000000260128333_tess_v01_llc.fits"
S = r"D:\second-sun\data\wave-3\lk\mastDownload\TESS\tess2025312202959-s0098-0000000260128333-0298-s\tess2025312202959-s0098-0000000260128333-0298-s_lc.fits"
t, f, _ = load(Q)
keep, _ = eclipse_mask(t, f, 14.6084, 4.7, 6.1, 0.454)
keep &= in_windows(t, good_windows(S))
ev = find_events(t[keep], f[keep]); fl = find_events(t[keep], 2 - f[keep])
print("QLP S98 (SPOC windows) events:", [(round(e["center"], 3), e["dur_h"], round(e["snr"], 1), round(e["depth_ppm"])) for e in ev])
print("flipped (false alarms):", [(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in fl])
found = any(abs(e["center"] - 4025.63) < 0.3 for e in ev)
print("planet found:", found); assert found
