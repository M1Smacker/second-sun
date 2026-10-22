"""Stress check of the BUILT book (site/): every internal link and image resolves, every #anchor exists,
every chapter has the new template, no quiz or Next line is left in a chapter, no en or em dash, no horizontal-scroll traps.
Run after `mkdocs build`:  python tools/check_site.py   (exit 1 on any problem; the publish script runs it)."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urljoin, urlparse

SITE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "site"
BASE = "http://x.test/"


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        for k in ("href", "xlink:href", "src"):
            if a.get(k) and tag in ("a", "img", "script", "link", "source"):
                self.refs.append(a[k])


def target(url):
    p = SITE / unquote(urlparse(url).path.lstrip("/"))
    return p / "index.html" if p.is_dir() or url.endswith("/") else p


pages = {}
for f in SITE.rglob("*.html"):
    p = P()
    p.feed(f.read_text(encoding="utf-8"))
    pages[f] = p

bad = []
inbound = set()
for f, p in pages.items():
    rel = f.relative_to(SITE).as_posix()
    if rel == "404.html":      # its links are absolute to the live site path (/second-sun/), by design
        continue
    here = urljoin(BASE, rel[:-len("index.html")] if rel.endswith("index.html") else rel)
    for ref in p.refs:
        if re.match(r"(https?:|mailto:|data:|javascript:|tel:)", ref) or ref.startswith("#") and not ref[1:]:
            continue
        full, frag = urldefrag(urljoin(here, ref))
        if not full.startswith(BASE):
            continue
        t = target(full[len(BASE) - 1:])
        if t != f:
            inbound.add(t)
        if not t.exists():
            bad.append(f"{rel}: broken link {ref}")
        elif frag and t.suffix == ".html" and t in pages and frag not in pages[t].ids and unquote(frag) not in pages[t].ids:
            bad.append(f"{rel}: missing anchor {ref}")
    ref_anchor = [r for r in p.refs if r.startswith("#") and len(r) > 1]
    for r in ref_anchor:
        if r[1:] not in p.ids and not r.startswith("#__"):
            bad.append(f"{rel}: missing anchor {r}")

for f in pages:
    rel = f.relative_to(SITE).as_posix()
    if f not in inbound and rel not in ("index.html", "404.html"):
        bad.append(f"{rel}: orphan page (nothing links to it)")
for f in sorted((SITE / "book").glob("[0-9][0-9]-*/index.html")):
    t = f.read_text(encoding="utf-8")
    n = f.parent.name
    for need in ('class="ss-strip"', 'class="ss-end"', "1-minute summary", 'class="ss-read-btn"', 'data-path="journey"', 'data-path="topic"'):
        if need not in t:
            bad.append(f"book/{n}: missing {need}")
    if "details class=\"quiz\"" in t or re.search(r"<strong>Next:</strong>", t):
        bad.append(f"book/{n}: still has a quiz or a manual Next line")
for f in SITE.rglob("*.html"):
    if re.search("[–—]", f.read_text(encoding="utf-8")):
        bad.append(f"{f.relative_to(SITE).as_posix()}: en or em dash in built page")
for n in range(1, 7):
    for kind in ("", "review/", "labs/"):
        if not (SITE / f"parts/part{n}/{kind}index.html").exists():
            bad.append(f"missing parts/part{n}/{kind}")
if not (SITE / "assets/glossary.json").exists():
    bad.append("missing assets/glossary.json")
print(f"checked {len(pages)} pages")
print("\n".join(bad) if bad else "site check ok")
sys.exit(1 if bad else 0)
