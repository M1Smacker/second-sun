# 035b: continue the Census period finder (after your 035 PARTIAL)

Written by Claude, 24 Nov 2026, 11:41 pm Kuwait. GO: Ahmed, 24 Nov 11:05 pm. Continues 035 on a new branch made from main (035 is merged: your scripts and private data are there). Tree node 2.1.

## Claude's read of your 035 report
Your stop was right: two fixes failed, so you diagnosed instead of guessing. The likely design gap: a box search finds A period, but 0.1% accuracy should not come from the search grid at all. It should come from the eclipse times. You already own a validated tool for that: eclipse timer v3 (032/032b), which fits a straight line to measured eclipse times and predicted held-out sectors for 67 of 70 tracks.

## Do now
1. **Two stages.** Stage 1, the box search, gives a coarse period and epoch only. Stage 2 measures each eclipse's time with the unchanged 032 measurement functions (AST-checked as before), resolves the half or double alias (odd/even depths, secondary phase), and fits the linear ephemeris with 032's error model. Report the Stage 2 period. Rerun `035_test.py`: the normal arm must reach 0.1% on the 4-day synthetic, and the broken-alias mutation must still fail. If Stage 2 still misses 0.1%, trace the failing path end to end (widths, grid, epoch convention) and stop with the trace; do not loosen the gate.
2. **Truth-side eclipse count, before validation** (your own point, adopted): for each of the 150 stars, count from the CATALOGUE ephemeris and the sector time spans how many primary eclipses fall inside the data. Stars with 3 or more define the 85% denominator, whatever the finder does. Write this count to `data/astra/035/truth_counts.json` before any finder output on real light exists.
3. **Light for the 114 stars without local files:** download their SPOC 2-minute light curves from MAST (lightkurve or astroquery, one worker, retries) into `data/astra/035/lc/`. At most 2 GB. Report files, bytes and failures (Claude tells Ahmed and logs `research/downloads.csv`).
4. **Then the preregistered validation** of 035, unchanged: per band, period within 0.1% for at least 85% of stars with 3 or more eclipses; half or double under 5%; every single-eclipse star flagged with no period.

## Rules
As 035: AGENTS.md; no pipeline or frozen edits; no planet search; at most 2 workers, NUMBA_NUM_THREADS=1. Data only under `data/astra/035/`. Report `research/astra/reports/035b-report.md`, plain verdict first (PASS, FAIL or PARTIAL per band). Meter before and after; stop near 80% of the 5-hour meter with a checkpoint.
