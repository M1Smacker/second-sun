"""Score fresh 031 quality-policy replays with the adopted 023 scoring rules."""
import argparse
from collections import defaultdict
import csv
import importlib
import json
import math
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('031_inputs')
H = D.H
S = importlib.import_module('023_scoring_rules')
O = importlib.import_module('031_outputs')
CONFIGS = ('B', 'B+C96', 'B+DS', 'K2', 'B+C96+M1',
           'B+C96+M2', 'B+C96+DS+M1', 'B+C96+DS+M2')
INDICES = {'V0': (0, 1, 2, 3), 'V1': (4, 6), 'V2': (5, 7)}
LABELS = ('c5', 'ecl_overlap', 'orbit_lock', 'p1_veto', 'repeater')


def finite(value):
    return value is not None and math.isfinite(value)


def truth(value):
    return bool(value) and value == value


def decision(row, index, rivals, intervals, cap, tier_of):
    """Return adopted B, C96, DS and C96+DS, using one common OAE pool."""
    event = dict(row)
    center = event['center']
    half = event['dur_h'] / 48
    event['dominated'] = any(
        other != index and rival['snr'] >= event['snr']
        and 1.5 * event['dur_h'] / 24 <= abs(center - rival['center']) <= 6.85
        and not any(truth(rival.get(flag)) for flag in LABELS)
        for other, rival in rivals.items()
    )
    known = any(center + half >= start and center - half <= stop
                for start, stop in intervals.get(event['sector'], ()))
    event['gap_dump'] = event['gap_dump'] or known
    baseline = tier_of(event) in S.TIERS
    within_cap = cap is None or event['depth_ppm'] <= cap
    uneven = any(not finite(v) or abs(v) > .25
                 for v in (event.get('lift_pre'), event.get('lift_post')))
    flags = str(event.get('flags') or '')
    event['gap_dump'] = known or 'gap edge' in flags or ('momentum dump' in flags and uneven)
    shaped = tier_of(event) in S.TIERS
    event['gap_dump'] = known or ('momentum dump' in flags and uneven)
    r2 = tier_of(event) in S.TIERS
    return [baseline, baseline and within_cap, shaped, r2 and within_cap]


def hold_details(row, index, rivals, intervals, tier_of, cap):
    event = dict(row)
    event['dominated'] = any(other != index and rival['snr'] >= event['snr']
        and 1.5 * event['dur_h'] / 24 <= abs(event['center'] - rival['center']) <= 6.85
        and not any(truth(rival.get(flag)) for flag in LABELS) for other, rival in rivals.items())
    known = any(event['center'] + event['dur_h']/48 >= a and event['center'] - event['dur_h']/48 <= b
                for a, b in intervals.get(event['sector'], ()))
    text = str(event.get('flags') or '')
    uneven = any(not finite(v) or abs(v) > .25 for v in (event.get('lift_pre'), event.get('lift_post')))
    result = []
    for variant in ('B', 'K2'):
        e = dict(event)
        e['gap_dump'] = (e['gap_dump'] or known) if variant == 'B' else known or ('momentum dump' in text and uneven)
        holds = {f: truth(e.get(f)) for f in ('step', 'ramp', 'repeater', 'dominated')}
        holds.update(dump=('momentum dump' in text and (variant == 'B' or uneven)),
                     gap_edge=('gap edge' in text and variant == 'B'), known=known,
                     cap=(variant == 'K2' and cap is not None and e['depth_ppm'] > cap), tier=tier_of(e))
        result.append(holds)
    return result


