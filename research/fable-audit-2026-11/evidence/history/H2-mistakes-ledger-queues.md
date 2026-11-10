# H2: mistakes, usage ledger, research sessions, fix queue, build queue

Read in full on 10 Nov 2026 (read-only): `research/mistakes.md` (34 rows), `research/usage-ledger.md` (167 lines), `research/research-sessions.md`, `research/RESEARCH-BLUEPRINT.md`, `research/stage3/FIX-QUEUE.md`, `research/stage3/BUILD-QUEUE.md`. Groupings and "LIKELY" marks are my reading, not statements in the files. Nothing was run; no code was opened to confirm a status.

## 1. Mistakes: recurring patterns (34 rows, 19 Oct to 8 Nov; all "Claude")

| Pattern | Times | Worst example | Rule exists? |
|---|---|---|---|
| A. Number or claim quoted from a formula, an assumption, a different estimator or n=1, instead of a like-for-like measurement | about 13 | 19 Oct: G1 feasibility said 2 to 5 R_earth; injection with the real rule found 0/8 at 2 to 6 R_earth, 7/8 at 7 (reach overstated about 2x in radius). Runner-up 8 Nov: Census "86% to 100%" counted the three spent nulls; forward value is 21% to 52% at 1,400 stars | Yes, many (injection-recovery only; same estimator; never n=1 as typical; "forecast counts only what is still to come"; CLAUDE.md verify rule). It still recurred on 2 Nov and 8 Nov, so the rules do not stop it; only a script that can contradict does |
| B. A check that could not fail, or tested the wrong path | 7 | 23 Oct: detect_v2 gave no events at all on 30-minute data and the QLP loader silently took `kspsap_flux` before sector 56; self-check used only 2-minute data. About half of QLP star-sectors would have looked quiet. Found by an outside review | Yes (inject through every loader path; "a check must be shown to be able to fail"; re-run the unbroken version first; a safety check must abort, not count) |
| C. Git, disk and shell hygiene (ignore patterns, build output pushed, writes to C:, stray stdin command, PowerShell 5.1 encoding, escaped backslashes) | about 12 | 20 Oct: `data/` in .gitignore hid `book/data/claims.csv`, so a fresh clone could not build the book | Yes, one rule per slip; the PowerShell or escaping family recurred 3 times (23 Oct, 24 Oct, 8 Nov) |
| D. Acting for Ahmed without asking, or asking badly (nationality, approval box before content, overnight stop on a question, Eyes scores not saved, "Copy my results" button) | 5 | 23 Oct: Eyes practice built with saving off; his first rounds are lost | Yes (memory rules) |
| E. Silent selection or parsing errors (sentinel -1 passes "morph < 0.5": 136 of 552 G1 rows; regex read s2019 as a sector: 5,639 vs 5,082; MAST metadata 1,629 vs 1,304 on disk) | 3 | 20 Oct morph -1: a quarter of G1 never characterised; the row says "Not fixed yet, decision pending" and no later row closes it | Yes (treat sentinels; count what is on disk; sectors from headers) |
| F. Test able to write to production (fake rounds to the real Firebase) | 1 | 24 Oct, caught before publish | Yes (uploader paused on localhost) |
| G. Usage cap overrun | 1 logged | 8 Nov: RS-012 used about 2 points against a written cap of 0.6 | Yes, new ("size research caps by tool calls") |

Things I noticed:
- **The register thins out after 24 Oct**: 31 rows in 19 to 24 Oct, then 3 rows in 17 days. Slips recorded elsewhere in that gap have no row here: PDF link popped a save dialog (ledger 29 Oct), mkdocs check that "had never run: wrong venv" (30 Oct), wrong red-noise diagnosis and a flawed period test (28 Oct), G3 download "would finish by itself" then stalled 2h40m (FIX 72), exporter quoting bug (FIX 77), stale tasks and a 30 MB listing (FIX 78), T107 radius count 846 vs 822, clock-time slip (6 Nov), script mislabel of "fails" (6 Nov).
- **"Estimate not written first" is the most repeated slip in the project and is not in mistakes.md at all**: the ledger itself marks about 22 lapses (27 Oct to 2 Nov), against its own "no exceptions" protocol.
- Outside reviewers found the two most dangerous errors (the loader on 23 Oct, the Census odds on 8 Nov).

## 2. Usage ledger

Rough split of the logged rows (my grouping; the weekly meter has 1-point steps, so each figure is about plus or minus 1):

