"""Vesper study: does a flag matter less for strong dips? Tier 1 would also pass an event with SNR >= X whose ONLY flags are in a waivable set (second-product disagreement is never waived).
Prints, per set, upside-down tier-1 per 1,000 star-sectors (rule 8 or fewer) and injected dips gained over the baseline, for X from 9 to 16 and two waivable sets. Dev data only; aggregates only.
Usage: python snr_waiver.py   (appends to research\stage3\snr-waiver.txt)"""
import numpy as np, pandas as pd
import flag_patterns as F

# the same pattern key as flag_patterns: FL + tier3; snr comes from the two loaders below
SETS = {"all but common, flipmatch": {"gap_dump", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated"},
        "gap_dump, step, ramp, repeater": {"gap_dump", "step", "ramp", "repeater"},
        "step only": {"step"}}


def passes(pat, snr, X, waive):
    if pat is None or pat[-1]:
        return False
    on = {n for n, v in zip(F.NAMES, pat) if v}
    return not on or (snr >= X and on <= waive)


def main():
    out = []
    for name in ("g1", "g2"):
        n, flips, b = F.load(name); fs = F.LAST[name]
        base = b.tier.isin(["1A", "1L", "1B"])
        for wname, waive in SETS.items():
            for X in (9, 10, 12, 14, 16):
                fl = sum(passes(p, s, X, waive) for p, s in zip(flips, fs))
                op = np.array([passes(p, s, X, waive) for p, s in zip(b.pat, b.snr)])
                ga, lo = int((op & ~base.values).sum()), int((~op & base.values).sum())
                out.append(f"{name} waive [{wname}] at SNR >= {X}: upside-down tier-1 {fl} = {1000 * fl / n:.2f} per 1,000; injected dips gained {ga}, lost {lo} of {len(b)} ({100 * ga / len(b):+.1f} points)")
    print("\n".join(out)); open("../research/stage3/snr-waiver.txt", "a", encoding="utf-8").write("\n".join(out) + "\n")


main()
