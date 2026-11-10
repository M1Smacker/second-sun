# Book coverage audit: is the filter, the mask and the science behind the project taught in the book? (10 Nov 2026, Sonnet 5.5 Extra, PLAN ONLY)

**Plain verdict: the book teaches the BREADTH well and the filter's recent DEPTH badly. 28 of 41 concepts are taught (chapters plus quiz or glossary), 7 are only mentioned, 3 live only in field notes, 3 are missing. The gaps cluster exactly where the last week's work happened: how the mask really works and fails, why injection order matters, how a hunt is judged (pass marks, preregistration), what a "no planet" result can and cannot exclude, and Census. Nothing was edited. Teaching waits for Petrova 1.0 and the re-search, as Ahmed said; Lesson 5 (plain words) already captures today's lesson.**

Method (CONFIRMED, a script that could contradict it): `scripts/book_coverage.py` counts keyword hits per concept in the TEACHING pages (chapters 1 to 15, labs, parts, start, learn quiz, glossary) and in the DIARY pages (field notes, versions, claims, other pages), then I read the passages for the weak ones. Full table: `evidence/book_coverage_matrix.txt`. A keyword count shows presence, not quality; quality was checked by reading the passages named below. Size of the teaching text: chapters 113 KB, labs 40, parts 20, start 24, learn 20, glossary 12; the diary (field notes) is 162 KB, i.e. a lot of the newest science sits where a learner does not read it.

## What is taught well (TAUGHT, depth checked or obvious)
Light curves and names (Ch 1 to 3), binaries and the planets around them (Ch 4), why two-sun transits wander in timing and duration (Ch 5, the words TTV and TDV are not used, the idea is taught), three-body orbits and the stability limit (Ch 6), noise and statistics (Ch 7), the detector steps, the upside-down control, tiers and flags (Ch 8, 10), pixel-level vetting (Ch 11), STANLEY and the professionals (Ch 12), the known planets, time systems, products (SPOC, TESS-SPOC, QLP), the hunts G1 to G3, the two-key rule and credit (CTOI, ExoFOP).

## The gaps (what the learner cannot find in a teaching page today)
| # | Gap | Evidence | Why it matters now |
|---|---|---|---|
| 1 | **Slow versus fast binaries and the timetable (period, epoch/ephemeris, drift)** | "ephemeris" 0 matches in teaching pages; "slow binary / one visit per phase" 1 line (Ch 2) | The whole mask story rests on it; catalogue masks (Prsa, TTC) need the timetable idea |
| 2 | **The mask's mechanism and its weakness** | Ch 8 step 1 says the mask folds at the binary period and finds the deep part; nothing on one visit per phase bin, 4 sigma, padding, or what it does to a planet; Ch 9 row says masked planets "now counted separately" | Now known wrong in effect; must be rewritten after the freeze |
| 3 | **Injection order (before or after the mask)** | 0 matches anywhere | The flaw that hid F-01; the single most transferable lesson |
| 4 | **How a hunt is judged: S1, S2, S3, the false-alarm mark of 8, sealed and one-shot runs** | S1/S2/S3 only in a field note; "preregistration" 1 chapter line plus quiz | A reader cannot tell why G1 to G3 "passed" or "failed" |
| 5 | **What a null can exclude: transit probability (coplanar, tilt), reach map (Horizon), occurrence (Armstrong's 10%)** | no chapter; only quiz check 10 and a field note | The honest meaning of "we found nothing" |
| 6 | **Real versus upside-down excess (the asymmetry check) as a fairness test** | 1 chapter line, quiz 1 line | Explains why a loose mask breaks the control |
| 7 | **Census** | field notes only | Next big step; learner never meets it |
| 8 | **Box search mechanics** (durations 3 to 20 h, score, why SNR 7) | thin: one figure caption and a lab line | Core of the detector |
| 9 | Version ladder and what a freeze guards (0.8.1, Petrova 1.0, zero-difference proof) | Ch 8 has the idea; versions.md is a diary page | Explains why 0.8.1 stays untouched and why 1.0 is a new number |
| 10 | Newest results (arm check m, K, the catalogue mask, repeat rule) | none; Lesson 5 is private | Teach after the freeze |

## Pages that are now factually stale (cross-reference the 16 places in `BOOK-SENTENCES-AFFECTED-2026-11-10.md`)
Ch 8 (floor 6 Earth radii), Ch 9 (tables 9.5, 9.6, "1 crossing in 11"), Lab 6, Lab 9 line 48, field notes 2026-10-20, 10-29, 11-04, learn quiz 5 (60 percent, 6 percent), claims F-015, F-029, F-048, F-088, F-089.

## How I would tackle it (plan only; nothing starts without Ahmed's go)
1. **Now (inside this cap):** the ONE book correction (0.6): mark the 16 places, add a short banner and a field note; no new chapter.
2. **After Petrova 1.0 is frozen and the old stars are re-searched** (his order), in the learning redesign: ONE new chapter "How the filter really works, step by step", ordered as the pipeline runs, 8 short pages, each = one picture, one worked example from our own data, three quiz checks and glossary terms:
   - P1 Slow and fast binaries: the timetable (period, epoch, widths, drift) and where it comes from (catalogues, Census list)
   - P2 The blindfold (mask): old one, why it fails for slow binaries, catalogue mask, repeat rule, single-visit lane
   - P3 Planting fake planets: before or after, the K scale, m, bumps; why a test can be fooled
   - P4 The fairness check: real against upside-down; what a broken control looks like
   - P5 Judging a hunt: pass marks S1 to S3, the mark of 8, preregistration, sealed runs, one-shot
   - P6 What "nothing found" can exclude: transit chance, reach, Kepler's rate; why our nulls are weak for slow binaries
   - P7 Versions and freezes: 0.8.1, Petrova 1.0, zero-difference proof
   - P8 Census: the list, the timetable columns, the plan
   Rewrite Ch 8 step 1 and Ch 9 sections 9.5 to 9.6 to point at P1 to P4. Sources already exist: `versions.md` ("How Vesper works"), `LESSON-5-...` (P1 to P4), `LESSON-2-WHAT-OUR-NULLS-MEAN-...` (P6), `WO-F01-PART-A-RESULT-2026-11-10.md`, Census plan notes.
3. **Rule so the gap does not reopen:** every new filter change ships with its teaching page the same day (the existing same-day lessons rule), and `scripts/book_coverage.py` is re-run after each book publish; a concept that moves from TAUGHT to DIARY ONLY is a defect.
4. **Cost (UNCERTAIN, from the ledger's ratios):** about 0.2 weekly points per page including quiz and glossary, so 8 pages 1.6 to 2.0, the chapter rewrites 0.5, one publish gate 0.15, total about 2.5. Part of the learning redesign (T133), not in this week's 30%.
5. **Open question for the redesign:** quizzes and the Learn dashboard (his top pain) should list P1 to P8 as one level, "L7 How the filter works", so the path stays linear.
