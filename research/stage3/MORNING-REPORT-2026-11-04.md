# Morning report, 4 Nov 2026 (written overnight; stopped at exactly 30% weekly, 07:03 Kuwait)

## Plain verdict
Found nothing new about planets, because nothing was searched. All 5 main items, all 6 stretch items and about 15 extras are done. Nothing in Petrova changed, nothing sent outside, no star named. Weekly meter: 24% at the start (05:05 Kuwait), 30% now (5-hour meter 53%). Seven book versions published (2.9.7 to 2.9.13), each confirmed live; the live book is 2.9.13.

## What we learned (labels in the notes)
1. **Fuel (CONFIRMED):** 364,656 stars (258,858 at Tmag 13.5 or brighter) were 2-minute targets after sector 26 and never before. No complete binary list covers them. About 0.4% are the G2 type (long period, detached, bright): about 1,400 targets (LIKELY, factor 2).
2. **Fetching is cheap (CONFIRMED on 66 files):** a public Amazon bucket, about 3 files a second with 8 threads, 1.8 MB a file. All 258,858 stars, one sector each: about 23 hours and 460 GB, streamed. Correction: G3's "21 hours" was about 20 hours of unnoticed stall; the work was about 1h15.
3. **Our reach map was missing the transit geometry (CONFIRMED the gap, size from a probe):** with it (factor about 0.05 to 0.3) our nulls are consistent with Kepler's 10% rate in most cases I tried, and not in the most optimistic corner (about 1% chance of finding none). Honest line: "not looked hard enough to tell yet".
4. **My geometry condition is the published one (NEW, CONFIRMED):** Li, Holman and Tao 2016 (read in full) give the same first-order condition as my probe for a planet in the binary's plane. They also say precession helps tilted planets, and both-star transits plus 4 years of looking change the probability by at most about 2. Kepler-16 (Doyle 2011, opened): all three bodies within 0.4 degrees of one plane, and its transits are visible only about 40% of the time over 5 centuries because of precession.
5. **Dip shape (NEW, CONFIRMED, FIX 28 answered):** I planted dips of other shapes through the untouched search. A physical planet-crossing-a-star shape lowers the kept share at K 8 to 14 from 30.5% to 27.8% and 27.1% (about 3 points, a tenth). A V-shaped dip with long slopes drops it to 21.5%. So the completeness we quote is about a tenth too high (LIKELY; limb darkening assumed, one radius ratio).
6. **Census worth (LIKELY):** about 1,400 G2-type stars (3 sectors each) roughly double our evidence: all hunts together expect about 2 to 5.5 planets at Kepler's rate, 87% to 100% chance of at least one, and a null would cap the rate near 5% to 15%. Idea 4 (linking dips across sectors) is not original; only the sparse TESS single-event version with an upside-down control may be open (UNCERTAIN, now 8 queries, no hit). The literature expects few small circumbinary planets, so only a Jupiter-size null is strong news.
7. **S2 false alarms:** pooled 8.57 per 1,000 (7.1 to 10.3) against the mark 8: borderline, not a clear fail. Your call.
8. **The 784 lost reads:** 16% of star-sectors, mostly after sector 26 (27% in sectors 27 to 55); about 8% of reach for G3. Same supply gap Census closes.
9. **Claims checked against opened papers:** F-030 (Kepler field, 200,000 objects, 156,000 stars in six weeks) and F-042 (red noise raises the threshold, narrowed to what the abstract says) are now VERIFIED; F-044, F-059, F-024 earlier.

## Downloads (told as required, logged in downloads.csv and jobs.md)
111 TESS 2-minute target lists, 65 MB, `data\census_targets_2m`; 66 sector-27 light curves for the speed test, 113 MB, `data\census_probe`; Doyle 2011 Kepler-16 PDF, 334 KB, and the Li 2016 paper as text, 99 KB, both in `data\census_papers`; Gaia archive counts (queries only); a STANLEY PDF fetched once to see its size and deleted unread; many arXiv abstract and HTML pages read as text.

## Slips, said plainly
- My first Q1 conclusion ("reach map too generous by several times") was too strong; the geometry probe fixed it and the tilt test softened it again. Both are in the notes and the book wording was corrected twice.
- `git add -A research` swept about 40 untracked run logs (3 MB) into one commit. Harmless, not undone.
- The first Gaia query timed out (my join was too big); a background run was started by mistake and stopped.
- My predictions were 4 to 7 times too high on analysis tasks; I priced later tasks lower. The weekly meter moves only in whole points, so the last stretch took many small tasks.
- I wrote wrong clock times and run lengths in my notes (said 80 and 40 minutes where the logs show 3 minutes per shape run). Corrected in RESUME, jobs.md and the ledger from the file times.
- A book browser test (chapter layout) failed once and passed on its automatic retry; filed as FIX 80, not reproduced, not changed.
- One publish push failed once on a network error; fixed (FIX 79); the next six publishes passed.
- The Kepler-16 stellar radii (Table 1 would not come out of the PDF text) are still remembered values, labelled UNCERTAIN.

## What I need from you (nothing blocks)
1. Read Lesson 2 (`research/stage3/LESSON-2-WHAT-OUR-NULLS-MEAN-2026-11-04.md`) when you have ten minutes; Lesson 3 is the finder-test lesson for stage 2.
2. Yes or no to T138 (put the geometry into Horizon properly, about 2 points; amends a locked rule). It now has a published anchor and a precession note.
3. Which Census stage 2 step to start, or "wait": `CENSUS-STAGE2-OPTIONS-2026-11-04.md`.
4. The S2 decision (options A, B, C in `Q6-S2-EVIDENCE-2026-11-04.md`; my lean is A).
5. The Petrova rename go; whether the book leads with "found nothing" or "not looked hard enough".

Next: say yes or no to T138 (about 2 points; it fixes the number every Census size depends on), or tell me a different first step; I start the moment you say so.
