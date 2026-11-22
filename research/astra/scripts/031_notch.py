"""N1 study switch for redirected modules only. Off leaves every object untouched.

The detector follows RS-039 A8b. Its box depth, not its median-centred detection
score, supplies the depth used by the existing tier rules.
"""
import ast
from pathlib import Path


def scores(np, bt, bf, bd, duration):
    w = max(int(round(duration * 60 / (bd * 1440))), 1)
    gap = max(int(round(.25 * w)), 1)
    flank = max(int(round(1.5 * w)), 1)
    valid = np.isfinite(bf)
    cn = np.r_[0, np.cumsum(valid)]
    cf = np.r_[0., np.cumsum(np.where(valid, bf, 0.))]
    n = len(bf)
    def mean(a, b):
        a, b = np.clip(a, 0, n), np.clip(b, 0, n)
        count = cn[b] - cn[a]
        return np.where(count > 0, (cf[b] - cf[a]) / np.maximum(count, 1), np.nan), count
    i = np.arange(n)
    box, kb = mean(i, i + w)
    left, kl = mean(i - gap - flank, i - gap)
    right, kr = mean(i + w + gap, i + w + gap + flank)
    good = (kb >= .8 * w) & (kl >= .6 * flank) & (kr >= .6 * flank)
    depth = np.where(good, np.fmin(left, right) - box, np.nan)
    center = bt + (w - 1) * bd / 2
    finite = np.isfinite(depth)
    snr = np.full(n, np.nan)
    if finite.sum() >= 20:
        median = np.median(depth[finite])
        sigma = 1.4826 * np.median(abs(depth[finite] - median))
        if np.isfinite(sigma) and sigma > 0:
            snr = (depth - median) / sigma
    return center, snr, depth


def mirrored(event, opposite):
    return any(abs(event['center'] - other['center']) <= .25 * event['dur_h'] / 24
               for other in opposite)


def install(S2, enabled=False, floor=4.5):
    if not enabled:
        return
    assert Path(S2.__file__).parent.name == 'source'
    assert Path(S2.__file__).parent.parent.name == '031'
    assert floor in (4.5, 5., 5.5, 6., 6.5, 7.)
    np = S2.np
    original = S2.Prod
    class NotchProd(original):
        def __init__(self, t, f, sign=1):
            self.t, self.f = t, (f if sign == 1 else 2 - f)
            tt, ff = S2.detrend(self.t, self.f, window_d=5.)
            self.bd = S2.bin_width(tt)
            self.bt, self.bf = S2.bin10(tt, ff, self.bd)
            self.med = np.nanmedian(self.bf)
            self.meds, self.cache, self.depths = {}, {}, {}

        def scores(self, duration):
            if duration not in self.cache:
                c, s, depth = scores(np, self.bt, self.bf, self.bd, duration)
                self.depths[duration] = depth
                self.cache[duration] = c, s, self.med - depth
            return self.cache[duration]

        def events(self, thr=None):
            threshold = floor if thr is None else thr
            candidates = []
            for duration in S2.DURS_H:
                centers, snr, _ = self.scores(duration)
                for i in np.flatnonzero(np.isfinite(snr) & (snr >= threshold)):
                    candidates.append((snr[i], centers[i], duration, self.depths[duration][i] * 1e6))
            candidates.sort(reverse=True)
            events = []
            for snr, center, duration, depth in candidates:
                if all(abs(center - e['center']) > .5 * max(duration, e['dur_h']) / 24 + .1 for e in events):
                    events.append(dict(center=float(center), snr=float(snr), dur_h=duration, depth_ppm=float(depth)))
            return events
    old_veto = S2.veto
    def veto(events, edges, dumps, opposite, flip_action='reject'):
        kept, _ = old_veto(events, edges, dumps, [], flip_action='flag')
        accepted, rejected = [], []
        for event in kept:
            if mirrored(event, opposite):
                if flip_action == 'reject':
                    rejected.append(dict(event, veto='matched in flipped data'))
                    continue
                event['flags'].append('matched in flipped data')
            accepted.append(event)
        return accepted, rejected
    S2.Prod, S2.veto = NotchProd, veto
    # Keep exact score and centre through threshold filtering and the short mirror
    # radius. This changes only N1 serialization, never the off-switch path.
    tree = ast.parse(Path(S2.__file__).read_text(encoding='utf-8'))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'do_group')
    source = ast.unparse(function)
    for expression in ("round(e['snr'], 2)", "round(e['center'], 4)"):
        assert source.count(expression) == 1
        source = source.replace(expression, expression[6:expression.rindex(',')])
    scope = S2.__dict__
    exec(compile(source, '<031 N1 do_group serialization>', 'exec'), scope)
    S2._n1_enabled = True
