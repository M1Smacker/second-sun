"""S1 sensitivity under the full filed rule (FIX 86, Claude, 14 Nov 2026). Replaces r1_readout.power_note, which used the UNSTRATIFIED
Fisher test for a STRATIFIED verdict and called the result what "would have been seen" (an exclusion). Codex brief 002 part B design:
the filed background tables are frozen; D extra real events (all assumed to clear every SNR bar and reach tier 1: an optimistic
strong-event scenario) are spread over the period bins in proportion to the sealed bar-7 totals, N placements per dose, doses 0 to 200
in steps of 5; the FULL rule is applied to each placement (stratified exact chance <= alpha at bar 7 AND sealed real above the
count expected from the seen share at bars 8, 10 and 12). Reports the first doses where the rule fires in at least 50% and 90% of
placements, as a multiple of the original bar-7 stratified expectation. This is a conditional sensitivity under stated assumptions,
NOT survey power and NOT an exclusion: noise counts, the reference and star correlations are not resampled.
rows: {bar: [(real_sealed, flip_sealed, real_seen, flip_seen) per bin]}; strat_exact: the readout's exact stratified test."""
import numpy as np

BARS = (7, 8, 10, 12)


def expected(tabs):
    return sum((rs + fs) * rr / (rr + fr) if rr + fr else 0.0 for rs, fs, rr, fr in tabs)


def fires(tables, strat_exact, alpha):
    return strat_exact(tables[7]) <= alpha and all(sum(t[0] for t in tables[b]) > expected(tables[b]) for b in BARS[1:])


def curve(tables, strat_exact, alpha=0.005, n=500, seed=20261114, doses=range(0, 201, 5)):
    rng = np.random.default_rng(seed)
    w = np.array([rs + fs for rs, fs, _, _ in tables[7]], float)
    w = w / w.sum() if w.sum() else np.full(len(w), 1 / len(w))
    cache, out = {}, []
    for dose in doses:
        hits = 0
        for added in rng.multinomial(dose, w, size=n):
            key = tuple(added)
            if key not in cache:
                planted = {b: [(r + int(a), f, rr, fr) for (r, f, rr, fr), a in zip(tables[b], added)] for b in BARS}
                cache[key] = fires(planted, strat_exact, alpha)
            hits += cache[key]
        out.append((dose, hits / n))
    return out


def crossings(tables, strat_exact, alpha=0.005, n=500, seed=20261114):
    c = curve(tables, strat_exact, alpha, n, seed)
    r7 = sum(t[0] for t in tables[7]); e7 = expected(tables[7])
    res = {}
    for q in (0.5, 0.9):
        first = next(((d, p) for d, p in c if p >= q), None)
        res[q] = None if first is None else dict(added=first[0], rate=first[1], total_real=r7 + first[0], multiple=(r7 + first[0]) / e7 if e7 else float("nan"))
    return res, e7


def note(tables, strat_exact, alpha=0.005, n=500, seed=20261114):
    res, e7 = crossings(tables, strat_exact, alpha, n, seed)
    parts = []
    for q in (0.5, 0.9):
        x = res[q]
        parts.append(f"{int(q * 100)}% of placements: not reached by 200 added" if x is None else
                     f"{int(q * 100)}% of placements at {x['added']} added (sealed real about {x['total_real']}, {x['multiple']:.1f} times the stratified expectation {e7:.1f})")
    return ("sensitivity (FIX 86; conditional, NOT an exclusion): adding strong tier-1 real events spread over the period bins like the sealed bar-7 events, "
            f"the full Amendment 3 rule fires in " + "; in ".join(parts) + f" ({n} placements per dose, steps of 5; noise, reference and star correlations not resampled)")
