"""RS-040 S0 (Claude, 22 Nov 2026, written BEFORE any score result): does one learned score beat the four soft hard-holds at EQUAL alarms?
Exploratory, one key, design stars only, 006 planet bench (older chain, P about 0.48). Not a freeze test: a go / no-go for a Codex brief S.

Fixed rules (written first):
- Hard holds stay: an event with c5, ecl_overlap, repeater, orbit_lock, p1_veto, flipmatch, burst/common, or tier 3 under B stays out.
  'Eligible' = an event whose B tier is 1A/1L/1B, or tier 2 caused ONLY by soft flags (step, ramp, gap_dump, dominated).
- Score = logistic regression (sklearn, L2, C = 1.0, standardised features), features: log10 snr, log10 depth, dur_h, |lift_pre| and
  |lift_post| (missing -> 2, capped at 2), min cover, min(ramp_d, 3) (missing -> 3), the four soft flags, c8_best capped at 20
  (missing -> 0), second product present, QLP product.
- Positives: planted events of BOTH arms (each in its own arm's frame), crossings not already tier 1 before injection ('pre' false).
  Negatives: un-injected background events of BOTH arms. Symmetric by construction.
- Two folds: stars split in halves by a fixed hash (seed 2026112240); train on one half, judge on the other, then swap.
- Threshold (on the TRAINING half only): the lowest cut whose training-half background passes at most B's real AND at most B's
  upside-down tier-1 counts on that half.
- Judged on the test half: planets found (real arm, new), equal weight per binary-period bin, against B on the same half; the
  upside-down arm (control) the same way; background real / upside-down counts against B.
- Go for a Codex brief S if, summed over both folds: real-arm planets gained >= +2.0 points of P, background real and upside-down
  each not above B, and the planted upside-down arm gain within 2 points of the real-arm gain (fairness)."""
import json, hashlib
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

D = Path(r"D:\second-sun\data\rs040"); OUT6 = Path(r"D:\second-sun\data\astra\006")
T1 = {"1A", "1L", "1B"}; SOFT = ["step", "ramp", "gap_dump", "dominated"]
HARD = ["c5", "ecl_overlap", "repeater", "orbit_lock", "p1_veto", "flipmatch", "burst", "common"]


def tb(s):
    return s.astype(str).str.lower().isin(["true", "1", "1.0"])


def prep(df):
    # 22 Nov 9:47 pm: first run crashed before any result (5 background events carry snr = inf); snr capped at 1e4, nothing else changed
    df = df.copy()
    for c in SOFT + HARD:
        df[c] = tb(df[c]) if c in df else False
    hard = df[HARD].any(axis=1) | (df.tier.astype(str) == "3")
    soft_only = (df.tier.astype(str) == "2") & ~hard
    df["eligible"] = df.tier.astype(str).isin(T1) | soft_only
    lift = lambda c: pd.to_numeric(df[c], errors="coerce").abs().fillna(2).clip(upper=2)
    X = pd.DataFrame(dict(lsnr=np.log10(pd.to_numeric(df.snr).clip(lower=1, upper=1e4)), ldep=np.log10(pd.to_numeric(df.depth_ppm).abs().clip(lower=10)),
                          dur=pd.to_numeric(df.dur_h), lpre=lift("lift_pre"), lpost=lift("lift_post"),
                          cov=np.minimum(pd.to_numeric(df.cover_pre, errors="coerce").fillna(0), pd.to_numeric(df.cover_post, errors="coerce").fillna(0)),
                          ramp=pd.to_numeric(df.ramp_d, errors="coerce").fillna(3).clip(upper=3),
                          c8=pd.to_numeric(df.c8_best, errors="coerce").fillna(0).clip(upper=20),
                          second=(pd.to_numeric(df.c8_n, errors="coerce").fillna(0) > 0).astype(float),
                          qlp=(df["product"].astype(str).str.startswith("QLP")).astype(float)))
    for c in SOFT:
        X[c] = df[c].astype(float)
    return df, X


def half(star):
    return int(hashlib.sha256(f"2026112240-{star}".encode()).hexdigest(), 16) % 2


