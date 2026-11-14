"""T129: N_eff check of the Re-search 1 null (counts only; fence B allows re-deriving the Re-search 1 counts from existing files; no search,
no event time printed). Question: the S1 test (r1_readout.strat_block, hypergeometric per bin) treats tier-1 events as independent. Events cluster
on stars. How large is the design effect, does the verdict change, and how much weaker is the power line once stars, not events, are the unit?
Method (independent of r1_readout's maths, reusing only its loaders): (1) per-star counts of real and upside-down tier-1 events in recovered
light, PDCSAP half, bar 7, exactly the selection of r1_readout.t1_counts; (2) deff of the real share = variance of the star-cluster bootstrap
share over the binomial variance at the same N; (3) a star-cluster version of the S1 chance: the sealed real share against the fixed seen-star
reference share, with the sealed share's spread from the star bootstrap; (4) the power line with N_eff = N / deff.
Run from pipeline/: SS_SET=g2 SS_RUN=r1_g2_unseen_bcd29c7aabb0 VESPER_OPTS=c6,p1 python this.py  (and the g3 run)."""
import os, sys, json
from pathlib import Path
sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
from scipy.stats import fisher_exact, norm
import stage3_core as C, stage3_report as R
import r1_readout as RO

name, run = C.DS.NAME, os.environ["SS_RUN"]
folder = C.DS.RUNS / run
ev, meta = R.load(str(folder / "groups"))
E = ev[ev.primary].copy(); E["rec"] = E.recovered.fillna(False).astype(bool)
t1 = E[E.rec & E.tier.isin(RO.T1)]
r, f = R.pdc_half(t1[t1.kind == "real"]), R.pdc_half(t1[t1.kind == "flip"])
ref = RO.ref_counts()
out = {}
rng = np.random.default_rng(20261114)
for bar in RO.BARS:
    rb, fb = r[r.snr >= bar], f[f.snr >= bar]
    stars = sorted(set(rb.tic) | set(fb.tic))
    cr = rb.groupby("tic").size().reindex(stars, fill_value=0).values; cf = fb.groupby("tic").size().reindex(stars, fill_value=0).values
    Rn, Fn = int(cr.sum()), int(cf.sum()); N = Rn + Fn
    rr, fr = ref[(name, "recovered", bar)]
    share_ref = rr / (rr + fr)
    if N == 0 or len(stars) < 2:
        out[bar] = dict(real=Rn, flip=Fn, stars=len(stars), note="too few"); continue
    share = Rn / N
    B = 20000; idx = rng.integers(0, len(stars), size=(B, len(stars)))
    br, bn = cr[idx].sum(1), (cr + cf)[idx].sum(1)
    ok = bn > 0; bs = br[ok] / bn[ok]
    var_boot = float(np.var(bs)); var_bin = share * (1 - share) / N
    deff = var_boot / var_bin if var_bin > 0 else float("nan")
    # star-cluster chance that the sealed real share exceeds the reference share by this much (normal on the bootstrap spread; reference treated as fixed, as in S1)
    z = (share - share_ref) / np.sqrt(var_boot) if var_boot > 0 else float("nan")
    p_cluster = float(norm.sf(z))
    p_event = float(fisher_exact([[Rn, Fn], [rr, fr]], alternative="greater")[1])
    # power: the smallest real count the event-level Fisher calls an excess at ALPHA, then the same with N_eff = N / deff (scaled counts)
    def need(scale):
        fs = max(int(round(Fn / scale)), 1)
        for Rt in range(1, 100000):
            if fisher_exact([[Rt, fs], [rr, fr]], alternative="greater")[1] <= RO.ALPHA:
                return Rt * scale / (fs * scale * rr / fr)
        return float("nan")
    out[bar] = dict(real=Rn, flip=Fn, stars=len(stars), stars_real=int((cr > 0).sum()), stars_flip=int((cf > 0).sum()),
                    max_events_one_star=int((cr + cf).max()), share=round(share, 3), share_ref=round(share_ref, 3), deff=round(deff, 2),
                    n_eff=round(N / deff, 1) if deff == deff and deff > 0 else None, p_event_unstratified=round(p_event, 4), p_cluster_unstratified=round(p_cluster, 4),
                    power_times_expected_event=round(need(1.0), 2), power_times_expected_cluster=round(need(max(deff, 1.0)), 2))
res = dict(list=name, run=run, note="counts only; unstratified versions (the verdict test is stratified by bin; deff is the point here)", bars=out)
Path(r"D:\second-sun\research\stage3\t129").mkdir(exist_ok=True)
Path(rf"D:\second-sun\research\stage3\t129\t129-{name}.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res, indent=1))
