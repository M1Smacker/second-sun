"""Every non-ASCII character the book shows must be drawn by a font the book itself serves (F4, 27 Oct 2026).
Why: before F4 all four served fonts lacked the Greek letters and maths signs used in the text (σ 38 times, ≈ 28 times, μ 11 times), so each phone
quietly borrowed them from its own system font. This test makes that finding permanent.
It reads the list of characters per font file from tools/font_coverage.json (made by make_font_coverage.py), refuses the list if a font file no longer
matches its recorded sha256, applies the unicode-range the CSS declares (a symbol the file has but the CSS does not claim is NOT drawn), and then checks the
text of the docs, data and scripts and, when a built site folder is given, of the built pages.
Usage: python tools/test_fonts.py [built_site_dir]      (standard library only)"""
import hashlib, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
FONTS = BOOK / "docs" / "assets" / "fonts"
READING = {"Atkinson Hyperlegible Next", "IBM Plex Sans", "SS Symbols", "SS Cross"}      # the faces a sentence of prose can use (Plex Mono is for code)


def parse_range(s):
    out = set()
    for part in s.split(","):
        part = part.strip().upper().replace("U+", "")
        if "-" in part:
            a, b = part.split("-"); out.update(range(int(a, 16), int(b, 16) + 1))
        elif part:
            out.add(int(part, 16))
    return out


def faces(css):
    res = []
    for block in re.findall(r"@font-face\s*\{(.*?)\}", css, re.S):
        fam = re.search(r'font-family:\s*"([^"]+)"', block).group(1)
        f = re.search(r'url\("fonts/([^"]+)"\)', block).group(1)
        ur = re.search(r"unicode-range:\s*([^;]+);", block)
        res.append((fam, f, parse_range(ur.group(1)) if ur else None))
    return res


def drawn_set(css, cov):
    out = {}
    for fam, f, ur in faces(css):
        if fam not in READING:
            continue
        cps = set(cov[f]["cps"])
        if ur is not None:
            cps &= ur
        out.setdefault(fam, set()).update(cps)
    return out


def missing(chars, drawn):
    ok = set().union(*drawn.values())
    return sorted(c for c in chars if ord(c) > 127 and ord(c) not in ok)


def strip_js(t):
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    return re.sub(r"(?m)(^|[^:\"'\\])//.*$", r"\1", t)


def source_chars():
    chars = {}
    for root in ("docs", "data", "progress", "overrides"):
        for p in (BOOK / root).rglob("*"):
            if not p.is_file() or "assets/fonts" in p.as_posix() or p.name.endswith(".min.js"):
                continue
            if p.suffix not in (".md", ".yml", ".yaml", ".html", ".js", ".csv"):
                continue
            t = p.read_text(encoding="utf-8", errors="ignore")
            if p.suffix == ".js":
                t = strip_js(t)
            for c in set(t):
                if ord(c) > 127:
                    chars.setdefault(c, set()).add(p.name)
    return chars


def site_chars(site):
    chars = {}
    for p in Path(site).rglob("*.html"):
        t = p.read_text(encoding="utf-8", errors="ignore")
        t = re.sub(r"<(script|style)\b.*?</\1>", " ", t, flags=re.S | re.I)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
        for c in set(t):
            if ord(c) > 127:
                chars.setdefault(c, set()).add(p.relative_to(site).as_posix())
    j = Path(site) / "assets" / "glossary.json"
    if j.exists():
        for c in set(j.read_text(encoding="utf-8")):
            if ord(c) > 127:
                chars.setdefault(c, set()).add("glossary.json")
    return chars


def main():
    cov = json.loads((HERE / "font_coverage.json").read_text(encoding="utf-8"))
    css = (BOOK / "docs" / "assets" / "observatory.css").read_text(encoding="utf-8")
    served = {p.name for p in FONTS.glob("*.woff2")}
    for name in sorted(served):                                                  # 1. the list matches the files
        assert name in cov, f"{name} has no entry in font_coverage.json: run tools/make_font_coverage.py"
        assert hashlib.sha256((FONTS / name).read_bytes()).hexdigest() == cov[name]["sha256"], f"{name} changed since font_coverage.json was made: run tools/make_font_coverage.py"
    for fam, f, _ in faces(css):                                                 # 2. every declared face has its file
        assert f in served, f"observatory.css declares {fam} from fonts/{f}, which does not exist"
    for name in served:                                                          # 3. no served font is left undeclared (dead weight in the offline cache)
        assert any(f == name for _, f, _ in faces(css)), f"fonts/{name} is not used by any @font-face"
    drawn = drawn_set(css, cov)
    assert missing({"\u210f", "\u2603"}, drawn) == ["\u210f", "\u2603"], "the checker must refuse characters no served font draws"   # 4. it can say no
    assert missing({"\u03c3", "\u2248", "\u2717", "\u00e9", "\u2192"}, drawn) == [], "σ ≈ ✗ é → must be drawn"
    sources = source_chars()
    bad = missing(sources, drawn)
    assert not bad, "characters no served font draws: " + ", ".join(f"{c} U+{ord(c):04X} in {sorted(sources[c])[:3]}" for c in bad)
    n_site = 0
    if len(sys.argv) > 1:
        built = site_chars(sys.argv[1])
        bad = missing(built, drawn)
        assert not bad, "built pages show characters no served font draws: " + ", ".join(f"{c} U+{ord(c):04X} in {sorted(built[c])[:3]}" for c in bad)
        n_site = len(built)
    only_sym = sorted(c for c in sources if ord(c) in (drawn["SS Symbols"] | drawn["SS Cross"]) and ord(c) not in (drawn["Atkinson Hyperlegible Next"] | drawn["IBM Plex Sans"]))
    print(f"pass: {len(sources)} distinct non-ASCII characters in the sources" + (f" and {n_site} in the built pages" if n_site else "")
          + f" are all drawn by the fonts the book serves ({len(only_sym)} of them by the two symbol files: {''.join(only_sym)})")


if __name__ == "__main__":
    main()
