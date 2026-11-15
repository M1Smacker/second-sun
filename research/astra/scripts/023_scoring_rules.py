"""Repeater and symmetric-coincidence scoring rules from brief 006."""
from itertools import combinations
import math

TIERS = {"1A", "1L", "1B"}


def binary_members(events, period):
    if not math.isfinite(period) or period <= 0:
        return set(range(len(events))) if len(events) >= 3 else set()

    def locked(a, b):
        separation = abs(a['center'] - b['center'])
        cycles = round(separation / period)
        return cycles >= 1 and abs(separation - cycles * period) <= 1 / 24

    members = set()
    for triple in combinations(range(len(events)), 3):
        if all(locked(events[a], events[b]) for a, b in combinations(triple, 2)):
            members.update(triple)
    return members


def symmetric_matches(real, flips, radius):
    """Recover reverse matches using the saved forward flags at rounding boundaries."""
    matched, possible = set(), set()
    uncertainty = .0001000001
    for event in real:
        distances = [abs(event['center'] - flip['center']) for flip in flips]
        certain = {i for i, d in enumerate(distances) if d < radius - uncertainty}
        boundary = {i for i, d in enumerate(distances) if abs(d - radius) <= uncertainty}
        if not event['flipmatch']:
            if certain:
                raise RuntimeError('Saved forward coincidence flag contradicts candidate distances')
            continue
        if not certain and not boundary:
            raise RuntimeError('Saved forward coincidence has no possible partner')
        if not certain and len(boundary) == 1:
            certain = boundary
        else:
            possible.update(boundary)
        matched.update(certain)
    return matched, possible - matched
