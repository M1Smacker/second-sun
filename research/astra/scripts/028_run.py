"""Resumable three-worker batch, periodic heartbeat, private logs and checkpoints."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timedelta,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import threading

ROOT=Path(r'D:\second-sun-astra'); S=ROOT/'research/astra/scripts'; OUT=ROOT/'data/astra/028'
PY=r'D:\second-sun\.venv\Scripts\python.exe'


def run(name,args=()):
    tag=name.removesuffix('.py')+'-'+'-'.join(map(str,args))
    marker=OUT/(tag+'.complete.json')
    if marker.exists(): return
    with (OUT/(tag+'.log')).open('w',encoding='utf-8') as log:
        result=subprocess.run([PY,'-I','-B',str(S/name),*map(str,args)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    if result.returncode: raise RuntimeError(tag+' failed; see private log')
    marker.write_text(json.dumps(dict(status='complete')),encoding='utf-8')


def main(stage):
    assert json.loads((OUT/'preflight.json').read_text(encoding='utf-8'))['passed'], 'Real-light preflight required'
    now=datetime.now(timezone(timedelta(hours=3)))
    progress=dict(status='running',stage=stage,started=now.isoformat(),expected_finish=(now+timedelta(hours=6)).isoformat(),workers=3)
    def save():
        p=OUT/'progress.pending.json'; p.write_text(json.dumps(progress,indent=2),encoding='utf-8'); p.replace(OUT/'progress.json')
    fingerprint={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in S.glob('028*.py')}
    lock=OUT/'run-source-hashes.json'
    if lock.exists(): assert json.loads(lock.read_text(encoding='utf-8'))==fingerprint,'Source changed since run; do not reuse stale checkpoints'
    else: lock.write_text(json.dumps(fingerprint,indent=2),encoding='utf-8')
    stop=threading.Event()
    def heartbeat():
        while not stop.wait(300):
            print('028 alive, stage',progress['stage'],flush=True)
    thread=threading.Thread(target=heartbeat,daemon=True); thread.start(); save()
    def tasks(name,items):
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures=[pool.submit(run,name,item) for item in items]
            for f in futures: f.result()
    try:
        run('028_checks.py'); run('028_inventory.py')
        tasks('028_generate.py',[(c,0,1,'background','--identity') for c in ('g2','g3')])
        for phase in ('background','planets','T156'):
            progress['stage']=phase; save()
            for c in ('g2','g3'): tasks('028_generate.py',[(c,k,3,phase) for k in range(3)])
            if phase=='background':
                progress['stage']='null calibration'; save()
                tasks('028_score.py',[(c,'null') for c in ('g2','g3')]); run('028_calibrate.py')
                if stage=='null': break
            else: tasks('028_score.py',[(c,phase) for c in ('g2','g3')])
        if stage=='all':
            progress['stage']='summary and verification'; save()
            run('028_summary.py'); run('028_verify.py'); run('028_report.py')
            fresh=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))['fresh_required']
            progress['status']='needs_fresh_seed' if fresh else 'complete'
            if not json.loads((OUT/'calibration.json').read_text(encoding='utf-8'))['mutation_sensitive']:
                progress['status']='needs_null_mutation_review'
        else: progress['status']='null_complete'
    except Exception as e:
        progress.update(status='failed',error=str(e)); raise
    finally:
        stop.set(); progress['finished']=datetime.now(timezone(timedelta(hours=3))).isoformat(); save()
    print('028 terminal',progress['status'],flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('stage',choices=('null','all')); main(p.parse_args().stage)
