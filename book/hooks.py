"""Second Sun book: build-time progress, claim chips and offline cache (an MkDocs hook).

No backend. Ahmed's progress lives in progress/*.yml, claims in data/claims.csv;
a commit that edits them is the save. At build time this hook:
  1. validates the data (a bad file fails `mkdocs build --strict`),
  2. swaps placeholders in pages for plain HTML:
       <!-- ss:progress-line -->  <!-- ss:levels -->  <!-- ss:milestones -->
       <!-- ss:quests -->  <!-- ss:candidates -->  <!-- ss:claims -->  {{claim:B9}}
  3. writes sw.js: the shell precache list, a version hash, and an image-cache
     version; fails the build if the precache is over budget (25 MB).
It never starts a build itself and only writes inside site_dir, so it can't
re-trigger `mkdocs serve` (tested; see report).
Design rule: quiet progress, no XP or badges (Ahmed, 2026-10-19).
Later step (SITE-BLUEPRINT.md §5): move this logic to tools/build_book.py.
Run `python hooks.py` for the self-check.
"""
import csv
import datetime
import hashlib
import json
import logging
import re
import sys
from collections import Counter
from html import escape
from pathlib import Path

import yaml
from mkdocs.exceptions import PluginError

ROOT = Path(__file__).parent
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))
import mission   # the 0-100 readiness score (book/mission.py)

DATA = {}
LOG = logging.getLogger("mkdocs.hooks.second_sun")
LABELS = {"VERIFIED", "LIKELY", "UNVERIFIED"}
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg")
PRECACHE_BUDGET = 25 * 1024 * 1024


def load(root=ROOT):
    d = {n: yaml.safe_load((root / "progress" / f"{n}.yml").read_text(encoding="utf-8"))
         for n in ("levels", "milestones", "quests", "candidates", "mission")}
    with open(root / "data" / "claims.csv", encoding="utf-8", newline="") as f:
        d["claims"] = list(csv.DictReader(f))
    return d


def validate(d):
    for row in d["levels"] + d["milestones"]:
        if row["done"] is not None and not isinstance(row["done"], datetime.date):
            raise ValueError(f"progress: 'done' must be a date (YYYY-MM-DD) or null: {row}")
    ids = [c["id"] for c in d["candidates"]]
    for cid in ids:
        if not re.fullmatch(r"SS-\d{4}", cid):
            raise ValueError(f"progress/candidates.yml: bad id {cid!r} (want SS-0001 style)")
    if len(ids) != len(set(ids)):
        raise ValueError("progress/candidates.yml: duplicate candidate id")
    claim_ids = [c["id"] for c in d["claims"]]
    if len(claim_ids) != len(set(claim_ids)):
        raise ValueError("data/claims.csv: duplicate claim id")
    for c in d["claims"]:
        if c["label"] not in LABELS:
            raise ValueError(f"data/claims.csv: {c['id']} has label {c['label']!r}; use one of {sorted(LABELS)}")
    real = [c for c in d["candidates"] if not c.get("example")]
    d["score"] = mission.score(d["mission"], REPO, set(claim_ids), len(real))
    for st in d["mission"].get("status", []):
        if not all(isinstance(st.get(k), str) and st[k].strip() for k in ("label", "value", "note")):
            raise ValueError(f"progress/mission.yml: status cell needs label, value and note: {st}")
    if len(d["mission"].get("status", [])) != 6:
        raise ValueError("progress/mission.yml: the status panel needs exactly 6 cells")
    d["health"] = health(d)
    d["n_candidates"] = len(real)


STALE = re.compile(r"coming soon|still being written|not yet written|\bTODO\b|\bTBD\b|\(coming\)", re.I)
DASH = re.compile("[\u2013\u2014]")   # book rule (Ahmed): no en or em dashes in book text


def health(d, docs=ROOT / "docs"):
    """Cheap, honest book checks from the sources. A dash fails the build; stale phrases are counted and shown."""
    pages = sorted(docs.rglob("*.md"))
    texts = {p: p.read_text(encoding="utf-8") for p in pages}
    dashes = [p.relative_to(docs).as_posix() for p, t in texts.items() if DASH.search(t)]
    if dashes:
        raise ValueError(f"en or em dash in book text (rule: none) in: {dashes[:6]}")
    n = Counter(c["label"] for c in d["claims"])
    return dict(pages=len(pages), chapters=len(list((docs / "book").glob("[0-9]*.md"))), labs=len(list((docs / "labs").glob("lab*.md"))),
                claims=len(d["claims"]), verified=n["VERIFIED"], likely=n["LIKELY"], unverified=n["UNVERIFIED"],
                stale=sum(len(STALE.findall(t)) for t in texts.values()))


