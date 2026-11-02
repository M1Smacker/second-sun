"""Loom phase 0 (research/stage3/loom-literature-2026-11-03.md, plan changes 2): fingerprint every light-curve file of a star set so a run can name EXACTLY the data it read.
For each FITS file: size, sha256 (the only version pin for QLP, whose headers carry no release keyword), and the header keys SECTOR, CAMERA, CCD, DATA_REL, PROCVER, TICVER (DATA_REL and
PROCVER exist in SPOC and TESS-SPOC files, 2 Nov 2026 sample). Read-only on the data; touches no frozen pipeline file. Writes data\\<set>\\manifest_fp.csv.
Usage: python manifest_fingerprint.py g2 [procs]      (g1, g2 or g3; 8 workers is the 70% CPU setting while Ahmed is away)"""
import csv, glob, hashlib, os, pathlib, sys, time, warnings, multiprocessing as mp
warnings.filterwarnings("ignore")
from astropy.io import fits

ROOT = pathlib.Path(r"D:\second-sun")
FIELDS = ["tic", "file", "family", "bytes", "sha256", "sector", "camera", "ccd", "data_rel", "procver", "ticver", "error"]


def one(path):
    p = pathlib.Path(path)
    name = p.name
    fam = "QLP" if name.startswith("hlsp_qlp") else ("TESS-SPOC" if name.startswith("hlsp_tess-spoc") else "SPOC")
    row = dict(tic=p.parent.name, file=name, family=fam, bytes=p.stat().st_size, sha256="", sector="", camera="", ccd="", data_rel="", procver="", ticver="", error="")
    try:
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        row["sha256"] = h.hexdigest()
        h0, h1 = fits.getheader(p, 0), fits.getheader(p, 1)
        get = lambda k: h0.get(k, h1.get(k, ""))
        row.update(sector=get("SECTOR"), camera=get("CAMERA"), ccd=get("CCD"), data_rel=get("DATA_REL"), procver=get("PROCVER"), ticver=get("TICVER"))
    except Exception as e:
        row["error"] = f"{type(e).__name__}: {str(e)[:80]}"
    return row


if __name__ == "__main__":
    name = sys.argv[1]; procs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    data = ROOT / "data" / name
    files = sorted(glob.glob(str(data / "*" / "*.fits")))
    t0 = time.time()
    with mp.Pool(procs) as pool:
        rows = pool.map(one, files, chunksize=64)
    out = data / "manifest_fp.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, FIELDS); w.writeheader(); w.writerows(rows)
    gb = sum(r["bytes"] for r in rows) / 1e9
    bad = [r for r in rows if r["error"]]
    shas = {}
    for r in rows:
        shas.setdefault(r["sha256"], []).append(r["file"])
    dup = sum(len(v) - 1 for v in shas.values() if len(v) > 1 and v and r["sha256"])
    print(f"{name}: {len(rows)} files, {gb:.1f} GB, {time.time() - t0:.0f} s, unreadable or errors {len(bad)}, duplicate contents {dup}")
    for fam in ("SPOC", "TESS-SPOC", "QLP"):
        sub = [r for r in rows if r["family"] == fam]
        print(f"  {fam}: {len(sub)} files; distinct DATA_REL {len({r['data_rel'] for r in sub} - {''})}; distinct PROCVER {len({r['procver'] for r in sub} - {''})}")
    print("written", out)
