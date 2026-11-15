"""Create redirected bench sources without changing git metadata or frozen code."""
import hashlib
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
SCRIPTS = ROOT / 'research/astra/scripts'
OUT = ROOT / 'data/astra/024'


def main():
    OUT.mkdir(exist_ok=True)
    destination = SCRIPTS / 'harness/sprint024'
    destination.mkdir(exist_ok=True)
    provenance = {}
    for path in (SCRIPTS / 'harness/sprint023').glob('*.py'):
        original = path.read_bytes().replace(b'\r\n', b'\n')
        copied = original.replace(b'sprint023', b'sprint024')
        copied = copied.replace(b'astra/023', b'astra/024')
        copied = copied.replace(b'"023"', b'"024"').replace(b"'023'", b"'024'")
        (destination / path.name).write_bytes(copied)
        provenance[path.name] = dict(source_sha256_lf=hashlib.sha256(original).hexdigest(),
                                     copy_sha256_lf=hashlib.sha256(copied).hexdigest())
    (destination / 'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    harness = (SCRIPTS / '003_harness.py').read_text(encoding='utf-8').replace('003', '024')
    (SCRIPTS / '024_harness.py').write_text(harness, encoding='utf-8')
    inputs = (SCRIPTS / '023_inputs.py').read_text(encoding='utf-8').replace("import_module('023_harness')", "import_module('024_harness')")
    (SCRIPTS / '024_inputs.py').write_text(inputs, encoding='utf-8')
    score = (SCRIPTS / '023_score.py').read_text(encoding='utf-8')
    score = score.replace("import_module('023_inputs')", "import_module('024_inputs')")
    score = score.replace('def main(campaign, bench, mode, limit=None):',
                          'def main(campaign, bench, mode, limit=None, baseline_run=False):')
    changes = {
        "groups = {key: retier(events) for key, events in groups.items()}": """generated = H.OUT / f'generated-{campaign}'
    coverage = json.loads((generated / 'counts.json').read_text(encoding='utf-8'))
    changed_keys = set() if baseline_run else {tuple(key) for key in coverage['affected']}
    extra_folder = H.OUT / f'coverage-{campaign}'
    extra_keys = set()
    if not baseline_run and (extra_folder / 'counts.json').exists():
        extra = json.loads((extra_folder / 'counts.json').read_text(encoding='utf-8'))
        extra_keys = {tuple(key) for key in extra['affected']}
        changed_keys |= extra_keys
    empty_folder = H.OUT / f'empty-{campaign}'
    empty_keys = set()
    if not baseline_run and (empty_folder / 'counts.json').exists():
        empty = json.loads((empty_folder / 'counts.json').read_text(encoding='utf-8'))
        empty_keys = {tuple(key) for key in empty['affected']}
        changed_keys |= empty_keys
    def generation_for(key):
        return empty_folder if key in empty_keys else extra_folder if key in extra_keys else generated
    for key in changed_keys:
        assert key in groups
        events = []
        for kind in D.KINDS:
            path = generation_for(key) / 'background' / kind / f'{key[0]}_{key[1]}.json'
            if path.exists():
                group = json.loads(path.read_text(encoding='utf-8'))
                assert (group['tic'], group['sector']) == key
                events.extend(group['events'])
        groups[key] = events
    groups = {key: retier(events) for key, events in groups.items()}""",
        "variant_prior = tiers(context[own | near]) if strict and mode != 'V0' else None":
            "variant_prior = tiers(context[own | near]) if strict and not baseline_run else None",
        "path = location / kind / f'{star}_{sec}.json'": """if (star, sec) in changed_keys:
                        location = generation_for((star, sec)) / bench / f'trial-{trial}' / str(sign)
                        brief = '024'
                    path = location / kind / f'{star}_{sec}.json'""",
        "result[arm] = [bool(hit - pre) for hit, pre in zip(hits, prior)]": """result[arm] = [bool(hit - pre) for hit, pre in zip(hits, prior)]
            detected = after[(after.tic == star) & after.primary & (after.kind == arm) & (after.snr >= 7)]
            result[arm + '_found'] = any(abs(event.center - center) <= duration / 2
                                       for event in detected.itertuples() for center, duration in observed)""",
        "if mode == 'V0':\n                expected = identity[trial][arm]":
            "if False:\n                expected = identity[trial][arm]",
    }
    for before, after in changes.items():
        if score.count(before) != 1:
            raise RuntimeError('Scorer source no longer matches the reviewed adapter')
        score = score.replace(before, after)
    score = score.replace('Re-score fixed raw-injection replays with the eight predeclared configurations.',
                          'Score fresh 024 subtraction replays with the adopted 023 scoring rules.')
    score = score.replace("f'{bench}-{campaign}-{mode}{suffix}.json'", "f'{\"baseline-\" if baseline_run else \"\"}{bench}-{campaign}-{mode}{suffix}.json'")
    score = score.replace("parser.add_argument('--limit', type=int)",
                          "parser.add_argument('--limit', type=int)\n    parser.add_argument('--baseline', action='store_true')")
    score = score.replace('arguments.mode, arguments.limit)', 'arguments.mode, arguments.limit, arguments.baseline)')
    score = score.replace("if False:\n                expected = identity[trial][arm]", "if baseline_run:\n                expected = identity[trial][arm]")
    (SCRIPTS / '024_score.py').write_text(score, encoding='utf-8')
    print('Prepared twelve redirected source modules and a guarded raw-light harness.')


if __name__ == '__main__':
    main()
