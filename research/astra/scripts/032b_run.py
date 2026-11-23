"""Checkpointed two-worker completion of G3 after affected-set H1 failure."""
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT/'data/astra/032b'
S = ROOT/'research/astra/scripts'


def main():
    assert sys.flags.isolated and sys.dont_write_bytecode
    print('READ only guarded design inputs; WRITE',OUT,flush=True)
    progress = OUT/'progress.json'
    if progress.exists():
        previous = json.loads(progress.read_text(encoding='utf-8'))
        assert previous['status'] == 'failed', 'Refuse overlapping or already-complete run'
    cached = json.loads((OUT/'cached-recount.json').read_text(encoding='utf-8'))
    assert cached['status'] == 'passed'
    assert not cached['sets']['affected']['rules']['H1'], 'This continuation is authorized only for the established H1 failure'
    files = sorted(S.glob('032b_*.py'))+sorted((S/'032b_harness').glob('*.py'))+[S/'032_error_model.py']
    hashes = {p.relative_to(S).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    lock = OUT/'run-source-hashes.json'
    if lock.exists():
        assert json.loads(lock.read_text(encoding='utf-8')) == hashes, 'Changed source since launch'
    else:
        lock.write_text(json.dumps(hashes,indent=2),encoding='utf-8')
    frozen = {p.name:hashlib.sha256((ROOT/'pipeline'/p.name).read_bytes()).hexdigest()
              for p in (S/'032b_harness').glob('*.py')}
    before = OUT/'frozen-before.json'
    if before.exists():
        assert json.loads(before.read_text(encoding='utf-8')) == frozen
    else:
        before.write_text(json.dumps(frozen,indent=2),encoding='utf-8')
    now = datetime.now(timezone(timedelta(hours=3)))
    state = dict(status='running',phase='G3 measurement',pid=os.getpid(),workers=2,
                 started=now.isoformat(),expected_finish=(now+timedelta(hours=2)).isoformat(),
                 estimate='Conservative unmeasured two-hour allowance',
                 part_b='not permitted: affected-set H1 failed, independently recounted within producer session')
    def save():
        state['updated_at'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        pending = progress.with_suffix('.pending.json')
        pending.write_text(json.dumps(state,indent=2),encoding='utf-8'); pending.replace(progress)
    env = dict(os.environ,NUMBA_NUM_THREADS='2',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',
               SS_SET='g3',TMP=str(OUT/'tmp'),TEMP=str(OUT/'tmp'),NUMBA_CACHE_DIR=str(OUT/'numba-cache'))
    def command(name,*args):
        return [sys.executable,'-I','-B',str(S/name),*args]
    save()
    handles, children = [], []
    try:
        for slot in range(2):
            handle = (OUT/f'measure-{slot}.log').open('a',encoding='utf-8'); handles.append(handle)
            children.append(subprocess.Popen(command('032b_worker.py',str(slot),'2'),cwd=ROOT,env=env,
                                             stdout=handle,stderr=subprocess.STDOUT))
        codes = [p.wait() for p in children]
        assert not any(codes), f'Measurement worker exit codes {codes}'
        state['phase'] = 'held-out summary and closed-form recount'; save()
        for name in ('032b_summary.py','032b_recount.py'):
            with (OUT/(name+'.log')).open('a',encoding='utf-8') as stream:
                subprocess.run(command(name),cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,check=True)
        assert hashes == {p.relative_to(S).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        assert frozen == {name:hashlib.sha256((ROOT/'pipeline'/name).read_bytes()).hexdigest() for name in frozen}
        summary = json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
        assert not summary['passed'], 'Previously established affected failure changed'
        state.update(status='complete',phase='Part A complete; FAIL; Part B not run',rules={k:v['rules'] for k,v in summary['sets'].items()},
                     source_identity_at_both_ends=True)
    except Exception as error:
        state.update(status='failed',error=str(error))
        raise
    finally:
        for handle in handles:
            handle.close()
        state['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat(); save()
        print('032b terminal:',state['status'],state['phase'],flush=True)


if __name__ == '__main__':
    main()
