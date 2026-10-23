"""The shape of the book: Parts, chapters, both reading orders, the home sky map, the chapter strip and the
Next/Previous links. Everything is generated from data/path.yml (and data/sky.json for the map), so one edit
moves a chapter everywhere. Used by hooks.py; `python shape.py` runs the self-check."""
import json
import math
import re
from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).parent
DASH = re.compile("[–—]")
COLOR = {"O": "#aac4ff", "B": "#aac4ff", "A": "#e8eeff", "F": "#fff8ec", "G": "#ffeeb8", "K": "#ffcf99", "M": "#ffb48a"}
# real figure of Cygnus (the Northern Cross), drawn faintly behind the book's six stars
FIGURE = [("Deneb", "Sadr"), ("Sadr", "Eta Cygni"), ("Eta Cygni", "Albireo"), ("Delta Cygni", "Sadr"), ("Sadr", "Gienah")]
W, H = 800, 560


def load(root=ROOT):
    path = yaml.safe_load((root / "data" / "path.yml").read_text(encoding="utf-8"))
    path["by_n"] = {c["n"]: c for c in path["chapters"]}
    path["part_by_n"] = {p["n"]: p for p in path["parts"]}
    path["sky"] = json.loads((root / "data" / "sky.json").read_text(encoding="utf-8"))
    return path


def validate(p, docs=ROOT / "docs"):
    ns = [c["n"] for c in p["chapters"]]
    if ns != list(range(1, len(ns) + 1)):
        raise ValueError("data/path.yml: chapters must be numbered 1..N in order")
    if sorted(j["ch"] for j in p["journey"]) != ns:
        raise ValueError("data/path.yml: the journey must list every chapter exactly once")
    for c in p["chapters"]:
        if c["part"] not in p["part_by_n"]:
            raise ValueError(f"data/path.yml: chapter {c['n']} has unknown part {c['part']}")
        if not (docs / "book" / f"{c['slug']}.md").exists():
            raise ValueError(f"data/path.yml: no page book/{c['slug']}.md")
        if len(c.get("story", "").split()) > 130:
            raise ValueError(f"data/path.yml: chapter {c['n']} story is over 130 words (brief: about 120)")
        if len(c["summary"]) != 3:
            raise ValueError(f"data/path.yml: chapter {c['n']} needs exactly 3 summary lines")
    for j in p["journey"]:
        if j.get("note") and not (docs / "field-notes" / f"{j['note']}.md").exists():
            raise ValueError(f"data/path.yml: journey note {j['note']} does not exist")
    files = sorted(f.stem for f in (docs / "book").glob("[0-9][0-9]-*.md"))
    if files != sorted(c["slug"] for c in p["chapters"]):
        raise ValueError(f"data/path.yml and docs/book/ list different chapters: {sorted(set(files) ^ {c['slug'] for c in p['chapters']})}")
    for part in p["parts"]:
        im = part.get("image")
        if im and not (docs / "assets" / "img" / "nasa" / im["file"]).exists():
            raise ValueError(f"data/path.yml: part {part['n']} image {im['file']} is not in docs/assets/img/nasa/")
        if part["star"] not in p["sky"]["named"]:
            raise ValueError(f"data/path.yml: star {part['star']!r} is not in data/sky.json (run tools/make_sky.py?)")
        if not any(c["part"] == part["n"] for c in p["chapters"]):
            raise ValueError(f"data/path.yml: part {part['n']} has no chapters")
    if DASH.search((root := ROOT / "data" / "path.yml").read_text(encoding="utf-8")):
        raise ValueError(f"{root}: en or em dash (rule: none)")


def check_nav(nav, p):
    """The sidebar (mkdocs.yml nav) and data/path.yml must agree on which chapter sits in which Part, in order."""
    read = next((list(i.values())[0] for i in nav if isinstance(i, dict) and "Read" in i), None)
    if read is None:
        raise ValueError("mkdocs.yml: the nav needs a Read tab")
    got = {}
    for item in read:
        (name, kids), = item.items()
        if not isinstance(kids, list):
            continue
        m = re.match(r"Part (\d+) ", name)
        if not m:
            raise ValueError(f"mkdocs.yml: Read section {name!r} should be named 'Part N ...'")
        for k in kids:
            if isinstance(k, dict):
                (t, f), = k.items()
                got[Path(f).stem] = (int(m.group(1)), t)
    want = {c["slug"]: (c["part"], title(c)) for c in p["chapters"]}
    if got != want or list(got) != list(want):
        diff = sorted(set(got.items()) ^ set(want.items()))[:4]
        raise ValueError(f"mkdocs.yml nav and data/path.yml disagree about the chapters (or their order): {diff}")


