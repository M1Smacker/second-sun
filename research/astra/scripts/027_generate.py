"""Replay c1a on design light with injections before windows, mask and detrending."""
import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('027_inputs')
H = D.H


def main(campaign, slot, slots, phase, identity=False):
    os.environ.update(SS_SET=campaign, VESPER_OPTS='c6,p1' + ('' if identity else ',c1a'), NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    guard.allow_machine_inputs(campaign)
    import numpy as np
    import pandas as pd
    import stage2_search as S2
    import stage3 as S3
    import stage3_core as C
    import sap_twin as T
    import vopts as V
    assert ('c1a' in V.ON) != identity
    out = H.OUT / f'generated-{campaign}'
    out.mkdir(exist_ok=True)
    progress_file = out / f'progress-{phase}-{slot}{"-identity" if identity else ""}.json'
    now = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', started=now.isoformat(), expected_finish=(now + timedelta(hours=5)).isoformat())
    def save():
        pending = progress_file.with_suffix('.pending')
        pending.write_text(json.dumps(progress), encoding='utf-8')
        pending.replace(progress_file)
    save()
    S3._init3(out, campaign, C.GRID_V5)
    # Choose only permitted reference hosts. Never open a fenced reference file.
    refs = {}
    for r in pd.read_csv(C.MANIFEST).drop_duplicates('file').itertuples():
        if r.author == 'SPOC' and str(r.tic) in guard.seen[campaign]:
            sec = int(r.file.split('-s')[1][:4])
            p = H.DATA / campaign / str(r.tic) / r.file
            guard.allow_design_file(p)
            refs.setdefault(sec, p)
    S2.S['spoc_by_sector'] = {sec: str(p) for sec, p in refs.items()}
    best = {(r.tic, r.sector): r.product for r in pd.read_csv(C.BEST).itertuples()}
    draws = defaultdict(list)
    if phase == 'planets':
        for p in sorted((H.DATA / 'astra/006').glob(f'planet-*-*-*-{campaign}/results.jsonl')):
            for line in D.read(guard, p, '006').splitlines():
                r = json.loads(line)
                assert str(r['star']) in guard.seen[campaign]
                if r['observed']:
                    for sec in r['changed']:
                        draws[r['star'], sec].append(r)
    elif phase == 'T156':
        for r, _ in D.t156_rows(guard, campaign):
            draws[r['star'], r['sector']].append(r)
    source = H.DATA / f'stage3_{campaign}' / f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
    sectors = defaultdict(list)
    for kind in D.KINDS:
        for p in sorted((source / kind).glob('*.json')):
            star, sec = map(int, p.stem.split('_'))
            if str(star) not in guard.seen[campaign]:
                continue
            guard.allow_design_file(p)
            previous = json.loads(p.read_text(encoding='utf-8'))
            files = []
            for meta in previous['meta']:
                file = H.DATA / campaign / str(star) / Path(meta['file'].removesuffix(T.SUFFIX)).name
                guard.allow_design_file(file)
                files.append(str(file) + (T.SUFFIX if kind == 'groups_sap' else ''))
            sectors[star, sec].append((kind, files, previous))
    if phase != 'background':
        assert draws.keys() <= sectors.keys(), 'Trial sector absent from design context'
    work = [(key, products) for key, products in sorted(sectors.items()) if phase == 'background' or key in draws]
    if identity:
        work = work[:25]
    work = work[slot::slots]
    raw_load, raw_prepare = S2.load, S2.prepare
    raw, prepared = {}, {}
    active, sign, depth = [], 0, 0.
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
        key = str(path)
        if key not in prepared:
            prepared[key] = raw_prepare(path)
        return prepared[key]
    S2.load, S2.prepare = load, prepare
    completed, generated = 0, 0
    def generate(destination, products, star, sec):
        nonlocal generated
        prepared.clear()
        # Each destination is a different injection. Cache is cleared between all arms.
        for kind, files, old in products:
            S2.GROUPS = destination / kind
            S2.GROUPS.mkdir(parents=True, exist_ok=True)
            path = Path(S3.do_group3((star, sec, files)))
            if kind == 'groups_sap':
                S3.add_pdc((path, [p.removesuffix(T.SUFFIX) for p in files], best.get((star, sec))))
            group = json.loads(path.read_text(encoding='utf-8'))
            assert not any(str(m.get('status')).startswith('ERROR') for m in group['meta']), 'Preparation error'
            if identity:
                canon = lambda ev: sorted(json.dumps(e, sort_keys=True) for e in ev)
                assert canon(group['events']) == canon(old['events']), 'c1a-off raw replay identity failed'
            generated += 1
    try:
        for (star, sec), products in work:
            raw.clear()
            for p in (H.DATA / campaign / str(star)).glob('*.fits'):
                guard.allow_design_file(p)
            if identity or phase == 'background':
                active, sign = [], 0
                generate(out / ('identity' if identity else 'background'), products, star, sec)
            else:
                for r in draws[star, sec]:
                    active = [(r['time'], r['duration_h']/24)] if phase == 'T156' else r['observed']
                    depth = r['depth_ppm'] * 1e-6
                    for sign in (1, -1):
                        generate(out / phase / f'trial-{r["trial"]}' / str(sign), products, star, sec)
            completed += 1
            progress.update(done=completed, total=len(work), groups=generated)
            save()
        if phase == 'background' and not identity and slot == 0:
            (out / 'counts.json').write_text(json.dumps(dict(affected=list(sectors))), encoding='utf-8')
        progress['status'] = 'complete'
        print(campaign, phase, slot, 'sectors', completed, 'groups', generated, 'identity' if identity else 'c1a', flush=True)
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
    p.add_argument('phase', choices=('planets', 'background', 'T156'))
    p.add_argument('--identity', action='store_true')
    a = p.parse_args()
    main(a.campaign, a.slot, a.slots, a.phase, a.identity)
