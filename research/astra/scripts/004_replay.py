"""Replay saved events with one flag changed. Run with Python -I -B."""
import argparse
from collections import Counter, defaultdict
from itertools import combinations
import importlib
import json
import math
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('004_harness')
T156 = H.OUT.with_name('003')
TIERS = {'1A', '1L', '1B'}


def binary_members(events, period):
    if not math.isfinite(period) or period <= 0:
        return set(range(len(events))) if len(events) >= 3 else set()

    def locked(a, b):
        separation = abs(a['center'] - b['center'])
        cycles = round(separation / period)
        return cycles >= 1 and abs(separation - cycles * period) <= 1 / 24

    members = set()
    for triple in combinations(range(len(events)), 3):
        if all(locked(events[a], events[b]) for a, b in combinations(triple, 2)):
            members.update(triple)
    return members


def symmetric_matches(real, flips, radius):
    """Recover reverse matches using the saved forward flags at rounding boundaries."""
    matched, possible = set(), set()
    uncertainty = .0001000001
    for event in real:
        distances = [abs(event['center'] - flip['center']) for flip in flips]
        certain = {i for i, d in enumerate(distances) if d < radius - uncertainty}
        boundary = {i for i, d in enumerate(distances) if abs(d - radius) <= uncertainty}
        if not event['flipmatch']:
            if certain:
                raise RuntimeError('Saved forward coincidence flag contradicts candidate distances')
            continue
        if not certain and not boundary:
            raise RuntimeError('Saved forward coincidence has no possible partner')
        if not certain and len(boundary) == 1:
            certain = boundary
        else:
            possible.update(boundary)
        matched.update(certain)
    return matched, possible - matched


