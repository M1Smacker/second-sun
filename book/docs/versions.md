# Versions

A version number says which exact rules or pages a result, a score or a progress mark belongs to. A baseline is the frozen copy we compare later versions against. Only things whose results or your progress depend on them have one.

| Thing | Version now | Baseline (frozen reference) | Why it has one |
|---|---|---|---|
| Vesper, the search | 0.8.0 | 0.7.1, and 0.8.0 once the sealed search is scored | every result depends on its exact rules |
| The G2 test (lists, rules, scorecard) | rules 1.1, scorecard 1.0 | the lock of 29 Oct | the rules were written before the results |
| The book | 2.4.0 | 2.4.0 (kept before the redesign) | it changes often and you read it daily |
| Learning track | 1.3 | 1.3 | a "level done" mark means what the level contained that day |
| Eyes mode | 1.3 | 1.3 | scores are compared over time |

Version numbers follow one rule: the first number changes when the old and new results or pages are no longer directly comparable, the second when something is added, the third for fixes that change no result.

## Vesper

Earlier names: Stage 2 and "v1 to v7". The full record, with fingerprints of each frozen version, is `research/stage3/VESPER-VERSIONS.md` in the project folder.

| Version | Date | What changed |
|---|---|---|
| 0.0.0 | 23 Oct | Trial search on 50 stars: boxes 3 to 15 hours, upside-down control, the first checks |
| 0.1 to 0.2 | 27 to 28 Oct | Tiers; checks for overlap with eclipses and for many repeated dips |
| 0.3.0 | 27 Oct | Check for a step in the baseline |
| 0.4.0 | 28 Oct | Check for the slow ramp after data resumes; check for a stronger event of the other kind |
| 0.5.0 | 28 Oct | The 20 hour box |
| 0.6.0 | 28 Oct | The raw-light (SAP) twin is searched too |
| 0.7.0 | 28 Oct | One shared-moment check for both kinds replaces the old burst check; raw-light dips must show in the cleaned light |
| 0.7.1 | 29 Oct | A switch between the two star lists, no rule changed. **Baseline of the improvement study** |
| 0.8.0 | 30 Oct | The orbit-locked check. Frozen (fingerprint 5f73692944aa) and used for the one-time search of the sealed G2 stars |

Tested in the study and not taken: wider smoothing windows, a looser step test, retrained check weights, a waiver for strong dips, and dropping the 3 hour box. None gave more real dips without more false alarms than our budget allows.

## The G2 test

| Part | Version | Date | Note |
|---|---|---|---|
| Star lists | G1: 549 stars. G2: 895 stars, 301 development and 594 sealed | 20 Oct, 29 Oct | Hash-locked lists |
| Preregistration | 1.0 | 29 Oct | Locked by Ahmed before any G2 search |
| Preregistration | 1.1 | 30 Oct | Amendment 1: the sealed download is approved, the sealed search is also the Vesper benchmark |
| Scorecard | 1.0 | 30 Oct | Eight lines with pass marks written before the sealed run |
| Data downloaded | G2 development: 29 Oct. G2 sealed: 30 Oct (594 stars, 17,383 files) | | The same star can have different files later |
| Software | Python 3.12.10 and the library versions recorded on 30 Oct | 30 Oct | File `research/stage3/ENVIRONMENT-BASELINE-2026-10-30.txt` |

## The book

The numbers before 2.4.0 were worked out afterwards from the project history, on 30 Oct.

| Version | Date | What a reader notices |
|---|---|---|
| 1.0.0 | 20 Oct | The first complete book: 15 chapters, labs, learning track, glossary |
| 1.1.0 | 21 Oct | The mission readiness bar and one label vocabulary |
| 2.0.0 | 23 Oct | New navigation: the sky map on the home page, three tabs, one chapter layout |
| 2.1.0 | 23 to 24 Oct | Eyes mode, its cloud backup, the hard test, measured feedback |
| 2.2.0 | 27 Oct | One learning path; new type and the chapter rail on large screens |
| 2.3.0 | 28 Oct | The first real search page; new sections in chapters 7 to 10 |
| 2.4.0 | 30 Oct | The Search window with live counts and pictures; additions to chapters 9, 10 and 14; this page |

## Learning track

| Version | Date | Change |
|---|---|---|
| 1.0 | 20 Oct | Levels 0 to 6 |
| 1.1 | 27 Oct | One path through the levels; chapter 3 moved into level 0; a last step after level 6 |
| 1.2 | 28 Oct | Checks added for the first real search |
| 1.3 | 30 Oct | Two checks in level 5 and three in level 6 |

From now on, when a level is marked done, the track version is written next to the date.

## Eyes mode

| Version | Date | Change |
|---|---|---|
| 1.0 | 23 Oct | Answers saved at once, the truth banner, the official test |
| 1.1 | 24 Oct | The hard test with its own pass line |
| 1.2 | 24 Oct | Measured three-line feedback, the twin drill |
| 1.3 | 27 Oct | Calibrated results screen, layout for large screens |

Each saved round carries a date, the name of its deck and a data-format number, so the version a round used can be read from its date.
