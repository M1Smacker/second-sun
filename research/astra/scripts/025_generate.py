"""Generate affected quality-policy replays and 50 unaffected sector identities."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('025_harness')
D = importlib.import_module('025_inputs')


def records(guard, campaign):
    result = {'T156': [r for r, _ in D.t156_rows(guard, campaign)], 'planets': []}
    for path in sorted((H.DATA / 'astra/006').glob(f'planet-*-*-*-{campaign}/results.jsonl')):
        result['planets'].extend(json.loads(line) for line in D.read(guard, path, '006').splitlines())
    for rows in result.values():
        assert len(rows) == len({r['trial'] for r in rows})
        assert all(str(r['star']) in guard.seen[campaign] for r in rows)
    return result


def main(campaign, smoke=False):
    os.environ.update(SS_SET=campaign, VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    refs = guard.allow_machine_inputs(campaign)
    import numpy as np
    import pandas as pd
    import stage2_search as S2
    import stage3 as S3
    import stage3_core as C
    import sap_twin as T
    Q = importlib.import_module('025_loader')
    out = H.OUT / f'{"smoke" if smoke else "generated"}-{campaign}'
    out.mkdir(exist_ok=True)
    now = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', started=now.isoformat(),
                    expected_finish=(now + timedelta(hours=2)).isoformat())

    def save():
        pending = out / 'progress.pending.json'
        pending.write_text(json.dumps(progress), encoding='utf-8')
        pending.replace(out / 'progress.json')

    save()
    S3._init3(out, campaign, C.GRID_V5)
    S2.S['spoc_by_sector'] = {s: str(p) for s, p in refs.items()}
    best = {(r.tic, r.sector): r.product for r in pd.read_csv(C.BEST).itertuples()}
    by_sector = defaultdict(list)
    for bench, rows in records(guard, campaign).items():
        for row in rows:
            for sector in ([row['sector']] if bench == 'T156' else row['changed']):
                by_sector[row['star'], sector].append((bench, row))
    source = H.DATA / f'stage3_{campaign}' / f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
    sectors = defaultdict(list)
    for kind in ('groups', 'groups_sap'):
        for path in sorted((source / kind).glob('*.json')):
            star, sector = map(int, path.stem.split('_'))
            if str(star) not in guard.seen[campaign]:
                continue
            guard.allow_design_file(path)
            previous = json.loads(path.read_text(encoding='utf-8'))
            files = []
            for meta in previous['meta']:
                file = H.DATA / campaign / str(star) / Path(meta['file'].removesuffix(T.SUFFIX)).name
                guard.allow_design_file(file)
                files.append(str(file) + (T.SUFFIX if kind == 'groups_sap' else ''))
            sectors[star, sector].append((kind, files, previous))
    raw_load, raw_prepare = S2.load, S2.prepare
    raw, prepared = {}, {}
    active, sign, depth = [], 0, 0.
    counts = Counter()
    affected, identity, coverage, support_rows = [], [], [], []
    roster = json.loads((H.OUT / 'roster.json').read_text(encoding='utf-8'))
    roster_ids = {r['trial'] for r in roster if r['campaign'] == campaign}

    def load(path, info=False):
        key = str(path), T.MODE['sap'], T.MODE['pdc'], info, Q.ENABLED
        if key not in raw:
            raw[key] = raw_load(path, info=info)
        result = raw[key]
        if not sign:
            return result
        t, f = result[:2]
        f = f.copy()
        for center, duration in active:
            shape = np.clip((duration / 2 - np.abs(t - center)) / (.1 * duration), 0, 1)
            f -= sign * depth * shape
        return t, f, *result[2:]

    def prepare(path):
        key = str(path)
        if key not in prepared:
            try:
                prepared[key] = raw_prepare(path)
            except Exception:
                counts['preparation_exceptions'] += 1
                raise
            data, meta = prepared[key]
            counts['prepare_' + str(meta.get('status'))] += 1
        return prepared[key]

    S2.load, S2.prepare = load, prepare

    def generate(destination, products, star, sector, compare=False):
        prepared.clear()
        for kind, files, previous in products:
            S2.GROUPS = destination / kind
            S2.GROUPS.mkdir(parents=True, exist_ok=True)
            path = Path(S3.do_group3((star, sector, files)))
            if kind == 'groups_sap':
                S3.add_pdc((path, [p.removesuffix(T.SUFFIX) for p in files], best.get((star, sector))))
            group = json.loads(path.read_text(encoding='utf-8'))
            assert not any(str(m.get('status')).startswith('ERROR') for m in group['meta'])
            if compare:
                canon = lambda es: sorted(json.dumps(e, sort_keys=True) for e in es)
                assert canon(group['events']) == canon(previous['events']), 'Untouched event identity failed'
                assert [m.get('status') for m in group['meta']] == [m.get('status') for m in previous['meta']]
                identity.append(dict(star=star, sector=sector, kind=kind))
            counts['generated_groups'] += 1

    identity_sectors = 0
    try:
        for number, ((star, sector), products) in enumerate(sorted(sectors.items())):
            raw.clear()
            prepared.clear()
            sign, active = 0, []
            for file in (H.DATA / campaign / str(star)).glob('*.fits'):
                guard.allow_design_file(file)
            changed = False
            file_changes = []
            for kind, files, previous in products:
                for file in files:
                    for mode in ('sap', 'pdc') if kind == 'groups_sap' else ('normal',):
                        T.MODE.update(sap=mode == 'sap', pdc=mode == 'pdc')
                        bare = file.removesuffix(T.SUFFIX)
                        Q.ENABLED = False
                        old = load(bare, info=True)
                        Q.ENABLED = True
                        new = load(bare, info=True)
                        different = not (np.array_equal(old[0], new[0]) and np.array_equal(old[1], new[1], equal_nan=True))
                        changed |= different
                        file_changes.append(dict(file=Path(bare).name, mode=mode, changed=different,
                                                 before=len(old[0]), after=len(new[0])))
            T.MODE.update(sap=False, pdc=False)
            Q.ENABLED = True
            coverage.append(dict(star=star, sector=sector, changed=changed, files=file_changes))
            if not changed:
                counts['unchanged_star_sectors'] += 1
                if identity_sectors < 25:
                    generate(out / 'identity', products, star, sector, compare=True)
                    identity_sectors += 1
                continue
            affected.append([star, sector])
            generate(out / 'background', products, star, sector)
            if smoke:
                break
            for bench, row in by_sector[star, sector]:
                active = [(row['time'], row['duration_h'] / 24)] if bench == 'T156' else row['observed']
                depth = row['depth_ppm'] * 1e-6
                for sign in (1, -1):
                    generate(out / bench / f'trial-{row["trial"]}' / str(sign), products, star, sector)
                    if bench == 'T156' and row['trial'] in roster_ids and sign == 1:
                        support = []
                        for kind, files, previous in products:
                            if kind != 'groups':
                                continue
                            for file, meta in zip(files, previous['meta']):
                                if meta.get('product') != row['product']:
                                    continue
                                data, status = prepare(file)
                                times = data['t'] if data is not None else np.array([])
                                Q.ENABLED = False
                                original = load(file, info=True)[0]
                                Q.ENABLED = True
                                cadence = np.median(np.diff(original)) if len(original) > 1 else np.nan
                                support.append(dict(status=status.get('status'), product=meta.get('product'),
                                    searched=bool(len(times) and np.min(np.abs(times - row['time'])) <= 1.5 * cadence)))
                        support_rows.append(dict(trial=row['trial'], support=support))
                counts[f'{bench}_sector_trials'] += 1
            sign = 0
            progress.update(done=number + 1, total=len(sectors), affected=len(affected))
            save()
        result = dict(campaign=campaign, counts=dict(counts), affected=affected, identity=identity,
                      identity_sectors=identity_sectors, coverage=coverage, support=support_rows)
        (out / 'counts.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        progress['status'] = 'complete'
        print(campaign, dict(counts), 'complete', flush=True)
    except Exception:
        progress['status'] = 'failed'
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('campaign', choices=('g2', 'g3'))
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    main(args.campaign, args.smoke)
