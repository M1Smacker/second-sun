"""Independent counts, star-bootstrap intervals and background blind-spot screens."""
from collections import Counter
import csv
import importlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('023_inputs')
H = D.H
O = importlib.import_module('023_outputs')
CONFIGS = ('B', 'B+C96', 'B+DS', 'B+C96+DS', 'B+C96+M1',
           'B+C96+M2', 'B+C96+DS+M1', 'B+C96+DS+M2')
SEED = 2026111523


def metric(rows, np):
    keys = sorted({(row['campaign'], row['star']) for row in rows})
    position = {key: i for i, key in enumerate(keys)}
    denominator = np.zeros((len(keys), 5), dtype=int)
    successes = np.zeros((len(keys), 5, 2, 8), dtype=int)
    transitions = np.zeros((5, 2, 8, 2), dtype=int)
    for row in rows:
        i = position[row['campaign'], row['star']]
        b = row['bin']
        denominator[i, b] += 1
        for arm, name in enumerate(('real', 'flip')):
            values = np.array(row[name], dtype=bool)
            successes[i, b, arm] += values
            transitions[b, arm, :, 0] += ~values[0] & values
            transitions[b, arm, :, 1] += values[0] & ~values
    counts = successes.sum(axis=0)
    n = denominator.sum(axis=0)
    rates = (counts / n[:, None, None]).mean(axis=0)
    rng = np.random.default_rng(SEED)
    samples = []
    while len(samples) < 10000:
        weights = rng.multinomial(len(keys), np.full(len(keys), 1 / len(keys)), size=200)
        den = weights @ denominator
        valid = (den > 0).all(axis=1)
        recovered = (weights[valid] @ successes.reshape(len(keys), -1)).reshape(-1, 5, 2, 8)
        samples.extend(recovered / den[valid, :, None, None])
    samples = np.asarray(samples[:10000])
    paired = np.quantile(samples[:, :, 0] - samples[:, :, 1], [.005, .995], axis=0).transpose(1, 2, 0)
    assert np.array_equal(counts - counts[:, :, [0]], transitions[:, :, :, 0] - transitions[:, :, :, 1])
    return dict(stars=len(keys), n=n.tolist(), counts=counts.tolist(), rates=rates.tolist(),
                rate95=np.quantile(samples.mean(axis=1), [.025, .975], axis=0).tolist(),
                moves=transitions.tolist(), paired99=paired.tolist(),
                paired_pass=((paired[:, :, 0] <= 0) & (paired[:, :, 1] >= 0)).all(axis=0).tolist())


