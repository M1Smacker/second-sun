"""G3 star list, step T111b: download the two small catalogue tables of the TESS Ten Thousand Catalog (Kostov et al. 2025, ApJS 279, 50; CC BY 4.0) with plain HTTP (never a browser).
Ahmed said yes on 2 Nov 2026 (tables only, no light curves). Saves to data\\g3\\catalog_ttc (a new folder; the files are untrusted text: read them only with explicit parsing), writes size and sha256 to the
folder's MANIFEST.txt and appends one row per file to research\\downloads.csv. Usage: python g3_catalog_download.py"""
import csv, datetime, hashlib, pathlib, sys
import requests

ROOT = pathlib.Path(r"D:\second-sun")
DEST = ROOT / "data" / "g3" / "catalog_ttc"
BASE = "https://content.cld.iop.org/journals/0067-0049/279/2/50/revision1/"
FILES = {"table3_new_ebs.txt": "apjsade2d8t3_mrt.txt", "table4_known_ebs.txt": "apjsade2d8t4_mrt.txt"}
HEAD = {"User-Agent": "Mozilla/5.0 (SecondSun research; contact via GitHub M1Smacker)"}
LIMIT = 60 * 1024 * 1024                                         # refuse anything over 60 MB: these tables are expected to be 1 to 3 MB

DEST.mkdir(parents=True, exist_ok=True)
manifest, rows = [], []
for local, remote in FILES.items():
    url = BASE + remote
    h = requests.head(url, headers=HEAD, allow_redirects=True, timeout=60)
    size = int(h.headers.get("Content-Length", -1))
    print(local, "HEAD", h.status_code, h.headers.get("Content-Type"), "bytes", size, flush=True)
    if h.status_code != 200 or size > LIMIT:
        sys.exit(f"stop: {url} answered {h.status_code}, size {size}")
    r = requests.get(url, headers=HEAD, timeout=300)
    r.raise_for_status()
    data = r.content
    (DEST / local).write_bytes(data)
    sha = hashlib.sha256(data).hexdigest()
    manifest.append(f"{local}  {len(data)} bytes  sha256 {sha}  from {url}")
    rows.append([datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), f"G3 catalogue table {local} (TESS Ten Thousand Catalog, Kostov et al. 2025)", url, len(data), str(DEST / local),
                 "G3 star list source (T111b); Ahmed said yes on 2026-11-02; tables only, no light curves", "g3-catalogue"])
    print(local, "saved", len(data), "bytes sha256", sha[:16], flush=True)
(DEST / "MANIFEST.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
with open(ROOT / "research" / "downloads.csv", "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)
print("done", len(rows), "files")
