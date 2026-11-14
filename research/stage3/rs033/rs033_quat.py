"""RS-033 feasibility (Claude, 14 Nov 2026): 2-second pointing jitter around dumps, sector 11. Method in POINTING-FEASIBILITY-2026-11-14.md."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rs032"))
import numpy as np, pandas as pd
from astropy.io import fits
import rs032_wobble as W                    # dumps (design stars), file lookup
ROOT = W.ROOT; SEC = 11
Q = fits.open(ROOT / "data" / "tess_quat_2026-11-14" / "tess2019140185400_sector11-quat.fits", memmap=True)
dumps = W.DUMPS[SEC]
ASEC = 206264.806
out = {"dumps": len(dumps), "profile": {}, "events": []}
JIT = {}
for cam in (1, 2, 3, 4):
    d = Q[cam].data
    t = np.asarray(d["TIME"], float)
    q = np.stack([np.asarray(d[f"C{cam}_Q{i}"], float) for i in (1, 2, 3)], 1) * 2 * ASEC
    ok = np.isfinite(t) & np.all(np.isfinite(q), 1)
    t, q = t[ok], q[ok]
    w = np.floor((t - t[0]) / (30 / 1440)).astype(int)
    df = pd.DataFrame(q, columns=["a", "b", "c"]); df["w"] = w
    dev = df[["a", "b", "c"]] - df.groupby("w")[["a", "b", "c"]].transform("mean")
    dev["w"] = w
    rms = np.sqrt((dev[["a", "b", "c"]] ** 2).sum(1).groupby(dev.w).mean())
    tw = pd.Series(t).groupby(w).mean()
    far = np.array([np.min(np.abs(dumps - x)) > 1.0 for x in tw.values]) if dumps.size else np.ones(len(tw), bool)
    ref = float(np.median(rms.values[far]))
    JIT[cam] = (tw.values, rms.values / ref)
    rel = np.array([(x - dumps[np.argmin(np.abs(dumps - x))]) * 24 for x in tw.values])
    prof = {}
    for h in range(-24, 12):
        m = (rel >= h) & (rel < h + 1)
        if m.any():
            prof[h] = round(float(np.median(rms.values[m] / ref)), 3)
    out["profile"][cam] = {"ref_arcsec": round(ref, 4), "by_hour_from_dump": prof}
    print("camera", cam, "ref", round(ref, 4), "arcsec;", {h: prof.get(h) for h in (-24, -18, -12, -8, -6, -4, -2, -1, 0, 1, 2, 6)}, flush=True)


def box_jitter(cam, c, dd):
    tw, r = JIT[cam]
    m = np.abs(tw - c) <= max(dd, 1 / 24) / 2 + 0.01
    return float(np.median(r[m])) if m.any() else np.nan


rows = pd.read_csv(ROOT / "data" / "rs032" / "wobble-rows.csv")
rows = rows[rows.sector == SEC]
for r in rows.itertuples():
    p = W.file_for(r.campaign, int(r.tic), SEC, r.product)
    if p is None:
        continue
    cam = int(fits.getheader(p, 0).get("CAMERA") or fits.getheader(p, 1).get("CAMERA") or 0)
    if cam not in JIT:
        continue
    out["events"].append(dict(group=r.group, tic=int(r.tic), cam=cam, dt_h=round(float((r.center - dumps[np.argmin(np.abs(dumps - r.center))]) * 24), 1),
                              jq=round(box_jitter(cam, r.center, r.dur_d), 3), J_centroid=r.J))
ev = pd.DataFrame(out["events"])
print(ev.groupby("group").jq.describe() if len(ev) else "no events")
print(ev[ev.group != "Pl2"])
(HERE / "quat.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
