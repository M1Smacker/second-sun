"""Resumable three-worker D1 bench; identities gate every new scoring phase."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT=Path(r'D:\second-sun-astra')
OUT=ROOT/'data/astra/031'
S=ROOT/'research/astra/scripts'
PY=r'D:\second-sun\.venv\Scripts\python.exe'


def run(name,args=()):
    args=list(map(str,args))
    tag=name.removesuffix('.py')+'-'+'-'.join(args)
    marker=OUT/(tag+'.complete.json')
    if marker.exists():
        assert json.loads(marker.read_text(encoding='utf-8'))['status']=='complete'
        return
    with (OUT/(tag+'.log')).open('w',encoding='utf-8') as stream:
        process=subprocess.run([PY,'-I','-B',str(S/name),*args],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,
                               env=dict(os.environ,NUMBA_NUM_THREADS='2'))
    if process.returncode:
        raise RuntimeError(tag+' failed; private terminal log available')
    marker.write_text(json.dumps(dict(status='complete')),encoding='utf-8')


def main():
    now=datetime.now(timezone(timedelta(hours=3)))
    progress=OUT/'progress.json'
    if progress.exists():
        previous=json.loads(progress.read_text(encoding='utf-8'))
        assert previous['status'] in ('failed','complete'), 'Existing supervisor marked running; refuse overlap'
        if previous['status']=='complete':
            print('Bench already complete; do not rerun.')
            return
    fingerprint={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in S.glob('031*.py')}
    locked=OUT/'run-source-hashes.json'
    if locked.exists():
        assert json.loads(locked.read_text(encoding='utf-8'))==fingerprint, 'Source changed since launch; review required before resuming'
    else:
        locked.write_text(json.dumps(fingerprint,indent=2),encoding='utf-8')
    provenance=json.loads((OUT/'source/provenance.json').read_text(encoding='utf-8'))
    frozen={name:hashlib.sha256((ROOT/'pipeline'/name).read_bytes()).hexdigest() for name in provenance}
    before=OUT/'frozen-before.json'
    if before.exists():
        assert json.loads(before.read_text(encoding='utf-8'))==frozen
    else:
        before.write_text(json.dumps(frozen,indent=2),encoding='utf-8')
    state=dict(status='running',stage='waiting for mandatory endpoint identities',pid=os.getpid(),
               started=now.isoformat(),expected_finish=(now+timedelta(hours=24)).isoformat(),workers=3,
               estimate='Conservative unmeasured 24-hour allowance for old D1 and three new-bench detectors')
    def save():
        pending=progress.with_suffix('.pending.json')
        pending.write_text(json.dumps(state,indent=2),encoding='utf-8')
        pending.replace(progress)
    def tasks(name,args):
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures=[pool.submit(run,name,a) for a in args]
            for f in futures:
                f.result()
    save()
    try:
        # This supervisor waits without any model progress polling or log reads.
        deadline=time.monotonic()+3600
        while True:
            identity=json.loads((OUT/'identity-progress.json').read_text(encoding='utf-8'))
            if identity['status']!='running':
                assert identity['status']=='complete', 'Mandatory identity failed; stop before new scoring'
                break
            assert time.monotonic()<deadline, 'Identity wait exceeded one hour; no new scoring'
            time.sleep(60)
        assert json.loads((OUT/'identity-checks.json').read_text(encoding='utf-8'))['status']=='passed'
        run('031_checks.py')
        run('031_retier_checks.py')
        run('031_t109.py',['--baseline-only'])
        state['stage']='fixed draw observability and historical replay validation';save()
        tasks('031_records.py',[(c,) for c in ('g2','g3')])
        run('031_layout.py')
        # Verify the adapted scorer itself on old B/N1 before any D1 score.
        tasks('031_mixed_score.py',[(c,p,v) for c in ('g2','g3') for p in ('choosing','fresh_old','T156_old') for v in ('B','N1')])
        run('031_verify.py',['--old-only'])
        state['stage']='untouched D1 raw-light background';save()
        for c in ('g2','g3'):
            tasks('031_generate.py',[(c,slot,3,'background','D1') for slot in range(3)])
        run('031_t109.py')
        for phase in ('choosing','fresh_old','T156_old','fresh_new','T156_new'):
            state['stage']=phase+' raw paired replay and tier scoring';save()
            versions=('D1',) if phase in ('choosing','fresh_old','T156_old') else ('B','N1','D1')
            for version in versions:
                for c in ('g2','g3'):
                    tasks('031_generate.py',[(c,slot,3,phase,version) for slot in range(3)])
                tasks('031_mixed_score.py',[(c,phase,version) for c in ('g2','g3')])
        state['stage']='paired whole-star summary and terminal verification';save()
        run('031_summary.py')
        run('031_verify.py')
        run('031_report.py')
        state.update(status='complete',stage='bench verified; report synthesis ready')
    except Exception as error:
        state.update(status='failed',error=str(error))
        # Counts-only terminal checkpoint for the next session, never claim a verdict.
        with (ROOT/'research/astra/reports/031-report.md').open('a',encoding='utf-8') as report:
            report.write('\n## Automatic terminal checkpoint\n\nPARTIAL: supervisor stopped in '+state['stage']+'. '+str(error)+'. No settings changed. See private progress.json and the named terminal log before any resume.\n')
        raise
    finally:
        state['finished']=datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()
        print('031 terminal status:',state['status'],flush=True)


if __name__=='__main__':
    main()
