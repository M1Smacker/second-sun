"""Deck for the real-layout rehearsal (Eyes ladder rung 3; research/stage3/REHEARSAL-V1.md; written 2 Nov 2026).
8 sessions of 20 items. Every item is a window of REAL TESS light (a development-slice binary, PDCSAP flux) with at most one hidden thing planted in it; no TIC number, no sector and no time
is stored in the deck, only anonymous flux arrays. Classes (the six answer buttons of the vetting brief): planet (a fake planet: 3 clear and 3 near the limit per session), eclipse (a real eclipse
of the binary), instrument (a ramp after a gap or a dip that ends at a gap), flare (fast rise, slow decay, brighter), step (a level change that stays), noise (nothing hidden: the best wiggle the
hunt's own box search finds in a different part of the sector).  Windows are +- max(1 d, 3 x box); P1 is the whole sector in 1 h bins, P2 the window in 6 min bins, P3 the binary phase.
Usage: SS_SET=g2 python make_rehearsal_deck.py [out.json]     (writes book/docs/assets/rehearsal-deck.json and research/stage3/rehearsal-deck-audit.txt; needs the development light curves on this PC)"""
import os, sys, json, glob, random, pathlib
os.environ.setdefault("SS_SET", "g2")
import numpy as np, pandas as pd
import dataset as DS, stage3_core as C, detect_v2 as D
from audit_paths import noise
from scipy.stats import rankdata

SEED, NSESS = 20261102, 8
PLAN = [("planet", "clear", 3), ("planet", "near", 3), ("eclipse", "", 3), ("instrument", "", 3), ("flare", "", 2), ("step", "", 2), ("noise", "", 4)]    # 20 per session
BOXES = (3, 4, 5, 6.5, 8, 10, 12, 15)
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else C.ROOT / "book" / "docs" / "assets" / "rehearsal-deck.json"
AUDIT = C.ROOT / "research" / "stage3" / "rehearsal-deck-audit.txt"
rng = np.random.default_rng(SEED)


def trapezoid(t, tc, dur_h, depth):
    d = dur_h / 24; r = np.clip((d / 2 - np.abs(t - tc)) / (0.2 * d), 0, 1)
    return -depth * 1e-6 * r


def grid_mean(t, f, lo, hi, step):
    """Mean flux (ppm about 1) on a regular grid; None where there are no points."""
    n = int(round((hi - lo) / step)); k = np.floor((t - lo) / step).astype(int); ok = (k >= 0) & (k < n) & np.isfinite(f)
    s = np.bincount(k[ok], weights=(f[ok] - 1) * 1e6, minlength=n)[:n]; c = np.bincount(k[ok], minlength=n)[:n]
    return [None if c[i] == 0 else int(round(s[i] / c[i])) for i in range(n)]


def sector_files(tic):
    return sorted(glob.glob(str(DS.DATA / str(tic) / "*.fits")))


class Star:
    """One loaded star-sector: raw normalized flux, eclipse bookkeeping, noise."""
    def __init__(self, tic, path, eph, widths):
        t, f, n, info = D.load(path, info=True)
        self.ok = info["product"] in ("SPOC", "TESS-SPOC") and (t.max() - t.min()) > 20 and len(t) > 5000
        if not self.ok:
            return
        self.tic, self.t, self.f = tic, t, f
        self.t0P = eph.by.get(tic, [(np.nan, np.nan, np.nan)])[0][:2]
        w = widths.get(tic)
        self.wp, self.ws = (w if w else (np.nan, np.nan))
        self.n8 = noise(t, f, 8.0)
        self.eph, self.cad = eph, float(np.median(np.diff(t)))
        self.gaps = [(t[i], t[i + 1]) for i in np.where(np.diff(t) > 0.25)[0]]
        self.ok = bool(np.isfinite(self.n8) and np.isfinite(self.wp) and np.isfinite(self.t0P[0]))

    def eclipses(self):
        """[(start, end, centre, kind)] of catalogue eclipses inside the data (primary at phase 0, secondary at 0.5)."""
        t0, P = self.t0P; out = []
        for k in range(int((self.t.min() - t0) / P) - 1, int((self.t.max() - t0) / P) + 2):
            for off, wd, kind in ((0.0, self.wp, "primary"), (0.5, self.ws, "secondary")):
                c = t0 + (k + off) * P; h = max(wd * P, 0.04) / 2 * 1.3
                if self.t.min() + 0.3 < c < self.t.max() - 0.3:
                    out.append((c - h, c + h, c, kind))
        return out

    def free(self, tc, dur_h, half_d):
        """True if a window around tc is inside the data and holds no catalogue eclipse and no big gap."""
        lo, hi = tc - half_d, tc + half_d
        if lo < self.t.min() + 0.2 or hi > self.t.max() - 0.2:
            return False
        if any(a < hi and b > lo for a, b, _, _ in self.eclipses()) or any(a < hi and b > lo for a, b in self.gaps):
            return False
        return (np.sum((self.t >= lo) & (self.t <= hi)) / (2 * half_d / self.cad)) > 0.9


