"""Count fixed-draw input failures without changing or scoring any draw.

Run: D:\second-sun\.venv\Scripts\python.exe -I -B research/astra/scripts/audit_031b_spans.py
Only counts and provenance are printed. Detailed inputs stay behind the guard.
"""
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('031_inputs')
H = D.H


def main():
    os.environ.update(SS_SET='g2', VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    for campaign in ('g2', 'g3'):
        guard.allow_machine_inputs(campaign)
    import pandas as pd
    import stage2_search as S2

    original = json.loads(D.read(guard, H.DATA/'astra/003/design.json', '003'))
    new = json.loads((H.OUT/'T156-new/design.json').read_text(encoding='utf-8'))
    assert original['seed'] == 2026111303 and new['seed'] == 2026112202
    assert len(original['trials']) == len(new['trials']) == 2000
    expected = {r['trial']: r for r in original['trials']}
    assert len(expected) == 2000
    results = {}
    seen = set()
    for campaign in ('g2', 'g3'):
        rows = [r for r, _ in D.t156_rows(guard, campaign)]
        for row in rows:
            assert row['trial'] not in seen
            seen.add(row['trial'])
            assert all(row[k] == v for k, v in expected[row['trial']].items())
            assert all(k in row for k in ('time', 'dip', 'bump'))
        results[campaign] = dict(original_results=len(rows), original_design_fields_equal=True)
        saved = H.OUT/'records'/f'T156_old-{campaign}.json'
        if saved.exists():
            archived = {r['trial']: r for r in rows}
            recorded = json.loads(saved.read_text(encoding='utf-8'))
            assert len(recorded) == len(rows)
            assert all({k: v for k, v in r.items() if k != '_archive_folder'} == archived[r['trial']]
                       for r in recorded)
            results[campaign]['existing_old_records_equal'] = True
        else:
            results[campaign]['existing_old_records_equal'] = 'not written before stop'
    assert seen == set(expected)

    for campaign in ('g2', 'g3'):
        best = pd.read_csv(H.DATA/campaign/'audit/best_per_star_sector.csv')
        bestmap = {(r.tic, r.sector): r.product for r in best.itertuples()}
        selected = [r for r in new['trials'] if r['campaign'] == campaign]
        spans = {}
        empty = []
        for r in selected:
            star, sector = r['star'], r['sector']
            assert str(star) in guard.seen[campaign]
            key = star, sector
            if key not in spans:
                path = H.DATA/f'stage3_{campaign}'/f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'/'groups'/f'{star}_{sector}.json'
                guard.allow_design_file(path)
                group = json.loads(path.read_text(encoding='utf-8'))
                product = bestmap.get(key)
                meta = next((m for m in group['meta'] if m.get('product') == product), group['meta'][0])
                rawpath = H.DATA/campaign/str(star)/meta['file']
                guard.allow_design_file(rawpath)
                times = S2.load(str(rawpath), info=True)[0]
                spans[key] = (len(times), bool(len(times) and times.max() > times.min()))
            if not spans[key][0]:
                empty.append(r)
        results[campaign].update(
            new_draws=len(selected), new_unique_groups=len(spans),
            empty_draws=len(empty), empty_unique_groups=sum(n == 0 for n, _ in spans.values()),
            nonempty_degenerate_groups=sum(n > 0 and not positive for n, positive in spans.values()),
            empty_draws_by_period_bin=[sum(r['bin'] == b for r in empty) for b in range(5)],
            replaced=0, redrawn=0, excluded=0,
        )

    source = H.ROOT/'research/astra/scripts'
    lockpath = H.OUT/'run-source-hashes.json'
    locked = json.loads(lockpath.read_text(encoding='utf-8'))
    current = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('031*.py')}
    assert current == locked, 'Existing bench source lock changed'
    report = dict(status='blocked_no_replacement_rule', campaigns=results,
                  original_total=len(seen), source_lock_unchanged=True,
                  lock_sha256=hashlib.sha256(lockpath.read_bytes()).hexdigest(),
                  records_sha256=current['031_records.py'],
                  original_worker_sha256=hashlib.sha256((source/'003_worker.py').read_bytes()).hexdigest(),
                  diagnostic_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  scope='Raw load only; no injection, masking, detrending, search or retiering')
    (H.OUT/'031b-span-audit.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
