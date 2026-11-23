"""Recover reviewed 014 code read-only, redirect its writes, freeze fresh controls."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/032'
SCRIPTS = ROOT / 'research/astra/scripts'
REF = 'astra/014-dumps-ephemerides'


def source(path):
    return subprocess.check_output(['git', 'show', f'{REF}:{path}'], cwd=ROOT).replace(b'\r\n', b'\n')


def main():
    OUT.mkdir(exist_ok=True)
    copies = SCRIPTS / '032_harness'
    copies.mkdir(exist_ok=True)
    prefix = 'research/astra/scripts/harness/sprint014/'
    provenance = json.loads(source(prefix + 'provenance.json'))
    for name, row in provenance.items():
        old = source(prefix + name)
        assert hashlib.sha256(old).hexdigest() == row['copy_sha256_lf']
        new = old.replace(b'"014"', b'"032"').replace(b'/ "014"', b'/ "032"')
        destination = copies / name
        if destination.exists():
            assert destination.read_bytes() == new, 'Existing harness differs; refusing overwrite'
        else:
            destination.write_bytes(new)
        row['source014_sha256_lf'] = row['copy_sha256_lf']
        row['copy_sha256_lf'] = hashlib.sha256(new).hexdigest()
    (OUT / 'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    for name in ('harness', 'outputs', 'eclipse_fit', 'eclipse_select', 'eclipse_calibrate', 'eclipse_worker'):
        old = source(f'research/astra/scripts/014_{name}.py').decode('utf-8')
        new = old.replace('014_', '032_').replace('"014"', '"032"').replace('astra/014', 'astra/032')
        new = new.replace('Path(__file__).resolve().with_name("harness") / "sprint014"',
                          'Path(__file__).resolve().with_name("032_harness")')
        new = new.replace('(COPIES / "provenance.json")', '(OUT / "provenance.json")')
        # Preserve extraction copies as the reference implementations; new orchestration is separate.
        destination = SCRIPTS / f'032_{name}.py'
        if not destination.exists():
            destination.write_text(new, encoding='utf-8', newline='\n')
    print('Recovered six 014 scripts and twelve harness modules; all output paths redirected to 032.')


if __name__ == '__main__':
    main()
