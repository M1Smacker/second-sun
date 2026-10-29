"""Stage 1 audit of ALL G1 star-sectors (Ahmed approved 2026-10-23). NOT a search: real-data events are never recorded.
Per light-curve file in data\\g1: what the loader did (product, flux column, cadence), camera/CCD, the borrowed good-time
windows (QLP), noise of box means at 3, 6.5 and 15 h, the planet radius that reaches SNR 7 in one 6.5 h crossing, one injected
standard dip (8 h, 3,000 ppm) and whether it came back, and events on the FLIPPED curve (centres kept, to calibrate the
same-moment filter). Every catalogue period of the star is masked (B3). RESUMABLE: rows already in the output CSV are skipped.
Usage:  python audit_all.py windows            build the SPOC good-time-window database (pickle)
        python audit_all.py run [n_procs]      audit every file (default 8 processes)
Output: research\\audit-2026-10-23\\audit_all.csv, spoc_windows.pkl"""
import sys, re, csv, pickle, pathlib, warnings, multiprocessing as mp
import numpy as np
from astropy.io import fits
from detect_v2 import (load, mask_all_periods, find_events, good_windows, in_windows, intersect_windows)
from audit_paths import noise
import dataset as DS

warnings.filterwarnings("ignore")
DATA = DS.DATA                                                   # dataset.py: G1 by default, G2 when SS_SET=g2
OUT = DS.AUDIT
WIN_DB = OUT / "spoc_windows.pkl"
RESULT = OUT / "audit_all.csv"
INJ_H, INJ_PPM, R_EARTH_PER_RSUN = 8.0, 3000.0, 109.08
FIELDS = ["tic", "file", "product", "sector", "camera", "ccd", "column", "cadence_min", "n_loaded", "n_filled", "win_src",
          "win_nn", "win_loo_cover", "win_loo_extra", "n_periods", "n_searched", "rstar_rsun", "noise_3h_ppm", "noise_6.5h_ppm",
          "noise_15h_ppm", "depth7_ppm", "rmin7_rearth", "inj_center", "inj_found", "inj_snr", "inj_depth_ppm",
          "flipped_events", "flipped_max_snr", "flipped_centers", "status"]


def g1_tables():
    rad = {}
    for r in csv.DictReader(l for l in open(r"D:\second-sun\targets\g1_targets.csv") if not l.startswith("#")):
        rad.setdefault(int(r["tic"]), float(r["tic_radius_rsun"] or "nan"))
    per = {}
    for r in csv.DictReader(open(r"D:\second-sun\research\wave-3-pipeline\g1_tmag.csv")):     # ALL catalogue periods (B3)
        if r["tic"].strip().isdigit() and int(r["tic"]) in rad and float(r["p_bin"]) > 0.2:
            per.setdefault(int(r["tic"]), set()).add(round(float(r["p_bin"]), 6))
    return rad, {k: sorted(v, reverse=True) for k, v in per.items()}


def g2_tables():
    """Same two tables for the G2 stars: radius (not in the TESS catalogue, so nan) and ALL catalogue periods of the star (B3), from every row of the TESS eclipsing binary catalogue with that TIC."""
    import pandas as pd
    tg = pd.read_csv(DS.TARGETS, comment="#").drop_duplicates("tic")
    rad = {int(t): float("nan") for t in tg.tic}
    eb = pd.read_csv(DS.ROOT / "data" / "xmatch" / "ebs.csv")
    per = {}
    for t, p in zip(eb.TIC, eb.Per):
        if int(t) in rad and float(p) > 0.2:
            per.setdefault(int(t), set()).add(round(float(p), 6))
    return rad, {k: sorted(v, reverse=True) for k, v in per.items()}


def tic_of(name):
    m = re.search(r"(?:s\d{4}-|[-_])(\d{16})", name)
    return int(m.group(1)) if m else None


def head(path):
    h = fits.getheader(path, 0)
    return h.get("SECTOR"), h.get("CAMERA"), h.get("CCD")


def is_spoc2(p):
    return p.name.startswith("tess") and p.name.endswith("_lc.fits")


def files():
    return sorted(p for p in DATA.rglob("*.fits") if tic_of(p.name))


def _win(p):
    sec, cam, ccd = head(p)
    try:
        return (sec, cam, ccd, tic_of(p.name), good_windows(str(p)))
    except Exception:
        return None


def build_windows(n):
    OUT.mkdir(parents=True, exist_ok=True)
    spoc = [p for p in files() if is_spoc2(p)]
    with mp.Pool(n) as pool:
        rows = [r for r in pool.imap_unordered(_win, spoc, chunksize=8) if r]
    db = {}
    for sec, cam, ccd, tic, w in rows:
        db.setdefault((sec, cam, ccd), {})[tic] = w
    pickle.dump(db, open(WIN_DB, "wb"))
    print(f"windows for {len(rows)} SPOC files in {len(db)} sector/camera/CCD groups; "
          f"groups with >=2 stars: {sum(len(v) >= 2 for v in db.values())}")


DB, RAD, PER = {}, {}, {}


