"""Reproduce both historical draw designs before writing the new fixed seeds.

No pipeline imports or scoring. Only catalogue rows and design-group filenames.
Run with D:\\second-sun\\.venv\\Scripts\\python.exe -I -B.
"""
import ast
import contextlib
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/031'


def draw(source, destination, seed, fresh=False):
    text = source.read_text(encoding='utf-8')
    if fresh:
        old = "DATA.resolve(strict=True) / 'astra' / 'fable-fresh'"
        assert text.count(old) == 1
        text = text.replace(old, "DATA.resolve(strict=True) / 'astra' / '031' / OUT.name")
    tree = ast.parse(text)
    tree.body = [n for n in tree.body if not isinstance(n, ast.If)]
    scope = {'__name__': 'isolated_draw_definition'}
    exec(compile(tree, str(source), 'exec'), scope)
    scope.update(OUT=destination, SEED=seed)
    destination.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        scope['main']()
    path = destination / ('planet-design.json' if fresh else 'design.json')
    return json.loads(path.read_text(encoding='utf-8')), hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert OUT.resolve() == (ROOT / 'data').resolve() / 'astra/031'
    OUT.mkdir(exist_ok=True)
    print('READ design catalogues and design-group filenames only; WRITE', OUT, flush=True)
    checks = {}
    for label, source, prior, old_seed, new_seed, fresh in (
        ('T156', ROOT/'research/astra/scripts/003_design.py', ROOT/'data/astra/003/design.json',
         2026111303, 2026112202, False),
        ('fresh', ROOT/'data/fable/x1/fresh_draws.py', ROOT/'data/astra/fable-fresh/planet-design.json',
         2026111601, 2026112201, True),
    ):
        historical = json.loads(prior.read_text(encoding='utf-8'))
        reproduced, digest = draw(source, OUT/f'{label}-identity', old_seed, fresh)
        if reproduced != historical:
            checks[label] = {'identity': False, 'status': 'STOP before scoring',
                             'historical_count': len(historical['trials']),
                             'reproduced_count': len(reproduced['trials'])}
            (OUT/'draw-checks.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')
            raise RuntimeError(label + ' original draw identity failed; no new scoring permitted')
        new, new_digest = draw(source, OUT/f'{label}-new', new_seed, fresh)
        assert len(new['trials']) == (1250 if fresh else 2000)
        assert new['trials'] != historical['trials']
        repeated, _ = draw(source, OUT/f'{label}-new', new_seed, fresh)
        assert repeated == new
        checks[label] = dict(identity=True, count=len(new['trials']), seed=new_seed,
                             original_sha256=digest, new_sha256=new_digest, repeat_identity=True,
                             source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    (OUT/'draw-checks.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main()
