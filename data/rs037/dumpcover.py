"""RS-038: how much of each sector lies inside our dump window (0.25 d after to 0.5 d before a dump, quality bit 32)? Do files carry centroids?"""
import glob, random, numpy as np, collections, re, sys
from astropy.io import fits
random.seed(1)
stars=glob.glob("data/g2/*/")+glob.glob("data/g3/*/")
random.shuffle(stars)
rows=[]; cols=collections.Counter(); seen=0
for s in stars:
    for f in glob.glob(s+"*.fits"):
        if "qlp" in f.lower(): continue
        try:
            with fits.open(f, memmap=False) as h:
                d=h[1].data; t=d["TIME"]; q=d["QUALITY"]; names=[c.name for c in h[1].columns]
                sec=h[0].header.get("SECTOR")
        except Exception as e: continue
        for c in ("MOM_CENTR1","POS_CORR1","PSF_CENTR1"): cols[c]+= c in names
        ok=np.isfinite(t); t,q=t[ok],q[ok]
        dumps=t[(q&32)>0]
        if len(t)<100: continue
        good=t[(q&(32|4|8|128))==0] if False else t
        near=np.zeros(len(t),bool)
        for dd in dumps: near|=(dd-t>-0.25)&(dd-t<0.5)
        span=t.max()-t.min()
        rows.append((sec, len(dumps), span/max(len(dumps),1), near.mean()))
        seen+=1
    if seen>=400: break
r=np.array(rows,float)
print("files:",len(r), "centroid columns present:",dict(cols))
for lo,hi in ((1,26),(27,55),(56,99)):
    m=(r[:,0]>=lo)&(r[:,0]<=hi)
    if m.sum(): print(f"sectors {lo}-{hi}: n={m.sum()} dumps/sector median {np.median(r[m,1]):.0f}, days between dumps {np.median(r[m,2]):.1f}, share of cadences inside dump window {np.median(r[m,3]):.3f} (90th pct {np.percentile(r[m,3],90):.3f})")
