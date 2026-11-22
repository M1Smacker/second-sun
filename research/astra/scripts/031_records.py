"""Prepare fixed old/new draw journals and raw-time observability, before search."""
import argparse
from collections import Counter, defaultdict
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('031_inputs')
H = D.H


def main(campaign):
    os.environ.update(SS_SET=campaign, VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    guard.allow_machine_inputs(campaign)
    import numpy as np
    import pandas as pd
    import stage2_search as S2
    import stage3 as S3
    import stage3_core as C
    import stage3_report as R
    import sap_twin as T
    # Pure orbit geometry copied into this brief; no original runner imports.
    Orbit = importlib.import_module('031_orbits').Orbit
    S3._init3(H.OUT/'records', campaign, C.GRID_V5)
    source = H.DATA/f'stage3_{campaign}'/f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
    best = pd.read_csv(C.BEST)[['tic','sector','product']].rename(columns={'product':'best'})
    bestmap = {(r.tic,r.sector):r.best for r in best.itertuples()}
    groups = defaultdict(list)
    events = []
    for kind in D.KINDS:
        for p in sorted((source/kind).glob('*.json')):
            star, sec = map(int,p.stem.split('_'))
            if str(star) not in guard.seen[campaign]:
                continue
            guard.allow_design_file(p)
            g = json.loads(p.read_text(encoding='utf-8'))
            groups[star,sec].append((kind,g))
            events.extend(g['events'])
    context = pd.DataFrame(events).merge(best,on=['tic','sector'],how='left')
    context['primary'] = context['product']==context['best']
    context['c8_best'] = pd.to_numeric(context.c8_best,errors='coerce')
    raw = {}
    def times(star, meta, sap=False):
        p = H.DATA/campaign/str(star)/Path(meta['file'].removesuffix(T.SUFFIX)).name
        guard.allow_design_file(p)
        key = str(p),sap
        if key not in raw:
            T.MODE['sap'] = sap
            try:
                raw[key] = S2.load(str(p),info=True)[0]
            finally:
                T.MODE['sap'] = False
        return raw[key]
    old = {}
    for phase, brief in (('choosing','006'),('fresh_old','fable-fresh')):
        rows = []
        for p in sorted((H.DATA/'astra'/brief).glob(f'planet-*-*-*-{campaign}/results.jsonl')):
            rows.extend(dict(json.loads(line), _archive_folder=str(p.parent)) for line in D.read(guard,p,brief).splitlines())
        old[phase] = rows
    old['T156_old'] = [dict(r,_archive_folder=str(folder)) for r,folder in D.t156_rows(guard,campaign)]
    def fresh_record(job):
        star = job['star']
        assert str(star) in guard.seen[campaign]
        orbit = Orbit(**{k:job[k] for k in ('binary_period','binary_epoch','planet_period','planet_epoch')})
        result = dict(job,observed=[],changed=[])
        for sec in job['sectors']:
            timestamps = []
            product = bestmap.get((star,sec))
            for kind,g in groups[star,sec]:
                for m in {m['file']:m for m in g['meta']}.values():
                    if product and m.get('product') not in (product,product+'-SAP'):
                        continue
                    t = times(star,m,kind=='groups_sap')
                    if len(t):
                        timestamps.append(t)
            if not timestamps:
                continue
            active = [(c,d) for c,d in orbit.crossings(min(t.min() for t in timestamps),max(t.max() for t in timestamps))
                      if any(np.any(abs(t-c)<=d/2) for t in timestamps)]
            result['observed'].extend(active)
            if active:
                result['changed'].append(sec)
        result['observed'] = sorted(set(tuple(v) for v in result['observed']))
        raw.clear()
        return result
    # Deterministic first ten archived trials test the extracted observability path.
    for r in old['fresh_old'][:10]:
        recovered = fresh_record(r)
        assert [list(v) for v in recovered['observed']] == r['observed']
        assert recovered['changed'] == r['changed']
    fresh = json.loads((H.OUT/'fresh-new/planet-design.json').read_text(encoding='utf-8'))
    newfresh = [fresh_record(r) for r in fresh['trials'] if r['campaign']==campaign]
    t156 = json.loads((H.OUT/'T156-new/design.json').read_text(encoding='utf-8'))
    newt156 = []
    excluded = Counter()
    for r in t156['trials']:
        if r['campaign'] != campaign:
            continue
        star,sec = r['star'],r['sector']
        assert str(star) in guard.seen[campaign]
        primary = next(g for kind,g in groups[star,sec] if kind=='groups')
        product = bestmap.get((star,sec))
        m = next((m for m in primary['meta'] if m.get('product')==product),primary['meta'][0])
        t = times(star,m)
        # Amendment 031c: exclude the same empty selected product for every recipe.
        if not len(t):
            excluded[r['bin']] += 1
            raw.clear()
            continue
        center = float(t.min()+r['phase_fraction']*(t.max()-t.min()))
        cameras = {e['camera'] for _,g in groups[star,sec] for e in g['events']}
        cameras.update(m['camera'] for m in primary['meta'] if 'camera' in m)
        sub = context[(context.tic==star)|((context.sector==sec)&context.camera.isin(cameras))].copy()
        base = R.apply_v7(R.merge_sap(sub)).reset_index(drop=True)
        base = base[(base.tic==star)&(base.sector==sec)]
        result = dict(r,time=center,product=product)
        for arm,label in (('real','dip'),('flip','bump')):
            prior = base[(base.kind==arm)&base.primary&(abs(base.center-center)<=r['duration_h']/48)]
            result[label] = dict(preexisting=bool(len(prior)))
        newt156.append(result)
        raw.clear()
    old.update(fresh_new=newfresh,T156_new=newt156)
    counts = {}
    for phase,rows in old.items():
        assert rows and len(rows)==len({r['trial'] for r in rows})
        (H.OUT/'records'/f'{phase}-{campaign}.json').write_text(json.dumps(rows),encoding='utf-8')
        counts[phase] = dict(total=len(rows),observable=sum(bool(r.get('observed')) for r in rows) if not phase.startswith('T156') else len(rows))
    counts['T156_new']['empty_span_excluded_by_bin'] = [excluded[b] for b in range(5)]
    # Fresh draws with no loaded times already have observed=[] and are omitted
    # by layout, generation and scoring, just like any other unobserved planet.
    counts['fresh_new']['unobserved_excluded_by_bin'] = [sum(r['bin']==b and not r['observed'] for r in newfresh) for b in range(5)]
    (H.OUT/'records'/f'{campaign}-complete.json').write_text(json.dumps(counts,indent=2),encoding='utf-8')
    print(campaign,json.dumps(counts),flush=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('campaign',choices=('g2','g3'))
    main(p.parse_args().campaign)
