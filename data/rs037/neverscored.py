"""RS-038 task B: why are 24% of planted crossings never scored? For each uncaptured crossing classify, from the raw files and the
group meta of the planted run: (1) no cadence at all in any file (archive gap); (2) cadences only with quality flags (which bits);
(3) good cadences but the star-sector failed to prepare (meta status, e.g. too little data after masking); (4) good cadences, prepared,
but the crossing's cadences were removed inside the chain (eclipse mask or windows) or the scored product had none."""
import json, glob, collections, numpy as np
from astropy.io import fits
R="D:/second-sun-astra/data/astra/006"
o={tuple(x["key"]):x for x in json.load(open("data/rs037/per-planet.json"))}
cache={}
def files(camp,tic):
    if (camp,tic) in cache: return cache[(camp,tic)]
    out=[]
    for f in glob.glob(f"data/{camp}/{tic}/*.fits"):
        try:
            with fits.open(f,memmap=False) as h:
                d=h[1].data; cols=[c.name for c in h[1].columns]
                q=np.array(d["QUALITY"] if "QUALITY" in cols else d["QUALITY"],int); t=np.array(d["TIME"],float)
                fx=np.array(d["SAP_FLUX"] if "SAP_FLUX" in cols else d[cols[1]],float)
                out.append((f.split("\\")[-1].split("/")[-1],h[0].header.get("SECTOR"),t,q,np.isfinite(fx)))
        except Exception as e: pass
    cache[(camp,tic)]=out; return out
cls=collections.Counter(); bits=collections.Counter(); status=collections.Counter(); per_planet=collections.Counter()
for d in glob.glob(R+"/planet-*"):
    if d.endswith((".log",".json")) or "short" in d: continue
    camp=d[-2:]
    for l in open(d+"/results.jsonl",encoding="utf-8"):
        r=json.loads(l); key=(camp,r["trial"]); x=o.get(key)
        if not x: continue
        sc=json.load(open(f"{d}/trial-{r['trial']}/scores.json"))
        capt={round(c,3) for s,a,tm,c,t,v in sc["1"] if tm==r["trial"] and a==1}
        metas={}
        for g in glob.glob(f"{d}/trial-{r['trial']}/1/groups/*.json"):
            for m in json.load(open(g))["meta"]: metas[(m["sector"],m["product"])]=m.get("status","")
        lostc=0
        for c,du in r["observed"]:
            if round(c,3) in capt: continue
            lostc+=1
            hw=du/2; any_c=False; good=False; bset=collections.Counter(); sec=None
            for name,s,t,q,fin in files(camp,r["star"]):
                m=(np.abs(t-c)<=hw)&np.isfinite(t)
                if m.any():
                    any_c=True; sec=s
                    if ((q[m]==0)&fin[m]).sum()>=3: good=True
                    for b in range(16):
                        if (q[m]&(1<<b)).any(): bset[b+1]+=1
            if not any_c: k="1 no cadence in any file (archive gap)"
            elif not good:
                k="2 only quality-flagged cadences"
                for b in bset: bits[b]+=1
            else:
                st=[v for (s,p),v in metas.items() if s==sec]
                if st and all(v!="ok" for v in st):
                    k="3 star-sector failed to prepare"; status[st[0][:45]]+=1
                else: k="4 good data, prepared, removed inside the chain (mask, windows, product)"
            cls[k]+=1
        if x["n"]==0 and not x["rec"]: per_planet["planets with no scored crossing"]+=1
print("uncaptured crossings by cause:"); [print(f"  {v:5d} {k}") for k,v in sorted(cls.items())]
print("quality bits seen on class 2 (bit number, 1-indexed; 6=dump, 13=stray light, 8=manual exclude, 5=argabrightening):", dict(sorted(bits.items())))
print("failed-prepare status:", dict(status.most_common(6)))
