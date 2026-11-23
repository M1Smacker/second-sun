"""Freeze all judging membership and sector counts before any 032b fitting."""
import csv
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
S = importlib.import_module('032b_eclipse_select')
H, O = S.H, S.O


def main():
    os.environ.update(SS_SET='g3', NUMBA_NUM_THREADS='2', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    guard = H.Guard(); guard.start()
    import pandas as pd
    import numpy as np
    targets = pd.read_csv(H.TARGETS, comment='#')
    old = json.loads(S.saved(guard, H.OUT.with_name('014')/'eclipse-samples.json', '014'))
    fresh = json.loads(S.saved(guard, H.OUT.with_name('032')/'fresh-controls.json', '032'))
    eph = list(csv.DictReader(S.saved(guard, H.OUT.with_name('032')/'ephemerides-v3.csv', '032').splitlines()))
    seen = sorted(int(r['star']) for r in eph if r['type'] == 'primary' and r['usable'] == 'True')
    assert len(seen) == 53 and set(seen) <= set(fresh['selected'])
    result = dict(seed=2026112318, sets={})
    for campaign in ('g2', 'g3'):
        periods = {int(r.tic):float(r.p_bin_d) for r in targets.itertuples()
                   if r.list == campaign and r.design_seen == 1}
        sectors, times = {}, {}
        source = H.DATA/f'stage3_{campaign}'/f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
        for path in sorted((source/'groups').glob('*.json')):
            star, sec = map(int, path.stem.split('_'))
            if star not in periods:
                continue
            sectors.setdefault(star, set()).add(sec)
            if sec in times:
                continue
            guard.allow_design_file(path)
            for m in json.loads(path.read_text(encoding='utf-8'))['meta']:
                file = H.DATA/campaign/str(star)/Path(m['file']).name
                guard.allow_design_file(file)
                midpoint = S.midpoint(file)
                if midpoint is not None:
                    times[sec] = midpoint
                    break
        if campaign == 'g2':
            selected = sorted(old['affected'])
            assert len(selected) == 112 and set(selected) <= periods.keys()
            selections = [('affected', selected), ('seen', seen)]
        else:
            eligible = {s for s in periods if len(sectors.get(s, [])) >= 3}
            assert len(eligible) >= 60, 'Fewer than 60 eligible G3 stars: no replacement rule'
            selected, _ = S.stratified(eligible, periods, 12, 2026112318)
            selections = [('g3', selected)]
            result['g3_eligible'] = len(eligible)
        for label, selected in selections:
            bins = np.bincount([np.searchsorted([10,14,20,27.4], periods[s], side='right') for s in selected], minlength=5).tolist()
            result['sets'][label] = dict(campaign=campaign, selected=selected, bins=bins,
                periods={s:periods[s] for s in selected}, sectors={s:sorted(sectors.get(s, [])) for s in selected},
                sector_midpoints=times)
            assert all(sec in times for s in selected for sec in sectors.get(s, []))
            print('BEFORE FITTING:', label, 'selected',len(selected),'bins',bins,
                  'with at least 3 catalogue sectors',sum(len(sectors.get(s, [])) >= 3 for s in selected), flush=True)
    path = H.OUT/'samples.json'
    if path.exists():
        assert json.loads(path.read_text(encoding='utf-8')) == json.loads(json.dumps(result))
    else:
        O.write_json(path, result, indent=2)


if __name__ == '__main__':
    main()
