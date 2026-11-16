"""Prepare redirected bench copies with all machine writes confined to brief 025."""
import hashlib
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
SCRIPTS = ROOT / 'research/astra/scripts'
OUT = ROOT / 'data/astra/025'


def main():
    destination = SCRIPTS / 'harness/sprint025'
    destination.mkdir(exist_ok=True)
    provenance = {}
    for path in (SCRIPTS / 'harness/sprint024').glob('*.py'):
        original = path.read_bytes().replace(b'\r\n', b'\n')
        copied = original.replace(b'sprint024', b'sprint025')
        copied = copied.replace(b'astra/024', b'astra/025')
        copied = copied.replace(b'"024"', b'"025"').replace(b"'024'", b"'025'")
        (destination / path.name).write_bytes(copied)
        provenance[path.name] = dict(source_sha256_lf=hashlib.sha256(original).hexdigest(),
                                     copy_sha256_lf=hashlib.sha256(copied).hexdigest())
    (destination / 'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    for filename in ('harness', 'inputs'):
        content = (SCRIPTS / f'024_{filename}.py').read_text(encoding='utf-8')
        content = content.replace('sprint024', 'sprint025').replace('astra/024', 'astra/025')
        content = content.replace('"024"', '"025"').replace("'024'", "'025'")
        content = content.replace('024_harness', '025_harness')
        (SCRIPTS / f'025_{filename}.py').write_text(content, encoding='utf-8')
    print('Prepared twelve redirected bench modules and the read/write guard.')


if __name__ == '__main__':
    main()
