"""Candidate C1 (10 Nov 2026, Opus 5.5 nested session): C0 catalogue windows (time only, no refit) + a REPEAT-CONFIRMED complement.
Design note: research/fable-audit-2026-11/DESIGN-C1-OPUS-2026-11-10.md. Not part of the frozen pipeline; nothing in pipeline/ is edited.

Complement, per period P of the star (catalogue period, else each audit_all.PER period):
 1. Light outside the C0 windows is flattened ADDITIVELY (r = f - running median over max(1 d, 4 primary widths)), so 2 - f gives exactly -r: the mirror rule holds by construction.
 2. Bins of b = max(wp / 3, 0.5 h) (1 h without a catalogue width); bin z = mean(r) / (sigma / sqrt(n)), sigma = robust per-cadence scatter.
    A LOW run = adjacent bins with z < -Z, a HIGH run = adjacent bins with z > +Z. Both kinds are collected (mirror rule).
 3. A run RECURS if another run of the SAME sign sits at the same binary phase (distance < half spans + TOL) in a DIFFERENT cycle of this sector, or,
    when P >= PSLOW (fewer than 2 cycles per sector), in a DIFFERENT sector of the same star (one product per sector, SPOC family first).
    Cross-sector phases are aligned on the catalogue epoch shifted by each sector's PRIMARY offset (C0.refit on the deep primary only); no catalogue -> no shift, TOL + DRIFT_H.
 4. Each recurring run masks its phase interval (half span x (1 + PAD) + 0.5 h) in EVERY cycle of the sector, the same cadences for both arms. Runs seen once are
    never masked (single-visit lane). Total repeat-masked phase is capped at CAP of the period (strongest runs first).
 5. Stars with no usable catalogue width: no frozen fold any more; the complement alone, with T0 = 0.
mask_runs(t, f, periods) like stage2_search.mask_runs; star from CURRENT_TIC. SYNTH (test hook) adds synthetic recurring eclipses to OTHER sectors' light."""
import os, sys, pathlib
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import c0_catalogue_mask as C0

Z = float(os.environ.get("C1_Z", "4.0"))
TOL_H, DRIFT_H, PAD, CAP = 1.0, 2.0, 0.5, 0.25
PSLOW = float(os.environ.get("C1_PSLOW", "13.0"))   # 1e9 = no cross-sector lane (variant C1f)
ZX = float(os.environ.get("C1_ZX", "2.0"))   # other-sector runs need peak |z| >= Z + ZX
WRATIO = 2.5                                  # matched runs must have half spans within a factor 2.5
ZRATIO = 3.0                                  # and, within a sector, peak |z| within a factor 3
CURRENT_TIC = None
SYNTH = None            # None or f(tic, t) -> additive flux; applied to other-sector light (the test adds it to the current light itself)
STATS = {}              # tic -> dict(rec=, single=, cap=)
_OTHER = {}


