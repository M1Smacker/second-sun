"""Wave 2 hands-on: download one of each TESS product for two ground-truth stars, measure size + time.

Run:  set caches (see WAVE-BRIEF-COMMON.md), then  .venv\Scripts\python research\wave-2-data\handson_downloads.py
Writes: research\wave-2-data\handson_results.csv and appends rows to research\downloads.csv
"""
import csv, os, time, datetime, pathlib
import lightkurve as lk

ROOT = pathlib.Path(r"D:\second-sun")
DL = ROOT / "data" / "wave-2" / "lk"
DL.mkdir(parents=True, exist_ok=True)
OUT = ROOT / "research" / "wave-2-data" / "handson_results.csv"
LEDGER = ROOT / "research" / "downloads.csv"

# (label, target, search function, kwargs) -- one file each
JOBS = [
    ("SPOC 2-min LC",      "TIC 260128333", lk.search_lightcurve,      dict(author="SPOC", exptime=120, sector=98)),
    ("SPOC 20-s LC",       "TIC 260128333", lk.search_lightcurve,      dict(author="SPOC", exptime=20,  sector=98)),
    ("SPOC 2-min TPF",     "TIC 260128333", lk.search_targetpixelfile, dict(author="SPOC", exptime=120, sector=98)),
    ("TESScut 15x15 FFI",  "TIC 260128333", lk.search_tesscut,         dict(sector=98)),
    ("SPOC 2-min LC",      "TIC 299096355", lk.search_lightcurve,      dict(author="SPOC", exptime=120, sector=82)),
    ("TESS-SPOC FFI LC",   "TIC 299096355", lk.search_lightcurve,      dict(author="TESS-SPOC", sector=82)),
    ("QLP FFI LC",         "TIC 299096355", lk.search_lightcurve,      dict(author="QLP", sector=82)),
    ("TGLC FFI LC",        "TIC 260128333", lk.search_lightcurve,      dict(author="TGLC", sector=10)),
    ("TESScut 15x15 FFI",  "TIC 299096355", lk.search_tesscut,         dict(sector=82)),
]

rows = []
for label, target, fn, kw in JOBS:
    t0 = time.time()
    rec = dict(product=label, target=target, sector=kw.get("sector"), ok=False, seconds="", bytes="", path="", note="")
    try:
        sr = fn(target, **{k: v for k, v in kw.items() if k != "sector"} | ({"sector": kw["sector"]} if "sector" in kw else {}))
        if len(sr) == 0:
            rec["note"] = "no product found"
        else:
            if fn is lk.search_tesscut:
                obj = sr[0].download(cutout_size=15, download_dir=str(DL))
            else:
                obj = sr[0].download(download_dir=str(DL))
            path = pathlib.Path(obj.path if hasattr(obj, "path") else obj.meta.get("FILENAME", ""))
            rec.update(ok=True, path=str(path), bytes=path.stat().st_size if path.exists() else "")
            rec["note"] = f"{len(sr)} result(s); n_cadences={len(obj)}"
    except Exception as e:  # record, don't stop
        rec["note"] = f"ERROR {type(e).__name__}: {str(e)[:150]}"
    rec["seconds"] = round(time.time() - t0, 1)
    rows.append(rec)
    print(rec)

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%MZ")
with open(LEDGER, "a", newline="") as f:
    for r in rows:
        if r["ok"]:
            csv.writer(f).writerow([now, f"{r['product']} {r['target']} S{r['sector']}", "MAST via lightkurve",
                                    r["bytes"], r["path"].replace(str(ROOT) + "\\", ""), "wave 2 size/time measurement", "2"])
