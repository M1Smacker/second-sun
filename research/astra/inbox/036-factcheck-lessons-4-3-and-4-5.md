# 036: fact-check Twinlight lessons 4.3 and 4.5

Written by Claude, 24 Nov 2026, 11:33 pm Kuwait. GO: Ahmed, 24 Nov 11:05 pm. Runs AFTER 035. Same job as your 034 and 034b (they were excellent: independent scripts, primary sources, the grader run for real). Tree node 4.1.

## Read
- `book/docs/learn/u4/l3-measuring-stars.md` and `book/tools/lesson_plots_u4c.py`: trapezoid fits give full eclipse lengths 5.37 and 13.25 h; sky speeds 169.0 and 68.6 km/s from h / r; R1 + R2 at least 2.35 Sun radii from both; with Kostov's i = 89.4182 and R1 + R2 = 2.70 the predicted contact lengths are 6.15 and 14.86 h; offsets at 88 and 85 degrees.
- **Added 11:45 pm:** `book/docs/learn/u5/l2-how-tess-watches.md` and `book/tools/lesson_plots_u5b.py` (sector 46 gaps raw 1.39 d and usable 2.74 d; targets per sector, hemispheres, 601,177 stars, median 2 sectors; HEASARC telescope facts). Check every number from the files and the HEASARC page. Also `u5/l3-pixels-to-light-curves.md` and `book/tools/lesson_plots_u5c.py` (aperture 20 of 121 pixels, background 11.7%, CROWDSAP / FLFRCSAP = PDCSAP / SAP; Stumpe 2012). And `u5/l4-what-goes-wrong.md` with `book/tools/lesson_plots_u5d.py` (quality flags by bit, background surge 29,166 against 2,482; check the meaning given for each flag, especially momentum dump and Argabrightening, against TESS documentation).
- `book/docs/learn/u4/l5-stability-and-rarity.md` and `book/tools/lesson_plots_u4d.py`: Holman and Wiegert 1999 fit, a_crit / a_bin = 3.516, a / a_crit = 1.335, P_crit 129.6 d; Martin, Mazeh and Fabrycky 2015; Armstrong et al. 2014.

## Check (each with evidence)
1. Every number, hint, answer and tolerance, with the real grader (your `check_034b_grader.cjs` approach; `book/tools/test_learn_grader.mjs` now exists too).
2. 4.3 physics: is (vT/2)^2 + (r cos i)^2 = (R1 + R2)^2 right for an eccentric orbit at conjunction (sky speed h / r, offset r cos i)? Is the trapezoid's total length a fair "first to last contact", and is limb darkening a sound LIKELY explanation for the 12% shortfall (measure it if you can: a limb-darkened model of the same eclipse)? Is the claim "at 85 degrees the far eclipse would not happen" right?
3. 4.5: the Holman and Wiegert coefficients against the paper itself (not a summary), and their stated validity range (e, mu, and what "critical" means: the paper's survival criterion and time span). The 10% (+18, -6.5) and its conditions; the 7-day statement; any claim stated more strongly than its source (for example "most known circumbinary planets sit near the edge", and "its orbit turns fastest close to the edge").
4. House rules: no en or em dashes, sources listed, no fence A or B star.

## Rules
Read-only on the book. Data only under `data/astra/036/`. Branch `astra/036-factcheck-4-3-4-5`. At most 1 worker. Report `research/astra/reports/036-report.md`, one row per finding, labels CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED; meter before and after in `research/astra/USAGE.md`; stop near 80% of the 5-hour meter with a checkpoint.
