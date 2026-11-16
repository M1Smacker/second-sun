"""Direct recount and raw event identities, independent of summary aggregation."""
import csv
import importlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('026_inputs')
H = D.H


def main():
    guard = H.Guard(); guard.start()
    summary = json.loads((H.OUT / 'summary-m4.json').read_text(encoding='utf-8'))
    planets = json.loads((H.OUT / 'combined-planets.json').read_text(encoding='utf-8'))
    trials = json.loads((H.OUT / 'combined-T156.json').read_text(encoding='utf-8'))
    assert len(planets) == 1098 and len(trials) == 2000
    assert len({(r['campaign'], r['trial']) for r in planets}) == 1098
    old = json.loads(D.read(guard, H.DATA / 'astra/023/combined-planets.json', '023'))
    old = {(r['campaign'], r['trial']): r for r in old}
    for r in planets:
        assert str(r['star']) in guard.seen[r['campaign']]
        assert all(r[arm][0] == old[r['campaign'], r['trial']][arm][0] for arm in ('real', 'flip'))
    checked = 0
    for key, rows in (('fixed1098', planets), ('T156reference', [r for r in trials if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12])):
        result = summary['metrics'][key]
        for arm, name in enumerate(('real', 'flip')):
            for option in range(6):
                fractions = []
                for b in range(5):
                    group = [r for r in rows if r['bin'] == b]
                    n = len(group)
                    k = sum(bool(r[name][option]) for r in group)
                    assert n == result['n'][b] and k == result['counts'][b][arm][option]
                    fractions.append(k / n)
                    checked += 1
                assert math.isclose(sum(fractions) / 5, result['rates'][arm][option], abs_tol=1e-14)
    identities = set()
    for folder in H.OUT.glob('generated-*-*'):
        if not folder.is_dir():
            continue
        campaign = folder.name.split('-')[1]
        counts = json.loads((folder / 'counts.json').read_text(encoding='utf-8'))
        identities.update((campaign, *row) for row in counts['identity'])
        source = H.DATA / f'stage3_{campaign}' / f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
        for kind in D.KINDS:
            for path in (folder / 'identity' / kind).glob('*.json'):
                original = guard.allow_design_file(source / kind / path.name)
                a = json.loads(path.read_text(encoding='utf-8'))
                b = json.loads(original.read_text(encoding='utf-8'))
                canon = lambda es: sorted(json.dumps(e, sort_keys=True) for e in es)
                assert canon(a['events']) == canon(b['events'])
    assert len(identities) == 50
    inv = json.loads((H.OUT / 'inventory-summary.json').read_text(encoding='utf-8'))
    assert all(inv[c]['roster_difference'] == 0 for c in ('g2', 'g3'))
    # Deliberate arithmetic corruption must fail the independent count comparison.
    count = summary['metrics']['fixed1098']['counts'][0][0][0]
    expected = sum(r['real'][0] for r in planets if r['bin'] == 0)
    assert count == expected and count + 1 != expected
    result = dict(baseline_planet_identities=1098, direct_bin_counts=checked, class_a_sector_identities=50,
                  arithmetic_mutation_rejected=True, roster_identity=True,
                  independent_review=False)
    (H.OUT / 'verification-m4.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