def _flat(t, f, wp):
    cad = np.median(np.diff(t)); L = max(1.0, 4 * wp) if np.isfinite(wp) else 1.0
    w = max(int(L / cad) | 1, 5)
    tr = pd.Series(f).rolling(w, center=True, min_periods=w // 4).median().values
    r = f - tr; s = 1.4826 * np.nanmedian(np.abs(r - np.nanmedian(r)))
    return r, s


def find_runs(t, f, keep, wp):
    """Residual low and high runs in the kept light: list of (sign, centre, half span, peak |z|)."""
    tk, fk = t[keep], f[keep]
    if len(tk) < 50:
        return []
    r, s = _flat(tk, fk, wp)
    b = max(wp / 3, 0.5 / 24) if np.isfinite(wp) else 1 / 24
    idx = np.floor((tk - tk.min()) / b).astype(int)
    df = pd.DataFrame(dict(i=idx, r=r)).dropna().groupby("i").r.agg(["mean", "size"]); df = df[df["size"] >= 3]
    z = df["mean"] / (s / np.sqrt(df["size"]))
    out = []
    for sign in (-1, 1):
        hit = z.index[(sign * z) > Z].values
        if not len(hit):
            continue
        groups = np.split(hit, np.where(np.diff(hit) > 1)[0] + 1)
        for g in groups:
            a, e = tk.min() + g[0] * b, tk.min() + (g[-1] + 1) * b
            out.append((sign, (a + e) / 2, (e - a) / 2, float(np.max(sign * z.loc[g]))))
    return out


def _offset(t, f, c):
    if c is None or not np.isfinite(c.get("wp", np.nan)):
        return 0.0
    cc = C0.refit(t, f, c)
    return float(cc.get("refit", 0.0))


def other_runs(tic, c, P):
    """Runs of the star's OTHER sectors: list of (sign, phase, half span [d], tmin, tmax). Cached per (tic, synth on/off)."""
    key = (tic, SYNTH is not None, round(P, 6))
    if key in _OTHER:
        return _OTHER[key]
    import wo_f01a_mask_loss as H
    man = pd.read_csv(H.DS.MANIFEST).drop_duplicates("file"); m = man[man.tic == tic].copy()
    m = m.assign(sec=m.file.str.extract(r"[-_]s(\d{4})[-_]", expand=False).astype(float).values,   # SPOC 'tess..-s0012-..' and QLP 'hlsp_qlp_tess_ffi_s0012-..'
                 pri=(m.author == "QLP").astype(int).values)
    m = m.sort_values(["sec", "pri"]).groupby("sec").head(1)
    out = []; wp = c["wp"] if c is not None else np.nan; T0 = c["T0"] if c is not None else 0.0
    for p in m.path:
        try:
            tf, meta, st = H.load_windowed(p)
        except Exception:
            continue
        if tf is None:
            continue
        t, f = tf
        if SYNTH is not None:
            f = f + SYNTH(tic, t)
        keep = ~C0.windows(t, c)[0] if c is not None and np.isfinite(wp) else np.ones(len(t), bool)
        off = _offset(t, f, c)
        for sign, tc, hs, zp in find_runs(t, f, keep, wp):
            if zp >= Z + ZX:                                                    # another sector's run must be clearly real (chance matches cost planet dips)
                out.append((sign, ((tc - T0 - off) / P) % 1.0, hs, t.min(), t.max()))
    _OTHER[key] = out
    return out


def complement(t, f, keep, tic, c, P):
    """Boolean mask (True = remove) of recurring-run phase intervals for period P, built from f only (applied to both arms by the caller)."""
    wp = c["wp"] if c is not None else np.nan; T0 = c["T0"] if c is not None else 0.0
    off = _offset(t, f, c)
    runs = find_runs(t, f, keep, wp)
    st = STATS.setdefault(tic, dict(rec=0, single=0, cap=0))
    ph = [((tc - T0 - off) / P) % 1.0 for _, tc, _, _ in runs]; cyc = [np.floor((tc - T0 - off) / P + 0.5) for _, tc, _, _ in runs]
    oth = other_runs(tic, c, P) if P >= PSLOW else []
    tol = TOL_H / 24 + (0 if c is not None else DRIFT_H / 24) * (P >= PSLOW)
    rec = []
    for i, (sign, tc, hs, zp) in enumerate(runs):
        hit = False
        for j, (s2, tc2, hs2, _) in enumerate(runs):
            if j != i and s2 == sign and cyc[j] != cyc[i] and max(hs, hs2) <= WRATIO * min(hs, hs2) and max(zp, runs[j][3]) <= ZRATIO * min(zp, runs[j][3]):   # same width and strength, as a real eclipse in every cycle
                d = min(abs(ph[i] - ph[j]), 1 - abs(ph[i] - ph[j])) * P
                hit |= d < hs + hs2 + tol
        for s2, ph2, hs2, a, b in oth:
            if s2 == sign and not (a <= t.max() and b >= t.min()) and max(hs, hs2) <= WRATIO * min(hs, hs2):
                d = min(abs(ph[i] - ph2), 1 - abs(ph[i] - ph2)) * P
                hit |= d < hs + hs2 + tol + DRIFT_H / 24
        if hit:
            rec.append((zp, ph[i], hs * (1 + PAD) + 0.5 / 24))
        st["rec" if hit else "single"] += 1
    out = np.zeros(len(t), bool); used = 0.0
    for zp, p0, half in sorted(rec, reverse=True):
        if used + 2 * half / P > CAP:
            st["cap"] += 1; continue
        used += 2 * half / P
        pt = ((t - T0 - off) / P) % 1.0
        out |= np.minimum(np.abs(pt - p0), 1 - np.abs(pt - p0)) * P <= half
    return out


def remove(t, f, periods, tic):
    """Boolean mask (True = remove) of C1 for this star-sector."""
    c = C0.cat().get(tic)
    if c is not None and not np.isfinite(c.get("wp", np.nan)):
        c = None
    rm = C0.windows(t, c)[0] if c is not None else np.zeros(len(t), bool)
    Ps = ([c["P"]] if c is not None else []) + [P for P in periods if c is None or abs(P / c["P"] - 1) >= 0.02]
    for P in Ps:
        cc = c if (c is not None and abs(P / c["P"] - 1) < 0.02) else None
        rm |= complement(t, f, ~rm, tic, cc, P)
    return rm


def mask_runs(t, f, periods, tic=None):
    tic = CURRENT_TIC if tic is None else tic
    rm = remove(t, f, periods, tic)
    return t[~rm], f[~rm], [(P, []) for P in periods]
