"""Quick look at one flagged event: SPOC light curve around it (raw + detrended, mask shown), binary phase,
and the same window in QLP (independent product, rule C8). Usage: python look_event.py (Kepler-16 S54 event)."""
import glob, pathlib, datetime, numpy as np, lightkurve as lk, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from detect_v2 import load, eclipse_mask_auto, detrend

TIC, P, SEC, TC = "299096355", 41.0775867, 54, 2775.659
BJD0_BTJD = 54965.657634 + 2400000 - 2457000          # Villanova bjd0 (BJD-2400000) -> BTJD
spoc = glob.glob(rf"D:\second-sun\data\overnight\lk\mastDownload\TESS\*-s{SEC:04d}-0000000{TIC}-*-s\*_lc.fits")[0]
t, f, _ = load(spoc)
keep, runs = eclipse_mask_auto(t, f, P)
tt, ff = detrend(t[keep], f[keep])
print(f"binary phase of event: {((TC - BJD0_BTJD) / P) % 1:.3f} (primary eclipse = 0); auto-mask runs {[(round(a,3), round(b,3)) for a, b in runs]}")
for ph0 in (0.0,):
    nxt = BJD0_BTJD + P * np.ceil((t.min() - BJD0_BTJD) / P)
    print("primary eclipses in this sector (catalogue ephemeris):", [round(x, 2) for x in np.arange(nxt, t.max(), P)])

sq = lk.search_lightcurve(f"TIC {TIC}", author="QLP", sector=SEC)
q = None
if len(sq):
    lcq = sq[0].download(download_dir=r"D:\second-sun\data\overnight\lk")
    pth = lcq.meta["FILENAME"]
    with open(r"D:\second-sun\research\downloads.csv", "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.utcnow():%Y-%m-%dT%H:%M:%SZ},Kepler-16 S{SEC} QLP LC,https://mast.stsci.edu,{pathlib.Path(pth).stat().st_size},{pth},vet dry-run event (C8),overnight\n")
    q = load(pth)

fig, ax = plt.subplots(3, 1, figsize=(8, 8), dpi=120, sharex=True)
w = np.abs(t - TC) < 3
ax[0].plot(t[w], f[w], ".", ms=1.5, color="#8a909c"); ax[0].plot(t[w & ~keep], f[w & ~keep], ".", ms=2, color="#1a1e26")
ax[0].axvspan(TC - 7.5 / 24, TC + 7.5 / 24, color="#b07a1e", alpha=.2); ax[0].set_ylabel("SPOC raw")
w2 = np.abs(tt - TC) < 3
ax[1].plot(tt[w2], (ff[w2] - 1) * 1e6, ".", ms=1.5, color="#8a909c"); ax[1].axvspan(TC - 7.5 / 24, TC + 7.5 / 24, color="#b07a1e", alpha=.2)
ax[1].set_ylabel("SPOC flat (ppm)")
if q is not None:
    tq, fq, _ = q; wq = np.abs(tq - TC) < 3
    ax[2].plot(tq[wq], (fq[wq] / np.nanmedian(fq[wq]) - 1) * 1e6, ".", ms=2, color="#8a909c")
    ax[2].axvspan(TC - 7.5 / 24, TC + 7.5 / 24, color="#b07a1e", alpha=.2)
ax[2].set_ylabel("QLP (ppm)"); ax[2].set_xlabel("BTJD")
fig.suptitle(f"Kepler-16, sector {SEC}: dry-run event at BTJD {TC}", x=0.02, ha="left")
out = pathlib.Path(r"D:\second-sun\research\overnight-science\kepler16_s54_event.png")
fig.tight_layout(); fig.savefig(out); print("saved", out)
