"""Pre-create all shared worker directories, validating draw hosts first."""
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('030_inputs')
H = D.H


def main():
    guard = H.Guard()
    guard.start()
    counts = {}
    for c in ('g2', 'g3'):
        root = H.OUT / f'generated-{c}'
        for phase in ('identity', 'background'):
            for kind in D.KINDS:
                (root / phase / kind).mkdir(parents=True, exist_ok=True)
        for phase, brief in (('planets', '006'), ('fresh', 'fable-fresh'), ('T156', '003')):
            if phase == 'T156':
                rows = [r for r, _ in D.t156_rows(guard, c)]
            else:
                rows = [json.loads(line) for p in sorted(H.OUT.with_name(brief).glob(f'planet-*-*-*-{c}/results.jsonl'))
                        for line in D.read(guard, p, brief).splitlines()]
                rows = [r for r in rows if r['observed']]
            assert rows and len(rows) == len({r['trial'] for r in rows})
            for r in rows:
                assert str(r['star']) in guard.seen[c]
                for sign in ('1', '-1'):
                    for kind in D.KINDS:
                        (root / phase / f'trial-{r["trial"]}' / sign / kind).mkdir(parents=True, exist_ok=True)
            counts[f'{c}-{phase}'] = len(rows)
    (H.OUT / 'layout.json').write_text(json.dumps(counts, indent=2), encoding='utf-8')
    print('Pre-created shared output directories; trial counts:', json.dumps(counts))


if __name__ == '__main__':
    main()
