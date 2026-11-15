"""Run the matrix without interactive polling, with at most two scoring workers."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/023'
SCRIPTS = ROOT / 'research/astra/scripts'
PYTHON = Path(r'D:\second-sun\.venv\Scripts\python.exe')


def main():
    started = datetime.now(timezone(timedelta(hours=3)))
    expected = started + timedelta(minutes=60)
    progress = dict(status='running', started=started.isoformat(), expected_finish=expected.isoformat(),
                    completed=[], workers=2, task='023 candidate matrix')

    def save():
        temporary = OUT / 'progress.pending.json'
        temporary.write_text(json.dumps(progress, indent=2), encoding='utf-8')
        temporary.replace(OUT / 'progress.json')

    def run(task):
        script, *arguments = task
        name = '-'.join(arguments) or script
        with (OUT / f'run-{name}.log').open('w', encoding='utf-8') as log:
            result = subprocess.run([str(PYTHON), '-I', '-B', str(SCRIPTS / script), *arguments],
                                    cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f'Worker failed: {name}, exit {result.returncode}')
        return name

    save()
    try:
        run(('023_checks.py',))
        # Complete baseline identity in both campaigns before running mask variants.
        for modes in (('V0',), ('V1', 'V2')):
            tasks = [('023_score.py', campaign, bench, mode)
                     for mode in modes for bench in ('planets', 'T156') for campaign in ('g2', 'g3')]
            with ThreadPoolExecutor(max_workers=2) as pool:
                for name in pool.map(run, tasks):
                    progress['completed'].append(name)
                    save()
        run(('023_summary.py',))
        run(('023_cap_diagnostic.py',))
        run(('023_verify.py',))
        progress['status'] = 'complete'
    except Exception as error:
        progress.update(status='failed', error=str(error))
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()


if __name__ == '__main__':
    main()
