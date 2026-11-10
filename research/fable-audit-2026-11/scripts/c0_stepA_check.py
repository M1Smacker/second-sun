"""Step A of the C0 design (10 Nov 2026, Opus 5.5): catalogue conventions, coverage, drift, and whether catalogue windows sit on the real eclipses.
COUNTS ONLY for set stars (no star ids, no times); TOI-1338 (published) is printed by name. Eclipses are not candidate events; nothing here looks at planet events.
Usage: SS_SET=g2|g3 python c0_stepA_check.py N_STARS"""
import os, sys, re, pathlib, warnings
os.environ.setdefault("NUMBA_NUM_THREADS", "1")
warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, pandas as pd
import wo_f01a_mask_loss as H
import c0_catalogue_mask as C0
import dataset as DS

SET = DS.NAME; N = int(sys.argv[1]); TOI1338 = 260128333
out = []; p = out.append


def coverage():
    tg = pd.read_csv(DS.TARGETS, comment="#").drop_duplicates("tic"); n = len(tg)
    for conv in (("T0", "phip") if SET == "g2" else ("T0",)):
        C0.CONV = conv; cat = C0.load_catalogue(SET)
        sec = sum(np.isfinite(c["phs"]) and np.isfinite(c["ws"]) for c in cat.values())
        wp = sum(np.isfinite(c["wp"]) for c in cat.values())
        ecc = sum(np.isfinite(c["phs"]) and abs(c["phs"] - 0.5) > 0.02 for c in cat.values())
        p(f"[{conv}] stars {n}; in catalogue with period within 2% {len(cat)}; usable primary width {wp} ({wp / n:.0%}); secondary width and phase {sec} ({sec / n:.0%}); secondary phase off 0.5 by > 0.02 {ecc}")
    if SET == "g2":
        php = np.array([c["phip"] for c in cat.values()]); php = php[np.isfinite(php)]
        p(f"Phip-pf quantiles (5,25,50,75,95%): {np.round(np.quantile(php, [.05, .25, .5, .75, .95]), 4)}; share within 0.01 of an integer {np.mean(np.abs(php - np.round(php)) < 0.01):.2f}")
        phis = np.array([c["phis"] for c in cat.values()]); phis = phis[np.isfinite(phis)]
        p(f"Phis-pf quantiles: {np.round(np.quantile(phis, [.05, .25, .5, .75, .95]), 4)}; Phis-pf minus Phip-pf quantiles: "
          f"{np.round(np.quantile([c['phis'] - c['phip'] for c in cat.values() if np.isfinite(c['phis']) and np.isfinite(c['phip'])], [.05, .25, .5, .75, .95]), 4)}")
        d = np.array([3 * np.hypot(c["eT0"], (4000 - c["T0"]) / c["P"] * c["eP"]) / c["wp"] for c in cat.values() if np.isfinite(c["wp"]) and np.isfinite(c["eP"])])
        p(f"Catalogue drift to BTJD 4000 (sector ~98), 3 sigma, in primary widths: quantiles (50,90,99%, max) {np.round(np.quantile(d, [.5, .9, .99, 1]), 3)}; share > 0.25 width {np.mean(d > 0.25):.3f} (n {len(d)})")
    else:
        ph = np.array([(c["phs"], c["phase_col"]) for c in cat.values() if np.isfinite(c["phs"]) and np.isfinite(c["phase_col"])])
        p(f"TTC: secondary phase from T0-sec vs the Phase column: |diff| quantiles (50,90,99%) {np.round(np.quantile(np.abs(ph[:, 0] - ph[:, 1]), [.5, .9, .99]), 3)} (n {len(ph)}); TTC gives no period or T0 errors, drift measured on the data below")
    return n


