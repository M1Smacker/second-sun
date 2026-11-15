"""Inline the trimmed Tree data into the design page."""
import pathlib
here = pathlib.Path(__file__).parent
data = (here / "tree-data-sample.json").read_text(encoding="utf-8").replace("</", "<\\/")
page = (here / "page.src.html").read_text(encoding="utf-8").replace("/*__TREE_DATA__*/", data)
(here / "golden-tree.html").write_text(page, encoding="utf-8")
print("ok", len(page))
