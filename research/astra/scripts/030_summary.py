"""Independent paired recount and whole-star bootstrap. No pipeline import."""
from collections import Counter, defaultdict
import csv
import importlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('030_inputs')
H = D.H
SEED = 2026111830


def metric(rows, np):
    stars = sorted({r['star'] for r in rows})
    index = {star: i for i, star in enumerate(stars)}
    den = np.zeros((len(stars), 5), dtype=int)
    hits = np.zeros((len(stars), 5, 4), dtype=int)
    for r in rows:
        i, b = index[r['star']], r['bin']
        den[i, b] += 1
        hits[i, b] += [r['B_real'], r['B_flip'], r['N1_real'], r['N1_flip']]
    n = den.sum(0)
    assert (n > 0).all()
    rates = hits.sum(0) / n[:, None]
    rng = np.random.default_rng(SEED)
    draws = []
    while len(draws) < 10000:
        weights = rng.multinomial(len(stars), np.full(len(stars), 1/len(stars)), size=200)
        denominator = weights @ den
        valid = (denominator > 0).all(1)
        numerator = (weights[valid] @ hits.reshape(len(stars), -1)).reshape(-1, 5, 4)
        draws.extend(numerator / denominator[valid, :, None])
    draws = np.asarray(draws[:10000])
    pooled = draws.mean(1)
    control = np.quantile(draws[:, :, 2] - draws[:, :, 3], [.005, .995], axis=0)
    crossing_counts = [dict(n=sum(r['n_crossings'] for r in rows if r['bin'] == b),
                           real=sum(len(r['real_crossings']) for r in rows if r['bin'] == b),
                           flip=sum(len(r['flip_crossings']) for r in rows if r['bin'] == b)) for b in range(5)]
    return dict(n=len(rows), hosts=len(stars), n_by_bin=n.tolist(), counts_by_bin=hits.sum(0).tolist(),
                rates=rates.mean(0).tolist(), rates_by_bin=rates.tolist(),
                rate95=np.quantile(pooled, [.025, .975], axis=0).tolist(),
                gain=float((rates[:, 2]-rates[:, 0]).mean()),
                gain95=np.quantile(pooled[:, 2]-pooled[:, 0], [.025, .975]).tolist(),
                control99=control.tolist(), control_pass=bool(((control[0] <= 0) & (control[1] >= 0)).all()),
                N1_crossings_by_bin=crossing_counts,
                N1_crossing_rate=sum(r['real'] for r in crossing_counts)/sum(r['n'] for r in crossing_counts))


def same(a, b):
    return all(a[k] == b[k] for k in ('campaign', 'tic', 'sector', 'kind')) and abs(a['center']-b['center']) <= .1+max(a['dur_h'], b['dur_h'])/48


