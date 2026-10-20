r"""Lab 9: run the whole route on a G1 star. Run:  .\.venv\Scripts\python.exe labs\lab9_your_star.py 48507019 3
Arguments: a TIC number from targets\g1_targets.csv, and how many SPOC sectors to use (default 3; each is about 2 MB).
Every download is logged in research\downloads.csv (project rule). Practice only: nothing here is a candidate."""
import _env, sys, csv, datetime, os
import numpy as np, lightkurve as lk, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, str(_env.ROOT / "pipeline"))
from detect_v2 import load, eclipse_mask_auto, find_events, systematics, veto

tic = int(sys.argv[1]) if len(sys.argv) > 1 else 48507019
nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 3
rows = [r for r in csv.DictReader(l for l in open(_env.ROOT / "targets/g1_targets.csv") if not l.startswith("#")) if int(r["tic"]) == tic]
if not rows:
    sys.exit(f"TIC {tic} is not in the G1 list. Pick one from targets/g1_targets.csv")
P = float(rows[0]["p_bin_d"])
print(f"TIC {tic} = KIC {rows[0]['kic']}, Tmag {rows[0]['tmag']}, binary period {P} d" + (f" (also {rows[1]['p_bin_d']} d)" if len(rows) > 1 else ""))

# 1. Find and download SPOC 2-minute light curves (logged).
res = lk.search_lightcurve(f"TIC {tic}", author="SPOC", exptime=120)
print(f"SPOC 2-minute sectors available: {len(res)}; using the first {min(nmax, len(res))}")
log = _env.ROOT / "research/downloads.csv"
paths = []
for r in res[:nmax]:
    lc = r.download(download_dir=str(_env.DATA)); p = lc.meta["FILENAME"]; paths.append(p)
    if p not in log.read_text(encoding="utf-8"):
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(f"{datetime.datetime.utcnow():%Y-%m-%dT%H:%M:%SZ},TIC {tic} {r.mission[0]} SPOC 2-min LC (Lab 9),https://mast.stsci.edu,{os.path.getsize(p)},{p},Bible Overhaul Lab 9,bible-overhaul\n")

# 2. One eclipse mask from ALL sectors folded together (one sector can't pin down a long-period binary's eclipses).
data = [load(p)[:2] for p in paths]
T = np.concatenate([d[0] for d in data]); F = np.concatenate([d[1] for d in data])
keep_all, runs = eclipse_mask_auto(T, F, P)
print(f"Eclipses found by folding all sectors: {len(runs)}; masked {100 * (1 - keep_all.mean()):.1f}% of the data")

# 3. Search each sector, search its upside-down copy, then apply the systematics flags (Chapter 10).
n_kept = 0
for p, (t, f) in zip(paths, data):
    k = np.isin(t, T[keep_all])
    ev = find_events(t[k], f[k]); flipped = find_events(t[k], 2 - f[k])
    edges, dumps = systematics(p)
    kept, rejected = veto(ev, edges, dumps, flipped)
    sector = p.split("-s00")[1][:2]
    print(f"\nSector {sector}: {len(ev)} events above SNR 7, {len(rejected)} rejected (also in flipped data), {len(flipped)} events in the flipped data")
    for e in kept:
        n_kept += 1
        print(f"  BTJD {e['center']:.3f}  {e['dur_h']:.0f} h  SNR {e['snr']:.1f}  {e['depth_ppm']:.0f} ppm  flags: {', '.join(e['flags']) or 'none'}")
        z = np.abs(t - e["center"]) < 1.5
        fig, ax = plt.subplots(figsize=(8, 3)); ax.plot(t[z], f[z], ".", ms=2, color="0.5"); ax.plot(t[z & ~k], f[z & ~k], ".", ms=2, color="C3")
        ax.axvline(e["center"], color="C0", lw=0.8); ax.set_title(f"TIC {tic} sector {sector}: event at BTJD {e['center']:.3f} (red = masked eclipse)")
        fig.tight_layout(); fig.savefig(_env.OUT / f"lab9_tic{tic}_{e['center']:.2f}.png", dpi=110); plt.close(fig)
print(f"\nEvents to vet by hand: {n_kept}. Pictures in {_env.OUT}")
