import pandas as pd, json
from astropy.io import ascii
base=r'D:\second-sun\data'
p=pd.read_csv(base+r'\xmatch\ebs.csv'); print('prsa',len(p),p.TIC.nunique())
g=pd.read_csv(base+r'\calnet_2026-11-07\gaia_dr3_vari_eb_for_calnet.csv'); print('gaia-calnet',len(g),list(g.columns)[:20])
c=ascii.read(base+r'\calnet_2026-11-07\newecl.dat',format='fixed_width_two_line'); print('calnet',len(c),c.colnames)
d=json.load(open(base+r'\calnet_2026-11-07\parsed.json')); print('parsed keys',list(d), [len(v) for v in d.values()])
for t in ('table3_new_ebs','table4_known_ebs'):
    x=ascii.read(base+rf'\g3\catalog_ttc\{t}.txt',format='mrt'); print(t,len(x),x.colnames)
