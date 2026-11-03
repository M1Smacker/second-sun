import glob, random, numpy as np, re, pathlib
from astropy.io import fits
random.seed(5)
files = glob.glob("D:/second-sun/data/g1/*/tess*-s*_lc.fits") + glob.glob("D:/second-sun/data/g2/*/tess*-s*_lc.fits")
by = {}
for f in files:
    m = re.search(r"-s(\d{4})-", f)
    if m: by.setdefault(int(m.group(1)), []).append(f)
print("SPOC 2-min files:", len(files), "sectors:", len(by))
iv_all, per_sector = [], {}
for sec, fl in sorted(by.items()):
    f = random.choice(fl)
    try:
        d = fits.getdata(f, 1); t = d["TIME"]; q = d["QUALITY"]
    except Exception: continue
    tt = t[((q & 32) > 0) & np.isfinite(t)]
    if len(tt) < 2: continue
    ev = [tt[0]]
    for x in tt[1:]:
        if x - ev[-1] > 0.3: ev.append(x)
    iv = np.diff(ev)
    if len(iv): per_sector[sec] = (len(ev), float(np.median(iv))); iv_all += list(iv)
iv_all = np.array(iv_all)
print("sectors sampled:", len(per_sector), "dump events:", sum(v[0] for v in per_sector.values()), "intervals:", len(iv_all))
print("interval days: min %.1f, 5%% %.1f, median %.1f, 95%% %.1f, max %.1f" % (iv_all.min(), *np.percentile(iv_all, [5, 50, 95]), iv_all.max()))
meds = np.array([v[1] for v in per_sector.values()]); print("per-sector median interval: min %.1f max %.1f" % (meds.min(), meds.max()))
# launch year: the earliest observation in our files
g = by[min(by)][0]; h = fits.getheader(g, 0); print("earliest sector in our files", min(by), "DATE-OBS", h.get("DATE-OBS") or fits.getheader(g, 1).get("DATE-OBS"))
cams = set(); 
for f in random.sample(files, 400): 
    h = fits.getheader(f, 0); cams.add((h.get("CAMERA"), h.get("CCD")))
print("camera/CCD pairs seen in 400 files:", len(cams), sorted(cams, key=str))
