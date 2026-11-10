"""C2 event-stage cross-sector phase veto (10 Nov 2026, Opus 5.5). Design note: research/fable-audit-2026-11/DESIGN-C2-OPUS-2026-11-10.md.
An event of one arm in the current sector is VETOED if the same star has an event of the SAME arm in a DIFFERENT sector at the same binary phase
(catalogue epoch + each sector's primary offset from the deep primary eclipse), with a similar duration (factor DUR_R) and depth (factor DEP_R).
Only for slow binaries (P >= PSLOW). The same code runs on both arms (real dips against real dips, upside-down bumps against upside-down bumps).
It removes EVENTS, never cadences, so a planet dip always stays in the light the search sees."""
import os, re
import numpy as np, pandas as pd

TOL_H = float(os.environ.get("C2_TOL_H", "2.0"))
DUR_R, DEP_R, PSLOW = 2.5, 3.0, 13.0
NMIN = int(os.environ.get("C2_NMIN", "2"))


def phase(center, P, T0, off):
    return ((center - T0 - off) / P) % 1.0


def veto(events, others, P, T0=0.0, off=0.0, tol_h=None):
    """events: list of event dicts (center, dur_h, depth_ppm) of ONE arm in the current sector; others: list of (phase, dur_h, depth_ppm) of the SAME arm in
    the star's other sectors. Returns (kept, vetoed)."""
    tol_h = TOL_H if tol_h is None else tol_h
    if not np.isfinite(P) or P < PSLOW or not others:
        return list(events), []
    kept, vet = [], []
    secs = {o[3] for o in others if len(o) > 3}
    nmin = NMIN if len(secs) >= 3 else 1                      # a star with 3+ other sectors: a real eclipse returns in at least NMIN of them; one chance partner is not enough
    for e in events:
        ph = phase(e["center"], P, T0, off); d1, a1 = e["dur_h"], abs(e["depth_ppm"]) + 1e-9
        hits = set()
        for o in others:
            p2, d2, a2 = o[0], o[1], abs(o[2]) + 1e-9
            dist_h = min(abs(ph - p2), 1 - abs(ph - p2)) * P * 24
            if dist_h < (d1 + d2) / 2 + tol_h and max(d1, d2) <= DUR_R * min(d1, d2) and max(a1, a2) <= DEP_R * min(a1, a2):
                hits.add(o[3] if len(o) > 3 else len(hits))
        (vet if len(hits) >= nmin else kept).append(e)
    return kept, vet


def sector_of(name):
    m = re.search(r"[-_]s(\d{4})[-_]", name)
    return int(m.group(1)) if m else None
