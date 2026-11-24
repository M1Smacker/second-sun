"""Census pool counts from eb_union.csv (Claude, 24 Nov 2026)."""
import pandas as pd, glob, re
u = pd.read_csv(r'D:\second-sun\data\census_union\eb_union.csv')
s = pd.read_csv(r'D:\second-sun\data\census_union\sources.csv')
print('TIC overlap prsa & calnet (any row):', len(set(s[s.source=='prsa2022'].tic) & set(s[s.source=='calnet+gaia_dr3'].tic)))
print('TIC overlap ttc_t3 & prsa:', len(set(s[s.source=='ttc_t3'].tic) & set(s[s.source=='prsa2022'].tic)))
late = set()
for f in glob.glob(r'D:\second-sun\data\census_targets_2m\all_targets_S*_v1.csv'):
    n = int(re.search(r'S(\d+)', f).group(1))
    if n >= 27:
        late |= set(pd.read_csv(f, comment='#').iloc[:, 0].astype('int64'))
u['twomin_s27plus'] = u.tic.isin(late)
new = u[u.searched.isna()]
base = new[(new.p_bin_d > 5) & new.has_ephemeris & new.has_width]
bright = base[base.tmag <= 13.5]
print('not searched:', len(new), '| P>5 eph+width:', len(base), '| of those Tmag<=13.5:', len(bright),
      '| Tmag unknown:', int(base.tmag.isna().sum()))
print('  bright with 2-min data in S27+:', int(bright.twomin_s27plus.sum()))
print('  bright by source:', bright.source.value_counts().to_dict())
print('  bright by period: 5-10', int(((bright.p_bin_d<=10)).sum()), '10-20', int(((bright.p_bin_d>10)&(bright.p_bin_d<=20)).sum()), '>20', int((bright.p_bin_d>20).sum()))
print('calnet with no period (needs our own fit):', int(((u.source=='calnet+gaia_dr3') & u.p_bin_d.isna()).sum()))
print('calnet in 2-min S27+:', int(((u.source=='calnet+gaia_dr3') & u.twomin_s27plus).sum()))
