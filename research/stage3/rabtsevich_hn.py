"""Read the public Hacker News thread about Rabtsevich via the HN Algolia API (item 50002665); print the story header and comments that look like the author's or that talk about method. Usage: python -I rabtsevich_hn.py"""
import json, urllib.request, re, html
UA = {"User-Agent": "Mozilla/5.0 (SecondSun research)"}
it = json.load(urllib.request.urlopen(urllib.request.Request("https://hn.algolia.com/api/v1/items/50002665", headers=UA), timeout=60))
print("story:", it.get("title"), "| by", it.get("author"), "| points", it.get("points"), "| url", it.get("url"), "| top-level comments", len(it.get("children", [])))
flat = []
def walk(n, depth=0):
    for c in n.get("children", []):
        t = re.sub(r"<[^>]+>", " ", html.unescape(c.get("text") or "")); flat.append((c.get("author"), depth, " ".join(t.split()))); walk(c, depth + 1)
walk(it); print("all comments:", len(flat))
authors = {}
for a, d, t in flat: authors[a] = authors.get(a, 0) + 1
print("busiest authors:", sorted(authors.items(), key=lambda x: -x[1])[:6])
pat = re.compile(r"\b(I'm the author|I am the author|my workflow|I used|I ran|prompt|subagent|fresh session|Codex|skeptic|shuffled|inject)\b", re.I)
n = 0
for a, d, t in flat:
    if pat.search(t) and len(t) > 120:
        n += 1
        if n <= 14: print(f"-- [{a}, depth {d}] {t[:520]}")
