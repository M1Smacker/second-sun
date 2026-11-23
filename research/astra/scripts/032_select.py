"""014 eligibility and stratification, with the preregistered fresh seed."""
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
S = importlib.import_module('032_eclipse_select')
H, O = S.H, S.O


def main():
    os.environ.update(SS_SET='g2', NUMBA_NUM_THREADS='2', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    guard = H.Guard()
    guard.start()
    guard.allow_machine_inputs('g2')
    import numpy as np
    import pandas as pd
    import petrova_mask as PM
    periods = {int(r.tic): r.p_bin_d for r in pd.read_csv(H.TARGETS, comment='#').itertuples()
               if r.list == 'g2' and r.design_seen == 1}
    old = json.loads(S.saved(guard, H.OUT.with_name('014') / 'eclipse-samples.json', '014'))
    affected = set(old['affected'])
    assert len(affected) == 112 and affected <= periods.keys()
    sectors, times = {}, {}
    for path in sorted((S.SOURCE / 'groups').glob('*.json')):
        star, sec = map(int, path.stem.split('_'))
        if star not in periods:
            continue
        guard.allow_design_file(path)
        sectors.setdefault(star, set()).add(sec)
        if sec not in times:
            for m in json.loads(path.read_text(encoding='utf-8'))['meta']:
                file = H.DATA / 'g2' / str(star) / Path(m['file']).name
                guard.allow_design_file(file)
                t = S.midpoint(file)
                if t is not None:
                    times[sec] = t
                    break
    assert set.union(*sectors.values()) <= times.keys()
    cat = PM.cat()
    eligible = set()
    for star in periods.keys() - affected:
        c = cat.get(star)
        if not c or not sectors.get(star) or not all(np.isfinite(c[k]) and c[k] > 0 for k in ('P', 'T0', 'eP', 'eT0')):
            continue
        if all(3*np.hypot(c['eT0'], round((times[k]-c['T0'])/c['P'])*c['eP']) < .05 for k in sectors[star]):
            eligible.add(star)
    spent = set(old['controls'] + old['holdout'])
    assert len(spent) == 100 and spent <= eligible
    fresh = eligible - spent
    if len(fresh) >= 60:
        selected, bins = S.stratified(fresh, periods, 12, 2026112316)
    else:
        selected = sorted(fresh)
        bins = np.bincount([np.searchsorted([10,14,20,27.4], periods[s], side='right') for s in selected], minlength=5).tolist()
    assert len(selected) == min(60, len(fresh)) and not (set(selected) & (spent | affected))
    result = dict(seed=2026112316, eligible=len(eligible), remaining=len(fresh), selected=selected,
                  bins=bins, periods={s: periods[s] for s in selected},
                  sector_midpoints=times, sectors={s: sorted(sectors[s]) for s in selected})
    destination = H.OUT / 'fresh-controls.json'
    if destination.exists():
        assert json.loads(destination.read_text(encoding='utf-8')) == json.loads(json.dumps(result))
    else:
        O.write_json(destination, result, indent=2)
    print('BEFORE FITTING: eligible', len(eligible), 'spent', len(spent), 'remaining', len(fresh),
          'selected', len(selected), 'period bins', bins, flush=True)


if __name__ == '__main__':
    main()