def chapter_for(p, src_uri):
    m = re.fullmatch(r"book/(\d\d)-[a-z0-9-]+\.md", src_uri)
    return p["by_n"].get(int(m.group(1))) if m else None


def part_for(p, src_uri):
    m = re.fullmatch(r"parts/part(\d)/index\.md", src_uri)
    return p["part_by_n"].get(int(m.group(1))) if m else None


def url(c, to_root):
    return f'{to_root}book/{c["slug"]}/'


def title(c):
    return f'{c["n"]}. {c["title"]}'


# ---------- chapter pages ----------
def strip(p, c, to_root):
    part = p["part_by_n"][c["part"]]
    dots = []
    prev_part = None
    for k in p["chapters"]:
        cur = ' aria-current="page"' if k["n"] == c["n"] else ""
        gap = " ss-gap" if prev_part is not None and k["part"] != prev_part else ""
        dots.append(f'<li class="{gap.strip()}"><a data-ch="{k["n"]}" href="{url(k, to_root)}" aria-label="Chapter {k["n"]}: {escape(k["title"])}"{cur}></a></li>')
        prev_part = k["part"]
    return (f'<nav class="ss-strip" aria-label="Where you are in the book"><p><a href="{to_root}">Map</a> · Part {part["n"]} of {len(p["parts"])}: '
            f'{escape(part["name"])} · Chapter {c["n"]} of {len(p["chapters"])}</p><ol>{"".join(dots)}</ol></nav>')


def summary(c):
    bullets = []
    for line in c["summary"]:
        head, _, rest = line.partition(": ")
        bullets.append(f"    - **{head}:** {rest}")
    out = '!!! abstract "1-minute summary"\n' + "\n".join(bullets) + "\n"
    if c.get("story"):
        out += '\n!!! quote "The story"\n    ' + c["story"].strip().replace("\n", "\n    ") + "\n"
    return out


def _order(p, kind):
    return [p["by_n"][j["ch"]] for j in p["journey"]] if kind == "journey" else p["chapters"]


def _link(c, to_root, rel, label, why=""):
    why = f"<em>{escape(why)}</em>" if why else ""
    return f'<a rel="{rel}" href="{url(c, to_root)}"><small>{label}</small><b>{escape(title(c))}</b>{why}</a>'


def chapter_end(p, c, to_root):
    pagers = ""
    start = f'{to_root}start/'
    for kind in ("journey", "topic"):
        seq = _order(p, kind)
        i = seq.index(c)
        prev = _link(seq[i - 1], to_root, "prev", "Previous") if i else ""
        if i + 1 < len(seq):
            nxt = _link(seq[i + 1], to_root, "next", "Next", seq[i + 1]["hook"])
        else:
            nxt = f'<a rel="next" href="{start}"><small>Next</small><b>Back to Start here</b><em>pick another path, or read the field notes</em></a>'
        pagers += f'<div class="ss-pager" data-path="{kind}">{prev}{nxt}</div>'
    part = p["part_by_n"][c["part"]]
    last = max(k["n"] for k in p["chapters"] if k["part"] == c["part"]) == c["n"]
    partend = (f'<p class="ss-partend">That is the end of Part {part["n"]}. <a href="{to_root}parts/part{part["n"]}/review/">Check yourself</a> · '
               f'<a href="{to_root}parts/part{part["n"]}/cheat/">Cheat sheet</a> · <a href="{to_root}parts/part{part["n"]}/labs/">Try it yourself (optional)</a></p>') if last else ""
    return (f'<nav class="ss-end" aria-label="Finish this chapter"><button type="button" class="ss-read-btn" data-ch="{c["n"]}" aria-pressed="false">Mark as read</button>'
            f'{pagers}{partend}<p class="ss-pathswitch">Reading order: <button type="button" data-path-set="journey">Journey</button> '
            f'<button type="button" data-path-set="topic">By topic</button></p></nav>')


def listen():
    """The read-aloud bar. Hidden until the page script finds the browser can speak."""
    return ('<div class="ss-listen" hidden role="group" aria-label="Read this chapter aloud"><button type="button" data-say="play">Listen</button>'
            '<button type="button" data-say="pause" hidden>Pause</button><button type="button" data-say="stop" hidden>Stop</button>'
            '<label>Speed <select data-say-rate><option value="0.85">Slow</option><option value="1" selected>Normal</option><option value="1.2">Fast</option></select></label>'
            '<span>Uses the voice on your own device.</span></div>')


