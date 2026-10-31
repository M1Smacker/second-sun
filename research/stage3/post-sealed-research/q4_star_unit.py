# Q4 (31 Oct 2026): the right unit and the right estimate for the control. Exploratory, after the scorecard; changes no result.
# usage: python q4_star_unit.py <run> <options|none> <stars in slice>
import os, sys
run, opts, nstars = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path.insert(0, r"D:\second-sun\pipeline")
os.environ["SS_SET"] = "g2"
if opts != "none":
    os.environ["VESPER_OPTS"] = opts
import pandas as pd, numpy as np
from scipy import stats
import stage3_report as R
ev, meta = R.load(rf"D:\second-sun\data\stage3_g2\{run}\groups")
E = R.pdc_half(ev[ev.primary]).copy()
E["snr"] = pd.to_numeric(E.snr, errors="coerce")
T1 = ["1A", "1L", "1B"]
stars = np.array(sorted(set(E.tic))); pad = nstars - len(stars)


def vec(mask):
    c = E[mask].groupby("tic").size()
    return np.array([c.get(s, 0) for s in stars] + [0] * pad, dtype=np.int32)


rng = np.random.default_rng(7); B = 20000
idx = rng.integers(0, nstars, (B, nstars), dtype=np.int32)
print(f"== {run} options={opts}: {nstars} stars; primary events {len(E)} (real {(E.kind=='real').sum()}, flip {(E.kind=='flip').sum()}) on {E.tic.nunique()} stars")
print("bar | tier1 real (stars) | tier1 flip (stars) | ratio full run [95% star-bootstrap] | expected real | real-exp [95% interval] | upper 95% one-sided | sd | deff | P(event Poisson) | P(star bootstrap) | detectable excess (80% power)")
for b in (7, 8, 10, 12):
    ok = E.snr >= b
    rawR, rawF = vec(ok & (E.kind == "real")), vec(ok & (E.kind == "flip"))
    t1r, t1f = vec(ok & (E.kind == "real") & E.tier.isin(T1)), vec(ok & (E.kind == "flip") & E.tier.isin(T1))
    if rawR.sum() == 0 or rawF.sum() == 0:
        print(b, "no raw events"); continue
    ratio = rawF.sum() / rawR.sum(); R1, F1 = t1r.sum(), t1f.sum(); exp = F1 / ratio
    rr, rf = rawR[idx].sum(1), rawF[idx].sum(1)
    good = rr > 0
    rb = np.where(good, rf / np.maximum(rr, 1), np.nan)
    dr, df = t1r[idx].sum(1), t1f[idx].sum(1)
    exc = dr - df / rb
    exc = exc[good]
    sd = exc.std(); pois = F1 / ratio + 0  # var under independent Poisson approx: R1 + F1/ratio^2 (both counts independent)
    deff = sd ** 2 / (R1 + F1 / ratio ** 2) if R1 + F1 > 0 else float("nan")
    p_ev = stats.poisson.sf(R1 - 1, exp) if exp > 0 else float("nan")
    p_st = (exc <= 0).mean()
    print(f"{b} | {R1} ({(t1r>0).sum()}) | {F1} ({(t1f>0).sum()}) | {ratio:.2f} [{np.nanpercentile(rb,2.5):.2f} to {np.nanpercentile(rb,97.5):.2f}] | {exp:.1f} | {R1-exp:+.1f} [{np.percentile(exc,2.5):+.1f} to {np.percentile(exc,97.5):+.1f}] | {np.percentile(exc,95):+.1f} | {sd:.1f} | {deff:.1f} | {p_ev:.2g} | share of draws real<=expected {100*p_st:.1f}% | {2.49*sd:.1f}")
    if b == 7:
        # star-level asymmetry: stars with >=1 raw flip vs stars with >=1 raw real (one count per star)
        sr, sf = (rawR > 0), (rawF > 0)
        print(f"   bar 7 raw events per star: real {rawR.sum()} on {sr.sum()} stars, flip {rawF.sum()} on {sf.sum()} stars; star-level ratio {sf.sum()/sr.sum():.2f}; event-level ratio {ratio:.2f}")
        tot = rawR + rawF; order = np.argsort(-tot)
        for k in (1, 5, 10, 25):
            keep = np.ones(nstars, bool); keep[order[:k]] = False
            print(f"   ratio after dropping the {k} heaviest stars (raw events): {rawF[keep].sum()/max(rawR[keep].sum(),1):.2f}  (they hold {100*tot[order[:k]].sum()/tot.sum():.0f}% of raw events)")
