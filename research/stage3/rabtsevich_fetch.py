"""Fetch the Zenodo READMEs of Rabtsevich's supporting record (v1.0.0 and v1.0.1) into data/rabtsevich_zenodo/. Small text files; Second Sun download rule: log it. Usage: python -I rabtsevich_fetch.py"""
import urllib.request, hashlib, pathlib, datetime
out = pathlib.Path("D:/second-sun/data/rabtsevich_zenodo"); out.mkdir(exist_ok=True)
jobs = {"v1.0.0": "https://zenodo.org/records/22967099/files/README.md?download=1", "v1.0.1": "https://zenodo.org/records/22999133/files/README.md?download=1"}
for tag, url in jobs.items():
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (SecondSun research; contact via GitHub M1Smacker)"})
    b = urllib.request.urlopen(req, timeout=60).read()
    (out / f"README_{tag}.md").write_bytes(b)
    print(tag, len(b), "bytes", hashlib.sha256(b).hexdigest()[:12], datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
