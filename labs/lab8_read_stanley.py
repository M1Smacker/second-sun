r"""Lab 8: read STANLEY's search result for TOI-1338. Run:  .\.venv\Scripts\python.exe labs\lab8_read_stanley.py
Reads data\stanley\PlanetSearchOutput\ss_toi1338_rec (STANLEY's stage 2, run on 20 October 2026, 33 minutes)."""
import _env, re
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

d = _env.ROOT / "data/stanley/PlanetSearchOutput/ss_toi1338_rec"
# The trial periods: STANLEY saves its grid as text. Pull out every number, keep the ones that are 85-105 days (in seconds).
nums = np.array([float(x) for x in re.findall(r"float64\(([^)]+)\)", (d / "TIC_260128333_searchParameters_array").read_text())])
P = nums[(nums > 85 * 86400) & (nums < 105 * 86400)] / 86400
sig = np.load(d / "TIC_260128333_searchResults_array_1_1.npy").reshape(len(P), -1)   # rows: periods, columns: orbit angles
sig = np.where(sig == -29, np.nan, sig)          # -29 marks an unused cell (some periods have fewer angles)
print(f"Grid: {len(P)} trial periods from {P[0]:.2f} to {P[-1]:.2f} days x up to {sig.shape[1]} starting angles = {np.isfinite(sig).sum()} orbits tried")
best = np.nanmax(sig, axis=1)
for k in np.argsort(best)[::-1][:5]:
    print(f"  period {P[k]:6.2f} d: best score {best[k]:5.1f} sigma")
g = sig[np.isfinite(sig)]
print(f"Typical score (median): {np.median(g):.1f} sigma; scores above 5 sigma: {100 * (g > 5).mean():.0f}% of all orbits")
print("TOI-1338 b's published period: 95.2 days (Kostov et al. 2020)")

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(P, best, "-", color="C0"); ax[0].axvline(95.2, color="C3", ls="--", label="TOI-1338 b, 95.2 d")
ax[0].set_xlabel("Trial planet period (days)"); ax[0].set_ylabel("Best score over all angles (sigma)"); ax[0].legend()
ax[1].hist(g, bins=60, color="0.5"); ax[1].set_xlabel("Score (sigma)"); ax[1].set_ylabel("Number of orbits"); ax[1].set_yscale("log")
fig.tight_layout(); out = _env.OUT / "lab8_stanley_toi1338.png"; fig.savefig(out, dpi=110); print("Picture saved:", out)
