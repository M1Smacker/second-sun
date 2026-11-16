"""Fixed raw-light controls on the first three eligible quiet class B hosts.

Eligibility is fixed before scoring: historical M2 host, a prepared best product,
post-detrending MAD <=1000 ppm, host cap >=4000 and <20000 ppm, and 80% cadence
coverage of four fixed six-hour boxes. No choice uses injected recovery outcomes.
"""
from collections import defaultdict
import csv
import importlib
import json
import math
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('026_harness')
D = importlib.import_module('026_inputs')
M = importlib.import_module('026_rules')


def main():
    campaign = 'g2'
    os.environ.update(SS_SET=campaign, VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard(); guard.start(); guard.allow_machine_inputs(campaign)
    import numpy as np
    import pandas as pd
    import stage2_search as S2
    import stage3 as S3
    import stage3_core as C
    import petrova_mask as PM
    import sap_twin as T
    import detect_v2 as detector
    out = H.OUT / 'controls-real'
    out.mkdir(exist_ok=True)
    S3._init3(out, campaign, C.GRID_V5)
    refs = {}
    for row in pd.read_csv(C.MANIFEST).drop_duplicates('file').itertuples():
        if row.author == 'SPOC':
            relative = Path(row.path).relative_to(Path(r'D:\second-sun') / 'data')
            path = H.DATA / relative
            assert path.resolve() == guard.data / relative
            refs.setdefault(int(row.file.split('-s')[1][:4]), path)
    guard.reads.update(p.resolve() for p in refs.values())
    S2.S['spoc_by_sector'] = {s: str(p) for s, p in refs.items()}
    best = {(r.tic, r.sector): r.product for r in pd.read_csv(C.BEST).itertuples()}
    radii = {}
    with (H.ROOT / 'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['set'] == campaign and r['tic'] in guard.seen[campaign]:
                try:
                    v = float(r['radius_rsun'])
                except ValueError:
                    continue
                if math.isfinite(v) and v > 0:
                    radii[int(r['tic'])] = v
    fallback = json.loads((H.OUT / 'fallback-radii.json').read_text(encoding='utf-8'))
    for key, radius in fallback.items():
        c, star = key.split(':')
        if c == campaign:
            radii.setdefault(int(star), radius)
    raw_load, raw_prepare = S2.load, S2.prepare
    frozen_mask, frozen_windows, frozen_refit = PM.mask_runs, PM.windows, PM.refit
    raw, prepared, offsets = {}, {}, {}
    current, sign, depth, active = None, 0, 0., []
    def load(path, info=False):
        key = str(path), T.MODE['sap'], T.MODE['pdc'], info
        if key not in raw:
            raw[key] = raw_load(path, info=info)
        result = raw[key]
        if not sign:
            return result
        t, f = result[:2]
        f = f.copy()
        for center, duration in active:
            f -= sign * depth * np.clip((duration / 2 - abs(t - center)) / (.1 * duration), 0, 1)
        return t, f, *result[2:]
    def prepare(path):
        nonlocal current
        current = str(path)
        if current not in prepared:
            prepared[current] = raw_prepare(path)
        return prepared[current]
    def mask(t, f, periods, tic):
        c = PM.cat()[int(tic)]
        if not sign:
            offsets[current] = frozen_refit(t, f, c)
        offset = offsets[current]
        PM.windows = lambda ts, cat: M.m2_windows(ts, cat, offset, np)
        PM.refit = lambda *unused: offset
        try:
            return frozen_mask(t, f, periods, tic)
        finally:
            PM.windows, PM.refit = frozen_windows, frozen_refit
    S2.load, S2.prepare, PM.mask_runs = load, prepare, mask
    inventory = json.loads((H.OUT / 'inventory-g2.json').read_text(encoding='utf-8'))
    periods = pd.read_csv(H.TARGETS, comment='#')
    periods = periods[(periods['list'] == 'g2') & (periods.design_seen == 1)].set_index('tic').p_bin_d.to_dict()
    selected, records, examined = set(), [], 0
    for item in inventory:
        star, sector = item['star'], item['sector']
        if item['category'] != 'B' or not item['historical_m2'] or star in selected or star not in radii:
            continue
        cap = 1e6 * min(1., (.2009 / radii[star]) ** 2)
        if not 4000 <= cap < 20000:
            continue
        examined += 1
        # A fixed cost ceiling, not a change in the selection thresholds.
        if examined > 200:
            break
        raw.clear(); prepared.clear(); offsets.clear()
        sign, active = 0, []
        # prepare() may consult the host's own SPOC file before that product's
        # turn in the loop. Authorize every design-only input first, as the
        # main generator does; otherwise the reader hides the guard rejection
        # behind a misleading unsupported/corrupt-product exception.
        for entry in item['products']:
            source = guard.allow_design_file(Path(entry['path']))
            previous = json.loads(source.read_text(encoding='utf-8'))
            for meta in previous['meta']:
                file = H.DATA / campaign / str(star) / Path(meta['file'].removesuffix(T.SUFFIX)).name
                guard.allow_design_file(file)
        products, primary = [], None
        for entry in item['products']:
            path = guard.allow_design_file(Path(entry['path']))
            previous = json.loads(path.read_text(encoding='utf-8'))
            files = []
            for meta in previous['meta']:
                file = H.DATA / campaign / str(star) / Path(meta['file'].removesuffix(T.SUFFIX)).name
                guard.allow_design_file(file)
                filename = str(file) + (T.SUFFIX if entry['kind'] == 'groups_sap' else '')
                files.append(filename)
                data, status = prepare(filename)
                if entry['kind'] == 'groups' and meta.get('product') == best.get((star, sector)) and data is not None:
                    primary = data
                if entry['kind'] == 'groups_sap':
                    prepare(str(file) + T.SUFFIX_PDC)
            products.append((entry['kind'], files))
        if primary is None:
            continue
        t, f = primary['t'], primary['f']
        if t[-1] - t[0] < 18:
            continue
        _, ff = detector.detrend(t, f)
        scatter = 1.4826 * np.nanmedian(abs(ff - np.nanmedian(ff)))
        if scatter > .001:
            continue
        cadence = float(np.median(np.diff(t)))
        origin = next((v for v in np.arange(t[0] + 2, t[-1] - 16, .5)
                       if all(np.count_nonzero(abs(t - (v + d)) <= .125) >= .8 * .25 / cadence for d in (0, 6, 7, 14))), None)
        if origin is None:
            continue
        selected.add(star)
        cases = [('eclipse2', .02, (0, 14)), ('eclipse5', .05, (0, 14)),
                 ('planet2', .004, (0, 14)), ('planet3_regular', .004, (0, 7, 14)),
                 ('planet3_irregular', .004, (0, 6, 14))]
        for label, depth, centers in cases:
            trial = len(records)
            active = [(float(origin + delta), .25) for delta in centers]
            record = dict(trial=trial, star=star, campaign=campaign, case=label,
                          bin=int(np.searchsorted([10, 14, 20, 27.4], periods[star], side='right')),
                          observed=active, changed=[sector], depth_ppm=depth * 1e6)
            records.append(record)
            # Save the chosen control before processing either injection arm.
            (out / 'records.json').write_text(json.dumps(records), encoding='utf-8')
            for sign in (1, -1):
                prepared.clear()
                destination = out / f'trial-{trial}' / str(sign)
                for kind, files in products:
                    S2.GROUPS = destination / kind
                    S2.GROUPS.mkdir(parents=True, exist_ok=True)
                    path = Path(S3.do_group3((star, sector, files)))
                    if kind == 'groups_sap':
                        S3.add_pdc((path, [p.removesuffix(T.SUFFIX) for p in files], best.get((star, sector))))
                    result = json.loads(path.read_text(encoding='utf-8'))
                    assert not any(str(m['status']).startswith('ERROR') for m in result['meta'])
        if len(selected) == 3:
            break
    (out / 'records.json').write_text(json.dumps(records), encoding='utf-8')
    summary = dict(selected_hosts=len(selected), trials=len(records), examined_sectors=min(examined, 200),
                   full_control_sample=len(selected) == 3)
    (out / 'counts.json').write_text(json.dumps(summary), encoding='utf-8')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
