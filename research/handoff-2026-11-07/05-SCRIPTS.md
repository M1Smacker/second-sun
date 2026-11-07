# Scripts behind the outside review (7 Nov 2026)

Re-run these to check my numbers. Both are small and read only public files or your own outputs.

## 1. Forward-looking Census odds (WO-1)

Inputs are the E values per 10% rate from `research/stage3/census_step1/census-worth2.txt` (existing hunts E0, Census Ec for 1,400 and 3,000 G2-type stars, 3 sectors). The 0.9 factor is the FIX 28 shape correction (about 10% relative).

```python
import numpy as np
r=np.logspace(-3,np.log10(0.4),4000)            # occurrence rate grid
priors={"Kepler-like (lognormal, median 10%, x2 spread)":np.exp(-0.5*(np.log(r/0.10)/np.log(2))**2),
        "broad (log-uniform 1% to 20%)":((r>=0.01)&(r<=0.20)).astype(float)}
w=np.gradient(np.log(r))
# (E0 existing hunts per 10% rate, Census E per 10% rate) for f 1.5/1.8/2.2, rules A/B ; 1400 and 3000 stars, 3 sectors
cases={"low (f2.2 A)":(1.28,0.70,1.51),"middle (f1.8 A)":(1.57,0.86,1.85),"high (f1.5 B)":(2.89,1.59,3.41)}
comp=0.9   # FIX 28: quoted completeness ~10% generous
for pn,p in priors.items():
  print(pn)
  for cn,(E0,E14,E30) in cases.items():
    post=p*np.exp(-comp*E0*r/0.1)*w; post/=post.sum()
    pr=p*w/ (p*w).sum()
    for N,Ec in((1400,E14),(3000,E30)):
      P=(post*(1-np.exp(-comp*Ec*r/0.1))).sum(); Pnaive=1-np.exp(-Ec*0.1/0.1)
      print(f"  {cn:16s} N={N}: P(>=1 planet in Census data passing search) {P:5.1%}  [naive at exactly 10%, no null update: {Pnaive:5.1%}]  posterior median rate {r[np.searchsorted(np.cumsum(post),0.5)]:.3f}")
```

Output on 7 Nov 2026:

```
Kepler-like (lognormal, median 10%, x2 spread)
  low (f2.2 A)     N=1400: P(>=1 planet in Census data passing search) 36.1%  [naive at exactly 10%, no null update: 50.3%]  posterior median rate 0.066
  low (f2.2 A)     N=3000: P(>=1 planet in Census data passing search) 59.2%  [naive at exactly 10%, no null update: 77.9%]  posterior median rate 0.066
  middle (f1.8 A)  N=1400: P(>=1 planet in Census data passing search) 40.0%  [naive at exactly 10%, no null update: 57.7%]  posterior median rate 0.062
  middle (f1.8 A)  N=3000: P(>=1 planet in Census data passing search) 63.7%  [naive at exactly 10%, no null update: 84.3%]  posterior median rate 0.062
  high (f1.5 B)    N=1400: P(>=1 planet in Census data passing search) 51.8%  [naive at exactly 10%, no null update: 79.6%]  posterior median rate 0.050
  high (f1.5 B)    N=3000: P(>=1 planet in Census data passing search) 75.9%  [naive at exactly 10%, no null update: 96.7%]  posterior median rate 0.050
broad (log-uniform 1% to 20%)
  low (f2.2 A)     N=1400: P(>=1 planet in Census data passing search) 21.1%  [naive at exactly 10%, no null update: 50.3%]  posterior median rate 0.028
  low (f2.2 A)     N=3000: P(>=1 planet in Census data passing search) 37.5%  [naive at exactly 10%, no null update: 77.9%]  posterior median rate 0.028
  middle (f1.8 A)  N=1400: P(>=1 planet in Census data passing search) 23.5%  [naive at exactly 10%, no null update: 57.7%]  posterior median rate 0.026
  middle (f1.8 A)  N=3000: P(>=1 planet in Census data passing search) 40.9%  [naive at exactly 10%, no null update: 84.3%]  posterior median rate 0.026
  high (f1.5 B)    N=1400: P(>=1 planet in Census data passing search) 31.2%  [naive at exactly 10%, no null update: 79.6%]  posterior median rate 0.021
  high (f1.5 B)    N=3000: P(>=1 planet in Census data passing search) 52.0%  [naive at exactly 10%, no null update: 96.7%]  posterior median rate 0.021
```

## 2. CALNet list check (WO-2)

Run from the repo root (`D:\second-sun`). Downloads one 1.26 MB public file; per the downloads rule, put it in a new folder under `data\` and log it.

```python
import csv, pathlib, urllib.request
url = "https://raw.githubusercontent.com/wangleon/CALNet/main/outputs/newecl.dat"
out = pathlib.Path(r"D:\second-sun\data\calnet_2026-11-07"); out.mkdir(parents=True, exist_ok=True)
f = out / "newecl.dat"
urllib.request.urlretrieve(url, f)
rows = f.read_text().splitlines()[2:]                     # two header lines (fixed_width_two_line)
tics = {r.split()[0] for r in rows if r.strip()}
gmag = []
for r in rows:
    try: gmag.append(float(r.rstrip()[-5:]))
    except ValueError: pass
gmag.sort()
print("rows", len(rows), "unique TIC", len(tics), "median G", gmag[len(gmag)//2],
      "G<12", sum(g < 12 for g in gmag), "G<13.5", sum(g < 13.5 for g in gmag))
seen = set()
for name in ("g1_targets.csv", "g2_targets.csv", "g3_targets.csv"):
    rs = list(csv.DictReader(l for l in open(rf"D:\second-sun\targets\{name}") if not l.startswith("#")))
    t = {r["tic"] for r in rs}; seen |= t
    print(name, len(t), "in CALNet", len(t & tics))
print("CALNet stars never searched by G1 to G3:", len(tics - seen))
```

Output on 7 Nov 2026 (Linux copy of the repo): rows 10,531, unique 10,531, median G 11.68, G<12: 5,973, G<13.5: 8,277; G1 549 targets, 51 in CALNet; G2 895, 0; G3 612, 20; never searched 10,460.

Note: the Gmag parse reads the last five characters of each line; 46 rows had no G value. A proper read uses `astropy.io.ascii.read(f, format="fixed_width_two_line")`.
