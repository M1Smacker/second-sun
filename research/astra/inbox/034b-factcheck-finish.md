# 034b: finish the fact-check of lessons 3.4, 4.1, 4.2 and 4.4

Written by Claude, 24 Nov 2026, 11:08 pm Kuwait. GO: Ahmed, 24 Nov 11:05 pm ("push the weekly cap to 14%... start working"). This continues your 034 (report `research/astra/reports/034-report.md`, merged). Your 5 confirmed findings were re-derived by Claude and fixed in Book 3.11.0 (FIX 103, commit b15147ea): read the current lesson text, not the old one.

## What changed since 034
- 4.2 now calls 0.192 AU the semi-major axis (midway between nearest and farthest; time average 0.211 AU stated), and 106 km/s a circular speed scale (true mean about 101 km/s).
- 4.4 uses chord / |v_planet - v_star| with projected, steady velocities; the reading now says both stars moved against the planet (about 7 and 29 km/s) in the central-crossing model.
- 4.1 problem 5 no longer calls 0.15 exact.

## Do now: your own list of six unchecked groups, in this order
1. Grading: every `data-answer`, `data-tol`, `data-unit` and hint in the four lessons, tested against the real grader in `book/docs/assets/learn.js` (extract the compare logic, run it in node or reimplement it exactly and say which). Would a correct answer be rejected, or a common wrong one accepted?
2. Raw eclipse light: TIC 172900988, sectors 44 to 47 SPOC 2-minute files already in `data/known/172900988/` (no download). Check the id against fences A and B first and report the check. Measure the two eclipse depths, centres, the 11.879 d separation and half-depth widths with your own short script.
3. The first-order timing rule (2/pi) e cos(omega): a primary or textbook source, and whether this system needs the inclination term. Then the omega sign argument from the eclipse lengths (2.74 h and 7.27 h), with impact parameter considered, and whether its convention matches the separation plot in `book/tools/lesson_plots_u4b.py`.
4. Lick 51 Peg: refit the 354 velocities in `data/learn-sources/lick-51peg-rv/` yourself (period, K, scatter); check the 1995 discovery, 2019 Nobel, iodine-cell and "never seen to transit" sentences against primary sources.
5. Physical caveats you listed (TESS band vs bolometric light, the temperature argument for unequal depths, the Doyle et al. 2011 citation and the slow turning of the planet's orbit tilt).
6. Fence and identifier audit of the four lessons and their plot JSON in `book/docs/assets/data/lessons/`.

## Rules
Read-only on the book. Data only under `data/astra/034b/`. Branch `astra/034b-factcheck-finish`. Meter before and after in `research/astra/USAGE.md`; stop near 80% of your 5-hour meter with a checkpoint report. A D1 bench (031) is running on 3 workers: use at most 1 worker and NUMBA_NUM_THREADS=1. Report `research/astra/reports/034b-report.md`, one row per finding (lesson, line, what, evidence, fix, severity), labelled CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED.
