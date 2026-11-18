"""Terminal producer checks, no claims of independent scientific review."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/030'
S = ROOT / 'research/astra/scripts'


def main():
    result = {}
    for p in S.glob('030*.py'):
        ast.parse(p.read_text(encoding='utf-8'))
    result['syntax'] = True
    locked = json.loads((OUT / 'run-source-hashes.json').read_text(encoding='utf-8'))
    now = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in S.glob('030*.py')}
    assert locked == now, 'Study scripts changed during the run'
    result['study_source_unchanged'] = True
    original = json.loads((OUT / 'frozen-before.json').read_text(encoding='utf-8'))
    assert all(hashlib.sha256((ROOT / 'pipeline' / name).read_bytes()).hexdigest() == digest for name, digest in original.items())
    result['frozen_source_unchanged'] = len(original)
    assert json.loads((OUT / 'notch-checks.json').read_text(encoding='utf-8'))['passed']
    assert json.loads((OUT / 'baseline-check.json').read_text(encoding='utf-8'))['background']['B'] == [174, 79]
    layout = json.loads((OUT / 'layout.json').read_text(encoding='utf-8'))
    for c in ('g2', 'g3'):
        for phase in ('background', 'planets', 'fresh', 'T156'):
            progress = [json.loads((OUT / f'generated-{c}/progress-{phase}-{i}.json').read_text(encoding='utf-8')) for i in range(3)]
            assert all(p['status'] == 'complete' and p['done'] == p['total'] for p in progress)
            assert sum(p['groups'] for p in progress) > 0
        assert layout[f'{c}-planets'] > 0
    result['all_worker_phases_terminal'] = True
    summary = json.loads((OUT / 'summary.json').read_text(encoding='utf-8'))
    assert summary['passes'] == all(summary['rules'].values())
    assert summary['seed'] == 2026111830 and summary['bootstrap_draws'] == 10000
    eligible = [r['floor'] for r in summary['alarm_curve'] if r['real'] <= 174 and r['upside_down'] <= 79]
    assert summary['threshold'] == min(eligible)
    for key, n in (('choosing_all', 1098), ('choosing_possible', 968), ('T156_all', 2000), ('T156_reference', 222)):
        assert summary['metrics'][key]['n'] == n
    result['selection_population_and_verdict_consistency'] = True
    result['passed'] = True
    (OUT / 'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
