"""Do background (no planet) dump-flagged events coincide across stars, while planted dips do not?"""
W=float(__import__("sys").argv[1])
import json, glob, collections, numpy as np
R="D:/second-sun-astra/data/astra/006"
bg={}
for f in glob.glob(R+"/planet-*/trial-*/0/groups/*.json"):
    k=f.replace("\\","/").split("/")[-1]
    if k in bg: continue
    g=json.load(open(f))
    bg[k]=[e for e in g["events"] if e["kind"] in ("real","flip")]
ev=[e for v in bg.values() for e in v]
print("star-sectors:",len(bg),"events:",len(ev), collections.Counter(e["kind"] for e in ev))
times=collections.defaultdict(list)
for e in ev: times[e["sector"]].append((e["center"],e["tic"]))
def others(e,w=W):
    return len({tic for c,tic in times[e["sector"]] if tic!=e["tic"] and abs(c-e["center"])<=w})
for kind in ("real","flip"):
  for lab,sel in (("dump-flagged",lambda e:e.get("gap_dump")),("not dump",lambda e:not e.get("gap_dump"))):
    xs=[e for e in ev if e["kind"]==kind and sel(e) and e["snr"]>=7]
    o=np.array([others(e) for e in xs])
    if len(o): print(f"{kind:4s} {lab:13s} n={len(xs):5d}  share with >=2 other stars within 0.1 d: {np.mean(o>=2):.2f}  >=1: {np.mean(o>=1):.2f}")
# planted dips: events in sign 1 matching planted crossings, flagged dump
res={}
for d in glob.glob(R+"/planet-*"):
    if d.endswith((".log",".json")) or "short" in d: continue
    for l in open(d+"/results.jsonl",encoding="utf-8"):
        r=json.loads(l); res[(d,r["trial"])]=r
o=[];n=0
for (d,tr),r in res.items():
    for f in glob.glob(f"{d}/trial-{tr}/1/groups/*.json"):
        for e in json.load(open(f))["events"]:
            if e["kind"]=="real" and e.get("gap_dump") and e["snr"]>=7 and any(abs(e["center"]-c)<=max(du/2,.25) for c,du in r["observed"]):
                o.append(others(e)); n+=1
o=np.array(o); print(f"planted dump-flagged dips n={n}  share with >=2 other stars: {np.mean(o>=2):.2f}  >=1: {np.mean(o>=1):.2f}")
