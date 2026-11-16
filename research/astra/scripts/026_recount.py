"""Independent count reconciliation of saved outcomes, without pipeline imports."""
import csv
import json
import math
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/026'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    with (ROOT / 'targets/r1_targets.csv').open(encoding='utf-8-sig') as f:
        seen = {(r['list'], int(r['tic'])) for r in csv.DictReader(
            line for line in f if not line.startswith('#')) if r['design_seen'] == '1' and r['list'] in ('g2', 'g3')}
    rows = read(OUT / 'combined-planets.json')
    trials = read(OUT / 'combined-T156.json')
    assert all((r['campaign'], r['star']) in seen for r in rows + trials)
    old = read(ROOT / 'data/astra/023/combined-planets.json')
    old = {(r['campaign'], r['trial']): r for r in old}
    old_t = read(ROOT / 'data/astra/023/combined-T156.json')
    old_t = {(r['campaign'], r['trial']): r for r in old_t}
    assert all(r[a][0] == old_t[r['campaign'], r['trial']][a][0]
               for r in trials for a in ('real', 'flip'))
    radii = {}
    with (ROOT / 'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            key = r['set'], int(r['tic'])
            if key not in seen:
                continue
            try:
                v = float(r['radius_rsun'])
            except ValueError:
                continue
            if math.isfinite(v) and v > 0:
                radii[key] = v
    depths = {}
    for p in (ROOT / 'data/astra/006').glob('planet-*-*-*-*/results.jsonl'):
        for line in p.read_text(encoding='utf-8').splitlines():
            r = json.loads(line)
            assert (r['campaign'], r['star']) in seen
            depths[r['campaign'], r['trial']] = r['depth_ppm']
    possible = [r for r in rows if (r['campaign'], r['star']) not in radii or
                depths[r['campaign'], r['trial']] <= 1e6 * min(1., (.2009 / radii[r['campaign'], r['star']]) ** 2)]
    assert len(possible) == 968
    summary = read(OUT / 'summary-m4.json')
    comparisons = {}
    checked = 0
    for name, population in [('fixed1098', rows), ('possible968', possible),
                             ('T156reference', [r for r in trials if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12])]:
        values = []
        for i in range(6):
            item = {}
            for arm, a in enumerate(('real', 'flip')):
                bins = [[r for r in population if r['bin'] == b] for b in range(5)]
                hits = [sum(bool(r[a][i]) for r in group) for group in bins]
                rate = sum(k / len(group) for k, group in zip(hits, bins)) / 5
                assert math.isclose(rate, summary['metrics'][name]['rates'][arm][i], abs_tol=1e-14)
                assert hits == [summary['metrics'][name]['counts'][b][arm][i] for b in range(5)]
                checked += 5
                item[a] = dict(recovered=sum(hits), gained=sum(r[a][i] and not r[a][0] for r in population),
                               lost=sum(r[a][0] and not r[a][i] for r in population))
            values.append(item)
        comparisons[name] = values
    fallback = {a: dict(lost=sum(old[r['campaign'], r['trial']][a][1] and not r[a][3] for r in rows),
                       gained=sum(r[a][3] and not old[r['campaign'], r['trial']][a][1] for r in rows)) for a in ('real', 'flip')}
    result = dict(possible_membership=968, t156_baseline_identities=2000,
                  direct_bin_counts=checked, gains_losses=comparisons,
                  fallback_increment_vs_old_C96=fallback, pipeline_imports=False,
                  independent_review=False)
    (OUT / 'recount-m4.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'gains_losses'}, indent=2))


if __name__ == '__main__':
    main()
