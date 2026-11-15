"""Two-worker background supervisor with terminal progress and fixed bench stages."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/025'
SCRIPTS = ROOT / 'research/astra/scripts'
PYTHON = Path(r'D:\second-sun\.venv\Scripts\python.exe')


def main():
    now = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', started=now.isoformat(),
                    expected_finish=(now + timedelta(hours=3)).isoformat(),
                    workers=2, completed=[], task='025 bit-4096 candidate')

    def save():
        pending = OUT / 'progress.pending.json'
        pending.write_text(json.dumps(progress, indent=2), encoding='utf-8')
        pending.replace(OUT / 'progress.json')

    def run(task):
        script, *arguments = task
        name = '-'.join((script.removesuffix('.py'), *arguments))
        with (OUT / f'{name}.log').open('w', encoding='utf-8') as log:
            result = subprocess.run([str(PYTHON), '-I', '-B', str(SCRIPTS / script), *arguments],
                                    cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f'Worker failed {name}, exit {result.returncode}')
        return name

    save()
    try:
        stages = [
            [('025_checks.py', c) for c in ('g2', 'g3')],
            [('025_generate.py', c) for c in ('g2', 'g3')],
            [('025_score.py', c, bench, 'V0', *extra) for extra in (('--baseline',), ())
             for bench in ('planets', 'T156') for c in ('g2', 'g3')],
            [('025_summary.py',)],
            [('025_verify.py',)],
        ]
        for tasks in stages:
            with ThreadPoolExecutor(max_workers=2) as pool:
                for name in pool.map(run, tasks):
                    progress['completed'].append(name)
                    save()
        progress['status'] = 'complete'
    except Exception as error:
        progress.update(status='failed', error=str(error))
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()


if __name__ == '__main__':
    main()
