"""The Drop box builder (BUILD T160; Ahmed's idea of 14 Nov 2026, built 15 Nov 2026 by Claude).

Reads, never edits: research/TREE.md (branches, weights, statuses, the research and Codex log), drops/*.md (one file per finished piece
of work), research/tree/node-plain.yml (what each branch is, in plain words), research/tree/phases.yml (the journey's big branches) and
book/docs/field-notes/*.md (the diary days). Writes ONE generated file: book/docs/assets/data/tree.json, which the Tree page draws.

It REFUSES (raises BuildRefused with a plain message, and writes nothing) when a drop:
  misses a required field or line; names a node that is not on the Tree; has a bad date or an unknown type, status or label; lists an id
  without plain words in brackets; names a fence A or fence B star (the sealed lists); is a lead not marked 'not checked yet';
  supersedes a drop that does not exist (or itself, or in a loop); or repeats another drop. It also refuses a TREE.md it cannot read.
The book build (hooks.py) runs it before every build, so a refusal stops the build and the publish before anything goes live.
Usage: python research/tree/brain_build.py [--check]   (--check: validate only, write nothing)"""
import csv, datetime as dt, json, re, sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book" / "docs" / "assets" / "data" / "tree.json"
GITHUB = "https://github.com/M1Smacker/second-sun/blob/main/"
TYPES = {"finding", "change", "decision", "lesson", "research", "fix", "build", "question", "run", "version", "rule", "lead", "idea"}
STATUSES = {"open", "done", "superseded"}
LABELS = {"CONFIRMED", "LIKELY", "UNCERTAIN", "NOT TESTED"}
NODE_STATUS = ("ACTIVE", "NEXT", "WAITS", "PARKED", "BLOCKED", "DONE")
ALLOW = {260128333, 172900988, 299096355, 158316612, 170348142, 164457525, 170344769}   # published systems (as fence_check.py)
MONTHS = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


class BuildRefused(ValueError):
    pass


def text(p):
    return p.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def plainify(s):
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    return " ".join(s.split())


def fences(root):
    a, b = set(), set()
    p = root / "targets" / "r1_targets.csv"
    if not p.exists():
        return a, b
    with open(p, encoding="utf-8-sig", newline="") as f:
        rows = csv.DictReader(line for line in f if not line.startswith("#"))
        for r in rows:
            try:
                t = int(float(r["tic"]))
            except (KeyError, ValueError):
                continue
            if r.get("list") == "g1":
                a.add(t)
            elif r.get("list") in ("g2", "g3") and str(r.get("design_seen", "")).strip() in ("0", "0.0"):
                b.add(t)
    return a - ALLOW, (b - a) - ALLOW


