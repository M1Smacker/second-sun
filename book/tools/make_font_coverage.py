"""Developer tool (needs `pip install fonttools brotli`): lists, for every font file the book serves, which characters it can draw, and records the file's
sha256. Writes book/tools/font_coverage.json. The publish gate cannot read woff2 files itself (no brotli there), so tools/test_fonts.py reads this list and
refuses it when a font file no longer matches its recorded sha256. Run again whenever a file in docs/assets/fonts changes:
    python book/tools/make_font_coverage.py"""
import hashlib, json, sys
from pathlib import Path
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "docs" / "assets" / "fonts"
out = {}
for p in sorted(FONTS.glob("*.woff2")):
    cmap = TTFont(str(p)).getBestCmap()
    out[p.name] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "cps": sorted(cmap)}
    print(f"{p.name}: {len(cmap)} characters")
(HERE / "font_coverage.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
print("written", HERE / "font_coverage.json")
