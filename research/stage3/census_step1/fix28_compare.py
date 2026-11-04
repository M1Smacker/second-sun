"""FIX 28: compare completeness for four injected shapes (G3, 300 star-sectors, same seeds). Paired by (tic, sector, dur, K, sign=+1). Aggregates only.
Inputs: data/chain_recovery_g3/rows_g3.pkl (official run) and rows_shape_{sym,skew,stretch,box}.pkl."""
import numpy as np, pandas as pd
D = r"D:\second-sun\data\chain_recovery_g3"
def load(name):
    d = pd.read_pickle(f"{D}\\rows_{name}.pkl")
    d = d[d.K.notna() & (d.sign == 1)].copy()
    d["tier1"] = d.tier1.astype(bool); d["seen"] = d.found_any.astype(bool)
    return d.set_index(["tic", "sector", "dur", "K"])
P = print
base = load("g3")
shapes = ["sym", "skew", "stretch", "box"]
rows = {s: load("shape_" + s) for s in shapes}
P(f"official rows_g3 (+1 signs with K): {len(base)}; shape rows: " + ", ".join(f"{s} {len(r)}" for s, r in rows.items()))
j = base[["tier1", "seen"]].join(rows["sym"][["tier1", "seen"]], rsuffix="_sym", how="inner")
P(f"\nIDENTITY CHECK, official vs the sym variant on {len(j)} matching injections: tier1 identical in {100*(j.tier1==j.tier1_sym).mean():.1f}%, seen identical in {100*(j.seen==j.seen_sym).mean():.1f}%; kept share {100*j.tier1.mean():.1f}% vs {100*j.tier1_sym.mean():.1f}%")
def rate(d, lo=8, hi=14):
    g = d[(d.index.get_level_values("K") >= lo) & (d.index.get_level_values("K") < hi)]
    return g.tier1.mean(), g.seen.mean(), len(g)
P("\nPAIRED COMPARISON, K 8 to 14 pooled (share kept in tier 1 / share seen), difference against sym with a star-sector bootstrap 95% interval")
common = rows["sym"].index
rng = np.random.default_rng(7)
keys = common.droplevel(["dur", "K"]).unique()
for s in shapes:
    r = rows[s].reindex(common)
    k = (r.index.get_level_values("K") >= 8) & (r.index.get_level_values("K") < 14)
    a, b = rows["sym"][k.tolist() if False else k], r[k]
    ok = a.tier1.notna().values & b.tier1.notna().values
    t0, t1 = a.tier1.values[ok].astype(float), b.tier1.values[ok].astype(float)
    ss = np.array([f"{x[0]}_{x[1]}" for x in a.index[ok]]); u = np.unique(ss); idx = {x: np.where(ss == x)[0] for x in u}
    diffs = []
    for _ in range(400):
        pick = rng.choice(u, len(u)); ii = np.concatenate([idx[x] for x in pick]); diffs.append(t1[ii].mean() - t0[ii].mean())
    P(f"  {s:8s}: kept {100*t1.mean():5.1f}% (sym {100*t0.mean():5.1f}%), difference {100*(t1.mean()-t0.mean()):+5.1f} points (95% {100*np.percentile(diffs,2.5):+.1f} to {100*np.percentile(diffs,97.5):+.1f}); n {ok.sum()}")
P("\nBY DURATION (kept share, K 8 to 14)")
for dur in (4.0, 8.0, 14.0, 20.0):
    line = []
    for s in shapes:
        r = rows[s]; g = r[(r.index.get_level_values("dur") == dur) & (r.index.get_level_values("K") >= 8) & (r.index.get_level_values("K") < 14)]
        line.append(f"{s} {100*g.tier1.mean():4.1f}%")
    P(f"  {dur:4.0f} h box: " + "; ".join(line))
P("\nBY K (kept share, all durations)")
for K in (8.0, 10.0, 12.0, 14.0):
    line = []
    for s in shapes:
        r = rows[s]; g = r[r.index.get_level_values("K") == K]
        line.append(f"{s} {100*g.tier1.mean():4.1f}%")
    P(f"  K {K:4.0f}: " + "; ".join(line))
