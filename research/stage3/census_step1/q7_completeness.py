"""RS-010 Q7 (night of 4 Nov 2026): what limits G3 completeness for a TOI-1338 b-size dip (2,300 ppm)? Own data only (G3 planted dips, 300 star-sectors x boxes); nothing changes."""
import pandas as pd, numpy as np
d = pd.read_pickle(r"D:\second-sun\data\chain_recovery_g3\rows_g3.pkl")
d = d[d.K.notna() & (d.sign == 1)].copy()
P = print
P(f"planted dips (sign +1, with a prepared product): {len(d)}; star-sectors {d.groupby(['tic','sector']).ngroups}; depth_ppm quantiles 10/50/90: {d.depth_ppm.quantile([.1,.5,.9]).round(0).tolist()}; K quantiles: {d.K.quantile([.1,.5,.9]).round(1).tolist()}")
d["seen"] = d.found_any.astype(bool); d["kept"] = d.tier1.astype(bool)
P(f"overall: seen {100*d.seen.mean():.0f}%, kept in tier 1 {100*d.kept.mean():.0f}%")
P("\nBy K (depth over the 8 h box noise): share seen / kept / kept-given-seen")
for lo, hi in ((0, 6), (6, 8), (8, 10), (10, 12), (12, 14), (14, 18), (18, 99)):
    g = d[(d.K >= lo) & (d.K < hi)]
    if len(g) > 20: P(f"  K {lo}-{hi}: n {len(g):5d}; seen {100*g.seen.mean():3.0f}%; kept {100*g.kept.mean():3.0f}%; kept given seen {100*g[g.seen].kept.mean():3.0f}%")
P("\nDips with depth 1,500 to 3,500 ppm (TOI-1338 b is 2,300 ppm as seen): by star brightness (Tmag)")
t = d[(d.depth_ppm >= 1500) & (d.depth_ppm <= 3500) & d.tmag.notna()]
P(f"  n {len(t)}; median K {t.K.median():.1f}; median noise {t.n8.median():.0f} ppm")
for lo, hi in ((0, 11.5), (11.5, 12.5), (12.5, 13.0), (13.0, 99)):
    g = t[(t.tmag >= lo) & (t.tmag < hi)]
    if len(g) > 15: P(f"  Tmag {lo}-{hi}: n {len(g):4d}; median noise {g.n8.median():5.0f} ppm; median K {g.K.median():4.1f}; seen {100*g.seen.mean():3.0f}%; kept {100*g.kept.mean():3.0f}%")
P("\nWhy seen dips are lost (flags set on seen-but-not-kept planted dips, any depth with K 8 to 14; a dip can carry several):")
s = d[(d.K >= 8) & (d.K < 14) & d.seen & ~d.kept]
flags = ["gap_dump", "flipmatch", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated", "common", "asym", "too_deep", "flare"]
P(f"  n {len(s)} of {len(d[(d.K>=8)&(d.K<14)&d.seen])} seen dips with K 8 to 14 are not kept")
for f in flags:
    if f in s: P(f"   {f:11s}: {100*s[f].astype(float).fillna(0).gt(0).mean():3.0f}%")
P("\nBy product family (best): kept share at K 8 to 14: " + "; ".join(f"{b}: {100*g.kept.mean():.0f}% (n {len(g)})" for b, g in d[(d.K >= 8) & (d.K < 14)].groupby("best")))
P("\nBy box length (dur, h) at K 8 to 14: " + "; ".join(f"{b}: seen {100*g.seen.mean():.0f}%, kept {100*g.kept.mean():.0f}%" for b, g in d[(d.K >= 8) & (d.K < 14)].groupby("dur")))
