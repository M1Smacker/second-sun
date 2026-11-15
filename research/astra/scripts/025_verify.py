"""Producer checks with a direct Python recount independent of aggregation arrays."""
from collections import Counter
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('025_harness')
D = importlib.import_module('025_inputs')


def main():
    guard = H.Guard()
    hashes = guard.start()
    summary = json.loads((H.OUT / 'summary.json').read_text(encoding='utf-8'))
    checks = []
    for bench in ('planets', 'T156'):
        rows = json.loads((H.OUT / f'combined-{bench}.json').read_text(encoding='utf-8'))
        subsets = [(bench if bench == 'planets' else 'all_T156', rows)]
        if bench == 'T156':
            subsets.append(('reference', [r for r in rows if 3000 <= r['depth_ppm'] <= 6000
                                         and 6 <= r['duration_h'] <= 12]))
        for label, selected in subsets:
            metrics = summary['measurements'][label]
            for b in range(5):
                group = [r for r in selected if r['bin'] == b]
                assert len(group) == metrics['n'][b]
                for a, arm in enumerate(('real', 'flip')):
                    for config in range(4):
                        actual = sum(bool(r[arm][config]) for r in group)
                        assert actual == metrics['counts'][b][a][config]
                        assert abs(actual / len(group) - metrics['rates'][b][a][config]) < 1e-14
            for config in range(4):
                average = sum(sum(bool(r['real'][config]) for r in selected if r['bin'] == b)
                              / sum(r['bin'] == b for r in selected) for b in range(5)) / 5
                assert abs(average - metrics['overall'][0][config]) < 1e-14
                assert sum(bool(r['real'][config]) and not bool(r['real'][config % 2]) for r in selected) == metrics['gains'][config]
                assert sum(bool(r['real'][config % 2]) and not bool(r['real'][config]) for r in selected) == metrics['losses'][config]
        checks.append(bench + ' direct trial, bin and transition counts')
    identity_count = 0
    for campaign in ('g2', 'g3'):
        records = importlib.import_module('025_generate').records(guard, campaign)
        generated = H.OUT / f'generated-{campaign}'
        counts = json.loads((generated / 'counts.json').read_text(encoding='utf-8'))
        changed = {tuple(key) for key in counts['affected']}
        assert all(str(star) in guard.seen[campaign] for star, sector in changed)
        assert counts['counts'].get('preparation_exceptions', 0) == 0
        by_sector = {}
        for bench, rows in records.items():
            for row in rows:
                for sector in ([row['sector']] if bench == 'T156' else row['changed']):
                    by_sector.setdefault((row['star'], sector), []).append((bench, row['trial']))
        source = H.DATA / f'stage3_{campaign}' / f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
        for star, sector in changed:
            for kind in ('groups', 'groups_sap'):
                original = source / kind / f'{star}_{sector}.json'
                if not original.exists():
                    continue
                paths = [generated / 'background' / kind / original.name]
                for bench, trial in by_sector.get((star, sector), []):
                    paths.extend(generated / bench / f'trial-{trial}' / str(sign) / kind / original.name
                                 for sign in (1, -1))
                for path in paths:
                    group = json.loads(path.read_text(encoding='utf-8'))
                    assert (group['tic'], group['sector']) == (star, sector)
                    assert not any(str(m.get('status')).startswith('ERROR') for m in group['meta'])
        unique_identity = {(r['star'], r['sector']) for r in counts['identity']}
        assert len(unique_identity) == counts['identity_sectors']
        identity_count += len(unique_identity)
        for row in counts['identity']:
            name = f'{row["star"]}_{row["sector"]}.json'
            guard.allow_design_file(source / row['kind'] / name)
            old = json.loads((source / row['kind'] / name).read_text(encoding='utf-8'))
            new = json.loads((generated / 'identity' / row['kind'] / name).read_text(encoding='utf-8'))
            canonical = lambda es: sorted(json.dumps(e, sort_keys=True) for e in es)
            assert canonical(old['events']) == canonical(new['events'])
        checks.append(campaign + ' replay completeness, identity and exception counts')
    assert identity_count >= 50
    for path, flags in ((H.DATA / 'g1/probe.fits', 0), (H.ROOT / 'AGENTS.md', os.O_WRONLY)):
        try:
            sys.audit('open', str(path), None, flags)
        except PermissionError:
            continue
        raise RuntimeError('Forbidden access was accepted')
    checks.append('two denied access events')
    source_hashes = json.loads((H.OUT / 'frozen-source-before.json').read_text(encoding='utf-8'))
    for name, digest in source_hashes.items():
        assert hashlib.sha256((H.ROOT / 'pipeline' / name).read_bytes()).hexdigest() == digest
    checks.append('twelve frozen source byte identities')
    result = dict(checks=checks, source_hashes=hashes, frozen_hashes=source_hashes,
                  producer_verification=True, independent_review=False)
    (H.OUT / 'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('Verified', len(checks), 'check groups. Producer verification, independent review pending.')


if __name__ == '__main__':
    main()