| Type | Tasks (about) | Points (about) | Actual / predicted |
|---|---|---|---|
| Pipeline code plus machine runs (Stage 3 v1 to v8, G2 switch, phase C, sealed run, 0.9 study, G3 prep and run) | 25 | 40 | 0.25 to 0.7 until 28 Oct, then 0.9 to 1.3 |
| Research (web plus own data, RS stints, audits, night stint of 4 Nov) | 20 stints, 60+ items | 24 | 0.15 to 0.45; one outlier 3.3x |
| Book, pages, design boards with publish gates | 15 | 21 | 0.2 to 0.5 (0.9 for a mixed day of small items) |
| Plans, Compass reviews, handoffs, notes, ask rounds | 20 | 10 | 0.3 to 0.6 |

Coverage gap (important): the ledger does not account for all the usage. Week of 27 Oct: meter 0 to 96, about 18 points have no row (for example 33 to 39, 44 to 47, 74 to 77, 80 to 83). Week of 3 Nov: rows cover about 1 to 30, 50 to 53 and 80 to 86; **30 to 50 and 53 to 80 (about 47 of 86 points) have no row**. The 6 Nov row says the meter is "partly other sessions on the account". So more than half of that week's spend is not attributed to any task.

Worst overruns:
- 8 Nov FFI door stages A to C: 3 points vs 1.6 predicted (1.9x); RS-012 alone about 2 vs cap 0.6 (3.3x); RS-013 never started because of it.
- 28 Oct v7 plus bug hunt: 4 points vs mid 2.2 (1.8x).
- 28 Oct v6 SAP twin: 1.6 vs 1.0 (1.6x), from unplanned analysis of a 19 against 1 tier-1 result.
- 30 Oct night: 10 points in one context that grew to 610K tokens; 2 to 3 Nov "night cont.": 2 points in 45 minutes at 634K to 719K.
- Reading one long pasted review cost 1 weekly point by itself (27 Oct).

Cheapest high-value tasks:
- First real Stage 3 search of 5,082 groups: about 0.4. Each of v2, v3, v4: 0.4 to 0.5.
- FIX 28 shape test: about 0.35 (gave the "minus 3 points" completeness correction).
- RS-003 Witness kill test: about 0.5 (NO-GO, saved a build). RS-004 verdicts: about 0.3.
- 4 Nov night items 1 to 3 (Census step 1 counts, lost reads, RESUME): about 0.5 for a 2.7 prediction; found G3 lost 16.1% of star-sectors.
- G3 search itself: about 1 point, 8 minutes of machine time.
- Nested Opus audit, 6 Nov: 1 point for about 20 tool rounds; changed Horizon R0 (Amendment 4).
- B-lite's unplanned SAP check, about 0.3: TOI-1338 b PDCSAP 4 of 8, SAP 7 of 8, union 8 of 8.

