"""Producer recount of metadata outputs, static checks and CLI path rejection."""
import ast
import importlib
import json
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parents[2]
OUT = ROOT/'data/astra/035'


def main():
    paths = sorted(SCRIPTS.glob('035_*.py'))
    for p in paths:
        ast.parse(p.read_text(encoding='utf-8'))
    sample = json.loads((OUT/'sample.json').read_text(encoding='utf-8'))
    inventory = json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
    selected = {int(r['tic']): int(r['band']) for r in sample['selected']}
    assert len(selected) == len(sample['selected']) == 150
    entries = inventory['manifest']
    assert {int(r['tic']) for r in entries} == selected.keys() and len(entries) == 150
    recount = []
    for b in range(3):
        records = [r for r in entries if selected[int(r['tic'])] == b]
        count = dict(stars=len(records), with_local=sum(bool(r['files']) for r in records),
                     files=sum(len(r['files']) for r in records),
                     bytes=sum(f['bytes'] for r in records for f in r['files']))
        assert count == inventory['counts'][b]
        recount.append(count)
    sys.path.insert(0, str(SCRIPTS))
    finder = importlib.import_module('035_period')
    rejected = 0
    for args in [(ROOT/'forbidden.npz', OUT/'unused.json'),
                 (OUT/'unused.npz', ROOT/'forbidden.json')]:
        sys.argv = ['035_period.py', *map(str, args)]
        try:
            finder.main()
        except PermissionError:
            rejected += 1
        else:
            raise AssertionError('CLI path rejection failed')
    report = ROOT/'research/astra/reports/035-report.md'
    text = report.read_text(encoding='utf-8')
    assert '\u2013' not in text and '\u2014' not in text
    result = dict(parsed_python_files=len(paths), metadata_recount=recount,
                  cli_rejected_paths=rejected, synthetic_gate='FAIL, intentionally unresolved',
                  independent_review=False)
    (OUT/'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
