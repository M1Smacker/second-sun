"""Vesper study C4-lite: which flag PATTERNS could pass as tier 1 at the same false-alarm budget? The 9 yes/no flags plus "second product disagrees" make a pattern per event. Patterns are ranked by
(share of injected dips that carry it) over (upside-down events per 1,000 star-sectors that carry it) and added, best first, until the upside-down tier-1 rate reaches the budget (8 per 1,000).
Trained on one set, scored on the other (both ways); a pattern needs 10 or more injected dips in the training set. Positives: injected dips K 8 to 14 from the chain_recovery rows (baseline 0.7.1).
Usage: python flag_patterns.py   (aggregates only; appends to research\stage3\flag-patterns.txt)"""
import os
import numpy as np, pandas as pd
from scipy.stats import binomtest
import dataset as DS

FL = ["gap_dump", "flipmatch", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated", "common"]
SETS = {"g1": ("fd788be04650", "../data/chain_recovery/rows_v7.pkl"), "g2": ("dev_73f62615e365", "../data/chain_recovery_g2/rows_g2dev.pkl")}
BUDGET, MIN_F, NAMES = 8.0, 10, FL + ["tier3"]
LAST = {}


def load(name):
    os.environ["SS_SET"] = name
    import importlib; importlib.reload(DS)
    import stage3_core as C, stage3_report as R
    importlib.reload(C); importlib.reload(R)
    run, rows = SETS[name]
    ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
    n = len(meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"]))
    E = ev[ev.primary & (ev.kind == "flip") & (ev.snr >= 7)].copy()
    E["t3"] = E.tier == "3"; LAST[name] = E.snr.values      # SNR of the upside-down events, same order as `flips` (used by snr_waiver.py)
    flips = [tuple(bool(x) for x in r) for r in E[FL + ["t3"]].values]
    b = pd.read_pickle(rows); b = b[b["error"].isna()] if "error" in b else b
    b = b[b.K.isin((8., 10., 12., 14.)) & (b.sign == 1) & b.tc.notna()].copy()
    b["found"] = b.tier.astype(str).str.len() > 0
    b["t3"] = b.tier == "3"
    b["pat"] = [tuple(bool(x) for x in r) if f else None for r, f in zip(b[FL + ["t3"]].values, b.found)]
    return n, flips, b


def choose(n, flips, b):
    nf, nn = b.pat.dropna().value_counts().to_dict(), pd.Series(flips).value_counts().to_dict()
    rank = sorted([p for p in nf if nf[p] >= MIN_F], key=lambda p: -(nf[p] / len(b)) / ((nn.get(p, 0) + 0.5) / n))
    keep, used = [], 0
    for p in rank:
        if used + nn.get(p, 0) > BUDGET * n / 1000:
            continue
        keep.append(p); used += nn.get(p, 0)
    return keep


def score(keep, n, flips, b, label):
    k = set(keep); fl = sum(p in k for p in flips)
    b = b.assign(opt=[p in k for p in b.pat], base=b.tier.isin(["1A", "1L", "1B"]))
    out = [f"{label}: {len(keep)} patterns pass; upside-down tier-1 {fl} = {1000 * fl / n:.2f} per 1,000 star-sectors (baseline rule: clean pattern only)"]
    for nm, sel in (("4 h", b.dur == 4), ("8 h", b.dur == 8), ("14 and 20 h", b.dur >= 14), ("all boxes", b.dur > 0)):
        g = b[sel]; ga, lo = int((g.opt & ~g.base).sum()), int((~g.opt & g.base).sum())
        p = binomtest(ga, ga + lo, 0.5).pvalue if ga + lo else 1.0
        out.append(f"   dips {nm}: base {100 * g.base.mean():.1f}% option {100 * g.opt.mean():.1f}%; gained {ga}, lost {lo}, net {ga - lo:+d}, exact p {p:.5f}")
    return out


def main():
    D = {s: load(s) for s in SETS}
    txt = []
    for tr, te in (("g1", "g2"), ("g2", "g1"), ("g1", "g1"), ("g2", "g2")):
        keep = choose(*D[tr])
        if tr != te or True:
            txt += score(keep, *D[te], f"train {tr} -> score {te}" + (" (IN-SAMPLE)" if tr == te else ""))
        if tr == "g1" and te == "g2":
            txt.append("   patterns kept (train g1): " + "; ".join("+".join(n for n, v in zip(NAMES, p) if v) or "clean" for p in keep))
        if tr == "g2" and te == "g1":
            txt.append("   patterns kept (train g2): " + "; ".join("+".join(n for n, v in zip(NAMES, p) if v) or "clean" for p in keep))
    print("\n".join(txt))
    open("../research/stage3/flag-patterns.txt", "a", encoding="utf-8").write("\n".join(txt) + "\n")


if __name__ == "__main__":
    main()
