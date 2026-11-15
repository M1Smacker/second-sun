import json, numpy as np, collections
o=json.load(open("data/rs037/per-planet.json"))
def P(flag):
    by=collections.defaultdict(list)
    for x in o: by[x["bin"]].append(flag(x))
    return round(float(np.mean([np.mean(v) for v in by.values()])),3)
lost=lambda x: (not x["rec"]) and max(x["s"],default=-9)>=7
for t2 in (4,5,6):
    print(f"lost-after-detection with a 2nd crossing >= {t2}:", P(lambda x: lost(x) and sorted(x["s"])[-2:][0]>=t2 if len(x["s"])>=2 else False), "of", P(lost))
# null side: how often does a no-planet position pair reach (>=7 and other >=t2)? per planet using null captures
for t2 in (4,5,6):
    a=[x for x in o if len(x["null"])>=2]
    hit=np.mean([ (sorted(x["null"])[-1]>=7 and sorted(x["null"])[-2]>=t2) for x in a])
    print(f"null pairs (>=7 and >= {t2}) at true positions:", round(float(hit),4), "n", len(a))
print("crossings in data per planet, B-missed with no capture:", collections.Counter(min(x["nobs"],5) for x in o if x["n"]==0 and not x["rec"]))
