"""One-off: rebuild FIX-QUEUE.md and BUILD-QUEUE.md from the archived copies, open items only, grouped by Tree node.
Item text is copied verbatim. Placement and status come from research/TREE.md (the PLACE table below mirrors it).
Claude, 13 Nov 2026."""
import re
from pathlib import Path
S = Path(__file__).resolve().parents[1] / "stage3"
fix_old = (S / "archive-FIX-QUEUE-to-2026-11-13.md").read_text(encoding="utf-8")
bld_old = (S / "archive-BUILD-QUEUE-to-2026-11-13.md").read_text(encoding="utf-8")

FIX = {  # id: node
 30: "1.1", 90: "1.1", 26: "1.2", 70: "1.2", 84: "1.2", 11: "1.3", 14: "1.3", 16: "1.3", 24: "1.4",
 19: "1.6", 21: "1.6", 22: "1.6",
 86: "3.1", 87: "3.1", 88: "3.1", 89: "3.2", 83: "3.2", 85: "3.2", 27: "3.3",
 25: "2.3", 72: "2.3",
 82: "4.3", 69: "4.3", 77: "4.2", 78: "4.3", 80: "4.3", 73: "4.1", 74: "4.1", 75: "4.1", 76: "4.1",
}
BLD = {
 "T34": "1.1", "T145": "1.1", "T157": "1.1",
 "T155": "1.2", "T137": "1.2",
 "T158": "1.3",
 "T31": "1.6", "T32": "1.6", "T33": "1.6", "T35": "1.6",
 "T156": "1.7", "T36": "1.7", "T109": "1.7",
 "T136": "2.1", "T139": "2.1", "T138": "2.1", "T140": "2.1", "T148": "2.1", "T152": "2.1", "T153": "2.1",
 "T37b": "2.2", "T150": "2.3", "T151": "2.3", "T119": "2.4", "T120": "2.4", "T121": "2.4", "T122": "2.4", "T123": "2.4", "T124": "2.4",
 "T101": "3.1", "T129": "3.1", "T117": "3.1", "T118": "3.1", "T54": "3.1",
 "T128": "3.2", "T142": "3.2", "T130": "3.2", "T52": "3.2",
 "T46": "3.3", "T47": "3.3", "T48": "3.3", "T49": "3.3", "T106": "3.3", "T141": "3.3", "T125": "3.3", "T126": "3.3", "T127": "3.3", "T60": "3.3",
 "T108": "3.4", "T149": "3.4",
 "T57a": "4.1", "T57b": "4.1", "T57c": "4.1", "T57d": "4.1", "T58a": "4.1", "T58b": "4.1", "T113": "4.1", "T114": "4.1",
 "T115": "4.1", "T116": "4.1", "T131": "4.1", "T132": "4.1", "T133": "4.1", "T134": "4.1", "T146": "4.1", "T147": "4.1", "T59c": "4.1",
 "T159": "4.2", "T51": "4.2", "T53": "4.2", "T50": "4.2",
 "T59d": "4.4", "T59e": "4.4", "T59g": "4.4", "T110": "4.4",
 "T55": "4.3", "T143": "4.3",
}
CLOSED_BLD = {  # moved out of the open list today, with the reason (the archive keeps the text)
 "T56": "a working rule, kept in memory; nothing to build",
 "T59a": "folded into T159 (control room)", "T59b": "folded into T159 (Netlify replaces Firebase)",
 "T135": "folded into T159 (control room)", "T154": "folded into T159 (control room)",
 "T104": "BUILT 2 Nov 2026 (its own line says so)",
 "T111": "done: the G3 list was found and searched (4 Nov 2026)", "T112": "done: G3 preregistration written and run (4 Nov 2026)",
 "T144": "done: this Tree clean-up (13 Nov 2026)",
}
CLOSED_FIX = {12: "superseded by T156 (whole-chain recovery measured on raw light)", 13: "superseded by T156",
              20: "superseded by T156", 29: "superseded by T156 (it measures exactly the thrown-away share)", 68: "DONE 3 Nov 2026 (its own line)",
              85: None}

def fix_line(n):
    m = re.search(rf"(?m)^[ \t]*{n}\. (.*)$", fix_old)
    return m.group(1)
def bld_line(t):
    m = re.search(rf"(?m)^- \[ \] (\*\*{re.escape(t)}[ .:].*)$", bld_old)
    if m: return m.group(1)
    m = re.search(rf"(?m)^## ({re.escape(t)} .*)$", bld_old)
    return m.group(1)