def main():
    guard = H.Guard()
    guard.start()
    import numpy as np
    choice = json.loads((H.OUT / 'chosen.json').read_text(encoding='utf-8'))
    floor = choice['threshold']
    assert floor is not None
    suffix = f'-floor{floor:g}' if floor != 7 else ''
    radii, tmag = {}, {}
    with (H.ROOT / 'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['set'] not in guard.seen or r['tic'] not in guard.seen[r['set']]:
                continue
            try:
                radius = float(r['radius_rsun'])
            except ValueError:
                continue
            if math.isfinite(radius) and radius > 0:
                radii[r['set'], int(r['tic'])] = radius
    with H.TARGETS.open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(line for line in f if not line.startswith('#')):
            if r['list'] in guard.seen and r['tic'] in guard.seen[r['list']]:
                try:
                    tmag[r['list'], int(r['tic'])] = float(r.get('tmag', 'nan'))
                except ValueError:
                    pass
    combined, documents = {}, {}
    for phase, brief in (('planets', '006'), ('fresh', 'fable-fresh'), ('T156', '003')):
        combined[phase] = []
        for c in ('g2', 'g3'):
            if phase == 'fresh':
                old = json.loads(D.read(guard, H.OUT.with_name('fable-f4') / f'x1-planets-{c}-V0.json', 'fable-f4'))
                bcol = old['configs'].index('B')
                key = 'planets'
            else:
                old = json.loads((H.OUT / f'baseline-{phase}-{c}-V0.json').read_text(encoding='utf-8'))
                bcol, key = 0, phase
            new = json.loads((H.OUT / f'{key}-{c}-V0{"-fresh" if phase == "fresh" else ""}{suffix}.json').read_text(encoding='utf-8'))
            records = dict()
            if phase == 'T156':
                records = {r['trial']: r for r, _ in D.t156_rows(guard, c)}
            else:
                for p in sorted(H.OUT.with_name(brief).glob(f'planet-*-*-*-{c}/results.jsonl')):
                    for line in D.read(guard, p, brief).splitlines():
                        r = json.loads(line)
                        if r['observed']:
                            assert r['trial'] not in records
                            records[r['trial']] = r
            base = {r['trial']: r for r in old['rows']}
            assert len(base) == len(old['rows'])
            assert base.keys() == records.keys() == {r['trial'] for r in new['rows']}
            for r in new['rows']:
                assert str(r['star']) in guard.seen[c]
                b, source = base[r['trial']], records[r['trial']]
                assert r['star'] == b['star'] == source['star']
                assert r['bin'] == b['bin'] == source['bin']
                radius = radii.get((c, r['star']))
                possible = radius is None or source['depth_ppm'] <= 1e6 * min(1., (.2009/radius)**2)
                merged = dict(r, possible=possible, depth_ppm=source['depth_ppm'],
                              B_real=b['real'][bcol], B_flip=b['flip'][bcol],
                              N1_real=r['real'][0], N1_flip=r['flip'][0],
                              B_real_found=b.get('real_found'), B_flip_found=b.get('flip_found'))
                combined[phase].append(merged)
            documents[phase, c] = old, new
    design = json.loads(D.read(guard, H.OUT.with_name('fable-fresh') / 'planet-design.json', 'fable-fresh'))
    assert design['seed'] == 2026111601
    assert len(combined['planets']) == 1098
    possible = [r for r in combined['planets'] if r['possible']]
    assert len(possible) == 968
    reference = [r for r in combined['T156'] if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]
    assert len(combined['T156']) == 2000 and len(reference) == 222
    populations = dict(choosing_all=combined['planets'], choosing_possible=possible,
                       fresh_all=combined['fresh'], fresh_possible=[r for r in combined['fresh'] if r['possible']],
                       T156_all=combined['T156'], T156_reference=reference,
                       T156_reference_possible=[r for r in reference if r['possible']])
    metrics = {key: metric(rows, np) for key, rows in populations.items()}
    assert round(metrics['choosing_all']['rates'][0]*100, 3) == 48.105
    assert round(metrics['choosing_possible']['rates'][0]*100, 3) == 48.404
    assert round(metrics['T156_reference']['rates'][0]*100, 3) == 34.207
    backgrounds, candidates = [], []
    for version in (0, 1):
        backgrounds.append([e for c in ('g2', 'g3') for e in documents['planets', c][version]['background'] if e['options'][0]])
        candidates.append([e for c in ('g2', 'g3') for e in documents['planets', c][version]['candidates']])
    new_events = [e for e in backgrounds[1] if not any(same(e, old) for old in backgrounds[0])]
    nr, nf = [sum(e['kind'] == arm for e in new_events) for arm in ('real', 'flip')]
    bg = [dict(real=sum(e['kind']=='real' for e in events), flip=sum(e['kind']=='flip' for e in events)) for events in backgrounds]
    assert bg[0] == dict(real=174, flip=79)
    strata = Counter()
    for e in backgrounds[1]:
        magnitude = tmag.get((e['campaign'], e['tic']), math.nan)
        bright = 'unknown' if not math.isfinite(magnitude) else ('<11', '11-12', '12-14', '14+')[int(np.searchsorted([11, 12, 14], magnitude, side='right'))]
        era = ('1-26', '27-55', '56-93', '94+')[int(np.searchsorted([27, 56, 94], e['sector'], side='right'))]
        for label, value in (('period_bin', e['bin']), ('brightness', bright), ('product', e['product']), ('era', era)):
            strata[f'{label}:{value}:{e["kind"]}'] += 1
    held = {}
    for arm in ('real', 'flip'):
        new_candidates = [e for e in candidates[1] if e['kind']==arm and not any(same(e, old) for old in candidates[0])]
        rejected = [e for e in new_candidates if not e['options'][0]]
        flags = Counter(k for e in rejected for k, v in e['holds'][0].items() if k != 'tier' and v)
        held[arm] = dict(new_detections=len(new_candidates), not_tier1=len(rejected), flags=dict(flags))
    known = json.loads((H.OUT / 'known.json').read_text(encoding='utf-8'))
    fresh = metrics['fresh_possible']
    checks = json.loads((H.OUT / 'notch-checks.json').read_text(encoding='utf-8'))
    identity = [json.loads((H.OUT / f'generated-{c}/progress-background-0-identity.json').read_text(encoding='utf-8')) for c in ('g2', 'g3')]
    rules = dict(a=fresh['gain'] >= .02 and fresh['gain95'][0] > 0,
                 b=bg[1]['real'] <= 174 and bg[1]['flip'] <= 79,
                 c=all(metrics[k]['control_pass'] for k in ('choosing_possible','fresh_possible')),
                 d=checks['off_switch_objects_unchanged'] and all(r['status']=='complete' for r in identity),
                 e=nr-2.3*nf <= 5,
                 f=metrics['T156_reference']['rates'][2] >= metrics['T156_reference']['rates'][0],
                 g=known['pass'])
    result = dict(threshold=floor, alarm_curve=choice['alarm_curve'], metrics=metrics, background=bg,
                  new_events=dict(real=nr, upside_down=nf, excess=nr-2.3*nf), background_strata=dict(strata),
                  holds=held, known=known, rules=rules, passes=all(rules.values()), seed=SEED, bootstrap_draws=10000)
    (H.OUT / 'summary.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(dict(threshold=floor, fresh_gain=fresh['gain'], fresh_gain95=fresh['gain95'], rules=rules)))


if __name__ == '__main__':
    main()
