# Q5/Q11/Q10 (31 Oct 2026): what does each safety check buy and cost, and what does the step check measure? Exploratory, after the scorecard; changes no result.
# Leave-one-check-out: for every check, drop it alone and count what would move to tier 1 among planted dips (completeness gain) and among sealed real / upside-down events (what comes with it).
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, r"D:\second-sun\pipeline"); os.environ["SS_SET"] = "g2"; os.environ["VESPER_OPTS"] = "c6"
import pandas as pd, numpy as np
import stage3_report as R, stage3_core as C
ev, meta = R.load(r"D:\second-sun\data\stage3_g2\sealed_5f73692944aa\groups")
E = R.pdc_half(ev[ev.primary]).copy()
for c in ("snr", "dur_h", "depth_ppm", "cover_pre", "cover_post", "lift_pre", "lift_post"):
    E[c] = pd.to_numeric(E[c], errors="coerce")
E = E[E.snr >= 7]
FL = ["gap_dump", "flipmatch", "c5", "ecl_overlap", "repeater", "orbit_lock", "step", "ramp", "dominated"]
T1 = ["1A", "1L", "1B"]
def b(x): return x.fillna(False).astype(bool)
for f in FL + ["common", "burst"]:
    if f in E: E[f] = E[f] if f in ("common",) else b(E[f])
def tier_without(row, drop):
    e = row.to_dict()
    for f in drop:
        if f == "common": e["common"] = 0; e["burst"] = False
        else: e[f] = False
    return C.tier_of(e)
base_real = int((E[E.kind == "real"].tier.isin(T1)).sum()); base_flip = int((E[E.kind == "flip"].tier.isin(T1)).sum())
print(f"sealed events SNR>=7 (primary PDC half): {len(E)}; tier 1 now: real {base_real}, flip {base_flip}")
P = pd.concat([pd.read_pickle(r"D:\second-sun\data\chain_recovery_g2\rows_sealed.pkl").assign(sl="sealed"), pd.read_pickle(r"D:\second-sun\data\chain_recovery_g2\rows_g2dev.pkl").assign(sl="dev")])
P = P[P.K.notna() & (P.K >= 8) & (P.K <= 14) & P.error.isna() & (P.sign == 1)]
for c in FL[:-1] + ["dominated", "common"]:
    if c in P: P[c] = b(P[c])
n_pl = len(P); t1 = P.tier1.astype(bool).mean() * 100
print(f"planted dips K 8-14 (both slices): {n_pl}, found {100*P.found_any.mean():.1f}%, tier 1 {t1:.1f}%\n")
print("check | planted: gain in tier-1 points if dropped alone (sealed / dev) | sealed events added to tier 1: real, upside-down | planted points per added upside-down event | share of ALL raw events carrying it: real, flip")
for f in FL + ["common"]:
    if f not in E or f not in P: continue
    gains = []
    for sl in ("sealed", "dev"):
        d = P[P.sl == sl]; lost = d[d.found_any & ~d.tier1.astype(bool) & (d.tier == "2")]
        only = lost[[x for x in FL if x in lost and x != "orbit_lock"] + ["common"]].copy()
        others = [x for x in only.columns if x != f]
        gains.append(100 * (only[f] & ~only[others].any(axis=1)).sum() / len(d))
    cand = E[(E.tier == "2") & E[f].astype(bool)] if f != "common" else E[(E.tier == "2") & (E.common.fillna(0) > 0)]
    add = {"real": 0, "flip": 0}
    for _, row in cand.iterrows():
        if tier_without(row, [f]) in T1: add[row.kind] += 1
    g = np.mean(gains)
    pr = f"{g/add['flip']:.2f}" if add["flip"] else "inf"
    sh = f"{100*E[E.kind=='real'][f].astype(bool).mean():.0f}%, {100*E[E.kind=='flip'][f].astype(bool).mean():.0f}%" if f != "common" else "-"
    print(f"{f:10s} | {gains[0]:+.1f} / {gains[1]:+.1f} | real +{add['real']}, flip +{add['flip']} | {pr} | {sh}")
# what the step check measures: its components, by box length and kind
print("\nstep check components on all raw events SNR>=7 (share of events): cover<0.5 on a side | a lift missing | |lift|>0.5 | step fired")
E["bx"] = pd.cut(E.dur_h, [0, 3.5, 7, 12, 25], labels=["3 h", "4-6.5 h", "8-12 h", "15-20 h"])
E["covlow"] = (E[["cover_pre", "cover_post"]].min(axis=1) < 0.5)
E["lnone"] = E.lift_pre.isna() | E.lift_post.isna()
E["lbig"] = ((E.lift_pre.abs() > 0.5) | (E.lift_post.abs() > 0.5))
for k in ("real", "flip"):
    for bx, g in E[E.kind == k].groupby("bx", observed=True):
        print(f"  {k:4s} {str(bx):8s} n {len(g):4d} | {100*g.covlow.mean():4.0f}% | {100*g.lnone.mean():4.0f}% | {100*g.lbig.mean():4.0f}% | {100*g.step.astype(bool).mean():4.0f}%")
print("lift size when measured, units of the dip depth (median |lift|, 75th, 90th pct) by SNR bin, flip events:")
for lo, hi in ((7, 8), (8, 10), (10, 15), (15, 1e9)):
    g = E[(E.snr >= lo) & (E.snr < hi)]; l = pd.concat([g.lift_pre.abs(), g.lift_post.abs()]).dropna()
    print(f"  SNR {lo}-{hi if hi<1e9 else '+'}: n {len(g)}, |lift| median {l.median():.2f}, p75 {l.quantile(.75):.2f}, p90 {l.quantile(.9):.2f}; step fired {100*g.step.astype(bool).mean():.0f}%")
# Q10: QLP-only stars
print("\nQ10: tier-1 by QLP-only star (sealed, bar 7):")
for q, g in E.groupby(E.qlp_only_star.astype(bool)):
    t = g[g.tier.isin(T1)]
    print(f"  QLP-only={q}: events real {int((g.kind=='real').sum())}, flip {int((g.kind=='flip').sum())}; tier-1 real {int((t.kind=='real').sum())}, flip {int((t.kind=='flip').sum())}; tier 1A real {int(((t.kind=='real')&(t.tier=='1A')).sum())}")
qp = P[P.sl == "sealed"]; print("  planted (sealed, K 8-14) tier-1 % by product:", {k: round(100 * v.tier1.astype(bool).mean(), 1) for k, v in qp.groupby("best")}, {k: len(v) for k, v in qp.groupby("best")})
# Q11: box share
t = E[E.tier.isin(T1)]
print("\nQ11: tier-1 events by box (real, flip):", {str(k): (int(((g.kind == 'real')).sum()), int((g.kind == 'flip').sum())) for k, g in t.groupby("bx", observed=True)})
