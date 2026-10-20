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
from html import escape
from pathlib import Path

import yaml
from mkdocs.exceptions import PluginError

ROOT = Path(__file__).parent
DATA = {}
LOG = logging.getLogger("mkdocs.hooks.second_sun")
LABELS = {"VERIFIED", "LIKELY", "UNVERIFIED"}
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg")
PRECACHE_BUDGET = 25 * 1024 * 1024


def load(root=ROOT):
    d = {n: yaml.safe_load((root / "progress" / f"{n}.yml").read_text(encoding="utf-8"))
         for n in ("levels", "milestones", "quests", "candidates")}
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


RENDER = {"progress-line": progress_line, "levels": levels, "milestones": milestones,
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
    print("self-check ok")
