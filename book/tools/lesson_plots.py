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
            tt.append(t[m].mean()); ff.append(np.median(f[m]))
    return np.array(tt), np.array(ff)


def write(name, tic, sector, t, f, title, note, unit="percent"):
    rel = f / np.median(f)
    y = (rel - 1) * 100 if unit == "percent" else rel
    doc = {"tic": tic, "sector": sector, "title": title, "note": note, "x": "Time (days, TESS clock)", "y": "Brightness change (%)" if unit == "percent" else "Brightness (1 = normal)",
           "unit": unit, "t": [round(v, 4) for v in t], "f": [round(v, 4) for v in y],
           "source": f"TESS sector {sector}, SPOC 2-minute light curve (PDCSAP), quality flags removed; MAST"}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
    print(f"{name}: {len(t)} points, {min(y):.3f} to {max(y):.3f}")


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
