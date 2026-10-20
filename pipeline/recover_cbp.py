r"""Step B of the smallest circumbinary injection-recovery test (Compass review 2026-10-20, priority 1).

Reads data/stanley/inj/*.npz from pipeline/stanley/inject_cbp.py (STANLEY N-body transit times, irregular).
For each injected planet: auto eclipse mask -> detect_v2.find_events, the same as our search. Per transit:
  in_mask   = transit centre falls inside the binary's eclipse mask (lost before the search even looks)
  in_gap    = no data within the transit
  found     = an event within max(0.5*duration, 0.25 d) of the injected centre
  retained  = depth left after our 2-d biweight detrend / injected depth (middle half of the transit)
Events already found in the un-injected light curve (TOI-1338 b, systematics) are not credited to injections.
Run with the main venv python.
"""
import pathlib, numpy as np
from detect_v2 import eclipse_mask_auto, find_events, detrend

INJ = pathlib.Path(__file__).resolve().parents[1] / "data" / "stanley" / "inj"
PBIN, RA_RSUN, FRAT = 14.60864170112763, 1.25, 0.01
REARTH_RSUN = 6.371e6 / 6.957e8

t = np.load(INJ / "time_btjd.npy")
f0 = np.load(INJ / "flux_orig.npy").astype(float)
keep, _ = eclipse_mask_auto(t, f0, PBIN)            # mask from the clean data, as the real search would
print(f"eclipse mask removes {100 * (1 - keep.mean()):.1f}% of cadences")
base = [e["center"] for e in find_events(t[keep], f0[keep])]


def near(c, centres, tol):
    return any(abs(c - x) < tol for x in centres)


rows = []
for p in sorted(INJ.glob("rp*_p*.npz")):
    d = np.load(p)
    fi = d["flux"].astype(float)
    tt, dur_h, rp, pp = d["tt"], d["dur_h"], float(d["rp"]), float(d["pp"])
    exp_depth = (rp * REARTH_RSUN / RA_RSUN) ** 2 / (1 + FRAT)
    ev = [e for e in find_events(t[keep], fi[keep]) if not near(e["center"], base, 0.5)]
    tk, fk = detrend(t[keep], fi[keep])
    n = dict(total=len(tt), in_gap=0, in_mask=0, searched=0, found=0); ret = []
    for c, dh in zip(tt, dur_h):
        half = dh / 48
        if not np.any(np.abs(t - c) < half):
            n["in_gap"] += 1; continue
        if not np.any(np.abs(t[keep] - c) < half):
            n["in_mask"] += 1; continue
        n["searched"] += 1
        n["found"] += near(c, [e["center"] for e in ev], max(half, 0.25))
        mid = np.abs(tk - c) < half / 2
        if mid.sum() >= 5:
            ret.append((1 - np.median(fk[mid])) / exp_depth)
    fakes = sum(not near(e["center"], tt, 0.5) for e in ev)
    r = np.median(ret) if ret else np.nan
    rows.append((p.stem, rp, pp, exp_depth * 1e6, n, r, fakes))
    print(f"{p.stem}: depth {exp_depth*1e6:.0f} ppm | {n['total']} transits: {n['in_gap']} in gaps, {n['in_mask']} "
          f"inside eclipse mask, {n['found']}/{n['searched']} found | median depth retained {r:.2f} | "
          f"{fakes} other new events", flush=True)
