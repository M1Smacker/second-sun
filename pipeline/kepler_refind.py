"""Kepler re-find test (deep review section 6): can detect_v2 find the known planet transits of Kepler-16, -34, -35
in the original Kepler long-cadence data?
Step "key": an answer key built with a DIFFERENT method than the detector (3-day median flatten, runs of >= 4 single
cadences below 4 robust sigma, out of eclipse), checked by eye on key_windows.png and against Davies et al. 2026 Table 2
transit counts (7, 9, 7). It is our own measurement, not a published table.
Step "score": detect_v2.find_events per quarter (2-day biweight, boxes 3-15 h, SNR >= 7) on PDCSAP and on SAP;
a transit counts as found if an event centre is within half the event's length plus 0.1 d of the key time.
Usage: python kepler_refind.py key | score"""
import sys, glob, json, pathlib, warnings
import numpy as np
import lightkurve as lk
from scipy.ndimage import median_filter
from detect_v2 import eclipse_mask_auto, find_events

warnings.filterwarnings("ignore")
D = pathlib.Path(r"D:\second-sun\data\kepler-refind")
OUT = pathlib.Path(r"D:\second-sun\research\kepler-refind-2026-10-23")
STARS = {"Kepler-16": (12644769, 41.0775867, 228.8), "Kepler-34": (8572936, 27.7958079, 288.8),
         "Kepler-35": (9837578, 20.7337490, 131.4)}   # KIC, P_bin (Villanova), planet period (d, for spacing check only)


def quarters(kic, col):
    out = []
    for p in sorted(glob.glob(str(D / "**" / f"kplr{kic:09d}-*_llc.fits"), recursive=True)):
        lc = lk.read(p, quality_bitmask="hard")
        t = lc.time.value; f = np.asarray(lc[col].value, float)
        ok = np.isfinite(t) & np.isfinite(f)
        if ok.sum() > 100:
            out.append((lc.meta.get("QUARTER"), t[ok], f[ok] / np.median(f[ok])))
    return out


def masked(kic, P, col):
    qs = quarters(kic, col)
    t = np.concatenate([q[1] for q in qs]); f = np.concatenate([q[2] for q in qs])
    keep, runs = eclipse_mask_auto(t, f, P)
    return [(q, tq, fq, keep[np.isin(t, tq)]) for q, tq, fq in qs], runs


def key():
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}
    for name, (kic, P, Pp) in STARS.items():
        qs, runs = masked(kic, P, "pdcsap_flux")
        cands = []
        for q, t, f, k in qs:
            t, f = t[k], f[k]
            r = f / median_filter(f, size=145, mode="nearest") - 1          # 145 cadences ~ 3 days
            sig = 1.4826 * np.median(np.abs(r - np.median(r)))
            low = r < -4 * sig
            i = 0
            while i < len(r):
                if low[i]:
                    j = i
                    while j + 1 < len(r) and low[j + 1] and t[j + 1] - t[j] < 0.05:
                        j += 1
                    if j - i + 1 >= 4:
                        s = slice(i, j + 1)
                        cands.append(dict(t=round(float(np.mean(t[s])), 3), q=q, n=j - i + 1,
                                          depth_ppm=round(float(-np.median(r[s])) * 1e6), dur_h=round((t[j] - t[i]) * 24 + 0.49, 1)))
                    i = j + 1
                else:
                    i += 1
        res[name] = dict(kic=kic, P_bin=P, eclipse_runs=[[round(a, 4), round(b, 4)] for a, b in runs], candidates=cands)
        print(name, "eclipse phase runs:", res[name]["eclipse_runs"])
        for c in cands:
            print("   ", c)
    json.dump(res, open(OUT / "key_candidates.json", "w"), indent=1)


def plot_key(times, half=1.5, fname="key_windows.png"):
    """times: {name: [t, ...]} -> one panel per window, for checking by eye (y range from out-of-eclipse points)."""
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    panels = [(n, t) for n, ts in times.items() for t in ts]
    cols = 6; rows = int(np.ceil(len(panels) / cols))
    fig, ax = plt.subplots(rows, cols, figsize=(3 * cols, 2.2 * rows), squeeze=False)
    data = {n: masked(STARS[n][0], STARS[n][1], "pdcsap_flux")[0] for n in times}
    for a, (n, t0) in zip(ax.flat, panels):
        ys = []
        for q, t, f, k in data[n]:
            w = np.abs(t - t0) < half
            if w.any():
                a.plot(t[w] - t0, f[w], ".", ms=2, color="0.6"); a.plot(t[w & k] - t0, f[w & k], ".", ms=2, color="k")
                ys += list(f[w & k])
        if len(ys) > 10:
            lo, hi = np.percentile(ys, [0.5, 99.5]); a.set_ylim(lo - 0.3 * (hi - lo), hi + 0.1 * (hi - lo))
        a.axvline(0, color="orange", lw=0.6); a.set_title(f"{n} {t0:.2f}", fontsize=8); a.tick_params(labelsize=6)
    for a in ax.flat[len(panels):]:
        a.axis("off")
    fig.tight_layout(); fig.savefig(OUT / fname, dpi=80)


def score(keyfile):
    k = json.load(open(keyfile))
    out = {}
    for name, (kic, P, Pp) in STARS.items():
        truth = k[name]
        out[name] = {}
        for col in ("pdcsap_flux", "sap_flux"):
            qs, _ = masked(kic, P, col)
            events = []
            for q, t, f, kp in qs:
                events += [dict(e, q=q) for e in find_events(t[kp], f[kp])]
            hit = lambda tt: any(abs(e["center"] - tt) < 0.5 * e["dur_h"] / 24 + 0.1 for e in events)
            found = [tt for tt in truth if hit(tt)]
            extra = [e for e in events if not any(abs(e["center"] - tt) < 0.5 * e["dur_h"] / 24 + 0.1 for tt in truth)]
            out[name][col] = dict(key=len(truth), found=len(found), missed=[tt for tt in truth if tt not in found],
                                  snr_found=[round(e["snr"], 1) for tt in found for e in events
                                             if abs(e["center"] - tt) < 0.5 * e["dur_h"] / 24 + 0.1][:len(found)],
                                  other_events=len(extra), quarters=len(qs),
                                  other_per_quarter=round(len(extra) / len(qs), 2),
                                  other=[(round(e["center"], 2), e["dur_h"], round(e["snr"], 1)) for e in extra][:15])
            print(name, col, {x: out[name][col][x] for x in ("key", "found", "missed", "snr_found", "other_events", "other_per_quarter")})
    json.dump(out, open(OUT / "score.json", "w"), indent=1)


if __name__ == "__main__":
    {"key": key, "score": lambda: score(OUT / "key.json")}[sys.argv[1]]()
