# Q3 (31 Oct 2026): are the short deep upside-down survivors flare-shaped? Exploratory, after the scorecard; changes no result.
# For events found in fast-cadence data (<= 3.4 min), measure the shape in the search's orientation (dip down): is the early part of the box deeper than the late part
# (a flare read upside down starts abruptly and recovers slowly)?  asym = (late third mean - early third mean) / box depth; > 0.5 reads "abrupt start, slow recovery". Box transit: about 0.
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, r"D:\second-sun\pipeline"); os.environ["SS_SET"] = "g2"; os.environ["VESPER_OPTS"] = "c6"
os.environ["NUMBA_NUM_THREADS"] = "1"
import numpy as np, pandas as pd
import stage3_report as R, detect_v2 as D
ev, meta = R.load(r"D:\second-sun\data\stage3_g2\sealed_5f73692944aa\groups")
E = ev[ev.primary].copy()
for c in ("snr", "dur_h", "depth_ppm", "center", "cover_pre", "cover_post"): E[c] = pd.to_numeric(E[c], errors="coerce")
E = E[E.snr >= 7]
m = meta.drop_duplicates(["tic", "sector", "product"]).set_index(["tic", "sector", "product"])
E["file"] = [m.file.get((a, b, c)) for a, b, c in zip(E.tic, E.sector, E["product"])]
E["cad"] = [m.cadence_min.get((a, b, c)) for a, b, c in zip(E.tic, E.sector, E["product"])]
E = E[(E.cad <= 3.4) & E.file.notna()]
T1 = ["1A", "1L", "1B"]
E["t1"] = E.tier.isin(T1); E["covmin"] = E[["cover_pre", "cover_post"]].min(axis=1)
rng = np.random.default_rng(3)
sel = {}
sel["flip tier-1"] = E[(E.kind == "flip") & E.t1]
sel["real tier-1"] = E[(E.kind == "real") & E.t1]
for k in ("flip", "real"):
    c = E[(E.kind == k) & ~E.t1 & (E.covmin >= 0.5) & (E.dur_h <= 6.5)]
    sel[f"{k} other, good coverage, box<=6.5 h"] = c.sample(min(len(c), 150), random_state=3)
print({k: len(v) for k, v in sel.items()}, "fast-cadence events:", len(E))
cache = {}


def shape(row):
    path = rf"D:\second-sun\data\g2\{row.tic}\{row.file}"
    if path not in cache:
        t, f, n = D.load(path); tt, ff = D.detrend(t, f); cache.clear(); cache[path] = (tt, ff)
    tt, ff = cache[path]
    g = ff if row.kind == "real" else 2.0 - ff
    d = row.dur_h / 24; c0 = row.center
    k = (tt > c0 - 1.5 * d) & (tt < c0 + 1.5 * d) & np.isfinite(g)
    t, g = tt[k], g[k]
    inbox = np.abs(t - c0) <= d / 2
    if inbox.sum() < 10:
        return None
    base = np.nanmedian(ff) if row.kind == "real" else 2.0 - np.nanmedian(ff)
    depth = base - np.mean(g[inbox])
    if not depth > 0:
        return None
    L = np.mean(g[(t >= c0 - d / 2) & (t < c0 - d / 6)]); Rr = np.mean(g[(t > c0 + d / 6) & (t <= c0 + d / 2)])
    sm = pd.Series(g[inbox]).rolling(5, center=True, min_periods=3).mean().values
    pk = (np.nanargmin(sm)) / max(inbox.sum() - 1, 1)
    return (Rr - L) / depth, pk, depth * 1e6


rows = []
for name, df in sel.items():
    df = df.sort_values(["tic", "file"])
    for r in df.itertuples():
        try:
            s = shape(r)
        except Exception as ex:
            s = None
        if s: rows.append((name, r.tic, r.sector, r.kind, r.dur_h, *s))
out = pd.DataFrame(rows, columns=["group", "tic", "sector", "kind", "dur_h", "asym", "peak", "depth_ppm"])
out.to_csv("q3_flare_shape_rows.csv", index=False)
print("group | n measured | asym median [IQR] | share asym>0.5 | peak position median | share peak<0.25 | median box h | median depth ppm")
for name, g in out.groupby("group"):
    print(f"{name} | {len(g)} | {g.asym.median():+.2f} [{g.asym.quantile(.25):+.2f}, {g.asym.quantile(.75):+.2f}] | {100*(g.asym>0.5).mean():.0f}% | {g.peak.median():.2f} | {100*(g.peak<0.25).mean():.0f}% | {g.dur_h.median()} | {g.depth_ppm.median():.0f}")
t1 = out[out.group.str.contains("tier-1")]
for k in ("flip", "real"):
    g = t1[t1.kind == k]
    print(f"tier-1 {k}: deep (>1%) n {int((g.depth_ppm>1e4).sum())}, asym>0.5 among deep {int(((g.depth_ppm>1e4)&(g.asym>0.5)).sum())}; shallow n {int((g.depth_ppm<=1e4).sum())}, asym>0.5 among shallow {int(((g.depth_ppm<=1e4)&(g.asym>0.5)).sum())}")
