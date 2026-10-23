"""Kepler re-find test, step 1: download Kepler long-cadence (1,800 s) light curves for Kepler-16, -34, -35 from MAST.
Every file is logged in research/downloads.csv. Output: data/kepler-refind/."""
import csv, datetime, pathlib
import lightkurve as lk

OUT = pathlib.Path(r"D:\second-sun\data\kepler-refind")
LOG = pathlib.Path(r"D:\second-sun\research\downloads.csv")
STARS = {"Kepler-16": 12644769, "Kepler-34": 8572936, "Kepler-35": 9837578}

with open(LOG, "a", newline="") as fh:
    w = csv.writer(fh)
    for name, kic in STARS.items():
        sr = lk.search_lightcurve(f"KIC {kic}", mission="Kepler", author="Kepler", exptime=1800)
        lcs = sr.download_all(download_dir=str(OUT), quality_bitmask="none")
        for lc in lcs:
            p = pathlib.Path(lc.meta["FILENAME"])
            w.writerow([datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), f"{name} Kepler LC Q{lc.meta.get('QUARTER')}",
                        "https://mast.stsci.edu", p.stat().st_size, str(p), "Kepler re-find test (deep review 6)", "refind"])
        print(name, kic, "quarters:", sorted(lc.meta.get("QUARTER") for lc in lcs))