def main(campaign, variant):
    os.environ.update(SS_SET=campaign, VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    if T156.resolve() != guard.data / 'astra' / '003':
        raise PermissionError('T156 source escapes its expected directory')
    print('READ saved design-only T156 journals and groups:', T156, flush=True)
    guard.allow_machine_inputs(campaign)
    import numpy as np
    import pandas as pd
    import stage3_core as C
    import stage3_report as R
    from detect_v2 import FLIP_D

    best = pd.read_csv(C.BEST)[['tic', 'sector', 'product']].rename(columns={'product': 'best'})
    # The frozen reporter rebuilds the same ephemeris on every call. Reuse it.
    ephemeris = C.Ephem(pd.read_csv(C.TARGETS, comment='#'), C.eb_widths())
    original_ephem = C.Ephem
    original_widths = C.eb_widths
    original_csv = pd.read_csv

    def cached_csv(path, *args, **kwargs):
        return target_frame.copy() if path == C.TARGETS else original_csv(path, *args, **kwargs)

    target_frame = pd.read_csv(C.TARGETS, comment='#')
    pd.read_csv = cached_csv
    C.eb_widths = lambda: None
    C.Ephem = lambda *_: ephemeris
    periods = pd.read_csv(H.TARGETS, comment='#')
    periods = periods[(periods['list'] == campaign) & (periods.design_seen == 1)].drop_duplicates('tic')
    period_by_star = dict(zip(periods.tic, periods.p_bin_d))
    source = H.DATA / f'stage3_{campaign}' / f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
    check = Counter()

    def read_private(path):
        resolved = path.resolve(strict=True)
        if resolved != guard.data / path.relative_to(H.DATA) or not resolved.is_relative_to(T156.resolve()):
            raise PermissionError('T156 path escape')
        guard.reads.add(resolved)
        return path.read_text(encoding='utf-8')

    def audit_and_change(events):
        partitions = defaultdict(list)
        for row in events:
            partitions[row['kind'], row['product']].append(row)
        changed = []
        for (kind, product), group in partitions.items():
            members = binary_members(group, period_by_star.get(group[0]['tic'], math.nan)) if variant == 'repeater' else set()
            if variant == 'fix91' and kind == 'flip':
                members, uncertain = symmetric_matches(partitions.get(('real', product), []), group, FLIP_D)
                check['ambiguous_fix91'] += len(uncertain)
            for index, row in enumerate(group):
                expected = dict(row, repeater=len(group) >= C.REPEAT_N)
                # SAP's pdc_snr was attached after writing the original stage-3 tier.
                expected.pop('pdc_snr', None)
                if C.tier_of(expected) != row['tier'] or expected['repeater'] != row['repeater']:
                    raise RuntimeError('Stored pre-union tier or repeater mismatch')
                check['stored_tiers'] += 1
                update = dict(row)
                if variant == 'repeater':
                    update['repeater'] = index in members
                elif kind == 'flip':
                    update['flipmatch'] = index in members
                if update != row:
                    check['flag_changes'] += 1
                tier_input = dict(update)
                tier_input.pop('pdc_snr', None)
                update['tier'] = C.tier_of(tier_input)
                changed.append((row, update))
        # Preserve input ordering for SAP association's first-match semantics.
        by_identity = {id(old): new for old, new in changed}
        return [by_identity[id(row)] for row in events]

    def frame(events):
        result = pd.DataFrame(events).merge(best, on=['tic', 'sector'], how='left')
        result['primary'] = result['product'] == result['best']
        result['c8_best'] = pd.to_numeric(result['c8_best'], errors='coerce')
        return result

    groups = defaultdict(list)
    cameras = defaultdict(set)
    for kind in ('groups', 'groups_sap'):
        for path in sorted((source / kind).glob('*.json')):
            star, sector = path.stem.split('_')
            if star not in guard.seen[campaign]:
                continue
            guard.allow_design_file(path)
            group = json.loads(path.read_text(encoding='utf-8'))
            key = int(star), int(sector)
            groups[key].extend(group['events'])
            cameras[key].update(row['camera'] for row in group['events'])
            if kind == 'groups':
                cameras[key].update(m['camera'] for m in group['meta'] if 'camera' in m)
            check['baseline_group_files'] += 1
    changes = {key: audit_and_change(events) for key, events in groups.items()}
    old_context = frame([event for group in groups.values() for event in group])
    new_context = frame([event for group in changes.values() for event in group])

    def tier(df):
        return R.apply_v7(R.merge_sap(df.reset_index(drop=True)))

    def background(df):
        output = tier(df)
        return output[output.primary & output.tier.isin(TIERS) & (output.snr >= 7)].kind.value_counts().to_dict()

    bg_old, bg_new = background(old_context), background(new_context)
    print('Baseline groups loaded and stored tiers checked', check['baseline_group_files'], flush=True)
    results = []
    for journal in sorted((T156 / 'workers').glob(f'{campaign}-*/results-*.jsonl')):
        for line in read_private(journal).splitlines():
            trial = json.loads(line)
            star, sector = trial['star'], trial['sector']
            if str(star) not in guard.seen[campaign] or trial['campaign'] != campaign:
                raise PermissionError('Journal trial outside allowed design stars')
            key = star, sector
            contexts = []
            for context in (old_context, new_context):
                own = (context.tic == star) & (context.sector == sector)
                near = (context.sector == sector) & context.camera.isin(cameras[key])
                contexts.append(context[((context.tic == star) | near) & ~own])
            result = {k: trial[k] for k in ('trial', 'bin', 'star', 'campaign', 'depth_ppm', 'duration_h')}
            for sign, label, arm in ((1, 'dip', 'real'), (-1, 'bump', 'flip')):
                events = []
                folder = journal.parent / f'trial-{trial["trial"]}-{sign}'
                for kind in ('groups', 'groups_sap'):
                    path = folder / kind / f'{star}_{sector}.json'
                    if kind == 'groups' or path.exists():
                        events.extend(json.loads(read_private(path))['events'])
                updated = audit_and_change(events)
                pair = []
                for context, candidates in zip(contexts, (events, updated)):
                    combined = pd.concat([context, frame(candidates)] if candidates else [context], ignore_index=True)
                    if combined.empty:
                        pair.append(False)
                        continue
                    scored = tier(combined)
                    matched = scored[(scored.tic == star) & (scored.sector == sector) & (scored.kind == arm)
                                     & (np.abs(scored.center - trial['time']) <= trial['duration_h'] / 48)]
                    pair.append(bool((matched.primary & matched.tier.isin(TIERS) & (matched.snr >= 7)).any())
                                and not trial[label]['preexisting'])
                if pair[0] != trial[label]['recovered']:
                    raise RuntimeError('Saved final recovery decision mismatch')
                check['final_recovery_decisions'] += 1
                result[label] = pair
            results.append(result)
            if len(results) % 100 == 0:
                print('Replayed paired trials:', len(results), flush=True)
    if check['ambiguous_fix91']:
        raise RuntimeError(f'FIX 91 has {check["ambiguous_fix91"]} rounded-centre boundary cases')
    pd.read_csv, C.Ephem, C.eb_widths = original_csv, original_ephem, original_widths
    output = dict(check=check, background_old=bg_old, background_new=bg_new, trials=results)
    (H.OUT / f'{variant}-{campaign}.json').write_text(json.dumps(output), encoding='utf-8')
    print(json.dumps(dict(check=check, trials=len(results))), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('campaign', choices=['g2', 'g3'])
    parser.add_argument('variant', choices=['repeater', 'fix91'])
    args = parser.parse_args()
    main(args.campaign, args.variant)
