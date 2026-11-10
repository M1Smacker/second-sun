"""Candidate C0 (10 Nov 2026, Opus 5.5 nested session): a TIME-ONLY eclipse mask from the catalogue ephemeris and widths, as in STANLEY (Martin and Fabrycky 2021)
and mono-cbp (Davies et al. 2026). Design note: research/fable-audit-2026-11/DESIGN-C0-OPUS-2026-11-10.md. NOT part of the frozen pipeline; nothing in pipeline/ is edited.

Windows (BTJD), for each catalogue eclipse n:
  primary   centre T0 + n P,             half width  PADF * wp / 2 + drift(n)
  secondary centre T0 + (n + phs) P,     half width  PADF * ws / 2 + drift(n)
  wp, ws in days; phs = secondary phase measured from the PRIMARY (see CONV); drift(n) = 3 * sqrt(e_T0^2 + (n e_P)^2) where the catalogue gives errors, else 0.
Sources:
  g2: Prsa et al. 2022 TESS EB catalogue (data/xmatch/ebs.csv, first row per TIC as in targets_g2_chain.py): BJD0, Per, e_BJD0, e_Per, Wp-pf, Ws-pf, Phip-pf, Phis-pf.
  g3: TESS Ten Thousand Catalog table 3 (data/g3/catalog_ttc/table3_new_ebs.txt): Per, T0-pri, Dur-pri, T0-sec, Phase, Dur-sec. No errors given.
Fallbacks (counted through FLAGS):
  'no_cat'   star not in the catalogue, period off by > 2 %, or no usable primary width -> the frozen data-driven mask (detect_v2.eclipse_mask_auto) for this star
  'no_sec'   no secondary width/phase -> secondary window at phase 0.5 with the primary width (the same choice eb_widths makes for a missing width)
  'extra_P'  a period in audit_all.PER that is not the catalogue period (a second binary) -> frozen data-driven mask for that period only
Signature: mask_runs(t, f, periods) like stage2_search.mask_runs; the star is set by CURRENT_TIC (the variant harness sets it per file). Returns (t, f, [(P, runs)]),
runs in phase units of (t % P) / P like the frozen function, so ecl_dist-style code can read them."""
import os, sys, pathlib
import numpy as np, pandas as pd
sys.path.insert(0, r"D:\second-sun\pipeline")
from detect_v2 import eclipse_mask_auto

ROOT = pathlib.Path(r"D:\second-sun")
PADF = 1.5          # window = 1.5 x catalogue width, fixed a priori (between mono-cbp 1.0 and Thornton 3.5; equal to the frozen mask's pad), NOT tuned on real events
CONV = "T0"         # Prsa primary centre: "T0" = at BJD0 (Phip-pf ignored), "phip" = at BJD0 + Phip-pf * P. Set from the step A check.
CURRENT_TIC = None
USE_2G = os.environ.get("C0_2G", "1") == "1"   # fall back to the two-Gaussian widths of the catalogue when the polyfit width is missing
G2RATIO = 1.44      # median Wp-2g / Wp-pf over 776 G2 stars (IQR 1.39 to 1.54, flat across period bins; evidence/c0_stepA and the 10 Nov ratio check)
FLAGS2G = set()
FLAGS = {}          # tic -> set of fallback flags actually used (for counting)
_CAT = None


def load_catalogue(name=None):
    """{tic: dict(P, T0 [BTJD], eT0, eP, wp [d], ws [d] or nan, phs [phase from primary] or nan, phip)} for the set's stars."""
    name = name or os.environ.get("SS_SET")
    tg = pd.read_csv(ROOT / "targets" / f"{name}_chain_targets.csv", comment="#").drop_duplicates("tic")
    pbin = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
    out = {}
    if name == "g2":
        eb = pd.read_csv(ROOT / "data" / "xmatch" / "ebs.csv").drop_duplicates("TIC")
        for r in eb.itertuples(index=False):
            tic = int(r.TIC)
            if tic not in pbin or not (abs(r.Per / pbin[tic] - 1) < 0.02):
                continue
            g = lambda c: float(getattr(r, c)) if pd.notna(getattr(r, c)) else np.nan
            P = float(r.Per); wp = g("_15"); ws = g("_18"); php = g("_17"); phs = g("_20")   # Wp-pf, Ws-pf, Phip-pf, Phis-pf (itertuples renames dashed columns)
            w2 = g("_21"); s2 = g("_24"); p2 = g("_23"); ps2 = g("_26")   # Wp-2g, Ws-2g, Phip-2g, Phis-2g: two-Gaussian fallback (Wp-2g / Wp-pf: median 1.44 over 776 G2 stars, flat in period, fixed a priori)
            if USE_2G and not (wp > 0) and w2 > 0:
                wp = w2 / G2RATIO; FLAGS2G.add(tic)
            if USE_2G and not (ws > 0) and s2 > 0 and np.isfinite(ps2) and np.isfinite(p2) and (p2 % 1.0 < 0.02 or p2 % 1.0 > 0.98):
                ws = s2 / G2RATIO; phs = ps2
            out[tic] = dict(P=P, T0=float(r.BJD0), eT0=g("e_BJD0"), eP=g("e_Per"), wp=wp * P if wp > 0 else np.nan, ws=ws * P if ws > 0 else np.nan,
                            phip=php, phis=phs, phs=np.nan)
            if np.isfinite(phs):
                out[tic]["phs"] = (phs - (php if np.isfinite(php) else 0.0)) % 1.0 if CONV == "phip" else phs % 1.0
            if CONV == "phip" and np.isfinite(php):
                out[tic]["T0"] = float(r.BJD0) + php * P
    else:
        lines = [l for l in open(ROOT / "data" / "g3" / "catalog_ttc" / "table3_new_ebs.txt", encoding="latin-1") if l[:10].strip().isdigit()]
        for l in lines:
            def num(a, b):
                try:
                    return float(l[a:b])
                except ValueError:
                    return np.nan
            tic = int(l[0:10]); P = num(44, 53)
            if tic not in pbin or not (abs(P / pbin[tic] - 1) < 0.02) or tic in out:
                continue
            T0 = num(54, 63); dp = num(68, 72); t0s = num(73, 82); ph = num(83, 87); ds = num(95, 99)   # MRT bytes are 1-based: Dur-pri 69-72, T0-sec 74-82, Phase 84-87, Dur-sec 96-99
            phs = ((t0s - T0) / P) % 1.0 if np.isfinite(t0s) else ph
            out[tic] = dict(P=P, T0=T0, eT0=np.nan, eP=np.nan, wp=dp / 24 if dp > 0 else np.nan, ws=ds / 24 if ds > 0 else np.nan, phs=phs, phase_col=ph)
    return out


