"""Foreground reproduction gate, at most three scoring workers."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/030'
S = ROOT / 'research/astra/scripts'
PY = r'D:\second-sun\.venv\Scripts\python.exe'


def run(args):
    tag = '-'.join(args).replace('.py', '')
    with (OUT / (tag + '.log')).open('w', encoding='utf-8') as log:
        result = subprocess.run([PY, '-I', '-B', str(S / args[0]), *args[1:]],
                                cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(tag + ' failed; inspect terminal private log')


def main():
    now = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', stage='B reproduction', started=now.isoformat(),
                    expected_finish=(now + timedelta(minutes=30)).isoformat(), workers=3)
    path = OUT / 'progress.json'
    path.write_text(json.dumps(progress, indent=2), encoding='utf-8')
    try:
        with ThreadPoolExecutor(max_workers=3) as pool:
            jobs = [pool.submit(run, ['030_score.py', c, b, 'V0', '--baseline'])
                    for b in ('planets', 'T156') for c in ('g2', 'g3')]
            for job in jobs:
                job.result()
        run(['030_baseline_check.py'])
        progress['status'] = 'baseline_complete'
    except Exception as error:
        progress.update(status='failed', error=str(error))
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        path.write_text(json.dumps(progress, indent=2), encoding='utf-8')
    print('B reproduction terminal:', progress['status'], flush=True)


if __name__ == '__main__':
    main()
