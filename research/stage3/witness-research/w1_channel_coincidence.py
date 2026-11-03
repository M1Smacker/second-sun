"""RS-003 Witness, own-data kill test (W1, W4, W6, W10). KILL RULE, written before the first run (3 Nov 2026):
 Witness is KILLED if (a) among upside-down control events found in SPOC 2-minute files (G1 run fd788be04650 and G2 development run dev_73f62615e365 pooled), the share whose channel statistic has p < 0.05
 is not above the 5% expected by chance with a one-sided binomial p < 0.01; or (b) at the published-and-updated TOI-1338 b transit times, half or more of the transits that have a SPOC file show p < 0.05 in the
 same statistic (the channels would veto a real planet). Otherwise it is alive for a bigger test only.
Statistic: five housekeeping channels (SAP_BKG, POS_CORR1, POS_CORR2, MOM_CENTR1, MOM_CENTR2), good-quality cadences, binned to 30 min, 1 day running-median removed. For an event (centre t0, box length d):
 channel value = mean inside [t0 - d/2, t0 + d/2]; 40 random windows of the same length elsewhere in the same file (no overlap with +-1 d of the event) give a null; z = (value - null median) / (1.4826 MAD);
 event statistic = max over channels of |z|; p = (1 + #null windows with a statistic at least as large) / 41. Max over channels already pays for the five channels. Aggregates only; no star IDs are printed.
Usage: python w1_channel_coincidence.py g1 | g2dev | toi1338"""
import os, sys, glob, json, warnings
warnings.filterwarnings("ignore")
mode = sys.argv[1]
if mode != "g1":
    os.environ["SS_SET"] = "g2"
sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
from astropy.io import fits
from scipy import stats
import dataset as DS, stage3_core as C, stage3_report as R
CH = ["SAP_BKG", "POS_CORR1", "POS_CORR2", "MOM_CENTR1", "MOM_CENTR2"]
rng = np.random.default_rng(20261103)
BIN = 1 / 48.0


def series(path):
    with fits.open(path) as h:
        d = h[1].data; t = np.array(d["TIME"], float); q = np.array(d["QUALITY"])
        ok = np.isfinite(t) & (q == 0)
        have = [c for c in CH if c in d.columns.names]
        raw = {c: np.array(d[c], float) for c in have}
    if not have or ok.sum() < 500:
        return None
    t0 = t[ok].min(); nb = int((t[ok].max() - t0) / BIN) + 1
    idx = ((t[ok] - t0) / BIN).astype(int); tb = t0 + (np.arange(nb) + .5) * BIN
    out = {}
    for c in have:
        y = raw[c][ok]; f = np.isfinite(y)
        s = np.bincount(idx[f], weights=y[f], minlength=nb); n = np.bincount(idx[f], minlength=nb)
        yb = np.where(n >= 5, s / np.maximum(n, 1), np.nan)
        if np.isfinite(yb).sum() < 100:
            continue
        sm = pd.Series(yb).rolling(49, center=True, min_periods=12).median().values
        out[c] = yb - sm
    return (tb, out) if out else None


def wmean(tb, y, c0, half):
    m = (tb >= c0 - half) & (tb <= c0 + half)
    need = max(3, int(0.6 * 2 * half / BIN))
    v = y[m]; v = v[np.isfinite(v)]
    return v.mean() if len(v) >= need else np.nan


def stat(tb, ch, t0, dur_h, nnull=40):
    half = dur_h / 48.0
    valid = np.where((np.abs(tb - t0) > 1.0 + half) & (tb > tb[0] + half) & (tb < tb[-1] - half))[0]
    if len(valid) < 200:
        return None
    cs = tb[rng.choice(valid, size=nnull * 3, replace=False if len(valid) >= nnull * 3 else True)]
    names = list(ch)
    nullm = {c: np.array([wmean(tb, ch[c], x, half) for x in cs]) for c in names}
    keep = np.all([np.isfinite(nullm[c]) for c in names], axis=0)
    if keep.sum() < 25:
        return None
    med = {c: np.median(nullm[c][keep]) for c in names}
    sd = {c: 1.4826 * np.median(np.abs(nullm[c][keep] - med[c])) + 1e-12 for c in names}
    ev = {c: wmean(tb, ch[c], t0, half) for c in names}
    if not all(np.isfinite(v) for v in ev.values()):
        return None
    zn = np.abs(np.array([[(nullm[c][j] - med[c]) / sd[c] for c in names] for j in np.where(keep)[0]]))
    ze = np.abs(np.array([(ev[c] - med[c]) / sd[c] for c in names]))
    snull = zn.max(axis=1); se = ze.max()
    p = (1 + (snull >= se).sum()) / (1 + len(snull))
    pc = [(1 + (zn[:, k] >= ze[k]).sum()) / (1 + len(snull)) for k in range(len(names))]
    return p, dict(zip(names, pc))