# ---------------- TREE.md ----------------
def read_tree(root):
    p = root / "research" / "TREE.md"
    if not p.exists():
        raise BuildRefused("research/TREE.md is missing")
    s = text(p)
    goal = re.search(r"^## Goal\n(.+)$", s, re.M)
    branches, nodes = {}, {}
    for m in re.finditer(r"^## (\d)\. (.+)$", s, re.M):
        branches[m.group(1)] = {"id": m.group(1), "title_tree": m.group(2).strip()}
    for m in re.finditer(r"^\*\*(\d\.\d) ([^\n]*?)\*\*(.*)$", s, re.M):
        nid, title, rest = m.group(1), m.group(2).strip().rstrip("."), m.group(3)
        if nid.split(".")[0] not in branches:
            raise BuildRefused(f"research/TREE.md: node {nid} has no '## {nid[0]}.' branch heading above it")
        w = re.search(r"\*Weight (\d)\.\*", rest)
        st = re.search(r"\*Status: ([^*]+)\*", rest)
        stext = st.group(1).strip() if st else ""
        word = next((k for k in NODE_STATUS if re.match(r"\W*" + k, stext)), None) or next((k for k in NODE_STATUS if k in stext), "PARKED")
        detail = re.sub(r"\*Weight \d\.\*", "", rest)
        detail = detail.replace(st.group(0), "") if st else detail
        loss = re.search(r"\bLoss:\s*(\d+(?:\s*\+\s*\d+)*)\s+of\s+(\d+)", rest)
        nodes[nid] = {"id": nid, "parent": nid.split(".")[0], "title_tree": title, "weight": int(w.group(1)) if w else 2,
                      "status": word, "status_text": plainify(stext), "detail": plainify(detail),
                      "loss": {"count": sum(int(v) for v in re.findall(r"\d+", loss.group(1))), "total": int(loss.group(2))} if loss else None}
    if not nodes:
        raise BuildRefused("research/TREE.md: no nodes found (lines like **1.1 Title.**)")
    log = []
    sec = s[s.index("## Research and Codex log"):] if "## Research and Codex log" in s else ""
    sec = sec.split("\n## ", 1)[0]
    for m in re.finditer(r"^- \*\*([^*]+)\*\* \(([^)]*)\):? ?(.*)$", sec, re.M):
        ident, meta, body = m.group(1).strip(), m.group(2), m.group(3)
        ns = re.findall(r"\b(\d\.\d)\b", meta.split("node", 1)[1]) if "node" in meta else []
        dm = re.search(r"\b(\d{1,2}) (Oct|Nov|Dec)\b", meta)
        date = dt.date(2026, MONTHS[dm.group(2)], int(dm.group(1))).isoformat() if dm else None
        log.append({"ident": ident, "nodes": [n for n in ns if n in nodes], "date": date, "body": plainify(body)})
    active = re.search(r"^## ACTIVE path now\n1\. (.+)$", s, re.M)
    bench = re.search(r"\*\*Bench so far:\*\*\s*(.+?)\s+R\s+([\d.]+)%\s*\[([\d.]+),\s*([\d.]+)\]", s)
    if not bench:
        raise BuildRefused("research/TREE.md: Bench so far rate and bounds are missing")
    rate, lower, upper = (float(bench.group(i)) for i in (2, 3, 4))
    if not 0 <= lower <= rate <= upper <= 100:
        raise BuildRefused("research/TREE.md: bench range must contain the rate, between 0 and 100")
    active_section = s.split("## ACTIVE path now\n", 1)[-1].split("\n## ", 1)[0]
    active_item = re.search(r"^\d+\. \*\*Active:\s*(.+?)\*\*", active_section, re.M)
    next_item = re.search(r"^- NEXT:\s*(.+)$", s, re.M)
    def path_item(value, position=None):
        label = plainify(value).rstrip(".")
        node = re.search(r"\bnode\s+(\d\.\d)\b", label)
        if not node and position is not None:
            # NEXT work lines live underneath their parent node heading.
            preceding = s[:position]
            headings = list(re.finditer(r"^\*\*(\d\.\d) ", preceding, re.M))
            node_id = headings[-1].group(1) if headings else None
        elif node:
            node_id = node.group(1)
        else:
            node_id = None
        return {"id": node_id if node_id in nodes else None, "title": label}
    path = {"active": path_item(active_item.group(1)) if active_item else None,
            "next": path_item(next_item.group(1), next_item.start()) if next_item else None}
    return {"goal": plainify(goal.group(1)) if goal else "", "branches": branches, "nodes": nodes, "log": log,
            "now": plainify(active.group(1)) if active else "", "path": path,
            "bench": {"label": bench.group(1).strip(), "rate": rate, "lower": lower, "upper": upper,
                      "verdict": "Fix first" if "**FIX FIRST**" in s.split("## ACTIVE path now", 1)[0] else ""}}


