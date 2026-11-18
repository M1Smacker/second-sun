"""Foreground three-worker bench with terminal checkpoints and locked source."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/030'
S = ROOT / 'research/astra/scripts'
PY = r'D:\second-sun\.venv\Scripts\python.exe'


def run(name, args=()):
    tag = name.removesuffix('.py') + '-' + '-'.join(map(str, args))
    marker = OUT / (tag + '.complete.json')
    if marker.exists():
        assert json.loads(marker.read_text(encoding='utf-8'))['status'] == 'complete'
        return
    with (OUT / (tag + '.log')).open('w', encoding='utf-8') as log:
        process = subprocess.run([PY, '-I', '-B', str(S/name), *map(str, args)], cwd=ROOT,
                                 stdout=log, stderr=subprocess.STDOUT)
    if process.returncode:
        raise RuntimeError(tag + ' failed; terminal private log available')
    marker.write_text(json.dumps(dict(status='complete')), encoding='utf-8')


def main():
    baseline = json.loads((OUT / 'progress.json').read_text(encoding='utf-8'))
    assert baseline['status'] in ('baseline_complete', 'failed', 'complete', 'running'), 'Unknown checkpoint'
    # A resume is allowed only after this run owns the progress file. No overlapping launches.
    if baseline['status'] == 'running':
        raise RuntimeError('A foreground job is marked running; do not launch a second copy')
    assert (OUT / 'baseline-check.json').is_file(), 'B reproduction must finish first'
    fingerprint = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in S.glob('030*.py')}
    lock = OUT / 'run-source-hashes.json'
    if lock.exists():
        assert json.loads(lock.read_text(encoding='utf-8')) == fingerprint, 'Source changed since checkpoint; STOP'
    else:
        lock.write_text(json.dumps(fingerprint, indent=2), encoding='utf-8')
    provenance = json.loads((OUT / 'source/provenance.json').read_text(encoding='utf-8'))
    frozen = {name: hashlib.sha256((ROOT/'pipeline'/name).read_bytes()).hexdigest() for name in provenance}
    before = OUT / 'frozen-before.json'
    if before.exists():
        assert json.loads(before.read_text(encoding='utf-8')) == frozen
    else:
        before.write_text(json.dumps(frozen, indent=2), encoding='utf-8')
    now = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', stage='preflight', started=now.isoformat(), workers=3,
                    expected_finish=(now + timedelta(hours=16)).isoformat(),
                    estimate='Conservative unmeasured estimate; three full injection populations with five-day detrending')
    def save():
        pending = OUT / 'progress.pending.json'
        pending.write_text(json.dumps(progress, indent=2), encoding='utf-8')
        pending.replace(OUT / 'progress.json')
    def tasks(name, args):
        with ThreadPoolExecutor(max_workers=3) as pool:
            jobs = [pool.submit(run, name, item) for item in args]
            for job in jobs:
                job.result()
    save()
    try:
        run('030_recount.py')
        run('030_checks.py')
        run('030_layout.py')
        tasks('030_generate.py', [(c, 0, 1, 'background', '--identity') for c in ('g2', 'g3')])
        # Failure here is a mandatory stop, before N1 sees any real light.
        for c in ('g2', 'g3'):
            identity = json.loads((OUT / f'generated-{c}/progress-background-0-identity.json').read_text(encoding='utf-8'))
            assert identity['status'] == 'complete' and identity['done'] == 25
        progress['stage'] = 'untouched N1 background'; save()
        for c in ('g2', 'g3'):
            tasks('030_generate.py', [(c, slot, 3, 'background') for slot in range(3)])
        progress['stage'] = 'six threshold alarm curves'; save()
        tasks('030_n1_score.py', [(c, 'planets', 'V0', '--floor', floor, '--background-only')
                                for floor in (4.5, 5, 5.5, 6, 6.5, 7) for c in ('g2', 'g3')])
        run('030_choose.py')
        choice = json.loads((OUT / 'chosen.json').read_text(encoding='utf-8'))
        if choice['threshold'] is None:
            progress.update(status='no_eligible_threshold', stage='selection stopped by written rule')
            return
        run('030_known.py')
        floor = choice['threshold']
        for phase in ('planets', 'fresh', 'T156'):
            progress['stage'] = phase; save()
            for c in ('g2', 'g3'):
                tasks('030_generate.py', [(c, slot, 3, phase) for slot in range(3)])
            args = [(c, 'T156' if phase == 'T156' else 'planets', 'V0', '--floor', floor,
                     *(('--fresh',) if phase == 'fresh' else ())) for c in ('g2', 'g3')]
            tasks('030_n1_score.py', args)
        progress['stage'] = 'paired bootstrap and verification'; save()
        run('030_summary.py')
        run('030_verify.py')
        progress.update(status='complete', stage='bench complete, report needs human-readable synthesis')
    except Exception as error:
        progress.update(status='failed', error=str(error))
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()
        print('030 terminal status:', progress['status'], flush=True)


if __name__ == '__main__':
    main()
