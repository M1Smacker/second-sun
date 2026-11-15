import json, collections, math, glob
R="D:/second-sun-astra/data/astra/006"
o = json.load(open("data/rs037/per-planet.json"))
res={}
for d in glob.glob(R+"/planet-*"):
    if d.endswith((".log",".json")) or "short" in d: continue
    for l in open(d+"/results.jsonl",encoding="utf-8"):
        r=json.loads(l); res[(d[-2:],r["trial"])]=(d,r)
tiers=collections.Counter(); flags=collections.Counter(); why=collections.Counter(); n=0
for x in o:
    if x["rec"] or max(x["s"],default=-9)<7: continue
    n+=1
    d,r=res[tuple(x["key"])]
    best=None
    for f in glob.glob(f'{d}/trial-{r["trial"]}/1/groups/*.json'):
        g=json.load(open(f))
        for e in g["events"]:
            if e["kind"]!="real": continue
            for c,dur in r["observed"]:
                if abs(e["center"]-c)<=max(dur/2,0.25) and (best is None or e["snr"]>best["snr"]): best=e
    if best is None: why["no event near crossing (dropped before events)"]+=1; continue
    tiers[best["tier"]]+=1
    for k in ("repeater","dominated","ramp","step","burst","gap_dump","flipmatch","ecl_overlap","c5"):
        if best.get(k): flags[k]+=1
    for fl in str(best.get("flags","")).split(";"):
        if fl.strip(): flags["text: "+fl.strip()[:50]]+=1
print("planets lost after detection:",n); print("no event:",dict(why)); print("tier of best matched event:",dict(tiers))
for k,v in flags.most_common(20): print(f"  {v:4d} {k}")
