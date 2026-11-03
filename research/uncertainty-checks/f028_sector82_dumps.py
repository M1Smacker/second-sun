import glob, numpy as np
from astropy.io import fits
fl = glob.glob("D:/second-sun/data/g1/*/tess*-s0082-*_lc.fits") + glob.glob("D:/second-sun/data/g2/*/tess*-s0082-*_lc.fits")
print(len(fl), "sector 82 files")
for f in fl[:4]:
    d = fits.getdata(f, 1); t = d["TIME"]; q = d["QUALITY"]
    tt = t[((q & 32) > 0) & np.isfinite(t)]
    ev = [tt[0]]
    for x in tt[1:]:
        if x - ev[-1] > 0.3: ev.append(x)
    print(f.split("\\")[-1][:40], len(ev), "events; intervals", np.round(np.diff(ev), 1))
