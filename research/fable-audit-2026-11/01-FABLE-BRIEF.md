# Fable brief: the Second Sun deep audit (run 1), then fixes on Ahmed's yes

Written 10 Nov 2026 by Opus 5.5 (medium) from 21 rounds of questions with Ahmed. His raw answers are in `00-PLAN-ANSWERS-SAVED.md` in this folder. If this brief and that file disagree, this brief wins. If either disagrees with what Ahmed says in chat, Ahmed wins.

You are Claude Fable 5.2, on medium effort. Use high effort where step 3 says so: statistics and the Petrova logic. You run as a nested session started from Ahmed's main Second Sun chat. Read this whole file before any other action.

---

## 0. Why you are here (Ahmed, in his words)

> "Man, we really need to improve our chances of finding a planet. It's my dream, man. Of course, sometimes you don't get what you want in life, but we have to keep trying, man. We have to improve our chances. We have to think outside the box while staying in it, meaning not neglecting normal data in front of you, but also thinking outside the box, which nobody other has tried or never really paid attention to." (8 Nov 2026)

> "This is huge for me. This is really huge, having Fable on my side. It's just for a little bit... I will use it fully to the max of Second Sun... This could improve our filter. This could improve our entire project Second Sun for good." (10 Nov 2026)

Ahmed owns Second Sun. It is an amateur, careful, preregistered TESS search for transiting circumbinary planets. He is a student in Kuwait (UTC+3) with exams on 13 Nov (physics) and 28 Nov (math), and he reads on an iPhone. You are his second key: an independent, stronger reviewer of everything Claude (Sonnet 5.5 and Opus 5.5) built over about 400 commits.

**The single most important outcome:** anything that raises the real chance that Second Sun finds a circumbinary planet. Judge every finding by that.

---

## 1. The absolute rules of run 1 (the audit)

**1.1 You change nothing.** You may read, run and check everything, including the frozen Petrova code, every note, all data on D: and the real G1 to G3 events. You may research the web. You do NOT:
- edit any existing file;
- file bugs or tasks in FIX-QUEUE or BUILD-QUEUE;
- change Petrova;
- push;
- publish the book;
- start any new search for planets;
- contact anyone or take any outward action.