NODES = {"1.1": "Tier-1 flags hold found planets back", "1.2": "Planet falls outside the searched windows", "1.3": "The detector misses the dip",
 "1.4": "The eclipse mask eats the transit", "1.6": "False alarms (keep the upside-down count low)", "1.7": "The scoreboard and its tools",
 "2.1": "Census: our own binary list", "2.2": "G1: the last unseen list", "2.3": "Data and downloads", "2.4": "Parked new systems (Horizon, Vigil, Witness, OMS)",
 "3.1": "Statistics and controls", "3.2": "Records, reproducibility and tests", "3.3": "Leads: how a dip becomes a claim", "3.4": "Going public later",
 "4.1": "Book and learning", "4.2": "Search window and control room", "4.3": "Machine, scripts and housekeeping", "4.4": "Eyes pages"}
HEAD = {"FIX": "# Fix queue: bugs only, grouped by the Tree\n\n", "BUILD": "# Build queue: builds, studies, features, grouped by the Tree\n\n"}
RULE = ("Rebuilt 13 Nov 2026 from the archived copy (`{arch}`, kept whole, nothing deleted). Open items only, text copied as it was. "
        "**Every new item needs a node of `research/TREE.md` before it is filed** (the heading it goes under), and `research/tree/tree_check.py` must pass. "
        "Order and status (ACTIVE, NEXT, WAITS, PARKED) live in the Tree, not here. Bugs here; builds, studies and features in the other queue (Ahmed, 30 Oct 2026).\n")

def write(kind, mapping, getter, arch, extra=""):
    out = HEAD[kind] + RULE.format(arch=arch) + extra
    for node in sorted(NODES, key=lambda s: tuple(map(int, s.split(".")))):
        ids = [i for i, nd in mapping.items() if nd == node]
        if not ids: continue
        out += f"\n## {node} {NODES[node]}\n"
        for i in ids:
            line = getter(i)
            out += (f"{i}. {line}\n" if kind == "FIX" else f"- [ ] {line}\n")
    return out

fix_extra = "\nNew items continue from 91. Closed today (text in the archive): " + "; ".join(f"{k} {v}" for k, v in CLOSED_FIX.items() if v) + ".\n"
fix_text = write("FIX", FIX, fix_line, "research/stage3/archive-FIX-QUEUE-to-2026-11-13.md", fix_extra)
fix_text = fix_text.replace("\n## 1.1 Tier-1 flags hold found planets back\n",
  "\n## 1.1 Tier-1 flags hold found planets back\n91. **M. The opposite-sign coincidence flag is applied to the real arm only (Codex brief 003, 13 Nov 2026; CONFIRMED on synthetic events; OPEN).** `pipeline/stage2_search.py` line 194 passes the upside-down events into the real-arm veto; line 195 passes an empty list into the upside-down-arm veto. `detect_v2.py` 274 to 277 sets the flag, `stage3_core.py` 65 to 67 reads it and 254 to 255 makes it tier 2. Codex's `003_checks.py`: a dip becomes tier 2 while the matching bump stays tier 1B. How often it fires on real data: NOT TESTED. Fix only in a new Petrova version, priced on the T156 bench (sensitivity and upside-down count).\n", 1)
bld_extra = "\nClosed today (text in the archive): " + "; ".join(f"{k} {v}" for k, v in CLOSED_BLD.items()) + ".\n"
bld_text = write("BUILD", BLD, bld_line, "research/stage3/archive-BUILD-QUEUE-to-2026-11-13.md", bld_extra)
bld_text = bld_text.rstrip("\n") + "\n- [ ] **T160. The Tree as the book's home page [Ahmed, 13 Nov 2026].** The home page (now the star picture) becomes the interactive, clickable Tree from `research/TREE.md`: every node opens its section, no highlighting, just clickable. Design slowly with Ahmed in many question rounds. Waits for the design rounds.\n"
bld_text = bld_text.replace("## 4.2 Search window and control room\n", "## 4.2 Search window and control room\n", 1)
(S / "FIX-QUEUE.md").write_text(fix_text, encoding="utf-8")
(S / "BUILD-QUEUE.md").write_text(bld_text, encoding="utf-8")
print("fix open", len(FIX) + 1, "build open", len(BLD) + 1)
