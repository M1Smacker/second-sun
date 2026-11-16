"""Install the fixed prototype into redirected copies and emit a reviewable diff."""
import difflib
import hashlib
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
SCRIPTS = ROOT / 'research/astra/scripts'


def main():
    destination = SCRIPTS / 'harness/sprint025'
    provenance = json.loads((destination / 'provenance.json').read_text(encoding='utf-8'))
    patch = []
    for name, count in (('detect_v2.py', 1), ('sap_twin.py', 2)):
        path = destination / name
        original = path.read_text(encoding='utf-8')
        before = 'lc = lk.read(path, quality_bitmask="hard")'
        after = 'lc = __import__("025_loader").read(lk, path)  # bench-only bit-4096 candidate'
        assert original.count(before) == count
        revised = original.replace(before, after)
        path.write_text(revised, encoding='utf-8')
        provenance[name]['copy_sha256_lf'] = hashlib.sha256(revised.encode('utf-8')).hexdigest()
        patch.extend(difflib.unified_diff(original.splitlines(True), revised.splitlines(True),
                                        fromfile=f'bench-before/{name}', tofile=f'bench-after/{name}'))
    (destination / 'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    (SCRIPTS / '025-loader-prototype.patch').write_text(''.join(patch), encoding='utf-8')
    print('Installed the predeclared bit-4096 candidate in two bench modules.')


if __name__ == '__main__':
    main()
