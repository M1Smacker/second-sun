"""Local contact sheet of Stage 2 survivors and of the surviving events on the known-host controls (key-1 inspection).
Writes ONLY to D:\\second-sun\\data\\stage2\\ (git-ignored). Never publish this image or its contents. Usage: python stage2_look.py"""
import pathlib, warnings
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import stage2_search as s
from detect_v2 import detrend

warnings.filterwarnings("ignore")
D = pathlib.Path(r"D:\second-sun\data\stage2")
surv = pd.read_csv(D / "survivors_LOCAL.csv")
R = pd.read_csv(D / "events_real_LOCAL.csv")
ctl = R[(R.stratum == "control") & ~R.gap_dump & ~R.burst & ~R.flipmatch]
rows = pd.concat([surv.assign(group="survivor"), ctl.assign(group="control")]).reset_index(drop=True)
s._init(); gl = {(t, sec): ps for t, sec, ps in s.groups()}
fig, ax = plt.subplots(len(rows), 2, figsize=(11, 2.1 * len(rows)), squeeze=False)
for i, r in rows.iterrows():
    d = None
    for p in gl[(int(r.tic), int(r.sector))]:
        dd, m = s.prepare(p)
        if dd is not None and m["product"] == r["product"]:
            d = dd; break
    t, f = d["t"], d["f"]; tt, ff = detrend(t, f)
    c, w = r.center, r.dur_h / 24
    for k, (half, y, tx, ty) in enumerate(((3.0, f, t, "masked flux"), (1.5, ff, tt, "flattened"))):
        a = ax[i, k]; sel = np.abs(tx - c) < half
        a.plot(tx[sel] - c, y[sel], ".", ms=1.5, color="0.5")
        if sel.sum() > 30:
            nb = max(1, int(round(0.04 / np.median(np.diff(tx))))); n = sel.sum() // nb
            yy = y[sel][: n * nb].reshape(n, nb).mean(1); xx = (tx[sel][: n * nb].reshape(n, nb).mean(1)) - c
            a.plot(xx, yy, "-", color="k", lw=0.8)
        a.axvspan(-w / 2, w / 2, color="orange", alpha=0.25); a.tick_params(labelsize=6)
        if k == 0:
            a.set_ylabel(f"{r.group[:4]} #{i}\nSNR {r.snr:.0f} {r.dur_h}h\n{r['product'][:4]} {'2nd:' + format(r.c8_best, '.0f') if r.c8_has else 'no 2nd'}", fontsize=6)
fig.tight_layout(); fig.savefig(D / "stage2_survivors_LOCAL.png", dpi=75)
print(len(rows), "rows:", rows.group.value_counts().to_dict(), "->", D / "stage2_survivors_LOCAL.png")
