"""Fixed D1 study switch. Duration selects both detector and diagnostic curve.

All candidates compete before non-overlap suppression. Rank by SNR/threshold.
The extreme cuts dispatch to the unmodified B or 030 N1 implementation.
"""
import ast
import importlib
from pathlib import Path


def endpoint(cut, grid):
    return 'B' if cut < min(grid) else 'N1' if cut >= max(grid) else 'D1'


def install(S2, S3, cut=8.):
    assert Path(S2.__file__).parent.parent.name == '031'
    N = importlib.import_module('031_notch')
    route = endpoint(cut, S2.DURS_H)
    if route == 'B':
        return route
    original_prod, original_veto = S2.Prod, S2.veto
    N.install(S2, enabled=True, floor=4.5)
    notch_prod = S2.Prod
    if route == 'N1':
        return route
    np = S2.np

    class DurationProd(original_prod):
        def __init__(self, t, f, sign=1):
            self.base = original_prod(t, f, sign)
            self.notch = notch_prod(t, f, sign)
            self.t, self.f = self.base.t, self.base.f
            # Only event-free diagnostic helpers use the default B attributes.
            self.bt, self.bf, self.bd, self.med = self.base.bt, self.base.bf, self.base.bd, self.base.med

        def for_duration(self, duration):
            return self.notch if duration <= cut else self.base

        def scores(self, duration):
            return self.for_duration(duration).scores(duration)

        def events(self, thr=None):
            assert thr is None, 'D1 thresholds are fixed by statistic'
            candidates = []
            for duration in S2.DURS_H:
                product = self.for_duration(duration)
                threshold = 6.5 if duration <= cut else 7.
                centers, snr, mean = product.scores(duration)
                for i in np.flatnonzero(np.isfinite(snr) & (snr >= threshold)):
                    depth = (product.depths[duration][i] if duration <= cut else product.meds.get(duration, product.med)-mean[i])*1e6
                    candidates.append((snr[i]/threshold, centers[i], duration, depth, snr[i]))
            candidates.sort(reverse=True)
            events = []
            for _, center, duration, depth, snr in candidates:
                if all(abs(center-e['center']) > .5*max(duration, e['dur_h'])/24+.1 for e in events):
                    events.append(dict(center=float(center), dur_h=duration, snr=float(snr), depth_ppm=float(depth)))
            return events

    def veto(events, edges, dumps, opposite, flip_action='reject'):
        accepted, rejected = [], []
        for event in events:
            if event['dur_h'] > cut:
                keep, reject = original_veto([event], edges, dumps, opposite, flip_action)
            else:
                keep, reject = original_veto([event], edges, dumps, [], 'flag')
                if N.mirrored(event, opposite):
                    if flip_action == 'reject':
                        keep, reject = [], [dict(event, veto='matched in flipped data')]
                    else:
                        keep[0]['flags'].append('matched in flipped data')
            accepted.extend(keep)
            rejected.extend(reject)
        return accepted, rejected

    S2.Prod, S2.veto = DurationProd, veto
    # Preserve B rounding for long boxes and N1 precision for short boxes.
    tree = ast.parse(Path(S2.__file__).read_text(encoding='utf-8'))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'do_group')
    source = ast.unparse(fn)
    # Save exact reverse mirror evidence now. Long-box serialization rounds the
    # centre, so mixed short/long mirrors cannot later use B's forward-flag trick.
    old = "veto(flip, d['edges'], dumps, [], flip_action='flag')"
    assert source.count(old) == 1
    source = source.replace(old, "veto(flip, d['edges'], dumps, real, flip_action='flag')")
    for field, digits in (('snr', 2), ('center', 4)):
        old = f"round(e['{field}'], {digits})"
        assert source.count(old) == 1
        source = source.replace(old, f"(e['{field}'] if e['dur_h'] <= {cut!r} else {old})")
    exec(compile(source, '<031 duration serialization>', 'exec'), S2.__dict__)
    # Step-shape measurements must use the selected statistic's own detrend.
    tree = ast.parse(Path(S3.__file__).read_text(encoding='utf-8'))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'add_step')
    source = ast.unparse(fn)
    assert source.count('P = cache[key]') == 1
    source = source.replace('P = cache[key]', "P = cache[key].for_duration(e['dur_h'])")
    exec(compile(source, '<031 duration step curve>', 'exec'), S3.__dict__)
    return route
