"""Data-path audit (deep review 2026-10-23, section 10): before any search, check every G1 star-sector light curve.
Per file it records what the loader did (product, sector, cadence, flux column, cadences kept, good-time windows)
and what the detector can see there:
  - noise of box means at 3, 6.5 and 15 h (ppm), the same robust spread the search uses;
  - depth7_ppm: the 6.5 h dip depth that would reach SNR 7, and the planet radius that makes it on this star
    (TIC radius, no dilution correction, so a lower limit);
  - one injected standard dip (8 h, 3,000 ppm, placed in the middle of the longest kept stretch) and whether it comes back;
  - events on the flipped light curve (false-alarm proxy).
This is NOT a search: real-data events are not recorded. Usage:
  python audit_paths.py <out.csv> <file> [<file> ...]      (files are light curves of G1 stars; others are skipped)"""
import sys, re, csv, pathlib, warnings
import numpy as np
from detect_v2 import load, eclipse_mask_auto, find_events, detrend, bin10, bin_width, box_scores, good_windows, in_windows

warnings.filterwarnings("ignore")
G1 = {}
for r in csv.DictReader(l for l in open(r"D:\second-sun\targets\g1_targets.csv") if not l.startswith("#")):
    G1.setdefault(int(r["tic"]), []).append((float(r["p_bin_d"]), float(r["tic_radius_rsun"] or "nan")))
INJ_H, INJ_PPM = 8.0, 3000.0
R_EARTH_PER_RSUN = 109.08


def tic_of(path):
    m = re.search(r"(?:s\d{4}-|-)(\d{16})", pathlib.Path(path).name)
    return int(m.group(1)) if m else None


def spoc_twin(path, tic, sector):
    """A SPOC 2-min file of the same star and sector on disk, for QLP good-time windows."""
    for p in pathlib.Path(r"D:\second-sun\data").rglob(f"tess*-s{sector:04d}-{tic:016d}-*-s_lc.fits"):
        return str(p)
    return None


def noise(t, f, dur_h):
    tt, ff = detrend(t, f)
    bd = bin_width(tt)
    _, _, m = box_scores(*bin10(tt, ff, bd), dur_h, bin_d=bd)
    g = np.isfinite(m)
    return 1.4826 * np.median(np.abs(m[g] - np.median(m[g]))) * 1e6 if g.sum() >= 20 else np.nan


def audit(path):
    tic = tic_of(path)
    if tic not in G1:
        return None
    t, f, nfill, info = load(path, info=True)
    row = dict(tic=tic, file=pathlib.Path(path).name, **info, n_loaded=len(t), n_filled=nfill, windows="")
    if info["needs_windows"]:
        twin = spoc_twin(path, tic, info["sector"])
        if twin:
            k = in_windows(t, good_windows(twin)); t, f = t[k], f[k]; row["windows"] = "own SPOC"
        else:
            row["windows"] = "NONE (unsafe: scattered light)"
    for P, rstar in G1[tic]:                       # mask every catalogue period of this star
        keep, _ = eclipse_mask_auto(t, f, P); t, f = t[keep], f[keep]
    row.update(n_searched=len(t), rstar_rsun=rstar)
    if len(t) < 200:
        return {**row, "status": "too little data"}
    for d in (3, 6.5, 15):
        row[f"noise_{d}h_ppm"] = round(noise(t, f, d), 1)
    row["depth7_ppm"] = round(7 * row["noise_6.5h_ppm"], 0)
    row["rmin7_rearth"] = round(rstar * np.sqrt(row["depth7_ppm"] * 1e-6) * R_EARTH_PER_RSUN, 2) if rstar == rstar else ""
    gaps = np.where(np.diff(t) > 0.25)[0]
    seg = np.split(np.arange(len(t)), gaps + 1)
    s = max(seg, key=lambda i: t[i[-1]] - t[i[0]])
    tc = 0.5 * (t[s[0]] + t[s[-1]])
    fi = f.copy(); fi[np.abs(t - tc) < INJ_H / 48] -= INJ_PPM * 1e-6
    ev = [e for e in find_events(t, fi) if abs(e["center"] - tc) < 0.3]
    row.update(inj_center=round(tc, 3), inj_found=bool(ev), inj_snr=round(ev[0]["snr"], 1) if ev else "",
               inj_depth_ppm=round(ev[0]["depth_ppm"]) if ev else "")
    fl = find_events(t, 2 - f)
    row.update(flipped_events=len(fl), flipped_max_snr=round(max((e["snr"] for e in fl), default=0), 1), status="ok")
    return row


if __name__ == "__main__":
    out, files = sys.argv[1], sys.argv[2:]
    rows = []
    for p in files:
        try:
            r = audit(p)
        except Exception as e:                    # a broken file is a finding, not a crash
            r = dict(tic=tic_of(p), file=pathlib.Path(p).name, status=f"ERROR {type(e).__name__}: {e}")
        if r:
            rows.append(r); print({k: r.get(k) for k in ("tic", "sector", "product", "column", "cadence_min", "windows",
                                                         "noise_6.5h_ppm", "rmin7_rearth", "inj_found", "inj_snr",
                                                         "flipped_events", "status")})
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} star-sectors audited -> {out}")
