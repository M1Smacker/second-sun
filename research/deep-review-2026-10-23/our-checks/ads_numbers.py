"""Check the specific numbers the review quotes against the ADS abstracts (and authors) saved by ads_check.py."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(os.path.join(os.path.dirname(__file__), "ads_out.json")))
CHECK = {
    "Oddo+2026 TESS M-dwarf CBP occurrence": [r"33", r"95", r"candidate", r"Martin"],
    "Martin 2017 transits come and go": [r"17", r"30", r"hidden|not transit|currently"],
    "Kostov+2020 multiple transits": [r"\b4\b|four", r"11|eleven", r"conjunction"],
    "Kostov+2025 TESS Ten Thousand": [r"1,?371", r"2,?458", r"Kepler"],
    "Armstrong+2014": [r"10", r"6 ?R|6R", r"300"],
    "Davies+2026 mono-cbp": [r"512", r"79", r"SAP|PDC", r"50", r"75"],
    "Borkovits+2025 Kepler EB ETVs w/ TESS": [r"243", r"triple", r"TESS"],
    "Kristiansen+2022 VSG": [r"72", r"69", r"welcome|surveyor"],
    "Battley+2021": [r"2066", r"Kepler-34|circumbinary"],
    "Kostov+2021 TIC 172900988": [r"one sector|single sector", r"false"],
    "Huang+2020 QLP": [r"spline|0\.3|long"],
    "Borkovits+2026 northern CVZ": [r"vanish|disappear", r"depth"],
}
for label, pats in CHECK.items():
    doc = d.get(label)
    if not doc:
        print("MISSING", label); continue
    ab = doc.get("abstract", "")
    au = "; ".join(doc.get("author", [])[:8])
    hits = {p: bool(re.search(p, ab + " " + au, re.I)) for p in pats}
    print(f"\n### {label} [{doc['bibcode']}]\n authors: {au}\n hits: {hits}")
    for p in pats:
        for m in re.finditer(p, ab, re.I):
            s = max(0, m.start() - 110); print("   ..." + ab[s:m.end() + 110].replace("\n", " ") + "...")
            break
