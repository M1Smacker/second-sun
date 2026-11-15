# Brief 022: fact-check Twinlight lessons 2.3, 2.4 and 2.5 (Claude, 15 Nov 2026, 3 pm; launch after 021 ends)

You run headless; nobody can answer questions. Choose the safest reading, say so in the report, go on. AGENTS.md wins over this brief.

## Why
Ahmed asked for the learning to be "the heart" of Second Sun; RS-036 planned 47 lessons (`research/stage3/rs036/COURSE-PLAN-2026-11-15.md`). Claude wrote three new lessons today. Your fact-checks of lessons 1.1 to 2.2 (017, 018) found real errors each time, so every lesson gets one before Claude calls it done.

## Mission: find errors, fix nothing
Do not edit source files and do not commit (the runner commits your report). Never push, never publish, never open the live Eyes page, never print key values.

## What to check
Files: `book/docs/learn/u2/l3-why-stars-differ.md`, `l4-light-from-two-stars.md`, `l5-gravity-from-scratch.md`. Also the nine one-line unit-number changes in `book/docs/learn/u1/*.md` and `u2/l1`, `u2/l2` (old "Unit 3" or "Unit 5" now point to the new numbering in `book/data/learn-units.yml`; check each points to the right unit or lesson).

1. **Every number.** Recompute each worked example, half-done example and problem answer with a fresh script (do not import ours). Check each `data-answer`, `data-tol` and every hint key against the arithmetic, including that a wrong hint value is not within tolerance of the right answer.
2. **Every fact against a primary source.** Kostov et al. 2021 (arXiv 2105.08614: radii, temperatures 6050 and 5983 K, contamination 0.000453, age 3.1 Gyr, crossing order primary then secondary); IAU 2015 B3 nominal values (Sun 5772 K, GM of Sun and Earth); TESS pixel 21 arcseconds (Ricker et al. 2015); Proxima Centauri visual magnitude about 11; Neptune 3.9 and Saturn 9.4 Earth radii; Jupiter about 13 km/s; ISS about 92 minutes; Kepler 1619, Principia 1687. Open the source; quote the sentence or table row.
3. **Physics claims.** Especially: (a) lesson 2.3's claim that most of the 45% versus 36% eclipse depth difference comes from the oval orbit (different overlap at the two eclipses), not temperature; check it against the paper's orbit (e = 0.45, its argument of periastron and inclination if given) or say how far you could get; (b) lesson 2.4's 2,860 ppm prediction against the measured 2,655 and the reasons given for the gap; (c) lesson 2.5's derivation and its statement that 4 pi squared over G equals 1 in years, AU and Suns.
4. **Teaching.** Anything a beginner would misread; any sentence stronger than its evidence; any jargon not explained on first use.
5. **Licence.** No sentence copied from OpenStax Astronomy 2e (CC BY-NC-SA): spot-check chapters 3 and 5 wording against the lessons.

## Report
`research/astra/reports/022-report.md`: verdict line first; a table (id LX-01 on, lesson, line, claim, what is wrong, evidence with link or script output, severity P1 to P4, CONFIRMED or HYPOTHESIS); then what you did NOT check. Scripts and outputs under `data/astra/022`.
