"""Restricted circular orbit search, no pipeline or data access.

Inputs contain candidates only, never planted orbital parameters. Roots are
pair-anchored templates; all compatible integer cycle gaps are enumerated.
"""
import math
from itertools import combinations
import numpy as np
from scipy.optimize import brentq

MU = 1/3
TOL = .1
FLOOR = 4.


def stability_ratio(mu=MU):
    return (1.60 + 4.12*mu - 5.09*mu*mu)**1.5


def corrected(times, period, binary_period, binary_epoch):
    rho = MU*(binary_period/period)**(2/3)
    return times-period/(2*math.pi)*np.arcsin(rho*np.sin(2*math.pi*(times-binary_epoch)/binary_period))


def speed(times, period, binary_period, binary_epoch):
    phase = 2*math.pi*(times-binary_epoch)/binary_period
    rho = MU*(binary_period/period)**(2/3)
    # Relative transverse speed divided by binary semimajor axis / day.
    return np.abs(2*math.pi*((period/binary_period)**(2/3)/period *
                            np.sqrt(1-(rho*np.sin(phase))**2) - MU/binary_period*np.cos(phase)))


def dedup(events):
    """One candidate per physical crossing across overlapping sector products."""
    keep = []
    for e in sorted(events, key=lambda x: (-x['snr'], x['center'], x.get('sector', 0))):
        if all(abs(e['center']-r['center']) > .1+max(e['dur_h'],r['dur_h'])/48 for r in keep):
            keep.append(e)
    return sorted(keep, key=lambda x: x['center'])


def search(events, binary_period, binary_epoch, mutation=False):
    """Return unique sets and every retained set's strongest pair template.

    At each template, scan every factor-two duration window. Within each
    cycle choose the strongest event, then scan descending-score prefixes.
    This finite subset policy is part of the search and null calibration.
    """
    ev = dedup([e for e in events if e['snr'] >= FLOOR])
    empty = dict(sets=[], templates=0, candidates=len(ev), max_score=0.)
    if len(ev)<3 or not all(map(math.isfinite, (binary_period,binary_epoch))) or binary_period<=0:
        return empty
    t = np.array([e['center'] for e in ev])
    d = np.array([e['dur_h']/24 for e in ev])
    score = np.minimum(7., np.array([e['snr'] for e in ev]))
    pmin, pmax = 4*binary_period, 8*binary_period
    assert pmin/binary_period > stability_ratio()
    maxshift = pmax/(2*math.pi)*math.asin(MU*(binary_period/pmax)**(2/3))
    templates = 0
    sets = {}
    def consider(period, epoch):
        nonlocal templates
        templates += 1
        u = corrected(t,period,binary_period,binary_epoch)
        cycles = np.rint((u-epoch)/period).astype(int)
        valid = np.ones(len(t),bool) if mutation else np.abs(u-epoch-cycles*period)<=TOL+1e-9
        chord = d*speed(t,period,binary_period,binary_epoch)
        valid &= np.isfinite(chord) & (chord>1e-10)
        # At most one event per orbital cycle. Timing bypass is the mutation.
        ix = np.flatnonzero(valid)
        if len(set(cycles[ix]))<3:
            return
        for lower in sorted(set(chord[ix])):
            subset = ix[(chord[ix]>=lower-1e-12)&(chord[ix]<=2*lower+1e-12)]
            best = {}
            for j in subset:
                cyc = int(cycles[j])
                if cyc not in best or score[j]>score[best[cyc]]:
                    best[cyc]=int(j)
            order = sorted(best.values(),key=lambda j:(-score[j],t[j]))
            total = 0.
            for n,j in enumerate(order,1):
                total += score[j]
                if n<3:
                    continue
                members = tuple(sorted(order[:n]))
                value = float(total/math.sqrt(n))
                old = sets.get(members)
                if old is None or value>old['score']:
                    sets[members] = dict(score=value, period=float(period), epoch=float(epoch),
                        events=[ev[k] for k in members], cycles=[int(cycles[k]) for k in members])
    for i,j in combinations(range(len(t)),2):
        gap = t[j]-t[i]
        lo = max(1, math.ceil((gap-2*maxshift)/pmax))
        hi = math.floor((gap+2*maxshift)/pmin)
        for k in range(lo,hi+1):
            def fun(p):
                u = corrected(t[[i,j]],p,binary_period,binary_epoch)
                return float(u[1]-u[0]-k*p)
            a,b = fun(pmin),fun(pmax)
            if a*b>0:
                continue
            p = brentq(fun,pmin,pmax,xtol=1e-10)
            consider(p,float(corrected(t[i],p,binary_period,binary_epoch)))
    result = list(sets.values())
    return dict(sets=result, templates=templates, candidates=len(ev),
                max_score=max((r['score'] for r in result),default=0.))


def members(result, floor, promotion=False):
    out = {}
    for group in result['sets']:
        if group['score'] < floor:
            continue
        for e in group['events']:
            if not promotion or e['snr']>=7:
                out[(e.get('sector'),e['center'],e['dur_h'])] = e
    return list(out.values())
