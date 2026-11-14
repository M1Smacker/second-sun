"""Checks for number_map (T130): python test_number_map.py (prints ok). Builds a tiny page, source and map in a temp folder."""
import pathlib, tempfile
import number_map as N

d = pathlib.Path(tempfile.mkdtemp()); (d / "nm").mkdir()
N.ROOT, N.NM = d, d / "nm"
(d / "page.md").write_text("# 11 November 2026\n\nWe found 34 real against 13 on 13 Nov 2026, chance 0.31.\n", encoding="utf-8")
(d / "src.txt").write_text("tier-1: real 34, upside-down 13\nbar 7 chance 0.3141\n", encoding="utf-8")
(d / "nm" / "PAGES.txt").write_text("page.md\n", encoding="utf-8")
head = "page,line,number,status,source_file,snippet,source_number,note\n"
good = head + ("page.md,3,34,TRACED,src.txt,tier-1: real,,\npage.md,3,13,TRACED,src.txt,upside-down 13,,\n"
               "page.md,3,0.31,TRACED,src.txt,bar 7 chance,0.3141,\n")
(d / "nm" / "NUMBER_MAP.csv").write_text(good, encoding="utf-8")
assert [t[1] for t in N.tokens("page.md")] == ["34", "13", "0.31"]          # the dates (heading, '13 Nov 2026') are not counted as numbers
assert N.check() == []
(d / "src.txt").write_text("tier-1: real 35, upside-down 13\nbar 7 chance 0.3141\n", encoding="utf-8")   # the source changed under the page
assert any(p.startswith("NOT IN SOURCE") and " 34:" in p for p in N.check())
(d / "nm" / "NUMBER_MAP.csv").write_text(good.replace("page.md,3,13,TRACED,src.txt,upside-down 13,,\n", ""), encoding="utf-8")
assert any(p.startswith("UNMAPPED") and " 13 " in p for p in N.check())   # a number with no row
(d / "page.md").write_text("# x\n\nWe found 34 real.\n", encoding="utf-8")
assert any(p.startswith("STALE ROW") for p in N.check())                  # a row whose number left the page
print("test_number_map ok")
