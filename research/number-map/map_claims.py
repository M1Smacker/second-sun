"""T130 helper: for a page whose lines cite facts-register claims ({{claim:F-nnn}}), propose a TRACED row for every number on such a line
that appears in one of the cited claims' rows of book/data/claims.csv (snippet 'F-nnn,'), and print every other number for manual review.
Writes nothing: prints CSV rows to stdout (review, then append). Usage: python map_claims.py <page>"""
import csv, io, re, sys
from pathlib import Path
sys.path.insert(0, r"D:\second-sun\pipeline")
import number_map as N
sys.stdout.reconfigure(encoding="utf-8")
page = sys.argv[1]
claims = {}
for l in (N.ROOT / "book" / "data" / "claims.csv").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(F-\d+),", l)
    if m:
        claims[m.group(1)] = l
lines = (N.ROOT / page).read_text(encoding="utf-8").splitlines()
out, rest, done = [], [], set()
for ln, num, text in N.tokens(page):
    if (ln, num) in done:
        continue
    done.add((ln, num))
    ids = re.findall(r"claim:(F-\d+)", lines[ln - 1])
    hit = next((i for i in ids if i in claims and N.number_in(claims[i], num)), None)
    if hit:
        out.append(dict(page=page, line=ln, number=num, status="TRACED", source_file="book/data/claims.csv", snippet=hit + ",", source_number="", note=""))
    else:
        rest.append((ln, num, text.strip()[:110]))
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=["page", "line", "number", "status", "source_file", "snippet", "source_number", "note"], lineterminator="\n")
for r in out:
    w.writerow(r)
print(buf.getvalue(), end="")
for r in rest:
    print("REVIEW", *r, sep="\t")
