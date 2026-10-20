r"""Lab 4: find a planet's dip, by eye and then with our search. Run:  .\.venv\Scripts\python.exe labs\lab4_find_a_dip.py
Uses TOI-1338 sector 98 (already on D:), where the known planet TOI-1338 b crossed on 16 December 2025."""
import _env, sys, glob
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, str(_env.ROOT / "pipeline"))
from detect_v2 import load, eclipse_mask_auto, detrend, find_events

path = glob.glob(str(_env.ROOT / "data/wave-*/lk/mastDownload/TESS/*s0098-0000000260128333-0298-s/*_lc.fits"))[0]
P_BIN = 14.6086                                   # TOI-1338's two stars orbit each other every 14.6 days
THR = 7.0                                         # the bar: keep dips more than THR times the noise (Chapter 7)
t, f, _ = load(path)
keep, _ = eclipse_mask_auto(t, f, P_BIN)
print(f"{len(t)} good measurements; eclipses of the two stars cover {100 * (1 - keep.mean()):.1f}% and are masked")
events = find_events(t[keep], f[keep], thr=THR)     # the box search from Chapter 8
print(f"Events above SNR {THR:g}: {len(events)}")
for e in events:
    print(f"  centre BTJD {e['center']:.3f}  length {e['dur_h']:.1f} h  SNR {e['snr']:.1f}  depth {e['depth_ppm']:.0f} ppm")

fig, ax = plt.subplots(3, 1, figsize=(10, 8))
ax[0].plot(t, f, ".", ms=1, color="0.5"); ax[0].plot(t[~keep], f[~keep], ".", ms=1, color="C3")
ax[0].set_title("Whole sector. Red: the two stars eclipsing each other (masked before searching)")
tt, ff = detrend(t[keep], f[keep])
ax[1].plot(tt, ff, ".", ms=1, color="0.5"); ax[1].set_title("Eclipses removed, slow wiggles flattened. Can you spot the dip?")
c = events[0]["center"] if events else tt.mean()
z = np.abs(tt - c) < 1.0
ax[2].plot(tt[z], ff[z], ".", ms=2, color="C0"); ax[2].set_title(f"Zoom: 2 days around BTJD {c:.2f}")
ax[2].set_xlabel("Time (BTJD days)"); fig.tight_layout()
out = _env.OUT / "lab4_toi1338_s98.png"; fig.savefig(out, dpi=110); print("Picture saved:", out)
