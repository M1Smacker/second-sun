# Census stage 2: the options in front of Ahmed (written overnight, 4 Nov 2026; a proposal only, nothing started)

You asked to decide "today or someday" whether we build the list. Tonight's groundwork (counts, fetch speed, yields, geometry, what Census is worth) is in `CENSUS-STEP1-COUNTS`, `CENSUS-STEP2-RESEARCH`, `CENSUS-WORTH`, `Q1`, `Q2`, `Q3-Q7`, `Q5` and `Q6` in this folder; Lesson 2 explains it in plain words. This page turns it into choices. Costs are my estimates from tonight's ledger (about 1 weekly point per 8 to 10 five-hour points) and are UNCERTAIN; the first column of each option is what you would be deciding.

## The choices, in the order I would take them
| # | Step | What it is | Cost (weekly points) | Time on the machine | Why it comes here |
|---|---|---|---|---|---|
| 1 | **T138: put the transit geometry into Horizon** | Open Li, Holman and Tao 2016 in full and finish the probe: companion sizes, check on the known Kepler planets, a locked amendment R0-2, re-run the three maps | about 2 | minutes | It decides how big Census must be. Without it every "worth" number is a range from 1 to 5. Needs your OK because it amends a locked rule. |
| 2 | **Finder test set** | Fetch 400 known eclipsing binaries and 400 non-binary controls (3 sectors each, 2,400 files, 4.3 GB, about 13 minutes), build a plain eclipse finder and score its recall by period and its false alarms on the controls. The ground truth is free: 4,161 binaries from the published list were 2-minute targets again after sector 26 (1,036 of the G2 type; 563 with 4 or more sectors). | about 2 to 3 (most of it thinking and teaching) | under 1 hour | A finder that cannot recover known binaries must not be turned loose on 259,000 unknown stars. |
| 3 | **Pilot on the long-coverage stars** | The 5,193 new stars with Tmag up to 13.5 and 8 or more sectors, all their sectors: 75,151 files, 135 GB, about 6.7 hours; about 85 binaries expected, about 27 of the G2 type | about 1.5 | 7 hours | Tests the finder, the fetch, and the linking of dips (idea 4) where it matters most, at a cost we can take in one night. |
| 4 | **The scan** | Every new bright star, one sector each (258,858 files, 463 GB, about 23 hours), then all sectors of the candidates; streamed, so nothing piles up on disk; about 1,400 G2-type targets expected | about 3 to 4 plus the vetting | 1 to 2 days | This is the Census list. |
| 5 | **Gaia queue (optional)** | The 5,503 Gaia candidates with P over 7 d and G under 14 as a priority list for the scan | about 1 | minutes | Gaia periods for long binaries are weak; use as a hint, not as truth. |
After step 4: audit and freeze a new Petrova, preregister, prepare the Search window, and your explicit go (stages 6 and 7 of the Census plan). The rename, T137 (window table), and the S2 decision all land before the freeze.

## My lean
Do step 1 first, then step 2, then step 3, with a short lesson before each so you stay in the loop. Step 4 only after step 2 has shown the finder works and after you have read the pilot's result. Total to a frozen list: about 8 to 10 points of my usage over several days, not months, if nothing surprises us.

## What you decide, and what I need from you
1. Yes or no to step 1 (T138), because it amends a locked rule.
2. Which step to start when you wake up, or say "wait".
3. Whether the book should keep "found nothing" first, or lead with "not looked hard enough to tell" (Lesson 2, question 1).

## Labels
LIKELY: costs and times (ledger-based), file counts and sizes (CONFIRMED arithmetic on the target lists and one probe). UNCERTAIN: sustained fetch speed over hours, the number of G2-type stars (factor 2), the finder's recall and false-alarm rate (not built). NOT TESTED: everything in steps 2 to 5.