def part_page(p, part, to_root):
    items = "".join(f'<li data-n="{c["n"]:02d}"><a href="{url(c, to_root)}"><b>{escape(title(c))}</b></a><span>{escape(c["summary"][0].partition(": ")[2])}</span></li>'
                    for c in p["chapters"] if c["part"] == part["n"])
    im = part.get("image")
    photo = (f'<figure class="ss-photo"><img src="{to_root}assets/img/nasa/{im["file"]}" alt="{escape(im["alt"])}" width="{im["w"]}" height="{im["h"]}" loading="lazy">'
             f'<figcaption>{escape(im["caption"])} Credit: {escape(im["credit"])}.</figcaption></figure>') if im else ""
    return (f'<p class="ss-meta">Part {part["n"]} of {len(p["parts"])} · star: {escape(part["star"])}</p>{photo}<p>{escape(part["blurb"])}</p>'
            f'<ol class="ss-chapters ss-plain">{items}</ol>'
            f'<p class="ss-partend"><a href="{to_root}parts/part{part["n"]}/review/">Check yourself</a> · <a href="{to_root}parts/part{part["n"]}/cheat/">Cheat sheet</a> · '
            f'<a href="{to_root}parts/part{part["n"]}/labs/">Try it yourself (optional)</a></p>')


def journey(p, to_root):
    rows = ""
    for i, j in enumerate(p["journey"], 1):
        c = p["by_n"][j["ch"]]
        note = f' <a class="ss-note" href="{to_root}field-notes/{j["note"]}/">Field note</a>' if j.get("note") else ""
        rows += (f'<li><a href="{url(c, to_root)}"><b>Chapter {c["n"]}: {escape(c["title"])}</b></a>'
                 f'<span>{escape(j["line"])}{note}</span></li>')
    return f'<ol class="ss-chapters ss-journey">{rows}</ol>'


def contents(p, to_root):
    out = ""
    for part in p["parts"]:
        items = "".join(f'<li data-n="{c["n"]:02d}"><a href="{url(c, to_root)}">{escape(c["title"])}</a><span>{escape(c["hook"][0].upper() + c["hook"][1:])}.</span></li>'
                        for c in p["chapters"] if c["part"] == part["n"])
        out += f'<h3 class="ss-parthead"><a href="{to_root}parts/part{part["n"]}/">Part {part["n"]} · {escape(part["name"])}</a></h3><ol class="ss-chapters">{items}</ol>'
    return out


# ---------- the sky ----------
def _proj(ra, dec, c0=(300.0, 40.0)):
    a, d, a0, d0 = map(math.radians, (ra, dec, c0[0], c0[1]))
    cosc = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a - a0)
    x = math.cos(d) * math.sin(a - a0) / cosc
    y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a - a0)) / cosc
    return -x, y, cosc          # east to the left, like the real sky


