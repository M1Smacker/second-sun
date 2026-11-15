"""Run fresh raw-light experiments and scoring with two worker processes."""
from concurrent.futures import ThreadPoolExecutor
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/024'
SCRIPTS = ROOT / 'research/astra/scripts'
PYTHON = Path(r'D:\second-sun\.venv\Scripts\python.exe')


def main(score_only=False, coverage_only=False, empty_mask=False):
    now = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', started=now.isoformat(),
                    expected_finish=(now + timedelta(minutes=40 if score_only else 120)).isoformat(),
                    completed=[], workers=2, task='024 raw-light subtraction')

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
        generation = [] if score_only else [('024_generate.py', campaign, *(['--empty-mask'] if empty_mask else ['--coverage-only'] if coverage_only else [])) for campaign in ('g2', 'g3')]
        if score_only:
            for campaign in ('g2', 'g3'):
                counts = json.loads((OUT / f'generated-{campaign}/counts.json').read_text(encoding='utf-8'))
                assert counts['campaign'] == campaign and counts['counts']['generated_groups'] > 0
        stages = [generation]
        if not (score_only or coverage_only or empty_mask):
            stages.extend([
                [('024_coverage_audit.py',)],
                [('024_generate.py', campaign, '--coverage-only') for campaign in ('g2', 'g3')],
                [('024_generate.py', campaign, '--empty-mask') for campaign in ('g2', 'g3')],
            ])
        stages.append([('024_score.py', campaign, bench, 'V0', *extra)
             for extra in (('--baseline',), ()) for bench in ('planets', 'T156')
             for campaign in ('g2', 'g3')])
        for tasks in stages:
            with ThreadPoolExecutor(max_workers=2) as pool:
                for name in pool.map(run, tasks):
                    progress['completed'].append(name)
                    save()
        run(('024_summary.py',))
        run(('024_strata.py',))
        run(('024_verify.py',))
        progress['status'] = 'complete'
    except Exception as error:
        progress.update(status='failed', error=str(error))
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--score-only', action='store_true')
    parser.add_argument('--coverage-only', action='store_true')
    parser.add_argument('--empty-mask', action='store_true')
    args = parser.parse_args()
    main(args.score_only, args.coverage_only, args.empty_mask)