def main(campaign, bench, mode, limit=None, baseline_run=False, floor=7.):
    assert mode == 'V0'
    os.environ.update(SS_SET=campaign, VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    guard.allow_machine_inputs(campaign)
    import numpy as np
    import pandas as pd
    import stage3_core as C
    import stage3_report as R
    from detect_v2 import FLIP_D

    strict = bench == 'T156'
    intervals = defaultdict(list)
    with (H.ROOT / 'research/stage3/rs028/known_events.csv').open(encoding='utf-8-sig') as source:
        for row in csv.DictReader(source):
            intervals[int(row['sector'])].append((float(row['start_tjd']) - .1,
                                                  float(row['end_tjd']) + .1))
    assert sum(map(len, intervals.values())) == 19
    target_frame = pd.read_csv(C.TARGETS, comment='#')
    ephemeris = C.Ephem(target_frame, C.eb_widths())
    original_csv = pd.read_csv
    pd.read_csv = lambda p, *a, **kw: target_frame.copy() if p == C.TARGETS else original_csv(p, *a, **kw)
    C.eb_widths = lambda: None
    C.Ephem = lambda *_: ephemeris
    targets = pd.read_csv(H.TARGETS, comment='#')
    allowed = targets[(targets['list'] == campaign) & (targets.design_seen == 1)].drop_duplicates('tic')
    periods = allowed.set_index('tic').p_bin_d.to_dict()
    best = pd.read_csv(C.BEST)[['tic', 'sector', 'product']].rename(columns={'product': 'best'})
    radii = {}
    with (H.ROOT / 'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as source:
        for row in csv.DictReader(source):
            if row['set'] == campaign and row['tic'] in guard.seen[campaign] and row['radius_rsun']:
                radius = float(row['radius_rsun'])
                if finite(radius) and radius > 0:
                    radii[int(row['tic'])] = min(1., (.2009 / radius) ** 2) * 1e6

    def retier(events):
        buckets = defaultdict(list)
        for event in events:
            buckets[event['kind'], event['product']].append(event)
        updates = {}
        for (kind, product), group in buckets.items():
            repeated = S.binary_members(group, periods[group[0]['tic']])
            flips = set()
            if kind == 'flip' and strict:
                flips, uncertain = S.symmetric_matches(buckets.get(('real', product), []), group, FLIP_D)
                if uncertain:
                    raise RuntimeError('Unresolved rounded coincidence')
            real = buckets.get(('real', product), []) if kind == 'flip' and not strict else []
            for i, event in enumerate(group):
                mirrored = i in flips if strict else any(abs(event['center'] - r['center']) < FLIP_D for r in real)
                revised = dict(event, repeater=i in repeated,
                               flipmatch=mirrored if kind == 'flip' else event['flipmatch'])
                temporary = dict(revised)
                temporary.pop('pdc_snr', None)
                revised['tier'] = C.tier_of(temporary)
                updates[id(event)] = revised
        return [updates[id(event)] for event in events]

    def frame(events):
        result = pd.DataFrame(events).merge(best, on=['tic', 'sector'], how='left')
        result['primary'] = result['product'] == result['best']
        result['c8_best'] = pd.to_numeric(result['c8_best'], errors='coerce')
        return result

    def tiers(events):
        return R.apply_v7(R.merge_sap(events.reset_index(drop=True))) if not events.empty else events

    source = H.DATA / f'stage3_{campaign}' / f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
    groups = defaultdict(list)
    cameras = defaultdict(set)
    for kind in D.KINDS:
        paths = (source / kind).glob('*.json')
        if strict:
            paths = sorted(paths)
        for path in paths:
            star, sector = map(int, path.stem.split('_'))
            if star not in periods:
                continue
            guard.allow_design_file(path)
            group = json.loads(path.read_text(encoding='utf-8'))
            assert int(group['tic']) == star and int(group['sector']) == sector
            groups[star, sector].extend(group['events'])
            cameras[star, sector].update(e['camera'] for e in group['events'])
            if (strict or not baseline_run) and kind == 'groups':
                cameras[star, sector].update(m['camera'] for m in group['meta'] if 'camera' in m)
    generated = H.OUT / f'generated-{campaign}'
    coverage = {} if baseline_run else json.loads((generated / 'counts.json').read_text(encoding='utf-8'))
    changed_keys = set() if baseline_run else {tuple(key) for key in coverage['affected']}
    def generation_for(key):
        return generated
    for key in changed_keys:
        assert key in groups
        events = []
        for kind in D.KINDS:
            path = generation_for(key) / 'background' / kind / f'{key[0]}_{key[1]}.json'
            assert path.is_file() == (source / kind / path.name).is_file(), 'Background coverage mismatch'
            if path.exists():
                group = json.loads(path.read_text(encoding='utf-8'))
                assert (group['tic'], group['sector']) == key
                events.extend(group['events'])
        groups[key] = events
    groups = {key: retier(events) for key, events in groups.items()}
    baseline = frame([e for events in groups.values() for e in events])
    context = baseline
    affected = set(map(int, json.loads(D.read(guard, H.OUT.with_name('010') / f'affected-{campaign}.json', '010'))))
    assert affected <= periods.keys()
    planet_folders = {}
    t156_folders = {}
    if mode != 'V0' and affected:
        replaced = defaultdict(list)
        for slot in range(3):
            folder = H.OUT.with_name('010') / f'{mode}-{campaign}-{slot}'
            D.read(guard, folder / 'counts.json', '010')
            for kind in D.KINDS:
                for path in sorted((folder / 'background' / kind).glob('*.json')):
                    key = tuple(map(int, path.stem.split('_')))
                    assert key[0] in affected and key in groups
                    replaced[key].extend(json.loads(D.read(guard, path, '010'))['events'])
            for path in folder.glob('trial-*'):
                trial = int(path.name.split('-')[1])
                assert trial not in planet_folders
                planet_folders[trial] = path
        assert replaced.keys() == {key for key in groups if key[0] in affected}
        context = frame([e for key, events in groups.items()
                         for e in (retier(replaced[key]) if key in replaced else events)])
        if strict:
            for slot in range(5):
                folder = H.OUT.with_name('011') / f't156-{mode.lower()}-{campaign}-{slot}'
                D.read(guard, folder / 'counts.json', '011')
                for path in folder.glob('trial-*'):
                    trial = int(path.name.split('-')[1])
                    assert trial not in t156_folders
                    t156_folders[trial] = path

    def options(events, candidates):
        keys = {(r.tic, r.sector, r.product) for r in candidates.itertuples()}
        pools = {key: group.to_dict('index')
                 for key, group in events.groupby(['tic', 'sector', 'product'], sort=False) if key in keys}
        flags = {}
        for index, row in candidates.to_dict('index').items():
            four = decision(row, index, pools[row['tic'], row['sector'], row['product']],
                            intervals, radii.get(row['tic']), C.tier_of)
            flags[index] = four if mode == 'V0' else [four[1], four[3]]
        return flags

    def passing(events, star, arm, observed):
        candidates = events[(events.tic == star) & events.primary & (events.kind == arm) & (events.snr >= floor)]
        matches = {j: candidates.index[abs(candidates.center - t) <= d / 2]
                   for j, (t, d) in enumerate(observed)}
        indices = sorted({int(i) for ids in matches.values() for i in ids})
        flags = options(events, events.loc[indices])
        hits = [set() for _ in INDICES[mode]]
        for crossing, ids in matches.items():
            for index in ids:
                for option, yes in enumerate(flags[index]):
                    if yes:
                        hits[option].add(crossing)
        return hits

    ranked = tiers(context)
    output = dict(campaign=campaign, bench=bench, mode=mode, configs=[CONFIGS[i] for i in INDICES[mode]],
                  rows=[], background=[], candidates=[], identity_mismatches=0, floor=floor)
    if not strict:
        flags = options(ranked, ranked[ranked.primary & (ranked.snr >= floor)])
        fields = ('tic', 'sector', 'camera', 'kind', 'product', 'center', 'dur_h', 'depth_ppm', 'snr',
                  'lift_pre', 'lift_post', 'flags', 'p1_P', 'p1_T0', 'p1_off')
        diagnostic_pools = {key: g.to_dict('index') for key, g in ranked.groupby(['tic', 'sector', 'product'], sort=False)}
        for index, accepted in flags.items():
            if True:
                event = {field: ranked.loc[index].get(field) for field in fields}
                event.update(options=accepted, campaign=campaign, radius_known=event['tic'] in radii,
                             bin=int(np.searchsorted([10, 14, 20, 27.4], periods[event['tic']], side='right')))
                pool = diagnostic_pools[event['tic'], event['sector'], event['product']]
                event['holds'] = hold_details(ranked.loc[index].to_dict(), index, pool, intervals, C.tier_of, radii.get(event['tic']))
                output['candidates'].append(event)
                if any(accepted):
                    output['background'].append(event)
        records = []
        for journal in sorted(H.OUT.with_name('006').glob(f'planet-*-*-*-{campaign}/results.jsonl')):
            for line in D.read(guard, journal, '006').splitlines():
                record = json.loads(line)
                assert record['star'] in periods
                if record['observed']:
                    records.append((record, journal.parent))
    else:
        records = list(D.t156_rows(guard, campaign))
        if mode != 'V0':
            assert t156_folders.keys() == {r['trial'] for r, _ in records if r['star'] in affected}
    assert len(records) == len({r['trial'] for r, _ in records})
    identity = json.loads(D.read(guard, H.OUT.with_name('013') / f'{bench}-{campaign}.json', '013'))
    identity = {r['trial']: r for r in identity['rows']}
    if mode == 'V0':
        assert identity.keys() == {r['trial'] for r, _ in records}

    k2_identity = None
    if baseline_run and not strict and floor == 7.:
        old = json.loads(D.read(guard, H.OUT.with_name('fable-f4') / f'x6-planets-{campaign}-V0.json', 'fable-f4'))
        col = old['configs'].index('B+C96*R2')
        k2_identity = {r['trial']: {arm: r[arm][col] for arm in ('real', 'flip')} for r in old['rows']}

    for number, (record, folder) in enumerate(records):
        if limit is not None and number >= limit:
            break
        star, trial = record['star'], record['trial']
        assert star in periods
        observed = [(record['time'], record['duration_h'] / 24)] if strict else record['observed']
        sectors = {record['sector']} if strict else set(record['changed'])
        near = np.logical_or.reduce([(context.sector == sec) & context.camera.isin(cameras[star, sec])
                                     for sec in sectors])
        own = context.tic == star
        in_sector = context.sector.isin(sectors)
        # Include newly available camera context introduced by mask variants.
        if mode != 'V0':
            for sec in sectors:
                cams = set(context.loc[(context.tic == star) & (context.sector == sec), 'camera'])
                near |= (context.sector == sec) & context.camera.isin(cams)
        keep = context[(own | near) & ~(own & in_sector)]
        before = tiers(context[(own & in_sector) | near]) if not strict else None
        variant_prior = tiers(context[own | near]) if strict and not baseline_run else None
        result = {key: record[key] for key in ('trial', 'star', 'bin', 'campaign')}
        if strict:
            result.update(depth_ppm=record['depth_ppm'], duration_h=record['duration_h'])
        for sign, arm, label in ((1, 'real', 'dip'), (-1, 'flip', 'bump')):
            revised = []
            for sec in sectors:
                brief = '003' if strict else '006'
                location = folder / (f'trial-{trial}-{sign}' if strict else f'trial-{trial}/{sign}')
                if mode != 'V0' and star in affected:
                    brief = '011' if strict else '010'
                    location = (t156_folders if strict else planet_folders)[trial] / str(sign)
                for kind in D.KINDS:
                    if (star, sec) in changed_keys:
                        location = generation_for((star, sec)) / bench / f'trial-{trial}' / str(sign)
                        brief = '031'
                    path = location / kind / f'{star}_{sec}.json'
                    expected_kind = source / kind / f'{star}_{sec}.json'
                    if (star, sec) in changed_keys and expected_kind.exists():
                        assert path.is_file(), 'Required changed-sector injection replay is missing'
                    if path.is_file():
                        group = json.loads(D.read(guard, path, brief))
                        assert int(group['tic']) == star and int(group['sector']) == sec
                        revised.extend(group['events'])
            filtered = retier(revised)
            after = tiers(pd.concat([keep, frame(filtered)] if filtered else [keep], ignore_index=True))
            if strict:
                after = after[after.sector == record['sector']]
            hits = passing(after, star, arm, observed) if strict or revised else [set() for _ in INDICES[mode]]
            if strict:
                prior = [{0} if record[label]['preexisting'] else set() for _ in INDICES[mode]]
                if variant_prior is not None:
                    extra = passing(variant_prior[variant_prior.sector == record['sector']], star, arm, observed)
                    prior = [a | b for a, b in zip(prior, extra)]
            else:
                prior = passing(before, star, arm, observed)
            result[arm] = [bool(hit - pre) for hit, pre in zip(hits, prior)]
            detected = after[(after.tic == star) & after.primary & (after.kind == arm) & (after.snr >= floor)]
            result[arm + '_found'] = any(abs(event.center - center) <= duration / 2
                                       for event in detected.itertuples() for center, duration in observed)
            if baseline_run and floor == 7.:
                expected = identity[trial][arm]
                assert result[arm][0] == expected[1], f'{bench} B identity differs at private trial'
                assert result[arm][2] == expected[2], f'{bench} DS identity differs at private trial'
        if k2_identity is not None:
            assert all(result[arm][3] == k2_identity[trial][arm] for arm in ('real', 'flip')), 'K2 identity differs'
        output['rows'].append(result)
    suffix = ('-smoke' if limit is not None else '') + (f'-floor{floor:g}' if floor != 7. else '')
    O.write_json(H.OUT / f'{"baseline-" if baseline_run else ""}{bench}-{campaign}-{mode}{suffix}.json', output,
                 default=lambda value: value.item() if isinstance(value, np.generic) else str(value))
    print(campaign, bench, mode, len(output['rows']), 'historical identity verified' if baseline_run else 'candidate scored', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('campaign', choices=('g2', 'g3'))
    parser.add_argument('bench', choices=('planets', 'T156'))
    parser.add_argument('mode', choices=('V0', 'V1', 'V2'))
    parser.add_argument('--limit', type=int)
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--floor', type=float, default=7.)
    arguments = parser.parse_args()
    main(arguments.campaign, arguments.bench, arguments.mode, arguments.limit, arguments.baseline, arguments.floor)
