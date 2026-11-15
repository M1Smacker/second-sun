"""RS-038 task A (preregistered here, before any result): does star-position jitter separate dump-flagged false alarms from planted planet dips?
Metric J (fixed now): in each SPOC/TESS-SPOC file, take MOM_CENTR1 and MOM_CENTR2 (quality 0 and finite), subtract a 1-day running median,
scale each by its sector robust spread (MAD x 1.4826), J = max of sqrt(z1^2+z2^2) over cadences within the event (centre +- half duration, at least +-2 h).
Planted dips: real data at the planted time (flux-only injection, so the centroid is what a real planet would face). Reported at J thresholds 3, 5, 8, 12; nothing tuned."""
import json, glob, collections, numpy as np
from astropy.io import fits
R="D:/second-sun-astra/data/astra/006"
def fpath(camp,tic,sector,product):
    pats={"QLP":f"data/{camp}/{tic}/hlsp_qlp_tess_ffi_s{sector:04d}-{tic:016d}*.fits","SPOC":f"data/{camp}/{tic}/tess*-s{sector:04d}-*{tic:016d}*_lc.fits","TESS-SPOC":f"data/{camp}/{tic}/hlsp_tess-spoc*{tic:016d}-s{sector:04d}*.fits"}
    if product not in pats: return None
    g=glob.glob(pats[product]); return g[0] if g else None
cache={}
def cent(path):
    if path in cache: return cache[path]
    try:
        with fits.open(path,memmap=False) as h:
            d=h[1].data; t=np.array(d["TIME"],float); q=np.array(d["QUALITY"]); cn=[c.name for c in h[1].columns]; a,b=("MOM_CENTR1","MOM_CENTR2") if "MOM_CENTR1" in cn else ("SAP_X","SAP_Y"); c1=np.array(d[a],float); c2=np.array(d[b],float)
    except Exception: cache[path]=None; return None
    ok=np.isfinite(t)&np.isfinite(c1)&np.isfinite(c2)&(q==0)
    t,c1,c2=t[ok],c1[ok],c2[ok]
    if len(t)<200: cache[path]=None; return None
    z=[]
    for c in (c1,c2):
        r=c.copy()
        for i0 in range(0,len(t)):
            pass
        # running median via binning (fast): 1-day bins interpolated
        b=np.floor((t-t[0])/0.5); med=np.array([np.median(c[b==k]) for k in np.unique(b)]); tm=np.array([np.median(t[b==k]) for k in np.unique(b)])
        r=c-np.interp(t,tm,med); s=1.4826*np.median(np.abs(r-np.median(r))) or 1e-9
        z.append(r/s)
    cache[path]=(t,np.hypot(*z)); return cache[path]
def J(camp,e,dur_d=None):
    p=fpath(camp,e["tic"],e["sector"],e["product"])
    if not p: return None
    x=cent(p)
    if x is None: return None
    t,zz=x; hw=max((dur_d or e["dur_h"]/24)/2, 2/24)
    m=np.abs(t-e["center"])<=hw
    return float(zz[m].max()) if m.any() else None
camp_of=lambda d: d[-2:]
bg=collections.defaultdict(list); seen=set(); skipped=collections.Counter()
for f in glob.glob(R+"/planet-*/trial-*/0/groups/*.json"):
    k=(f.replace("\\","/").split("/")[-5][-2:], f.replace("\\","/").split("/")[-1])
    if k in seen: continue
    seen.add(k)
    for e in json.load(open(f))["events"]:
        if e["snr"]>=7 and e.get("gap_dump") and e["kind"] in ("real","flip"):
            j=J(k[0],e)
            if j is None: skipped[e["product"]]+=1
            else: bg[e["kind"]].append(j)
pl=[]; plost=[]
lost=set(tuple(x["key"]) for x in json.load(open("data/rs037/per-planet.json")) if (not x["rec"]) and max(x["s"],default=-9)>=7)
for d in glob.glob(R+"/planet-*"):
    if d.endswith((".log",".json")) or "short" in d: continue
    for l in open(d+"/results.jsonl",encoding="utf-8"):
        r=json.loads(l)
        for f in glob.glob(f"{d}/trial-{r['trial']}/1/groups/*.json"):
            for e in json.load(open(f))["events"]:
                if e["kind"]=="real" and e["snr"]>=7 and e.get("gap_dump"):
                    hit=[du for c,du in r["observed"] if abs(e["center"]-c)<=max(du/2,.25)]
                    if not hit: continue
                    j=J(camp_of(d),e)
                    if j is None: skipped["planted "+e["product"]]+=1; continue
                    pl.append(j)
                    if (camp_of(d),r["trial"]) in lost: plost.append(j)
print("skipped (no centroid file, mostly QLP):",dict(skipped))
for name,v in (("background real arm",bg["real"]),("background upside-down arm",bg["flip"]),("planted planet dips",pl),("planted, planets lost after detection",plost)):
    v=np.array(v); print(f"{name:40s} n={len(v):5d} median J {np.median(v):6.1f}  share J>=3 {np.mean(v>=3):.2f}  >=5 {np.mean(v>=5):.2f}  >=8 {np.mean(v>=8):.2f}  >=12 {np.mean(v>=12):.2f}")
