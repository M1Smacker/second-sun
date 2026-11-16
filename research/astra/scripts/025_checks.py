"""Runtime quality mutations, real-product coverage and wrong-epoch eclipses."""
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('025_harness')


def main(campaign):
    os.environ.update(SS_SET=campaign, VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    import numpy as np
    import stage2_search as S
    import petrova_mask as PM
    Q = importlib.import_module('025_loader')
    checks = Q.checks()
    trace = json.loads((H.OUT / f'trace-{campaign}.json').read_text(encoding='utf-8'))
    chosen = {}
    for row in trace['rows']:
        for file in row['files'] + row.get('alternatives', []):
            sec = row['sector']
            era = 'pre56' if sec < 56 else '56to93' if sec < 94 else '94plus'
            cadence = round(file['cadence_min'] * 60)
            key = (file['product'], era, cadence)
            chosen.setdefault(key, (row, file))
    paths = []
    for (product, era, cadence), (row, file) in sorted(chosen.items()):
        path = H.DATA / campaign / str(row['star']) / file['file']
        guard.allow_design_file(path)
        Q.ENABLED = False
        before = S.load(str(path), info=True)
        Q.ENABLED = True
        after = S.load(str(path), info=True)
        # No old cadence may be lost, including paths unaffected by this policy.
        assert np.isin(before[0], after[0]).all()
        assert before[3]['product'] == after[3]['product']
        assert before[3]['column'] == after[3]['column']
        paths.append(dict(product=product, era=era, cadence_seconds=cadence,
                          before=len(before[0]), after=len(after[0])))
    mutations = []
    roster = json.loads((H.OUT / 'roster.json').read_text(encoding='utf-8'))
    candidates = [r for r in roster if r['campaign'] == campaign and r['cause'].endswith('load')]
    for row in candidates:
        for file in row['files']:
            if not file['finite_near'] or '4096' not in file['rejected_bits']:
                continue
            path = H.DATA / campaign / str(row['star']) / file['file']
            guard.allow_design_file(path)
            Q.ENABLED = False
            before = S.load(str(path), info=True)
            Q.ENABLED = True
            after = S.load(str(path), info=True)
            cad = np.median(np.diff(before[0]))
            supports = lambda t: bool(len(t) and np.min(abs(t - row['time'])) <= 1.5 * cad)
            assert not supports(before[0]), 'The baseline must fail the archived centre-support test'
            assert supports(after[0]), 'The candidate must pass the archived centre-support test'
            # Returning to the original loader is the explicit mutant.
            Q.ENABLED = False
            mutant = S.load(str(path), info=True)
            assert not supports(mutant[0]), 'The candidate acceptance test failed to reject the mutant'
            Q.ENABLED = True
            mutations.append(dict(trial=row['trial'], product=file['product'],
                                  before=False, after=True, reverted_mutant=False))
    # Known truth in this control comes from synthetic construction.
    # A 30-d binary in one sector has no repeated primary to rescue a wrong epoch.
    residue = []
    for cadence in (1800, 600, 200):
        t = np.arange(1000., 1027., cadence / 86400)
        rng = np.random.default_rng(25 + cadence)
        f = 1 + rng.normal(0, .001, len(t))
        shape = np.clip((4 / 24 - np.abs(t - 1004.)) / (.8 / 24), 0, 1)
        f -= .05 * shape
        q = np.where(shape > 0, 4096, 0)
        cat = dict(P=30., T0=1000., eP=0., eT0=0., wp=8 / 24, ws=8 / 24, phs=.5)
        old_keep = Q.flags_mask(q, False, 1, False)
        new_keep = Q.flags_mask(q, False, 1, True)
        retained = []
        for keep in (old_keep, new_keep):
            tt, ff = t[keep], f[keep]
            rm = PM.remove(tt, ff, [30.], cat)
            prods = S.Prod(tt[~rm], ff[~rm])
            near = [e for e in prods.events() if abs(e['center'] - 1004.) < 4 / 24]
            retained.append(bool(near))
        assert not retained[0] and retained[1], 'Wrong-epoch eclipse control no longer exposes the hazard'
        residue.append(dict(cadence_seconds=cadence, baseline_detected=retained[0],
                            candidate_detected=retained[1], true_source='synthetic deep eclipse'))
    result = dict(campaign=campaign, synthetic=checks, runtime_product_paths=paths,
                  archived_mutations=mutations, wrong_epoch_eclipse=residue)
    (H.OUT / f'checks-{campaign}.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(campaign, len(paths), 'product/era/cadence paths,', len(mutations),
          'archived mutations, three synthetic wrong-epoch controls', flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
