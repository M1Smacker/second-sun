"""Copy the reviewed 032 I/O harness into the 032b output boundary."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
S = ROOT/'research/astra/scripts'
OUT = ROOT/'data/astra/032b'


def main():
    OUT.mkdir(exist_ok=True)
    for name in ('tracks', 'tmp', 'numba-cache', 'prep'):
        (OUT/name).mkdir(exist_ok=True)
    copies = S/'032b_harness'
    copies.mkdir(exist_ok=True)
    provenance = {}
    paths = list((S/'032_harness').glob('*.py'))
    paths += [S/f'032_{name}.py' for name in ('harness', 'outputs', 'eclipse_fit', 'eclipse_select', 'eclipse_calibrate')]
    for src in paths:
        old = src.read_text(encoding='utf-8')
        new = old.replace('032', '032b')
        ast.parse(new)
        dst = copies/src.name if src.parent.name == '032_harness' else S/src.name.replace('032_', '032b_')
        if dst.exists():
            assert dst.read_text(encoding='utf-8') == new, 'Refuse changed copy'
        else:
            dst.write_text(new, encoding='utf-8', newline='\n')
        if dst.parent == copies:
            provenance[dst.name] = dict(copy_sha256_lf=hashlib.sha256(new.encode()).hexdigest(),
                                        source032_sha256_lf=hashlib.sha256(old.encode()).hexdigest())
    (OUT/'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    print('Prepared 032b output guard and unchanged measurement/alias/trap functions.')


if __name__ == '__main__':
    main()