def cat():
    global _CAT
    if _CAT is None:
        _CAT = load_catalogue()
    return _CAT


REFIT = os.environ.get("C0_REFIT", "1") == "1"        # per-sector phase refit: shift both windows together by the offset (within the catalogue's 3-sigma drift, at most P/4) that makes the primary window deepest
RESID = 0.1         # after a refit the drift term is replaced by 0.1 primary width


def refit(t, f, c):
    """Copy of c with T0 shifted to the deepest primary position in this sector (same shift for primary and secondary: a period error moves both alike).
    Uses the real flux only; the caller applies the resulting time-only windows to both arms. No eclipse covered -> c unchanged (full drift term kept)."""
    P, T0, wp = c["P"], c["T0"], c["wp"]
    n = np.round((np.median(t) - T0) / P)
    eT0 = c["eT0"] if np.isfinite(c.get("eT0", np.nan)) else 0.0; eP = c["eP"] if np.isfinite(c.get("eP", np.nan)) else 0.0
    D = min(max(3 * np.hypot(eT0, n * eP), 0.5 * wp), P / 4)
    ff = f / np.nanmedian(f); best = (np.inf, 0.0)
    ph = ((t - T0) / P + 0.5) % 1.0 - 0.5                           # primary phase in (-0.5, 0.5]
    for s in np.arange(-D, D + 1e-9, wp / 10):
        k = np.abs(ph * P - s) <= wp / 2
        if k.sum() >= 5:
            m = np.mean(ff[k])
            if m < best[0]:
                best = (m, s)
    if not np.isfinite(best[0]):
        return c
    return dict(c, T0=T0 + best[1], eT0=np.nan, eP=np.nan, refit=best[1], resid=RESID * wp)


def windows(t, c, padf=None):
    """Boolean 'inside a catalogue eclipse window' for times t, and whether a catalogue secondary was used."""
    padf = PADF if padf is None else padf
    P, T0 = c["P"], c["T0"]
    eT0 = c["eT0"] if np.isfinite(c.get("eT0", np.nan)) else c.get("resid", 0.0) / 3; eP = c["eP"] if np.isfinite(c.get("eP", np.nan)) else 0.0
    sec_ok = np.isfinite(c["phs"]) and np.isfinite(c["ws"])
    phs = c["phs"] if sec_ok else 0.5
    ws = c["ws"] if sec_ok else c["wp"]
    inside = np.zeros(len(t), bool)
    for off, w in ((0.0, c["wp"]), (phs, ws)):
        n = np.round((t - T0) / P - off)                       # nearest eclipse number for each time
        cen = T0 + (n + off) * P
        half = padf * w / 2 + 3 * np.sqrt(eT0 ** 2 + (n * eP) ** 2)
        inside |= np.abs(t - cen) <= half
    return inside, sec_ok


def mask_runs(t, f, periods, tic=None):
    tic = CURRENT_TIC if tic is None else tic
    c = cat().get(tic)
    fl = FLAGS.setdefault(tic, set()); out = []
    if tic in FLAGS2G:
        fl.add("w2g")
    if c is None or not np.isfinite(c["wp"]):
        fl.add("no_cat")
        for P in periods:
            keep, runs = eclipse_mask_auto(t, f, P); out.append((P, runs)); t, f = t[keep], f[keep]
        return t, f, out
    if REFIT:
        c = refit(t, f, c)
        if "refit" not in c:
            fl.add("no_refit")
    inside, sec_ok = windows(t, c)
    if not sec_ok:
        fl.add("no_sec")
    out.append((c["P"], [])); t, f = t[~inside], f[~inside]
    for P in periods:
        if abs(P / c["P"] - 1) >= 0.02:
            fl.add("extra_P")
            keep, runs = eclipse_mask_auto(t, f, P); out.append((P, runs)); t, f = t[keep], f[keep]
    return t, f, out