# ---------------- drops ----------------
def flow_list(head, key):
    """Read 'key: [a (x, y), b]' splitting on commas OUTSIDE round brackets (YAML would split inside them)."""
    m = re.search(r"^" + key + r":\s*(.*)$", head, re.M)
    if not m:
        return None
    v = m.group(1).split(" #", 1)[0].strip()
    if not v or v in ("[]", "~", "null"):
        return []
    if not (v.startswith("[") and v.endswith("]")):
        return [v]
    out, depth, cur = [], 0, ""
    for ch in v[1:-1]:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return [x.strip().strip("'\"") for x in out if x.strip()]


FIELD_LINE = re.compile(r"^\*\*(Plain|Why it matters|Explanation|Technical):\*\*\s*(.*)$", re.M)


def read_drop(p, nodes, fa, fb):
    raw = text(p)
    name = p.name
    if not raw.startswith("---\n"):
        raise BuildRefused(f"drops/{name}: must start with a '---' header block")
    try:
        head, body = raw[4:].split("\n---\n", 1)
        meta = yaml.safe_load(head) or {}
    except (ValueError, yaml.YAMLError) as e:
        raise BuildRefused(f"drops/{name}: the header block is not readable ({type(e).__name__})")
    if not isinstance(meta, dict):
        raise BuildRefused(f"drops/{name}: the header block must be 'key: value' lines")
    for k in ("type", "node", "date", "status", "by"):
        if meta.get(k) in (None, ""):
            raise BuildRefused(f"drops/{name}: missing '{k}:'")
    lines = {k: v.strip() for k, v in FIELD_LINE.findall(body)}
    for k in ("Plain", "Why it matters"):
        if not lines.get(k):
            raise BuildRefused(f"drops/{name}: missing the '**{k}:**' line")
    typ, status, node = str(meta["type"]).strip(), str(meta["status"]).strip(), str(meta["node"]).strip()
    if typ not in TYPES:
        raise BuildRefused(f"drops/{name}: unknown type '{typ}' (one of {', '.join(sorted(TYPES))})")
    if status not in STATUSES:
        raise BuildRefused(f"drops/{name}: unknown status '{status}' (open, done or superseded)")
    if node not in nodes:
        raise BuildRefused(f"drops/{name}: node '{node}' is not on the Tree (research/TREE.md)")
    label = meta.get("label")
    if label is not None and str(label).strip() not in LABELS:
        raise BuildRefused(f"drops/{name}: label '{label}' is not CONFIRMED, LIKELY, UNCERTAIN or NOT TESTED")
    if typ == "finding" and not label:
        raise BuildRefused(f"drops/{name}: a finding needs a label (CONFIRMED, LIKELY, UNCERTAIN or NOT TESTED)")
    try:
        when = dt.datetime.strptime(str(meta["date"]).strip(), "%Y-%m-%d %H:%M")
    except ValueError:
        raise BuildRefused(f"drops/{name}: date must look like 2026-11-15 03:40")
    if not dt.datetime(2026, 10, 1) <= when <= dt.datetime.now() + dt.timedelta(days=1):
        raise BuildRefused(f"drops/{name}: date {when:%Y-%m-%d %H:%M} is outside the project's time")
    for k in ("ids", "links", "supersedes"):
        v = flow_list(head, k)
        if v is not None:
            meta[k] = v
    ids = meta.get("ids") or []
    if not isinstance(ids, list):
        raise BuildRefused(f"drops/{name}: 'ids:' must be a list like [FIX 96 (the depth cap)]")
    for i in ids:
        if not re.search(r"\(.{3,}\)", str(i)):
            raise BuildRefused(f"drops/{name}: id '{i}' has no plain words in brackets (rule: explain every id)")
    allt = raw
    nums = {int(x) for x in re.findall(r"(?<![\d.])(\d{6,10})(?![\d.])", allt)}
    bad = sorted(nums & (fa | fb))
    if bad:
        raise BuildRefused(f"drops/{name}: names {len(bad)} star(s) from the sealed lists (fence A or B); never on the Tree")
    if typ == "lead" and "not checked yet" not in allt.lower():
        raise BuildRefused(f"drops/{name}: a lead must be marked 'not checked yet'")
    sup = meta.get("supersedes") or []
    if not isinstance(sup, list):
        raise BuildRefused(f"drops/{name}: 'supersedes:' must be a list of drop file names")
    links = meta.get("links") or []
    if not isinstance(links, list):
        raise BuildRefused(f"drops/{name}: 'links:' must be a list of paths")
    return {"id": "d:" + p.stem, "file": name, "kind": "drop", "type": typ, "node": node, "when": when.strftime("%Y-%m-%dT%H:%M"),
            "date": when.date().isoformat(), "status": status, "by": str(meta["by"]).strip(), "label": str(label).strip() if label else None,
            "plain": lines["Plain"], "why": lines["Why it matters"], "explanation": lines.get("Explanation", ""),
            "technical": lines.get("Technical", ""), "ids": [str(i) for i in ids],
            "links": [{"path": str(l), "url": GITHUB + str(l).strip().lstrip("/")} for l in links],
            "supersedes": [str(x).strip() for x in sup]}


