"""Petrova 1.0 eclipse mask and event veto (study switch p1, vopts.py; Re-search 1, research/stage3/R1-PREREGISTRATION.md, build spec R1-BUILD-SPEC-2026-11-11.md).
Why: the Vesper 0.8.1 mask (detect_v2.eclipse_mask_auto) folds ONE sector and cuts the low phases, so in a slow binary it cuts a planet's dip with the eclipses (audit F-01,
WO-F01-PART-A-RESULT-2026-11-10.md). This module is the candidate C2 of research/fable-audit-2026-11 (DESIGN-C0, C1, C2-OPUS-2026-11-10.md), copied from the tested scripts
c0_catalogue_mask.py, c1_mask.py (variant C1f) and c2_event_veto.py, with the settings of the full-size runs: no refit of the windows, no cross-sector lane, Z 5, veto TOL 1 h, NMIN 2.
All numbers are fixed a priori from the catalogue and from planted dips and synthetic eclipses, never from a real event. Nothing here runs unless the switch p1 is on.

Three parts:
 1. WINDOWS (time only, from the catalogue ephemeris and widths, as STANLEY and mono-cbp do): for each catalogue eclipse the window is 1.5 x width wide plus a drift term. No flux is used, so a planet
    dip cannot be mistaken for an eclipse and both arms (real and upside-down) get the same cadences.
 2. REPEAT LANE (inside one sector): residual low OR high runs in the kept light (additive flattening, so 2 - f gives the mirror image) that come back at the same binary phase in another cycle of the
    SAME sector, with a similar width and strength, are masked in every cycle. A run seen once is never masked.
 3. EVENT VETO (slow binaries, P of 13 d or more): an event is flagged p1_veto when the same star has an event of the SAME arm in at least NMIN other sectors at the same binary phase (catalogue epoch +
    that sector's primary offset), with similar duration and depth. It removes events, never cadences. In the chain a vetoed event goes to tier 2 (flag, never delete).
Recovered light = cadences the old mask removes on EITHER arm (f or 2 - f) and this mask keeps; an event counts as evidence in Re-search 1 only if its centre lies there."""
import pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(r"D:\second-sun-astra")
PADF = 1.5            # window = 1.5 x catalogue width (equal to the old mask's pad); not tuned on events
G2RATIO = 1.44        # median Wp-2g / Wp-pf over 776 G2 stars: two-Gaussian width fallback, fixed a priori
Z = 5.0               # repeat lane: run threshold in sigma (C1f full-size runs)
TOL_H, PAD, CAP = 1.0, 0.5, 0.25
WRATIO, ZRATIO = 2.5, 3.0
VETO_TOL_H, VETO_DUR_R, VETO_DEP_R, VETO_PSLOW, VETO_NMIN = 1.0, 2.5, 3.0, 13.0, 2
_CAT = {}


# ---------------------------------------------------------------- catalogue (part 1)
def load_catalogue(name, targets_csv):
    """{tic: dict(P, T0 [BTJD], eT0, eP, wp [d], ws [d] or nan, phs [phase from the primary] or nan)}. g1 and g2: TESS eclipsing binary catalogue (Prsa et al. 2022, data/xmatch/ebs.csv), the TESS
    period must equal the target list period within 2%; the primary is at BJD0 (the Phip column is ignored: settled on real light in step A of DESIGN-C0). g3: TESS Ten Thousand Catalog table 3."""
    tg = pd.read_csv(targets_csv, comment="#").drop_duplicates("tic")
    pbin = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
    out = {}
    if name in ("g1", "g2"):
        eb = pd.read_csv(ROOT / "data" / "xmatch" / "ebs.csv").drop_duplicates("TIC")
        for r in eb.to_dict("records"):
            tic = int(r["TIC"])
            if tic not in pbin or not (abs(r["Per"] / pbin[tic] - 1) < 0.02):
                continue
            g = lambda c: float(r[c]) if pd.notna(r[c]) else np.nan
            P = float(r["Per"]); wp, ws, phs = g("Wp-pf"), g("Ws-pf"), g("Phis-pf")
            w2, s2, p2, ps2 = g("Wp-2g"), g("Ws-2g"), g("Phip-2g"), g("Phis-2g")
            if not (wp > 0) and w2 > 0:
                wp = w2 / G2RATIO
            if not (ws > 0) and s2 > 0 and np.isfinite(ps2) and np.isfinite(p2) and (p2 % 1.0 < 0.02 or p2 % 1.0 > 0.98):
                ws = s2 / G2RATIO; phs = ps2
            out[tic] = dict(P=P, T0=float(r["BJD0"]), eT0=g("e_BJD0"), eP=g("e_Per"), wp=wp * P if wp > 0 else np.nan, ws=ws * P if ws > 0 else np.nan,
                            phs=(phs % 1.0) if np.isfinite(phs) else np.nan)
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
            out[tic] = dict(P=P, T0=T0, eT0=np.nan, eP=np.nan, wp=dp / 24 if dp > 0 else np.nan, ws=ds / 24 if ds > 0 else np.nan, phs=phs)
    return out


