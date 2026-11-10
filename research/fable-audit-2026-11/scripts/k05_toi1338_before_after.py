"""K-05: Chapter 9 check. TOI-1338 (public star) own 40 SPOC 2-min files, dips injected BEFORE vs AFTER the frozen mask (same code as wo_f01a_mask_loss.py). Counts only."""
import os, sys; os.environ.setdefault("SS_SET", "g2")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glob, numpy as np, pandas as pd
import wo_f01a_mask_loss as W
W.init()
paths = sorted(glob.glob(r"D:\second-sun\data\g2\260128333\tess*_lc.fits"))
rows = []
for i, p in enumerate(paths):
    rows += W.run_file((p, 260128333, 14.6086, "SPOCfam", 14, i))
df = pd.DataFrame(rows)
print("files", len(paths), "with injections", df[df.K.notna()].file.nunique() if "K" in df else 0, "skips", int(df.skip.notna().sum()) if "skip" in df else 0)
d = df[df.K.notna() & (df.sign == 1)]
print("dips, TOI-1338 (P 14.6 d, bin 14-20): found before the mask / after the mask / share of dip cadences cut, n files per cell")
for K in sorted(d.K.unique()):
    for dur in sorted(d.dur.unique()):
        g = d[(d.K == K) & (d.dur == dur)]
        print(f"  K {K:4g} dur {dur:4g} h: {g.found_before.mean():.2f} / {g.found_after.mean():.2f} / cut {g.cut.mean():.2f}  n {len(g)}")
g = d[d.K.isin((12.0, 18.0, 25.0))]
print(f"  K 12/18/25 all durations pooled: {g.found_before.mean():.2f} / {g.found_after.mean():.2f}  (m = {g.found_before.mean() / g.found_after.mean():.2f})")
b = df[df.K.notna() & (df.sign == -1)]
print("bumps (proof):", f"{b.found_before.mean():.2f} / {b.found_after.mean():.2f}")
