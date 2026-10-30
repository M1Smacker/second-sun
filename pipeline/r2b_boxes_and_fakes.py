"""Vesper study R2b: (1) which box length do tier-1 false alarms and tier-1 recovered fakes sit in? (2) the near-miss control: the same 'just inside a flag threshold' test on tier-1 recovered fakes.
Fakes = injected dips (sign 1) of K 8 to 14 found as primary events (paired_feat.pkl). Aggregates only. Usage: python r2b_boxes_and_fakes.py (writes research/stage3/r2b-boxes.txt)"""
import numpy as np, pandas as pd
import score_c4 as S4

out = []
for name in ("g1", "g2"):
    A = S4.load(name); P = A["P"]; Pf = A["Pf"]
    t1 = Pf[P.loc[Pf.index, "tier1_b"].astype(bool)]
    out.append(f"{name}: injected dips (K 8 to 14) {len(P)}; found as primary {len(Pf)}; tier-1 in the baseline run {int(P.tier1_b.astype(bool).sum())}")
    out.append("   tier-1 fakes by the box length of the event that was found (rows) and the injected box (columns 4, 8, 14, 20 h):")
    ct = pd.crosstab(pd.to_numeric(t1.ev_dur_h), t1.dur)
    for d, r in ct.iterrows():
        out.append(f"      found at {d:>4} h: " + ", ".join(f"inj {int(c)} h: {int(v)}" for c, v in r.items()))
    share3 = (pd.to_numeric(t1.ev_dur_h) == 3).mean(); out.append(f"   share of tier-1 fakes found at the 3 h box: {100 * share3:.1f}% (upper bound on the loss if the 3 h box is dropped; the next-best box would often still find them)")
    g = lambda c: pd.to_numeric(t1["ev_" + c], errors="coerce")
    lift = np.maximum(g("lift_pre").abs().fillna(0), g("lift_post").abs().fillna(0)); cover = np.minimum(g("cover_pre").fillna(1), g("cover_post").fillna(1))
    near = pd.DataFrame({"step lift 0.25 to 0.5": (lift >= 0.25) & (lift < 0.5), "side cover 0.5 to 0.75": (cover >= 0.5) & (cover < 0.75), "ramp distance 1 to 2 d": (g("ramp_d") >= 1.0) & (g("ramp_d") < 2.0),
                         "eclipse phase 0.35 to 0.7 d": (g("ph_d") >= 0.35) & (g("ph_d") < 0.7), "repeat count 2": g("repeat_n") == 2, "common count 2": g("common_n") == 2})
    out.append(f"   control, tier-1 fakes near a threshold: " + ", ".join(f"{c} {100 * near[c].mean():.0f}%" for c in near.columns) + f"; near at least one {100 * near.any(axis=1).mean():.0f}% of {len(t1)} (survivors: see r2-survivors.txt)")
print("\n".join(out)); open("../research/stage3/r2b-boxes.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
