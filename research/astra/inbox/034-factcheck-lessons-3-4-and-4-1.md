# 034: fact-check Twinlight lessons 3.4 Doppler and 4.1 Eclipsing binaries

Written by Claude, 23 Nov 2026, 11:24 am Kuwait. GO: Ahmed, 22 Nov 9:30 pm and 23 Nov 10:43 am. Same job as your 018 and 022: an independent read for errors of fact, arithmetic, physics and teaching, with each finding checked by a script or a primary source. Both lessons are already live (Book 3.10.0 and 3.11.0) with "fact-check pending"; Claude fixes what you confirm.

## Read
- `book/docs/learn/u3/l4-doppler.md` and its plot script `book/tools/lesson_plots_u3c.py` (data `data/learn-sources/lick-51peg-rv/`, 354 Lick velocities of 51 Peg, Fischer et al. 2014, VizieR J/ApJS/210/5).
- `book/docs/learn/u4/l1-eclipsing-binaries.md` and `book/tools/lesson_plots_u4.py` (TIC 172900988, TESS sectors 44 to 47 SPOC light in `data/known/172900988/`; Kostov et al. 2021, arXiv 2105.08614).

- **Added 23 Nov 11:43 am:** `book/docs/learn/u4/l2-how-two-stars-orbit.md` (script `book/tools/lesson_plots_u4b.py`: omega 70.6 degrees from e cos(omega) = 0.149 and the sign from eclipse lengths 2.74 h and 7.27 h; separation 0.106 to 0.278 AU) and `book/docs/learn/u4/l4-planets-around-two-suns.md` (relative-speed reading of the 0.4 d and 0.27 d dips; dilution depth; the Doyle et al. 2011 citation). Check these the same way, including whether the omega sign argument is sound and whether its convention matches the separation plot.

## Check (each with the evidence named)
1. Every number in both lessons: recompute it (problems, worked examples, hints, `data-why`, answers and tolerances; would a correct answer be rejected or a common wrong one accepted?).
2. Physics: Doppler formula and signs; centre of mass rule and the Jupiter and Earth examples; the m sin i formula and its assumptions; minimum mass; the iodine-cell sentence; the 1995 discovery and the 2019 Nobel sentence; whether "51 Pegasi b has never been seen to transit" is still true (primary source).
3. Eclipses: the depth rule and its limb-darkening caveat; the claim that nearly equal temperatures cannot explain 43.5% against 35.8%; the first-order timing rule (2/pi) e cos(omega) (give a primary or textbook source for it, and say whether the factor needs (1 + 1/sin^2 i) or similar for this system); the exact e cos(omega) = 0.149 (re-derive independently, not by importing our script); the eclipse depths and the 11.879 d separation from the light (your own short script).
4. Teaching: anything a beginner would misread; any claim stated more strongly than its source.
5. House rules: no en or em dashes; sources listed; no hunt-list star (fence A or B) anywhere.

## Report
`research/astra/reports/034-report.md`: one row per finding (lesson, line, what is wrong, evidence, suggested fix, severity). Read-only on the book: do not edit lessons. Data only under `data/astra/034/`; branch `astra/034-factcheck-3-4-4-1`. Meter before and after, logged in `research/astra/USAGE.md`.
