"""Look up every arXiv id the deep review cites in ADS. Key from ADS_DEV_KEY (never printed)."""
import os, sys, json, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")
key = os.environ.get("ADS_DEV_KEY") or sys.exit("ADS_DEV_KEY not set")
IDS = {
    "Davies+2026 mono-cbp": "2604.09435", "Martin 2017 transits come and go": "1611.00526",
    "Martin&Fabrycky 2021 STANLEY": "2101.03186", "Kostov+2020 multiple transits": "2008.02756",
    "Kostov+2021 TIC 172900988": "2105.08614", "Kostov+2025 TESS Ten Thousand": "2506.05631",
    "Oddo+2026 TESS M-dwarf CBP occurrence": "2610.22625", "Borkovits+2025 Kepler EB ETVs w/ TESS": "2502.09480",
    "Borkovits+2026 northern CVZ": "2604.04004", "Borkovits+2016": "1510.08272", "Slawson+2011": "1103.1659",
    "Huang+2020 QLP": "2011.06459", "Hippke+2019 wotan": "1906.00966", "Battley+2021": "2103.03259",
    "Welsh+2012": "1204.3955", "Doyle+2011": "1109.3432", "Kristiansen+2022 VSG": "2205.07832",
    "Armstrong+2014": "1404.5617", "Stassun+2018 TIC (ticgen cite)": "1706.00495",
}
def q(params):
    url = "https://api.adsabs.harvard.edu/v1/search/query?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + key})
    return json.load(urllib.request.urlopen(req, timeout=30))["response"]["docs"]
out = {}
for label, ax in IDS.items():
    docs = q({"q": f"identifier:arXiv:{ax}", "fl": "bibcode,title,author,year,pub,abstract", "rows": 1})
    if not docs:
        print(f"[NOT FOUND] {label} arXiv:{ax}"); continue
    d = docs[0]
    au = d.get("author", ["?"])
    print(f"[{d['bibcode']}] {label} | {au[0]}{' et al.' if len(au) > 1 else ''} {d.get('year')} | {d.get('title', ['?'])[0][:110]} | {d.get('pub')}")
    out[label] = d
json.dump(out, open(os.path.join(os.path.dirname(__file__), "ads_out.json"), "w"), indent=1)
# Martin, Mazeh, Fabrycky 2015 and Martin coauthorship on Oddo
for qq in ('author:"Martin, D" year:2015 bibstem:MNRAS volume:453 page:3554', ):
    for d in q({"q": qq, "fl": "bibcode,title", "rows": 2}):
        print("  extra:", d["bibcode"], d["title"][0][:100])
