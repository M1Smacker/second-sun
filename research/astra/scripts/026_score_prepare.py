"""Build the M4 scorer from 023 with explicit, reviewable substitutions."""
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
S = ROOT / 'research/astra/scripts'


def main():
    text = (S / '023_score.py').read_text(encoding='utf-8')
    def replace(old, new):
        nonlocal text
        assert old in text, old[:80]
        text = text.replace(old, new)
    replace("D = importlib.import_module('023_inputs')", "D = importlib.import_module('026_inputs')\nM = importlib.import_module('026_rules')")
    replace("O = importlib.import_module('023_outputs')", "O = importlib.import_module('026_outputs')")
    start = text.index('CONFIGS = ')
    end = text.index('LABELS = ', start)
    text = text[:start] + "CONFIGS = ('B', 'B+M2', 'B+M4', 'B+C96fallback', 'B+C96+DS+M4', 'cap+R2+M4')\nINDICES = {'V0': (0, 3), 'V2': (1,), 'V4': (2, 4, 5)}\n" + text[end:]
    replace('return [baseline, baseline and within_cap, shaped, shaped and within_cap]',
            "event['gap_dump'] = known or ('momentum dump' in flags and uneven)\n    released = tier_of(event) in S.TIERS\n    return [baseline, baseline, baseline, baseline and within_cap, shaped and within_cap, released and within_cap]")
    replace('    def retier(events):', '''    fallback = json.loads((H.OUT / 'fallback-radii.json').read_text(encoding='utf-8'))
    for key, radius in fallback.items():
        name, star = key.split(':')
        if name == campaign and int(star) not in radii:
            radii[int(star)] = min(1., (.2009 / radius) ** 2) * 1e6
    inventory = json.loads((H.OUT / f'inventory-{campaign}.json').read_text(encoding='utf-8'))
    class_b = {(r['star'], r['sector']) for r in inventory if r['category'] == 'B'}
    b_hosts = {star for star, sector in class_b}
    new_b = {r['star'] for r in inventory if r['category'] == 'B' and not r['historical_m2']}

    def retier(events):''')
    # Only V2 uses the global historical M2 selection. V4 uses it just on class B sectors.
    replace("if mode != 'V0' and affected:", "if mode != 'V0' and (affected or (mode == 'V4' and new_b)):")
    replace("folder = H.OUT.with_name('010') / f'{mode}-{campaign}-{slot}'", "folder = H.OUT.with_name('010') / f'V2-{campaign}-{slot}'")
    replace("folder = H.OUT.with_name('011') / f't156-{mode.lower()}-{campaign}-{slot}'", "folder = H.OUT.with_name('011') / f't156-v2-{campaign}-{slot}'")
    replace("        context = frame([e for key, events in groups.items()", '''        if mode == 'V4':
            replaced = {key: value for key, value in replaced.items() if key in class_b}
            for folder in sorted(H.OUT.glob(f'generated-{campaign}-*')):
                assert (folder / 'counts.json').is_file(), 'M4 generation not complete'
                for kind in D.KINDS:
                    for path in (folder / 'background' / kind).glob('*.json'):
                        key = tuple(map(int, path.stem.split('_')))
                        assert key in class_b and key[0] in new_b
                        replaced.setdefault(key, []).extend(json.loads(path.read_text(encoding='utf-8'))['events'])
            assert replaced.keys() == class_b, 'Missing M4 class B background'
        context = frame([e for key, events in groups.items()''')
    replace("            flags[index] = four if mode == 'V0' else [four[1], four[3]]", '''            values = [four[i] for i in INDICES[mode]]
            if mode == 'V4' and row['tic'] in b_hosts:
                leftovers = events[(events.tic == row['tic']) & events.primary & (events.kind == row['kind']) & (events.snr >= 7)]
                why = M.reason(leftovers.to_dict('records'), radii.get(row['tic']))
                if why:
                    values = [False] * len(values)
            flags[index] = values''')
    replace("    if mode == 'V0':\n        assert identity.keys()", "    if mode == 'V0':\n        assert identity.keys()")
    # V4 needs every sector of the host in the hold pool, including prior context.
    replace("        before = tiers(context[(own & in_sector) | near]) if not strict else None",
            "        before = tiers(context[(own if mode == 'V4' else own & in_sector) | near]) if not strict else None")
    replace("if mode != 'V0' and star in affected:", "if mode != 'V0' and star in affected and (mode != 'V4' or (star, sec) in class_b):")
    replace("                for kind in D.KINDS:\n                    path = location / kind / f'{star}_{sec}.json'", '''                if mode == 'V4' and (star, sec) in class_b and star in new_b:
                    locations = [p / bench / f'trial-{trial}' / str(sign) for p in H.OUT.glob(f'generated-{campaign}-*')
                                 if (p / bench / f'trial-{trial}' / str(sign) / 'groups' / f'{star}_{sec}.json').is_file()]
                    assert len(locations) == 1, 'Missing fresh M4 injection replay'
                    location, brief = locations[0], '026'
                for kind in D.KINDS:
                    path = location / kind / f'{star}_{sec}.json' ''')
    replace("            if strict:\n                after = after[after.sector == record['sector']]", "            if strict and mode != 'V4':\n                after = after[after.sector == record['sector']]")
    replace("extra = passing(variant_prior[variant_prior.sector == record['sector']], star, arm, observed)",
            "extra = passing(variant_prior if mode == 'V4' else variant_prior[variant_prior.sector == record['sector']], star, arm, observed)")
    replace("                assert result[arm][2] == expected[2], f'{bench} DS identity differs at private trial'", "                # The second output is C96 with fallback; baseline identity remains exact.")
    replace("choices=('V0', 'V1', 'V2')", "choices=('V0', 'V2', 'V4')")
    text = text.replace('eight predeclared configurations', 'six predeclared configurations')
    text = '\n'.join(line.rstrip() for line in text.splitlines()) + '\n'
    compile(text, '026_score.py', 'exec')
    (S / '026_score.py').write_text(text, encoding='utf-8')
    print('Prepared six-configuration scorer; B identity remains mandatory.')


if __name__ == '__main__':
    main()
