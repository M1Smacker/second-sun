r"""Lab 5: fold a binary's light curve and look at both eclipses. Run:  .\.venv\Scripts\python.exe labs\lab5_two_suns.py
Uses TOI-1338 sector 98 (already on D:). The two stars orbit each other every 14.6086 days."""
import _env, sys, glob
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, str(_env.ROOT / "pipeline"))
from detect_v2 import load, eclipse_mask_auto
from wotan import flatten

path = glob.glob(str(_env.ROOT / "data/wave-*/lk/mastDownload/TESS/*s0098-0000000260128333-0298-s/*_lc.fits"))[0]
P = 14.6086                                       # days, from the binary's catalogue period
t, f, _ = load(path)
keep, runs = eclipse_mask_auto(t, f, P)           # finds the eclipses by folding (Chapter 6)
flat = flatten(t, f, method="biweight", window_length=2.0)
ph = (t % P) / P                                  # phase: where in the orbit each measurement sits (0 to 1)
print(f"Folded {len(t)} measurements at P = {P} d. Eclipses found: {len(runs)}")
for a, b in runs:
    m = (ph >= a % 1) & (ph <= b % 1) if a >= 0 else (ph >= a + 1) | (ph <= b)
    depth = 1 - np.nanmedian(flat[m])              # the middle value inside the eclipse: not fooled by noisy low points
    centre = ((a + b) / 2) % 1
    print(f"  phase {centre:.3f}: depth {depth * 100:.2f}%, width about {(b - a) * P * 24:.1f} h")
c = sorted(((a + b) / 2) % 1 for a, b in runs)
if len(c) == 2:
    print(f"Second eclipse comes {((c[1] - c[0]) % 1):.3f} of an orbit after the first (0.500 would mean a circular orbit)")
print(f"Masked before searching: {100 * (1 - keep.mean()):.1f}% of the data")

fig, ax = plt.subplots(1, 3, figsize=(12, 4), gridspec_kw={"width_ratios": [2, 1, 1]})
ax[0].plot(ph[keep], flat[keep], ".", ms=1, color="0.5"); ax[0].plot(ph[~keep], flat[~keep], ".", ms=1, color="C3")
ax[0].set_xlabel("Phase (fraction of the 14.6-day orbit)"); ax[0].set_title("Folded: every orbit stacked")
for k, cc in enumerate(c[:2]):
    z = np.abs(((ph - cc + 0.5) % 1) - 0.5) < 0.02
    ax[k + 1].plot((((ph[z] - cc + 0.5) % 1) - 0.5) * P * 24, flat[z], ".", ms=2, color="C3")
    ax[k + 1].set_title(f"Eclipse at phase {cc:.3f}"); ax[k + 1].set_xlabel("Hours from centre")
fig.tight_layout(); out = _env.OUT / "lab5_toi1338_fold.png"; fig.savefig(out, dpi=110); print("Picture saved:", out)
