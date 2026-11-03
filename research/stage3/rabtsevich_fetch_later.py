"""Fetch his two later preprints (L 279-94 and KIC 3755522; 150 KB and 164 KB) from Zenodo into data/rabtsevich_zenodo/later/. Usage: python -I rabtsevich_fetch_later.py"""
import urllib.request, pathlib, hashlib
UA = {"User-Agent": "Mozilla/5.0 (SecondSun research)"}
d = pathlib.Path("D:/second-sun/data/rabtsevich_zenodo/later"); d.mkdir(exist_ok=True)
for rid, key, out in ((23509748, "Rabtsevich_2026_L279-94_TIC100796276.pdf", "l279-94.pdf"), (23807946, "manuscript.pdf", "kic3755522.pdf")):
    b = urllib.request.urlopen(urllib.request.Request(f"https://zenodo.org/records/{rid}/files/{key}?download=1", headers=UA), timeout=60).read()
    (d / out).write_bytes(b); print(out, len(b), hashlib.sha256(b).hexdigest()[:12])
