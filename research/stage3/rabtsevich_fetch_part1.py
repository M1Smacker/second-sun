"""Fetch part1 (7 MB) of Rabtsevich's v1.0.0 supporting record into data/rabtsevich_zenodo/v1.0.0/, unzip, list text files, grep tool-workflow words. Usage: python -I rabtsevich_fetch_part1.py"""
import urllib.request, zipfile, pathlib, hashlib, re
UA = {"User-Agent": "Mozilla/5.0 (SecondSun research)"}
d = pathlib.Path("D:/second-sun/data/rabtsevich_zenodo/v1.0.0"); d.mkdir(exist_ok=True)
z = d / "part1_A_transits_archival_fpp.zip"
b = urllib.request.urlopen(urllib.request.Request("https://zenodo.org/records/22967099/files/part1_A_transits_archival_fpp.zip?download=1", headers=UA), timeout=180).read()
z.write_bytes(b); print(len(b), "bytes md5-check skipped, sha256", hashlib.sha256(b).hexdigest()[:12])
with zipfile.ZipFile(z) as zf:
    zf.extractall(d / "part1"); names = zf.namelist()
print(len(names), "files; top folders:", sorted({n.split('/')[0] for n in names}))
words = re.compile(r"Claude|Codex|ChatGPT|GPT|subagent|sub-agent|fresh session|clean session|prompt|agent|reviewer|audit pass|pass-3|pass 3", re.I)
hits = {}
for n in names:
    if n.lower().endswith((".md", ".txt")):
        t = (d / "part1" / n).read_text(encoding="utf-8", errors="ignore")
        c = len(words.findall(t))
        if c: hits[n] = c
for n, c in sorted(hits.items(), key=lambda x: -x[1])[:25]: print(c, n)
