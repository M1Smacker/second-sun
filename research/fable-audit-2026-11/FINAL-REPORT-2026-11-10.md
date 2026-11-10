# Final report for Ahmed, 10 Nov 2026 (written while you were away; Sonnet 5.5 Extra, with Opus 5.5 medium in a nested session)

## The bottom line (read this if nothing else)
1. **The flaw is real and now measured.** Our old eclipse "blindfold" deleted 4 to 6 of every 10 strong planet dips, almost all of them in slow binaries. Our old tests hid the fake planets after the blindfold, so they could not see it.
2. **We have a repaired blindfold that works.** The best version (C2) keeps 99 of every 100 planted dips and planted bumps are untouched. It is not perfect: the slowest faint binaries (G3, over 27 days) keep an imbalance.
3. **The book is corrected and live** (version 2.10.0): one new field note and a "Correction" box on every page that quoted the old numbers. "We found no excess of real dips over noise" still stands. What it rules out is much less than we wrote.
4. **Nothing is frozen and nothing is re-searched yet.** Both need your yes (below).
5. **Usage:** about 3 weekly points for the whole job (predicted about 6). The meter reads 22% against your 30% cap.

## What was done, step by step
| Step | Result |
|---|---|
| Cheap checks | 16 places in the book rest on mask-blind tests (list in `BOOK-SENTENCES-AFFECTED-2026-11-10.md`); Lab 6, the STANLEY-timed test and the whole-chain test all injected after the mask or built it from clean light (confirmed in the code). Our test harness passed a deliberate-break test. |
| Literature (RS-016) | The two closest published searches (STANLEY and a 2026 TESS single-transit search) mask eclipses from the **catalogue timetable**, not from the flux. |
| Opus job 1, C1 | Failed its first test: the cross-sector part deleted planet dips. Useful: showed the within-sector part is good. |
| Me: C1f full test | Planted dips 99% kept, bumps 100%, control fair for binaries under 13 days. Slow binaries still unbalanced. |
| Opus job 2, C2 | Adds a step that drops EVENTS (not light) that come back at the same binary phase in another sector. Small test: partly passes. |
| Me: C2 full test | See the table below. |
| Book audit (plan only, as you asked) | 28 of 41 concepts are taught; the gaps are exactly the recent work. Plan below. |
| Book correction | New field note 10 Nov; Correction boxes on Chapters 8 and 9, Labs 6 and 9, three field notes and the Learn page; five claims moved to LIKELY (upper limit); two Chapter 9 sentences rewritten; home recap; version 2.10.0. Live. |
| Housekeeping | RESUME cut from 23,700 to 8,300 words (the rest is in `RESUME-ARCHIVE.md`, nothing deleted); star-name check written and run (clean); 40 commits pushed. |

## The mask candidates, side by side (counts only; real stars are not listed anywhere)
| Candidate | Planted strong dips kept (m) | Bumps kept | Real over upside-down events (balanced = about 1) |
|---|---|---|---|
| Old mask (0.8.1) | 0.40 to 0.60 | 1.00 | G2 62 / 110, G3 65 / 93 (slow bins starved) |
| C0 timetable only | 0.98 to 1.00 | 1.00 | G2 215 / 115, G3 328 / 134 (eclipses leak) |
| C1f timetable + repeat inside a sector | 0.99 | 1.00 | G2 169 / 112, G3 217 / 133 |
| **C2 = C1f + event veto (best)** | **0.99** (chance cost of the veto up to 3%) | 0.98 to 1.00 | **G2 110 / 109, G3 174 / 131** |
Where C2 is still off: G3 over 27 days (41 / 16), G3 5 to 10 days and 20 to 27 days (1.4, 1.3), G2 20 to 27 days (10 / 26: the real side is now smaller, the old excess of upside-down events we already knew about). Honest wording for the book later: "a null in the slowest faint binaries excludes less".