def sky(p, d, to_root):
    s = p["sky"]
    named = s["named"]
    star = {n: s["bright"][v["i"]] for n, v in named.items()}
    focus = [_proj(*star[x["star"]][:2])[:2] for x in p["parts"]] + [_proj(*q)[:2] for q in s["field"]] + [_proj(*star["Vega"][:2])[:2]]
    xs, ys = [q[0] for q in focus], [q[1] for q in focus]
    pad = 0.10
    sc = min(W * (1 - 2 * pad) / (max(xs) - min(xs)), H * (1 - 2 * pad) / (max(ys) - min(ys)))
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2

    def xy(ra, dec):
        x, y, _ = _proj(ra, dec)
        return W / 2 + (x - cx) * sc, H / 2 - (y - cy) * sc

    g = []
    plane = [xy(*q) for q in s["plane"] if _proj(*q)[2] > 0.6]
    if plane:
        pts = " ".join(f"{x:.0f},{y:.0f}" for x, y in plane)
        deg = math.radians(1) * sc
        g.append(f'<g filter="url(#ss-blur)" fill="none" stroke-linejoin="round" stroke-linecap="round">'
                 f'<polyline points="{pts}" stroke="#8fa6ff" stroke-opacity=".07" stroke-width="{16 * deg:.0f}"/>'
                 f'<polyline points="{pts}" stroke="#b9c8ff" stroke-opacity=".09" stroke-width="{6 * deg:.0f}"/></g>')
    # a faint chart grid, like a real star chart: parallels every 10 degrees, meridians every hour of right ascension
    def inside(pts):
        return [(x, y) for x, y in pts if 0 < x < W and 0 < y < H]
    gl, gt = [], []
    for dec in (30, 40, 50):
        pts = inside([xy(ra, dec) for ra in range(240, 361, 2)])
        if len(pts) > 1:
            gl.append(pts)
            x, y = max(pts)
            gt.append(f'<text x="{x - 8:.0f}" y="{y + 15:.0f}" text-anchor="end">+{dec}°</text>')
    for ra in (285, 300, 315):
        pts = inside([xy(ra, dec) for dec in range(5, 81, 2)])
        if len(pts) > 1:
            gl.append(pts)
            x, y = max(pts, key=lambda q: q[1])
            gt.append(f'<text x="{x + 6:.0f}" y="{y - 8:.0f}">{ra // 15}h</text>')
    g.append('<g class="ss-grid"><g fill="none">' + "".join('<polyline points="' + " ".join(f"{x:.0f},{y:.0f}" for x, y in pts) + '"/>' for pts in gl) + "</g>" + "".join(gt) + "</g>")
    g.append('<g class="ss-g1">' + "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.05"/>' for x, y in (xy(*q) for q in s["field"])) + "</g>")
    g.append('<g class="ss-bg">' + "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(.7, .55 + (5.6 - b[2]) * .45):.2f}" fill="{COLOR.get(b[3], "#fff")}"/>'
        for b in s["bright"] for x, y in [xy(b[0], b[1])] if -10 < x < W + 10 and -10 < y < H + 10) + "</g>")
    pos = {n: xy(*star[n][:2]) for n in star}
    g.append('<g class="ss-fig">' + "".join(
        f'<line x1="{pos[a][0]:.1f}" y1="{pos[a][1]:.1f}" x2="{pos[b][0]:.1f}" y2="{pos[b][1]:.1f}" pathLength="1"/>' for a, b in FIGURE) + "</g>")
    vx, vy = pos["Vega"]
    g.append(f'<text class="ss-lbl ss-dim" x="{vx - 12:.0f}" y="{vy + 5:.0f}" text-anchor="end">Vega</text>')
    fx = sum(xy(*q)[0] for q in s["field"]) / len(s["field"])
    fy = min(xy(*q)[1] for q in s["field"])
    g.append(f'<text class="ss-lbl ss-amber" x="{fx:.0f}" y="{fy - 14:.0f}" text-anchor="middle">Our {s.get("g1_total", 549)} Kepler stars ({s["g1_with_position"]} drawn)</text>')

    nodes = ""
    for part in p["parts"]:
        x, y = pos[part["star"]]
        mag = star[part["star"]][2]
        r = max(5.0, min(10.0, 5 + (3.4 - mag) * 2.2))
        chs = [c for c in p["chapters"] if c["part"] == part["n"]]
        R = r + 26
        dots = ""
        for i, c in enumerate(chs):
            ang = math.radians(-90 + 360 * i / len(chs) + (35 if len(chs) == 1 else 0))
            dx, dy = x + R * math.cos(ang), y + R * math.sin(ang)
            dots += (f'<a xlink:href="{url(c, to_root)}" aria-label="Chapter {c["n"]}: {escape(c["title"])}"><title>Chapter {c["n"]}: {escape(c["title"])}</title>'
                     f'<circle class="ss-hit" cx="{dx:.1f}" cy="{dy:.1f}" r="25"/><circle class="ss-ch" data-ch="{c["n"]}" cx="{dx:.1f}" cy="{dy:.1f}" r="5.2"/></a>')
        # Albireo is a real double star (an orange sun and a blue one, 34 arcseconds apart): drawn as two, the gap enlarged
        twin = f'<circle cx="{x + 12:.1f}" cy="{y - 9:.1f}" r="{r * .55:.1f}" fill="#aac4ff"/>' if part["star"] == "Albireo" else ""
        # Put the label where it touches nothing: try right, left, below, above; the first spot that stays inside
        # the picture and clear of the other Parts' rings wins (the ring is drawn as a circle of radius R + 8).
        others = [pos[q["star"]] for q in p["parts"] if q is not part]
        lw = 12 * len(f"{part['n']} {part['short']}")          # label width in map units (22 px semi-bold text)
        spots = [("start", x + R + 10, y + 5, x + R + 10, x + R + 10 + lw, y - 14, y + 9),
                 ("end", x - R - 10, y + 5, x - R - 10 - lw, x - R - 10, y - 14, y + 9),
                 ("middle", x, y + R + 26, x - lw / 2, x + lw / 2, y + R + 8, y + R + 32),
                 ("middle", x, y - R - 12, x - lw / 2, x + lw / 2, y - R - 34, y - R - 8)]

        def fits(s):
            _, _, _, x0, x1, y0, y1 = s
            if x0 < 4 or x1 > W - 4 or y0 < 4 or y1 > H - 4:
                return False
            return all(math.hypot(ox - min(max(ox, x0), x1), oy - min(max(oy, y0), y1)) > R + 8 for ox, oy in others)
        anchor, lx, ly = next(((s[0], s[1], s[2]) for s in spots if fits(s)), spots[0][:3])
        nodes += (f'<g class="ss-part"><circle class="ss-ring" cx="{x:.1f}" cy="{y:.1f}" r="{R:.1f}"/>{dots}'
                  f'<a xlink:href="{to_root}parts/part{part["n"]}/" aria-label="Part {part["n"]}: {escape(part["name"])}">'
                  f'<title>Part {part["n"]}: {escape(part["name"])} (the star {escape(part["star"])})</title><circle class="ss-hit" cx="{x:.1f}" cy="{y:.1f}" r="25"/>'
                  f'<circle class="ss-halo" cx="{x:.1f}" cy="{y:.1f}" r="{r * 2.4:.1f}" fill="url(#ss-halo)"/>'
                  f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{COLOR.get(star[part["star"]][3], "#fff")}"/>{twin}</a>'
                  f'<text class="ss-lbl" x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}">{part["n"]} {escape(part["short"])}</text></g>')
    defs = ('<defs><filter id="ss-blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="22"/></filter>'
            '<radialGradient id="ss-halo"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>')
    return (f'<svg class="ss-sky" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" role="group" aria-label="Map of the book on the real sky around Cygnus">{defs}'
            f'<rect class="ss-sky-bg" width="{W}" height="{H}" rx="10"/>{"".join(g)}{nodes}</svg>')


