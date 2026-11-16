"""Catalogue-only falsification gate. Run with the project Python -I -B.

Executes only copied load_catalogue/windows AST nodes, never imports pipeline.
All windows are evaluated on synthetic times and design hosts only.
"""
import ast
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import sys

ROOT = Path(r'D:\second-sun-astra')
DATA = ROOT / 'data'
OUT = DATA / 'astra/026'


def main():
    if not sys.flags.isolated or not sys.dont_write_bytecode:
        raise RuntimeError('Use -I -B')
    import numpy as np
    import pandas as pd
    actual = DATA.resolve(strict=True)
    if OUT.resolve() != actual / 'astra/026':
        raise PermissionError('Output path escape')
    print(f'READ catalogue metadata via {DATA}', flush=True)
    print(f'WRITE {OUT}', flush=True)
    reads = {DATA / 'xmatch/ebs.csv', DATA / 'g3/catalog_ttc/table3_new_ebs.txt'}
    reads.update(DATA / f'astra/010/affected-{c}.json' for c in ('g2', 'g3'))

    def audit(event, args):
        if event == 'open' and not isinstance(args[0], int):
            path = Path(os.path.abspath(os.fsdecode(args[0])))
            resolved = path.resolve()
            writing = args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)
            if writing and not (path.is_relative_to(OUT) and resolved.is_relative_to(OUT.resolve())):
                raise PermissionError('Write outside 026')
            if not writing and resolved.is_relative_to(actual):
                if path not in reads and not (path.is_relative_to(OUT) and resolved.is_relative_to(OUT.resolve())):
                    raise PermissionError('Data read not allowlisted')
        elif event in ('os.mkdir', 'os.remove', 'os.rmdir', 'os.rename', 'os.symlink', 'os.link', 'subprocess.Popen', 'os.system'):
            raise PermissionError('Mutation or process launch disabled in trace')

    sys.addaudithook(audit)
    with (ROOT / 'targets/r1_targets.csv').open(encoding='utf-8-sig') as f:
        targets = list(csv.DictReader(line for line in f if not line.startswith('#')))
    seen = {c: {int(r['tic']) for r in targets if r['list'] == c and r['design_seen'] == '1'} for c in ('g2', 'g3')}
    forbidden = {int(r['tic']) for r in targets if r['list'] == 'g1' or r['design_seen'] == '0'}
    source = (ROOT / 'pipeline/petrova_mask.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('load_catalogue', 'windows')]
    assert len(nodes) == 2
    copied = ast.Module(body=nodes, type_ignores=[])
    ns = dict(np=np, pd=pd, ROOT=ROOT, G2RATIO=1.44, PADF=1.5)
    exec(compile(copied, '<026 copied frozen catalogue/windows>', 'exec'), ns)
    (OUT / 'frozen-functions.py').write_text(ast.unparse(copied), encoding='utf-8')

    def padding(c, t):
        e0 = c['eT0'] if math.isfinite(c['eT0']) else 0.
        ep = c['eP'] if math.isfinite(c['eP']) else 0.
        return 3 * math.hypot(e0, round((t - c['T0']) / c['P']) * ep)

    def cover(c, t):
        d = padding(c, t)
        ws = c['ws'] if math.isfinite(c['ws']) and math.isfinite(c['phs']) else c['wp']
        return min(1., min(1., (1.5*c['wp'] + 2*d)/c['P']) + min(1., (1.5*ws + 2*d)/c['P']))

    summary = {'source_sha256': hashlib.sha256(source.encode()).hexdigest(), 'campaigns': {}}
    catalogues = {}
    for campaign in ('g2', 'g3'):
        full = ns['load_catalogue'](campaign, ROOT / f'targets/{campaign}_chain_targets.csv')
        cat = {s: c for s, c in full.items() if s in seen[campaign] and s not in forbidden and np.isfinite(c['wp'])}
        catalogues[campaign] = cat
        old = set(map(int, json.loads((DATA / f'astra/010/affected-{campaign}.json').read_text(encoding='utf-8'))))
        assert old <= seen[campaign] and not old & forbidden
        rows = {}
        for t in (1500., 2500., 3500.):
            new = {s for s, c in cat.items() if cover(c, t) > .25}
            added = {s for s, c in cat.items() if 4 * padding(c, t) / c['P'] > .25}
            rows[str(int(t))] = dict(full_window=len(new), drift_added=len(added), overlap=len(old & new),
                                    old_only=len(old-new), new_only=len(new-old), symmetric_difference=len(old ^ new))
        summary['campaigns'][campaign] = dict(design=len(seen[campaign]), valid_catalogue=len(cat), old_010=len(old), epochs=rows)
        if campaign == 'g2':
            # The exact ranking operation used by drift.py, on catalogue metadata only.
            valid = [(s, c) for s, c in full.items() if np.isfinite(c['wp'])]
            order = np.argsort(-np.array([padding(c, 3500.) for _, c in valid]))[:5]
            witnesses = [valid[i] for i in order]
    eligible = [(s, c) for s, c in witnesses if s in seen['g2'] and s not in forbidden]
    checked = []
    for star, c in eligible:
        # One full synthetic orbit centred on the diagnostic timestamp.
        t = 3500. + (np.arange(20000) / 20000 - .5) * c['P']
        mask, _ = ns['windows'](t, c)
        # Independent implementation via scalar nearest centres, with floor rounding.
        e0 = c['eT0'] if math.isfinite(c['eT0']) else 0.
        ep = c['eP'] if math.isfinite(c['eP']) else 0.
        ok = math.isfinite(c['phs']) and math.isfinite(c['ws'])
        predicted = np.zeros(t.size, dtype=bool)
        for phase, width in ((0., c['wp']), (c['phs'] if ok else .5, c['ws'] if ok else c['wp'])):
            cycles = np.floor((t-c['T0'])/c['P']-phase+.5)
            dist = np.abs(t-c['T0']-(cycles+phase)*c['P'])
            predicted |= dist <= .75*width + 3*np.hypot(e0, cycles*ep)
        assert np.array_equal(mask, predicted), 'Independent window mismatch'
        checked.append(dict(star=star, fraction=float(mask.mean()), passes=bool(mask.mean()>.25)))
    passed = sum(r['passes'] for r in checked)
    summary['gate'] = dict(named_examples=len(witnesses), authorized_examples=len(eligible),
                           excluded_examples=len(witnesses)-len(eligible), reproduced=passed,
                           required=5, passed=passed>=5)
    (OUT / 'trace-private.json').write_text(json.dumps({'witnesses': [s for s, _ in witnesses], 'checks': checked}, indent=2), encoding='utf-8')
    (OUT / 'trace-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