**1.2 What you MAY write (the complete list):**
- (a) Files inside `research/fable-audit-2026-11/` (this folder): your report, STATE.md, `fable-ledger.md`, work orders, evidence, scripts and lesson drafts.
- (b) New scratch data folders `D:\second-sun\data\fable_audit_<name>\`, for downloads, injections, re-runs and outputs. One new folder per job; never write into existing data folders.
- (c) One appended line per download in `research/downloads.csv`. This is the only edit to an existing file.
- (d) The new private skill `C:\Users\hanzl\.claude\skills\second-sun-auditor\` (section 6). Ahmed allowed you to install it during run 1 because it is new and touches nothing that exists.
- (e) One local git commit of this folder at the end of run 1 (`git add research/fable-audit-2026-11` plus `research/downloads.csv`). Never push.
- (f) Your own scratchpad.

RESUME.md, `research/usage-ledger.md` and every other file are updated by Sonnet after you. Do not touch them.

**1.3 Re-runs are allowed and encouraged** when they are read-only on old data:
- injection-recovery tests;
- re-running Petrova 0.8.1 (or a modified copy kept in your scratch folder) on G1 to G3 light;
- testing the known circumbinary planets.

All of these write only into `data\fable_audit_*`. This is never a new search of unseen stars. If a re-run shows a possible real planet signal, see 1.5.

**1.4 Privacy (same rules as the project):**
- Star IDs (TIC, Gaia), event times and lead details never leave `data\`, your scratch folders or the private skill.
- Anything in the repo uses counts only.
- The report goes in the repo, so it uses counts and code only.
- If you must name stars to make a finding reproducible, put the names in `data\fable_audit_private\NAMES.md` and refer to them by code (S1, S2...).
- Never anywhere public.

**1.5 Urgent finds.** Examples: a bug that made a past null wrong, or something that looks like a real planet signal. Put it at the very TOP of the report under "URGENT", flagged, and keep working. Do not stop. A possible planet is a private lead: describe it in `data\fable_audit_private\`, never claim it, and note that the project's two-key rule applies.

**1.6 Labels.** Every important finding is labelled CONFIRMED, LIKELY, UNCERTAIN or NOT TESTED, with what you checked and links. Never invent facts, citations or checks. Bad news is said blunt and plain.

**1.7 Writing style for Ahmed:**
- no en or em dashes;
- short sentences, phone-first;
- one note in chat after each area (P, N, S, R, B, L), one or two lines;
- the full report in chat at the end (he asked for it in full).

**1.8 Helpers.** You may start read-only helper agents for searching, reading and checking, to cover more ground and keep your context small. They burn the same meter. Helpers never write anything except to your scratchpad. Give each a tight, self-contained prompt and a stated cap.

---

## 2. Usage: meters, stop lines and the week's plan

Ahmed is on the **Pro** plan. Facts below are from the Anthropic help pages read 10 Nov 2026 (support.claude.com 17506494 and 11647753). CONFIRMED:
- Fable is included until 16 Nov 2026, 11:59 pm PT (17 Nov about 10:59 Kuwait), up to 50% of the weekly limit.
- Pro gets ONE Fable reset. It gives back the usage spent on Fable on the weekly limit and refills the 5-hour window. It does not raise limits.
- Fable use LIKELY counts on "Weekly · all models" as well as on the separate "Weekly · Fable" meter.

**2.1 First 15 minutes: the meter test.**
1. Read both weekly meters and the 5-hour meter (the `get_usage` tool of the ccd_session_mgmt server; load it with ToolSearch if it is deferred).
2. Work about 15 minutes, starting with the reading in step 3.0.
3. Read the meters again.
4. Report in one chat line which meters moved and by how much.

**2.2 Stop lines for run 1.** The audit plus research plus report stops at whichever comes first:
- about **30 points on "Weekly · Fable"**;
- **"Weekly · all models" at 40%**, if Fable counts there. The reading at the start of the brief was 6%; Ahmed's physics chats also run in parallel.

Keep the last part of the budget for writing the report: the report always gets finished. If you near a stop line mid-area, write that area's findings, STATE.md and the report with what you have.

**2.3 Ahmed's week (Kuwait time). You must fit into it:**

| Day | What | Weekly bar after (rough) |
|---|---|---|
| Tue 10 | Brief written (Opus). Run 1 starts tonight. Physics chats (Ahmed gives them 15 points in total until 13 Nov). | about 22 |
| Wed 11 | Run 1 continues. Physics chats. | about 39 |
| Thu 12 | Run 1 ends: report in chat, then your question rounds wait for him. | about 53 at most |
| Fri 13 | Physics exam, then off. His math plan may happen 13 or 14 (20 points). | 53 to 73 |
| Sat 14 | Ahmed answers your question rounds (ask-tool, about 15 min on his phone). You do ONLY the approved "Fable only" fixes (at most about 12 Fable points). Then Ahmed presses the Fable reset, which refunds every Fable point used so far. | back to about 23 (+20 if math was done) |
| Sun 15 | His math plan (20) and his father's website (10). | about 53 |
| Mon 16 | His Cowork questions (20 to 30). Optional run 2 after the reset: stops at **92% on "Weekly · all models"** (about 9 points), only "Fable only" items or sharper work orders. | 83 to 92 |
| Tue 17 01:00 | Weekly reset. Sonnet 5.5 Extra takes over your work orders from Ahmed's normal Second Sun cap. | 0 |

**Consequence:**
- Run 2 may get almost nothing.
- Everything you find must be finishable by Sonnet 5.5 Extra or Opus 5.5 from your work orders alone (section 5).
- Your highest-value output is not the fixes you make. It is the findings plus work orders plus lessons you leave behind.

**2.4 Your ledger (Ahmed's request).** Keep `fable-ledger.md` in this folder. Add a row after every task, or whenever you judge best. Each row holds:
- date and time (read the clock with `Get-Date`, never guess; `resetsAt` values are UTC, add 3 hours for Kuwait);
- task and area (P, N, S, R, B, L);
- your predicted cost;
- both weekly meters and the 5-hour meter, before and after;
- actual cost;
- number of findings.

The meters move in whole points. Note that.

**2.5 Cost lessons we already paid for:**
- A research stint of about 170 tool calls on a 300K+ context cost about 3 weekly points against a 0.6 cap: about 0.018 points per call. Size caps by tool calls.
- Batch page reads into one script.
- Keep context small with helpers.
- Before compaction, write STATE.md (section 4).

---

## 3. The run 1 plan, step by step

**Order of areas:**
1. P: Petrova, the filter.
2. N: numbers and statistics.
3. S: stars and data supply.
4. R: process and project health.
5. B: book and tools, at most about 10% of the meter.
6. L: lessons for smaller models, budget your judgement, written bit by bit.

**Research:**
- About 15% of the meter goes to web research, done where the audit shows a gap.
- Follow `research/RESEARCH-BLUEPRINT.md`: questions tied to decisions, our own data first, primary sources, the exact sentence pulled out, labels.
- Number research stints RS-015 onward and mark them "(Fable)". Because you change no existing file in run 1, write the RS entries in your report under "Research stints". Sonnet copies them into `research/research-sessions.md` later.
- Check the highest RS number in that file first. Our records say RS-012 is done and RS-013/014 are not started, so you may reuse RS-013 (K2) and RS-014 (M dwarfs) if you do that research.

**Trust nothing important.** Every conclusion that steered a decision is rechecked, and every decision number is re-derived by an independent method, not by re-reading our script. Two outside checks have each found a decision-changing arithmetic error before:
- the Census odds counted spent hunts as future chance (WO-1, fixed 8 Nov);
- see `research/mistakes.md` and `research/stage3/LESSON-4-WHAT-THE-OUTSIDE-CHECK-FOUND-2026-11-06.md`.

### 3.0 Read the full history first (Ahmed's choice: everything)
Use helpers to read in parallel and summarise into your scratchpad, so your own context stays lean. Reading list, in this order:
1. `CLAUDE.md` (the standing rules) and the memory index `C:\Users\hanzl\.claude\projects\D--second-sun\memory\MEMORY.md` with its files.
2. `RESUME.md` (about 20,000 words, newest block on top).
3. `research/mistakes.md`, `research/usage-ledger.md` and `research/research-sessions.md`.
4. `research/stage3/FIX-QUEUE.md` and `BUILD-QUEUE.md`.
5. `research/stage3/` notes, newest first:
   - G3-PREREGISTRATION, G3-RESULT, VESPER-VERSIONS;
   - HORIZON-DESIGN and HORIZON-R0-RULE;
   - CENSUS-*, Q1 to Q7, LESSON-2/3/4;
   - FFI-DOOR-*, G5-SIZING, Q3-Q4, K2-CBP-LITERATURE;
   - OPUS-TRIAL-AUDIT, KEYSTONE-EXAM-SPEC.
6. `research/compass-reviews/` (all), and `research/handoff-2026-11-07/` (the outside Opus review and its 22 work orders, with our verification in `compass-reviews/2026-11-08-handoff-verification.md`).
7. `git log` (all of it, about 400 commits). Skim for decisions and reversals.
8. Earlier waves (`research/wave-*`, `audit-2026-10-23`, `deep-review-2026-10-23`): skim only.

### 3.1 P: Petrova (the frozen filter, Vesper 0.8.1). Effort: high for logic
Core chain:
- `pipeline/detect_v2.py`: the `load` loader, quality masks, flux choice per product.
- `pipeline/stage2_search.py`: the search, including the upside-down arm (`flip_action="flag"`).
- `pipeline/stage3_core.py`: tiers, `tier_of`, keys.
- `pipeline/stage3.py` and `pipeline/vopts.py`: frozen options.
- The run scripts `g3_run.py` and `sealed_run.py`.
- Version history in `research/stage3/VESPER-VERSIONS.md`.

About 9,000 lines in all, with the core about 2,000.

Settle these known doubts first:
1. **FIX 84.** From Sector 56, QLP's QUALITY flag uses bit 31, which lightkurve's "hard" mask misses. Did flagged cadences enter G3's QLP reads, and could that have changed G3's null or the S2 numbers? Measure it on the real G3 QLP files (counts).
2. **S2 failed in G2 and G3** (too many upside-down first-tier dips: pooled 8.57 per 1,000 star-sectors against the mark of 8). Find the root cause. WO-14 asks to check the eccentric-binary secondary eclipse explanation FIRST (T145). Then the others: systematics, momentum dumps, scattered light, detrending edges.
3. **FIX 70 / T137:** the QLP neighbour-window rule and the lost reads. 13.9% to 16.1% of G3 reads had no safe windows. How much light is thrown away needlessly?
4. **FIX 83:** `test_detect_v2_paths.py` prints "pass" after "skip". What else do the tests fail to test?

Ahmed's filter goals:
- catch smaller planets (the limit is about 6 Earth radii at Tmag 12 for a Sun-like host);
- fix the S2 failures;
- recover more lost light;
- handle single and long-period transits better.

Also:
- **Test Petrova on the known transiting circumbinary planets.** Use the TESS ones (TOI-1338 b, TIC 172900988 b and any others with TESS light) on real light. For the Kepler ones (Kepler-16, 34, 35, 38, 47, 64, 413, 453, 1647, 1661 ...), inject transits with their real parameters into TESS-like light of our stars. Which would we have caught, and why not the others?
- **Question everything,** including whether transit search is the best method for us. Compare with eclipse timing variations, apsidal motion and single-transit stacking. You may propose anything, even a rewrite or a new method such as a learned vetter fed by the Annex/Petrova dataset (T150/T151). Label each idea with evidence, cost and a test.

**Stop sign for Petrova and statistics (also for the lessons):** proposals for Petrova go into the report as "Petrova 1.0 candidates". The frozen 0.8.1 is never edited.

### 3.2 N: numbers and statistics. Effort: high
Re-derive independently every number that steered a decision:
- the **Census odds** (`research/stage3/census_step1/census_worth3.py`): posterior over the rate from three empty hunts, priors A and B, trim c = 0.9;
- the **S2 interval** (8.57 per 1,000; 7.08 to 10.29);
- the **Horizon reach map** (`pipeline/horizon_reach.py`, `horizon_region.py`): rule R0 Amendment 4, g = min(1, (P_b/P_p)^(2/3)/f) with f in {1.5, 1.8, 2.2}, the main scenario F = 5.6, the ceiling 0.3/E;
- **completeness:** the c = 0.9 trim (FIX 28), injection-recovery scripts (`chain_recovery*.py`, `faint_recovery.py`, `paired_recovery.py`);
- **star values:**
  - a faint star is worth 0.21 of a G2-sealed star;
  - a bright Census-type star is worth 0.45;
  - the per-1,000 E values;
  - the noise fit log10(noise8) = 0.26 + 0.211 x Tmag, extrapolated to bright stars (UNCERTAIN);
- the **G1 to G3 nulls** themselves: are they as strong as we say?
- the **occurrence anchor** (Armstrong 2014: about 10% for giants above about 6 Earth radii) and whether newer work changes it.

For each number:
- our value;
- your value and method;
- the difference;
- whether a decision changes.

### 3.3 S: stars and data supply (more and brighter stars)
- **The bright pool.** Size the true pool of bright, slow, detached eclipsing binaries that TESS saw, combining every source:
  - Gaia DR3 `vari_eclipsing_binary`: the exact pool from 8 Nov, period over 5 d, is 4,016 below G 13, 8,059 below G 14 and 14,870 below G 15;
  - CALNet (10,531 EBs; `data\calnet_2026-11-07\`);
  - Prsa 2022 (`data\xmatch\ebs.csv`);
  - TTC (`data\g3\catalog_ttc\`);
  - the 2-minute target lists S1 to 111 (`data\census_targets_2m`);
  - ASAS-SN, ZTF, WASP, KELT and other public lists.
- **Rank sources** by planet chance per point spent.
- **The full-frame door** (QLP, TESS-SPOC, TGLC, eleanor). Stages A to C gave:
  - U1 = 93% of 400 stars have FFI light in at least 2 sectors;
  - U6 = 22.7% of star-sectors have a second product;
  - Gaia periods are right for 59% (34% for TWOGAUSSIANS) against Prsa (n = 90).

  See `FFI-DOOR-TEST-PLAN-2026-11-08.md` and `FFI-DOOR-RESEARCH-2026-11-08.md`. Ahmed's choice: you may **redesign the test** as a new preregistration draft, in your folder only, rather than run stage D. Is U6 the right gate? Can TESS itself supply periods? Is QLP from Sector 94 (TGLC-based) readable?
- **Census (G4) stage 2 (T139).** CALNet first. Ahmed's 8 Nov decision: do NOT size the slow pool from the 80 Gaia periods; plan to get periods from TESS for the bright CALNet stars. Check that plan.
- **Draft G4 and G5 star-list rules.** Ahmed's G5 idea: 5,000 to 10,000 stars down to about G 14, fainter only for M-dwarf hosts. Star-list design is Ahmed's decision, so this is a draft with options.
- **M-dwarf hosts: a full study.** Pool size (we found only 46 red-dwarf stars with a good parallax), detection limit, occurrence evidence, recommendation.
- **Gaia DR4:** find the real release date, and decide whether G5 should wait for it (2.39 million EBs, 66 months of data).
- **Other missions:** K2 (80-day campaigns suit slow binaries), Kepler leftovers, CHEOPS, PLATO (LOPS2 field, launch date). Which public data has nobody searched for circumbinary planets?
- **Outside-the-box ideas:** consider many, report the **top 5 in depth**, each grounded in a paper, our data or arithmetic, with cost and a test.
- **A 2027 roadmap** ranked by planet chance per point, fitted to Ahmed's study calendar (`research/handoff-2026-11-07/04-MASTERY-PLAN.md`):
  - Checker Season to end of January;
  - boards February to May;
  - Engineer Summer June to mid-November;
  - Inventor Year from late November.

### 3.4 R: process and project health
- **Rules and memory** (CLAUDE.md, the memory files, the `my-take` skill): which rules help, which waste points or conflict? Ahmed chose to MERGE useful rules into your new skill (section 6) rather than edit the originals. Proposals for the originals go in the report only.
- **Queues:** FIX-QUEUE and BUILD-QUEUE (more than 80 build lines). Mark what is dead, duplicated or wrongly ranked. Report only.
- **Tests and reproducibility:**
  - 65 of 111 pipeline files have hard D: paths;
  - there is no CI;
  - could a stranger rerun G3 from the repo?
- **Cost per result:** study `research/usage-ledger.md`. Where did points go, and how do we get more science per point?
- **Pending decisions from 8 Nov.** Give a recommendation on each, asked in your end rounds:
  - S2 option A, B or C (Opus leaned A);
  - the name for Ahmed's second key (first or second);
  - shortening RESUME with history moved to RESUME-ARCHIVE.md;
  - pushing the local commits (16f3f0a onward; nothing has been pushed since);
  - an outside check on every number that reaches Ahmed as a decision.

### 3.5 B: book and tools (at most about 10% of the meter)
- **Book** (`book/`, MkDocs; published by `research\burn-3-book\tools\publish_book.ps1 -Test`):
  - wrong or stale science;
  - the learning track design (his daily tool; his top annoyance is "not having a complete dashboard for reading/learning"; agreed build order in memory `project_learning_track_build_order.md`);
  - structure and clutter on a phone;
  - the publish pipeline.
- **Tools** (Eyes, the Search window page, the live-update and export scripts):
  - could a tool show a wrong or misleading result?
  - could a star ID or event time leak publicly?
  - breakage and flaky tests (FIX 80).

**NEVER click the live Eyes page** (m1smacker.github.io): answering cards uploads to Ahmed's real cloud. Read the code instead.

### 3.6 L: lessons for smaller models (see section 6)
Write lesson notes as you go, the moment a finding teaches something. Do a final editing pass before the report.

---

## 4. Checkpoints and continuity

- **STATE.md** in this folder, updated after every step: done, doing, next, meter readings, open threads. Any model (or you after compaction or the reset) must be able to resume from it alone.
- Before any compaction, write STATE.md first, then continue alone.
- **Evidence:** save every script and output you rely on, under this folder (code, counts) or `data\fable_audit_*` (data), so a smaller model can rerun and check it.
- Write each area's findings into the report as soon as that area ends.

---

## 5. The report and the work orders

**5.1 `REPORT.md` in this folder.** It opens with:
1. **URGENT** items, if any.
2. **One plain verdict line.**
3. **A ranked findings list.** Rank by effect on the chance of finding a planet. For each finding:
   - ID (F-01 ...) and area;
   - label (CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED) and the evidence (files, lines, the output that shows it);
   - effect on planet chance (rough change in expected detections E or the odds, or "protects a null");
   - risk if ignored;
   - cost in weekly points per model (Sonnet 5.5 Extra / Opus 5.5 / Fable);
   - difficulty tag: **Sonnet ok**, **Opus needed** or **Fable only**;
   - link to its work order.

After the list:
- "Research stints" (RS entries ready to copy);
- "Petrova 1.0 candidates";
- "Top 5 outside-the-box ideas";
- "2027 roadmap";
- "Proposed rule changes";
- "Decisions for Ahmed".

**5.2 Work orders: the most important thing you leave behind.** Run 2 may never happen, so every finding needs a work order (`work-orders/WO-F01.md` ...) that Sonnet 5.5 Extra can execute cold, without you. Each work order holds:
- **Goal**, in one sentence.
- **Why it matters**, in plain words.
- **Exact location:** files, functions, line numbers, and the commit you read them at.
- **Evidence and how to reproduce it:** the command, the expected output, where your saved script is.
- **Step-by-step method,** small steps. Say what the right result looks like at each step.
- **The proof test:** what must be true after the fix, and how to check it.
- **Traps:** the mistakes a weaker model is likely to make here, what you saw that it might miss, and why.
- **Do not touch:** frozen files, sealed results, private data.
- **Stop signs:** when to stop and ask Ahmed, or flag for Opus or Fable, instead of guessing. This is mandatory for anything touching Petrova or a decision number.
- **Model and cost:** which model, and the predicted points.
- **Needs Ahmed's yes?:** yes for Petrova changes, star-list design, any search, outward actions and S2. Otherwise per the rules.

**5.3 In chat at the end of run 1:**
- The full report, in Ahmed's style.
- Then "Run 1 done". Tell him exactly when to press the Fable reset: AFTER the approved fixes on 14 Nov, not before.
- Then your **decision rounds** using the AskUserQuestion tool (Ahmed asked for ask-tool rounds; up to 4 questions per round, 2 to 4 options each, your recommendation first and marked). Cover:
  - which findings to fix;
  - which are "Fable only" and should be done by you before the reset;
  - the pending 8 Nov decisions;
  - Petrova 1.0 direction;
  - G4 and G5 star-list options;
  - the FFI-door redesign;
  - rule merges.

**5.4 The fix step (14 Nov, before the reset), only after his answers:**
- Do ONLY the approved "Fable only" items, at most about 12 Fable points.
- Petrova 0.8.1 stays frozen. A Petrova change means a new version per `VESPER-VERSIONS.md` and the project's versioning rules, never a silent edit, and never re-interpreting sealed results.
- Commit locally, never push.
- Then file the approved findings into FIX-QUEUE and BUILD-QUEUE (tag [FABLE-Fnn]); Ahmed's yes makes this allowed.
- Tell him: "press the reset now".

---

## 6. Lessons for smaller models: the `second-sun-auditor` skill

**Purpose (Ahmed):**
- You cannot hand over your reasoning, but you can leave checklists, worked examples and "always check" rules.
- These make Sonnet 5.5 Extra and Opus 5.5 better at this project: scanning for bugs, fixing without new bugs, checking numbers, researching and planning.

**Where and when:**
- Ahmed's private user skills: `C:\Users\hanzl\.claude\skills\second-sun-auditor\SKILL.md`, plus any reference files beside it.
- Private, never in the repo. Because it is private it may hold anything, including real examples.
- Installed during run 1 (Ahmed's explicit exception).
- Budget: your judgement.

**Format:**
- A standard skill with front matter (`name`, and a `description` that triggers it when a model audits, fixes, tests, researches, plans or checks numbers in Second Sun).
- Keep SKILL.md tight; put long material in reference files it links.
- One set of rules for all models (no per-model versions).

**Must contain:**
1. **How to scan for bugs here:**
   - where bugs hide in this repo (quality masks and flag bits, time systems BJD/BTJD/TCB, units, window edges, off-by-one, file products and eras, hard paths, silent skips);
   - each with what to check.
2. **How to fix without making new bugs:**
   - test first;
   - smallest change;
   - frozen-version discipline;
   - what to re-run after a fix;
   - never call a fix done without running it (memory: "unverified is not fixed").
3. **How to check numbers:**
   - re-derive independently;
   - sanity limits and units;
   - the errors outside checks caught (WO-1 and others).
4. **How to research and plan:**
   - the research blueprint in practice;
   - sizing caps by tool calls;
   - planning order;
   - predicting cost.
5. **Using the usage meter wisely:** the cost rules from the ledger, batching, when to stop.
6. **"Mistakes Claude keeps making here", blunt:**
   - from `research/mistakes.md`, the ledger, the outside reviews and your audit;
   - each pattern with the rule that stops it (for example budget overruns, untested "fixes", guessed clock times, guessed numbers).
7. **Stop signs (Petrova and statistics only):** situations where a smaller model must stop, label UNCERTAIN and ask Ahmed or flag for Opus or Fable instead of guessing.
8. **3 to 6 short worked examples:** before and after code of real bugs you found.
9. **Merged useful rules** from CLAUDE.md, memory and `my-take` (Ahmed chose to merge into the skill rather than edit the originals). Note the source of each.
10. **Upkeep rule:** any model may ADD a lesson when a new mistake is caught (dated, with the source). Rules you mark "core, do not weaken" are never weakened or removed without Ahmed's yes.

**Proof that it helps (prepare now, run next week):**
- Build a **blind bug test** in `data\fable_audit_bugtest\`: a scratch copy of a few pipeline files with 4 to 8 planted bugs of the kinds you found. Never touch the real code.
- Answer key in `data\fable_audit_private\BUGTEST-KEY.md`.
- A work order `work-orders/WO-BUGTEST.md`: next week, Sonnet 5.5 Extra hunts the bugs once WITHOUT the skill and once WITH it (fresh sessions), and the scores are compared.

---

## 7. Glossary (what our words mean)

- **Second Sun:** the project. **Book:** the MkDocs site in `book/`, published to GitHub Pages.
- **Petrova (= Vesper 0.8.1):** the frozen search filter. "Vesper" is the code name in files; Ahmed calls it Petrova, and the rename waits for his go.
- **Frozen:** settings and code fixed per version, never tuned on results.
- **G1, G2, G3:** the three hunts so far, all empty of leads.
  - G2 has a development half and a sealed half.
  - G3 used 611 TTC stars, mostly FFI light (QLP), and spent Vesper 0.8.1's one-shot.
- **G4 = Census:** our own eclipsing-binary list from post-sector-26 TESS data, chosen by value. Stage 1 is done; stage 2 (T139) is planned.
- **G5:** the next, bigger hunt (5,000 to 10,000 stars to about G 14).
- **Real arm / upside-down arm:** the search runs on real light and on flipped light. Upside-down dips measure the false-alarm rate.
- **S1 / S2:** the preregistered success checks. S1: no excess on the real arm. S2: upside-down first-tier dips at most 8 per 1,000 star-sectors. S2 FAILED in G2 and G3.
- **Tiers 1A, 1L, 1B, 2:** event tiers in `stage3_core.tier_of`. 1A and 1L need a second product; 1B is one product only. Flagged events go to tier 2.
- **Keys / two keys:** independent confirmations. A named lead needs two keys and Ahmed's yes before anything is said.
- **Horizon (reach map):** our expected-detections model. E = expected planets at a 10% rate; ceiling = 0.3/E; rule R0 Amendment 4.
- **Census odds:** the forward chance that G4 finds at least one planet.
- **FFI door:** using full-frame-image light curves (QLP, TESS-SPOC, TGLC) for stars with no 2-minute data.
- **U1 to U9:** the FFI-door metrics.
- **CALNet:** a public list of about 10,531 EBs from 2-minute data, sectors 1 to 88.
- **TTC:** the TESS Ten Thousand Catalog.
- **Prsa 2022:** the TESS EB catalogue.
- **FIX n / T n:** items in FIX-QUEUE (bugs) and BUILD-QUEUE (builds, studies).
- **WO-n:** the outside handoff's work orders (2026-11-07).
- **RS-nnn:** numbered research stints.
- **Compass review:** our review-only pass on big advice.
- **Eyes:** Ahmed's card-scoring tool (live page; never click it).
- **Search window:** the book page that shows a hunt's progress.
- **Keystone (T134):** the second-key exam.
- **Checker Season, Engine Room:** parts of Ahmed's study plan.
- **The Annex (T150):** the library of everything the filter flagged.
- **The Petrova dataset (T151):** labelled events for a future vetter.
- **Points:** weekly usage points (percent of the weekly limit).

## 8. Repo map

- `pipeline/`: all science code (about 111 files). Core chain: `detect_v2.py` (load), `stage2_search.py`, `stage3_core.py`, `stage3.py`, `vopts.py`. Also run scripts (`g3_run.py`, `sealed_run.py`), recovery/injection scripts, Horizon (`horizon_reach.py`, `horizon_region.py`), tests (`test_*.py`) and Eyes scripts (`eyes_*.py`).
- `targets/`: the hunt target lists (`g1_targets.csv`, `g2_targets.csv`, `g3_targets.csv`).
- `data/` (git-ignored, private):
  - light curves and outputs per hunt (`g1`, `g2`, `g3`, `stage2`, `stage3`, `stage3_g2`, `stage3_g3`; events in `.../groups/*.json`, real and upside-down together);
  - `census_targets_2m` (2-minute lists S1 to 111);
  - `calnet_2026-11-07`, `xmatch`, `ffi_door_2026-11-08` (the 400-star sample, IDs private), `known` (known planets);
  - plus many dry runs.
- `research/`:
  - `stage3/`: current notes, queues, preregistrations, census and FFI scripts;
  - `compass-reviews/`, `handoff-2026-11-07/` (outside review);
  - `mistakes.md`, `usage-ledger.md`, `research-sessions.md`, `downloads.csv`, `jobs.md`, `RESEARCH-BLUEPRINT.md`;
  - `burn-3-book/tools/` (book publish script);
  - older `wave-*` folders.
- `book/`: `docs/` (pages, learning track `learn/`, `versions.md`), `mkdocs.yml`, `tools/`.
- `labs/`, `experiments/`, `proofs/`: older side work.
- Private backup of all G1 to G3 event JSONs: `D:\ss-private-backup\events-g1-g3-2026-11-08\` (read-only, hash-verified).
- Python:
  - venvs in `.venv*`;
  - PowerShell `python` has numpy;
  - plain `python -I` lacks astropy and lightkurve, so check the right venv first;
  - set PYTHONUTF8=1 and PYTHONIOENCODING=utf-8.
- Windows tips:
  - use absolute paths (the .NET process directory differs from PowerShell's);
  - some files are CRLF;
  - a foreground `sleep` is blocked, so run long jobs in the background.

## 9. Mistakes history to keep in mind
Read `research/mistakes.md` fully. Patterns so far:
- Arithmetic that changed decisions, caught only by outside checks:
  - WO-1 counted spent hunts as future chance;
  - Opus trial audit, 6 Nov.
- "Fixes" called done without being run: 3 of 12 had failed.
- Budget overruns: 1.9 times predicted on 8 Nov.
- Guessed clock times.
- Estimates from small sky samples that were 27% to 40% too high.
- A test that prints "pass" after "skip".

You are here to find the ones we have not seen.

---

## 10. Start checklist
1. Read this brief and `00-PLAN-ANSWERS-SAVED.md`.
2. Read the meters. Create STATE.md and `fable-ledger.md`.
3. Post one chat line to Ahmed: "Fable run 1 started, meters X/Y/Z, first note after 15 minutes."
4. Step 3.0 (reading, with helpers), then the meter test line (2.1).
5. Areas P, N, S, R, B in order, with lessons written as you go. One chat line per area.
6. Report, chat report, decision rounds. Then wait for Ahmed.
