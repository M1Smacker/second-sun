"""Print metadata (not files) of Rabtsevich's Zenodo records via the public API. Usage: python -I rabtsevich_zenodo_meta.py <record id> ..."""
import sys, json, urllib.request, re
for rid in sys.argv[1:]:
    req = urllib.request.Request(f"https://zenodo.org/api/records/{rid}", headers={"User-Agent": "Mozilla/5.0 (SecondSun research)"})
    d = json.load(urllib.request.urlopen(req, timeout=60)); m = d["metadata"]
    print("==", rid, "|", m.get("title"), "|", m.get("publication_date"), "|", m.get("resource_type", {}).get("title"), "| version", m.get("version"))
    print("   related:", [(r.get("relation"), r.get("identifier")) for r in m.get("related_identifiers", [])])
    for f in d.get("files", []): print("   file:", f["key"], f["size"], "bytes")
    desc = re.sub(r"<[^>]+>", " ", m.get("description", "")); print("   desc:", " ".join(desc.split())[:1800])
