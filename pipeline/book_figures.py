"""Figures for book chapter 4, from real TOI-1338 sector 98 data and tonight's results.
Writes PNGs (phone-width friendly) into book/docs/book/img/. Dark-on-light neutral palette, one amber accent."""
import json, pathlib, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from detect_v2 import load, eclipse_mask, detrend, bin10, box_scores

OUT = pathlib.Path(r"D:\second-sun\book\docs\book\img"); OUT.mkdir(parents=True, exist_ok=True)
AMBER, INK, GREY = "#b07a1e", "#1a1e26", "#8a909c"
plt.rcParams.update({"font.size": 13, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": GREY, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})
P98 = r"D:\second-sun\data\wave-3\lk\mastDownload\TESS\tess2025312202959-s0098-0000000260128333-0298-s\tess2025312202959-s0098-0000000260128333-0298-s_lc.fits"

t, f, _ = load(P98)
keep, T1 = eclipse_mask(t, f, 14.6084, 4.7, 6.1, 0.454)

# Fig 4.1: raw light curve with eclipses marked and the planet transit
fig, ax = plt.subplots(figsize=(7.8, 4.2), dpi=150)
ax.plot(t, f, ".", ms=1, color=GREY, label="all data")
ax.plot(t[~keep], f[~keep], ".", ms=1.5, color=INK, label="eclipses (masked)")
ax.axvspan(4025.45, 4025.80, color=AMBER, alpha=.25, lw=0, label="TOI-1338 b transit")
ax.set_xlabel("Time (BTJD days)"); ax.set_ylabel("Relative brightness")
ax.set_ylim(0.93, 1.01); ax.legend(loc="lower left", fontsize=10, frameon=False, markerscale=4, handletextpad=1.2)
ax.set_title("TOI-1338, TESS sector 98", fontsize=13, loc="left")
fig.tight_layout(); fig.savefig(OUT / "fig4-1-s98-raw.png"); plt.close(fig)

# Fig 4.2: detrended, binned, plus box SNR for 6.5 h
tt, ff = detrend(t[keep], f[keep])
bt, bf = bin10(tt, ff)
c, snr, _ = box_scores(bt, bf, 6.5)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.8, 5.6), dpi=150, sharex=True)
a1.plot(bt, (bf - 1) * 1e6, ".", ms=2, color=GREY)
a1.axvspan(4025.45, 4025.80, color=AMBER, alpha=.25, lw=0)
a1.set_ylabel("Brightness (ppm)"); a1.set_ylim(-5000, 3000)
a1.set_title("After masking eclipses and flattening (10-min bins)", fontsize=13, loc="left")
a2.plot(c, snr, color=INK, lw=1)
a2.axhline(7, color=AMBER, lw=1.5, ls="--"); a2.text(c[0], 7.4, "threshold 7", color=AMBER, fontsize=11)
a2.set_ylabel("Box SNR (6.5 h)"); a2.set_xlabel("Time (BTJD days)")
fig.tight_layout(); fig.savefig(OUT / "fig4-2-s98-snr.png"); plt.close(fig)

# Fig 4.3: injection results v1 vs v2
inj = json.load(open(pathlib.Path(__file__).with_name("accept_v2_results.json")))["injection"]
re_ = [r["R_earth"] for r in inj]
v2 = [r["recovered"] / r["n"] for r in inj]
v1 = [0, 0, 0, 0, 0, 7 / 8, 1]  # burn 1, research/burn-1-science/inject_results.json
fig, ax = plt.subplots(figsize=(7.8, 4.0), dpi=150)
w = 0.38
ax.bar(np.array(re_) - w / 2, v1, w, color=GREY, label="v1 (burn 1)")
ax.bar(np.array(re_) + w / 2, v2, w, color=AMBER, label="v2 (tonight)")
ax.set_xlabel("Fake planet size (Earth radii)"); ax.set_ylabel("Fraction found")
ax.set_ylim(0, 1.05); ax.legend(frameon=False, fontsize=11)
ax.set_title("Fake planets hidden in sector 98: how many we find", fontsize=13, loc="left")
fig.tight_layout(); fig.savefig(OUT / "fig4-3-injection.png"); plt.close(fig)
print("figures:", sorted(p.name for p in OUT.glob("*.png")))
