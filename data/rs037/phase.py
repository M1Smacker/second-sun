import json, glob, numpy as np
R="D:/second-sun-astra/data/astra/006"
cap=[];unc=[];uncw=[]
for d in glob.glob(R+"/planet-*"):
    if d.endswith((".log",".json")) or "short" in d: continue
    for l in open(d+"/results.jsonl",encoding="utf-8"):
        r=json.loads(l); P=r["binary_period"]; E=r["binary_epoch"]
        try: sc=json.load(open(f"{d}/trial-{r['trial']}/scores.json"))
        except FileNotFoundError: continue
        capt={round(c,3) for s,a,tm,c,t,v in sc["1"] if tm==r["trial"] and a==1}
        for c,du in r["observed"]:
            ph=((c-E)/P)%1; dd=min(ph,1-ph,abs(ph-0.5))*P   # days from primary or a phase-0.5 secondary
            (cap if round(c,3) in capt else unc).append((dd,du,P))
for name,v in (("scored",cap),("never scored",unc)):
    v=np.array(v); near=v[:,0]<=v[:,1]/2+0.3
    print(f"{name:13s} n={len(v)}  share whose crossing overlaps the time of an eclipse (phase 0 or 0.5, +-half duration+0.3 d): {near.mean():.2f}")
    for lo,hi in ((0,7.5),(7.5,15),(15,30),(30,60),(60,1e9)):
        m=(v[:,2]>=lo)&(v[:,2]<hi)
        if m.sum(): print(f"   binary period {lo}-{hi} d: n={m.sum()} near eclipse {near[m].mean():.2f}")
