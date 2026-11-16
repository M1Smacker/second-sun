"""Prepare guarded, redirected copies; only git show, never git writes."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(r'D:\second-sun-astra')
SCRIPTS = ROOT / 'research/astra/scripts'
OUT = ROOT / 'data/astra/026'


def main():
    copies = OUT / 'copies'
    copies.mkdir(exist_ok=True)
    provenance = {}
    for path in (SCRIPTS / 'harness/sprint023').glob('*.py'):
        original = path.read_bytes().replace(b'\r\n', b'\n')
        content = original.replace(b'sprint023', b'sprint026').replace(b'astra/023', b'astra/026')
        content = content.replace(b'"023"', b'"026"').replace(b"'023'", b"'026'")
        (copies / path.name).write_bytes(content)
        provenance[path.name] = dict(source_sha256_lf=hashlib.sha256(original).hexdigest(),
                                     copy_sha256_lf=hashlib.sha256(content).hexdigest())
    (copies / 'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    for name in ('harness', 'inputs', 'outputs'):
        content = (SCRIPTS / f'023_{name}.py').read_text(encoding='utf-8').replace('023', '026')
        if name == 'harness':
            content = content.replace('Path(__file__).resolve().with_name("harness") / "sprint026"', 'OUT / "copies"')
        (SCRIPTS / f'026_{name}.py').write_text(content, encoding='utf-8')
    trace = subprocess.check_output(['git', 'show', 'astra/026-fix101-mask-drift:research/astra/scripts/026_trace.py'], cwd=ROOT)
    (SCRIPTS / '026_trace.py').write_bytes(trace)
    for name in ('010_generate.py', '010_diagnose.py'):
        content = subprocess.check_output(['git', 'show', 'astra/010-mask-timing:research/astra/scripts/' + name], cwd=ROOT)
        (OUT / name).write_bytes(content)
    print('Prepared 12 redirected source copies, guard and historical references.')


if __name__ == '__main__':
    main()