## Your question: should Petrova go up a number, like 1.1?
- Today "Petrova" is your name for the filter that is officially still **Vesper 0.8.1** (the rename waits for your go). 
- Our rule (`versions.md`): any change to the rules is a **new frozen version**, never an edit of the old one. The mask is a rule change, so yes, a new number is required.
- My answer: call the new filter **Petrova 1.0.0**, not 1.1. Reason: 0.8.1 stays untouched as the old reference, and 1.0.0 marks the first version whose tests are honest (the planted fakes go in before the mask). The next rule change after that would be **1.1.0**. If you prefer 1.1, say so; it only changes a label.
- The "same results as before" proof will deliberately fail for slow binaries, because the new mask keeps light the old one deleted. That is the point, not a bug.

## The book audit and how I would tackle it (plan only)
Full file: `BOOK-COVERAGE-AUDIT-2026-11-10.md`. 28 of 41 concepts are taught, 7 only mentioned, 3 live only in field notes, 3 are missing. Missing or thin: slow versus fast binaries and the timetable idea; how the mask works and fails; planting fakes before or after; how a hunt is judged (pass marks, preregistration); what a null can exclude; the upside-down fairness check; Census. Plan, after Petrova 1.0 is frozen and the old stars are re-searched (as you said): one new chapter of 8 short pages in pipeline order, each with a picture, a real example and quiz checks, about 2.5 points, part of the learning redesign. Rule going forward: no filter change without its teaching page the same day, and the coverage script is re-run after every publish.

## How the old stars will be searched again, in plain words
1. **What we have:** the light of all 2,056 stars from our three searches is already on your D: drive. **Nothing needs downloading.**
2. **Why again:** our old searches covered slow binaries badly, because the blindfold ate planet dips. The old results stay exactly as filed. This is a new, separate pass with a new version name.
3. **Before we run anything:** we write down the rules and the pass marks and save them with a timestamp (a "preregistration"). Then we freeze Petrova 1.0.0 so nobody, including me, can tune it after seeing results. (You said yes to this idea long ago; each freeze still needs your go.)
4. **The new filter, in one breath:** cover each binary's eclipses using its timetable; also cover little dips that come back on the binary's own beat; search the light; then throw away events that repeat at the same point of the binary's orbit in another month, because planets do not.
5. **The honesty check:** every star is searched twice, normal and upside down. The upside-down copy shows how many fake dips noise alone makes. If normal gets clearly more than upside-down, something real may be there. If not, it is a clean "nothing", now covering the slow binaries.
6. **Looking at results:** first only the totals. No star is named. If there is an excess, I look at which stars privately, two independent checks, and only then do I tell you. Nothing leaves the PC without your yes.
7. **Cost and time:** freeze and preregistration about 2 points, the search itself about 2 points. The machine part takes minutes (the old hunts took 8 minutes). Needs your yes for the freeze.
8. **After that:** the learning redesign (book chapter of 8 pages), and Census, which will also write down each new binary's timetable so the new filter works from day one.

## Usage (predicted, actual, lessons)
- Predicted about 6 weekly points for this job; actual about 3 (19% to 22%; the 5-hour meter 29% to 45%).
- Opus job 1: predicted 1.0, actual about 1.0 (26 calls). Opus job 2: predicted 0.9, actual about 0.6 (16 calls). Main session about 1.5.
- Lessons: a call-count stop line works, a whole-point meter line stopped Opus too early on the first job; machine runs while Opus designs are almost free; one script that prints a compact table per run keeps each iteration to 2 or 3 calls; at 70 to 80% of context every call costs more.
- One thing to know: Opus ran an extra counts-only diagnosis on real light after its first report (written up in the C0 addendum, not used to tune anything). It never listed stars or events.

## Decisions I need from you (when you are back)
1. Name: **Petrova 1.0.0**, or 1.1? And your go for the rename Vesper to Petrova at the freeze.
2. Go to write the preregistration and freeze Petrova 1.0.0 (about 2 points).
3. Go for the re-search of the old stars (about 2 points).
4. Context is at about 80%: please compact before the next big job (RESUME is current).

Next: your word on 1 to 3. Then I write the preregistration first (cheapest, and it fixes the pass marks before any run), and the learning redesign starts after the re-search.