def status_panel(d):
    cells = "".join(f'<div><dt>{escape(c["label"])}</dt><dd>{escape(c["value"])}<small>{escape(c["note"])}</small></dd></div>' for c in d["mission"]["status"])
    return (f'<section class="ss-status-panel" aria-label="Mission status"><header><span>Mission status</span>'
            f'<span>Updated <b>{d["score"]["updated"]}</b></span></header><dl>{cells}</dl>'
            f'<p>Nothing here is a discovery yet. Every number links back to a test in <a href="book/08-our-detector/">Chapter 8</a>.</p></section>')


def mission_bar(d):
    """Home page only (its links are relative to the site root)."""
    s, h = d["score"], d["health"]; pct = round(s["total"])
    segs = "".join(f'<span class="ss-seg" style="flex:{st["weight"]} 1 0" title="{escape(st["name"])}: {st["points"]:.1f} of {st["weight"]}">'
                   f'<i style="width:{100 * st["points"] / st["weight"]:.1f}%"></i></span>' for st in s["stages"])
    legend = "".join(f'<li><span>{escape(st["name"])}</span><b>{st["points"]:.0f} / {st["weight"]}</b></li>' for st in s["stages"])
    return (f'<section class="ss-mission" aria-label="Mission readiness"><header><span>Mission readiness</span><span>Updated <b>{s["updated"]}</b></span></header>'
            f'<p class="ss-mission-num"><b>{pct}</b><small>/ 100</small></p>'
            f'<div class="ss-mission-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pct}" '
            f'aria-label="Mission readiness, {pct} out of 100">{segs}</div><ul class="ss-mission-legend">{legend}</ul>'
            f'<p class="ss-mission-note">How complete and how well built <em>our plan</em> is. It is <b>not</b> the chance of finding a planet. '
            f'Candidates found: <b>{d["n_candidates"]}</b>.</p>'
            f'<p class="ss-mission-note"><a href="progress/#mission-readiness">What is counted, and why</a> · Book: {h["pages"]} pages, {h["labs"]} labs, '
            f'{h["claims"]} facts ({h["verified"]} verified, {h["likely"]} likely, {h["unverified"]} unverified), {h["stale"]} stale phrases</p></section>')


def _ev(e):
    kind, _, ref = e.partition(":")
    if kind == "claim":
        return f'<a href="../claims/#claim-{escape(ref.lower())}">{escape(ref)}</a>'
    if kind == "file":
        return f'<a href="https://github.com/M1Smacker/second-sun/blob/main/{escape(ref)}"><code>{escape(ref)}</code></a>'
    return f'<a href="{escape(ref)}">link</a>'


def mission_detail(d):
    s, h = d["score"], d["health"]
    parts = [f'<p><b>{s["total"]:.1f} / 100.</b> Typed by us with proof: {s["typed"]:.1f}. Counted by the program from files: {s["auto"]:.1f}.</p>']
    for st in s["stages"]:
        rows = ""
        for i in st["items"]:
            note = "<br><small>" + escape(i["note"]) + "</small>" if i["note"] else ""
            credit = "auto" if i["auto"] else format(i["credit"], ".2f")
            proof = " ".join(_ev(e) for e in i["evidence"]) or ("counted by the program" if i["auto"] else "")
            rows += f'<tr><td>{escape(i["what"])}{note}</td><td>{i["weight"]}</td><td>{credit}</td><td>{i["points"]:.2f}</td><td>{proof}</td></tr>'
        parts.append(f'<section class="ss-card"><h3>{escape(st["name"])} · {st["points"]:.1f} / {st["weight"]}</h3><p>{escape(st["blurb"])}</p>'
                     f'<table><thead><tr><th>What</th><th>Weight</th><th>Credit</th><th>Points</th><th>Proof</th></tr></thead><tbody>{rows}</tbody></table></section>')
    chg = "".join(f'<li><b>{c["date"]}</b> {c["delta"]:+.2f} points: {escape(str(c["why"]))}</li>' for c in s["changes"])
    parts.append(f'<h3>Changes to the number</h3><ul>{chg}</ul>')
    parts.append(f'<h3>Book health</h3><ul><li>{h["pages"]} pages, {h["chapters"]} chapters, {h["labs"]} labs</li>'
                 f'<li>{h["claims"]} facts: {h["verified"]} verified, {h["likely"]} likely, {h["unverified"]} unverified</li>'
                 f'<li>Stale phrases ("coming soon" and similar): {h["stale"]}</li><li>En or em dashes in book text: 0 (a dash fails the build)</li></ul>')
    return "".join(parts)


