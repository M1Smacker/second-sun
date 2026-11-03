"""Fetch the S110 preregistration README and short PDF from Zenodo record 23175179 into data/rabtsevich_zenodo/ and print the creators of his other records. Usage: python -I rabtsevich_fetch_prereg.py"""
import urllib.request, urllib.parse, json, pathlib, hashlib
UA = {"User-Agent": "Mozilla/5.0 (SecondSun research)"}
out = pathlib.Path("D:/second-sun/data/rabtsevich_zenodo")
for key in ("README.md", "PREREG_S110_SHORT.pdf"):
    b = urllib.request.urlopen(urllib.request.Request(f"https://zenodo.org/records/23175179/files/{key}?download=1", headers=UA), timeout=60).read()
    (out / ("prereg_s110_" + key)).write_bytes(b); print(key, len(b), hashlib.sha256(b).hexdigest()[:12])
for rid in (23807946, 23807813, 23509748, 23415929, 23290795, 23175179):
    m = json.load(urllib.request.urlopen(urllib.request.Request(f"https://zenodo.org/api/records/{rid}", headers=UA), timeout=60))["metadata"]
    print(rid, m.get("publication_date"), [c.get("name") for c in m.get("creators", [])], "|", m.get("title")[:100])
