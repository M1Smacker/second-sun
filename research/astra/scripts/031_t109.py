"""Amended rule (g): sector-local T109/Q5 path, fixed N1 threshold.

Read only the published system's guarded design groups. Reuse the completed
raw-light N1 replays, then apply Q5's sector-local context and matching windows.
No search, threshold selection, or injection population is rerun.
"""
import argparse
import ast
from collections import defaultdict
import hashlib
from itertools import combinations
import json
import math
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import importlib
H = importlib.import_module('031_harness')
N = importlib.import_module('031_notch')


def definitions(path, names, scope):
    tree = ast.parse(path.read_text(encoding='utf-8'))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), scope)


def main(baseline_only=False):
    os.environ.update(SS_SET='g2', VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    guard.allow_machine_inputs('g2')
    import numpy as np
    import pandas as pd
    import stage3_core as C
    import stage3_report as R

    spec = H.ROOT / 'research/stage3/t109/t109_toi1338_bench.py'
    constants = {}
    for node in ast.parse(spec.read_text(encoding='utf-8')).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ('TIC', 'OBS', 'PRED'):
                constants[node.targets[0].id] = ast.literal_eval(node.value)
    star = constants['TIC']
    windows = {**constants['OBS'], **constants['PRED']}
    assert len(windows) == 13 and str(star) in guard.seen['g2']
    floor = 6.5
    assert floor == 6.5
    scope = dict(defaultdict=defaultdict, combinations=combinations, np=np,
                 FLIP_D=.3, WIN_D=6.85,
                 EXPL=('c5', 'ecl_overlap', 'orbit_lock', 'p1_veto', 'repeater'))
    # Copy only pure definitions, never import the original scripts or their ROOT.
    definitions(H.ROOT / 'research/stage3/006-check/p_recount.py', ('binary_members', 'bench'), scope)
    definitions(H.ROOT / 'research/stage3/rs024/rs024_options.py', ('truthy', 'prep', 'dominated', 'tier_under'), scope)
    targets = pd.read_csv(C.TARGETS, comment='#')
    period = float(targets.loc[targets.tic == star, 'p_bin_d'].iloc[0])
    best = pd.read_csv(C.BEST)[['tic', 'sector', 'product']].rename(columns={'product': 'best'})
    source = H.DATA / 'stage3_g2' / f'r1dev_g2_seen_{H.DEVELOPMENT_HASH}'
    generated = H.OUT / 'generated-D1-g2/background'
    groups = {}
    hashes = {}
    for sec in sorted(windows):
        groups[sec] = []
        for kind in ('groups', 'groups_sap'):
            path = source / kind / f'{star}_{sec}.json'
            if path.exists():
                guard.allow_design_file(path)
                old = json.loads(path.read_text(encoding='utf-8'))
                assert (old['tic'], old['sector']) == (star, sec)
                groups[sec].append((kind, path, old))
        # Q5 counts all thirteen windows, including a no-stored-file outcome.
        # Preserve that outcome rather than creating new coverage for this gate.

    scored = {'B': [], 'D1': []}
    def score(events, sec, n1=False):
        if n1:
            events = [e for e in events if e['snr'] >= floor]
        key = lambda e: (e['product'],e['kind'],e['center'],e['dur_h'])
        saved_mirrors = {key(e):e['flipmatch'] for e in events}
        events = scope['bench'](events, period, C)
        if n1:
            for e in events:
                opposite = [v for v in events if v['product'] == e['product'] and v['kind'] != e['kind']]
                e['flipmatch'] = N.mirrored(e, opposite) if e['dur_h'] <= 8 else saved_mirrors[key(e)]
                flags = [x for x in str(e.get('flags') or '').split('; ') if x != 'matched in flipped data']
                if e['flipmatch']:
                    flags.append('matched in flipped data')
                e['flags'] = '; '.join(flags)
                temporary = dict(e)
                temporary.pop('pdc_snr', None)
                e['tier'] = C.tier_of(temporary)
        if not events:
            return False, 0, 0
        frame = pd.DataFrame(events).merge(best, on=['tic', 'sector'], how='left')
        frame['primary'] = frame['product'] == frame['best']
        frame['c8_best'] = pd.to_numeric(frame['c8_best'], errors='coerce')
        frame = R.apply_v7(R.merge_sap(frame.reset_index(drop=True)))
        frame, pools = scope['prep'](frame)
        for i in frame.index:
            e = frame.loc[i]
            scored['D1' if n1 else 'B'].append(dict(sector=int(sec), kind=e['kind'],
                primary=bool(e['primary']), snr=float(e['snr']), center=float(e['center']),
                tier=scope['tier_under'](frame, pools, i, 'OAE', C)))
        center, sigma = windows[sec]
        near = frame[(frame.kind == 'real') & ((frame.center-center).abs() <= 3*sigma+.1)
                     & frame.primary & (frame.snr >= (floor if n1 else 7))]
        tiers = [scope['tier_under'](frame, pools, i, 'OAE', C) for i in near.index]
        identity = sum(scope['dominated'](frame.loc[i], i, pools, 'O0') == bool(scope['truthy'](frame.loc[i].get('dominated'))) for i in near.index)
        return any(t in {'1A', '1L', '1B'} for t in tiers), len(near), identity

    def count(version):
        found, nnear, ident = [], 0, 0
        for sec, products in groups.items():
            events = []
            for kind, path, old in products:
                if version == 'D1':
                    path = generated / kind / path.name
                    assert path.is_file(), 'Missing completed N1 replay for T109'
                    doc = json.loads(path.read_text(encoding='utf-8'))
                    assert (doc['tic'], doc['sector']) == (star, sec)
                    canon = lambda rows: sorted(json.dumps(dict(r, file=Path(r['file']).name), sort_keys=True) for r in rows)
                    assert canon(doc['meta']) == canon(old['meta']), 'T109 input/preprocessing mismatch'
                    assert not any(str(r.get('status', '')).startswith('ERROR') for r in doc['meta'])
                else:
                    doc = old
                hashes[str(path.relative_to(H.DATA))] = hashlib.sha256(path.read_bytes()).hexdigest()
                events.extend(doc['events'])
            yes, n, same = score(events, sec, version == 'D1')
            if yes:
                found.append(sec)
            nnear += n
            ident += same
        return dict(OBS=sum(s in constants['OBS'] for s in found),
                    PRED=sum(s in constants['PRED'] for s in found), total=len(found),
                    sectors_checked=len(groups), sectors_with_data=sum(bool(g) for g in groups.values()),
                    missing_sectors=sum(not g for g in groups.values()),
                    primary_matches=nnear, O0_identity_matches=ident)

    baseline = count('B')
    (H.OUT / 't109-baseline.json').write_text(json.dumps(baseline, indent=2), encoding='utf-8')
    print('T109 B:', json.dumps(baseline), flush=True)
    assert baseline['total'] == 6, 'STOP: T109 B does not reproduce six of thirteen'
    assert baseline['primary_matches'] == baseline['O0_identity_matches'], 'Q5 O0 identity failed'
    if baseline_only:
        return
    n1 = count('D1')
    path = H.OUT / 'known.json'
    result = {}
    result.update(B=baseline, D1=n1, n_transits=13, threshold=floor,
                  scope='Full T109/Q5 sector-local path, nine observed and four forecast matching windows',
                  note='New D1 raw-light design-background groups, same T109 windows',
                  **{'pass': n1['total'] >= 6})
    path.write_text(json.dumps(result, indent=2), encoding='utf-8')
    (H.OUT / 't109-scored.json').write_text(json.dumps(scored), encoding='utf-8')
    (H.OUT / 't109-input-hashes.json').write_text(json.dumps(hashes, indent=2), encoding='utf-8')
    print('T109 D1:', json.dumps(n1), 'PASS' if result['pass'] else 'FAIL', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline-only', action='store_true')
    main(parser.parse_args().baseline_only)
