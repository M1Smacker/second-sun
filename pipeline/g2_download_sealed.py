"""G2 SEALED slice download (Ahmed's go to the download, 30 Oct 2026; preregistration Amendment 1, commit 3947b18). The 594 sealed stars of targets/g2_targets.csv.
Same method as g2_download.py (the development download): every SPOC 2-min, TESS-SPOC and QLP light-curve file of every star, one folder per star in D:\\second-sun\\data\\g2\\<tic>\\,
appended to data\\g2\\manifest.csv. RESUMABLE (files on disk with the right size are skipped; a finished star leaves a _done file). NO light curve is opened or read here: this script only fetches
and counts bytes. Stops if the total passes 26 GB (estimate 16 to 17 GB). Each finished star adds one row to research\\downloads.csv.
Usage: python g2_download_sealed.py [n_threads]    (4 is polite to MAST)
"""
import sys, csv, time, threading, datetime, pathlib, warnings
import requests
import lightkurve as lk
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings("ignore")
OUT = pathlib.Path(r"D:\second-sun\data\g2")
LOG = pathlib.Path(r"D:\second-sun\research\downloads.csv")
MANIFEST = OUT / "manifest.csv"
LIMIT = 26 * 1024**3
WANT = {"SPOC": 120, "TESS-SPOC": None, "QLP": None}     # author -> required exposure (s), None = any
lock = threading.Lock()
total = [0]


def tics():
    with open(r"D:\second-sun\targets\g2_targets.csv", encoding="utf-8") as fh:
        rows = list(csv.DictReader(l for l in fh if not l.startswith("#")))
    sealed = sorted({int(r["tic"]) for r in rows if r["slice"] == "sealed"})
    assert len(sealed) == 594, f"the sealed slice should have 594 stars, found {len(sealed)}"
    return sealed


def wanted(row):
    a = str(row["author"]); fn = str(row["productFilename"])
    if a not in WANT or (WANT[a] and int(row["exptime"]) != WANT[a]):
        return False
    return fn.endswith("_lc.fits") or fn.endswith("_llc.fits")


def fetch(url, dest, size):
    if dest.exists() and dest.stat().st_size == size:
        return False
    tmp = dest.with_suffix(".part")
    for attempt in range(4):
        try:
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(tmp, "wb") as fh:
                    for chunk in r.iter_content(1 << 20):
                        fh.write(chunk)
            tmp.replace(dest)
            return True
        except Exception:
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"download failed: {dest.name}")


def do_star(tic):
    d = OUT / str(tic); d.mkdir(parents=True, exist_ok=True)
    if (d / "_done").exists():
        return tic, 0, 0
    sr = lk.search_lightcurve(f"TIC {tic}", author=list(WANT))
    rows = [r for r in sr.table if wanted(r)]
    nb = nf = 0
    for r in rows:
        dest = d / str(r["productFilename"]); size = int(r["size"])
        url = "https://mast.stsci.edu/api/v0.1/Download/file?uri=" + str(r["dataURI"])
        new = fetch(url, dest, size)
        nb += dest.stat().st_size; nf += 1
        with lock:
            total[0] += dest.stat().st_size if new else 0
            with open(MANIFEST, "a", newline="") as fh:
                csv.writer(fh).writerow([tic, r["author"], r["productFilename"], dest.stat().st_size, str(dest)])
        if total[0] > LIMIT:
            raise SystemExit("26 GB limit reached: stop and ask Ahmed")
    (d / "_done").write_text(str(nf))
    with lock, open(LOG, "a", newline="") as fh:
        csv.writer(fh).writerow([datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                 f"G2 sealed TIC {tic}: {nf} light-curve files (SPOC 2-min, TESS-SPOC, QLP)", "https://mast.stsci.edu",
                                 nb, str(d), "G2 sealed slice (Ahmed said go to the download on 2026-10-30); file list in data\\g2\\manifest.csv", "g2-sealed"])
    return tic, nf, nb


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    if not MANIFEST.exists():
        MANIFEST.write_text("tic,author,file,bytes,path\n")
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    todo = tics()
    done = 0
    with ThreadPoolExecutor(n) as ex:
        for tic, nf, nb in ex.map(do_star, todo):
            done += 1
            if done % 10 == 0 or done == len(todo):
                print(f"{done}/{len(todo)} stars; new bytes this run {total[0] / 1e9:.2f} GB", flush=True)
    print("ALL DONE", flush=True)
