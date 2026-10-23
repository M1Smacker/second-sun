"""One small diagram for the top of each chapter (inline SVG, 420 x 150, theme colours through CSS variables).
`figure(n)` returns the HTML for chapter n. Every diagram has a title for screen readers. Run `python diagrams.py` for the self-check."""
import math
from html import escape

W, H = 420, 150


def t(x, y, s, anchor="middle", cls=""):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{escape(s)}</text>'


def line(x1, y1, x2, y2, cls="l"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"/>'


def circ(x, y, r, cls="l"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" class="{cls}"/>'


def box(x, y, w, h, label, cls="l", sub=""):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" class="{cls}"/>' + t(x + w / 2, y + h / 2 + (-2 if sub else 5), label, cls="bx")
    return s + (t(x + w / 2, y + h / 2 + 14, sub, cls="sm") if sub else "")


def arrow(x1, y, x2, cls="l"):
    return line(x1, y, x2, y, cls) + f'<path d="M{x2 - 7} {y - 4} L{x2} {y} L{x2 - 7} {y + 4}" class="{cls}"/>'


def curve(x0, x1, y, dips, cls="l"):
    """A flat light curve with box-shaped dips: dips = [(centre, width, depth)]"""
    pts, x = [f"M{x0} {y}"], x0
    for c, w, d in sorted(dips):
        pts += [f"L{c - w / 2 - 2} {y}", f"L{c - w / 2} {y + d}", f"L{c + w / 2} {y + d}", f"L{c + w / 2 + 2} {y}"]
    pts.append(f"L{x1} {y}")
    return f'<path d="{" ".join(pts)}" class="{cls}"/>'


def ellipse(cx, cy, rx, ry, cls="l", rot=0):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" class="{cls}"/>'


def d1():
    return (circ(200, 75, 14, "fa") + line(214, 68, 290, 30) + line(214, 75, 290, 75) + line(214, 82, 290, 120) + line(186, 68, 110, 30) + line(186, 82, 110, 120)
            + t(295, 34, "KIC 12644769", "start") + t(295, 79, "TIC 299096355", "start") + t(295, 124, "Gaia DR3", "start") + t(105, 34, "Kepler-16", "end") + t(105, 124, "one star", "end"))


def d2():
    return (curve(20, 400, 50, [(120, 22, 70), (300, 34, 6)]) + t(120, 140, "eclipse: deep", cls="sm") + t(300, 140, "planet: shallow", cls="sm") + line(20, 50, 400, 50, "g")
            + t(30, 24, "brightness", "start", "sm") + t(400, 24, "time", "end", "sm"))


def d3():
    out = ""
    for i, (a, s) in enumerate([("TESS camera", "in orbit"), ("NASA pipeline", "cleans it"), ("MAST archive", "free online"), ("Your D: drive", "our code")]):
        x = 4 + i * 104
        out += box(x, 45, 94, 60, a, "l" if i < 3 else "a", s) + (arrow(x + 96, 75, x + 104, "g") if i < 3 else "")
    return out


def d4():
    out = ellipse(210, 75, 120, 62, "g") + circ(210, 75, 4, "g") + ellipse(210, 75, 20, 20, "g")
    out += circ(223, 75, 5, "f") + circ(190, 76, 3, "fa") + circ(330, 75, 5, "fa") + t(330, 100, "planet", cls="sm") + t(210, 142, "two suns, one planet around both", cls="sm")
    return out


def d5():
    xs = [60, 155, 252, 340]
    out = curve(20, 400, 60, [(x, 8, 30) for x in xs], "a") + "".join(line(20 + i * 95, 52, 20 + i * 95, 100, "g") for i in range(5))
    out += t(107, 122, "93 days", cls="sm") + t(203, 122, "95 days", cls="sm") + t(296, 122, "88 days", cls="sm") + t(210, 20, "grey: where a clock would put the dips", cls="sm")
    return out


def d6():
    return (circ(210, 75, 34, "g") + circ(210, 75, 52, "dash") + circ(210, 75, 64, "a") + circ(200, 75, 5, "f") + circ(222, 75, 3, "fa") + circ(274, 75, 4, "fa")
            + t(360, 52, "planet's orbit", "middle", "sm") + t(360, 112, "too close:", "middle", "sm") + t(360, 128, "unstable", "middle", "sm") + t(60, 80, "stars", "middle", "sm"))


def d7():
    out, seed = "", 11
    for i in range(70):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        r = (seed / 0x7FFFFFFF - 0.5) * 34
        x = 20 + i * 5.4
        out += circ(f"{x:.1f}", f"{75 + r + (14 if 28 < i < 44 else 0):.1f}", 1.7, "f")
    return out + f'<rect x="{20 + 28 * 5.4}" y="30" width="{16 * 5.4}" height="90" class="dipbox"/>' + t(210, 142, "a dip must stand out from the scatter", cls="sm")


def d8():
    return (curve(20, 400, 50, [(210, 60, 14)], "l") + f'<rect x="170" y="36" width="80" height="44" rx="3" class="dipbox"/>' + t(210, 98, "sliding box", cls="sm")
            + line(20, 130, 400, 130, "g") + f'<path d="M20 130 L150 130 L210 106 L270 130 L400 130" class="a"/>' + t(30, 118, "score", "start", "sm"))


def d9():
    return (curve(20, 400, 60, [(110, 18, 4), (300, 30, 26)], "l") + f'<rect x="276" y="56" width="48" height="36" rx="3" class="dash"/>' + t(300, 112, "hidden fake planet", cls="sm")
            + t(110, 112, "real data", cls="sm") + t(300, 20, "found?", cls="a-text"))


def d10():
    out = ""
    for i in range(9):
        out += circ(30 + (i % 3) * 16, 40 + (i // 3) * 24, 5, "f")
    out += f'<path d="M100 28 L190 60 L190 90 L100 122 Z" class="g"/>' + f'<path d="M200 60 L290 60" class="g"/>'
    out += circ(350, 75, 9, "fa") + arrow(292, 75, 335, "g")
    return out + t(50, 142, "dips", cls="sm") + t(150, 142, "tests", cls="sm") + t(350, 142, "candidate", cls="sm")


def d11():
    out = ""
    for r in range(5):
        for c in range(5):
            out += f'<rect x="{150 + c * 24}" y="{15 + r * 24}" width="22" height="22" class="g" />'
    return out + circ(246, 75, 7, "fa") + circ(318, 112, 3, "f") + circ(246, 75, 30, "dash") + t(360, 42, "neighbour", "middle", "sm") + t(100, 79, "our star", "middle", "sm") + line(318, 112, 345, 48, "g")


def d12():
    out = "".join(ellipse(210, 75, 40 + 8 * i, 18 + 4 * i, "g", rot) for i, rot in enumerate([0, 25, 50, 75, 100, 125, 150, 175]))
    return out + ellipse(210, 75, 76, 38, "a", 25) + t(210, 146, "thousands of orbits tried, the best one kept", cls="sm")


def d13():
    out = t(30, 26, "D:\\second-sun", "start", "mono")
    for i, (n, s) in enumerate([("book", "this book"), ("labs", "scripts you run"), ("pipeline", "our search code"), ("research", "decisions, mistakes"), ("data", "downloads (not in git)")]):
        y = 50 + i * 20
        out += line(40, y - 14, 40, y - 4, "g") + line(40, y - 4, 56, y - 4, "g") + t(62, y, n, "start", "mono") + t(170, y, s, "start", "sm")
    return out


def d14():
    out = ""
    for i, a in enumerate(["a dip", "vetting", "short paper", "ExoFOP"]):
        x = 6 + i * 104
        out += box(x, 55, 90, 40, a, "l" if i != 3 else "a") + (arrow(x + 92, 75, x + 104, "g") if i < 3 else "")
    return out + t(210, 130, "publish first, then NASA's candidate site", cls="sm")


def d15():
    out = ""
    for i, a in enumerate(["numbers", "automation", "record", "rules", "words"]):
        x = 8 + i * 82
        out += box(x, 45, 74, 44, a) + t(x + 37, 112, f"pattern {i + 1}", cls="sm")
    return out


DIAGRAMS = {1: (d1, "One star, three catalogues, three numbers: Kepler-16."), 2: (d2, "Two kinds of dip in a light curve."),
            3: (d3, "From a camera in orbit to a file on your PC."), 4: (d4, "A planet circling two suns."),
            5: (d5, "Crossings that miss the clock."), 6: (d6, "The planet keeps outside the unstable zone."),
            7: (d7, "A dip has to stand out from the scatter."), 8: (d8, "Slide a box along the light curve; the score peaks at the dip."),
            9: (d9, "Hide a fake planet, then see if the search finds it."), 10: (d10, "Most dips do not survive the tests."),
            11: (d11, "Whose light dimmed? Look at the pixels."), 12: (d12, "Try thousands of orbits and keep the one that stacks."),
            13: (d13, "Everything lives in one folder."), 14: (d14, "Publish first, then NASA's candidate site."),
            15: (d15, "Five patterns behind fifteen mistakes.")}


def figure(n):
    fn, cap = DIAGRAMS[n]
    return (f'<figure class="ss-dg"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{escape(cap)}"><title>{escape(cap)}</title>{fn()}</svg>'
            f'<figcaption>{escape(cap)}</figcaption></figure>')


if __name__ == "__main__":
    for n in DIAGRAMS:
        s = figure(n)
        assert s.count("<svg") == 1 and "\u2014" not in s and "\u2013" not in s and "nan" not in s, n
    print("diagrams self-check ok:", len(DIAGRAMS))