def build(star, cls, tier, k_hint):
    """One item or None. Returns the item dict (no identifying fields)."""
    t, f = star.t.copy(), star.f.copy(); n8 = star.n8; box = float(rng.choice(BOXES)); meta = {}
    half = max(1.0, 3 * box / 24)
    if cls in ("planet", "flare", "step", "noise"):
        for _ in range(300):
            tc = float(rng.uniform(t.min() + half + 0.3, t.max() - half - 0.3))
            if star.free(tc, box, half):
                break
        else:
            return None
    if cls == "planet":
        K = float(rng.uniform(13, 24) if tier == "clear" else rng.uniform(6.5, 9.5)); dep = K * n8
        f = f * (1 + trapezoid(t, tc, box, dep)); meta = dict(depth_ppm=int(round(dep)), strength=round(K, 1), box_h=box)
    elif cls == "flare":
        A = float(rng.uniform(8, 25)) * n8 * 1e-6; tau = float(rng.uniform(0.4, 2.0)) / 24; dt = t - tc
        f = f * (1 + np.where(dt >= 0, A * np.exp(-dt / tau), np.where(dt > -0.004, A * (1 + dt / 0.004), 0.0))); meta = dict(amp_ppm=int(round(A * 1e6)), box_h=box)
    elif cls == "step":
        s = float(rng.choice([-1, 1]) * rng.uniform(6, 14)) * n8 * 1e-6
        f = f * (1 + np.where(t >= tc, s, 0.0)); meta = dict(step_ppm=int(round(s * 1e6)), box_h=box)
    elif cls == "eclipse":
        ecl = [e for e in star.eclipses() if abs(e[2] - t.min()) > 0.3 and (e[1] - e[0]) > 0.04]
        rng.shuffle(ecl)
        for a, b, c, kind in ecl:
            half_e = max(1.0, 3 * ((b - a) * 24) / 24)
            if c - half_e < t.min() + 0.2 or c + half_e > t.max() - 0.2:
                continue
            inn = (np.abs(t - c) < (b - a) / 4); out = ((np.abs(t - c) > (b - a)) & (np.abs(t - c) < half_e))
            if inn.sum() < 5 or out.sum() < 20:
                continue
            depth = (np.nanmedian(f[out]) - np.nanmedian(f[inn])) * 1e6
            if 300 <= depth <= 80000:                                  # visible as a dip, not so deep that it fills the panel
                tc, box = c, min(BOXES, key=lambda x: abs(x - (b - a) * 24 / 1.3)); half = half_e; meta = dict(depth_ppm=int(round(depth)), kind=kind, box_h=box); break
        else:
            return None
    elif cls == "instrument":
        gs = [g for g in star.gaps if g[0] > t.min() + 1.5 and g[1] < t.max() - 1.5]
        if not gs:
            return None
        g = gs[int(rng.integers(len(gs)))]; A = float(rng.uniform(8, 20)) * n8 * 1e-6
        if rng.random() < 0.6:                                          # ramp after the data resume: scattered light and thermal settling
            tau = float(rng.uniform(0.15, 0.5)); dt = t - g[1]
            f = f * (1 - np.where(dt >= 0, A * np.exp(-dt / tau), 0.0)); tc = g[1] + tau / 2; kind = "ramp after a gap"
        else:                                                           # a dip that ends where the data stop (pointing jitter before a momentum dump)
            L = float(rng.uniform(0.15, 0.5)); dt = t - g[0]
            f = f * (1 - np.where((dt <= 0) & (dt >= -L), A, 0.0)); tc = g[0] - L / 2; kind = "dip ending at a gap"
        box = min(BOXES, key=lambda x: abs(x - max(3.0, 24 * (tau if kind.startswith("ramp") else L)))); half = max(1.0, 3 * box / 24); meta = dict(kind=kind, box_h=box)
        if tc - half < t.min() + 0.2 or tc + half > t.max() - 0.2:
            return None
    elif cls == "noise":
        tt, ff = D.detrend(t, f); bd = D.bin_width(tt); bt, bf = D.bin10(tt, ff, bd)
        c, snr, _ = D.box_scores(bt, bf, box, bin_d=bd); snr = np.nan_to_num(snr, nan=-9)
        for i in np.argsort(-snr)[:400]:
            if star.free(float(c[i]), box, half):
                tc = float(c[i]); meta = dict(strength=round(float(snr[i]), 1), box_h=box); break
        else:
            return None
    lo, hi = tc - half, tc + half
    p2 = grid_mean(t, f, lo, hi, 1 / 240)
    ts0 = float(np.floor(t.min()))
    p1 = grid_mean(t, f, ts0, ts0 + 28, 1 / 24)
    bin30 = [v for v in grid_mean(t, f, t.min(), t.max(), 1 / 48) if v is not None]
    sig = float(1.4826 * np.median(np.abs(np.diff(bin30))) / np.sqrt(2)) if len(bin30) > 50 else float(n8)
    ecl_ivs = [[round(a - ts0, 3), round(b - ts0, 3)] for a, b, _, _ in star.eclipses()]
    t0, P = star.t0P; ph = float(((tc - t0) / P) % 1.0)
    return dict(cls=cls, tier=tier or None, meta=meta, box_h=box, t_lo=round(lo - ts0, 4), t_hi=round(hi - ts0, 4), tc=round(tc - ts0, 4), p2=p2, p1=p1, p1_t0=0.0, sigma=round(sig, 1),
                ecl=ecl_ivs, phase=round(ph, 4), wp=round(float(star.wp), 4), ws=round(float(star.ws), 4), star=0)


