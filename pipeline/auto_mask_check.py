"""Does eclipse_mask_auto (no widths given) agree with the hand-tuned TOI-1338 mask, and do we still find the planet?"""
import numpy as np
from detect_v2 import load, eclipse_mask, eclipse_mask_auto, find_events
S = r"D:\second-sun\data\wave-3\lk\mastDownload\TESS\tess2025312202959-s0098-0000000260128333-0298-s\tess2025312202959-s0098-0000000260128333-0298-s_lc.fits"
t, f, _ = load(S)
k_hand, _ = eclipse_mask(t, f, 14.6084, 4.7, 6.1, 0.454)
k_auto, runs = eclipse_mask_auto(t, f, 14.6084)
print("auto runs (phase):", [(round(a, 4), round(b, 4)) for a, b in runs])
print(f"masked: hand {100*(~k_hand).mean():.1f}%  auto {100*(~k_auto).mean():.1f}%  agree on {100*(k_hand == k_auto).mean():.1f}% of points")
ev = find_events(t[k_auto], f[k_auto])
print("events (auto mask):", [(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in ev])
assert len(runs) >= 1 and any(abs(e["center"] - 4025.63) < 0.3 for e in ev), "auto mask must keep the planet findable"
print("auto mask check passed")