def cat():
    if not _CAT:
        import dataset as DS
        _CAT.update(load_catalogue(DS.NAME, DS.TARGETS))
    return _CAT


def windows(t, c, padf=None):
    """Boolean 'inside a catalogue eclipse window' for times t (primary, and secondary at its catalogue phase or 0.5 with the primary width), and whether a catalogue secondary was used."""
    padf = PADF if padf is None else padf
    P, T0 = c["P"], c["T0"]
    eT0 = c["eT0"] if np.isfinite(c.get("eT0", np.nan)) else 0.0; eP = c["eP"] if np.isfinite(c.get("eP", np.nan)) else 0.0
    sec_ok = np.isfinite(c["phs"]) and np.isfinite(c["ws"])
    phs = c["phs"] if sec_ok else 0.5
    ws = c["ws"] if sec_ok else c["wp"]
    inside = np.zeros(len(t), bool)
    for off, w in ((0.0, c["wp"]), (phs, ws)):
        n = np.round((t - T0) / P - off)
        cen = T0 + (n + off) * P
        half = padf * w / 2 + 3 * np.sqrt(eT0 ** 2 + (n * eP) ** 2)
        inside |= np.abs(t - cen) <= half
    return inside, sec_ok


def refit(t, f, c):
    """Offset (d) that puts the primary window on the deepest primary position of THIS sector (real flux). Used only to align phases across sectors, never to place the windows."""
    P, T0, wp = c["P"], c["T0"], c["wp"]
    n = np.round((np.median(t) - T0) / P)
    eT0 = c["eT0"] if np.isfinite(c.get("eT0", np.nan)) else 0.0; eP = c["eP"] if np.isfinite(c.get("eP", np.nan)) else 0.0
    D = min(max(3 * np.hypot(eT0, n * eP), 0.5 * wp), P / 4)
    ff = f / np.nanmedian(f); best = (np.inf, 0.0)
    ph = ((t - T0) / P + 0.5) % 1.0 - 0.5
    for s in np.arange(-D, D + 1e-9, wp / 10):
        k = np.abs(ph * P - s) <= wp / 2
        if k.sum() >= 5:
            m = np.mean(ff[k])
            if m < best[0]:
                best = (m, s)
    return float(best[1]) if np.isfinite(best[0]) else 0.0


