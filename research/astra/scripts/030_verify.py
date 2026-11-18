"""Terminal producer checks, no claims of independent scientific review."""
import ast
import csv
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
    result['study_source_matches_amended_lock'] = True
    amendment = json.loads((OUT / '030d-source-amendment.json').read_text(encoding='utf-8'))
    changed = {name for name in amendment['before'] if amendment['before'][name] != now[name]}
    added = now.keys() - amendment['before'].keys()
    assert changed == {'030_finish.py', '030_verify.py'}
    assert added == {'030_t109.py'}
    assert amendment['after'] == now
    result['heavy_scoring_sources_unchanged'] = True
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
    known = json.loads((OUT / 'known.json').read_text(encoding='utf-8'))
    assert summary['known'] == known
    assert known['B']['total'] == 6 and known['threshold'] == 6.5
    assert known['pass'] == (known['N1']['total'] >= 6) == summary['rules']['g']
    assert known['n_transits'] == 13
    assert known['design_background']['B']['total'] == 1
    assert known['design_background']['N1']['total'] == 2
    spec = {}
    for node in ast.parse((ROOT / 'research/stage3/t109/t109_toi1338_bench.py').read_text(encoding='utf-8')).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('OBS', 'PRED'):
            spec[node.targets[0].id] = ast.literal_eval(node.value)
    scored = json.loads((OUT / 't109-scored.json').read_text(encoding='utf-8'))
    windows = {**spec['OBS'], **spec['PRED']}
    with (ROOT / 'data/t109/toi1338_q5.csv').open(encoding='utf-8') as f:
        historical = list(csv.DictReader(f))
    history_hits = {int(r['sector']) for r in historical if r['oae'] == 'tier1'}
    history_missing = {int(r['sector']) for r in historical if r.get('status') == 'no stored file'}
    for version, floor in (('B', 7), ('N1', 6.5)):
        # Independently count the saved final tiers; no pipeline or producer import.
        accepted = {r['sector'] for r in scored[version] if r['kind'] == 'real' and r['primary']
                    and r['snr'] >= floor and r['tier'] in ('1A', '1L', '1B')
                    and abs(r['center'] - windows[r['sector']][0]) <= 3*windows[r['sector']][1] + .1}
        assert len(accepted) == known[version]['total']
        assert sum(s in spec['OBS'] for s in accepted) == known[version]['OBS']
        assert sum(s in spec['PRED'] for s in accepted) == known[version]['PRED']
        assert known[version]['sectors_checked'] == 13
        assert known[version]['missing_sectors'] == len(history_missing) == 1
        if version == 'B':
            assert accepted == history_hits
    hashes = json.loads((OUT / 't109-input-hashes.json').read_text(encoding='utf-8'))
    assert len(hashes) == 38
    assert all(hashlib.sha256((ROOT / 'data' / p).read_bytes()).hexdigest() == sha for p, sha in hashes.items())
    result['t109_recount_and_historical_window_identity'] = True
    result['t109_inputs_unchanged'] = len(hashes)
    result['passed'] = True
    (OUT / 'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
