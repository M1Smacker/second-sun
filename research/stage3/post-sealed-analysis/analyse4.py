import os, sys
run, opts, nstars, ratio = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
sys.path.insert(0, r"D:\second-sun\pipeline")
os.environ["SS_SET"] = "g2"
if opts != "none":
    os.environ["VESPER_OPTS"] = opts
import pandas as pd, numpy as np
import stage3_report as R
ev, meta = R.load(rf"D:\second-sun\data\stage3_g2\{run}\groups")
E = R.pdc_half(ev[ev.primary]).copy()
E["depth_ppm"] = pd.to_numeric(E.depth_ppm, errors="coerce"); E["dur_h"] = pd.to_numeric(E.dur_h, errors="coerce"); E["snr"] = pd.to_numeric(E.snr, errors="coerce")
T1 = ["1A", "1L", "1B"]
t = E[E.tier.isin(T1)]
real = t[t.kind == "real"].groupby("tic").size(); flip = t[t.kind == "flip"].groupby("tic").size()
stars = sorted(set(E.tic))                      # stars with any event; pad with zero-event stars up to nstars
r = np.array([real.get(s, 0) for s in stars] + [0] * (nstars - len(stars))); f = np.array([flip.get(s, 0) for s in stars] + [0] * (nstars - len(stars)))
rng = np.random.default_rng(1); B = 20000
idx = rng.integers(0, nstars, (B, nstars))
dr, df = r[idx].sum(1), f[idx].sum(1)
exc = dr - df / ratio
print(f"== {run} options={opts}: stars in slice {nstars}; tier-1 real {r.sum()} events on {(r>0).sum()} stars; flip {f.sum()} on {(f>0).sum()} stars; noise-expected real {f.sum()/ratio:.1f} (ratio {ratio})")
print(f"   cluster bootstrap over stars (20,000 draws): real minus expected = {r.sum()-f.sum()/ratio:+.1f}, 95% interval {np.percentile(exc,2.5):+.1f} to {np.percentile(exc,97.5):+.1f}; share of draws with real <= expected {100*(exc<=0).mean():.1f}%")
print(f"   stars with a real tier-1 event {(r>0).sum()} vs stars with an upside-down one {(f>0).sum()} (ratio-free, per-star view)")
tr = t[t.kind == "real"]; tf = t[t.kind == "flip"]
for nm, x in (("real", tr), ("flip", tf)):
    if len(x):
        print(f"   tier-1 {nm}: depth ppm quantiles {x.depth_ppm.quantile([0,.25,.5,.75,1]).round().tolist()}; durations {x.dur_h.value_counts().sort_index().to_dict()}; deeper than 1%: {int((x.depth_ppm>10000).sum())}")