def kind_of(ident):
    for pat, k in ((r"^RS-\d", "Research"), (r"^Codex \d", "Codex job"), (r"^FIX \d", "Fix"), (r"^T\d", "Build"), (r"^BUILD", "Build")):
        if re.match(pat, ident):
            return k
    return "Note"


def build(root=ROOT, write=True):
    tree = read_tree(root)
    nodes = tree["nodes"]
    fa, fb = fences(root)
    ddir = root / "drops"
    drops = [read_drop(p, nodes, fa, fb) for p in sorted(ddir.glob("*.md")) if p.name.lower() != "readme.md"] if ddir.exists() else []
    names = {d["file"] for d in drops}
    seen = {}
    for d in drops:
        key = (d["date"], d["plain"].lower())
        if key in seen:
            raise BuildRefused(f"drops/{d['file']}: repeats drops/{seen[key]} (same day, same plain line)")
        seen[key] = d["file"]
        for x in d["supersedes"]:
            x = x if x.endswith(".md") else x + ".md"
            if x == d["file"]:
                raise BuildRefused(f"drops/{d['file']}: supersedes itself")
            if x not in names:
                raise BuildRefused(f"drops/{d['file']}: supersedes '{x}', which is not in drops/")
    by_file = {d["file"]: d for d in drops}
    for d in drops:                                            # loops in supersedes chains
        cur, path = d, set()
        while cur and cur["supersedes"]:
            if cur["file"] in path:
                raise BuildRefused(f"drops/{d['file']}: the 'supersedes' chain loops back on itself")
            path.add(cur["file"])
            nxt = cur["supersedes"][0]
            cur = by_file.get(nxt if nxt.endswith(".md") else nxt + ".md")
    replaced = {x if x.endswith(".md") else x + ".md" for d in drops for x in d["supersedes"]}
    for d in drops:
        d["superseded"] = d["file"] in replaced or d["status"] == "superseded"
    drop_text = " ".join(" ".join(d["ids"]) + " " + d["plain"] for d in drops)
    leaves = list(drops)
    for i, e in enumerate(tree["log"]):
        if not e["nodes"]:
            continue
        short = re.split(r"[ (]", e["ident"].replace("**", ""), 1)[0:2]
        token = " ".join(e["ident"].split()[:2]).rstrip(":,")
        if token and token in drop_text:
            continue                                           # the drop tells this piece better
        first = re.split(r"(?<=\.)\s", e["body"], 1)[0][:240]
        leaves.append({"id": f"l:{i}", "kind": "log", "type": kind_of(e["ident"]).lower(), "node": e["nodes"][0], "also": e["nodes"][1:],
                       "date": e["date"], "when": (e["date"] + "T00:00") if e["date"] else None, "status": "done",
                       "plain": f"{kind_of(e['ident'])}: {first}", "why": "", "explanation": "", "technical": e["body"],
                       "ids": [e["ident"]], "links": [], "superseded": False, "by": "Claude" if not e["ident"].startswith("Codex") else "Codex",
                       "label": None})
    plain = yaml.safe_load(text(root / "research" / "tree" / "node-plain.yml"))
    phases = yaml.safe_load(text(root / "research" / "tree" / "phases.yml")) or []
    pb = plain.get("branches", {})
    for k in list(tree["branches"]) + list(nodes):
        if str(k) not in pb:
            raise BuildRefused(f"research/tree/node-plain.yml: no plain words for node {k}")
    out_nodes = []
    for b in sorted(tree["branches"]):
        kids = sorted(n for n in nodes if nodes[n]["parent"] == b)
        out_nodes.append({"id": b, "parent": "goal", "title": pb[b]["title"], "plain": pb[b]["plain"], "lesson": pb[b].get("lesson"),
                          "sub": pb[b].get("sub", ""), "loss": None,
                          "weight": max(nodes[n]["weight"] for n in kids) if kids else 2,
                          "status": next((s for s in NODE_STATUS if any(nodes[n]["status"] == s for n in kids)), "PARKED"),
                          "children": kids})
    for n in sorted(nodes):
        v = nodes[n]
        hist = sorted((l for l in leaves if l["node"] == n or n in l.get("also", [])), key=lambda l: l["when"] or "", reverse=True)
        out_nodes.append({"id": n, "parent": v["parent"], "title": pb[n]["title"], "id_tree": v["title_tree"], "plain": pb[n]["plain"],
                          "sub": pb[n].get("sub", ""), "loss": v["loss"],
                          "lesson": pb[n].get("lesson"), "weight": v["weight"], "status": v["status"], "status_text": v["status_text"],
                          "detail": v["detail"], "history": [l["id"] for l in hist]})
    notes = sorted(p.stem for p in (root / "book" / "docs" / "field-notes").glob("20??-??-??.md"))
    days = {}
    for l in leaves:
        if l["date"]:
            days.setdefault(l["date"], {"date": l["date"], "diary": None, "leaves": []})["leaves"].append(l["id"])
    for n in notes:
        days.setdefault(n, {"date": n, "diary": None, "leaves": []})["diary"] = f"field-notes/{n}/"
    for d in days.values():
        d["leaves"].sort(key=lambda i: next((l["when"] or "" for l in leaves if l["id"] == i), ""))
    for ph in phases:
        ph["from"] = str(ph["from"])
    result = {"generated": dt.datetime.now().strftime("%Y-%m-%dT%H:%M"), "goal": {"title": plain["goal"]["title"], "plain": plain["goal"]["plain"], "tree": tree["goal"]},
              "bench": tree["bench"], "path": tree["path"],
              "now": tree["now"], "nodes": out_nodes, "leaves": sorted(leaves, key=lambda l: l["when"] or "", reverse=True),
              "days": sorted(days.values(), key=lambda d: d["date"]), "phases": sorted(phases, key=lambda p: p["from"])}
    if write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        new = json.dumps(result, ensure_ascii=False, indent=1)
        old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if re.sub(r'"generated": "[^"]*"', "", old) != re.sub(r'"generated": "[^"]*"', "", new):
            OUT.write_text(new, encoding="utf-8")
    return result


if __name__ == "__main__":
    try:
        r = build(write="--check" not in sys.argv)
    except BuildRefused as e:
        print("REFUSED:", e)
        sys.exit(1)
    print(f"tree ok: {len(r['nodes'])} branches, {len(r['leaves'])} leaves ({sum(l['kind'] == 'drop' for l in r['leaves'])} drops), "
          f"{len(r['days'])} days, {len(r['phases'])} phases" + ("" if "--check" in sys.argv else f"; wrote {OUT.relative_to(ROOT)}"))