def denominators():
    rows = []
    for camp in ("g2", "g3"):
        for j in sorted(OUT6.glob(f"planet-*-*-*-{camp}/results.jsonl")):
            for line in j.read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                if r["observed"]:
                    rows.append(dict(campaign=camp, trial=r["trial"], star=r["star"], bin=r["bin"]))
    return pd.DataFrame(rows)


def P(found, den):
    """equal weight per bin: found = set of (campaign, trial)."""
    return 100 * np.mean([den[den.bin == b].apply(lambda r: (r.campaign, r.trial) in found, axis=1).mean() for b in sorted(den.bin.unique())])


def main():
    pl, Xp = prep(pd.read_csv(D / "planted.csv", low_memory=False))
    bg, Xb = prep(pd.read_csv(D / "background.csv", low_memory=False))
    pl = pl[~tb(pl["pre"])]; Xp = Xp.loc[pl.index]
    pl["h"] = pl.star.map(half); bg["h"] = bg.tic.map(half)
    den = denominators(); den["h"] = den.star.map(half)
    out = dict(rows_planted=len(pl), rows_background=len(bg), folds=[])
    tot = dict(gain_real=0.0, gain_flip=0.0)
    for test in (0, 1):
        tr = test ^ 1
        pos = pl[(pl.h == tr) & pl.eligible]; neg = bg[(bg.h == tr) & bg.eligible]
        X = pd.concat([Xp.loc[pos.index], Xb.loc[neg.index]]); y = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
        sc = StandardScaler().fit(X); m = LogisticRegression(C=1.0, max_iter=2000).fit(sc.transform(X), y)
        s_bg = pd.Series(m.decision_function(sc.transform(Xb.loc[bg.index])), index=bg.index)
        s_pl = pd.Series(m.decision_function(sc.transform(Xp.loc[pl.index])), index=pl.index)
        btier = bg.tier.astype(str).isin(T1)
        ref = {k: int(((bg.h == tr) & btier & (bg.kind == k)).sum()) for k in ("real", "flip")}
        cut = None
        for t in np.sort(s_bg[(bg.h == tr) & bg.eligible].unique()):
            sel = (bg.h == tr) & bg.eligible & (s_bg >= t)
            if all(int((sel & (bg.kind == k)).sum()) <= ref[k] for k in ("real", "flip")):
                cut = float(t); break
        dt = den[den.h == test]
        f = dict(test_half=test, cut=cut, weights=dict(zip(X.columns, np.round(m.coef_[0], 3).tolist())))
        for arm in ("real", "flip"):
            a = pl[(pl.h == test) & (pl.arm == arm)]
            fb = set(zip(a[a.tier.astype(str).isin(T1)].campaign, a[a.tier.astype(str).isin(T1)].trial))
            ok = a.eligible & (s_pl.loc[a.index] >= cut)
            fs = set(zip(a[ok].campaign, a[ok].trial))
            f[arm] = dict(P_B=round(P(fb, dt), 2), P_S=round(P(fs, dt), 2), gained=len(fs - fb), lost=len(fb - fs))
            tot["gain_" + arm] += (P(fs, dt) - P(fb, dt)) / 2
        for k in ("real", "flip"):
            f["bg_" + k] = dict(B=int(((bg.h == test) & btier & (bg.kind == k)).sum()),
                                S=int(((bg.h == test) & bg.eligible & (s_bg >= cut) & (bg.kind == k)).sum()))
        out["folds"].append(f)
    out["mean_gain_real"] = round(tot["gain_real"], 2); out["mean_gain_flip"] = round(tot["gain_flip"], 2)
    bgS = {k: sum(f["bg_" + k]["S"] for f in out["folds"]) for k in ("real", "flip")}
    bgB = {k: sum(f["bg_" + k]["B"] for f in out["folds"]) for k in ("real", "flip")}
    out["go"] = bool(out["mean_gain_real"] >= 2.0 and all(bgS[k] <= bgB[k] for k in bgS) and abs(out["mean_gain_flip"] - out["mean_gain_real"]) <= 2.0)
    Path(__file__).with_name("s0-result.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