def progress_line(d):
    counted = [lv for lv in d["levels"] if lv["level"] != "L0"]   # L0 is a warm-up, not counted
    done = sum(1 for lv in counted if lv["done"])
    nxt = next((lv for lv in d["levels"] if not lv["done"]), None)
    after = f' · Next: <b>{escape(nxt["level"])} {escape(nxt["title"])}</b>' if nxt else " · Track complete"
    pct = round(100 * done / len(counted))
    return (f'<p class="ss-progress">Level {done} of {len(counted)}{after}'
            f'<span class="ss-bar" role="progressbar" aria-valuemin="0" aria-valuemax="{len(counted)}" '
            f'aria-valuenow="{done}" aria-label="Learning track progress"><span style="width:{pct}%"></span></span></p>')


def checklist(rows, label):
    items = "".join(
        f'<li class="{"done" if r["done"] else ""}"><span class="ss-check" aria-hidden="true">{"✓" if r["done"] else ""}</span>'
        f'{escape(label(r))}<small>{escape(str(r["done"])) if r["done"] else ""}</small></li>' for r in rows)
    return f'<ul class="ss-list">{items}</ul>'


def levels(d):
    return checklist(d["levels"], lambda r: f'{r["level"]} {r["title"]}')


def milestones(d):
    return checklist(d["milestones"], lambda r: r["what"])


def quests(d):
    out = []
    for q in d["quests"]:
        steps = "".join(f'<li class="{"done" if s.get("done") else ""}">{escape(s["step"])}</li>' for s in q["steps"])
        out.append(f'<section class="ss-card"><p class="ss-meta">{escape(q["kind"])} quest · {escape(q["status"])}</p>'
                   f'<h3>{escape(q["title"])}</h3><p>{escape(q["why"])}</p><ol>{steps}</ol></section>')
    return "".join(out)


def candidates(d):
    if not d["candidates"]:
        return '<p class="ss-empty">No candidates yet. The first one will be SS-0001.</p>'
    out = []
    for c in d["candidates"]:
        demo = '<p class="ss-meta">Layout example, not a real candidate</p>' if c.get("example") else ""
        facts = "".join(f"<dt>{escape(k)}</dt><dd>{escape(str(v))}</dd>" for k, v in c["facts"].items())
        keys = " · ".join(f"{escape(k)}: {escape(v)}" for k, v in c["keys"].items())
        nick = f' "{escape(c["nickname"])}"' if c.get("nickname") else ""
        out.append(f'<section class="ss-card">{demo}<h3><code>{escape(c["id"])}</code>{nick}</h3>'
                   f'<p class="ss-meta"><span class="ss-status">{escape(c["status"])}</span> · Keys: {keys}</p>'
                   f'<dl class="ss-facts">{facts}</dl><p>{escape(c["note"])}</p></section>')
    return "".join(out)


def chip(c, to_root):
    title = f'{c["label"]} · {c["source"]} · checked {c["checked"]}'
    return (f'<a class="ss-chip ss-chip--{c["label"].lower()}" href="{to_root}claims/#claim-{c["id"].lower()}" '
            f'title="{escape(title)}">{escape(c["label"])}</a>')


def claims_table(d):
    rows = "".join(
        f'<tr id="claim-{escape(c["id"].lower())}"><td><code>{escape(c["id"])}</code></td><td>{escape(c["claim"])}</td>'
        f'<td>{chip(c, "../")}</td><td><a href="{escape(c["url"])}">{escape(c["source"])}</a></td>'
        f'<td>{escape(c["checked"])}</td></tr>' for c in d["claims"])
    return (f'<table><thead><tr><th>ID</th><th>Claim</th><th>Confidence</th><th>Source</th><th>Checked</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>')


RENDER = {"status-panel": status_panel, "mission-bar": mission_bar, "mission-detail": mission_detail, "progress-line": progress_line, "levels": levels, "milestones": milestones,
          "quests": quests, "candidates": candidates, "claims": claims_table}


def expand(markdown, page_url, d):
    """Replace placeholders. page_url like 'learn/l1-dip-depth/' (directory URLs)."""
    to_root = "../" * page_url.count("/")
    by_id = {c["id"]: c for c in d["claims"]}

    def claim(m):
        if m.group(1) not in by_id:
            raise PluginError(f"unknown claim id {m.group(1)!r} on page {page_url or 'index'} (add it to data/claims.csv)")
        return chip(by_id[m.group(1)], to_root)

    def block(m):
        if m.group(1) not in RENDER:
            raise PluginError(f"unknown placeholder ss:{m.group(1)} on page {page_url or 'index'}")
        return RENDER[m.group(1)](d)

    markdown = re.sub(r"\{\{claim:([A-Za-z0-9-]+)\}\}", claim, markdown)
    return re.sub(r"<!-- ss:([a-z-]+) -->", block, markdown)


