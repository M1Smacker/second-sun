"""Count TOI-1338 b matches using the stored T109 matching specification only."""
import ast
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/030'


def main():
    tree = ast.parse((ROOT / 'research/stage3/t109/t109_toi1338_bench.py').read_text(encoding='utf-8'))
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ('TIC', 'OBS', 'PRED'):
                constants[node.targets[0].id] = ast.literal_eval(node.value)
    assert len(constants) == 3
    floor = json.loads((OUT / 'chosen.json').read_text(encoding='utf-8'))['threshold']
    assert floor is not None
    suffix = '-background' + (f'-floor{floor:g}' if floor != 7 else '')
    versions = dict(B=OUT / 'baseline-planets-g2-V0.json', N1=OUT / f'planets-g2-V0{suffix}.json')
    result = {}
    for name, path in versions.items():
        doc = json.loads(path.read_text(encoding='utf-8'))
        events = [e for e in doc['background'] if e['tic'] == constants['TIC'] and e['kind'] == 'real' and e['options'][0]]
        counts = {}
        for group in ('OBS', 'PRED'):
            counts[group] = sum(any(e['sector'] == sec and abs(e['center'] - t) <= 3*s + .1 for e in events)
                                for sec, (t, s) in constants[group].items())
        counts['total'] = counts['OBS'] + counts['PRED']
        result[name] = counts
    result['n_transits'] = 13
    result['pass'] = None  # Rule (g) requires the separate full T109 path.
    result['note'] = 'design background holds 2 of 13 sectors'
    result['scope'] = 'Full design-background tier context; matching windows from existing T109 specification, nine observed plus four forecast epochs'
    (OUT / 'known.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
