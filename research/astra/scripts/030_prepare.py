"""Create private bench copies and guarded baseline scorer. Never import production."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
S = ROOT / 'research/astra/scripts'
OUT = ROOT / 'data/astra/030'


def main():
    assert OUT.resolve() == (ROOT / 'data').resolve() / 'astra/030'
    OUT.mkdir(exist_ok=True)
    copies = OUT / 'source'
    copies.mkdir(exist_ok=True)
    provenance = {}
    for p in (S / 'harness/sprint027').glob('*.py'):
        original = p.read_bytes().replace(b'\r\n', b'\n')
        content = original.replace(b'astra/027', b'astra/030').replace(b'"027"', b'"030"').replace(b"'027'", b"'030'")
        ast.parse(content)
        (copies / p.name).write_bytes(content)
        provenance[p.name] = dict(source_sha256_lf=hashlib.sha256(original).hexdigest(),
                                 copy_sha256_lf=hashlib.sha256(content).hexdigest())
    assert len(provenance) == 12
    (copies / 'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    for name in ('harness', 'inputs', 'outputs', 'score', 'baseline_check'):
        content = (S / f'027_{name}.py').read_text(encoding='utf-8').replace('027', '030')
        if name == 'harness':
            content = content.replace('Path(__file__).resolve().with_name("harness") / "sprint030"', 'OUT / "source"')
        ast.parse(content)
        (S / f'030_{name}.py').write_text(content, encoding='utf-8')
    print('Prepared 12 private redirected modules and B scorer. Writes: data/astra/030.')


if __name__ == '__main__':
    main()