def _init():
    global DB, RAD, PER
    DB = pickle.load(open(WIN_DB, "rb")); RAD, PER = g1_tables() if DS.NAME == "g1" else g2_tables()


def neighbour_windows(sec, cam, ccd, exclude):
    lists = [w for tic, w in DB.get((sec, cam, ccd), {}).items() if tic != exclude and w]
    return (intersect_windows(lists), len(lists)) if lists else ([], 0)


def audit(path):
    path = pathlib.Path(path)
    tic = tic_of(path.name)
    t, f, nfill, info = load(str(path), info=True)
    sec, cam, ccd = head(path)
    row = dict(tic=tic, file=path.name, product=info["product"], sector=info["sector"], camera=cam, ccd=ccd,
               column=info["column"], cadence_min=info["cadence_min"], n_loaded=len(t), n_filled=nfill, win_src="",
               win_nn="", win_loo_cover="", win_loo_extra="")
    if info["needs_windows"]:
        nbw, nn = neighbour_windows(sec, cam, ccd, tic)
        own = next((p for p in path.parent.glob(f"tess*-s{sec:04d}-{tic:016d}-*_lc.fits")), None)
        if own is not None:
            ow = good_windows(str(own))
            k_own, k_nb = in_windows(t, ow), in_windows(t, nbw) if nbw else np.zeros(len(t), bool)
            if nn >= 2:                                              # leave-one-out: how good would borrowed windows have been?
                row["win_loo_cover"] = round(float((k_own & k_nb).sum() / max(k_own.sum(), 1)), 3)
                row["win_loo_extra"] = round(float((k_nb & ~k_own).sum() / max(k_nb.sum(), 1)), 3)
            t, f = t[k_own], f[k_own]; row.update(win_src="own SPOC", win_nn=nn)
        elif nn >= 2:
            k = in_windows(t, nbw); t, f = t[k], f[k]; row.update(win_src="neighbours", win_nn=nn)
        elif nn == 1:
            k = in_windows(t, nbw); t, f = t[k], f[k]; row.update(win_src="ONE neighbour (weak)", win_nn=nn)
        else:
            row.update(win_src="NONE (unsafe)", win_nn=0)
    periods = PER.get(tic, [])
    rstar = RAD.get(tic, float("nan"))
    row.update(n_periods=len(periods), rstar_rsun=rstar)
    if len(t) < 200:
        return {**row, "n_searched": len(t), "status": "too little data"}
    t, f = mask_all_periods(t, f, periods)
    row["n_searched"] = len(t)
    if len(t) < 200:
        return {**row, "status": "too little data after masking"}
    for d in (3, 6.5, 15):
        row[f"noise_{d}h_ppm"] = round(noise(t, f, d), 1)
    n65 = row["noise_6.5h_ppm"]
    row["depth7_ppm"] = round(7 * n65, 0) if n65 == n65 else ""
    row["rmin7_rearth"] = round(rstar * np.sqrt(7 * n65 * 1e-6) * R_EARTH_PER_RSUN, 2) if n65 == n65 and rstar == rstar else ""
    seg = np.split(np.arange(len(t)), np.where(np.diff(t) > 0.25)[0] + 1)
    s = max(seg, key=lambda i: t[i[-1]] - t[i[0]])
    tc = 0.5 * (t[s[0]] + t[s[-1]])
    fi = f.copy(); fi[np.abs(t - tc) < INJ_H / 48] -= INJ_PPM * 1e-6
    ev = [e for e in find_events(t, fi) if abs(e["center"] - tc) < 0.3]
    row.update(inj_center=round(tc, 3), inj_found=bool(ev), inj_snr=round(ev[0]["snr"], 1) if ev else "",
               inj_depth_ppm=round(ev[0]["depth_ppm"]) if ev else "")
    fl = find_events(t, 2 - f)                                       # flipped curve only: real-data events are NOT recorded
    row.update(flipped_events=len(fl), flipped_max_snr=round(max((e["snr"] for e in fl), default=0), 1),
               flipped_centers=" ".join(f"{e['center']:.3f}:{e['snr']:.1f}" for e in fl), status="ok")
    return row


def safe_audit(p):
    try:
        return audit(p)
    except Exception as e:
        return dict(tic=tic_of(pathlib.Path(p).name), file=pathlib.Path(p).name, status=f"ERROR {type(e).__name__}: {str(e)[:80]}")


def run(n):
    done = set()
    if RESULT.exists():
        done = {r["file"] for r in csv.DictReader(open(RESULT))}
    todo = [p for p in files() if p.name not in done]
    new = not RESULT.exists()
    print(f"{len(todo)} files to audit ({len(done)} already done)", flush=True)
    with open(RESULT, "a", newline="") as fh, mp.Pool(n, initializer=_init) as pool:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new:
            w.writeheader()
        for i, row in enumerate(pool.imap_unordered(safe_audit, todo, chunksize=4), 1):
            w.writerow(row)
            if i % 50 == 0:
                fh.flush(); print(f"{i}/{len(todo)}", flush=True)
    print("AUDIT DONE", flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    build_windows(n) if mode == "windows" else run(n)
