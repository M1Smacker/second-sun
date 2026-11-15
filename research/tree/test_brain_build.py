"""Tests for brain_build.py (Claude, 15 Nov 2026). Every refusal must refuse; awkward but valid files must pass; 1,000 drops must be quick.
Runs on a temporary copy of the real inputs; never prints a fenced star id. Run: python research/tree/test_brain_build.py"""
import csv, shutil, sys, tempfile, time, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCRATCH = ROOT / "data" / "astra" / "020" / "builder-tests"
SCRATCH.mkdir(parents=True, exist_ok=True)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import brain_build as B


def fresh():
    t = Path(tempfile.mkdtemp(dir=SCRATCH))
    (t / "research" / "tree").mkdir(parents=True)
    shutil.copy(ROOT / "research" / "TREE.md", t / "research" / "TREE.md")
    for f in ("node-plain.yml", "phases.yml"):
        shutil.copy(HERE / f, t / "research" / "tree" / f)
    shutil.copytree(ROOT / "drops", t / "drops")
    (t / "targets").mkdir()
    shutil.copy(ROOT / "targets" / "r1_targets.csv", t / "targets" / "r1_targets.csv")
    (t / "book" / "docs" / "field-notes").mkdir(parents=True)
    for p in (ROOT / "book" / "docs" / "field-notes").glob("20*.md"):
        shutil.copy(p, t / "book" / "docs" / "field-notes" / p.name)
    return t


GOOD = """---
type: {type}
node: {node}
date: {date}
label: CONFIRMED
status: done
by: Claude
links: [research/TREE.md]
ids: [{ids}]
supersedes: [{sup}]
---
**Plain:** {plain}
**Why it matters:** A test drop.
"""


def drop(t, name, **kw):
    v = dict(type="finding", node="1.6", date="2026-11-15 03:00", ids="FIX 96 (the depth cap)", sup="", plain="A test drop.")
    v.update(kw)
    (t / "drops" / name).write_text(GOOD.format(**v), encoding="utf-8")


def refused(what, t, needle):
    try:
        B.build(t, write=False)
    except B.BuildRefused as e:
        assert needle in str(e), f"{what}: refused for the wrong reason: {e}"
        print(f"  refused as it should: {what}")
        return
    raise AssertionError(f"NOT refused: {what}")


n = 0
r = B.build(ROOT, write=False); n += 1
assert len(r["nodes"]) >= 20 and any(l["kind"] == "drop" for l in r["leaves"]), "real data"
print(f"  real data passes: {len(r['nodes'])} branches, {len(r['leaves'])} leaves")

def design_fields(result):
    ns = {v["id"]: v for v in result["nodes"]}
    return {
        "sub": ns["1"].get("sub") == "Petrova · 222 test planets" and ns["2.1"].get("sub") == "Our own binary star list",
        "loss": ns["1.1"].get("loss") == {"count": 53, "total": 222} and ns["1.2"].get("loss") == {"count": 52, "total": 222} and ns["2.1"].get("loss") is None,
        "bench": result.get("bench") == {"label": "Petrova 1.0.0", "rate": 27.5, "lower": 20.7, "upper": 33.7, "verdict": "Fix first"},
        "path": result.get("path", {}).get("active", {}).get("id") == "4.1" and result.get("path", {}).get("next", {}).get("id") == "1.1",
    }

fields = design_fields(r)
for field, passed in fields.items():
    print(f"  design field {field}: {'PASS' if passed else 'FAIL'}")
assert all(fields.values()), "incorrect design A fields"
n += len(fields)

# Change the source values as well as checking today's values. This catches a
# builder which returns constants that happen to match the current Tree.
t = fresh()
source = (t / "research" / "TREE.md").read_text(encoding="utf-8")
changed = source.replace("Loss: 45 + 7 of 222", "Loss: 12 + 8 of 90")
changed = changed.replace("R 27.5% [20.7, 33.7]", "R 31.25% [21.125, 41.875]")
changed = changed.replace("(node 4.1).** The Tree page", "(node 4.2).** The Tree page")
changed = changed.replace("- NEXT:", "- NEXT: first test item (node 3.2).\n- NEXT:", 1)
(t / "research" / "TREE.md").write_text(changed, encoding="utf-8")
plain_path = t / "research" / "tree" / "node-plain.yml"
plain_path.write_text(plain_path.read_text(encoding="utf-8").replace("Our own binary star list", "A changed subtitle"), encoding="utf-8")
mutated = B.build(t, write=False)
ns = {v["id"]: v for v in mutated["nodes"]}
assert ns["2.1"]["sub"] == "A changed subtitle"
assert ns["1.2"]["loss"] == {"count": 20, "total": 90}
assert mutated["bench"]["rate"] == 31.25 and mutated["bench"]["lower"] == 21.125 and mutated["bench"]["upper"] == 41.875
assert mutated["path"]["active"]["id"] == "4.2" and mutated["path"]["next"]["id"] == "3.2"
assert mutated["path"]["next"]["title"] == "first test item (node 3.2)"
print("  source changes propagate: sub, summed loss, unrounded bench, first path item")
n += 4
(t / "research" / "TREE.md").write_text(source.replace("(node 4.1).** The Tree page", ".** The Tree page"), encoding="utf-8")
assert B.build(t, write=False)["path"]["active"]["id"] is None
print("  an active item without a node keeps a null id")
n += 1
(t / "research" / "TREE.md").write_text(source.replace("R 27.5% [20.7, 33.7]", "R 27.5% [30, 33.7]"), encoding="utf-8")
refused("bench range excludes rate", t, "bench range")
n += 1
shutil.rmtree(t)

