"""Negative and positive tests for the book's shape rules (data/path.yml, the nav, the sky map).
Each broken copy must be refused with a plain message; the real files must pass. Run: python tools/test_shape.py"""
import copy
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import shape  # noqa: E402

P = shape.load()
NAV = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))["nav"]
shape.validate(P)
shape.check_nav(NAV, P)


def refused(what, fn, *args):
    try:
        fn(*args)
    except ValueError as e:
        print(f"  refused: {what}: {str(e)[:90]}")
        return
    raise AssertionError(f"NOT refused: {what}")


def broken(change):
    q = copy.deepcopy(P)
    change(q)
    q["by_n"] = {c["n"]: c for c in q["chapters"]}
    q["part_by_n"] = {x["n"]: x for x in q["parts"]}
    return q


refused("a chapter missing from the journey", shape.validate, broken(lambda q: q["journey"].pop()))
refused("a chapter listed twice in the journey", shape.validate, broken(lambda q: q["journey"].append(dict(q["journey"][0]))))
refused("a story over 130 words", shape.validate, broken(lambda q: q["chapters"][0].update(story="word " * 131)))
refused("a chapter with two summary lines", shape.validate, broken(lambda q: q["chapters"][0]["summary"].pop()))
refused("a chapter with no page", shape.validate, broken(lambda q: q["chapters"][0].update(slug="01-nope")))
refused("a chapter in an unknown Part", shape.validate, broken(lambda q: q["chapters"][0].update(part=9)))
refused("a Part star missing from the sky data", shape.validate, broken(lambda q: q["parts"][0].update(star="Nowhere")))
refused("a journey note that does not exist", shape.validate, broken(lambda q: q["journey"][0].update(note="2099-01-01")))
refused("chapters out of order", shape.validate, broken(lambda q: q["chapters"].reverse()))
refused("a chapter missing from the learning track", shape.validate, broken(lambda q: q["track"][0]["chapters"].pop()))
refused("a chapter listed twice in the learning track", shape.validate, broken(lambda q: q["track"][3]["chapters"].append(1)))
refused("levels out of order in the track", shape.validate, broken(lambda q: q["track"].reverse()))
refused("a level with no chapters and no page", shape.validate, broken(lambda q: q["track"][1].pop("page")))
refused("a chapter moved to another level but not on the learning page", shape.validate, broken(lambda q: (q["track"][0]["chapters"].remove(3), q["track"][3]["chapters"].append(3))))
nav = copy.deepcopy(NAV)
read = list(nav[0].values())[0]
parts = [i for i in read if isinstance(list(i.values())[0], list)]
a, b = list(parts[0].values())[0], list(parts[1].values())[0]
a[1], b[1] = b[1], a[1]           # swap a chapter between Part 1 and Part 2 in the sidebar only
refused("the sidebar putting a chapter in the wrong Part", shape.check_nav, nav, P)
refused("a nav with no Read tab", shape.check_nav, [], P)
import diagrams  # noqa: E402
assert set(diagrams.DIAGRAMS) == {c["n"] for c in P["chapters"]}, "every chapter needs a diagram in book/diagrams.py"
assert shape._seq(P) == [1, 2, 3, 7, 8, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15], "the learning path Ahmed approved on 27 Oct 2026"
assert "learn/l1-dip-depth" in shape.chapter_end(P, P["by_n"][3], "../../") and "Level 1" in shape.chapter_end(P, P["by_n"][3], "../../")
assert "book/04-two-suns" in shape.chapter_end(P, P["by_n"][8], "../../"), "the end of Level 3 leads to the start of Level 4"
assert shape.chapter_for(P, "book/08-our-detector.md")["n"] == 8 and shape.chapter_for(P, "start/index.md") is None
print("all shape checks passed")