def main():
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic"); dev = tg[tg["slice"] == "dev"]
    eph = C.Ephem(tg, C.eb_widths()); widths = C.eb_widths(); tics = [int(x) for x in dev.tic]; rng.shuffle(tics)
    need = {(cls, tier): n * NSESS for cls, tier, n in PLAN}; got = {k: [] for k in need}; sid = 0; seen = 0
    for tic in tics:
        if all(len(got[k]) >= need[k] for k in need):
            break
        files = sector_files(tic); rng.shuffle(files)
        for path in files[:2]:
            try:
                s = Star(tic, path, eph, widths)
            except Exception:
                continue
            if not s.ok:
                continue
            seen += 1; sid += 1; used = 0
            keys = list(need); rng.shuffle(keys)
            for key in keys:                                           # at most 3 items from one star-sector, so the deck holds many different stars
                if used >= 3:
                    break
                if len(got[key]) >= need[key]:
                    continue
                it = build(s, key[0], key[1], None)
                if it is not None:
                    it["star"] = sid; got[key].append(it); used += 1
    short = {k: (len(v), need[k]) for k, v in got.items() if len(v) < need[k]}
    assert not short, f"not enough items: {short}"
    sessions = []
    for si in range(NSESS):
        items = []
        for (cls, tier), v in got.items():
            n = dict(((c, t), x) for c, t, x in PLAN)[(cls, tier)]
            items += v[si * n:(si + 1) * n]
        rng.shuffle(items); sessions.append(items)
    # no two neighbouring items of one star (the page also reshuffles with this rule)
    deck = dict(v=1, made="2026-11-02", seed=SEED, classes=["planet", "eclipse", "instrument", "flare", "step", "noise"], sessions=sessions)
    OUT.write_text(json.dumps(deck, separators=(",", ":")), encoding="utf-8")
    # leak audit: can a simple feature separate planets from non-planets without looking at the picture? (0.5 = no; the strength of the dip itself is legitimately informative)
    rows = []
    for si, items in enumerate(sessions):
        for it in items:
            p2 = np.array([np.nan if v is None else v for v in it["p2"]], float); fin = np.isfinite(p2)
            rows.append(dict(planet=it["cls"] == "planet", box=it["box_h"], sigma=it["sigma"], gapfrac=1 - fin.mean(), phase=min(it["phase"], 1 - it["phase"]), pos=(it["tc"] - it["t_lo"]) / (it["t_hi"] - it["t_lo"]),
                             nmin=np.nanmin(p2) / it["sigma"], nrange=(np.nanmax(p2) - np.nanmin(p2)) / it["sigma"], p1gap=sum(v is None for v in it["p1"])))
    df = pd.DataFrame(rows)
    def auc(x, y):
        r = rankdata(x); n1 = y.sum(); n0 = len(y) - n1
        return (r[y.values].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    lines = [f"Rehearsal deck audit (seed {SEED}): {NSESS} sessions x 20 items; planets {int(df.planet.sum())}, others {int((~df.planet).sum())}; star-sectors used {sid}; deck {OUT.stat().st_size / 1e6:.2f} MB",
             "AUC of one simple feature separating planets from all other items (0.5 = cannot tell; the dip's own depth in noise units, nmin, is allowed to separate, it is the signal):"]
    for c in ("box", "sigma", "gapfrac", "phase", "pos", "p1gap", "nmin", "nrange"):
        lines.append(f"  {c:8s} AUC {auc(df[c].fillna(df[c].median()), df.planet):.2f}")
    lines.append("classes per session (should be 3+3 planets, 3 eclipse, 3 instrument, 2 flare, 2 step, 4 noise): " + str([{c: sum(i['cls'] == c for i in s) for c in deck['classes']} for s in sessions][0]))
    AUDIT.write_text("\n".join(lines) + "\n", encoding="utf-8"); print("\n".join(lines))


if __name__ == "__main__":
    main()
