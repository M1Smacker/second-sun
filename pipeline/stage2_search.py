"""Stage 2: trial search of about 50 G1 stars (Ahmed approved 2026-10-23: "Approve Stage 2 ... Stop and report before Stage 3").
FIRST REAL-DATA SEARCH. Real events are written ONLY to D:\\second-sun\\data\\stage2\\ (git-ignored). Never commit them; publish aggregates only.
Per (star, sector) group, every available product (SPOC 2-min, TESS-SPOC, QLP) is searched on the real curve and on the upside-down curve:
all catalogue periods masked, QLP limited to borrowed good-time windows, events flagged (gap edge, momentum dump, upside-down match, burst of
the same moment on other stars), distance to the masked eclipses recorded (leakage check), and the same dip looked up in the OTHER products
(rule C8). One dip is also injected into every product at the same time, to measure how many real dips each check would lose.
Usage: python stage2_search.py select | run [n_procs] | check"""
import sys, json, csv, pathlib, warnings, multiprocessing as mp
import numpy as np, pandas as pd
import lightkurve as lk
import audit_all as A
import dataset as DS
from detect_v2 import (load, eclipse_mask_auto, find_events, detrend, bin10, bin_width, box_scores, DURS_H, veto,
                       good_windows, in_windows)
from audit_paths import noise

warnings.filterwarnings("ignore")
OUT = pathlib.Path(r"D:\second-sun\data\stage2")
GROUPS = OUT / "groups"
STARS = pathlib.Path(r"D:\second-sun\targets\stage2_stars.csv")
CONTROLS = {"Kepler-16": 299096355, "Kepler-38": 158316612, "Kepler-64": 170348142, "Kepler-453": 164457525, "Kepler-1647": 170344769}
BURST_D, FLIP_BURST_MIN = 0.1, 3


def select():
    per = pd.read_csv(r"D:\second-sun\research\audit-2026-10-23\per_star.csv")
    tg = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#").drop_duplicates("tic").set_index("tic")
    man = pd.read_csv(r"D:\second-sun\data\g1\manifest.csv").drop_duplicates("file")
    has_spoc = set(man[man.author == "SPOC"].tic)
    rows = [dict(tic=t, name=n, stratum="control") for n, t in CONTROLS.items()]
    pool = per[(per.best_rmin <= 15) & ~per.tic.isin(CONTROLS.values())].copy()
    pool["stratum"] = pd.cut(pool.tmag, [0, 11, 12, 14], right=False, labels=["bright<11", "mid11-12", "faint12+"])
    rng = np.random.default_rng(20261023)
    for s, g in pool.groupby("stratum", observed=True):
        for t in rng.choice(g.tic.values, size=min(15, len(g)), replace=False):
            rows.append(dict(tic=int(t), name="", stratum=s))
    df = pd.DataFrame(rows)
    df["kic"] = df.tic.map(tg.kic); df["tmag"] = df.tic.map(tg.tmag); df["has_spoc"] = df.tic.isin(has_spoc)
    df["best_rmin"] = df.tic.map(per.set_index("tic").best_rmin)
    df.to_csv(STARS, index=False)
    print(df.groupby("stratum", observed=True).agg(n=("tic", "size"), spoc=("has_spoc", "sum"), tmag=("tmag", "median"),
                                                  rmin=("best_rmin", "median")).to_string())


class Prod:
    """One product of one star-sector, prepared once: eclipses masked, detrended, binned; scores cached per box length."""
    def __init__(self, t, f, sign=1):
        self.t, self.f = t, (f if sign == 1 else 2 - f)
        tt, ff = detrend(self.t, self.f)
        self.bd = bin_width(tt); self.bt, self.bf = bin10(tt, ff, self.bd); self.cache = {}
        self.med = np.nanmedian(self.bf)

    def scores(self, d):
        if d not in self.cache:
            self.cache[d] = box_scores(self.bt, self.bf, d, bin_d=self.bd)
        return self.cache[d]

    def events(self, thr=7.0):                                   # same logic as detect_v2.find_events, on cached scores
        cands = []
        for d in DURS_H:
            c, snr, m = self.scores(d)
            for i in np.where(np.nan_to_num(snr) >= thr)[0]:
                cands.append((snr[i], c[i], d, (self.med - m[i]) * 1e6))
        cands.sort(reverse=True); ev = []
        for snr, c, d, depth in cands:
            if all(abs(c - e["center"]) > 0.5 * max(d, e["dur_h"]) / 24 + 0.1 for e in ev):
                ev.append(dict(center=float(c), dur_h=d, snr=float(snr), depth_ppm=float(depth)))
        return ev

    def snr_near(self, center, dur_h):
        c, snr, _ = self.scores(dur_h)
        sel = (np.abs(c - center) < 0.5 * dur_h / 24 + 0.1) & np.isfinite(snr)
        return float(np.max(snr[sel])) if sel.any() else np.nan

    def snr_near_any(self, center):
        v = [self.snr_near(center, d) for d in DURS_H]
        return float(np.nanmax(v)) if np.isfinite(v).any() else np.nan