def main():
    import os
    os.environ.update(SS_SET='g2', VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    guard.allow_machine_inputs('g2')
    guard.allow_machine_inputs('g3')
    import numpy as np
    import petrova_mask as PM

    combined = {}
    background = [[] for _ in CONFIGS]
    for bench in ('planets', 'T156'):
        rows = {}
        for campaign in ('g2', 'g3'):
            for mode in ('V0', 'V1', 'V2'):
                data = json.loads((H.OUT / f'{bench}-{campaign}-{mode}.json').read_text(encoding='utf-8'))
                indices = [CONFIGS.index(name) for name in data['configs']]
                for source in data['rows']:
                    assert str(source['star']) in guard.seen[campaign]
                    key = campaign, source['trial']
                    if key not in rows:
                        rows[key] = dict(source, real=[None] * 8, flip=[None] * 8)
                    row = rows[key]
                    assert all(row[field] == source[field] for field in ('star', 'bin', 'campaign'))
                    for arm in ('real', 'flip'):
                        for i, value in zip(indices, source[arm]):
                            assert row[arm][i] is None
                            row[arm][i] = value
                if bench == 'planets':
                    for event in data['background']:
                        assert str(event['tic']) in guard.seen[campaign]
                        for i, value in zip(indices, event['options']):
                            if value:
                                background[i].append(dict(event))
        result = sorted(rows.values(), key=lambda r: (r['campaign'], r['trial']))
        assert all(all(v is not None for v in r[arm]) for r in result for arm in ('real', 'flip'))
        assert len(result) == (1098 if bench == 'planets' else 2000)
        assert len({r['trial'] for r in result}) == len(result)
        combined[bench] = result
        O.write_json(H.OUT / f'combined-{bench}.json', result)
    reference = [r for r in combined['T156'] if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]
    assert len(reference) == 222
    planets = metric(combined['planets'], np)
    reference_metric = metric(reference, np)
    all_t156 = metric(combined['T156'], np)

    def read_old(name, brief):
        return json.loads(D.read(guard, H.OUT.with_name(brief) / name, brief))

    old_summary = read_old('summary.json', '013')
    identity = dict(P=planets['rates'][0][0], R=reference_metric['rates'][0][0],
                    real=len([r for r in background[0] if r['kind'] == 'real']),
                    flip=len([r for r in background[0] if r['kind'] == 'flip']))
    assert abs(identity['P'] - old_summary['planets']['rates'][0][1]) < 1e-12
    assert abs(identity['R'] - old_summary['reference']['rates'][0][1]) < 1e-12
    assert [identity['real'], identity['flip']] == [174, 79]
    assert round(identity['P'] * 100, 2) == 48.11
    assert round(identity['R'] * 100, 2) == 34.21
    # Check the independent depth-cap implementation against 014's background pricing.
    cap_counts = [sum(r['kind'] == arm for r in background[1]) for arm in ('real', 'flip')]
    assert cap_counts == [124, 53]
    dump_map = read_old('dump-summary.json', '014')
    dump_refs = read_old('dump-references.json', '014')
    dumps = {int(sector): np.asarray(row['starts']) for sector, row in dump_refs.items()}
    catalogues = {}
    for campaign in ('g2', 'g3'):
        catalogue = PM.load_catalogue(campaign, H.ROOT / f'targets/{campaign}_chain_targets.csv')
        catalogues[campaign] = {star: row for star, row in catalogue.items() if str(star) in guard.seen[campaign]}

    def same_event(a, b):
        return (a['campaign'], a['tic'], a['sector'], a['kind']) == (b['campaign'], b['tic'], b['sector'], b['kind']) and abs(a['center'] - b['center']) <= .1 + max(a['dur_h'], b['dur_h']) / 48

    def eclipse_distance(event, offset):
        catalogue = catalogues[event['campaign']].get(event['tic'])
        if catalogue is None or not math.isfinite(catalogue['wp']) or catalogue['wp'] <= 0 or not math.isfinite(offset):
            return None, None, None
        phase = ((event['center'] - catalogue['T0'] - offset) / catalogue['P']) % 1
        distance = lambda position: abs((phase - position + .5) % 1 - .5) * catalogue['P']
        secondary = math.isfinite(catalogue['phs']) and math.isfinite(catalogue['ws']) and catalogue['ws'] > 0
        return (distance(0) / catalogue['wp'],
                distance(catalogue['phs'] if secondary else .5) / (catalogue['ws'] if secondary else catalogue['wp']),
                not secondary)

    private = []
    table = []
    for i, name in enumerate(CONFIGS):
        counts = Counter((r['campaign'], r['kind'], r['bin']) for r in background[i])
        real = sum(r['kind'] == 'real' for r in background[i])
        flip = len(background[i]) - real
        new = [r for r in background[i] if r['kind'] == 'real' and not any(same_event(r, old) for old in background[0])]
        lost = [r for r in background[0] if r['kind'] == 'real' and not any(same_event(r, old) for old in background[i])]
        screen = Counter()
        for source in new:
            event = dict(source, configuration=name)
            times = dumps.get(event['sector'], np.array([]))
            hours = float(24 * (event['center'] - times[np.argmin(abs(times - event['center']))])) if len(times) else None
            contains = hours is not None and abs(hours) <= event['dur_h'] / 2
            near = hours is not None and (abs(hours) <= 12 or contains)
            precursor = hours is not None and -6 <= hours < -3 and not contains
            primary, secondary, fallback = eclipse_distance(event, 0.)
            offset = event.get('p1_off')
            refit_primary, refit_secondary, refit_fallback = eclipse_distance(event, offset if offset is not None else math.nan)
            raw_leftover = primary is not None and min(primary, secondary) <= 1
            refit_leftover = refit_primary is not None and min(refit_primary, refit_secondary) <= 1
            unknown = hours is None or primary is None or refit_primary is None
            union = near or raw_leftover or refit_leftover
            screen.update(new=1, dump12h=int(near), dump_precursor=int(precursor),
                          eclipse_catalogue=int(raw_leftover), eclipse_refit=int(refit_leftover),
                          eclipse_union=int(raw_leftover or refit_leftover),
                          union=int(union), unknown=int(unknown), worst_union=int(union or unknown),
                          secondary_fallback=int(bool(fallback)))
            event.update(dump_hours=hours, box_contains_dump=contains, dump12h=near,
                         dump_precursor=precursor, primary_widths=primary, secondary_widths=secondary,
                         secondary_fallback=fallback, refit_primary_widths=refit_primary,
                         refit_secondary_widths=refit_secondary, eclipse_catalogue=raw_leftover,
                         eclipse_refit=refit_leftover, conservative_union=union, unknown=unknown)
            private.append(event)
        failures = [b for b in range(5) if not (planets['paired99'][b][i][0] <= 0 <= planets['paired99'][b][i][1])]
        p, lower = planets['rates'][0][i], planets['rate95'][0][0][i]
        rules = dict(a=p >= .5 and lower >= .4, b=flip <= 79, c=not failures, d=real <= 174,
                     e_sufficient=screen['worst_union'] <= 5)
        table.append(dict(configuration=name, P=p, P95=[lower, planets['rate95'][1][0][i]],
                          R=reference_metric['rates'][0][i],
                          R95=[reference_metric['rate95'][0][0][i], reference_metric['rate95'][1][0][i]],
                          real=real, flip=flip, spare=79 - flip, failed_control_bins=failures,
                          new_real=len(new), lost_real=len(lost), screen=dict(screen),
                          background_by_bin={f'{c}:{a}:{b}': n for (c, a, b), n in counts.items()},
                          missing_radius=sum(not r['radius_known'] for r in background[i]),
                          rules=rules, go_sufficient=all(rules.values())))
    output = dict(identity=identity, configurations=table, planets=planets, reference=reference_metric,
                  T156=all_t156, bootstrap_seed=SEED, bootstrap_replicates=10000,
                  replicated_dump_windows=dump_map['replicated'], dump_reference_summary=dump_map['references'])
    O.write_json(H.OUT / 'summary.json', output, indent=2)
    if private:
        with (H.OUT / 'new-real-events.csv').open('w', encoding='utf-8', newline='') as destination:
            writer = csv.DictWriter(destination, fieldnames=list(private[0]))
            writer.writeheader()
            writer.writerows(private)
    for row in table:
        print(row['configuration'], f"P={row['P']:.6f}", f"R={row['R']:.6f}", row['real'], row['flip'],
              'screen', row['screen'], 'rules', row['rules'], flush=True)


if __name__ == '__main__':
    main()
