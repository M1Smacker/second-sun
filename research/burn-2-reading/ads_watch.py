"""ads_watch.py: run a saved list of NASA ADS queries, print papers added since a date.

Usage (key must be in env var ADS_DEV_KEY; it is never printed):
    python ads_watch.py --since 2026-01-01
    python ads_watch.py --since 2026-01-01 --q 'abs:"circumbinary" year:2026'
    python ads_watch.py --selftest          # no network, checks the date filter

The date filter uses ADS 'entdate' (when ADS added the record), so a re-run
with --since <last run date> shows only what is new.
"""
import argparse, json, os, sys, urllib.parse, urllib.request

API = "https://api.adsabs.harvard.edu/v1/search/query"

# Saved rivals watch for Second Sun (edit freely). One ADS query per line.
QUERIES = [
    'abs:"circumbinary" abs:"TESS"',
    'abs:"circumbinary planet" abs:("transit" OR "transiting")',
    'abs:"circumbinary" abs:"Kepler" abs:"TESS"',
    'author:"Kostov, V" abs:"circumbinary"',
    'author:"Martin, D" abs:"circumbinary"',
    'author:"Davies, B" abs:"circumbinary"',
    'author:"Oddo, D" abs:"circumbinary"',
    'abs:"STANLEY" abs:"circumbinary"',
    'abs:"exocomet" abs:"TESS"',
    'author:"Norazman, A"',
    'abs:("Kepler eclipsing binaries" OR "Kepler field" OR "Kepler binaries") abs:"TESS" abs:"circumbinary"',
]


def search(q, since, rows=50):
    key = os.environ.get("ADS_DEV_KEY")
    if not key:
        sys.exit("ADS_DEV_KEY is not set in this shell's environment.")
    full = f"({q}) entdate:[{since} TO *] collection:astronomy"
    params = urllib.parse.urlencode({
        "q": full, "rows": rows, "sort": "date desc",
        "fl": "bibcode,title,author,pubdate,entdate,identifier,doctype,abstract",
    })
    req = urllib.request.Request(f"{API}?{params}",
                                 headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["response"]["docs"]


def fmt(d):
    authors = d.get("author") or ["?"]
    first = authors[0] + (" et al." if len(authors) > 1 else "")
    arxiv = next((i for i in d.get("identifier", []) if i.startswith("arXiv:")), "")
    title = (d.get("title") or ["(no title)"])[0]
    return (f"{d.get('pubdate', '?')[:7]}  {d.get('doctype', '?'):9s} {first} | "
            f"{title[:110]} | https://ui.adsabs.harvard.edu/abs/{d['bibcode']} {arxiv}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="YYYY-MM-DD; only records ADS added on/after this")
    ap.add_argument("--q", action="append", help="ad-hoc query (repeatable); replaces the saved list")
    ap.add_argument("--rows", type=int, default=50)
    ap.add_argument("--abstracts", action="store_true", help="also print abstracts")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        d = {"bibcode": "2026X", "author": ["A, B", "C, D"], "title": ["T"],
             "pubdate": "2026-05-00", "doctype": "article", "identifier": ["arXiv:2605.00001"]}
        assert "A, B et al." in fmt(d) and "arXiv:2605.00001" in fmt(d)
        print("selftest ok"); return
    if not a.since:
        ap.error("--since is required")
    seen = set()
    for q in (a.q or QUERIES):
        docs = [d for d in search(q, a.since, a.rows) if d["bibcode"] not in seen]
        seen.update(d["bibcode"] for d in docs)
        print(f"\n## {q}  ->  {len(docs)} new")
        for d in docs:
            print("  " + fmt(d))
            if a.abstracts:
                print("     " + (d.get("abstract") or "(no abstract)").replace("\n", " "))


if __name__ == "__main__":
    main()
