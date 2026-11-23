"""Checkpointed two-worker Part A runner. Never launches Part B automatically."""
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT/'data/astra/032'
SCRIPTS = ROOT/'research/astra/scripts'


def write_progress(state, **fields):
    path = OUT/'progress.json'
    previous = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    previous.update(state=state, updated_at=datetime.now(timezone.utc).isoformat(), **fields)
    pending = path.with_suffix('.pending.json')
    pending.write_text(json.dumps(previous, indent=2), encoding='utf-8')
    pending.replace(path)


def main():
    assert sys.flags.isolated and sys.dont_write_bytecode
    print('READ design-only G2 inputs through 032_harness; WRITE', OUT, flush=True)
    for name in ('tracks','tmp','numba-cache','prep'):
        (OUT/name).mkdir(exist_ok=True)
    env = dict(os.environ, NUMBA_NUM_THREADS='2', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
               TMP=str(OUT/'tmp'), TEMP=str(OUT/'tmp'), SS_SET='g2', NUMBA_CACHE_DIR=str(OUT/'numba-cache'))
    started = datetime.now(timezone.utc)
    write_progress('running', phase='measure', started_at=started.isoformat(),
                   expected_finish=(started+timedelta(minutes=90)).isoformat(),
                   estimate_basis='Conservative planning allowance, not a measured duration.', workers=2)
    handles, children = [], []
    try:
        for slot in range(2):
            log = (OUT/f'measure-{slot}.log').open('a', encoding='utf-8')
            handles.append(log)
            children.append(subprocess.Popen([sys.executable,'-I','-B',str(SCRIPTS/'032_eclipse_worker.py'),str(slot),'2','fresh'],
                                             cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT))
        # Wait for both even if one fails. Never leave an unaccounted child running.
        codes = [p.wait() for p in children]
        if any(codes):
            raise RuntimeError(f'Measurement worker exit codes {codes}')
        write_progress('running', phase='summary')
        with (OUT/'summary.log').open('a', encoding='utf-8') as log:
            subprocess.run([sys.executable,'-I','-B',str(SCRIPTS/'032_summary.py')], cwd=ROOT, env=env,
                           stdout=log, stderr=subprocess.STDOUT, check=True)
        result = json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
        write_progress('complete', phase='part_a_complete', rules=result['rules'],
                       part_b='eligible, awaiting implementation' if result['rules']['passed'] else 'not run: Part A failed')
    except Exception as error:
        write_progress('failed', error=str(error))
        raise
    finally:
        for log in handles:
            log.close()


if __name__ == '__main__':
    main()
