import json, numpy as np, collections, math
o = json.load(open("data/rs037/per-planet.json"))
def P(flag):
    by = collections.defaultdict(list)
    for x in o: by[x["bin"]].append(flag(x))
    return round(float(np.mean([np.mean(v) for v in by.values()])),3)
nul = np.array([v for x in o for v in x["null"]])
mad = np.median(np.abs(nul-np.median(nul)))*1.4826
print("null robust std (MAD):", round(mad,2), " frac |snr|>7:", round(float(np.mean(np.abs(nul)>7)),4), " >7:", round(float(np.mean(nul>7)),4))
print("null pct 50/90/99/99.9:", np.percentile(nul,[50,90,99,99.9]).round(2))
z = [x for x in o if x["n"]==0]
print("no capture:", len(z), " with observed crossings in data:", sum(1 for x in z if x["nobs"]>0), " P share:", P(lambda x: x["n"]==0))
print("observed-but-uncaptured crossings over all planets:", sum(max(x["nobs"]-x["n"],0) for x in o), "of observed", sum(x["nobs"] for x in o))
best = lambda x: max(x["s"], default=-9)
eq = lambda x: (sum(x["s"])/math.sqrt(len(x["s"]))) if x["s"] else -9
print("pools (P points):")
print("  recovered by B:", P(lambda x: x["rec"]))
print("  single>=7 but B missed (lost in vetting/tiers):", P(lambda x: (not x["rec"]) and best(x)>=7))
print("  B missed, single<7, stack eq>=7:", P(lambda x: (not x["rec"]) and best(x)<7 and eq(x)>=7))
print("  B missed, single<7, stack eq>=9:", P(lambda x: (not x["rec"]) and best(x)<7 and eq(x)>=9))
print("  B missed, has captures, nothing reaches 7:", P(lambda x: (not x["rec"]) and x["n"]>0 and best(x)<7 and eq(x)<7))
print("  B missed, no capture:", P(lambda x: (not x["rec"]) and x["n"]==0))
print("  B recovered but best capture <7 (oddities):", P(lambda x: x["rec"] and best(x)<7))
# single >= 6 (looser single bar)
for t in (5,6):
    print(f"  single>={t} or B:", P(lambda x: x["rec"] or best(x)>=t))
