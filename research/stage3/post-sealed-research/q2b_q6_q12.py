# Q2 (per-star efficiency), Q6 (events across sectors per star), Q12 (crowding keys in the light-curve headers). 31 Oct 2026, exploratory.
import os, sys, json, glob, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, r"D:\second-sun\pipeline"); os.environ["SS_SET"] = "g2"; os.environ["VESPER_OPTS"] = "c6"
import numpy as np, pandas as pd
import stage3_report as R
ev, meta = R.load(r"D:\second-sun\data\stage3_g2\sealed_5f73692944aa\groups")
ss = meta[meta.status == "ok"].drop_duplicates(["tic", "sector"]).groupby("tic").size()
print(f"Q2: sectors per star with data (sealed 594 stars): mean {ss.mean():.1f}, median {ss.median():.0f}, 25-75% {ss.quantile(.25):.0f}-{ss.quantile(.75):.0f}; star-sectors {int(ss.sum())}")
P = pd.concat([pd.read_pickle(r"D:\second-sun\data\chain_recovery_g2\rows_sealed.pkl"), pd.read_pickle(r"D:\second-sun\data\chain_recovery_g2\rows_g2dev.pkl")])
P = P[P.K.notna() & P.error.isna() & (P.sign == 1) & (P.dur == 8)].copy(); P["sig"] = P.depth_ppm / P.K
cK = P.groupby("K").apply(lambda v: v.tier1.astype(bool).mean()); Ks, Cs = np.array(cK.index, float), cK.values
C = lambda K: float(np.interp(K, Ks, Cs, left=Cs[0] * max(K, 0) / Ks[0]))
sg = P.sig.median(); nsec = ss.mean(); W = 26.0
print(f"noise per 8 h box median {sg:.0f} ppm; tier-1 completeness (8 h box) by K: " + ", ".join(f"K{int(k)} {100*c:.0f}%" for k, c in zip(Ks, Cs)))
print("depth ppm (what planet) | K | completeness | expected tier-1 detections per planet-bearing star over all its sectors at P = 60 / 95 / 150 / 300 d | limit on (planets per binary x geometry g) at P=95 and 300 d: N_ul 8.3 | N_ul 1.0")
for dep, nm in ((1000, "~4 Re, 1 Rsun"), (2300, "TOI-1338 b as seen (median depth of its events)"), (4000, "6.85 Re, 1 Rsun, undiluted"), (10000, "Jupiter, 1 Rsun")):
    K = dep / sg; c = C(K); D = [nsec * W / p * c for p in (60, 95, 150, 300)]
    lim = lambda n, d: n / (594 * d) if d > 0 else float("inf")
    print(f"  {dep:6d} ({nm}) | {K:4.1f} | {100*c:3.0f}% | " + " / ".join(f"{d:.2f}" for d in D) + f" | P95: {100*lim(8.3,D[1]):.1f}% | {100*lim(1.0,D[1]):.2f}%   P300: {100*lim(8.3,D[3]):.1f}% | {100*lim(1.0,D[3]):.2f}%")
# Q6
E = ev[ev.primary]; E = E[pd.to_numeric(E.snr, errors="coerce") >= 7]
t1 = E[E.tier.isin(["1A", "1L", "1B"])]
for k in ("real", "flip"):
    g = t1[t1.kind == k].groupby("tic").sector.nunique()
    print(f"Q6: tier-1 {k}: stars with events in 1 sector {int((g==1).sum())}, 2 sectors {int((g==2).sum())}, 3+ sectors {int((g>=3).sum())}; max sectors on one star {int(g.max())}")
# Q12
lj = r"D:\second-sun\data\stage3_g2\sealed_5f73692944aa\watch_leads.json"
try:
    L = json.load(open(lj)); print("Q12 leads json keys:", list(L.keys())[:8])
    cards = L.get("cards") or L.get("leads") or []
    tics = sorted({int(c["tic"]) for c in cards if isinstance(c, dict) and "tic" in c})[:12]
except Exception as ex:
    print("leads json:", ex); tics = []
from astropy.io import fits
for tic in tics[:8]:
    fs = sorted(glob.glob(rf"D:\second-sun\data\g2\{tic}\*.fits"))
    for f in fs[:3]:
        try:
            h0, h1 = fits.getheader(f, 0), fits.getheader(f, 1)
            keys = {k: (h1.get(k) if k in h1 else h0.get(k)) for k in ("CROWDSAP", "FLFRCSAP", "PDCVAR", "PDCMETHD", "TESSMAG", "RADIUS", "TEFF")}
            print(f"  TIC {tic} {os.path.basename(f)[:52]}: " + ", ".join(f"{k}={v}" for k, v in keys.items() if v is not None) or "no keys")
        except Exception as ex:
            print("  header error", tic, ex)
