"""Read saved trials only: independent counts, stratified tables, fixed-window comparisons."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(r'D:\second-sun-astra');OUT=ROOT/'data/astra/003'
rows=[json.loads(x) for p in (OUT/'workers').glob('*/results-*.jsonl') for x in p.read_text(encoding='utf-8').splitlines()]
assert len(rows)==len({r['trial'] for r in rows})==2000
ref=lambda r:3000<=r['depth_ppm']<=6000 and 6<=r['duration_h']<=12
rr=[r for r in rows if ref(r)];summary=json.loads((OUT/'recovery-summary.json').read_text(encoding='utf-8'))
rate=sum(sum(r['dip']['recovered'] for r in rr if r['bin']==k)/sum(r['bin']==k for r in rr) for k in range(5))/5
assert abs(rate-summary['R'])<1e-14
labels=['5 to 10','10 to 14','14 to 20','20 to 27.4','27.4+']
lines=['# 003 final tables','', 'CONFIRMED: independent journal aggregation, no pipeline imports or new searches. Counts are dip recoveries unless stated. Intervals are the saved star-cluster bootstrap, not independently recomputed.','']
def table(headers,data):
    lines.extend(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|'])
    lines.extend('| '+' | '.join(map(str,row))+' |' for row in data);lines.append('')
pc=lambda x:f'{100*x:.1f}%'
lines+=['## Period and paired control','']
table(['Period d','Ref recovered/n','Ref R, 95% CI','All dip/bump (n=400)','Dip-only / bump-only','Paired difference 99% CI, points'],[
 [labels[k],f"{b['reference_dip']}/{b['reference_n']}",f"{pc(b['reference_R'])} [{pc(b['reference_ci95'][0])}, {pc(b['reference_ci95'][1])}]",f"{b['dip']}/{b['bump']}",f"{b['dip_only']}/{b['bump_only']}",f"[{100*b['paired_difference_ci99'][0]:.2f}, {100*b['paired_difference_ci99'][1]:.2f}]"] for k,b in enumerate(summary['bins'])])
lines+=['All five paired, star-clustered 99% intervals include zero (Bonferroni across five bins). This is no detected aggregate difference, not proof of equivalence or absence of a structural bug. Reference totals: 61 dips, 62 bumps.','', '## Sequential losses','']
losses=[]
for title,source in [('Reference',rr),('All depths/durations',rows)]:
    data=[]
    for k in range(5):
        sub=[r for r in source if r['bin']==k];n=len(sub)
        counts=[sum(not r['dip']['recovered'] and r['dip']['stage']==j for r in sub) for j in range(5)]
        caught=sum(r['dip']['recovered'] for r in sub);assert sum(counts)+caught==n
        data.append([labels[k],n]+[f'{v} ({100*v/n:.1f}%)' for v in counts]+[caught])
        if title=='Reference':losses.append(counts)
    lines += [f'### {title}',''];table(['Period d','n','No windows','Outside/gap','Mask/support','No event','Below tier 1','Caught'],data)
lines+=['## Product, era, campaign and brightness','', 'Equal-bin R standardizes over five period bins; pooled reference fractions are also shown. Missing-best groups stay in the denominator. Sparse subgroup rates are descriptive, not separately calibrated decisions.','']
for split,vals in summary['splits'].items():
    lines += [f'### {split}',''];table(['Group','All n','Dip / bump','Ref recovered/n','Equal-bin R'],[[k,v['n'],f"{v['dip']}/{v['bump']}",f"{v['reference_dip']}/{v['reference_n']}",pc(v['R_equal_bins']) if v['R_equal_bins'] is not None else 'Unavailable'] for k,v in vals.items()])
lines+=['## Depth and duration cells','']
depths=['1000 to 2000','2000 to 3000','3000 to 6000','6000 to 10000'];dur=['3 to 6','6 to 12','12 to 18']
table(['Depth ppm','Duration h','n','Dip','Bump','Dip rate'],[[depths[c['depth_bin']],dur[c['duration_bin']],c['n'],c['dip'],c['bump'],pc(c['dip']/c['n'])] for c in summary['cells']])
variants={w:{r['trial']:r for p in (OUT/f'study-w{w}').glob('*/results-*.jsonl') for r in map(json.loads,p.read_text(encoding='utf-8').splitlines())} for w in (1,3)}
chosen=[r for r in rows if r['trial'] in variants[1]];assert len(chosen)==570
study=[]
for label,ws,require_all in [('2+1 day union',[1],False),('2+3 day union',[3],False),('2+1+3 day union',[1,3],False),('2 plus agreement of 1 and 3',[1,3],True)]:
    gains={}
    for arm in ('dip','bump'):
        test=all if require_all else any
        gains[arm]=sum(not r[arm]['recovered'] and test(variants[w][r['trial']][arm]['recovered'] for w in ws) for r in chosen)
    study.append([label,gains['dip'],gains['bump']])
lines+=['## Saved-window alternatives (exploratory post hoc reading)','', 'No new settings were run. Agreement is a post hoc diagnostic, not a validated selected rule. Bump gains below are newly recovered injected bumps, not background false alarms.','']
table(['Rule on selected failures','New dips','New planted bumps'],study)
lines+=['## Short-period context','']
context=[]
for key,fun in [('product',lambda r:r['product']),('campaign',lambda r:r['campaign']),('brightness',lambda r:'<11' if r['tmag']<11 else '11-12' if r['tmag']<12 else '12+')]:
    for val in sorted({fun(r) for r in rr}):
        a=[r for r in rr if r['bin']==0 and fun(r)==val];b=[r for r in rr if r['bin']!=0 and fun(r)==val]
        context.append([key,val,f"{sum(r['dip']['recovered'] for r in a)}/{len(a)}",f"{sum(r['dip']['recovered'] for r in b)}/{len(b)}"])
table(['Split','Group','5 to 10 d recovery','Other bins pooled'],context)
(ROOT/'research/astra/reports/003-tables.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
result=dict(R=rate,reference_n=len(rr),reference_losses=losses,study=study,short_context=context)
(OUT/'followup-counts.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
