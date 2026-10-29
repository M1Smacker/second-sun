"""Known-planet test data for the Vesper study (Ahmed said yes on 29 Oct 2026): every SPOC 2-min, TESS-SPOC and QLP light curve of one star NOT in G1 or G2, into data\\known\\<tic>.
Same choice of files as g1_download.py; every file is logged in research\\downloads.csv. Usage: python known_download.py <tic>"""
import sys, csv, pathlib, datetime, urllib.request
import lightkurve as lk

ROOT = pathlib.Path(r"D:\second-sun")
WANT = {"SPOC": 120, "TESS-SPOC": None, "QLP": None}


def main(tic):
    for f in ("g1_targets.csv", "g2_targets.csv"):
        assert f"\n{tic}," not in (ROOT / "targets" / f).read_text() and f",{tic}," not in (ROOT / "targets" / f).read_text(), f"TIC {tic} is in {f}: not a free test star"
    out = ROOT / "data" / "known" / str(tic); out.mkdir(parents=True, exist_ok=True)
    tab = lk.search_lightcurve(f"TIC {tic}", author=list(WANT)).table
    n, size = 0, 0
    for r in tab:
        a, fn = str(r["author"]), str(r["productFilename"])
        if a not in WANT or (WANT[a] and int(r["exptime"]) != WANT[a]) or not fn.endswith(".fits"):
            continue
        dest = out / fn
        if not dest.exists():
            urllib.request.urlretrieve("https://mast.stsci.edu/api/v0.1/Download/file?uri=" + str(r["dataURI"]), dest)
        n += 1; size += dest.stat().st_size
    with open(ROOT / "research" / "downloads.csv", "a", newline="") as fh:
        csv.writer(fh).writerow([datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), f"Known circumbinary planet host TIC {tic}: {n} light-curve files (SPOC 2-min, TESS-SPOC, QLP)",
                                 "https://mast.stsci.edu", size, str(out), "Vesper study known-planet test set (Ahmed said yes 29 Oct 2026); not in G1 or G2", "study"])
    print(f"TIC {tic}: {n} files, {size / 1e6:.1f} MB -> {out}")


if __name__ == "__main__":
    main(int(sys.argv[1]))
