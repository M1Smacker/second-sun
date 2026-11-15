"""Static verification for brief 016. Does not import the search pipeline."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "data/astra/016/site"
TOOLS = ROOT / "research/burn-3-book/tools"
source = (TOOLS / "site_check.mjs").read_text(encoding="utf-8")
pages = json.loads(re.search(r"const PAGES = (\[.*?\]);", source).group(1))
assert len(pages) == 15 and len(set(pages)) == 15
assert not re.search(r'"(?:start/|progress/|quests/|parts/|book/\d|learn/l1)', source)
for page in pages:
    html = (SITE / page / "index.html").read_text(encoding="utf-8")
    assert not re.search(r'<meta\s+name="ss-redirect"', html), page
print(f"Book 3 canonical pages exist without redirect markers: {len(pages)}")

publish = (TOOLS / "publish_book.ps1").read_text(encoding="utf-8")
mode_line = next(line for line in publish.splitlines() if 'foreach ($m in' in line)
assert '"tree"' in mode_line and '"chapter"' in mode_line
print("Publish list includes Tree and retained responsive chapter checks")
assert (SITE / "assets/data/tree.json").read_bytes() == (ROOT / "data/astra/016/generated-tree.json").read_bytes()
print("Built Tree is byte-identical to this build's isolated generated asset")

archive = ROOT / "book/archive-v2"
files = [p for p in archive.rglob("*") if p.is_file()]
for original in files:
    copied = SITE / "v2" / original.relative_to(archive)
    assert hashlib.sha256(original.read_bytes()).digest() == hashlib.sha256(copied.read_bytes()).digest()
print(f"Archive copy has matching bytes for {len(files)} files")
print("These static checks establish routing and byte identity. Browser behavior is recorded separately.")