def latest_note(docs):
    notes = sorted(f for f in (docs / "field-notes").glob("20??-??-??.md"))
    if not notes:
        return None
    f = notes[-1]
    m = re.search(r"^# (.+)$", f.read_text(encoding="utf-8"), re.M)
    return f.stem, (m.group(1) if m else f.stem)


def home(p, d, to_root, docs=ROOT / "docs"):
    chs = json.dumps([{"n": c["n"], "t": c["title"], "u": url(c, to_root)} for c in p["chapters"]], separators=(",", ":"))
    note = latest_note(docs)
    note_html = f'<a href="{to_root}field-notes/{note[0]}/">{escape(note[1])}</a>' if note else "none yet"
    pct = round(d["score"]["total"])
    return (f'<section class="ss-home"><figure class="ss-sky-wrap">{sky(p, d, to_root)}<figcaption>The real sky around Cygnus, with east to the left. Each large star is one '
            f'Part of the book, at its true place, and bigger means brighter. The small dots around it are its chapters. Albireo is the real double star, with its gap enlarged. Amber specks are our Kepler stars. '
            f'Sources: Bright Star Catalogue and the Villanova Kepler EB catalog.</figcaption></figure>'
            f'<div class="ss-home-row"><a class="ss-start" href="{to_root}start/">Start here</a>'
            f"<div class=\"ss-resume\" data-chapters=\"{escape(chs)}\"><b>Where you stopped</b><span>Nothing read yet. 0 of {len(p['chapters'])} chapters.</span></div></div>"
            f'<dl class="ss-glance"><div><dt>Readiness</dt><dd><a href="{to_root}progress/">{pct} / 100</a></dd></div>'
            f'<div><dt>Candidates</dt><dd><a href="{to_root}candidates/">{d["n_candidates"]}</a></dd></div>'
            f'<div class="ss-wide"><dt>Latest field note</dt><dd>{note_html}</dd></div></dl></section>')


if __name__ == "__main__":
    p = load()
    validate(p)
    assert len(p["chapters"]) == 15 and len(p["parts"]) == 6
    assert all(summary(c).count("\n    - ") == 3 for c in p["chapters"])
    c8 = p["by_n"][8]
    e = chapter_end(p, c8, "../../")
    assert 'data-path="journey"' in e and 'data-path="topic"' in e and "Mark as read" in e and "ss-partend" not in e
    assert "ss-partend" in chapter_end(p, p["by_n"][3], "../../")          # last chapter of Part 1
    assert strip(p, c8, "../../").count("<a data-ch") == 15
    svg = sky(p, {"score": {"total": 36}}, "")
    assert svg.count('class="ss-ch"') == 15 and svg.count('class="ss-part"') == 6 and "Albireo" in svg
    assert "—" not in svg and "<script" not in svg
    print("shape self-check ok")
