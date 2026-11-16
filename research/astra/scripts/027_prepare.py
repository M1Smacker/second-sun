"""Prepare redirected bench copies, without importing the production pipeline."""
import hashlib
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
S = ROOT / 'research/astra/scripts'
OUT = ROOT / 'data/astra/027'


def main():
    OUT.mkdir(exist_ok=True)
    copies = S / 'harness/sprint027'
    copies.mkdir(exist_ok=True)
    provenance = {}
    for p in (S / 'harness/sprint023').glob('*.py'):
        original = p.read_bytes().replace(b'\r\n', b'\n')
        content = original.replace(b'sprint023', b'sprint027').replace(b'astra/023', b'astra/027')
        content = content.replace(b'"023"', b'"027"').replace(b"'023'", b"'027'")
        (copies / p.name).write_bytes(content)
        provenance[p.name] = dict(source_sha256_lf=hashlib.sha256(original).hexdigest(),
                                  copy_sha256_lf=hashlib.sha256(content).hexdigest())
    assert len(provenance) == 12
    (copies / 'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    for name in ('harness', 'inputs', 'outputs'):
        source = (S / f'023_{name}.py').read_text(encoding='utf-8').replace('023', '027')
        (S / f'027_{name}.py').write_text(source, encoding='utf-8')
    print('Prepared 12 redirected source copies and access guard; data output data/astra/027.')


if __name__ == '__main__':
    main()
