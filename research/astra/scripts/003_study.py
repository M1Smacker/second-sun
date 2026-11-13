"""Run fixed 1- and 3-day variants on original pre-detection losses; reuse 2-day results."""
import argparse
import json
from pathlib import Path
import subprocess
import time
from datetime import datetime,timezone
ROOT=Path(r'D:\second-sun-astra'); OUT=ROOT/'data/astra/003'; PYTHON=r'D:\second-sun\.venv\Scripts\python.exe'
def main(args):
    assert not (OUT/'STOP.json').exists(), 'Stop sign must be resolved before more work'
    base=[]
    for p in (OUT/'workers').glob('*/results-*.jsonl'):
        base.extend(json.loads(x) for x in p.read_text(encoding='utf-8').splitlines())
    assert len(base)==2000 and len({r['trial'] for r in base})==2000
    # Mask failures are not in scope. Absent windows/gaps are retained and explicitly unrepaired.
    selected=[r['trial'] for r in base if not r['dip']['recovered'] and r['dip']['stage']==3]
    payload=dict(trials=sorted(selected),window_gap_unrepaired=sum(not r['dip']['recovered'] and r['dip']['stage']<2 for r in base))
    path=OUT/'study-selection.json'
    if path.exists(): assert json.loads(path.read_text(encoding='utf-8'))==payload
    else: path.write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps(dict(selected_pairs=len(selected),window_gap_unrepaired=payload['window_gap_unrepaired'])),flush=True)
    # Run each window in sequence, no more than four worker processes total.
    for window in (1,3):
        processes=[]; streams=[]
        for campaign,slots in [('g2',args.g2),('g3',args.g3)]:
            for slot in range(slots):
                name=f'study-w{window}-{campaign}-{slot}'
                stdout=(OUT/f'{name}.log').open('w',encoding='utf-8'); stderr=(OUT/f'{name}-error.log').open('w',encoding='utf-8'); streams += [stdout,stderr]
                command=[PYTHON,'-I','-B',str(ROOT/'research/astra/scripts/003_worker.py'),'--campaign',campaign,'--slot',str(slot),'--slots',str(slots),
                    '--start','0','--limit','2000','--study-window',str(window)]
                processes.append(subprocess.Popen(command,cwd=ROOT,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW))
        while any(p.poll() is None for p in processes):
            statuses=[]
            for p in (OUT/f'study-w{window}').glob('*/progress.json'):
                try: statuses.append(json.loads(p.read_text(encoding='utf-8')))
                except json.JSONDecodeError: pass
            (OUT/'progress.json').write_text(json.dumps(dict(phase=f'multiwindow-{window}d',status='running',trials_done=sum(x['trials_done'] for x in statuses),
                trials_planned=len(selected),last_update_utc=datetime.now(timezone.utc).isoformat()),indent=2),encoding='utf-8')
            time.sleep(15)
        for s in streams:s.close()
        assert not (OUT/'STOP.json').exists() and all(p.returncode==0 for p in processes), 'Study worker stopped'
    variants={}
    for window in (1,3):
        rows=[]
        for p in (OUT/f'study-w{window}').glob('*/results-*.jsonl'): rows.extend(json.loads(x) for x in p.read_text(encoding='utf-8').splitlines())
        assert len(rows)==len(selected) and {r['trial'] for r in rows}==set(selected)
        variants[window]={r['trial']:r for r in rows}
    groups=[]
    for k in range(5):
        chosen=[r for r in base if r['trial'] in selected and r['bin']==k]
        groups.append(dict(bin=k,n=len(chosen),dip_gained=sum(any(variants[w][r['trial']]['dip']['recovered'] for w in (1,3)) for r in chosen),
            bump_baseline=sum(r['bump']['recovered'] for r in chosen),
            bump_union=sum(r['bump']['recovered'] or any(variants[w][r['trial']]['bump']['recovered'] for w in (1,3)) for r in chosen)))
    result=dict(selected_pairs=len(selected),unrepaired_window_gap=payload['window_gap_unrepaired'],bins=groups,
        interpretation='Union of separately vetted routes, not candidate merging before vetting; selected-failure design study only')
    (OUT/'study-summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps(result,indent=2))
    (OUT/'progress.json').write_text(json.dumps(dict(phase='multiwindow',status='complete',trials_done=len(selected),trials_planned=len(selected),
        last_update_utc=datetime.now(timezone.utc).isoformat()),indent=2),encoding='utf-8')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--g2',type=int,default=3);p.add_argument('--g3',type=int,default=1)
    args=p.parse_args();assert args.g2+args.g3<=4;main(args)
