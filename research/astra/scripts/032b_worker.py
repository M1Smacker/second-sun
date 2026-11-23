"""Two disjoint G3 shards using exactly the 032 measurement code."""
import argparse
from collections import Counter
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
S = importlib.import_module('032b_eclipse_select')
F = importlib.import_module('032b_eclipse_fit')
H, O = S.H, S.O


def main(slot, slots):
    os.environ.update(SS_SET='g3', NUMBA_NUM_THREADS='2', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    guard = H.Guard(); guard.start(); guard.allow_machine_inputs('g3')
    import numpy as np
    import pandas as pd
    import detect_v2 as V
    import petrova_mask as PM
    import sap_twin as T
    samples = json.loads((H.OUT/'samples.json').read_text(encoding='utf-8'))['sets']['g3']
    ids = sorted(samples['selected'])
    assert len(ids) == len(set(ids)) == 60 and all(str(s) in guard.seen['g3'] for s in ids)
    best = pd.read_csv(H.DATA/'g3/audit/best_per_star_sector.csv')
    best = {(r.tic,r.sector):r.product for r in best.itertuples() if r.tic in ids}
    source = H.DATA/'stage3_g3'/f'r1dev_g3_seen_{H.DEVELOPMENT_HASH}'
    cat = PM.cat()
    counts = Counter()
    for star in ids[slot::slots]:
        checkpoint = H.OUT/'tracks'/f'g3-{star}.json'
        if checkpoint.exists():
            counts['resumed'] += 1
            continue
        entry = cat.get(star)
        result = dict(star=star, sample='g3', catalogue=entry, fit={})
        if not entry or not np.isfinite(entry['wp']) or entry['wp'] <= 0:
            result['reason'] = 'no catalogue primary width'
            O.write_json(checkpoint, result)
            counts['no catalogue width'] += 1
            continue
        raw, seen = [], set()
        for kind in ('groups', 'groups_sap'):
            for file in sorted((source/kind).glob(f'{star}_*.json')):
                guard.allow_design_file(file)
                sec = int(file.stem.split('_')[1])
                for m in json.loads(file.read_text(encoding='utf-8'))['meta']:
                    name = m['file'].removesuffix(T.SUFFIX)
                    key = sec, kind, name
                    if key in seen:
                        continue
                    seen.add(key)
                    path = H.DATA/'g3'/str(star)/Path(name).name
                    guard.allow_design_file(path)
                    loader = T.load_sap if kind == 'groups_sap' else V.load
                    t, f, _, meta = loader(str(path), info=True)
                    product = meta['product']
                    valid = np.isfinite(t)&np.isfinite(f)
                    if valid.sum() < 10:
                        counts['empty or short inputs'] += 1
                        continue
                    rank = 0 if product == best.get((star,sec)) else 2 if kind == 'groups_sap' else 1
                    raw.append((sec,rank,product,t[valid],f[valid]))
                    counts['product curves loaded'] += 1
        result['input_curves'] = len(raw)
        result['sectors'] = sorted({s for s,*_ in raw})
        result['fit'] = F.fit_star(raw,entry['P'],entry['wp'],entry['ws'] if entry['ws'] > 0 else entry['wp'],entry.get('phs',float('nan')))
        O.write_json(checkpoint, result)
        counts['processed'] += 1
    O.write_json(H.OUT/f'measure-{slot}.json',dict(counts=counts))
    print('Completed G3 shard',slot,dict(counts),flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('slot',type=int); p.add_argument('slots',type=int)
    a = p.parse_args(); main(a.slot,a.slots)
