"""Fetch the 116 KB Research Note PDF from Zenodo record 22967456 into data/rabtsevich_zenodo/ and extract its text (never opened in the browser pane). Usage: python -I rabtsevich_fetch_note.py"""
import urllib.request, pathlib, hashlib
out = pathlib.Path("D:/second-sun/data/rabtsevich_zenodo")
req = urllib.request.Request("https://zenodo.org/records/22967456/files/manuscript.pdf?download=1", headers={"User-Agent": "Mozilla/5.0 (SecondSun research)"})
b = urllib.request.urlopen(req, timeout=60).read(); (out / "manuscript_note.pdf").write_bytes(b)
print(len(b), "bytes", hashlib.sha256(b).hexdigest()[:12])
try:
    from pypdf import PdfReader
except ImportError:
    raise SystemExit("pypdf not installed")
r = PdfReader(str(out / "manuscript_note.pdf")); t = "\n\n".join(p.extract_text() for p in r.pages)
(out / "manuscript_note.txt").write_text(t, encoding="utf-8"); print(len(r.pages), "pages", len(t), "chars")
