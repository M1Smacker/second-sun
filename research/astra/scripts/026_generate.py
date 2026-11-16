"""Generate only M4 class B sectors absent from M2 replays, plus A identities."""
import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('026_harness')
D = importlib.import_module('026_inputs')
M = importlib.import_module('026_rules')


def main(campaign, slot, slots):
    os.environ.update(SS_SET=campaign, VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    guard.allow_machine_inputs(campaign)
    import numpy as np
    import pandas as pd
    import stage2_search as S2
    import stage3 as S3
    import stage3_core as C
    import petrova_mask as PM
    import sap_twin as T
    out = H.OUT / f'generated-{campaign}-{slot}'
    out.mkdir(exist_ok=True)
    now = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', started=now.isoformat(), expected_finish=(now + timedelta(hours=1)).isoformat())
    def save():
        (out / 'progress.json').write_text(json.dumps(progress), encoding='utf-8')
    save()
    S3._init3(out, campaign, C.GRID_V5)
    # Frozen reference selection, machine-input-only permission in AGENTS section 4.2.
    refs = {}
    for row in pd.read_csv(C.MANIFEST).drop_duplicates('file').itertuples():
        if row.author == 'SPOC':
            sector = int(row.file.split('-s')[1][:4])
            relative = Path(row.path).relative_to(Path(r'D:\second-sun') / 'data')
            path = H.DATA / relative
            if path.resolve() != guard.data / relative:
                raise PermissionError('Reference path escape')
            refs.setdefault(sector, path)
    guard.reads.update(path.resolve() for path in refs.values())
    S2.S['spoc_by_sector'] = {s: str(p) for s, p in refs.items()}
    best = {(r.tic, r.sector): r.product for r in pd.read_csv(C.BEST).itertuples()}
    inventory = json.loads((H.OUT / f'inventory-{campaign}.json').read_text(encoding='utf-8'))
    b_hosts = {r['star'] for r in inventory if r['category'] == 'B'}
    identities = [r for r in inventory if r['category'] == 'A' and r['star'] not in b_hosts][:25]
    rows = [r for r in inventory if r['category'] == 'B' and not r['historical_m2']]
    work = [(r, False) for r in rows[slot::slots]]
    if slot == 0:
        work += [(r, True) for r in identities]
    draws = defaultdict(list)
    for r, _ in D.t156_rows(guard, campaign):
        draws[r['star'], r['sector']].append(('T156', r))
    for path in sorted((H.DATA / 'astra/006').glob(f'planet-*-*-*-{campaign}/results.jsonl')):
        for line in D.read(guard, path, '006').splitlines():
            r = json.loads(line)
            assert str(r['star']) in guard.seen[campaign]
            for sector in r['changed']:
                draws[r['star'], sector].append(('planets', r))
    raw_load, raw_prepare = S2.load, S2.prepare
    frozen_mask, frozen_windows, frozen_refit = PM.mask_runs, PM.windows, PM.refit
    raw, prepared, offsets = {}, {}, {}
    active, sign, depth, current, use_m2 = [], 0, 0., None, False
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
        if not use_m2:
            return frozen_mask(t, f, periods, tic)
        c = PM.cat().get(int(tic))
        assert c is not None and np.isfinite(c['wp'])
        if not sign:
            offsets[current] = frozen_refit(t, f, c)
        offset = offsets[current]
        PM.windows = lambda ts, cat: M.m2_windows(ts, cat, offset, np)
        PM.refit = lambda *args: offset
        try:
            return frozen_mask(t, f, periods, tic)
        finally:
            PM.windows, PM.refit = frozen_windows, frozen_refit
    S2.load, S2.prepare, PM.mask_runs = load, prepare, mask
    identity = []
    counts = dict(groups=0, new_b_sectors=len(work) - (len(identities) if slot == 0 else 0))
    try:
        for n, (item, compare) in enumerate(work):
            star, sector = item['star'], item['sector']
            assert str(star) in guard.seen[campaign]
            raw.clear(); offsets.clear()
            use_m2 = not compare
            products = []
            for entry in item['products']:
                path = guard.allow_design_file(Path(entry['path']))
                group = json.loads(path.read_text(encoding='utf-8'))
                files = []
                for meta in group['meta']:
                    file = H.DATA / campaign / str(star) / Path(meta['file'].removesuffix(T.SUFFIX)).name
                    guard.allow_design_file(file)
                    files.append(str(file) + (T.SUFFIX if entry['kind'] == 'groups_sap' else ''))
                products.append((entry['kind'], files, group))
            def generate(destination):
                prepared.clear()
                for kind, files, previous in products:
                    S2.GROUPS = destination / kind
                    S2.GROUPS.mkdir(parents=True, exist_ok=True)
                    path = Path(S3.do_group3((star, sector, files)))
                    if kind == 'groups_sap':
                        S3.add_pdc((path, [p.removesuffix(T.SUFFIX) for p in files], best.get((star, sector))))
                    result = json.loads(path.read_text(encoding='utf-8'))
                    assert not any(str(m['status']).startswith('ERROR') for m in result['meta'])
                    if compare:
                        canon = lambda es: sorted(json.dumps(e, sort_keys=True) for e in es)
                        assert canon(result['events']) == canon(previous['events']), 'Class A event identity failed'
                    counts['groups'] += 1
            sign, active = 0, []
            generate(out / ('identity' if compare else 'background'))
            if compare:
                identity.append([star, sector])
            else:
                for bench, draw in draws[star, sector]:
                    active = [(draw['time'], draw['duration_h'] / 24)] if bench == 'T156' else draw['observed']
                    depth = draw['depth_ppm'] * 1e-6
                    for sign in (1, -1):
                        generate(out / bench / f'trial-{draw["trial"]}' / str(sign))
            progress.update(done=n + 1, total=len(work))
            save()
        (out / 'counts.json').write_text(json.dumps(dict(counts=counts, identity=identity)), encoding='utf-8')
        progress['status'] = 'complete'
        print(campaign, slot, counts, 'identity sectors', len(identity), flush=True)
    except Exception:
        progress['status'] = 'failed'
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('campaign', choices=('g2', 'g3'))
    p.add_argument('slot', type=int)
    p.add_argument('slots', type=int)
    a = p.parse_args()
    main(a.campaign, a.slot, a.slots)
