"""Prepare output-redirected copies and identity scorers, never production imports."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
S = ROOT/'research/astra/scripts'
OUT = ROOT/'data/astra/031'


def main():
    assert OUT.resolve() == (ROOT/'data').resolve()/'astra/031'
    copies = OUT/'source'
    copies.mkdir(exist_ok=True)
    provenance = {}
    for p in (OUT.with_name('030')/'source').glob('*.py'):
        original = p.read_bytes().replace(b'\r\n', b'\n')
        content = original.replace(b'astra/030', b'astra/031').replace(b'"030"', b'"031"').replace(b"'030'", b"'031'")
        ast.parse(content)
        (copies/p.name).write_bytes(content)
        provenance[p.name] = dict(source_sha256_lf=hashlib.sha256(original).hexdigest(),
                                  copy_sha256_lf=hashlib.sha256(content).hexdigest())
    assert len(provenance) == 12
    (copies/'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    for name in ('harness', 'inputs', 'outputs', 'notch', 'score'):
        content = (S/f'030_{name}.py').read_text(encoding='utf-8').replace('030', '031')
        ast.parse(content)
        (S/f'031_{name}.py').write_text(content, encoding='utf-8')
    # Read-only archived pre-tier events, selected only for the all-N1 endpoint.
    content = (S/'030_n1_score.py').read_text(encoding='utf-8').replace('030', '031')
    old = "    generated = H.OUT / f'generated-{campaign}'"
    new = """    generated = H.OUT.with_name('030') / f'generated-{campaign}'
    for saved in generated.rglob('*.json'):
        if saved.parent.name in D.KINDS:
            assert saved.stem.split('_')[0] in guard.seen[campaign]
        guard.reads.add(saved.resolve())"""
    assert content.count(old) == 1
    content = content.replace(old, new).replace("brief = '031'", "brief = '030'")
    (S/'031_endpoint_n1.py').write_text(content, encoding='utf-8')
    print('Prepared 12 private modules and endpoint scorers under brief 031.')


if __name__ == '__main__':
    main()
