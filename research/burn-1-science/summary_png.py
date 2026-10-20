"""Burn 1: one phone-friendly summary picture (1080 x 1920 px, large fonts) -> burn1_summary.png."""
import json, pathlib, numpy as np, batman
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = pathlib.Path(__file__).parent
d = np.load(here / "fit_event_data.npz")
grid = json.loads((here / "chi2_grid_results.json").read_text())["fine"]
inj = json.loads((here / "inject_results.json").read_text())
diag = json.loads((here / "diagnose_results.json").read_text())

BLUE, ORANGE, INK, INK2, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#fcfcfb"
GOOD, BAD = "#0ca30c", "#d03b3b"
PRED_T0, PRED_DUR = 4025.5927, 6.31
plt.rcParams.update({"font.size": 21, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})

fig = plt.figure(figsize=(9, 16), dpi=120, facecolor=SURF)
fig.text(0.05, 0.982, "TOI-1338 b: our test, 16 Dec 2025", fontsize=28, weight="bold", color=INK, va="top")
fig.text(0.05, 0.950, "A known planet with two suns.\nInternal tool test, not a discovery.", fontsize=20,
         color=INK2, va="top")
fig.text(0.05, 0.900, "Orange band = when a 2024 paper said it would be.", fontsize=19, color=INK, va="top")
fig.text(0.05, 0.880, "Blue dots = what TESS saw (30-min averages).", fontsize=19, color=INK, va="top")

# --- Panel 1: predicted vs seen -------------------------------------------------
ax = fig.add_axes([0.19, 0.645, 0.77, 0.21], facecolor=SURF)
t, f, base = d["t"], d["f"], d["base"]
r = f / base
hrs = (t - PRED_T0) * 24
edges = np.arange(hrs.min(), hrs.max() + 0.5, 0.5)
idx = np.digitize(hrs, edges)
bins = [k for k in np.unique(idx) if np.sum(idx == k) >= 5]
bh = np.array([hrs[idx == k].mean() for k in bins])
bf = np.array([r[idx == k].mean() for k in bins])
ax.axvspan(-PRED_DUR / 2, PRED_DUR / 2, color=ORANGE, alpha=0.15, lw=0)
ax.axvline(0, color=ORANGE, lw=3)
u = [2 * np.sqrt(0.17) * 0.478, np.sqrt(0.17) * (1 - 2 * 0.478)]
p = batman.TransitParams()
ars = np.sqrt(1.047 ** 2 - 0.428 ** 2) / np.sin(np.pi * grid["best_T14_h"] / 24 / 95.4)
p.t0, p.per, p.rp, p.a, p.inc = grid["best_t0"], 95.4, 0.0475, ars, np.degrees(np.arccos(0.428 / ars))
p.ecc, p.w, p.u, p.limb_dark = 0.0, 90.0, u, "quadratic"
m1 = batman.TransitModel(p, t).light_curve(p) - 1
amp = np.sum(m1 * (r - 1)) / np.sum(m1 * m1)  # scale model depth to the data (least squares)
tf = np.linspace(t.min(), t.max(), 4000)
ax.plot((tf - PRED_T0) * 24, amp * (batman.TransitModel(p, tf).light_curve(p) - 1) * 1e6, color=BLUE, lw=2.5)
ax.plot(bh, (bf - 1) * 1e6, "o", ms=9, color=BLUE, mec=SURF, mew=2)
ax.set_xlim(-12, 14)
ax.set_ylim(-4000, 1300)
ax.set_xlabel("hours from the predicted middle", labelpad=4)
ax.set_ylabel("dimming (ppm)")
fig.text(0.05, 0.585, "RIGHT: same night, same length", fontsize=23, color=GOOD, va="top", weight="bold")
fig.text(0.05, 0.560, f"(~{grid['best_T14_h']:.1f} h seen vs 6.3 h predicted).\n"
         f"Ours is ~{grid['dt_min']:.0f} min later than predicted.", fontsize=20, color=INK, va="top")

# --- Panel 2: recovery of published transits --------------------------------------
fig.text(0.05, 0.495, "Can our method find its OLD transits?", fontsize=23, weight="bold", color=INK, va="top")
why = {3: "only 30-min data", 10: "hidden by eclipse mask", 27: "too shallow for our rule",
       30: "no clean data then", 34: "too shallow for our rule", 37: "too shallow for our rule",
       62: "no clean data then"}
y = 0.462
for row in diag:
    s = row["sector"]
    ok = row.get("w1", {}).get("recovered", False)
    fig.text(0.07, y, ("✓ found" if ok else "✗ missed"), fontsize=19, color=GOOD if ok else BAD,
             weight="bold", va="top")
    fig.text(0.29, y, f"Sector {s}" + ("" if ok else f": {why.get(s, '')}"), fontsize=19, color=INK, va="top")
    y -= 0.0215
fig.text(0.07, y - 0.002, "3 of the 6 that are in our data.", fontsize=19, color=INK2, va="top")

# --- Panel 3: injection-recovery ---------------------------------------------------
fig.text(0.05, 0.200, "Fake planets hidden in the Dec 2025 data:", fontsize=21, color=INK, va="top", weight="bold")
fig.text(0.05, 0.178, "found only when 7x Earth or bigger.", fontsize=21, color=INK, va="top")
ax = fig.add_axes([0.19, 0.045, 0.77, 0.095], facecolor=SURF)
R = [row["R_earth"] for row in inj["rows"]]
frac = [row["recovered"] / row["n"] for row in inj["rows"]]
ax.bar(R, frac, width=0.7, color=BLUE)
ax.set_xticks(R)
ax.set_ylim(0, 1.05); ax.set_yticks([0, 1]); ax.set_yticklabels(["0%", "100%"])
ax.set_xlabel("fake planet size (x Earth)", labelpad=2)
ax.axvline(7.66, color=ORANGE, lw=3)
ax.annotate("TOI-1338 b's size", xy=(7.66, 0.5), xytext=(4.0, 0.5), color=INK, fontsize=18, va="center",
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))

fig.savefig(here / "burn1_summary.png", facecolor=SURF)
print("wrote", here / "burn1_summary.png")
