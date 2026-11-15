import os, sys, json, glob, collections, numpy as np
os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1"); sys.path.insert(0, os.path.abspath("pipeline"))
import petrova_mask as PM
C = PM.cat()
def cover(tic, t):
    c = C.get(int(tic))
    if c is None or not np.isfinite(c.get("wp", np.nan)): return (np.nan, np.nan)
    P, T0 = c["P"], c["T0"]; eT0 = c["eT0"] if np.isfinite(c.get("eT0", np.nan)) else 0.0; eP = c["eP"] if np.isfinite(c.get("eP", np.nan)) else 0.0
    n = abs(np.round((t - T0) / P)); drift = 3*np.sqrt(eT0**2 + (n*eP)**2)
    sec_ok = np.isfinite(c["phs"]) and np.isfinite(c["ws"]); ws = c["ws"] if sec_ok else c["wp"]
    return min(1.0, min(1.0,(PM.PADF*c["wp"]+2*drift)/P) + min(1.0,(PM.PADF*ws+2*drift)/P)), min(1.0,(PM.PADF*c["wp"]+PM.PADF*ws)/P)
o = json.load(open("data/rs037/per-planet.json"))
res = {}
for d in glob.glob("D:/second-sun-astra/data/astra/006/planet-*"):
    if d.endswith((".log",".json")) or "short" in d: continue
    for l in open(d+"/results.jsonl",encoding="utf-8"):
        r = json.loads(l); res[(d[-2:], r["trial"])] = r
rows = []
for x in o:
    r = res[tuple(x["key"])]
    cs = [cover(r["star"], c)[0] for c, du in r["observed"]] or [np.nan]
    w = [cover(r["star"], c)[1] for c, du in r["observed"]] or [np.nan]
    rows.append((x["bin"], x["rec"], np.nanmean(cs) if np.isfinite(cs).any() else np.nan, np.nanmean(w) if np.isfinite(w).any() else np.nan, x["n"], len(r["observed"])))
a = np.array(rows, float)
blown = a[:,2] - a[:,3] > 0.25   # drift adds more than a quarter of the orbit
print("planets:", len(a), " planets whose star's windows are blown by drift (+25% of orbit or more at its crossing times):", int(blown.sum()))
def P(mask_fn):
    by = collections.defaultdict(list)
    for row, m in zip(a, mask_fn): by[row[0]].append(m)
    return round(float(np.mean([np.mean(v) for v in by.values()])), 3)
print("  share of P weight on blown stars:", P(blown))
print("  B recovery on blown stars:", round(float(a[blown,1].mean()),3), " on other stars:", round(float(a[~blown,1].mean()),3))
print("  crossings scored on blown stars:", int(a[blown,4].sum()), "of", int(a[blown,5].sum()), " | others:", int(a[~blown,4].sum()), "of", int(a[~blown,5].sum()))
gain = blown & (a[:,1]==0)
print("  P points held by missed planets on blown stars (upper bound of a fix):", P(gain), " realistic (other-star recovery rate x share):", round(P(blown)*(a[~blown,1].mean()-a[blown,1].mean()),3))
