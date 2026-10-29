"""Vesper study C4: one calibrated planet-likeness score instead of nine yes/no flags (VESPER-STUDY-PLAN.md designs). Positives: injected dips (K 8 to 14) found as primary events, from paired_feat.pkl;
negatives: upside-down primary events of the full baseline runs. Trained on SNR 7 to 10 only (both classes, so SNR does not carry the score), on one set, scored on the other (both ways).
Operating point: the score cut that gives 8 upside-down tier-1 per 1,000 star-sectors on the TRAINING set (5-fold out-of-fold scores, folds by star). Second-product disagreement (tier 3) and SAP-only events keep their old rule.
Models: logistic regression (readable weights) and gradient boosting (a ceiling check: if it cannot beat the flags, nothing from these numbers can). Usage: python score_c4.py   (aggregates only; appends to research\stage3\score-c4.txt)"""
import os
import numpy as np, pandas as pd
from scipy.stats import binomtest
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold
import dataset as DS

SETS = {"g1": ("fd788be04650", "../data/chain_recovery/paired_feat.pkl", "../data/chain_recovery/rows_v7.pkl"),
        "g2": ("dev_73f62615e365", "../data/chain_recovery_g2/paired_feat.pkl", "../data/chain_recovery_g2/rows_g2dev.pkl")}
BOOL = ["gap_dump", "flipmatch", "dominated"]
NUM = ["dur_h", "lift_pre", "lift_post", "cover_pre", "cover_post", "ramp_d", "ecl_d", "ecl_w", "burst_n", "common_n", "repeat_n", "ph_d", "c8_n"]
BUDGET = 8.0


def feats(d, pre=""):
    X = pd.DataFrame(index=d.index)
    for c in BOOL:
        X[c] = d[c].astype(float)
    g = lambda c: pd.to_numeric(d[pre + c], errors="coerce")
    X["dur_h"] = np.log(g("dur_h"))
    X["lift_max"] = np.clip(np.maximum(g("lift_pre").abs().fillna(3), g("lift_post").abs().fillna(3)), 0, 3)
    X["cover_min"] = np.clip(np.minimum(g("cover_pre").fillna(0), g("cover_post").fillna(0)), 0, 1)
    X["ramp_d"] = np.clip(g("ramp_d").fillna(9), 0, 9)
    X["ecl_ratio"] = np.clip((g("ecl_d") / g("ecl_w")).fillna(20), 0, 20)
    X["has_ecl"] = g("ecl_w").notna().astype(float)
    X["burst_n"] = np.clip(g("burst_n").fillna(0), 0, 10); X["common_n"] = np.clip(g("common_n").fillna(0), 0, 10)
    X["repeat_n"] = np.clip(g("repeat_n").fillna(1), 0, 10)
    X["ph_d"] = np.clip(g("ph_d").fillna(3), 0, 3)
    X["c8_n"] = np.clip(g("c8_n").fillna(0), 0, 4)
    return X


def load(name):
    os.environ["SS_SET"] = name
    import importlib; importlib.reload(DS)
    import stage3_core as C, stage3_report as R
    importlib.reload(C); importlib.reload(R)
    run, pf, rows = SETS[name]
    ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
    ss = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"])
    n = len(ss)
    N = ev[ev.primary & (ev.kind == "flip") & (ev.snr >= 7)].copy().reset_index(drop=True)
    N["t3"] = N.tier == "3"; N["sap"] = N.seen_by == "SAP only"; N["base"] = N.tier.isin(["1A", "1L", "1B"])
    Xn = feats(N); Xn["snr"] = N.snr
    b = pd.read_pickle(rows); b = b[b["error"].isna()] if "error" in b else b
    b = b[b.K.isin((8., 10., 12., 14.)) & (b.sign == 1) & b.tc.notna()][["tic", "sector", "dur", "K", "tier1"]]
    P = pd.read_pickle(pf); P = P[P["error"].isna()] if "error" in P else P
    P = b.merge(P, on=["tic", "sector", "dur", "K"], how="left", suffixes=("_b", ""))
    P["found"] = P.found_primary.fillna(False).astype(bool)
    P["t3"] = P.tier.astype(str) == "3"; P["sap"] = P.seen_by.astype(str) == "SAP only"
    Pf = P[P.found].copy(); Xp = feats(Pf, "ev_"); Xp["snr"] = Pf.snr
    return dict(n=n, tics=ss.tic.values, N=N, Xn=Xn, P=P, Pf=Pf, Xp=Xp)


def models():
    return {"logistic": make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000)),
            "boosting": HistGradientBoostingClassifier(max_depth=3, max_iter=150, learning_rate=0.08, random_state=0)}


