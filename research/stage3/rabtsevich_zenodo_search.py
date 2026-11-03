"""List public Zenodo records matching Rabtsevich (metadata only, no files). Usage: python -I rabtsevich_zenodo_search.py"""
import json, urllib.request, urllib.parse, re
q = urllib.parse.quote('creators.name:"Rabtsevich" OR "TIC 4206066"')
req = urllib.request.Request(f"https://zenodo.org/api/records?q={q}&sort=newest&size=20", headers={"User-Agent": "Mozilla/5.0 (SecondSun research)"})
d = json.load(urllib.request.urlopen(req, timeout=60))
for h in d["hits"]["hits"]:
    m = h["metadata"]
    print(h["id"], "|", m.get("publication_date"), "|", m.get("resource_type", {}).get("title"), "| v", m.get("version"), "|", m.get("title"), "| files:", [(f["key"], f["size"]) for f in h.get("files", [])][:6])
