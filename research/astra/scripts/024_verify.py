"""Different-method trial recount and source/access verification."""
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('024_harness')


def main():
    guard = H.Guard()
    hashes = guard.start()
    summary = json.loads((H.OUT / 'summary.json').read_text(encoding='utf-8'))
    checks = []
    for bench in ('planets', 'T156'):
        rows = json.loads((H.OUT / f'combined-{bench}.json').read_text(encoding='utf-8'))
        subsets = [(bench if bench == 'planets' else 'all_T156', rows)]
        if bench == 'T156':
            subsets.append(('reference', [r for r in rows if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]))
        for label, selected in subsets:
            stored = summary['measurements'][label]
            assert len(selected) == sum(stored['n'])
            for b in range(5):
                bin_rows = [r for r in selected if r['bin'] == b]
                assert len(bin_rows) == stored['n'][b]
                for arm, key in enumerate(('real', 'flip')):
                    for j in range(4):
                        hits = sum(bool(r[key][j]) for r in bin_rows)
                        found = sum(bool(r[key + '_found'][j]) for r in bin_rows)
                        assert hits == stored['counts'][b][arm][j]
                        assert found == stored['found_counts'][b][arm][j]
                        assert abs(hits / len(bin_rows) - stored['rates'][b][arm][j]) < 1e-14
            checks.append(label + ' direct trial recount')
    # Historical reference equality, including every individual baseline recovery.
    old = H.DATA / 'astra/023'
    for bench in ('planets', 'T156'):
        path = old / f'combined-{bench}.json'
        guard.reads.add(path.resolve())
        historical = {(r['campaign'], r['trial']): r for r in json.loads(path.read_text(encoding='utf-8'))}
        current = json.loads((H.OUT / f'combined-{bench}.json').read_text(encoding='utf-8'))
        for row in current:
            previous = historical[row['campaign'], row['trial']]
            for arm in ('real', 'flip'):
                assert row[arm][:2] == previous[arm][:2]
        checks.append(bench + ' historical B and C96 identity')
    for campaign in ('g2', 'g3'):
        data = json.loads((H.OUT / f'generated-{campaign}/counts.json').read_text(encoding='utf-8'))
        changed = {tuple(key) for key in data['affected']}
        extra_path = H.OUT / f'coverage-{campaign}/counts.json'
        if extra_path.exists():
            extra = json.loads(extra_path.read_text(encoding='utf-8'))
            extra_keys = {tuple(key) for key in extra['affected']}
            audit = json.loads((H.OUT / f'coverage-audit-{campaign}.json').read_text(encoding='utf-8'))
            assert extra_keys == {tuple(key) for key in audit['uncertain']}
            changed |= extra_keys
        empty_path = H.OUT / f'empty-{campaign}/counts.json'
        if empty_path.exists():
            empty = json.loads(empty_path.read_text(encoding='utf-8'))
            empty_keys = {tuple(key) for key in empty['affected']}
            audit = json.loads((H.OUT / f'coverage-audit-{campaign}.json').read_text(encoding='utf-8'))
            assert empty_keys == {tuple(key) for key in audit['empty_mask_uncertain']}
            changed |= empty_keys
        assert all(str(star) in guard.seen[campaign] for star, _ in changed)
        locations = {}
        for mode in ('empty', 'coverage', 'generated'):
            folder = H.OUT / f'{mode}-{campaign}'
            manifest = folder / 'counts.json'
            if manifest.exists():
                for key in json.loads(manifest.read_text(encoding='utf-8'))['affected']:
                    pair = tuple(key)
                    assert pair not in locations
                    locations[pair] = folder
        def folder_for(star, sector):
            return locations[star, sector]
        kinds = {}
        source = H.DATA / f'stage3_{campaign}' / f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
        for star, sector in changed:
            kinds[star, sector] = [kind for kind in ('groups', 'groups_sap')
                                   if (source / kind / f'{star}_{sector}.json').exists()]
            assert 'groups' in kinds[star, sector]
            for kind in kinds[star, sector]:
                background = folder_for(star, sector) / 'background' / kind / f'{star}_{sector}.json'
                saved = json.loads(background.read_text(encoding='utf-8'))
                assert (saved['tic'], saved['sector']) == (star, sector)
        for bench in ('planets', 'T156'):
            generator = importlib.import_module('024_generate')
            rows = generator.records(guard, campaign)[bench]
            expected = {(r['trial'], r['star'], sector, sign)
                        for r in rows for sector in ([r['sector']] if bench == 'T156' else r['changed'])
                        if (r['star'], sector) in changed for sign in (1, -1)}
            actual = set()
            for mode in ('generated', 'coverage', 'empty'):
                for path in (H.OUT / f'{mode}-{campaign}' / bench).glob('trial-*/*/groups/*.json'):
                    trial = int(path.parents[2].name.removeprefix('trial-'))
                    sign = int(path.parents[1].name)
                    star, sector = map(int, path.stem.split('_'))
                    actual.add((trial, star, sector, sign))
            assert actual == expected
            for trial, star, sector, sign in expected:
                for kind in kinds[star, sector]:
                    path = folder_for(star, sector) / bench / f'trial-{trial}' / str(sign) / kind / f'{star}_{sector}.json'
                    saved = json.loads(path.read_text(encoding='utf-8'))
                    assert (saved['tic'], saved['sector']) == (star, sector)
                    assert not any(str(m.get('status')).startswith('ERROR') for m in saved['meta'])
        checks.append(campaign + ' complete replay coverage and design membership')
    for path, flags in ((H.DATA / 'g1/probe.fits', 0), (H.ROOT / 'AGENTS.md', 1)):
        try:
            sys.audit('open', str(path), None, flags)
        except PermissionError:
            continue
        raise RuntimeError('Access rejection check failed')
    checks.append('two denied access probes')
    assert summary['synthetic']['asymmetric_mutation_rejected']
    assert summary['symmetry_max_error'] < 2e-14
    checks.append('synthetic mutation and real-light inversion')
    measured = H.OUT / 'source-bundle-at-measurement'
    if measured.exists():
        for path in measured.glob('*.py'):
            original = path.read_bytes().replace(b'\r\n', b'\n')
            current = (H.COPIES / path.name).read_bytes().replace(b'\r\n', b'\n')
            expected = original
            if path.name == 'stage2_search.py':
                needle = b'np.random.default_rng(20261024)'
                assert original.count(needle) == 1
                assert original.index(b'def select():') < original.index(needle) < original.index(b'class Prod:')
                expected = original.replace(needle, b'np.random.default_rng(20261023)')
            assert current == expected
        checks.append('measured source snapshot differs only in unused legacy selection seed')
    result = dict(checks=checks, source_hashes=hashes, measurement_source_snapshot=str(measured), producer_verification=True,
                  independent_review=False)
    (H.OUT / 'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('Verified', len(checks), 'groups of checks')


if __name__ == '__main__':
    main()
