r"""Lab 6: hide fake planets in real data and see which ones our search finds. Run:  .\.venv\Scripts\python.exe labs\lab6_fake_planets.py
Uses TOI-1338 sector 98. Each fake is a realistic transit shape (batman) added BEFORE our cleaning, like a real planet."""
import _env, sys, glob
import numpy as np, batman, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, str(_env.ROOT / "pipeline"))
from detect_v2 import load, eclipse_mask_auto, detrend, find_events

path = glob.glob(str(_env.ROOT / "data/wave-*/lk/mastDownload/TESS/*s0098-0000000260128333-0298-s/*_lc.fits"))[0]
t, f, _ = load(path)
keep, _ = eclipse_mask_auto(t, f, 14.6086)
R_STAR = 1.25                                    # the big star's radius in Suns (STANLEY's fit)
SIZES = (3, 4, 5, 6, 8)                          # fake planet radii, in Earth radii
TIMES = (3998.0, 4013.0, 4028.5, 4042.0)         # BTJD: inside good data, away from eclipses and the real planet (4025.6)

def transit(rp_earth, t0, tt=None):
    p = batman.TransitParams()
    p.t0, p.per, p.rp, p.a, p.inc, p.ecc, p.w = t0, 95.2, rp_earth * 0.009168 / R_STAR, 78.6, 90.0, 0.0, 90.0
    p.u, p.limb_dark = [0.4, 0.2], "quadratic"    # star darker at its edge (limb darkening)
    tt = t if tt is None else tt
    return batman.TransitModel(p, tt).light_curve(p)

print(f"{'size':>6} {'depth':>7}   found at " + "  ".join(f"{x:.1f}" for x in TIMES) + "   depth kept")
for rp in SIZES:
    k2 = (rp * 0.009168 / R_STAR) ** 2                         # textbook depth: (planet size / star size) squared
    mid_model = 1 - transit(rp, 0.0, np.linspace(-0.08, 0.08, 161)).mean()   # real centre depth: the star's edge is darker, so the middle is deeper
    hits, kept = [], []
    for t0 in TIMES:
        fi = f * transit(rp, t0)                  # multiply: the planet blocks a fraction of the light
        ev = find_events(t[keep], fi[keep])
        hits.append("yes" if any(abs(e["center"] - t0) < 0.25 for e in ev) else " no")
        tt, ff = detrend(t[keep], fi[keep]); mid = np.abs(tt - t0) < 0.08
        kept.append((1 - np.median(ff[mid])) / mid_model if mid.sum() >= 5 else np.nan)   # nan: masked out, nothing to measure
    print(f"{rp:4g} R+ {k2 * 1e6:5.0f}ppm   " + "    ".join(hits) + f"      {np.nanmedian(kept) * 100:4.0f}%")

fi = f * transit(5, TIMES[1]); tt, ff = detrend(t[keep], fi[keep]); z = np.abs(tt - TIMES[1]) < 1
fig, ax = plt.subplots(figsize=(8, 3)); ax.plot(tt[z], ff[z], ".", ms=2); ax.axvline(TIMES[1], color="C3", lw=0.8)
ax.set_title("A fake 5-Earth-radius planet hidden at BTJD 4013.0 (red line), after cleaning"); ax.set_xlabel("BTJD")
fig.tight_layout(); out = _env.OUT / "lab6_fake_5re.png"; fig.savefig(out, dpi=110); print("Picture saved:", out)
