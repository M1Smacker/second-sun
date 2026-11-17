"""Prepare private redirected source copies. No git operation or pipeline import."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
S = ROOT / 'research/astra/scripts'
OUT = ROOT / 'data/astra/028'


def main():
    assert OUT.resolve() == (ROOT/'data').resolve()/'astra/028'
    OUT.mkdir(exist_ok=True)
    copies = OUT/'source'
    copies.mkdir(exist_ok=True)
    provenance = {}
    for p in (S/'harness/sprint027').glob('*.py'):
        original = p.read_bytes().replace(b'\r\n', b'\n')
        content = original.replace(b'astra/027', b'astra/028').replace(b'"027"', b'"028"').replace(b"'027'", b"'028'")
        ast.parse(content)
        (copies/p.name).write_bytes(content)
        provenance[p.name] = dict(source_sha256_lf=hashlib.sha256(original).hexdigest(),
                                 copy_sha256_lf=hashlib.sha256(content).hexdigest())
    assert len(provenance) == 12
    (copies/'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    for name in ('harness', 'inputs', 'outputs'):
        content = (S/f'027_{name}.py').read_text(encoding='utf-8').replace('027', '028')
        if name == 'harness':
            content = content.replace('Path(__file__).resolve().with_name("harness") / "sprint028"', 'OUT / "source"')
        (S/f'028_{name}.py').write_text(content, encoding='utf-8')
    print('Prepared 12 private redirected modules and guard, writes data/astra/028.')


if __name__ == '__main__':
    main()
