"""Vesper study: sensitivity at a FIXED false-alarm budget (the yardstick). The SNR bar of an option is the lowest bar (grid 0.25) at which upside-down tier-1 per 1,000 star-sectors is 8 or fewer.
  python bar_budget.py bar <run folder>                                  (SS_SET as for fa_count.py; prints the lowest bar that meets the budget)
  python bar_budget.py pair <baseline rows.pkl> <label> <bar>            (paired comparison, option tier 1 also needs snr >= bar; baseline unchanged at 7; appends to research\stage3\paired-bar.txt)"""
import sys
import numpy as np, pandas as pd
from scipy.stats import binomtest
import stage3_core as C, stage3_report as R, chain_recovery as X

T1 = ["1A", "1L", "1B"]
if sys.argv[1] == "bar":
    ev, meta = R.load(str(C.DS.RUNS / sys.argv[2] / "groups"))
    n = len(meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"]))
    E = ev[ev.primary]; f = E[(E.kind == "flip") & E.tier.isin(T1)]; r = E[(E.kind == "real") & E.tier.isin(T1)]
    for b in np.arange(7, 14.01, 0.25):
        rate = 1000 * (f.snr >= b).sum() / n
        if rate <= 8:
            print(f"{C.DS.NAME} {sys.argv[2]}: lowest bar {b:.2f}: upside-down {(f.snr >= b).sum()} ({rate:.2f} per 1,000), real tier-1 {(r.snr >= b).sum()}"); break
else:
    base, label, bar = sys.argv[2], sys.argv[3], float(sys.argv[4])
    b = pd.read_pickle(base); b = b[b["error"].isna()] if "error" in b else b
    b = b[b.K.isin((8., 10., 12., 14.)) & b.sign.notna() & b.tc.notna()].copy(); b["t1_base"] = b.tier.isin(T1)
    o = pd.read_pickle(X.PREP / f"paired_{label}.pkl"); o = o[o["error"].isna()] if "error" in o else o
    o["t1_opt"] = o.tier.isin(T1) & (o.snr >= bar)
    m = b.merge(o[["tic", "sector", "dur", "K", "sign", "t1_opt"]], on=["tic", "sector", "dur", "K", "sign"])
    txt = [f"{C.DS.NAME} option {label} at bar {bar:.2f} (upside-down budget 8 per 1,000), paired against baseline 0.7.1 at bar 7; {len(m)} injections"]
    d = m[m.sign == 1]
    for name, sel in (("4 h", d.dur == 4.0), ("8 h", d.dur == 8.0), ("14 and 20 h", d.dur >= 14.0), ("all boxes", d.dur > 0)):
        g = d[sel]; gain, lost = int((g.t1_opt & ~g.t1_base).sum()), int((~g.t1_opt & g.t1_base).sum())
        p = binomtest(gain, gain + lost, 0.5).pvalue if gain + lost else 1.0
        txt.append(f"DIPS {name}: base {100 * g.t1_base.mean():.1f}% option {100 * g.t1_opt.mean():.1f}%; gained {gain}, lost {lost}, net {gain - lost:+d}, exact p {p:.5f}")
    dp, bp = m[m.sign == 1].t1_opt.mean(), m[m.sign == -1].t1_opt.mean()
    txt.append(f"Mirror: option dip {100 * dp:.1f}% vs bump {100 * bp:.1f}% (gap {100 * (bp - dp):+.1f}; rule within 3)")
    print("\n".join(txt))
    with open(C.ROOT / "research" / "stage3" / "paired-bar.txt", "a", encoding="utf-8") as fh:
        fh.write("\n".join(txt) + "\n")
