"""QLP TOI-1338 S98 with windows = intersection of 3 NEIGHBOURS' SPOC windows (TOI-1338's own file NOT used), start-trimmed."""
import glob
from detect_v2 import load, eclipse_mask, find_events, good_windows, intersect_windows, in_windows
Q = r"D:\second-sun\data\wave-3\lk\mastDownload\HLSP\hlsp_qlp_tess_ffi_s0098-0000000260128333_tess_v01_llc\hlsp_qlp_tess_ffi_s0098-0000000260128333_tess_v01_llc.fits"
nb = [p for p in glob.glob(r"D:\second-sun\data\overnight\lk\mastDownload\TESS\*s0098*\*_lc.fits") if "260128333" not in p]
win = intersect_windows([good_windows(p) for p in nb], trim_start_d=0.5)
print(len(nb), "neighbours; windows:", [(round(a, 2), round(b, 2)) for a, b in win])
t, f, _ = load(Q)
keep, _ = eclipse_mask(t, f, 14.6084, 4.7, 6.1, 0.454)
keep &= in_windows(t, win)
ev = find_events(t[keep], f[keep]); fl = find_events(t[keep], 2 - f[keep])
print("events:", [(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in ev], "| fakes", len(fl), "max", round(max([e["snr"] for e in fl], default=0), 1), "| kept", round(keep.mean(), 2))
found = any(abs(e["center"] - 4025.63) < 0.3 for e in ev); print("planet found:", found)
