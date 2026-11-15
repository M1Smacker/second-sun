"""RS-037 Q1: how far could adding up crossings carry P? Uses Astra 006 per-crossing SNR captures
(scores.json: sector, arm, template, centre, t, snr) and 023 config-B recovery. Read only."""
import json, glob, math, collections, sys
import numpy as np
R = r"D:/second-sun-astra/data/astra"
dirs = [d for d in glob.glob(R+"/006/planet-*") if "short" not in d and "score" not in d and not d.endswith(".log") and not d.endswith(".json")]
res = {}
for d in dirs:
    camp = d[-2:]
    for line in open(d+"/results.jsonl", encoding="utf-8"):
        r = json.loads(line); r["dir"] = d
        res[(camp, r["trial"])] = r
print("trials with results:", len(res), "dirs:", len(dirs))
B = {}
for camp in ("g2","g3"):
    p = json.load(open(f"{R}/023/planets-{camp}-V0.json"))
    i = p["configs"].index("B")
    for row in p["rows"]:
        B[(camp,row["trial"])] = (row["bin"], row["real"][i], row["flip"][i])
print("023 B rows:", len(B), "joined:", len(set(B)&set(res)))
out = []
for key,(b,rec,fl) in B.items():
    r = res.get(key)
    if not r: continue
    f = f'{r["dir"]}/trial-{key[1]}/scores.json'
    try: sc = json.load(open(f))
    except FileNotFoundError: continue
    def per(sign, arm):
        best = {}
        for sector, a, tmpl, centre, t, snr in sc[sign]:
            if a != arm or tmpl != key[1]: continue
            k = round(centre, 3)
            best[k] = max(best.get(k, -99), snr)   # one value per crossing
        return list(best.values())
    s_dip = per("1", 1)       # planet planted, real arm
    s_null = per("0", 1)      # same crossing positions, no planet
    out.append(dict(key=key, bin=b, rec=rec, n=len(s_dip), s=s_dip, null=s_null, nobs=len(r["observed"])))
print("planets with captures:", len(out))
def comb(s, how):
    s = np.array(s, float)
    if len(s)==0: return -9
    if how=="eq": return s.sum()/math.sqrt(len(s))           # equal-weight stack, realistic
    if how=="q": return math.sqrt((np.clip(s,0,None)**2).sum())  # optimistic
nb = collections.Counter(o["bin"] for o in out)
def P(flag):  # equal weight per bin
    by = collections.defaultdict(list)
    for o in out: by[o["bin"]].append(flag(o))
    return np.mean([np.mean(v) for v in by.values()]), {k: round(float(np.mean(v)),3) for k,v in sorted(by.items())}
print("bins:", dict(sorted(nb.items())))
print("P under B (this subset):", P(lambda o: o["rec"]))
print("crossings per planet: ", collections.Counter(min(o["n"],6) for o in out))
for thr in (7, 8, 9, 10, 11):
    for how in ("eq","q"):
        print(f"stack {how} >= {thr}: P", P(lambda o: o["rec"] or comb(o["s"],how)>=thr))
print("single best >=7 (capture check):", P(lambda o: max(o["s"],default=-9)>=7))
for thr in (8,9,10):
  nul = [comb(o["null"],"eq") for o in out if o["null"]]
  print(f"null eq stack >= {thr} at fixed true positions:", np.mean(np.array(nul)>=thr), "n", len(nul))
nul = np.array([x for o in out for x in o["null"]]); print("null per-crossing snr mean, std:", nul.mean().round(2), nul.std().round(2), len(nul))
json.dump([dict(o, key=list(o["key"])) for o in out], open("D:/second-sun/data/rs037/per-planet.json","w"))
