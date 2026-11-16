"""Predeclared M4 mask and event hold. No pipeline imports or file writes."""
from itertools import combinations
import math


def drift(c, time):
    e0 = c.get('eT0', 0)
    ep = c.get('eP', 0)
    e0 = e0 if math.isfinite(e0) else 0
    ep = ep if math.isfinite(ep) else 0
    return 3 * math.hypot(e0, round((time - c['T0']) / c['P']) * ep)


def category(c, time):
    if c is None or not all(math.isfinite(c.get(k, math.nan)) for k in ('P', 'T0', 'wp')) or c['wp'] <= 0:
        return 'unknown'
    return 'B' if drift(c, time) > c['wp'] else 'A'


def m2_windows(t, c, offset, np):
    # Exact historical 010 V2 arithmetic, including unshifted drift cycle.
    p, epoch = c['P'], c['T0']
    secondary = np.isfinite(c['phs']) and np.isfinite(c['ws'])
    ep = c['eP'] if np.isfinite(c['eP']) else 0
    e0 = c['eT0'] if np.isfinite(c['eT0']) else 0
    result = np.zeros(len(t), dtype=bool)
    for phase, width in ((0, c['wp']), (c['phs'], c['ws']) if secondary else (.5, c['wp'])):
        cycles = np.round((t - epoch - offset) / p - phase)
        centers = epoch + offset + (cycles + phase) * p
        half = .75 * width + np.minimum(3 * np.hypot(e0, np.round((t - epoch) / p - phase) * ep), width)
        result |= np.abs(t - centers) <= half
    return result, secondary


def reason(events, cap):
    """One host, one arm. Caller passes primary SNR>=7 events from all sectors."""
    unique = []
    for event in sorted(events, key=lambda e: -e['snr']):
        if not any(abs(event['center'] - e['center']) <= max(event['dur_h'], e['dur_h']) / 48 for e in unique):
            unique.append(event)
    if cap is not None and any(e['depth_ppm'] > cap for e in unique):
        return 'above_host_cap'
    unique.sort(key=lambda e: e['center'])
    for a, b, c in combinations(unique, 3):
        depths = [e['depth_ppm'] for e in (a, b, c)]
        if min(depths) <= 0 or max(depths) > 1.3 * min(depths):
            continue
        if abs(b['center'] - (a['center'] + c['center']) / 2) <= 1 / 24:
            return 'three_periodic'
    return None


def held(events, cap, class_b):
    why = reason(events, cap) if class_b else None
    return [dict(e, timing_unverified=bool(why), timing_reason=why,
                 tier='2' if why else e.get('tier')) for e in events]
