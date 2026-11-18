"""Independent B recount from archived outcomes and raw injection journals."""
import csv
import json
import math
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/030'


def main():
    radii, allowed = {}, {'g2': set(), 'g3': set()}
    with (ROOT / 'targets/r1_targets.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(l for l in f if not l.startswith('#')):
            if r['list'] in allowed and r['design_seen'] == '1':
                allowed[r['list']].add(int(r['tic']))
    with (ROOT / 'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['set'] not in allowed or int(r['tic']) not in allowed[r['set']]:
                continue
            try:
                radius = float(r['radius_rsun'])
            except ValueError:
                continue
            if math.isfinite(radius) and radius > 0:
                radii[r['set'], int(r['tic'])] = radius
    allrows, possible, bg = [], [], [0, 0]
    for c in allowed:
        doc = json.loads((OUT.with_name('027') / f'baseline-planets-{c}-V0.json').read_text(encoding='utf-8'))
        indexed = {r['trial']: r for r in doc['rows']}
        assert all(r['star'] in allowed[c] for r in indexed.values())
        allrows += list(indexed.values())
        for i, arm in enumerate(('real', 'flip')):
            bg[i] += sum(e['kind'] == arm and e['options'][0] for e in doc['background'])
        seen = set()
        for journal in sorted(OUT.with_name('006').glob(f'planet-*-*-*-{c}/results.jsonl')):
            for line in journal.read_text(encoding='utf-8').splitlines():
                r = json.loads(line)
                assert r['star'] in allowed[c]
                if not r['observed']:
                    continue
                assert r['trial'] not in seen
                seen.add(r['trial'])
                radius = radii.get((c, r['star']))
                if radius is None or r['depth_ppm'] <= 1e6 * min(1., (.2009 / radius) ** 2):
                    possible.append(indexed[r['trial']])
        assert seen == indexed.keys()
    def summary(rows):
        bins = [dict(n=sum(r['bin'] == b for r in rows),
                     hits=sum(r['bin'] == b and r['real'][0] for r in rows)) for b in range(5)]
        return dict(n=len(rows), bins=bins, percent=sum(b['hits'] / b['n'] for b in bins) * 20)
    result = dict(all1098=summary(allrows), possible968=summary(possible), background=bg,
                  source='archived 027 outcomes independently joined to 006 draw journals; no pipeline import')
    (OUT / 'independent-recount.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))
    assert result['all1098']['n'] == 1098 and result['possible968']['n'] == 968
    assert round(result['all1098']['percent'], 3) == 48.105
    assert round(result['possible968']['percent'], 3) == 48.404
    assert bg == [174, 79]


if __name__ == '__main__':
    main()