# ---------------------------------------------------------------- repeat lane (part 2)
def _flat(t, f, wp):
    cad = np.median(np.diff(t)); L = max(1.0, 4 * wp) if np.isfinite(wp) else 1.0
    w = max(int(L / cad) | 1, 5)
    tr = pd.Series(f).rolling(w, center=True, min_periods=w // 4).median().values
    r = f - tr; s = 1.4826 * np.nanmedian(np.abs(r - np.nanmedian(r)))
    return r, s


def find_runs(t, f, keep, wp):
    """Residual low and high runs in the kept light: list of (sign, centre, half span, peak |z|). Both signs are collected (mirror rule)."""
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
        for g in np.split(hit, np.where(np.diff(hit) > 1)[0] + 1):
            a, e = tk.min() + g[0] * b, tk.min() + (g[-1] + 1) * b
            out.append((sign, (a + e) / 2, (e - a) / 2, float(np.max(sign * z.loc[g]))))
    return out


def complement(t, f, keep, c, P):
    """Boolean mask (True = remove) of runs that recur at the same binary phase in a different cycle of this sector, for period P. Built from f only; the caller applies it to both arms."""
    wp = c["wp"] if c is not None else np.nan; T0 = c["T0"] if c is not None else 0.0
    off = refit(t, f, c) if c is not None else 0.0
    runs = find_runs(t, f, keep, wp)
    ph = [((tc - T0 - off) / P) % 1.0 for _, tc, _, _ in runs]; cyc = [np.floor((tc - T0 - off) / P + 0.5) for _, tc, _, _ in runs]
    tol = TOL_H / 24
    rec = []
    for i, (sign, tc, hs, zp) in enumerate(runs):
        hit = False
        for j, (s2, tc2, hs2, _) in enumerate(runs):
            if j != i and s2 == sign and cyc[j] != cyc[i] and max(hs, hs2) <= WRATIO * min(hs, hs2) and max(zp, runs[j][3]) <= ZRATIO * min(zp, runs[j][3]):
                d = min(abs(ph[i] - ph[j]), 1 - abs(ph[i] - ph[j])) * P
                hit |= d < hs + hs2 + tol
        if hit:
            rec.append((zp, ph[i], hs * (1 + PAD) + 0.5 / 24))
    out = np.zeros(len(t), bool); used = 0.0
    for zp, p0, half in sorted(rec, reverse=True):
        if used + 2 * half / P > CAP:
            continue
        used += 2 * half / P
        pt = ((t - T0 - off) / P) % 1.0
        out |= np.minimum(np.abs(pt - p0), 1 - np.abs(pt - p0)) * P <= half
    return out


def remove(t, f, periods, c):
    """Boolean mask (True = remove) for one star-sector: catalogue windows plus the repeat lane, for the catalogue period and for every other period of the star."""
    if c is not None and not np.isfinite(c.get("wp", np.nan)):
        c = None
    rm = windows(t, c)[0] if c is not None else np.zeros(len(t), bool)
    Ps = ([c["P"]] if c is not None else []) + [P for P in periods if c is None or abs(P / c["P"] - 1) >= 0.02]
    for P in Ps:
        cc = c if (c is not None and abs(P / c["P"] - 1) < 0.02) else None
        rm |= complement(t, f, ~rm, cc, P)
    return rm


def old_removed(t, f, periods):
    """Cadences the Vesper 0.8.1 mask removes (eclipse_mask_auto on the given light, one period after the other), as a boolean over the ORIGINAL t."""
    from detect_v2 import eclipse_mask_auto
    idx = np.arange(len(t)); gone = np.zeros(len(t), bool)
    for P in periods:
        keep, _ = eclipse_mask_auto(t[idx], f[idx], P)
        gone[idx[~keep]] = True; idx = idx[keep]
    return gone


def intervals(t, flag):
    """[[t_start, t_end], ...] of runs of consecutive cadences with flag True (gaps larger than 3 cadences split a run)."""
    if not flag.any():
        return []
    gap = 3 * float(np.median(np.diff(t)))
    tt = t[flag]; cut = np.where(np.diff(tt) > gap)[0]
    lo = np.r_[tt[0], tt[cut + 1]]; hi = np.r_[tt[cut], tt[-1]]
    return [[round(float(a), 4), round(float(b), 4)] for a, b in zip(lo, hi)]


def mask_runs(t, f, periods, tic):
    """Same return shape as stage2_search.mask_runs, plus an info dict stored in the group meta: catalogue period P, epoch T0, this sector's primary offset (for the event veto) and the recovered-light
    intervals. runs are empty (the chain's eclipse-distance fields are then not available, as in the C0 to C2 tests)."""
    c = cat().get(int(tic))
    if c is not None and not np.isfinite(c.get("wp", np.nan)):
        c = None
    rm = remove(t, f, periods, c)
    # recovered light must be the same for both arms AND chosen without favouring either: the old mask cuts LOW phases of the real arm, so cadences picked from the real arm alone are low-flux spots and
    # the real arm would get more events there by construction (seen in the first development counts, 11 Nov). The union of the cuts the old mask makes on f and on 2 - f is unchanged by the flip.
    old = old_removed(t, f, periods) | old_removed(t, 2 - f, periods)
    if c is not None:
        P, T0, off = float(c["P"]), float(c["T0"]), refit(t, f, c)
    else:
        P, T0, off = (float(periods[0]) if len(periods) else float("nan")), 0.0, 0.0
    info = dict(P=P, T0=T0, off=round(off, 5), cat=c is not None, n_removed=int(rm.sum()), recovered=intervals(t, old & ~rm))
    return t[~rm], f[~rm], [(p, []) for p in periods], info


def in_recovered(center, intervals_):
    return any(a <= center <= b for a, b in intervals_)


# ---------------------------------------------------------------- event veto (part 3)
def veto_events(ev):
    """ev = DataFrame of the PRIMARY events of a run (columns tic, kind, sector, center, dur_h, depth_ppm, p1_P, p1_T0, p1_off). Returns a bool array, True = vetoed. Real events are judged against
    real events, upside-down against upside-down (one code, both arms). Binaries of P under 13 d are never vetoed."""
    out = np.zeros(len(ev), bool); pos = {ix: n for n, ix in enumerate(ev.index)}
    need = ev[ev["p1_P"].notna() & (ev["p1_P"] >= VETO_PSLOW)]
    for _, g in need.groupby(["tic", "kind"]):
        ix, sec = g.index.values, g["sector"].values.astype(int)
        Ps = g["p1_P"].values.astype(float)
        ph = ((g["center"].values - g["p1_T0"].values - g["p1_off"].values) / Ps) % 1.0
        d = g["dur_h"].values.astype(float); a = np.abs(g["depth_ppm"].values.astype(float)) + 1e-9
        for i in range(len(g)):
            oth = np.where(sec != sec[i])[0]
            nmin = VETO_NMIN if len(set(sec[oth])) >= 3 else 1          # a star with 3 or more other sectors: a real eclipse returns in at least NMIN of them
            hits = set()
            for j in oth:
                dist_h = min(abs(ph[i] - ph[j]), 1 - abs(ph[i] - ph[j])) * Ps[i] * 24
                if dist_h < (d[i] + d[j]) / 2 + VETO_TOL_H and max(d[i], d[j]) <= VETO_DUR_R * min(d[i], d[j]) and max(a[i], a[j]) <= VETO_DEP_R * min(a[i], a[j]):
                    hits.add(int(sec[j]))
            out[pos[ix[i]]] = len(hits) >= nmin
    return out


# ---------------------------------------------------------------- self-test (synthetic light only)
def selftest():
    rng = np.random.default_rng(5)
    t = np.arange(0, 27, 2 / 1440); P = 6.0
    f = 1 + rng.normal(0, 1000e-6, t.size)
    ecl = np.zeros(t.size, bool)
    for k in range(5):                                   # an eclipse the catalogue does not know, 5 h wide, 4 cycles in the sector
        ecl |= np.abs(t - (2.2 + k * P)) < 2.5 / 24
    f[ecl] -= 0.02
    dip = np.abs(t - 20.9) < 4 / 24; f[dip] -= 0.004      # a planet-like single dip, 8 h, 4 x the per-cadence scatter x 4 (visible, never repeats)
    rm = remove(t, f, [P], None)                          # star without a catalogue width: the repeat lane alone
    assert rm[ecl].mean() > 0.9, f"repeat lane left the recurring eclipse: removed {rm[ecl].mean():.2f}"
    assert rm[dip].mean() < 0.05, f"repeat lane removed the single dip: {rm[dip].mean():.2f}"
    assert (remove(t, 2 - f, [P], None) == rm).all(), "mirror rule broken: the mask of 2 - f differs"
    c = dict(P=P, T0=2.2, eT0=np.nan, eP=np.nan, wp=5 / 24, ws=np.nan, phs=np.nan)
    w, sec_ok = windows(t, c); assert w[ecl].mean() > 0.99 and not sec_ok and w[dip].mean() < 0.05
    f2 = f.copy(); f2[ecl] += 0.02                         # same star, eclipse known: catalogue windows alone remove it, the single dip stays
    assert remove(t, f2, [P], c)[ecl].mean() > 0.99 and remove(t, f2, [P], c)[dip].mean() < 0.05
    ev = pd.DataFrame([dict(tic=1, kind="real", sector=s, center=ph0 + 20 * s, dur_h=5.0, depth_ppm=9000.0, p1_P=20.0, p1_T0=0.0, p1_off=0.0)
                       for s, ph0 in ((1, 3.0), (2, 3.0), (3, 3.0), (4, 11.0))] + [dict(tic=2, kind="real", sector=s, center=3.0 + 10 * s, dur_h=5.0, depth_ppm=9000.0, p1_P=10.0, p1_T0=0.0, p1_off=0.0) for s in (1, 2, 3)])
    v = veto_events(ev)
    assert list(v) == [True, True, True, False, False, False, False], list(v)    # recurring at the same phase is vetoed (4 sectors: 3 others, NMIN 2); the other phase and P under 13 d are kept
    print("petrova_mask selftest passed")


if __name__ == "__main__":
    selftest()
