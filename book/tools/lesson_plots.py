"""Real TESS light for the Twinlight lessons (Claude, 15 Nov 2026).

Reads one SPOC light-curve file of a published system, bins it, and writes a small JSON that learn.js draws as an interactive plot.
Refuses any star on a hunt list (fence A, fence B, every G list) unless it is a published system on the allow list, so a sealed or blind
star can never reach a lesson. Run: .venv\\Scripts\\python.exe book\\tools\\lesson_plots.py
"""
import csv, json, sys
from pathlib import Path

import numpy as np
from astropy.io import fits

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book" / "docs" / "assets" / "data" / "lessons"
ALLOW = {260128333, 172900988, 299096355, 158316612, 170348142, 164457525, 170344769}   # published systems (as fence_check.py)


def hunt_ids():
    ids = set()
    for p in (ROOT / "targets").glob("*.csv"):
        with open(p, encoding="utf-8-sig") as f:
            rows = csv.DictReader(l for l in f if not l.startswith("#"))
            for r in rows:
                for k in ("tic", "TIC", "tic_id", "ticid"):
                    if r.get(k):
                        try:
                            ids.add(int(float(r[k])))
                        except ValueError:
                            pass
    return ids


def guard(tic):
    if tic in hunt_ids() and tic not in ALLOW:
        sys.exit(f"REFUSED: TIC {tic} is on a hunt list; lessons use published systems only")


def load(path, tic):
    guard(tic)
    with fits.open(path) as h:
        d, hdr = h[1].data, h[0].header
        assert int(hdr["TICID"]) == tic, f"file is TIC {hdr['TICID']}, not {tic}"
        t, f, q = d["TIME"], d["PDCSAP_FLUX"], d["QUALITY"]
        ok = np.isfinite(t) & np.isfinite(f) & (q == 0)
        return np.asarray(t[ok], float), np.asarray(f[ok], float), int(hdr["SECTOR"])


def binned(t, f, minutes):
    w = minutes / 1440
    k = np.floor((t - t[0]) / w).astype(int)
    tt, ff = [], []
    for i in np.unique(k):
        m = k == i
        if m.sum() >= 3:
            tt.append(t[m].mean()); ff.append(f[m].mean())   # plain average, the same operation lesson 1.3 teaches (Codex 017)
    return np.array(tt), np.array(ff)


def write(name, tic, sector, t, f, title, note, unit="percent", source=None):
    rel = f / np.median(f)
    y = {"percent": (rel - 1) * 100, "ppm": (rel - 1) * 1e6}.get(unit, rel)
    ylab = {"percent": "Brightness change (%)", "ppm": "Brightness change (ppm)"}.get(unit, "Brightness (1 = normal)")
    doc = {"tic": tic, "sector": sector, "title": title, "note": note, "x": "Time (days, TESS clock)", "y": ylab,
           "unit": unit, "t": [round(v, 4) for v in t], "f": [round(v, 4) for v in y],
           "source": source or f"TESS sector {sector}, SPOC 2-minute light curve (PDCSAP), quality flags removed; MAST"}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
    print(f"{name}: {len(t)} points, {min(y):.4g} to {max(y):.4g} {unit}")


if __name__ == "__main__":
    tic = 172900988
    src = ROOT / "data" / "known" / "172900988" / "tess2021284114741-s0044-0000000172900988-0215-s_lc.fits"
    t, f, s = load(src, tic)
    tb, fb = binned(t, f, 30)
    write("u1-sector", tic, s, tb, fb, "TIC 172900988, one TESS sector",
          "Each point is 30 minutes of light averaged. The deep drops are the two stars eclipsing each other.")
    # one eclipse up close: the deepest 30-minute point, plus or minus 0.6 days, at 10-minute bins
    c = tb[np.argmin(fb)]
    m = (t > c - 0.6) & (t < c + 0.6)
    te, fe = binned(t[m], f[m], 10)
    write("u1-eclipse", tic, s, te, fe * np.median(f) / np.median(f[(t > c - 3) & (t < c + 3)]), "One eclipse up close",
          "Each point is 10 minutes. The bottom of the dip is how much light was blocked.")
    # one quiet day, every 2-minute point (lesson 1.3, noise): the first full day (at least 700 points) at least 1 day away from both eclipses
    ecl = [2507.395, 2519.273]
    d0 = next(x for x in np.arange(np.ceil(t[0]), t[-1] - 1, 0.25)
              if ((t >= x) & (t < x + 1)).sum() >= 700 and all(abs(e - x) > 1.0 and abs(e - x - 1) > 1.0 for e in ecl))
    m = (t >= d0) & (t < d0 + 1)
    print("quiet day starts", d0)
    write("u1-quiet-day", tic, s, t[m], f[m], "One quiet day, every point",
          "Each point is 2 minutes. No eclipse here: the spread is noise.")
    tq, fq = binned(t[m], f[m], 30)
    write("u1-quiet-day-30", tic, s, tq, fq / np.median(fq) * np.median(f[m]), "The same day, 30-minute averages",
          "Each point averages 15 of the 2-minute points.")

    # the planet itself (lesson 1.4): sector 21, QLP full-frame light (30 min). The two dips sit 4.9 days apart, as Kostov et al. 2021 describe
    # ("transited the primary star and then 5 days later it transited the secondary star"); times found by our own scan, 15 Nov 2026.
    from scipy.ndimage import median_filter
    src = ROOT / "data" / "known" / "172900988" / "hlsp_qlp_tess_ffi_s0021-0000000172900988_tess_v01_llc.fits"
    guard(tic)
    with fits.open(src) as h:
        assert int(h[0].header["TICID"]) == tic
        d = h[1].data
        t2, f2, q2 = np.asarray(d["TIME"], float), np.asarray(d["SAP_FLUX"], float), d["QUALITY"]
    ok = np.isfinite(t2) & np.isfinite(f2) & (q2 == 0)
    t2, f2 = t2[ok], f2[ok]
    for name, c in (("u1-planet-a", 1883.39), ("u1-planet-b", 1888.31)):
        m = np.abs(t2 - c) < 1.0
        tt, ff = t2[m], f2[m] / np.median(f2[m])
        oot = np.abs(tt - c) > 0.35
        trend = np.interp(tt, tt[oot], median_filter(ff[oot], size=25, mode="nearest"))
        write(name, tic, 21, tt, ff / trend, "The planet crossing a star" + (" (first time)" if name.endswith("a") else ", 4.9 days later"),
              "Each point is 30 minutes. Slow changes are divided out, as in lesson 1.3.", unit="ppm",
              source="TESS sector 21, QLP full-frame light curve (30-minute), quality flags removed, slow changes divided out with the dip masked; MAST")

    # four sectors in a row (lesson 2.1, orbits and periods): sectors 44 to 47, 2-minute light, 1-hour averages
    import glob
    T, F = [], []
    for p in sorted(glob.glob(str(ROOT / "data" / "known" / "172900988" / "tess2021*-s004[4-7]-*_lc.fits"))):
        tt, ff, _ = load(p, tic)
        T.append(tt); F.append(ff / np.median(ff))
    tb4, fb4 = [], []
    for tt, ff in zip(T, F):
        a, b = binned(tt, ff, 60); tb4.append(a); fb4.append(b)
    write("u2-four-sectors", tic, 44, np.concatenate(tb4), np.concatenate(fb4), "Four TESS sectors in a row (44 to 47)",
          "Each point is 1 hour of light averaged. About 106 days, with a gap every 27 days.",
          source="TESS sectors 44 to 47, SPOC 2-minute light curves (PDCSAP), quality flags removed, each sector divided by its own median; MAST")