def mask_runs(t, f, periods):
    out = []
    for P in periods:
        keep, runs = eclipse_mask_auto(t, f, P)
        out.append((P, runs)); t, f = t[keep], f[keep]
    return t, f, out


def ecl_dist(center, runs_all):
    """Days (and eclipse widths) from a time to the nearest masked eclipse of any period of the star (0 inside a run)."""
    best = (np.nan, np.nan)
    for P, runs in runs_all:
        ph = (center % P) / P
        for a, b in runs:
            d = 0.0 if a <= ph <= b else min(abs(ph - a), abs(ph - b), abs(ph - a + 1), abs(ph - b - 1), abs(ph - a - 1), abs(ph - b + 1))
            if not np.isfinite(best[0]) or d * P < best[0]:
                best = (d * P, (b - a) * P)
    return best[0], (best[0] / best[1] if best[1] else np.nan)


S = {}


def _init():
    A._init()
    man = pd.read_csv(DS.MANIFEST).drop_duplicates("file")       # dataset.py: G1 by default, G2 when SS_SET=g2
    sp = man[man.author == "SPOC"]
    S["spoc_by_sector"] = {}
    for r in sp.itertuples():
        S["spoc_by_sector"].setdefault(int(r.file.split("-s")[1][:4]), r.path)
    a = pd.read_csv(DS.AUDIT / "audit_all.csv")
    S["burst"] = {}                                              # (sector, camera) -> (centres, tics) of upside-down events of ALL stars
    for r in a[a.flipped_events > 0].itertuples():
        for item in str(r.flipped_centers).split():
            S["burst"].setdefault((r.sector, r.camera), ([], []))
            S["burst"][(r.sector, r.camera)][0].append(float(item.split(":")[0])); S["burst"][(r.sector, r.camera)][1].append(r.tic)
    S["burst"] = {k: (np.array(v[0]), np.array(v[1])) for k, v in S["burst"].items()}
    S["dumps"] = {}


def dumps_for(sector):
    if sector not in S["dumps"]:
        p = S["spoc_by_sector"].get(sector)
        if p is None:
            S["dumps"][sector] = np.array([])
        else:
            lc = lk.read(p, quality_bitmask="none"); t = lc.time.value; q = np.asarray(lc.quality.value, int)
            d = t[(q & 32) > 0]; S["dumps"][sector] = d[np.isfinite(d)]
    return S["dumps"][sector]


def burst_n(sector, camera, center, own_tic):
    c, tics = S["burst"].get((sector, camera), (np.array([]), np.array([])))
    near = np.abs(c - center) < BURST_D
    return len(set(tics[near]) - {own_tic})


def prepare(path):
    path = pathlib.Path(path); tic = A.tic_of(path.name)
    t, f, nfill, info = load(str(path), info=True)
    sec, cam, ccd = A.head(path)
    meta = dict(tic=tic, file=path.name, product=info["product"], sector=sec, camera=cam, ccd=ccd, column=info["column"],
               cadence_min=info["cadence_min"], win_src="")
    if info["needs_windows"]:
        nbw, nn = A.neighbour_windows(sec, cam, ccd, tic)
        own = next((p for p in path.parent.glob(f"tess*-s{sec:04d}-{tic:016d}-*_lc.fits")), None)
        if own is not None:
            k = in_windows(t, good_windows(str(own))); meta["win_src"] = "own SPOC"
        elif nn >= 2:
            k = in_windows(t, nbw); meta["win_src"] = "neighbours"
        else:
            return None, {**meta, "status": "no safe windows"}
        t, f = t[k], f[k]
    if len(t) < 200:
        return None, {**meta, "status": "too little data"}
    dt = np.diff(t); edges = np.concatenate([t[:-1][dt > 0.25], t[1:][dt > 0.25], [t.min(), t.max()]])
    t, f, runs = mask_runs(t, f, A.PER.get(tic, []))
    if len(t) < 200:
        return None, {**meta, "status": "too little data after masking"}
    return dict(t=t, f=f, runs=runs, edges=edges, meta=meta), {**meta, "status": "ok", "n_searched": len(t)}


