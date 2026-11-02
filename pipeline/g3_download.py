"""G3 download (Ahmed's go to the download, 2 Nov 2026 night; research/stage3/G3-PREREGISTRATION.md). The 612 stars of targets/g3_targets.csv.
Same method as g2_download.py (the development download): every SPOC 2-min, TESS-SPOC and QLP light-curve file of every star, one folder per star in D:\\second-sun\\data\\g3\\<tic>\\,
appended to data\\g3\\manifest.csv. RESUMABLE (files on disk with the right size are skipped; a finished star leaves a _done file). NO light curve is opened or read here: this script only fetches
and counts bytes. Stops if the total passes 30 GB (estimate 5 to 15 GB). Each finished star adds one row to research\\downloads.csv.
Usage: python g3_download.py [n_threads]    (Ahmed, 2 Nov 2026 night: normal priority, not low; 12 threads)
"""
import os, sys, csv, time, threading, datetime, pathlib, warnings
import requests
import lightkurve as lk
from astroquery.mast import Observations
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings("ignore")
Observations.TIMEOUT = 120          # FIX-QUEUE 72: a hung MAST query fails in 2 min (the default is 600) and safe_star retries it
STUCK_S = 20 * 60                   # FIX-QUEUE 72: no star finished for this long: print STUCK and exit with code 3 (rerun resumes)
OUT = pathlib.Path(r"D:\second-sun\data\g3")        # never data\g2: the G2 manifest decides QLP windows (FIX-QUEUE 70)
LOG = pathlib.Path(r"D:\second-sun\research\downloads.csv")
MANIFEST = OUT / "manifest.csv"
LIMIT = 30 * 1024**3
WANT = {"SPOC": 120, "TESS-SPOC": None, "QLP": None}     # author -> required exposure (s), None = any
lock = threading.Lock()
total = [0]


def tics():
    with open(r"D:\second-sun\targets\g3_targets.csv", encoding="utf-8") as fh:
        rows = list(csv.DictReader(l for l in fh if not l.startswith("#")))
    sealed = sorted({int(r["tic"]) for r in rows})
    assert len(sealed) == 612, f"the G3 list should have 612 stars, found {len(sealed)}"
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
            raise SystemExit("30 GB limit reached: stop and ask Ahmed")
    (d / "_done").write_text(str(nf))
    with lock, open(LOG, "a", newline="") as fh:
        csv.writer(fh).writerow([datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                 f"G3 TIC {tic}: {nf} light-curve files (SPOC 2-min, TESS-SPOC, QLP)", "https://mast.stsci.edu",
                                 nb, str(d), "G3 star list (Ahmed said you can download them tonight, 2026-11-02); file list in data\\g3\\manifest.csv", "g3"])
    return tic, nf, nb


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_star(tic, tries=4, wait=30):
    """FIX-QUEUE 72: one star's MAST timeout no longer kills the run. Retry with growing waits; after the last try report the star as failed (-1)."""
    for attempt in range(tries):
        try:
            return do_star(tic)
        except Exception as e:
            print(f"{now()} TIC {tic} try {attempt + 1}/{tries} failed: {type(e).__name__}: {str(e)[:100]}", flush=True)
            time.sleep(wait * (attempt + 1))
    return tic, -1, 0


def watchdog(state):
    """FIX-QUEUE 72: heartbeat line every minute; exit non-zero when no star has finished for STUCK_S."""
    while True:
        time.sleep(60)
        idle = time.time() - state["last"]
        print(f"{now()} heartbeat: {state['done']} stars done, last one {idle / 60:.0f} min ago", flush=True)
        if idle > STUCK_S:
            print(f"STUCK: no star finished for {STUCK_S // 60} minutes; exiting with code 3 (rerun resumes)", flush=True)
            os._exit(3)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    if not MANIFEST.exists():
        MANIFEST.write_text("tic,author,file,bytes,path\n")
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    todo = tics()
    state = {"done": 0, "last": time.time()}
    threading.Thread(target=watchdog, args=(state,), daemon=True).start()
    failed = []
    with ThreadPoolExecutor(n) as ex:
        for fu in as_completed([ex.submit(safe_star, t) for t in todo]):
            tic, nf, nb = fu.result()
            if nf < 0:
                failed.append(tic)
            state["done"] += 1; state["last"] = time.time()
            if state["done"] % 10 == 0 or state["done"] == len(todo):
                print(f"{now()} {state['done']}/{len(todo)} stars; new bytes this run {total[0] / 1e9:.2f} GB", flush=True)
    if failed:
        print(f"FAILED STARS ({len(failed)}): {failed}  (rerun to retry them)", flush=True)
        sys.exit(2)
    print("ALL DONE", flush=True)
