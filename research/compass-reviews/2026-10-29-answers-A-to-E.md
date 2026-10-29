# Answers to the outside AI's A to E prompt (29 Oct 2026)

Ahmed allowed this on 29 Oct ("i also allow to run the embedded A to E prompts since they benifit Project second sun"). It is a review of the outside AI's seven priorities against the repository, written AFTER step 0 and step 1 were done, so it uses measured numbers. Review mode for the plan itself: nothing here changes a frozen result, no real event was inspected, `pipeline/eyes_rules_test.py` was not run. Labels: VERIFIED, LIKELY, UNCERTAIN, NOT TESTED. Evidence files: `research/stage3/learnings-2026-10-29.md`, `chain_recovery_v7.txt`, `fill_audit_v7.txt`, `g2-counts-2026-10-29.md`, `G2-PREREGISTRATION.md`, and the earlier `compass-reviews/2026-10-28-outside-ai-vesper-review.md`.

## A. Strongest recommended next action
**Build the per-flag ledger: for each flag, what it costs real planet-like dips and what it buys against false alarms.** Why: step 1 showed the whole chain keeps only 44% to 64% of even very deep dips (VERIFIED, `chain_recovery_v7.txt`), and the data-edge flags (gap and dump, ramp, flat baseline) alone remove 32% of them. The same flags are what cut the upside-down tier 1 from 234 to 32. Whether each flag is worth its price is the question that decides v8, and both halves of the ledger are cheap now: the cost half exists (the rows in `data/chain_recovery/rows_v7.pkl`), the benefit half comes from the ladder in the aggregates and the upside-down copy. Run it while the G2 development slice downloads.

## B. Ordered work plan (usage points are my guesses from today's ledger rows, UNCERTAIN)
| # | Task | Depends on | Acceptance | Points | Machine |
|---|---|---|---|---|---|
| 0 | Steps 0 and 1 (done 29 Oct) | | harness identical to the real run in 299 of 299; ceiling and 50% depth measured | 4 (spent) | 20 min |
| 1 | G2 development slice download (301 stars, about 9 to 10 GB) | Ahmed's A (given) | every file recorded in the manifest; byte counts match | 0.2 | 15 to 60 min network |
| 2 | Per-flag ledger (cost per flag from the rows; benefit per flag from the upside-down ladder), by box length | none | one table, labels, no setting changed | 0.5 to 1 | none |
| 3 | Switch the data paths to G2 without changing a rule; zero-difference test on G1 | 1 | same events, tiers and hash behaviour on G1 as now | 0.5 to 1 | 20 min |
| 4 | Run the frozen chain on the development slice (development use) and `chain_recovery.py` on it | 3 | 0 errors; completeness table for dev | 0.5 | about 1 h plus 30 min |
| 5 | v8 candidates, each measured on G1 and dev: longer smoothing window for long boxes (FIX-QUEUE 11), a flat-baseline test that allows for the smoothing, a gap rule that scales with box length | 2, 4 | v8 beats v7 in tier 1 recovery at a given depth by a set margin (propose: 10 points at 12 times the noise for 14 h and 20 h boxes) with the upside-down tier 1 count not rising faster than the real recovery | 2 to 4 | 3 to 5 h |
| 6 | Optional: block bootstrap for the SNR bar only (not the flags) | 4 | agrees with the measured asymmetry within a stated margin | 0.5 to 1 | 1 h |
| 7 | Freeze v8, lock the preregistration, search the sealed slice once, then completeness on 300 sealed star-sectors | 5, Ahmed's go | sealed rules followed to the letter | 1 to 2 | 3 to 4 h plus 40 min; download about 19 GB |
| 8 | Blind look at events (the 7 raw-light dips plus matched controls from earlier ladder rungs) | Eyes ladder rungs 1 and 3, Ahmed's yes | fair control built, same renderer, no labels | 1 to 2 | none |

## C. Biggest risks that could invalidate the science if left alone
1. **A weak null presented as a strong one.** At 50% recovery the chain needs about 8,000 ppm for the middle star; most known transiting circumbinary planets make shallower dips (VERIFIED arithmetic on NASA archive values, upper bounds). Every null must carry the completeness table.
2. **Labels that hide what is inside.** "Cleaned light" was 10 of 14 raw QLP flux (VERIFIED). Fixed in the briefing; the code and report still carry the word until the next freeze.
3. **Tuning on the test set.** v1 to v7 were chosen after seeing G1. Mitigation: the G2 split and preregistration, binding only once locked.
4. **An unfair control.** The upside-down copy overstates false alarms 1.25 to 2.5 times (measured) and the checks treat dips and mirror bumps about equally (32% against 34%, p = 0.06); the cause of the small edge is UNCERTAIN. The raw-light half has no fair control at all.
5. **Planet radius from a wrong star.** G1 and G2 have no light ratio or radius ratio; a TIC radius describes the blend. Depth first, radius only as a range.
6. **Data versions.** QLP sectors 74 to 79 had a timestamp bug of up to about 3 minutes in version 1; MAST re-delivered version 2. VERIFIED: all 1,021 QLP files we hold for those sectors are v02. Irrelevant for hours-long dips but it matters for any period work. The saved TESS binary catalogue lists sectors up to 39 (not the paper's 1 to 26); whether periods were redone is UNCERTAIN.
7. **Overlap with the professionals' search.** Some of the 895 G2 stars were searched by Davies and colleagues; we do not hold their list (NOT TESTED).

## D. Disagreements with the outside plan, with evidence
1. It put the fill and error audit first as its own phase. Measured: the fill is 0.67% of cadences and acts on both sides alike; no swallowed failure matters (`fill_audit_v7.txt`). It was a quick check, not a phase.
2. Its block bootstrap tests only the SNR bar; gaps, orbit starts, common moments and eclipse phase are timeline effects it cannot reproduce.
3. Its matched comparison stars need a new download (at least 5 to 6 GB) and have no eclipses, so the eclipse flags cannot be tested on them.
4. It treated recovery as limited by SNR. Measured: at 18 times the noise a dip is seen 99% of the time and kept 44% to 64%; the flags, not the search, set the ceiling.
5. Its "specific flaw" in the blind review was a misreading of our plan (see the 28 Oct review). Its real point (no control exists for the 7 raw-light dips) stands.
6. Its G2 idea of "Kepler leftovers in a separate pool" does not fit the catalogue: only 53 of our 549 G1 stars are in it, so G2 is mostly new sky, and its size is 28 GB for all 895, not small.

## E. Files and read-only checks for the next approved task (the per-flag ledger)
- Cost half: `data/chain_recovery/rows_v7.pkl` (private, injections only, not real events), `pipeline/chain_recovery.py` (`summarize`, `FLAGS`).
- Benefit half: `research/stage3/aggregate_v7.txt` (ladder, sections 4 and 5), `research/stage3/asymmetry_v6sap.txt`, `asymmetry_v5.txt`, `pipeline/stage3_core.py` (`tier_of`, `enrich_event`), `pipeline/stage3_report.py`.
- Read-only checks: (a) for each flag, the share of injected primary dips it removes by box length (already printed in part); (b) for each flag, the real and upside-down tier 1 counts with and without it, rebuilt by switching the flag off in a copy of the tiering function (no search); (c) the ratio of the two per box length.
- Do not edit: any file named in `stage3.current_settings` code list (frozen hash fd788be04650).