def fit(model, A):
    sel_p, sel_n = (A["Xp"].snr < 10) & ~A["Pf"].t3.values & ~A["Pf"].sap.values, (A["Xn"].snr < 10) & ~A["N"].t3.values & ~A["N"].sap.values
    X = pd.concat([A["Xp"][sel_p], A["Xn"][sel_n]]).drop(columns="snr"); y = np.r_[np.ones(sel_p.sum()), np.zeros(sel_n.sum())]
    w = np.r_[np.full(sel_p.sum(), 0.5 / sel_p.sum()), np.full(sel_n.sum(), 0.5 / sel_n.sum())] * len(y)
    if hasattr(model, "steps"):
        model.fit(X, y, logisticregression__sample_weight=w)
    else:
        model.fit(X, y, sample_weight=w)
    return model


def cut_for(name, A):
    """Cut on the out-of-fold score of the training set's own upside-down events so that passes (score >= cut, plus unchanged tier-1 SAP-only) are 8 per 1,000 star-sectors."""
    N, Xn = A["N"], A["Xn"].drop(columns="snr")
    oof = np.zeros(len(N)); groups = N.tic.values
    for tr, te in GroupKFold(5).split(Xn, groups=groups):
        sub = dict(A); sub["N"] = N.iloc[tr]; sub["Xn"] = A["Xn"].iloc[tr]
        mdl = fit(models()[name], sub); oof[te] = mdl.predict_proba(Xn.iloc[te])[:, 1]
    elig = ~N.t3.values & ~N.sap.values
    fixed = int((N.sap & N.base).sum())
    allow = int(BUDGET * A["n"] / 1000) - fixed
    s = np.sort(oof[elig])[::-1]
    return s[allow] + 1e-12 if allow < len(s) else 0.0


def evaluate(name, A, B, label):
    mdl = fit(models()[name], A); cut = cut_for(name, A)
    pn = mdl.predict_proba(B["Xn"].drop(columns="snr"))[:, 1]
    flips_pass = int((((pn >= cut) & ~B["N"].t3.values & ~B["N"].sap.values) | (B["N"].sap.values & B["N"].base.values)).sum())
    pp = mdl.predict_proba(B["Xp"].drop(columns="snr"))[:, 1]
    P = B["P"].copy(); P["opt"] = False
    ok = ((pp >= cut) & ~B["Pf"].t3.values & ~B["Pf"].sap.values) | (B["Pf"].sap.values & B["Pf"].tier1.values)
    P.loc[B["Pf"].index, "opt"] = ok
    P["base"] = P.tier1_b.astype(bool)
    out = [f"{label} [{name}]: upside-down tier-1 on the scored set {flips_pass} = {1000 * flips_pass / B['n']:.2f} per 1,000 star-sectors (cut set on the training set for 8)"]
    for nm, sel in (("4 h", P.dur == 4), ("8 h", P.dur == 8), ("14 and 20 h", P.dur >= 14), ("all boxes", P.dur > 0)):
        g = P[sel]; ga, lo = int((g.opt & ~g.base).sum()), int((~g.opt & g.base).sum())
        p = binomtest(ga, ga + lo, 0.5).pvalue if ga + lo else 1.0
        out.append(f"   dips {nm}: base {100 * g.base.mean():.1f}% option {100 * g.opt.mean():.1f}%; gained {ga}, lost {lo}, net {ga - lo:+d}, exact p {p:.5f}")
    if name == "logistic":
        co = pd.Series(mdl[-1].coef_[0], index=B["Xn"].drop(columns="snr").columns).sort_values()
        out.append("   weights (standardised, + = more planet-like): " + ", ".join(f"{k} {v:+.2f}" for k, v in co.items()))
    return out


def half(A, mask):
    """The part of a loaded set whose star (tic) satisfies mask(tic); used for the within-G2 transfer check (the sealed slice is G2-like, G1 is not)."""
    n = int(mask(A["tics"]).sum()); kn, kp = mask(A["N"].tic.values), mask(A["Pf"].tic.values)
    Pm = mask(A["P"].tic.values)
    return dict(n=n, tics=A["tics"][mask(A["tics"])], N=A["N"][kn], Xn=A["Xn"][kn], P=A["P"][Pm], Pf=A["Pf"][kp], Xp=A["Xp"][kp])


if __name__ == "__main__":
    D = {s: load(s) for s in SETS}
    txt = []
    if os.environ.get("C4_WITHIN"):
        for nm, f in (("tic parity", lambda t: t % 2 == 0), ("tic//1000 parity", lambda t: (t // 1000) % 2 == 0)):
            for model in ("logistic", "boosting"):
                for x, y in ((f, lambda t: ~f(t)), (lambda t: ~f(t), f)):
                    txt += evaluate(model, half(D["g2"], x), half(D["g2"], y), f"within G2 dev, split by {nm}, half sizes {half(D['g2'], x)['n']} -> {half(D['g2'], y)['n']}")
        print(chr(10).join(txt)); open("../research/stage3/score-c4.txt", "a", encoding="utf-8").write(chr(10).join(txt) + chr(10)); raise SystemExit
    for name in ("logistic", "boosting"):
        for tr, te in (("g1", "g2"), ("g2", "g1")):
            txt += evaluate(name, D[tr], D[te], f"train {tr} -> score {te}")
    print("\n".join(txt))
    open("../research/stage3/score-c4.txt", "a", encoding="utf-8").write("\n".join(txt) + "\n")
