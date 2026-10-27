# Compass review: Phase E1 (Stage 3 preparation), 27 October 2026

Review only. Written before any E1 code. Labels: VERIFIED (read the code or ran it), LIKELY, UNCERTAIN, NOT TESTED. Plan reviewed: `research/TODO-after-weekly-reset-2026-10-26.md`, Phase E1 items (a) to (f), plus the Stage 3 definition in `RESUME.md` and `research/stage2-2026-10-23/README.md`.

## Verdict: REVISE (go ahead with the changes below)

## What is correct
- **(a) C5 belongs in the pipeline. VERIFIED.** The rule exists only in `stage2_report.py` (applied after the search, 0.35 d from the catalogue primary or phase 0.5) and as a printout in `stage2_phase.py`. The group files the search writes carry no phase distance, so every Stage 3 event would need the report to recompute it.
- **(b) QLP-only stars need their own label. VERIFIED.** 237 of 549 stars have only QLP files (manifest), 275 have SPOC, 312 have TESS-SPOC. The lenient second-product rule keeps events that have no second product, so on these stars the rule confirms nothing. 12 of the 50 Stage 2 stars were QLP-only.
- **(c) Plan list size from real counts. VERIFIED.** Stage 2 found 0.076 real against 0.178 upside-down events per star-sector. The upside-down count is an upper bound, not the planning number.
- **(d) 136 stars with no measured eclipse shape. VERIFIED.** 136 of 552 target rows (136 stars) have morph = -1. Ahmed's recorded default (decisions.md, 20 Oct) is to keep them and measure the eclipses ourselves; the existing automatic mask (`eclipse_mask_auto`, called inside `prepare()`) already does that, so no new science is needed, only a record of whether it found a run.
- **Time and room. LIKELY.** Stage 2 took about 15 minutes for 474 groups on 8 cores; 5,064 groups scales to about 160 minutes. D: has 491 GB free; all 8,100 light-curve files are on disk (VERIFIED).
- **The search itself must not change. VERIFIED.** `Prod.events()` was checked identical to `detect_v2.find_events` on 33 files. E1 must not edit `detect_v2.py` or `stage2_search.py`.

## What needs changing, and why it matters
1. **Never write Stage 3 into `data/stage2`. VERIFIED risk.** `stage2_search.py` hard-codes the output folder and the star list, and `do_group` skips any group file that already exists. A Stage 3 run pointed at the same folder would silently reuse Stage 2 results for the 50 trial stars (the README says those are searched again), and a resume after a settings change would mix old and new results. Fix: a wrapper that points the output at a folder named by the settings hash. `select()` also rewrites `stage2_stars.csv`; it must not be run again.
2. **Do not edit the Stage 2 files; wrap them.** The module reads its output folder and star list from module-level names, so a wrapper can redirect them without changing a line. The Stage 2 results then stay reproducible, and a regression test can prove the wrapper returns identical events.
3. **Tiers, not a deletion list.** Tier 1A: no flag, second product agrees at SNR 4 or more. 1L: agrees at 3 to 4. 1B: no flag and no second product (QLP-only stars land here, unconfirmable by this check). Tier 2: any flag (gap or dump, burst, matched upside-down, C5), kept, lower priority. Tier 3: a second product exists and disagrees (SNR under 3), kept and labelled. Stage 2's "survivors" are exactly 1A, 1L and 1B, so the numbers can be checked against the published aggregate.
4. **C5 radius: keep 0.35 d, measure its cost. VERIFIED.** The binary periods run from 5.01 d to 1,087 d, so C5 never covers more than 28% of a timeline: at least 5% of the timeline for 353 stars, at least 10% for 217, at least 20% for 70, none at 30% or more. A fixed radius is acceptable. It is a flag, not a deletion, because a real transit can fall on an eclipse phase. UNCERTAIN: whether 0.35 d is right for very wide eclipses; not tested, not changed.
5. **List-size planning must not use hard-coded class sizes.** `stage2_report.py` hard-codes 801, 1067 and 3196 star-sectors. A test should derive them from the data and confirm the numbers (checked in the test).
6. **(e) Freezing is a one-way step; build the tool, do not run it.** The hash should cover the settings, the star list, the data manifest, the code files and the git commit, and the results folder should be named by it. Ahmed says when it is run, before any result is read.
7. **(f) Panel data is under-specified: defer.** Its user is the Eyes pass on real events, which Ahmed has gated behind his own practice and a pass test. Build it when that spec exists. Writing it now would be guessing.
8. **Pair search is missing from the E1 list. UNCERTAIN.** `RESUME.md` defines Stage 3 as "add C5 phase check and pair search"; the Phase E list never mentions pair search. It is NOT TESTED and not built here. It needs an explicit decision before the run: build it, or say plainly that Stage 3 is single-dip only.

## Single best next step
Write a wrapper that redirects Stage 2's output by settings hash and adds the C5 distance, the second-product state, the QLP-only label and the tier to every event. Prove it by (1) rebuilding Stage 2's published waterfall exactly from the old group files and (2) re-running the 5 known hosts through the wrapper and getting identical events.

## Not checked
No Stage 3 search was run. No settings were frozen. Detector science (thresholds, durations) was not reviewed, only what the plan changes.
