import pandas as pd, numpy as np
FL = ["gap_dump", "flipmatch", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated"]
for lab, f in (("sealed", r"D:\second-sun\data\chain_recovery_g2\rows_sealed.pkl"), ("dev", r"D:\second-sun\data\chain_recovery_g2\rows_g2dev.pkl")):
    r = pd.read_pickle(f)
    r = r[r.K.notna() & (r.K >= 8) & (r.K <= 14) & r.error.isna()]
    print(f"== planted rows {lab}: {len(r)} (K 8 to 14), sign counts {r.sign.value_counts().to_dict()}")
    for sg, nm in ((1, "DIPS"), (-1, "BUMPS")):
        d = r[r.sign == sg]
        print(f"  {nm}: found at all {100*d.found_any.mean():.1f}%, found in the primary product {100*d.found_primary.mean():.1f}%, tier-1 {100*d.tier1.mean():.1f}%")
    d = r[r.sign == 1]
    print("  DIPS by duration: n, found_any%, tier1%")
    for dur, g in d.groupby("dur"):
        print(f"    {dur:>4} h  n {len(g):4d}  any {100*g.found_any.mean():5.1f}  primary {100*g.found_primary.mean():5.1f}  tier1 {100*g.tier1.mean():5.1f}")
    print("  DIPS by K: n, any, tier1")
    for k, g in d.groupby("K"):
        print(f"    K {k:>4}  n {len(g):4d}  any {100*g.found_any.mean():5.1f}  tier1 {100*g.tier1.mean():5.1f}")
    fa = d[d.found_any & ~d.tier1.astype(bool)]
    print(f"  found but NOT tier-1: {len(fa)} of {int(d.found_any.sum())} found; tier values {fa.tier.value_counts().to_dict()}")
    print("  among those, flag shares:", {f_: round(100 * fa[f_].fillna(False).astype(bool).mean(), 1) for f_ in FL + ["common"] if f_ in fa})
    print("  tier-1 fraction by tmag tercile (dips):", {str(q): round(100 * g.tier1.mean(), 1) for q, g in d.groupby(pd.qcut(d.tmag, 3))})