def spoc_file(base, tic, sector):
    g = sorted(glob.glob(os.path.join(str(base), str(tic), f"tess*-s{int(sector):04d}-*_lc.fits")))
    return g[0] if g else None


rows = []
if mode in ("g1", "g2dev"):
    run = "fd788be04650" if mode == "g1" else "dev_73f62615e365"
    ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
    e = ev[(ev["product"].isin(["SPOC", "SPOC-SAP"])) & (ev.snr >= 7)].copy()
    e["ck"] = e.center.round(1)
    e = e.drop_duplicates(["tic", "sector", "ck", "kind"])
    print(f"{mode}: data folder {DS.DATA}; SPOC and SPOC-SAP events at SNR 7+ after de-duplication: real {int((e.kind == 'real').sum())}, upside-down {int((e.kind == 'flip').sum())}; "
          f"upside-down tier 1 (all products, SNR 7+, primary): {int(((ev.kind == 'flip') & ev.primary & (ev.snr >= 7) & ev.tier.isin(['1A', '1L', '1B'])).sum())}", flush=True)
    cache = {}
    for _, r in e.iterrows():
        k = (r.tic, r.sector)
        if k not in cache:
            f = spoc_file(DS.DATA, r.tic, r.sector); cache = {k: series(f) if f else None}
        s = cache[k]
        if s is None:
            continue
        o = stat(s[0], s[1], float(r.center), float(r.dur_h))
        if o:
            rows.append(dict(kind=r.kind, tier=str(r.tier), p=o[0], **{"p_" + c: v for c, v in o[1].items()}))
else:
    ex = json.load(open(r"D:\second-sun\research\stage3\toi1338b-expected.json"))["epochs"]
    shift = {27: .262, 34: .306, 37: .015, 62: .286, 65: .604, 68: .305, 89: .833, 93: .880, 96: 1.312, 98: .973}   # section E of scorecard-plus-sealed.txt
    for s, sh in shift.items():
        for x in [x for x in ex if x["sector"] == s]:
            f = spoc_file(r"D:\second-sun\data\g2", 260128333, s)
            if not f:
                continue
            se = series(f)
            o = stat(se[0], se[1], x["btjd"] + sh, x["dur_h"]) if se else None
            if o:
                rows.append(dict(kind="toi1338b", tier="-", sector=s, p=o[0], **{"p_" + c: v for c, v in o[1].items()}))
d = pd.DataFrame(rows)
print(f"events with a usable file and enough null windows: {len(d)}")
for name, g in (("upside-down, tier 1", d[(d.kind == "flip") & d.tier.isin(["1A", "1L", "1B"])]), ("upside-down, tier 2 or 3", d[(d.kind == "flip") & ~d.tier.isin(["1A", "1L", "1B"])]),
                ("upside-down, all", d[d.kind == "flip"]), ("real, tier 1", d[(d.kind == "real") & d.tier.isin(["1A", "1L", "1B"])]), ("real, all", d[d.kind == "real"]), ("TOI-1338 b transits", d[d.kind == "toi1338b"])):
    if len(g):
        k = int((g.p < .05).sum()); bt = stats.binomtest(k, len(g), .05, alternative="greater").pvalue
        per = ", ".join(f"{c[2:]} {int((g[c] < .05).sum())}" for c in g.columns if c.startswith("p_"))
        print(f"  {name:26s}: n {len(g):4d}; p < 0.05 in {k} ({100 * k / len(g):.1f}%, 5% expected); one-sided binomial p {bt:.3g}; by channel p < 0.05: {per}")
