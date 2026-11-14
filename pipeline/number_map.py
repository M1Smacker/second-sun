"""Number-to-file audit for published result pages (BUILD T130; Claude, 14 Nov 2026; after Rabtsevich's NOTE_NUMBER_MAP.csv).
Every number printed in a page listed in research/number-map/PAGES.txt must have a row in research/number-map/NUMBER_MAP.csv saying where it comes
from: the source file and a snippet that must appear in that file on a line that also contains the number (or the row says NOT A RESULT: a date,
a list position, a version, a duration of reading). The check prints the coverage and every problem; exit 1 on any problem.
Problems: UNMAPPED (a number with no row), SOURCE MISSING (the file is gone), NOT IN SOURCE (no line of the file has both the snippet and the
number), STALE ROW (a row whose number is no longer on that page line), FLAGGED (status MISMATCH: a known problem waiting for Ahmed's wording call).
Numbers are matched as printed ("0.41", "803", "3.3"); thousands separators are removed ("2,381" = "2381").
Usage: python number_map.py            (check)      python number_map.py list <page>   (print every number token of a page with its line)"""
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(r"D:\second-sun")
NM = ROOT / "research" / "number-map"
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
SKIP = [re.compile(p) for p in (
    rf"\b\d{{1,2}} (?:{MONTHS})(?: \d{{4}})?",           # dates: 11 November 2026, 13 Nov
    r"\b(?:Petrova|Vesper|version|v)\s?\d+(?:\.\d+)+",   # versions
    r"\bday \d+\b", r"\babout \d+ min\b",                # the field-note meta line
    r"\b(?:G|S|T|FIX |RS-|WO-|F-)\d+\b",                 # names of lists, sectors, tasks
    r"^\s*\d+\.\s",                                       # list positions at the start of a line
    r"\(\d+\)", r"\b\d{4}-\d{2}-\d{2}\b")]
NUM = re.compile(r"(?<![\w.])\d{1,3}(?:,\d{3})+(?:\.\d+)?(?![\w])|(?<![\w.])\d+(?:\.\d+)?(?![\w])")


def tokens(page):
    out = []
    for i, line in enumerate((ROOT / page).read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith(("<p class=\"ss-meta\"", "#")):
            continue
        masked = line
        for p in SKIP:
            masked = p.sub(lambda m: " " * len(m.group(0)), masked)
        for m in NUM.finditer(masked):
            out.append((i, m.group(0).replace(",", ""), line))
    return out


def load_map():
    p = NM / "NUMBER_MAP.csv"
    return list(csv.DictReader(open(p, encoding="utf-8"))) if p.exists() else []


def number_in(line, num):
    return re.search(rf"(?<![\d.]){re.escape(num)}(?![\d])", line.replace(",", "")) is not None


def check():
    pages = [l.strip() for l in (NM / "PAGES.txt").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    rows = load_map()
    idx = {}
    for r in rows:
        idx.setdefault((r["page"], int(r["line"]), r["number"]), []).append(r)
    problems, n_tok, n_ok, n_nar = [], 0, 0, 0
    for page in pages:
        toks = tokens(page)
        seen = set()
        for line_no, num, text in toks:
            n_tok += 1
            key = (page, line_no, num); seen.add(key)
            rs = idx.get(key)
            if not rs:
                problems.append(f"UNMAPPED {page}:{line_no} {num}   | {text.strip()[:110]}")
                continue
            r = rs[0]
            st = r["status"]
            if st == "NOT A RESULT":
                n_nar += 1; continue
            if st == "DERIVED":                      # computed from mapped numbers; the note must say how
                if not r.get("note"):
                    problems.append(f"DERIVED WITHOUT NOTE {page}:{line_no} {num}")
                else:
                    n_ok += 1
                continue
            if st == "MISMATCH":
                problems.append(f"FLAGGED {page}:{line_no} {num}: {r['note']}")
                continue
            src = ROOT / r["source_file"]
            if not src.exists():
                problems.append(f"SOURCE MISSING {page}:{line_no} {num}: {r['source_file']}"); continue
            lines = src.read_text(encoding="utf-8", errors="replace").splitlines()
            if not any(r["snippet"] in l and number_in(l, r.get("source_number") or num) for l in lines):
                problems.append(f"NOT IN SOURCE {page}:{line_no} {num}: no line of {r['source_file']} has '{r['snippet']}' and {r.get('source_number') or num}")
                continue
            n_ok += 1
        for (pg, ln, num), rs in idx.items():
            if pg == page and (pg, ln, num) not in seen:
                problems.append(f"STALE ROW {pg}:{ln} {num} (no longer on that line)")
    cov = (n_ok + n_nar) / n_tok if n_tok else 1.0
    print(f"pages {len(pages)}, numbers {n_tok}: traced to a file {n_ok}, not a result {n_nar}, coverage {100 * cov:.1f}%")
    for p in problems:
        print("  " + p)
    return problems


def suggest(page, sources):
    """For every number of a page, the source line (among the given files) that contains the number and shares the most words with the page
    line. A suggestion only: every row is still reviewed by hand before it enters the map."""
    srcs = {s: (ROOT / s).read_text(encoding="utf-8", errors="replace").splitlines() for s in sources}
    words = lambda t: {w.lower() for w in re.findall(r"[A-Za-z]{4,}", t)}
    for ln, num, text in tokens(page):
        best = (0, None, None, None)
        for s, lines in srcs.items():
            for i, l in enumerate(lines, 1):
                if number_in(l, num):
                    sc = len(words(text) & words(l))
                    if sc > best[0]:
                        best = (sc, s, i, l.strip())
        print(f"{ln}\t{num}\t" + (f"{best[1]}:{best[2]} ({best[0]})\t{best[3][:150]}" if best[1] else "NO SOURCE LINE"))


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "suggest":
        suggest(sys.argv[2], sys.argv[3:]); sys.exit(0)
    if len(sys.argv) == 3 and sys.argv[1] == "list":
        for ln, num, text in tokens(sys.argv[2]):
            print(f"{ln}\t{num}\t{text.strip()[:140]}")
    else:
        sys.exit(1 if check() else 0)
