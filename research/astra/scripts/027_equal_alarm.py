"""Run only the preregistered, conditionally authorized SNR ladder."""
from concurrent.futures import ThreadPoolExecutor
import importlib
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0,str(Path(__file__).parent))
M=importlib.import_module('027_summary')
ROOT=Path(r'D:\second-sun-astra')
OUT=ROOT/'data/astra/027'
PY=r'D:\second-sun\.venv\Scripts\python.exe'
LADDER=(7.,7.5,8.,8.5,9.,10.)


def main():
    import numpy as np
    summary=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
    choices={}
    for index,base,col in ((1,0,0),(3,2,3)):
        name=M.NAMES[index]
        if not summary['rules'][name]['equal_alarm_eligible']:
            continue
        bg={}
        for baseline in (True,False):
            bg[baseline]=[]
            for c in ('g2','g3'):
                d=json.loads((OUT/f'{"baseline-" if baseline else ""}planets-{c}-V0.json').read_text(encoding='utf-8'))
                bg[baseline]+=[e for e in d['background'] if e['options'][col]]
        target=sum(e['tic']%2==0 and e['kind']=='flip' for e in bg[True])
        ladder=[dict(floor=f,flip=sum(e['tic']%2==0 and e['kind']=='flip' and e['snr']>=f for e in bg[False])) for f in LADDER]
        floor=next((r['floor'] for r in ladder if r['flip']<=target),None)
        choices[name]=dict(index=index,base=base,column=col,floor=floor,choosing_base_flip=target,ladder=ladder)
    if not choices:
        print('Equal-alarm ladder not authorized: background is not the only failed rule.')
        return
    # All choosing decisions are saved before the held-out scoring runs.
    (OUT/'equal-alarm-choices.json').write_text(json.dumps(choices,indent=2),encoding='utf-8')
    def run(args):
        c,b,f=args
        file=OUT/f'{b}-{c}-V0-floor{f:g}.json'
        if file.exists():
            return
        with (OUT/f'equal-{b}-{c}-{f:g}.log').open('w',encoding='utf-8') as log:
            subprocess.run([PY,'-I','-B',str(ROOT/'research/astra/scripts/027_score.py'),c,b,'V0','--floor',str(f)],
                           cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    tasks=[(c,b,f) for f in sorted({r['floor'] for r in choices.values() if r['floor'] is not None and r['floor']!=7}) for b in ('planets','T156') for c in ('g2','g3')]
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run,tasks))
    original={b:json.loads((OUT/f'combined-{b}.json').read_text(encoding='utf-8')) for b in ('planets','T156')}
    # Use exactly the fixed physical subset saved by the summary, with no redraw.
    import csv,math
    radii={}
    with (ROOT/'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            try:
                v=float(r['radius_rsun'])
            except ValueError:
                continue
            if math.isfinite(v) and v>0:
                radii[r['set'],int(r['tic'])]=v
    # Only observable design trials are represented; no new light is read here.
    depths={}
    for c in ('g2','g3'):
        for p in (ROOT/'data/astra/006').glob(f'planet-*-*-*-{c}/results.jsonl'):
            for line in p.read_text(encoding='utf-8').splitlines():
                r=json.loads(line)
                depths[c,r['trial']]=r['depth_ppm']
    results={}
    for name,ch in choices.items():
        floor=ch['floor']; i=ch['index'];base=ch['base'];col=ch['column']
        if floor is None:
            results[name]=dict(ch,status='No ladder floor reaches the choosing-half upside-down target')
            continue
        chosen={}; background=[]; basebg=[]
        for bench in ('planets','T156'):
            rows={}
            for c in ('g2','g3'):
                suffix=f'-floor{floor:g}' if floor!=7 else ''
                d=json.loads((OUT/f'{bench}-{c}-V0{suffix}.json').read_text(encoding='utf-8'))
                rows.update({(c,r['trial']):r for r in d['rows']})
                if bench=='planets':
                    background += [e for e in d['background'] if e['options'][col]]
                    bd=json.loads((OUT/f'baseline-planets-{c}-V0.json').read_text(encoding='utf-8'))
                    basebg += [e for e in bd['background'] if e['options'][col]]
            chosen[bench]=json.loads(json.dumps(original[bench]))
            for r in chosen[bench]:
                for arm in ('real','flip'):
                    r[arm][i]=bool(rows[r['campaign'],r['trial']][arm][col])
        out=dict(ch,status='scored',label='chosen on half the stars, a proposal, not a frozen setting')
        for split in ('held_out_odd','pooled'):
            select=lambda r:split=='pooled' or r['star']%2==1
            planets=[r for r in chosen['planets'] if select(r)]
            possible=[]
            for r in planets:
                rad=radii.get((r['campaign'],r['star']))
                if rad is None or depths[r['campaign'],r['trial']]<=1e6*min(1.,(.2009/rad)**2):
                    possible.append(r)
            reference=[r for r in chosen['T156'] if select(r) and 3000<=r['depth_ppm']<=6000 and 6<=r['duration_h']<=12]
            values={}
            for label,rows in (('all_planets',planets),('possible_planets',possible),('T156_reference',reference)):
                metric=M.metric(rows,np)
                values[label]=dict(n=len(rows),base=metric['rates'][0][base],candidate=metric['rates'][0][i],
                    candidate95=[metric['rate95'][q][0][i] for q in (0,1)],
                    change=metric['change_base'][i],change95=[metric['change_base95'][q][i] for q in (0,1)],
                    control_pass=metric['paired_pass'][i])
            select_event=lambda e:split=='pooled' or e['tic']%2==1
            values['background']={n:{arm:sum(select_event(e) and e['kind']==arm for e in events) for arm in ('real','flip')}
                                  for n,events in (('base',basebg),('candidate',background))}
            out[split]=values
        results[name]=out
    (OUT/'equal-alarm.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('Conditional equal-alarm analysis complete for',len(results),'candidates.')


if __name__=='__main__':
    main()
