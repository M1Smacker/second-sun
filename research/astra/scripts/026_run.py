"""Run the prepared M4 bench with three workers, logs and terminal progress."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/026'
SCRIPTS = ROOT / 'research/astra/scripts'
PYTHON = Path(r'D:\second-sun\.venv\Scripts\python.exe')


def run(name, args=()):
    label = name.removesuffix('.py') + ('-' + '-'.join(map(str, args)) if args else '')
    with (OUT / f'{label}.log').open('w', encoding='utf-8') as log:
        result = subprocess.run([str(PYTHON), '-I', '-B', str(SCRIPTS / name), *map(str, args)],
                                cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'{label} failed; inspect its private log after terminal status')


def main():
    now = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', started=now.isoformat(),
                    expected_finish=(now + timedelta(hours=2)).isoformat(), workers=3)
    def save():
        (OUT / 'progress-m4.json').write_text(json.dumps(progress, indent=2), encoding='utf-8')
    save()
    try:
        run('026_inventory.py')
        assert (OUT / 'synthetic-controls.json').is_file(), 'Run cheap controls before full bench'
        run('026_score_prepare.py')
        for campaign in ('g2', 'g3'):
            progress['stage'] = f'generate-{campaign}'
            save()
            with ThreadPoolExecutor(max_workers=3) as pool:
                futures = [pool.submit(run, '026_generate.py', (campaign, slot, 3)) for slot in range(3)]
                for future in futures:
                    future.result()
        progress['stage'] = 'score'
        save()
        tasks = [(c, b, m) for c in ('g2', 'g3') for b in ('planets', 'T156') for m in ('V0', 'V2', 'V4')]
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(run, '026_score.py', task) for task in tasks]
            for future in futures:
                future.result()
        progress['stage'] = 'summarize'
        save()
        run('026_summary.py')
        progress.update(status='complete', stage='complete')
    except Exception as error:
        progress.update(status='failed', error=str(error))
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()
    print('M4 machine bench complete; scientific acceptance and producer verification pending.')


if __name__ == '__main__':
    main()