def on_config(config):
    DATA.clear()
    DATA.update(load())
    try:
        validate(DATA)
    except ValueError as e:
        raise PluginError(str(e)) from e
    return config


def on_page_markdown(markdown, page, config, files):
    return expand(markdown, page.url, DATA)


def precache_list(site_dir):
    """Shell files: every page and asset, plus 'dir/' for each dir/index.html (pretty URLs).
    Left out: source maps, .gz, lunr language packs (English search never loads them), and
    content images (runtime image cache). Theme images under assets/ stay in the shell."""
    site = Path(site_dir)
    files = []
    for p in sorted(site.rglob("*")):
        rel = p.relative_to(site).as_posix()
        if p.is_dir() or rel == "sw.js" or rel.endswith((".map", ".gz")) or rel.startswith("assets/javascripts/lunr/"):
            continue
        if rel.lower().endswith(IMAGE_EXT) and not rel.startswith("assets/"):
            continue
        files.append(rel)
        if p.name == "index.html":
            files.append(rel[: -len("index.html")] or "./")
    return files


def content_images(site_dir):
    site = Path(site_dir)
    return sorted(p for p in site.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXT
                  and not p.relative_to(site).as_posix().startswith("assets/"))


def on_post_build(config):
    site = Path(config["site_dir"])
    files = precache_list(site)
    real = [f for f in files if not f.endswith("/")]
    size = sum((site / f).stat().st_size for f in real)
    if size > PRECACHE_BUDGET:
        raise PluginError(f"offline precache is {size / 2**20:.1f} MB, over the {PRECACHE_BUDGET / 2**20:.0f} MB budget")
    digest, img_digest = hashlib.sha256(), hashlib.sha256()
    for f in real:
        digest.update(f.encode() + (site / f).read_bytes())
    for p in content_images(site):
        img_digest.update(p.relative_to(site).as_posix().encode() + p.read_bytes())
    sw = (ROOT / "sw-template.js").read_text(encoding="utf-8")
    sw = (sw.replace("__VERSION__", digest.hexdigest()[:12])
            .replace("__IMG_VERSION__", img_digest.hexdigest()[:12])
            .replace("__SHELL__", json.dumps(files)))
    (site / "sw.js").write_text(sw, encoding="utf-8")
    LOG.info("offline precache: %d entries, %.0f KB; version %s", len(files), size / 1024, digest.hexdigest()[:12])


if __name__ == "__main__":
    d = load()
    validate(d)
    assert "Level 0 of 6" in progress_line(d)
    two = {**d, "levels": [{**lv, "done": datetime.date(2026, 10, 20)} if i < 2 else lv
                             for i, lv in enumerate(d["levels"])]}
    assert "Level 1 of 6" in progress_line(two) and "Next: <b>L2" in progress_line(two)  # L0 + L1 done, L0 not counted
    bad = load()
    bad["candidates"].append(dict(bad["candidates"][0]))
    try:
        validate(bad)
        raise AssertionError("duplicate id not caught")
    except ValueError:
        pass
    assert "<script" not in candidates({"candidates": [{**d["candidates"][0], "note": "<script>x</script>"}]})
    # claim chips: relative link depth, unknown id fails, bad label fails
    first = d["claims"][0]["id"]
    assert f'href="../../claims/#claim-{first.lower()}"' in expand("{{claim:" + first + "}}", "learn/x/", d)
    assert 'href="claims/#claim-' in expand("{{claim:" + first + "}}", "", d)
    for broken in ("{{claim:NOPE}}", "<!-- ss:nope -->"):
        try:
            expand(broken, "", d)
            raise AssertionError(f"{broken} not caught")
        except PluginError:
            pass
    badlabel = load()
    badlabel["claims"][0] = {**badlabel["claims"][0], "label": "SURE"}
    try:
        validate(badlabel)
        raise AssertionError("bad label not caught")
    except ValueError:
        pass
    assert d["score"]["total"] > 0 and 'role="progressbar"' in mission_bar(d) and status_panel(d).count("<dt>") == 6
    assert "ss-card" in mission_detail(d) and f'aria-valuenow="{round(d["score"]["total"])}"' in mission_bar(d)
    print("self-check ok")
