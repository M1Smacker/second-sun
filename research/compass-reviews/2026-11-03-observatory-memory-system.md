# Compass review: Observatory Memory System (OMS), 3 Nov 2026

Proposal written by ChatGPT for Ahmed, reviewed by Claude (Sonnet 5.5) on 3 Nov 2026 from 01:39 Kuwait. Review only. Concept saved in full in `research/stage3/OMS-DESIGN.md`.

**Verdict: REVISE.** On the proposal's own scale: DEFER, with one small piece kept (evidence index, T124). Ahmed agreed to the reduced scope and the reopen rule on 3 Nov, and decided that the next three weeks go to finishing and measuring the systems we have.

## What is correct in the proposal
- The wish for traceable, versioned, correctable knowledge is right, and its eight rules are sound (evidence before classification, similarity is not proof, no autonomous decisions, two-key kept, immutable history, provenance, visible uncertainty, reproducibility).
- The validation idea (hide outcomes in a frozen set, measure usefulness and false associations) is the right shape.
- Asking Claude to challenge it and to prefer a small reliable system over an impressive one is the right posture.

## Checks made (our files read; label CONFIRMED unless stated)
- Build queue: 52 open boxes, 12 done (grep of `- [ ]` and `- [x]` in BUILD-QUEUE.md).
- G3 download stalled at 410 of 612 since 2 Nov 06:13 (fix item 72 open). Vesper 0.9 not frozen. Loom is at research stage. Downloads page and F4 redesign not built.
- `book/docs/candidates.md` holds only a marker: no candidate has ever gone through the two-key process.
- Sealed G2 scorecard (scorecard-plus-sealed.txt): at bar 7, tier-1 real 26 against upside-down 59 (ratio 1.18); real events did not outnumber the control.
- Git tracks 746 files; `.git` is 12 MB. Repo is public; `data\` is git-ignored; real events stay in `data\` by rule.
- TESS publishes per-sector Data Release Notes with known issues such as scattered light and momentum dumps ([HEASARC condensed notes](https://heasarc.gsfc.nasa.gov/docs/tess/data_release_notes.html)). LIKELY: seen in a search summary, page not opened, early sectors only.
- Uniform external vetting dispositions exist for TOIs ([TESS Triple-9 catalog, arXiv:2203.15826](https://arxiv.org/abs/2203.15826)). LIKELY: search summary only.

## Existing equivalents (so OMS would duplicate)
| OMS part | Already in the repo |
|---|---|
| Detector Memory | VESPER-VERSIONS.md, SETTINGS_FROZEN_*.json hashes, versions.md, loss-ledger, flag-patterns, chain_recovery results, benchmark and scorecard files |
| Artifact Library | the 9 Vesper flags and the 6 Eyes classes, assigned to every event automatically |
| Target and Sector Memory | Loom phase 0 windows table and phase 4 run status record (queued); Vigil ledger (queued); sector flags inside every data file |
| Decisions, lessons, forecasts | decisions.md (126 lines), mistakes.md, predictions.md, 15 Compass reviews |
| Leads and two-key | LEADS-RULES.md, leads_export.py, two-key-method-2026-10-24.md |

## Wrong or out of date in the proposal
1. 549 targets was G1; the lists are now 549, 895 and 612 stars.
2. Stage 1 recorded no events; Stage 2 was the 50-star trial; the working pipeline is Vesper 0.8.0 on the G lists.
3. "Claims Register": `research/claims.md` is an empty table; the real register is `book/data/claims.csv` (99 rows) and holds book facts, not investigation outcomes.
4. Vocabulary: since 28 Oct our word is CONFIRMED, not VERIFIED.
5. Core problem: almost no labelled real artifacts exist. The known-truth examples are planted dips and the upside-down control. There is little real history to retrieve.
6. The valuable half (real events) cannot sit in a public repo's tamper-evident history.

## Scientific risks (LIKELY: my reasoning)
- Adaptive triage is a researcher degree of freedom against frozen settings and preregistered rules.
- Sealed or spent data could leak into later reviews through retrieval.
- Showing counts such as "11 of 14 similar ones were artifacts" anchors a human reviewer (rule 4 of the proposal already worries about this).
- More warnings is not more accuracy; a replay test could only run on planted and upside-down events, which is already what the Vesper flags do.

## Smallest useful version (kept, T124)
An evidence index inside Loom phase 4: a read-only script that builds a plain page linking existing records by star list, Vesper version and sector. No new database, no real events, nothing classified. About 0.8 point (NOT TESTED). Full OMS guess 12 to 20 points (UNCERTAIN).

## Reopen rule (my rule of thumb, UNCERTAIN)
G3 result read, Loom phase 4 exists, and about 10 real leads closed with a documented cause.

## Single decision asked, and the answer
Add systems or finish and measure the ones we have? Ahmed, 3 Nov 2026: finish and measure for the next three weeks. No new system gets a design until the T122 verdicts are in and the G3 result is read; new ideas go on a one-line parking list.

## Weakness of this review
Facts come from reading our own files (strong). The two web checks are search summaries (weak). The judgment is my own reasoning, and model reviews by the same family are the weakest evidence we have (see `research/learning-and-checking-literature-2026-11-02.md`, Part B).