Cost rules of thumb stated in the files:
- About 8 five-hour points = 1 weekly point (later 6.7 to 10); about 100K to 110K added context tokens = 1 weekly point.
- Machine time is free; polling is not. "Do not poll."
- Cost per step grows with context: about 0.3 point per step after compaction, 0.5 at 200K, about 1 at 500K+; 0.05 to 0.07 per tool call at 630K+; 0.018 per call at 300K+ (so a 0.6 cap allows about 30 calls).
- Gut multipliers: design, plans, documents 0.3 to 0.6; book work with a gate 0.4 to 0.9; pipeline code plus runs 0.9 to 1.2; "own-data analysis plus a note" is priced 5 to 7 times too high (real 0.15 to 0.25 each).
- Units: Artifact publish 0.15 to 0.25; publish gate 0.1 to 0.15 (about 1 five-hour point); plan document 0.15 to 0.3; notes plus commit 0.1 to 0.25; researched question 0.04 to 0.15; two papers read as text plus scripts about 0.4; "new frozen version plus full bug hunt" 3 to 5.
- Size classes for research questions: S 0.02, M 0.05 to 0.08, L 0.15 to 0.25.
- Read only the regions the plan names (a third of F4's cost was reading); HTML not PDF; targeted JavaScript extraction is far cheaper than full page text; a fresh nested session is cheap.

Research sessions: highest number used is **RS-013**. RS-013 (K2 archive literature, cap 0.4) is NOT STARTED (stopped at the 86.5% weekly line). RS-008 WITHDRAWN (0 used). RS-012 has 2 items NOT TESTED (ASAS-SN and Hipparcos counts). RS-010 and RS-011 rows are incomplete (no used, answered or open columns; RS-011 says "more rows below as done" and none follow), and RS-010 to RS-013 sit below the "Research before numbering" section, outside the table. No number is reserved beyond RS-013; next free is RS-014. RS-001 to RS-005 tally: 89 asked, 79 answered, 5 partly, 5 open (all decisions for Ahmed).

## 3. FIX-QUEUE

Counts (my reading): **54 numbered items** (1 to 30, 61 to 84; 31 to 60 moved to the build queue). Done or closed: 26 (1 to 10, 15, 17, 18, 23, 28, 61 to 68, 71, 79, 81), plus 3 closed in effect (25, 77, 78) = 29. **Open: 25.** Items 5, 10 and 18 are done but carry open tails.

Open items:

| No | Meaning | Files | My mark |
|---|---|---|---|
| 11 | Longer detrending window for long boxes (2 d keeps 57% of a 20 h dip) [WO-4] | detect_v2, search chain (frozen) | live, changes the search |
| 12 | Injected depth to planet radius per brightness class | recovery harness | LIKELY superseded by Horizon (T119, T107) |
| 13 | Faint-dip recovery with second-product and burst flags | step_retention / recovery | LIKELY done in passing (chain recovery 29 Oct, T103) |
| 14 | Mask-before-detrend and three-window check [WO-4] | detect_v2 (frozen) | live, changes the search |
| 16 | B-lite follow-ups (same injections through mono-cbp, repeat run, more known planets) | outside clone | live, cheap (under 0.3 each); overlaps T109 |
| 19 | Second-product check against OTHER files' PDCSAP; SAP in 1,599 SPOC-family files | sap_twin.py, tiers | live |
| 20 | Recovery with every check, in planet size | sap_recovery.py | LIKELY superseded (chain_recovery, Horizon) |
| 21b | Keep the report out of the code hash | stage3_report.py, freeze | process note, open |
| 22 | "Cleaned-light half" is mostly QLP raw flux; rename, per-column asymmetry | stage3_report.py (in hash) | live, needs a freeze |
| 24 | G2 ephemeris wrong phase for about 7% of stars in C5 and overlap flags; 115 of 895 never overlap-flagged | flags, catalogue tables | live; not in 0.8.0 or 0.8.1 as far as the queue says |
| 26 | Coverage hole: 5.0% of star-sectors no product, 10% of QLP files without neighbours | stage2_search neighbour windows | duplicate of T137 (and of FIX 70's option) |
| 27 | Eclipse-timing second key [WO-20] | new | a build, misfiled in the bug list |
| 29 | Print kept share of time beside every recovery table | recovery reports | live, small |
| 30 | Orbit-locked dips | c6 switch | STALE: text ends "To build as switch c6"; the ledger says c6 was built and frozen in v8 on 30 Oct. Follow-ups are T36 and T145 |
| 69 | Local `mkdocs serve` reload loop (UNCERTAIN) | dev only | overlaps T55 |
| 70 | QLP-only events depend on the manifest | stage2_search.py `neighbour_windows` | header says "nothing fixed yet", but the 3 Nov ledger row lists a "hashed union windows table" built for G3 (0.8.1). LIKELY fixed for G3 in passing; G1 and G2 reruns still exposed; status needs a line |
| 72 | G3 download timeout | pipeline/g3_download.py | patched, never met a real timeout; G3-only script, effectively dead unless reused for Census |
| 73, 74 | Evidence chips clutter; no Back button | book.js, hooks, manifest | folded into T133 stage 1, "do not build separately" |
| 75, 76 | Voice; formulas | book.js, `.ss-eq` | folded into T133 stage 4 and the 8 Nov build order (items 3 and 4) |
| 80 | Flaky chapter browser test | site_check.mjs | open, cause UNCERTAIN; T143 proposes parking it |
| 82 | Hard-coded D: paths in 65 of 111 pipeline files [WO-8] | dataset.py and core chain (frozen) | live, needs go and a freeze |
| 83 | Tests print pass after skip; no CI [WO-9] | pipeline/test_detect_v2_paths.py | live; step 1 needs no go |
| 84 | QLP quality bit 31 not in the hard mask | detect_v2.load (frozen) | live, effect NOT TESTED; touches the G3 result |

Also: FIX 79 is ticked but says "the full script path is UNVERIFIED until the next publish"; at least six publishes followed (2.9.8 to 2.9.15) and no line closes it.

Short quotes:
- **FIX 70**: "A QLP-only star-sector's events depend on which other stars are in the data manifest (CONFIRMED 2 Nov 2026)... 77 of 583 such groups (13%) in the development slice gave different events in the 2 Nov run than in the 29 Oct run; groups with their own SPOC windows never changed (2,651 of 2,651 identical)... Options: freeze the neighbour-window table per star list as a hashed file, or take neighbours only from the star's own list. Decide before the G3 preregistration (T112). About 0.5 point." [WO-5]
- **FIX 80**: "Browser chapter test failed once, passed on its automatic retry... `a note sits 502 px from its anchor (limit 120)`... original logic 1 failure in 50 runs, patched logic 1 in 30; about 2 failures in 80 runs, a rate of roughly 1 in 40 (UNCERTAIN, wide interval). The patch made no visible difference and is reverted. STATUS: still OPEN, cause UNCERTAIN".
- **FIX 83**: "Tests can print 'pass' after 'skip', and nothing runs them automatically [WO-9]... prints 'skip B2' (line 36) and 'skip B5' (line 50) and returns, then the runner prints 'pass' (line 65)... Step 1... needs no go. Step 2 (a GitHub Actions workflow on Ubuntu, after FIX 82...) adds a system and needs Ahmed's go."
- **FIX 84**: "QLP's quality flag moves to bit 31 from Sector 56 and the loader's lightkurve 'hard' mask does not contain it (... OPEN; effect NOT TESTED)... hard mask of 24319, which includes 4096 but not 2^30. So QLP-flagged cadences of Sector 56 and later may survive `detect_v2.load`, in G3 and in any future FFI search... Frozen loader NOT touched".
- **FIX 28**: "ANSWERED 4 Nov 2026 night as a measurement: kept share at K 8 to 14 is 30.5% for the trapezoid, 26.1% skewed, 21.5% stretched (V-like), 29.1% box; the quoted completeness is probably generous by 1 to 9 points... a limb-darkened physical shape... costs 2.7 and 3.4 points (about 10% relative), so minus 3 points is the best correction."

## 4. BUILD-QUEUE

Counts (my reading): **95 distinct T-numbers** (T128 appears twice; T144 itself says "82 task lines"). Done: 16 (T37, T38 to T45, T59f, T59h, T102, T103, T105, T107, T138). Part done: T128 (G3 only). Withdrawn: T131, T132. **Open or not ticked: 76.** The file's gate ("nothing here starts until the research is done and Ahmed says go") and its total guess (33 to 40 points) date from 30 Oct and are stale.

Open items, one line each:
- T31 depth guard `dg`, T32 near-zero baseline `nd`, T33 flare shape `fl` at 0.5: built and accepted on development, NOT frozen.
- T34 step check review (biggest completeness cost). T35 decide the 3 h box. T36 cross-sector orbit-lock harness.
- T37b fresh sealed-style test of 0.9: SUPERSEDED (G3 spent the fresh list on 0.8.1; Census is next).
- T46 by-eye record per lead (needs T59d). T47 crowding note on lead cards. T48 "too deep" tag. T49 raw-light twin picture. T50 census page of 895 stars.
- T51 commit message wording. T52 read settings from the run, not env vars. T53 DONE-file marker. T54 funnel regression test. T55 preview recipe (overlaps FIX 69). T56 fresh-context rule (a rule, not a task).
- T57a to T57d chapter and quiz checks for the sealed result; T58a, T58b teaching notes: LIKELY partly done in passing (chapters 9 and 10, field notes), never ticked.
- T59a Downloads page. T59b Firebase channel. T59c F4 redesign (8 to 15). T59d real-candidate Eyes page. T59e eye-training record. T59g Ahmed's sittings.
- T60 Rabtsevich follow-up after 26 Nov (date-driven).
- T101 scrambled second control: conflicts with FIX 6, which withdrew a scrambled control as "not a null for our search".
- T104 cover and lift in planted rows: BUILT, not ticked.
- T106 cross-sector linker: absorbed by T141. T108 go-professional playbook. T109 larger known-planet test. T110 Eyes pass line.
- T111 find the list, T112 write the G3 rule: DONE in fact (G3 preregistered and run 4 Nov), not ticked.
- T113 to T116 rehearsal and learning features. T117 evidence ladder. T118 negative controls (needs Loom, held).
- T119 Horizon: R0, R1/R2 and Amendment 4 exist; R1b (real window fold, ceilings optimistic 5 to 25%) open.
- T120 Vigil: CHANGED, go later. T121 Witness: NO-GO. T122 research on new systems: effectively DONE (RS-001 to RS-005), not ticked. T123 OMS: DEFERRED. T124 evidence index (needs Loom phase 4).
- T125 lead follow-up protocol. T126 second implementation per lead. T127 wider novelty check. T129 N_eff check. T130 number-to-file audit.
- T133 Learning Space (stage 1 first; his current priority). T134 Keystone exam. T135 Search Window 2.0 (10 to 15.5).
- T136 Census (top priority; stage 2 waits). T137 window table. T139 to T153 below.
- T140 Horizon vs Davies 2026. T141 two-dip linker. T142 automatic run record (extends T128). T143 slim RESUME and publish rhythm (conflicts with two CLAUDE.md rules; his call). T144 queue triage. T146 Engine Room. T147 one name for his key. T148 PLATO count. T149 asymmetry novelty check.

Duplicates or overlaps: T106 and T141; T128 and T142; T137, FIX 26 and FIX 70; T55 and FIX 69; T50 and T43; T144 and this audit. Dead or parked: T37b, T121, T123, T131, T132, T56, T118, T124.

**Ten with the most effect on the chance of finding a planet (my judgment):**
1. T136 with T139: Census stage 2, more stars is the main lever (21% to 52% at 1,400 stars).
2. T137: recovers the 16.1% of star-sectors G3 lost (27% in sectors 27 to 55).
3. T34: the step check kept 48% of planted dips that were found 98% at K 14.
4. T141 (with T106): linking two weaker dips lowers the effective bar.
5. T152: a second FFI product; U6 covers only 22.7% of star-sectors.
6. T33 with T31 and T32, frozen: `fl` flagged about 18 of 42 upside-down tier-1 events against 1 of 26 real.
7. T35: the 3 h box holds 75% of upside-down tier-1 events; planet transits are 4.7 to 13.5 h.
8. T145: understand the orbit-locked dips that made most of the G2 excess.
9. T109: more known planets than TOI-1338 b to prove recovery.
10. T153: Gaia DR4 pool (2,392,500 EB rows against 188,407).
Not T-numbers but in the same class: FIX 11, FIX 14 and FIX 84.

Short quotes:
- **T137**: "G3 lost 16.1% of its star-sectors (655 of 4,080) because the borrowed-windows rule found fewer than 2 neighbouring 2-minute stars... about 100 sectors x 16 = 1,600 groups, roughly 3,000 small files... about +8% reach at the Kepler-16 cell; for Census it removes a 20% loss before it starts. Needs a new Petrova version... Cost about 2 to 3 points (UNCERTAIN)."
- **T139**: "Census stage 2: public EB lists first [WO-2]. Amends T136, not yet applied to the plan. Union of Prsa 2022, CALNet (10,531 stars...), TESS Ten Thousand and Gao 2025... a first slice of about 10 to 21 GB instead of 460 to 910 GB... Cost: about 1.5."
- **T145**: "Orbit-locked dips: understand them [WO-14]. Phase-fold the 8 stars of FIX 30, compare SAP and PDCSAP, check pixels... first hypothesis: shallow secondary eclipses of eccentric binaries... Report only. Cost: about 1."
- **T150**: "The Annex: an index of every flagged dip [WO-21, Ahmed's idea...]... one row per event... Rules: real and upside-down stay mixed and unlabelled; never used to change Petrova or re-score a sealed run; IDs and times private... Done when row count equals event count. Cost: about 1.3."
- **T151**: "Petrova dataset for machine learning [WO-22, Ahmed's idea; after T150]. One clean table of planted fakes, upside-down events, flagged instrumental events and Eyes labels, with light-curve cut-outs. Cost: about 1."
- **T152**: "Can the unchanged loader read TGLC and TASOC light curves...? U6 (both QLP and TESS-SPOC FFI) at only 22.7% of star-sectors; TGLC covers 35.5% of the 400 stars (lower bound), TASOC 18.5%, GSFC-ELEANOR-LITE 50% (S1 to 26)... NOT TESTED."
- **T153**: "Refresh the slow-EB pool on Gaia DR4 when it is released... vari_eclipsing_binary with 2,392,500 rows and data to 20 Jan 2020... the release date is not on the page (UNCERTAIN). The DR3 pool (188,407 rows...) is a stopgap for G5 sizing".
