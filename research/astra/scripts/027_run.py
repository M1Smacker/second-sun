"""Foreground, resumable orchestration; private logs and terminal checkpoints."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/027'
S = ROOT / 'research/astra/scripts'
PY = r'D:\second-sun\.venv\Scripts\python.exe'


def run(name, args):
    tag = name.removesuffix('.py') + '-' + '-'.join(map(str, args))
    marker = OUT / (tag + '.complete.json')
    if marker.exists():
        return
    with (OUT / (tag + '.log')).open('w', encoding='utf-8') as log:
        result = subprocess.run([PY, '-I', '-B', str(S/name), *map(str, args)], cwd=ROOT,
                                stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(tag + ' failed; private terminal log available')
    marker.write_text(json.dumps(dict(status='complete')), encoding='utf-8')


def main(stage, workers):
    now = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', stage=stage, started=now.isoformat(),
                    expected_finish=(now + timedelta(hours=6)).isoformat(), workers=workers)
    def save():
        (OUT/'progress.json').write_text(json.dumps(progress, indent=2), encoding='utf-8')
    def tasks(name, items):
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(run, name, item) for item in items]
            for future in futures:
                future.result()
    save()
    try:
        if stage == 'baseline':
            tasks('027_score.py', [(c,b,'V0','--baseline') for b in ('planets','T156') for c in ('g2','g3')])
            run('027_baseline_check.py', [])
            tasks('027_generate.py', [(c,0,1,'background','--identity') for c in ('g2','g3')])
        elif stage == 'replay':
            assert (OUT/'027_baseline_check-.complete.json').exists(), 'Baseline completion marker missing'
            assert all((OUT/f'027_generate-{c}-0-1-background---identity.complete.json').exists() for c in ('g2','g3'))
            for phase in ('planets','background','T156'):
                progress['stage'] = phase
                save()
                # One campaign at a time, at most three workers, regardless of other jobs.
                for c in ('g2','g3'):
                    tasks('027_generate.py', [(c,k,workers,phase) for k in range(workers)])
                if phase == 'background':
                    tasks('027_score.py', [(c,'planets','V0') for c in ('g2','g3')])
                elif phase == 'T156':
                    tasks('027_score.py', [(c,'T156','V0') for c in ('g2','g3')])
            run('027_summary.py', [])
        progress.update(status='complete', stage=stage)
    except Exception as e:
        progress.update(status='failed', error=str(e))
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()
    print('Completed stage', stage, flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('stage', choices=('baseline','replay'))
    p.add_argument('--workers', type=int, default=3, choices=(1,2,3))
    a = p.parse_args()
    main(a.stage, a.workers)
