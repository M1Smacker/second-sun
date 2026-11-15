"""One-off Book 3.0 migration (Claude, 15 Nov 2026; Ahmed's decisions in research/stage3/REDESIGN-DECISIONS-2026-11-15.md).
- removes Book 2's textbook (book/, parts/, the old learn pages) and the Story-so-far set (start/), Quests and Progress;
  all of them stay readable in the frozen Book 2 at /v2/ (book/archive-v2, tag book-2-final);
- rewrites every link in the kept pages that pointed at a removed page so it opens the same place in /v2/;
- writes small redirect pages at the old addresses (old links open the Tree or the new Learning home), each noindex
  and marked <meta name="ss-redirect"> so the orphan check knows them;
- moves data/path.yml to data/path-book2.yml (the Book 2 chapter scaffolding is retired; kept as record).
Run once from book/: python tools/book3_migrate.py   (refuses to run twice)."""
import os, re, shutil, subprocess, sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REMOVE_DIRS = ["book", "parts", "start"]
REMOVE_FILES = ["quests.md", "progress.md", "learn/l1-dip-depth.md"]

if not (DOCS / "book").exists():
    sys.exit("already migrated (docs/book is gone)")


def url_of(rel):                                   # docs-relative md path -> built URL path (use_directory_urls)
    p = PurePosixPath(rel)
    if p.name == "index.md":
        return (str(p.parent) + "/") if str(p.parent) != "." else ""
    return str(p.with_suffix("")) + "/"


removed = []
for d in REMOVE_DIRS:
    removed += [p.relative_to(DOCS).as_posix() for p in (DOCS / d).rglob("*.md")]
removed += [f for f in REMOVE_FILES if (DOCS / f).exists()]
removed_set = set(removed)

LINK = re.compile(r"(\]\()([^)\s]+?\.md)(#[^)\s]*)?(\))")
changed = 0
for md in DOCS.rglob("*.md"):
    rel = md.relative_to(DOCS).as_posix()
    if rel in removed_set:
        continue
    text = md.read_text(encoding="utf-8")
    here_url = url_of(rel)

    def fix(m):
        global changed
        target = os.path.normpath(os.path.join(os.path.dirname(rel), m.group(2))).replace("\\", "/")
        if target not in removed_set:
            return m.group(0)
        changed += 1
        dest = "v2/" + url_of(target)
        up = "../" * here_url.count("/")
        return f"{m.group(1)}{up}{dest}{m.group(3) or ''}{m.group(4)}"
    new = LINK.sub(fix, text)
    if new != text:
        md.write_text(new, encoding="utf-8")

STUB = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow">'
        '<meta name="ss-redirect" content="book3"><meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{to}">'
        '<title>Moved</title></head><body><p>This page moved in Book 3.0. <a href="{to}">Continue</a>. The old page is in the '
        '<a href="{v2}">frozen Book 2</a>.</p></body></html>\n')
stubs = 0
for rel in removed:
    u = url_of(rel)
    dest = "learn/" if rel.startswith(("book/", "parts/", "learn/")) else ""
    up = "../" * u.count("/")
    out = DOCS / u / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(STUB.format(to=up + dest, v2=up + "v2/" + u), encoding="utf-8")
    stubs += 1

for d in REMOVE_DIRS:
    for p in (DOCS / d).rglob("*"):
        if p.is_file() and p.suffix != ".html":
            p.unlink()
for f in REMOVE_FILES:
    if (DOCS / f).exists():
        (DOCS / f).unlink()
for d in REMOVE_DIRS:                              # drop now-empty folders (images of removed chapters included)
    for p in sorted((DOCS / d).rglob("*"), key=lambda x: -len(x.parts)):
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()
if (ROOT / "data" / "path.yml").exists():
    (ROOT / "data" / "path.yml").rename(ROOT / "data" / "path-book2.yml")
print(f"removed {len(removed)} pages, rewrote {changed} links to /v2/, wrote {stubs} redirect pages, retired data/path.yml")
