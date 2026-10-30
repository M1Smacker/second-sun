import os, sys
run, opts = sys.argv[1], sys.argv[2]
sys.path.insert(0, r"D:\second-sun\pipeline")
os.environ["SS_SET"] = "g2"
if opts != "none":
    os.environ["VESPER_OPTS"] = opts
import pandas as pd, numpy as np
import stage3_report as R
ev, meta = R.load(rf"D:\second-sun\data\stage3_g2\{run}\groups")
E = R.pdc_half(ev[ev.primary])
T1 = ["1A", "1L", "1B"]
print(f"== {run} options={opts}: primary PDCSAP-half events {len(E)}; star-sectors in meta {meta[['tic','sector']].drop_duplicates().shape[0]}; stars {E.tic.nunique()}")
FL = ["gap_dump", "flipmatch", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated", "orbit_lock"]


def clus(X, name):
    n = len(X)
    if not n:
        print(f"  {name}: 0"); return
    c = X.groupby("tic").size().sort_values(ascending=False)
    print(f"  {name}: {n} events on {len(c)} stars; max per star {c.iloc[0]}; top3 stars hold {c.iloc[:3].sum()} ({100*c.iloc[:3].sum()/n:.0f}%); top10 hold {c.iloc[:10].sum()} ({100*c.iloc[:10].sum()/n:.0f}%)")


for k in ("real", "flip"):
    clus(E[E.kind == k], f"all events SNR>=7 {k}")
for k in ("real", "flip"):
    clus(E[(E.kind == k) & E.tier.isin(T1)], f"tier-1 {k}")
for k in ("real", "flip"):
    clus(E[(E.kind == k) & (E.tier == "1A")], f"tier-1A {k}")
print("  flag shares among ALL events (a flag can overlap others), real vs flip:")
for f in FL:
    if f in E:
        a = E[E.kind == "real"][f].fillna(False).astype(bool).mean() * 100; b = E[E.kind == "flip"][f].fillna(False).astype(bool).mean() * 100
        print(f"    {f:11s} real {a:5.1f}%  flip {b:5.1f}%")
print("  tier split real/flip:", E[E.kind == "real"].tier.value_counts().to_dict(), E[E.kind == "flip"].tier.value_counts().to_dict())
t1r = E[(E.kind == "real") & E.tier.isin(T1)]
if len(t1r):
    print("  tier-1 real depth_ppm quantiles", t1r.depth_ppm.quantile([0, .25, .5, .75, 1]).round().tolist(), "durations", t1r.dur_h.value_counts().sort_index().to_dict(), "snr", t1r.snr.quantile([0, .5, 1]).round(1).tolist())
    print("  tier-1 real deeper than 1%:", int((t1r.depth_ppm > 10000).sum()), "deeper than 0.3%:", int((t1r.depth_ppm > 3000).sum()))
t1f = E[(E.kind == "flip") & E.tier.isin(T1)]
if len(t1f):
    print("  tier-1 flip depth_ppm quantiles", t1f.depth_ppm.quantile([0, .25, .5, .75, 1]).round().tolist(), "durations", t1f.dur_h.value_counts().sort_index().to_dict())
print("  QLP-only stars among tier-1 real/flip:", int(t1r.qlp_only_star.sum()) if len(t1r) else 0, int(t1f.qlp_only_star.sum()) if len(t1f) else 0)
