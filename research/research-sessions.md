# Research sessions: numbered, one line each (started 3 Nov 2026)

Why: Ahmed asked (3 Nov 2026) that every research stint gets a number and a short summary of what was searched, so it is easy to find and to plan the open questions. Method: `research/RESEARCH-BLUEPRINT.md` (applies automatically). Usage costs also go in `research/usage-ledger.md`.

## Rules
- A session is one research stint with its own usage cap, written down BEFORE it starts (a share of weekly usage, for example 5%). The number of questions is free inside the cap; small questions go with the bigger ones.
- At the end: fill the row. Count the questions still open, tell Ahmed the number, and agree a time for them with him together with the other work.
- Numbering: RS-001 and up, never reused. Research done before 3 Nov is listed below without numbers.

## Sessions
| No | Date | What we searched (short) | Cap | Used | Asked | Answered | Partly | Open | Model | File |
|---|---|---|---|---|---|---|---|---|---|---|
| RS-001 | 3 Nov | Vigil gates: MAST metadata backtest of data supply and release lag for the 2,056 stars of G1, G2, G3; QLP method change at S94 and its timing correction; TESS schedule to Sept 2028; GitHub Actions, n8n, Oracle, PythonAnywhere limits; online FDR papers; control wobble per sector on the G2 runs; period ratios of known circumbinary planets; git dates versus OpenTimestamps; alert services | 5 | about 1 (with RS-002, see below) | 49 (the Vigil block) | 16 | 5 | 28 | Sonnet 5.5 Extra | `research/stage3/vigil-literature-2026-11-03.md` |
| RS-002 | 3 Nov | Horizon: Oddo et al. 2026 (found, read), Holman and Wiegert stability formula, Armstrong 2014 occurrence, Feldman-Cousins, TTC table columns (no radii), planting code and eclipse share of time, ceiling statistics, slice check (dev only) | 3 | about 1 | 14 (the Horizon block) | 11 | 2 | 1 | Sonnet 5.5 Extra | `research/stage3/horizon-literature-2026-11-03.md` |
| RS-003 | 3 Nov | Witness: own-data kill test (channel excursions at control and real events in G1 and G2 dev SPOC files, plus the TOI-1338 b transits), Hveto paper read, novelty versus K2SFF/EVEREST/DV, channel meanings and per-product availability. VERDICT: NO-GO for now (fails its own pre-written kill rule narrowly: 6 of 40, p = 0.0139) | 1.5 | about 0.5 | 12 | 11 | 1 | 0 | Sonnet 5.5 Extra | `research/stage3/witness-literature-2026-11-03.md` |
| RS-004 | planned | Parked ideas (Twin Test T-1 to T-3, Numbers Desk N-1 to N-3, state pack S-1) and the cross-cutting questions X-1 to X-7; writes the one-page verdict per system | 1.5 | | 14 | | | | Sonnet 5.5 Extra | |
| RS-005 | planned | Closes the open and partly answered Vigil and Horizon items (29 open, 7 partly): cadence changes, multi-sector lead rule, prediction coverage, yield bracket, terms of use, secrets, determinism, list epochs, version and window rules, public/private list, ledger genesis and correction, outsider rebuild, backups, time systems, disk, MAST outages, review cost, pins, replay test, H-3, H-11, Li 2016 | 5 | | 36 | | | | Sonnet 5.5 Extra | |

**Tally after RS-002 (3 Nov):** of the 89 questions of the brief, 27 answered, 7 partly answered, 29 open inside the two researched blocks, 26 not yet researched (Witness 12, parked 7, cross-cutting 7). The two P1 questions still open in the researched blocks: V-C3 (needs a runner test and Ahmed's GitHub step) and V-D1 (Ahmed's call).

## Cost record (to size questions later; estimates from the readings, the weekly meter has 1-point steps)
- RS-001 and RS-002 together, with the G3 download fix and restart, 3 Nov 02:29 to about 02:55 Kuwait: weekly 2% to 4%, 5-hour meter 13% to 24% (about 8 five-hour points per weekly point, so about 1.4 weekly points by that ruler), context 226K to 425K tokens. About 63 questions touched, 34 answered or partly answered: roughly 0.04 to 0.06 weekly point per answered question on average.
- Size classes (my estimate from this stint, NOT precise): S = one own-data lookup or one fact from a page already open, about 0.02; M = one primary page opened and the exact sentences pulled, about 0.05 to 0.08; L = an own-data script plus sources (supply backtest, control wobble), about 0.15 to 0.25. Wall time was short because pages are read with one small script each; the context grew about 100K tokens per heavy batch, which is what drives the cost.

## Research before numbering (files only; summaries not rewritten here)
- 23 Oct: `research/deep-research-brief-2026-10-23.md`, `research/vetting-page-research-2026-10-23/`
- 28 Oct: `research/audit-2026-10-28-report.md`, `research/audit-2026-10-28-varwise-mono-cbp.md`
- 29 Oct: `research/stage3/vesper-study-literature-2026-10-29.md`
- 30 Oct: `research/live-updates-literature-2026-10-30.md`, `research/stage3/rabtsevich-literature-2026-10-30.md`
- 31 Oct: `research/stage3/post-sealed-literature-2026-10-31.md`
- 2 Nov: `research/learning-and-checking-literature-2026-11-02.md`, `research/stage3/loom-literature-2026-11-03.md`
