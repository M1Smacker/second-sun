"""Count actual retained nonzero quality flags on one design file per runtime path."""
from collections import Counter
import importlib
import inspect
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
    import lightkurve as lk
    from lightkurve.io.qlp import read_qlp_lightcurve
    from lightkurve.utils import TessQualityFlags
    import stage2_search as S
    Q = importlib.import_module('025_loader')
    trace = json.loads((H.OUT / f'trace-{campaign}.json').read_text(encoding='utf-8'))
    chosen = {}
    for row in trace['rows']:
        for file in row['files'] + row.get('alternatives', []):
            era = 'pre56' if row['sector'] < 56 else '56to93' if row['sector'] < 94 else '94plus'
            key = file['product'], era, round(file['cadence_min'] * 60)
            observed_high_bit = any(int(word) & 2 ** 29 for word in file['quality_words'])
            if key not in chosen or observed_high_bit:
                chosen[key] = row, file
    result = []
    for (product, era, cadence), (row, file) in sorted(chosen.items()):
        path = H.DATA / campaign / str(row['star']) / file['file']
        guard.allow_design_file(path)
        lc = lk.read(str(path), quality_bitmask='none')
        tt = lc.time.value
        q = np.asarray(lc.quality.value, np.int64)
        arms = []
        for enabled in (False, True):
            Q.ENABLED = enabled
            loaded = S.load(str(path), info=True)[0]
            selected = np.isin(tt, loaded)
            kept = q[selected]
            bits = {str(1 << b): int(np.count_nonzero(kept & (1 << b)))
                    for b in range(32) if np.any(kept & (1 << b))}
            expected = Q.flags_mask(q, product == 'QLP', row['sector'], enabled)
            assert np.all(expected[selected]), 'Returned timestamp violates the declared mask'
            arms.append(dict(kept=len(loaded), kept_nonzero=int(np.count_nonzero(kept)), bits=bits))
        result.append(dict(product=product, era=era, cadence_seconds=cadence, baseline=arms[0], candidate=arms[1]))
    source, first_line = inspect.getsourcelines(read_qlp_lightcurve)
    evidence = dict(lightkurve_version=lk.__version__, hard_mask=int(TessQualityFlags.HARD_BITMASK),
                    QLP_reader_first_line=first_line, QLP_reader_source=''.join(source),
                    flag_labels=TessQualityFlags.STRINGS, paths=result)
    (H.OUT / f'quality-audit-{campaign}.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
    print(campaign, len(result), 'actual kept-quality path checks', flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
