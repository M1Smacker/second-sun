"""Counts-only phase and morphology comparison for design-set tier transitions."""
import importlib,json,math,os,sys
from collections import Counter,defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('005_harness')
name=sys.argv[1]
os.environ.update(SS_SET=name,VESPER_OPTS='c6,p1',NUMBA_NUM_THREADS='2')
g=H.Guard();g.start()
import numpy as np
import pandas as pd
import petrova_mask as PM
catalogue=PM.cat()
metadata=pd.read_csv(H.TARGETS,comment='#')
metadata=metadata[(metadata['list']==name)&(metadata.design_seen==1)].drop_duplicates('tic').set_index('tic')
depths={}
if name=='g2':
    table=pd.read_csv(H.DATA/'xmatch'/'ebs.csv',usecols=['TIC','Wp-pf','Ws-pf','Dp-pf','Ds-pf','Dp-2g','Ds-2g']).drop_duplicates('TIC')
    table=table[table.TIC.isin(metadata.index)]
    for r in table.to_dict('records'):
        depths[r['TIC']]=tuple(abs(r[f'D{e}-pf'] if r[f'W{e}-pf']>0 else r[f'D{e}-2g']) for e in ('p','s'))
else:
    table=H.DATA/'g3'/'catalog_ttc'/'table3_new_ebs.txt'
    for line in table.read_text(encoding='latin-1').splitlines():
        if not line[:10].strip().isdigit():continue
        star=int(line[:10])
        if star not in metadata.index or star in depths:continue
        try:period=float(line[44:53])
        except ValueError:continue
        if abs(period/metadata.at[star,'p_bin_d']-1)>=.02:continue
        def depth_field(a,b):
            try:return abs(float(line[a:b]))/1000
            except ValueError:return math.nan
        depths[star]=depth_field(64,67),depth_field(88,94)
source=json.loads((H.OUT/f'phase-input-{name}.json').read_text(encoding='utf-8'))
peers=defaultdict(list)
for arm,star,sector,product,centre,depth,duration in source['candidates']:
    peers[arm,star,sector,product].append(centre)

def ratio_bin(value):
    return 'missing' if not math.isfinite(value) else '<0.5' if value<.5 else '0.5 to 1' if value<1 else '1 to 2' if value<2 else '>=2'

def summary(rows):
    counts={k:Counter() for k in ['product','era','primary_width','secondary_width','nearest_width','duration_ratio','depth_ratio','cycle_partner']}
    stars=Counter()
    for arm,star,sector,product,centre,depth,duration in rows:
        eclipse_depth=math.nan
        stars[star]+=1
        counts['product'][product]+=1;counts['era']['<56' if sector<56 else '56 to 93' if sector<94 else '94+']+=1
        c=catalogue.get(star)
        if c and math.isfinite(c['wp']) and c['wp']>0:
            phase=(centre-c['T0'])/c['P']; sec_ok=math.isfinite(c['phs']) and math.isfinite(c['ws']) and c['ws']>0
            off=c['phs'] if sec_ok else .5; ws=c['ws'] if sec_ok else c['wp']
            primary=abs(phase-round(phase))*c['P']/c['wp']
            secondary=abs(phase-off-round(phase-off))*c['P']/ws
            for key,value in [('primary_width',primary),('secondary_width',secondary),('nearest_width',min(primary,secondary))]:counts[key][ratio_bin(value)]+=1
            counts['duration_ratio'][ratio_bin(duration/24/(c['wp'] if primary<=secondary else ws))]+=1
            if star in depths and (primary<=secondary or sec_ok):
                eclipse_depth=depths[star][int(secondary<primary)]
        else:
            for key in ['primary_width','secondary_width','nearest_width','duration_ratio']:counts[key]['missing']+=1
        counts['depth_ratio'][ratio_bin(abs(depth)*1e-6/eclipse_depth if eclipse_depth>0 else math.nan)]+=1
        period=float(metadata.at[star,'p_bin_d'])
        times=peers[arm,star,sector,product]
        for label,factor in [('half',.5),('one',1),('twice',2)]:
            if any(abs(abs(t-centre)-factor*period)<=1/24 for t in times):counts['cycle_partner'][label]+=1
        for label,factor in [('half-triple',.5),('one-triple',1),('twice-triple',2)]:
            offsets=[round((t-centre)/(factor*period)) for t in times if t!=centre and abs(t-centre-round((t-centre)/(factor*period))*factor*period)<=1/24]
            if len(set(offsets)-{0})>=2:counts['cycle_partner'][label]+=1
    return dict(events=len(rows),stars=len(stars),max_per_star=max(stars.values(),default=0),star_multiplicity=dict(Counter(stars.values())),**counts)
result={f'{cohort}_{arm}':summary([r for r in source[cohort] if r[0]==arm]) for cohort in ('old','gained','lost') for arm in ('real','flip')}
(H.OUT/f'phase-summary-{name}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