def measure(t, f, c, conv_label):
    """In-window depth of the primary and secondary (catalogue width x 1.0) against out-of-window flux, in sigma; deepest out-of-window binned dip (bins of wp/2) in sigma;
    offset of the deepest point within 2 widths of each predicted primary, in widths."""
    f = f / np.nanmedian(f)
    inw, _ = C0.windows(t, c, padf=1.0); inw15, _ = C0.windows(t, c, padf=1.5)
    cp = dict(c, ws=np.nan, phs=np.nan); cpp, _ = C0.windows(t, dict(cp, phs=0.0, ws=c["wp"]), padf=1.0)   # primary only
    out_ = f[~inw15]; med = np.median(out_); sd = 1.4826 * np.median(np.abs(out_ - med))
    r = {}
    for lab, k in (("pri", cpp), ("sec", inw & ~cpp)):
        r[lab] = (med - np.mean(f[k])) / (sd / np.sqrt(k.sum())) if k.sum() >= 3 else np.nan
    # deepest binned point outside the 1.5x windows (would be a missed or mislocated eclipse)
    bw = max(c["wp"] / 2, 0.02); tt, ff = t[~inw15], f[~inw15]
    if len(tt) > 50:                       # detrend the kept light with a running median of max(1 d, 4 widths) so spots and ellipsoidal swings are not counted as eclipses
        L = max(1.0, 4 * c["wp"]); cad = np.median(np.diff(tt)); w = max(int(L / cad) | 1, 5)
        ff = ff - pd.Series(ff).rolling(w, center=True, min_periods=w // 4).median().values + 1.0
        sd = 1.4826 * np.nanmedian(np.abs(ff - np.nanmedian(ff))); med = np.nanmedian(ff)
        b = np.floor((tt - tt.min()) / bw); dfm = pd.DataFrame(dict(b=b, f=ff)).groupby("b").f.agg(["mean", "size"]); dfm = dfm[dfm["size"] >= 5]
        r["out_min"] = float(((med - dfm["mean"]) / (sd / np.sqrt(dfm["size"]))).max()) if len(dfm) else np.nan
    else:
        r["out_min"] = np.nan
    offs = []
    for n in np.unique(np.round((t - c["T0"]) / c["P"])):
        cen = c["T0"] + n * c["P"]; k = np.abs(t - cen) < 2 * c["wp"]
        if k.sum() > 10 and np.any(np.abs(t[k] - cen) < 0.25 * c["wp"]):
            ks = pd.Series(f[k]).rolling(5, center=True, min_periods=3).median().values
            offs.append((t[k][np.nanargmin(ks)] - cen) / c["wp"])
    r["off"] = float(np.median(offs)) if offs else np.nan
    return r


def files():
    man = pd.read_csv(DS.MANIFEST).drop_duplicates("file"); man = man[man.author == "SPOC"].copy()
    man["sec"] = man.file.str.extract(r"-s(\d{4})-").astype(float)
    last = man.sort_values("sec").groupby("tic").tail(1)
    return last


H.init(); n = coverage(); last = files(); rng = np.random.default_rng(11)
C0.CONV = "T0"; base = C0.load_catalogue(SET)
convs = ("catalogue", "refit")
cats = {"catalogue": base, "refit": base}
pool = [x for x in last.tic.unique() if x in cats[convs[0]] and np.isfinite(cats[convs[0]][x]["wp"]) and x != TOI1338]
pick = list(rng.choice(pool, min(N, len(pool)), replace=False)) + ([TOI1338] if SET == "g2" else [])
rows = []
for tic in pick:
    r0 = last[last.tic == tic].iloc[0]
    tf, meta, st = H.load_windowed(r0.path)
    if tf is None:
        rows.append(dict(tic=tic, skip=st)); continue
    t, f = tf
    for conv in convs:
        c = cats[conv][tic]
        if conv == "refit":
            c = C0.refit(t, f, c)
        m = measure(t, f, c, conv)
        rows.append(dict(tic=tic, conv=conv, sector=r0.sec, P=c["P"], ecc=bool(np.isfinite(c["phs"]) and abs(c["phs"] - 0.5) > 0.02), **m))
        if tic == TOI1338:
            k = np.round((3995.62 - c["T0"]) / c["P"])
            p(f"TOI-1338 [{conv}] sector {int(r0.sec)}: predicted primary nearest 3995.62 at BTJD {c['T0'] + k * c['P']:.3f}; primary width {c['wp'] * 24:.1f} h; secondary phase {c['phs']:.4f}; "
              f"primary depth {m['pri']:.1f} sigma, secondary {m['sec']:.1f} sigma, deepest out-of-window bin {m['out_min']:.1f} sigma, median primary offset {m['off']:.2f} widths")
df = pd.DataFrame(rows); ok = df[df.get("conv").notna()] if "conv" in df else df.iloc[0:0]
p(f"\nStars checked on their latest SPOC 2-min sector: {len(pick)} (skipped {int(df.get('skip', pd.Series(dtype=object)).notna().sum())}); sectors used, quantiles (0,50,100%): {np.quantile(ok.sector, [0, .5, 1]) if len(ok) else 'n/a'}")
for conv in convs:
    o = ok[(ok.conv == conv) & (ok.tic != TOI1338)]
    p(f"[{conv}] n {len(o)}: primary in-window depth > 5 sigma: {(o.pri > 5).sum()}; < 2 sigma: {(o.pri < 2).sum()}; secondary > 5 sigma: {(o.sec > 5).sum()}; "
      f"|primary offset| < 0.25 width: {(o.off.abs() < 0.25).sum()} of {o.off.notna().sum()}; offset quantiles (10,50,90%) {np.round(np.nanquantile(o.off, [.1, .5, .9]), 2) if o.off.notna().any() else 'n/a'}; "
      f"deepest out-of-window bin > 8 sigma (eclipse left outside the 1.5x windows): {(o.out_min > 8).sum()} (of which eccentric {(o[o.out_min > 8].ecc).sum()})")
print("\n".join(out))
