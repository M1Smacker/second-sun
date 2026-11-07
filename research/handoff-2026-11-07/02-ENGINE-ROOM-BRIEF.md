# Engine Room: brief for a new book Part (WO-15)

*Purpose: take Ahmed from "can vet a candidate" (Checker, the current learning track L0 to L6) to "can read, explain, change and test any core file" (Engineer). He starts Tier 2 after his HSSC-II boards (about June 2027). Build the map page and ER1 earlier if he wants a taste; the rest can wait. Needs his go.*

## Why a book Part, not files next to the code

A lesson per pipeline file would mean 111 explainers and a cluttered `pipeline/` folder. Most of those files are one-off studies. The core chain every search runs through is about a dozen files and roughly 2,000 lines. So: one map page that classes every file, and ten lessons on the core chain, all inside the book. Nothing is added to `pipeline/`.

Name: **Engine Room** (Chapter 13 is already "Your workshop", so do not call it Workshop). Folder `book/docs/engine-room/`. The learning track gets one level after Level 6: **L7 · Engine Room**, with its own checks, and the Read menu gets the Part.

## The map page

One table, every file in `pipeline/` (and the run scripts that matter), one line each, in four classes:

| Class | Meaning | Ahmed's depth |
|---|---|---|
| Core | every search runs through it | Master |
| Test | proves the core did not break | Confident |
| Study | answered one question once; its result is in a note | Aware |
| Retired | superseded; kept for the record | none |

Generate the table from the code where possible (imports, which files the frozen settings list) and keep it honest with a check that fails when a new file appears in `pipeline/` without a class.

## The ten lessons

| Lesson | Question it answers | Files |
|---|---|---|
| ER1 Getting the light | where does each number come from, and what can silently go missing? | `dataset.py`, the download scripts, quality flags in `detect_v2.load` |
| ER2 Cleaning and safe windows | how do we take out slow trends and the bad stretches without eating dips? | `detect_v2.detrend`, `good_windows`, `stage3_core.py` |
| ER3 The detector | how does a box slide along the light and turn into a signal-to-noise number? | `detect_v2.bin10`, `box_scores`, `find_events` |
| ER4 Flags and tiers | why is a dip kept, flagged or moved down? | `detect_v2.veto`, `vopts.py`, the tier rules |
| ER5 The upside-down control and the scorecard | how do we know how many dips noise alone makes? | `scorecard_plus.py` |
| ER6 Planting fakes | how do we measure what we would have missed? | `chain_recovery.py` |
| ER7 Freezing and fingerprints | how do we stop ourselves tuning on results? | `audit_all.py`, `SETTINGS_FROZEN_*.json`, the sealed wrapper |
| ER8 Horizon | how many planets should we have expected, and how high can the rate be if we found none? | `horizon_reach.py`, `stability.py` (include the WO-1 lesson: evidence already spent is not counted again) |
| ER9 Leads | how does a surviving dip reach the Search window, and what stays private? | `leads_export.py` |
| ER10 Tests | how does the project prove it did not break itself, and how do you catch a test that lies? | the `test_*.py` files (use the skip-prints-pass case from WO-9 as the example) |

## How each lesson works (about 2 to 3 hours each)

1. **Read.** An annotated excerpt of the real code, 20 to 60 lines, with plain-word margin notes. Each excerpt names the frozen version and the file's hash.
2. **Predict.** One or two written questions before running anything, for example: "If the shortest box drops from 3 hours to 2, what happens to false alarms and to recovery of 3-hour dips?" He writes his answer first.
3. **Change.** He makes that change on a sandbox copy (a script makes the copy under `D:\second-sun\sandbox\`, git-ignored; never the real files, never C:).
4. **Check.** Run the matching test and a small measurement; compare with the prediction. Being wrong here is the point of the lesson.
5. **Explain back.** Five plain sentences on what the file does and why it is built that way. Claude marks it against a short rubric (correct, complete, in his own words).

End of each lesson: three checks in the existing quiz style, so progress shows on the track like every other level.

## Keeping lessons true

A guard test (run in the publish gate) checks that every code excerpt quoted in an Engine Room page still matches the named file at the named hash, or matches the current file if the page says "current". When the pipeline changes, the guard fails and names the lesson, so the book never teaches old code.

## Finish test for Tier 2 (put it in the track, align with Keystone T134)

1. **Mutation hunt:** Claude plants three bugs in a sandbox copy of the core chain; Ahmed finds and explains at least two in one sitting.
2. **One real improvement, end to end:** a build-queue item he plans, changes, tests and compares event by event against the frozen run, with a write-up Claude reviews as a stranger would.

## Style

Book rules apply: plain words, no en or em dashes, phone-first, the "In plain words" box at the top, sources at the bottom. Keep maths to what the code uses, written the same way the code writes it.
