"""Recover read-only historical harness sources and redirect their output roots."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(r'D:\second-sun-astra')
SCRIPTS = ROOT / 'research/astra/scripts'
OUT = ROOT / 'data/astra/023'
BRANCH = 'astra/014-dumps-ephemerides'


def historical(path, branch=BRANCH):
    return subprocess.check_output(['git', 'show', f'{branch}:{path}'], cwd=ROOT)


def main():
    OUT.mkdir(exist_ok=True)
    reference = OUT / 'source-reference'
    reference.mkdir(exist_ok=True)
    copies = SCRIPTS / 'harness/sprint023'
    copies.mkdir(exist_ok=True)
    prefix = 'research/astra/scripts/harness/sprint014/'
    provenance = json.loads(historical(prefix + 'provenance.json'))
    for name, record in provenance.items():
        content = historical(prefix + name).replace(b'\r\n', b'\n')
        assert hashlib.sha256(content).hexdigest() == record['copy_sha256_lf']
        content = content.replace(b'sprint014', b'sprint023').replace(b'astra/014', b'astra/023')
        content = content.replace(b'"014"', b'"023"').replace(b'"014/', b'"023/')
        record['copy_sha256_lf'] = hashlib.sha256(content).hexdigest()
        (copies / name).write_bytes(content)
    (copies / 'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    for suffix in ('harness', 'inputs', 'outputs', 'scoring_rules'):
        content = historical(f'research/astra/scripts/014_{suffix}.py')
        content = content.replace(b'014', b'023')
        (SCRIPTS / f'023_{suffix}.py').write_bytes(content)
    for branch, names in (
        ('astra/013-known-events-ds', ('013_score.py', '013_summary.py')),
        ('astra/011-mask-timing-oae', ('011_score.py', '011_events.py')),
        (BRANCH, ('014_dump_summary.py', '014_dumps.py', '014_deep_summary.py')),
    ):
        for name in names:
            (reference / name).write_bytes(historical('research/astra/scripts/' + name, branch))
    print('Recovered 12 redirected harness modules and four helpers. Historical reference code is private.')


if __name__ == '__main__':
    main()
