# Brief 025 (big run A3): the planets lost at load, root cause and fix (Claude, 15 Nov 2026; launch after 024 ends)

You run headless; nobody can answer questions. Choose the safest reading, say so in the report, go on. AGENTS.md wins over this brief.

## Why
Node 1.2 of the Tree: of 52 planted planets that fall outside the searched windows on T156, your 005 part C found 15 sit in true archive gaps, **21 are lost at load**, and 16 had usable data before the window rule (ceiling 2.6 to 7.0 points of R). A loss at load is the kind of silent loss that is a bug until shown otherwise: light that exists, that a planet sits in, never reaches the search. Fable hunts silent losses on Monday; this job hands her the facts for the biggest known one.

## Before computing (write into the report first)
- The list of the 21 (from your 005 data) and, for each, the hypothesis classes you will test: file not downloaded or not in the manifest; product choice (SPOC, TESS-SPOC, QLP) picks a file without the planet's cadences; quality mask drops the cadences (which bits); time-system or sector mix-up; a try/except or `continue` that skips silently (count every skip path); the 30-min, 10-min or 200-s cadence paths (one test file per path, as the auditor skill demands).
- The pass rule for a fix: recovers at least half of the 21 to the search, frees planets on T156 without adding upside-down tier-1 background, and changes nothing on star-sectors that were loaded correctly (zero-difference identity check on 50 untouched star-sectors).

## Do
1. For each of the 21: trace the exact line where its light is lost (file, function, line, condition), with the evidence (counts, a printed row). Group by cause.
2. Repeat for the 16 "usable data before the window rule": which rule removes them, and is the rule doing what its comment says?
3. For the biggest cause, write a fix on a bench copy, show its test fail before and pass after (a mutation check), and score it: T156 R, planet bench P, untouched-light background both arms, the identity check.
4. Count across ALL of T156 (not just the 21) how many planted planets each cause touches.

## Your method log
`research/astra/reports/025-worklog.md` while you work, same format as 023 and 024.

## Rules and report
Branch `astra/025-load-losses` from the latest main. Cap 50 five-hour points; machine time free; never poll. Data under `data\astra\025\`. Fence A and B never; no G1 or sealed data; frozen files untouched (fixes in your harness copy, proposed as a patch file for Claude); never push. Report `research/astra/reports/025-load-losses.md`: verdict line first; the cause table with counts; the fix and its numbers; what you did NOT check; usage.
