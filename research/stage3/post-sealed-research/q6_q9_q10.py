# Q6 (cross-sector events), Q9 (heavy stars), Q10 (QLP-only stars). 31 Oct 2026, exploratory, sealed run with c6.
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, r"D:\second-sun\pipeline"); os.environ["SS_SET"] = "g2"; os.environ["VESPER_OPTS"] = "c6"
import numpy as np, pandas as pd
import stage3_report as R, stage3_core as C
ev, meta = R.load(r"D:\second-sun\data\stage3_g2\sealed_5f73692944aa\groups")
E = R.pdc_half(ev[ev.primary]).copy(); E["snr"] = pd.to_numeric(E.snr, errors="coerce"); E = E[E.snr >= 7]
T1 = ["1A", "1L", "1B"]; E["t1"] = E.tier.isin(T1)
# Q10
prods = meta[meta.status == "ok"].groupby("tic")["product"].agg(lambda s: set(s))
qonly = {t for t, s in prods.items() if s <= {"QLP"}}
print(f"Q10: stars {len(prods)}; QLP-only stars (all their ok products are QLP): {len(qonly)} ({100*len(qonly)/len(prods):.0f}%)")
E["qonly"] = E.tic.isin(qonly)
for q, g in E.groupby("qonly"):
    t = g[g.t1]
    print(f"   QLP-only={q}: stars with events {g.tic.nunique()}; raw events real {int((g.kind=='real').sum())}, flip {int((g.kind=='flip').sum())}; tier-1 real {int(((t.kind=='real')).sum())} flip {int((t.kind=='flip').sum())}; per 100 stars tier-1 real {100*(t.kind=='real').sum()/max(g.tic.nunique(),1):.1f}, flip {100*(t.kind=='flip').sum()/max(g.tic.nunique(),1):.1f}")
# Q9
tot = E.groupby("tic").size().sort_values(ascending=False)
ep = C.Ephem(pd.read_csv(C.TARGETS, comment="#"), C.eb_widths())
print("\nQ9: 12 heaviest stars by raw events (real, flip, tier-1 real, tier-1 flip, binary period d if known, orbit_lock events):")
for tic in tot.index[:12]:
    g = E[E.tic == tic]; per = [round(p, 2) for _, p, _ in ep.by.get(int(tic), [])][:2]
    print(f"   {int(tic)}: {len(g)} events (real {int((g.kind=='real').sum())}, flip {int((g.kind=='flip').sum())}); t1 real {int(((g.kind=='real')&g.t1).sum())}, t1 flip {int(((g.kind=='flip')&g.t1).sum())}; P {per}; orbit_lock {int(g.orbit_lock.astype(bool).sum()) if 'orbit_lock' in g else 'n/a'}")
heavy = set(tot.index[:25]); h = E[E.tic.isin(heavy)]; o = E[~E.tic.isin(heavy)]
print(f"   25 heaviest stars: raw real {int((h.kind=='real').sum())} flip {int((h.kind=='flip').sum())} (ratio {((h.kind=='flip').sum()/(h.kind=='real').sum()):.2f}); the other {o.tic.nunique()} stars: real {int((o.kind=='real').sum())} flip {int((o.kind=='flip').sum())} (ratio {((o.kind=='flip').sum()/(o.kind=='real').sum()):.2f}); heavy stars with a known binary period: {sum(1 for t in heavy if ep.by.get(int(t)))} of 25")
# Q6
t1r = E[E.t1 & (E.kind == "real")]
g = t1r.groupby("tic").sector.nunique(); multi = g[g >= 2].index
print(f"\nQ6: stars with tier-1 real events in 2+ sectors: {len(multi)}")
for tic in multi:
    x = t1r[t1r.tic == tic].sort_values("center")
    per = [round(p, 2) for _, p, _ in ep.by.get(int(tic), [])][:2]
    print(f"   {int(tic)}: sectors {sorted(set(x.sector))}, events {len(x)}, centre gaps (d) {np.round(np.diff(x.center.values), 1).tolist()[:6]}, box h {sorted(set(x.dur_h))}, P_binary {per}, orbit_lock events {int(x.orbit_lock.astype(bool).sum()) if 'orbit_lock' in x else 'n/a'}")
