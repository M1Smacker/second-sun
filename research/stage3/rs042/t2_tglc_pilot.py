"""RS-042 T2 (Claude, 22 Nov 2026, 11:20 pm): same star, same sector: is TGLC light quieter than our QLP light?
Removes T1's star-mix doubt. Design stars only (design_seen = 1). Picks up to 30 design star-sectors that have a local QLP file and a
TGLC light curve on MAST (astroquery, provenance TGLC), spread over Tmag 10 to 13.5; downloads ONLY those TGLC files into
data/tglc_pilot/ (new folder). For each pair: our QLP light via the search loader (detect_v2.load), restricted to the same safe
windows the search uses (x4_faint rule) and to cadences TGLC also has (within 2 min); TGLC cal_aper_flux and cal_psf_flux (finite,
TGLC_flags == 0) on the same cadences. Both: 2-day wotan biweight, 1-hour bins, robust scatter (1.4826 MAD) = noise per hour;
6-hour bins scaled by sqrt(6) over the 1-hour value = red factor. Prints medians of TGLC/QLP ratios by Tmag band.
Prediction (T1): ratio about 0.8 for white noise, lower at Tmag 12+."""
import os, sys, glob, json, pathlib, collections
import numpy as np
ROOT = "D:/second-sun"; OUT = pathlib.Path(ROOT) / "data" / "tglc_pilot"; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, os.path.join(ROOT, "data", "fable", "f2"))
import x4_faint as X
import pandas as pd
from astroquery.mast import Observations
from astropy.io import fits
from wotan import flatten


def noise(t, f):
    ff = flatten(t, f, method="biweight", window_length=2.0); ok = np.isfinite(ff); t, ff = t[ok], ff[ok]
    def binned(h):
        e = np.arange(t.min(), t.max() + h / 24, h / 24); i = np.digitize(t, e)
        m = np.array([ff[i == k].mean() for k in np.unique(i) if (i == k).sum() >= 0.6 * (h / 24) / np.median(np.diff(t))])
        return 1.4826 * np.median(np.abs(m - np.median(m))) if len(m) > 20 else np.nan
    s1, s6 = binned(1), binned(6)
    return s1 * 1e6, s6 * np.sqrt(6) / s1


def main():
    tg = pd.read_csv(f"{ROOT}/targets/r1_targets.csv", comment="#"); tg = tg[(tg.design_seen == 1) & tg.tmag.between(10, 13.5)].drop_duplicates("tic")
    tg = tg.sample(frac=1, random_state=20261122)
    pairs, log = [], []
    for _, r in tg.iterrows():
        if len(pairs) >= 30: break
        camp, tic = r["list"], int(r["tic"])
        qlp = {int(p.split("_s")[1][:4]): p for p in glob.glob(f"{ROOT}/data/{camp}/{tic}/hlsp_qlp_*_llc.fits")}
        if not qlp: continue
        try:
            obs = Observations.query_criteria(provenance_name="TGLC", target_name=str(tic))
        except Exception as e:
            log.append(f"{tic} query error {e}"); continue
        for o in obs:
            s = int(o["sequence_number"])
            if s in qlp and len(pairs) < 30:
                pairs.append(dict(campaign=camp, tic=tic, tmag=float(r["tmag"]), sector=s, qlp=qlp[s], obsid=o["obsid"])); break
    print("pairs", len(pairs), flush=True)
    rows = []
    X.init("g2")
    for p in pairs:
        X.init(p["campaign"]); S2, A = X.G["S2"], X.G["A"]
        prods = Observations.get_product_list(str(p["obsid"]))
        prods = prods[[str(n).endswith("_llc.fits") for n in prods["productFilename"]]]
        man = Observations.download_products(prods, download_dir=str(OUT), cache=True)
        path = str(man["Local Path"][0])
        with fits.open(path) as h:
            d = h[1].data; tt = np.asarray(d["time"], float); flags = np.asarray(d["TGLC_flags"], int)
            fa, fp = np.asarray(d["cal_aper_flux"], float), np.asarray(d["cal_psf_flux"], float)
        t, f, _, info = S2.load(p["qlp"], info=True)
        sec, cam, ccd = A.head(pathlib.Path(p["qlp"]))
        own = next(iter(glob.glob(f"{ROOT}/data/{p['campaign']}/{p['tic']}/tess*-s{sec:04d}-{p['tic']:016d}-*_lc.fits")), None)
        nbw, nn = A.neighbour_windows(sec, cam, ccd, p["tic"])
        k = S2.in_windows(t, S2.good_windows(own)) if own else (S2.in_windows(t, nbw) if nn >= 2 else np.zeros(len(t), bool))
        t, f = t[k], f[k]
        good = np.isfinite(tt) & (flags == 0)
        j = np.searchsorted(tt[good], t).clip(0, good.sum() - 1) if good.sum() else None
        res = dict(tic=p["tic"], tmag=p["tmag"], sector=p["sector"], n_qlp=len(t))
        if j is None or len(t) < 200: rows.append(res); continue
        match = np.abs(tt[good][j] - t) < 2 / 1440
        tq, fq = t[match], f[match]; idx = j[match]
        res["n_common"] = int(match.sum())
        if match.sum() < 200: rows.append(res); continue
        res["qlp"] = noise(tq, fq)
        for name, fl in (("aper", fa), ("psf", fp)):
            v = fl[good][idx]; ok = np.isfinite(v) & (v > 0)
            res[name] = noise(tq[ok], v[ok] / np.nanmedian(v[ok])) if ok.sum() > 200 else None
        rows.append(res); print(json.dumps(res), flush=True)
    json.dump(rows, open(OUT / "t2_rows.json", "w"))
    files = list(OUT.rglob("*.fits")); print("downloaded files", len(files), "MB", round(sum(f.stat().st_size for f in files) / 1e6, 1))
    for band, lo, hi in (("10-11.5", 10, 11.5), ("11.5-13.5", 11.5, 13.5), ("all", 0, 99)):
        R = [r for r in rows if "qlp" in r and lo <= r["tmag"] < hi]
        for name in ("aper", "psf"):
            w = [r[name][0] / r["qlp"][0] for r in R if r.get(name)]; rr = [r[name][1] / r["qlp"][1] for r in R if r.get(name)]
            if w: print(f"Tmag {band} {name}: n {len(w)}, white ratio median {np.median(w):.2f} (IQR {np.quantile(w,.25):.2f} to {np.quantile(w,.75):.2f}), red ratio {np.median(rr):.2f}")


if __name__ == "__main__":
    main()