def do_group(args):
    tic, sector, paths = args
    out = GROUPS / f"{tic}_{sector}.json"
    if out.exists():
        return str(out)
    res = dict(tic=tic, sector=sector, meta=[], events=[], inj=[])
    prods = {}
    for p in paths:
        try:
            d, m = prepare(p)
        except Exception as e:
            res["meta"].append(dict(file=pathlib.Path(p).name, status=f"ERROR {type(e).__name__}: {str(e)[:80]}")); continue
        res["meta"].append(m)
        if d is not None:
            d["real"], d["flip"] = Prod(d["t"], d["f"]), Prod(d["t"], d["f"], -1)
            prods[d["meta"]["product"]] = d
    dumps = dumps_for(sector)
    for name, d in prods.items():
        m = d["meta"]
        real, flip = d["real"].events(), d["flip"].events()
        none = np.array([])
        kept_r, _ = veto(real, d["edges"], dumps, flip, flip_action="flag")
        kept_f, _ = veto(flip, d["edges"], dumps, [], flip_action="flag")
        for kind, evs, key in (("real", kept_r, "real"), ("flip", kept_f, "flip")):
            for e in evs:
                others = [o for n2, o in prods.items() if n2 != name]
                c8 = [o[key].snr_near(e["center"], e["dur_h"]) for o in others]
                c8 = [x for x in c8 if np.isfinite(x)]
                ed, ew = ecl_dist(e["center"], d["runs"])
                res["events"].append(dict(kind=kind, tic=tic, sector=sector, camera=m["camera"], ccd=m["ccd"], product=name,
                                          column=m["column"], center=round(e["center"], 4), dur_h=e["dur_h"], snr=round(e["snr"], 2),
                                          depth_ppm=round(e["depth_ppm"]), flags="; ".join(e["flags"]),
                                          ecl_d=ed, ecl_w=ew, c8_best=max(c8) if c8 else None, c8_n=len(c8),
                                          burst_n=burst_n(sector, m["camera"], e["center"], tic)))
    # injection: the SAME dip in every product at the same time (what a real astrophysical dip would do)
    if prods:
        a = max(prods.values(), key=lambda d: d["t"].max() - d["t"].min())
        seg = np.split(np.arange(len(a["t"])), np.where(np.diff(a["t"]) > 0.25)[0] + 1)
        s = max(seg, key=lambda i: a["t"][i[-1]] - a["t"][i[0]]); tc = 0.5 * (a["t"][s[0]] + a["t"][s[-1]])
        n8 = noise(a["t"], a["f"], 8.0)
        if np.isfinite(n8):
            depth = float(np.clip(12 * n8, 1500, 40000)); snr_inj = {}
            for name, d in prods.items():
                fi = d["f"].copy(); fi[np.abs(d["t"] - tc) < 4 / 24] -= depth * 1e-6
                snr_inj[name] = Prod(d["t"], fi).snr_near_any(tc)
            for na, sa in snr_inj.items():
                for nb, sb in snr_inj.items():
                    if na != nb:
                        res["inj"].append(dict(tic=tic, sector=sector, A=na, B=nb, depth_ppm=round(depth), snr_A=sa, snr_B=sb))
    json.dump(res, open(out, "w"), default=lambda o: None if o != o else float(o))
    return str(out)


def groups():
    st = pd.read_csv(STARS)
    g = {}
    for tic in st.tic:
        for p in sorted((DS.DATA / str(tic)).glob("*.fits")):
            sec = A.head(p)[0]
            g.setdefault((int(tic), int(sec)), []).append(str(p))
    return [(t, s, ps) for (t, s), ps in sorted(g.items())]


def safe(a):
    try:
        return do_group(a)
    except Exception as e:
        return f"ERROR {a[0]} {a[1]}: {type(e).__name__}: {str(e)[:100]}"


if __name__ == "__main__":
    mode = sys.argv[1]
    OUT.mkdir(parents=True, exist_ok=True); GROUPS.mkdir(exist_ok=True)
    if mode == "select":
        select()
    elif mode == "check":                                        # Prod.events() must equal detect_v2.find_events on the same data
        _init(); tic, sec, paths = groups()[0]
        d, m = prepare(paths[0]); ev = find_events(d["t"], d["f"]); pe = Prod(d["t"], d["f"]).events()
        assert len(ev) == len(pe) and all(abs(a["center"] - b["center"]) < 1e-6 and abs(a["snr"] - b["snr"]) < 1e-6 for a, b in zip(ev, pe)), (ev[:2], pe[:2])
        print("check ok:", len(ev), "events identical in Prod.events() and find_events() on", m["file"][:40])
    else:
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
        gl = groups(); print(f"{len(gl)} star-sector groups", flush=True)
        with mp.Pool(n, initializer=_init) as pool:
            for i, r in enumerate(pool.imap_unordered(safe, gl), 1):
                if r.startswith("ERROR"):
                    print(r, flush=True)
                if i % 25 == 0:
                    print(f"{i}/{len(gl)}", flush=True)
        print("STAGE2 SEARCH DONE", flush=True)