with open(ROOT / "targets" / "r1_targets.csv", encoding="utf-8-sig") as f:
    g1 = next(int(float(x["tic"])) for x in csv.DictReader(l for l in f if not l.startswith("#")) if x.get("list") == "g1" and int(float(x["tic"])) not in B.ALLOW)

cases = [
    ("missing node", lambda t: (t / "drops" / "2026-11-15-0300-x.md").write_text(GOOD.format(type="finding", node="1.6", date="2026-11-15 03:00", ids="", sup="", plain="x").replace("node: 1.6\n", ""), encoding="utf-8"), "missing 'node:'"),
    ("unknown node", lambda t: drop(t, "2026-11-15-0300-x.md", node="9.9"), "not on the Tree"),
    ("bad date", lambda t: drop(t, "2026-11-15-0300-x.md", date="15/11/2026"), "date must look like"),
    ("future date", lambda t: drop(t, "2026-11-15-0300-x.md", date="2031-01-01 00:00"), "outside the project's time"),
    ("bare id", lambda t: drop(t, "2026-11-15-0300-x.md", ids="FIX 96"), "no plain words in brackets"),
    ("fence A star", lambda t: drop(t, "2026-11-15-0300-x.md", plain=f"Star {g1} looked odd."), "sealed lists"),
    ("fence B star", lambda t: drop(t, "2026-11-15-0300-x.md", plain=f"Star {next(iter(B.fences(ROOT)[1]))} looked odd."), "sealed lists"),
    ("lead not marked", lambda t: drop(t, "2026-11-15-0300-x.md", type="lead"), "not checked yet"),
    ("unknown type", lambda t: drop(t, "2026-11-15-0300-x.md", type="gossip"), "unknown type"),
    ("supersedes missing", lambda t: drop(t, "2026-11-15-0300-x.md", sup="2026-11-01-0000-nothing.md"), "not in drops/"),
    ("supersedes itself", lambda t: drop(t, "2026-11-15-0300-x.md", sup="2026-11-15-0300-x.md"), "supersedes itself"),
    ("supersedes loop", lambda t: (drop(t, "2026-11-15-0300-a.md", sup="2026-11-15-0301-b.md", plain="A."), drop(t, "2026-11-15-0301-b.md", sup="2026-11-15-0300-a.md", plain="B.", date="2026-11-15 03:01")), "loops"),
    ("duplicate", lambda t: (drop(t, "2026-11-15-0300-a.md"), drop(t, "2026-11-15-0301-b.md", date="2026-11-15 03:01")), "repeats"),
    ("missing Plain line", lambda t: (t / "drops" / "2026-11-15-0300-x.md").write_text(GOOD.format(type="finding", node="1.6", date="2026-11-15 03:00", ids="", sup="", plain="x").replace("**Plain:** x\n", ""), encoding="utf-8"), "Plain"),
    ("finding without label", lambda t: (t / "drops" / "2026-11-15-0300-x.md").write_text(GOOD.format(type="finding", node="1.6", date="2026-11-15 03:00", ids="", sup="", plain="x").replace("label: CONFIRMED\n", ""), encoding="utf-8"), "needs a label"),
    ("no header", lambda t: (t / "drops" / "2026-11-15-0300-x.md").write_text("**Plain:** x\n", encoding="utf-8"), "header block"),
    ("TREE.md missing", lambda t: (t / "research" / "TREE.md").unlink(), "TREE.md is missing"),
    ("branch without plain words", lambda t: (t / "research" / "tree" / "node-plain.yml").write_text((HERE / "node-plain.yml").read_text(encoding="utf-8").replace('  "4.4":', '  "x4.4":'), encoding="utf-8"), "no plain words for node 4.4"),
]
for what, make, needle in cases:
    t = fresh(); make(t); refused(what, t, needle); n += 1
    shutil.rmtree(t, ignore_errors=True)

t = fresh()                                                       # awkward but valid: CRLF, BOM, comma inside brackets, README ignored
(t / "drops" / "2026-11-15-0300-crlf.md").write_bytes(("﻿" + GOOD.format(type="finding", node="4.1", date="2026-11-15 03:00",
    ids="T160 (the Tree, built from drops), FIX 73 (calmer chips)", sup="", plain="CRLF and BOM are fine.")).replace("\n", "\r\n").encode("utf-8"))
r = B.build(t, write=False)
leaf = next(l for l in r["leaves"] if l["id"] == "d:2026-11-15-0300-crlf")
assert leaf["ids"] == ["T160 (the Tree, built from drops)", "FIX 73 (calmer chips)"], leaf["ids"]
print("  passes as it should: CRLF, BOM, comma inside brackets"); n += 1
for p in (t / "drops").glob("2*.md"):
    p.unlink()
r = B.build(t, write=False); assert not [l for l in r["leaves"] if l["kind"] == "drop"]
print("  passes as it should: empty drops folder"); n += 1
for i in range(1000):
    drop(t, f"2026-11-15-{i // 60:02d}{i % 60:02d}-s{i}.md", date=f"2026-11-15 {i // 60 % 24:02d}:{i % 60:02d}", plain=f"Stress drop {i}.", node=["1.1", "2.2", "3.1", "4.1"][i % 4])
t0 = time.time(); r = B.build(t, write=False); dt_ = time.time() - t0
assert dt_ < 10, f"1,000 drops took {dt_:.1f} s"
print(f"  1,000 drops built in {dt_:.2f} s"); n += 1
shutil.rmtree(t, ignore_errors=True)
print(f"test_brain_build: {n} checks passed")
