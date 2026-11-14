"""Tree check (Claude, 13 Nov 2026). Fails if any open item in the fix or build queue has no place on the Tree.

Rules checked:
1. Every open FIX item (numbered line) and every open BUILD item (- [ ] **Tnnn) sits under a '## n.n' heading.
2. That heading's node number exists in research/TREE.md (as **n.n ).
3. Every item is named somewhere in research/TREE.md ('FIX n' or 'Tnnn', ranges like 'T46 to T49' count).
Usage: python research/tree/tree_check.py   (exit 1 on any problem)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
tree = (ROOT / "research" / "TREE.md").read_text(encoding="utf-8")
nodes = set(re.findall(r"\*\*(\d\.\d) ", tree))


def named_in_tree(kind, ident):
    if kind == "FIX":
        n = int(ident)
        if re.search(rf"FIX (\d+, )*{n}\b", tree) or re.search(rf"FIX[^.]*?\b{n}\b", tree):
            return True
        for a, b in re.findall(r"FIX (\d+) to (\d+)", tree):
            if int(a) <= n <= int(b):
                return True
        return False
    if re.search(rf"\b{ident}\b", tree):
        return True
    m = re.match(r"T(\d+)([a-z]?)$", ident)
    for a, b in re.findall(r"T(\d+)[a-z]? to T(\d+)[a-z]?", tree):
        if int(a) <= int(m.group(1)) <= int(b):
            return True
    return False


problems = []
for kind, name, pat in (("FIX", "FIX-QUEUE.md", r"^(\d+)\. "), ("BUILD", "BUILD-QUEUE.md", r"^- \[ \] (?:\[[^\]]*\] )?\*\*(T\d+[a-z]?)[ .:]|^- \[ \] (?:\[[^\]]*\] )?(T\d+[a-z]?) ")):  # phase tag [..] since the 14 Nov triage
    node = None
    count = 0
    for line in (ROOT / "research" / "stage3" / name).read_text(encoding="utf-8").splitlines():
        h = re.match(r"^## (\d\.\d) ", line)
        if h:
            node = h.group(1)
            if node not in nodes:
                problems.append(f"{name}: heading {node} is not a node of TREE.md")
            continue
        m = re.match(pat, line)
        if not m:
            continue
        ident = next(g for g in m.groups() if g)
        count += 1
        if node is None:
            problems.append(f"{name}: {kind} {ident} has no node heading above it")
        if not named_in_tree(kind, ident):
            problems.append(f"{name}: {kind} {ident} is not named in TREE.md")
    print(f"{name}: {count} open items checked")
    open_lines = sum(1 for l in (ROOT / "research" / "stage3" / name).read_text(encoding="utf-8").splitlines() if re.match(r"^(\d+\. |- \[ \] )", l))
    if count != open_lines:  # a pattern that silently stops matching must fail, not pass (14 Nov: 0 of 59 builds were checked)
        problems.append(f"{name}: {open_lines} open lines but only {count} matched the item pattern")
print(f"TREE.md nodes: {len(nodes)}")
if problems:
    print("TREE CHECK FAILED:")
    for p in problems:
        print("  " + p)
    sys.exit(1)
print("TREE CHECK PASSED: every open item has a place on the Tree")
