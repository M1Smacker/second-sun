"""Generate subtraction background and raw-injection replays on design stars."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('024_harness')


def read_old(guard, path, brief):
    if not path.resolve().is_relative_to(guard.data / 'astra' / brief):
        raise PermissionError('Historical input outside expected brief')
    guard.reads.add(path.resolve())
    return json.loads(path.read_text(encoding='utf-8'))


def records(guard, campaign):
    result = {'planets': [], 'T156': []}
    for path in sorted((H.DATA / 'astra/006').glob(f'planet-*-*-*-{campaign}/results.jsonl')):
        guard.reads.add(path.resolve())
        result['planets'].extend(json.loads(line) for line in path.read_text(encoding='utf-8').splitlines())
    for path in sorted((H.DATA / 'astra/003').glob(f'workers/{campaign}-*/results-*.jsonl')):
        guard.reads.add(path.resolve())
        result['T156'].extend(json.loads(line) for line in path.read_text(encoding='utf-8').splitlines())
    for rows in result.values():
        assert len(rows) == len({r['trial'] for r in rows})
        assert all(str(r['star']) in guard.seen[campaign] for r in rows)
    return result


def main(campaign, smoke=False, coverage_only=False, empty_mask=False):
    os.environ.update(SS_SET=campaign, VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    refs = guard.allow_machine_inputs(campaign)
    import numpy as np
    import pandas as pd
    import stage2_search as S2
    import stage3 as S3
    import stage3_core as C
    import petrova_mask as PM
    import sap_twin as T
    from astropy.io import fits
    subtraction = importlib.import_module('024_subtract')
    out = H.OUT / (f'empty-{campaign}' if empty_mask else f'coverage-{campaign}' if coverage_only else f'smoke-{campaign}' if smoke else f'generated-{campaign}')
    out.mkdir(exist_ok=True)
    started = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', started=started.isoformat(),
                    expected_finish=(started + timedelta(hours=1)).isoformat())
    (out / 'progress.json').write_text(json.dumps(progress), encoding='utf-8')
    S3._init3(out, campaign, C.GRID_V5)
    S2.S['spoc_by_sector'] = {s: str(p) for s, p in refs.items()}
    targets = pd.read_csv(H.TARGETS, comment='#')
    targets = targets[(targets['list'] == campaign) & (targets.design_seen == 1)].drop_duplicates('tic')
    periods = targets.set_index('tic').p_bin_d.to_dict()
    best = {(r.tic, r.sector): r.product for r in pd.read_csv(C.BEST).itertuples()}
    jobs = records(guard, campaign)
    by_sector = defaultdict(list)
    for bench, rows in jobs.items():
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
    raw_load, raw_prepare, raw_mask = S2.load, S2.prepare, PM.mask_runs
    raw, prepared, traces = {}, {}, {}
    sign, depth, enabled = 0, 0., True
    active = []
    current = None
    stats = Counter()
    affected, scatter, controls, identities, coverage = [], [], [], [], []
    control_stars = set()
    coverage_keys = set()
    if coverage_only or empty_mask:
        audit = json.loads((H.OUT / f'coverage-audit-{campaign}.json').read_text(encoding='utf-8'))
        coverage_keys = {tuple(key) for key in audit['empty_mask_uncertain' if empty_mask else 'uncertain']}

    def load(path, info=False):
        key = (str(path), T.MODE['sap'], T.MODE['pdc'], info)
        if key not in raw:
            raw[key] = raw_load(path, info=info)
        row = raw[key]
        if not sign:
            return row
        t, f = row[:2]
        f = f.copy()
        for center, duration in active:
            shape = np.clip((duration / 2 - np.abs(t - center)) / (.1 * duration), 0, 1)
            f -= sign * depth * shape
        return t, f, *row[2:]

    def prepare(path):
        nonlocal current
        current = str(path)
        if current not in prepared:
            prepared[current] = raw_prepare(path)
        return prepared[current]

    def mask(t, f, catalogue_periods, star):
        result = raw_mask(t, f, catalogue_periods, star)
        times, flux = result[:2]
        if not len(times):
            return result
        corrected, meta = subtraction.correct(times, flux, periods[int(star)], float(t.min()), float(np.ptp(t)))
        if not sign:
            mirror, _ = subtraction.correct(times, 2 - flux, periods[int(star)], float(t.min()), float(np.ptp(t)))
            error = float(np.max(np.abs(corrected + mirror - 2)))
            if error > 2e-14:
                raise RuntimeError('Real-light subtraction inversion failed')
            meta['symmetry_error'] = error
        traces[current] = dict(meta, t=times, before=flux, after=corrected)
        return (times, corrected if enabled else flux, *result[2:])

    S2.load, S2.prepare, PM.mask_runs = load, prepare, mask

    def groups(destination, products, star, sector):
        prepared.clear()
        for kind, files, previous in products:
            S2.GROUPS = destination / kind
            S2.GROUPS.mkdir(parents=True, exist_ok=True)
            path = Path(S3.do_group3((star, sector, files)))
            if kind == 'groups_sap':
                S3.add_pdc((path, [p.removesuffix(T.SUFFIX) for p in files], best.get((star, sector))))
            saved = json.loads(path.read_text(encoding='utf-8'))
            if any(str(m.get('status')).startswith('ERROR') for m in saved['meta']):
                raise RuntimeError('Pipeline preparation reported an error')
            if not enabled:
                canonical = lambda es: sorted(json.dumps(e, sort_keys=True) for e in es)
                if canonical(saved['events']) != canonical(previous['events']):
                    raise RuntimeError('Disabled subtraction identity mismatch')
                identities.append(dict(star=star, sector=sector, kind=kind))
            stats['generated_groups'] += 1

    for number, ((star, sector), products) in enumerate(sorted(sectors.items())):
        if (coverage_only or empty_mask) and (star, sector) not in coverage_keys:
            continue
        raw.clear()
        prepared.clear()
        traces.clear()
        sign = 0
        active = []
        for file in (H.DATA / campaign / str(star)).glob('*.fits'):
            guard.allow_design_file(file)
        # Header time span is an upper bound on all subsequently retained cadences.
        # It saves loading products that cannot possibly have three full cycles.
        possible = False
        for kind, files, previous in products:
            for file in files:
                path = file.removesuffix(T.SUFFIX)
                with fits.open(path, memmap=False) as hdus:
                    starts = [h.header.get('TSTART') for h in hdus]
                    stops = [h.header.get('TSTOP') for h in hdus]
                bounds = [(a, b) for a, b in zip(starts, stops) if a is not None and b is not None]
                if not bounds or any(b - a >= 3 * periods[star] for a, b in bounds):
                    possible = True
        stats['star_sectors_total'] += 1
        if not possible and not 5 <= periods[star] < 10:
            stats['star_sectors_header_skip'] += 1
            coverage.append(dict(star=star, sector=sector, period=periods[star], status='fewer_than_three_cycles'))
            continue
        for kind, files, previous in products:
            for file in files:
                prepare(file)
        for trace in traces.values():
            stats[f'product_{trace["status"]}'] += 1
        changed = any(not np.array_equal(v['before'], v['after']) for v in traces.values())
        coverage.append(dict(star=star, sector=sector, period=periods[star],
                             status='changed' if changed else 'unchanged',
                             products=[{k: v for k, v in trace.items() if k not in ('t', 'before', 'after')}
                                       for trace in traces.values()]))
        for file, trace in traces.items():
            if file.endswith(T.SUFFIX_PDC):
                continue
            before, after = trace['before'], trace['after']
            scatter.append(dict(star=star, sector=sector, file=Path(file).name,
                                before=float(np.std(before)), after=float(np.std(after)),
                                bins=trace['bins'], status=trace['status'],
                                symmetry_error=trace.get('symmetry_error')))
        if not changed and not (coverage_only or empty_mask):
            stats['star_sectors_coverage_skip'] += 1
            continue
        affected.append([star, sector])
        if len(identities) < 4:
            enabled = False
            groups(out / 'identity', products, star, sector)
            enabled = True
        groups(out / 'background', products, star, sector)
        if not (coverage_only or empty_mask) and campaign == 'g2' and len(control_stars) < 20 and star not in control_stars:
            chosen = next((file for kind, files, old in products for file, meta in zip(files, old['meta'])
                           if meta.get('product') == best.get((star, sector)) and file in traces
                           and traces[file]['status'] == 'applied' and traces[file]['bins'] > 1), None)
            if chosen:
                sign = 0
                prepared.clear()
                d0, _ = prepare(chosen)
                trace0 = {key: value.copy() if hasattr(value, 'copy') else value for key, value in traces[chosen].items()}
                raw_t = load(chosen, info=True)[0]
                origin = float(raw_t.min())
                period = periods[star]
                active = [(origin + (.25 + k) * period, 8 / 24)
                          for k in range(int(np.ptp(raw_t) / period) + 2)]
                sign, depth = 1, .004
                prepared.clear()
                d1, _ = prepare(chosen)
                trace1 = traces[chosen]
                def amplitude(t0, f0, t1, f1):
                    common, a, b = np.intersect1d(t0, t1, return_indices=True)
                    shape = np.zeros(len(common))
                    for c, duration in active:
                        shape += np.clip((duration / 2 - np.abs(common - c)) / (.1 * duration), 0, 1)
                    difference = f1[b] - f0[a]
                    off = shape == 0
                    baseline = np.median(difference[off]) if off.any() else 0
                    return float(-np.sum(shape * (difference - baseline)) / np.sum(shape ** 2) / depth) if np.sum(shape ** 2) else None
                dt0, df0 = S2.detrend(d0['t'], d0['f'])
                dt1, df1 = S2.detrend(d1['t'], d1['f'])
                controls.append(dict(star=star, sector=sector,
                    after_mask=amplitude(trace0['t'], trace0['before'], trace1['t'], trace1['before']),
                    after_subtraction=amplitude(trace0['t'], trace0['after'], trace1['t'], trace1['after']),
                    after_detrending=amplitude(dt0, df0, dt1, df1)))
                control_stars.add(star)
                sign = 0
        if smoke:
            break
        for bench, row in by_sector[star, sector]:
            active = [(row['time'], row['duration_h'] / 24)] if bench == 'T156' else row['observed']
            depth = row['depth_ppm'] * 1e-6
            for sign in (1, -1):
                groups(out / bench / f'trial-{row["trial"]}' / str(sign), products, star, sector)
            stats[f'{bench}_sector_trials'] += 1
        sign = 0
        progress.update(done=number + 1, total=len(sectors))
        (out / 'progress.json').write_text(json.dumps(progress), encoding='utf-8')
    result = dict(campaign=campaign, counts=dict(stats), affected=affected, scatter=scatter,
                  controls=controls, identity=identities, coverage=coverage)
    (out / 'counts.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    progress.update(status='complete', finished=datetime.now(timezone(timedelta(hours=3))).isoformat())
    (out / 'progress.json').write_text(json.dumps(progress), encoding='utf-8')
    print(campaign, dict(stats), 'complete', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('campaign', choices=('g2', 'g3'))
    parser.add_argument('--smoke', action='store_true')
    parser.add_argument('--coverage-only', action='store_true')
    parser.add_argument('--empty-mask', action='store_true')
    args = parser.parse_args()
    main(args.campaign, args.smoke, args.coverage_only, args.empty_mask)
