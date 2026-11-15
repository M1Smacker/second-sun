# Second Sun: session handoff, 28 October 2026 (evening, Kuwait)

Written by the long-running Claude Code session `local_7c594ce3-7265-4f13-95ce-3cd78a5e5f21` ("Unknown mysteries and problems to solve", started 19 Oct 2026 14:18 UTC, still running, model Claude Sonnet 5.5) for a fresh session in the same project. State verified at commit `4100fca`; this file's own commit follows it. Labels: CONFIRMED (a file, a tool run or a source I inspected backs it), LIKELY, UNCERTAIN, NOT TESTED. Older notes say VERIFIED; read it as CONFIRMED.

The science state is NOT repeated here. It lives in `VESPER-BRIEFING.md` (19 sections, commit `1848a6b`). This file holds what the briefing lacks: repository and session facts, non-science threads, working agreements, where we left off, and what not to trust.

Privacy: aggregates only. No star IDs or event times from the real search appear here, and none were read to write it. No Firebase keys, device IDs, tokens or email appear either.

---

## 1. Executive summary

- Second Sun is a search for circumbinary planets in public TESS data (549 Kepler-field eclipsing binaries, list "G1"), plus a public teaching book with a training game (Eyes mode). The owner is Ahmed, a student who is still learning the vocabulary.
- The search is now called **Vesper** (Ahmed chose the name on 28 Oct 2026; renaming inside the book and notes is still pending). It has seven frozen versions. The newest is **v7, hash `fd788be04650`**.
- Result of v7 on the 549 stars: tier 1 is **21 real dips against 32 upside-down dips**. No candidate exists. **Nobody, human or AI, has looked at any real event.** The 21 sit on 17 stars; none is on a TESS Object of Interest or a known circumbinary host; 3 are in the TESS eclipsing-binary catalogue. Seven of the 21 are dips seen only in the raw (SAP) light and cannot be certified, because the upside-down copy is not a fair control for that half.
- The main scientific finding of 28 Oct is a measurement of our blind spot: an 8 hour dip is found 61 times in 100 when it is 10 times the star's normal 8 hour noise, 22 in 100 at 8 times, 2 in 100 at 6 times. Faint planets could be hiding in these stars.
- The repository is clean: branch `main`, equal to `origin/main`, nothing uncommitted, nothing unpushed. The book is published to `gh-pages` at `c07f73d` and the two pages checked today return HTTP 200.
- Ahmed's open decisions (section 8): a blind shuffled look at the 7 raw-light-only dips; whether to start the briefing's plan steps 1 and 2; the rename; the real book redesign (F4) go; the outside review of `VESPER-BRIEFING.md` is expected to come back and must go through Compass before anything is built.
- Weekly usage is 38% (resets 2 Nov 21:59 UTC); Ahmed's working cap is 10 weekly points per day.

## 2. Verified repository and Git state (checked 28 Oct, about 18:20 UTC)

| Item | Value | Label |
|---|---|---|
| Path | `D:\second-sun` (a separate git repository; `C:\CLaudeCode` is the client-studio folder where this session was started) | CONFIRMED |
| Branch / HEAD | `main`, `4100fca6b73db11bc259aa785b94926f1875f826`, equal to `origin/main` (checked with `git rev-parse` and `git ls-remote`) | CONFIRMED |
| Remote | `https://github.com/M1Smacker/second-sun.git` (public) | CONFIRMED |
| `gh-pages` head | `c07f73dbf937b85578031807b352275f5ee7c78e` (book published 28 Oct; live pages `/start/first-search/` and `/field-notes/2026-10-28/` return 200) | CONFIRMED |
| Working tree | clean (`git status --short` empty), no stash, one worktree, 0 unpushed commits | CONFIRMED |
| Ignored (not in git) | `data/` (6.0 GB: downloaded light curves, real events, stage 2 and stage 3 run folders, STANLEY outputs), `.venv/`, `.venv-docs/`, `.venv-tests/`, `.cache/`, `book/site/`, `labs/out/`, `pipeline/__pycache__/`, `research/audit-2026-10-23/spoc_windows.pkl` | CONFIRMED |
| Outside the repo | `D:\ss-external` (the GPL tool mono-cbp and its own Python environment), `D:\ss-artifact-work` (paused design Artifact work), `D:\Backup-from-C` (copy-only backup script), a Firebase service-account key held in a separate folder on D: (never open it) | CONFIRMED (paths seen in notes; contents not opened) |

Last 8 commits (all 28 Oct 2026): `4100fca` Compass review of the handoff prompt; `1848a6b` VESPER-BRIEFING.md; `46e136a` RESUME bug-hunt note and ledger row; `f252ee6` PDCSAP test limits note; `6969044` book bug fixes (first-search and story pages brought to v7); `aeb2401` v7 notes; `aa29f8a` v7 frozen and measured; `79eeb99` v7 code.

Nothing is uncommitted. There are no unfinished code changes. Other repositories exist for client work in `C:\CLaudeCode`; Ahmed cancelled pushing the "exposed client repos" (TODO item A3). Do not push them.

## 3. Current pipeline and configuration

Read `VESPER-BRIEFING.md` sections 4 (chain), 5 (history), 6 (results) and 11 (script weaknesses). Short form:

- **Production chain:** `pipeline/detect_v2.py` (loader, 2 day biweight detrend, 10 minute bins, box matched filter 3 to 20 h, SNR from robust scatter), `stage2_search.py`, `audit_all.py`, `audit_paths.py`, `common_time.py`, `stage3.py`, `stage3_core.py`, `stage3_report.py`, `sap_twin.py`. Tests: `pipeline/test_stage3_prep.py` and others.
- **Measurement harnesses (not production search):** `step_retention.py`, `faint_recovery.py`, `sap_recovery.py`, `asymmetry_test.py`, `pair_search.py`, `sap_fairness.py`, `compare_versions.py`, `compare_monocbp.py`.
- **Prototypes, one-offs and early experiments:** `dryrun_kepler16*.py`, `diag_v2.py`, `borrow_windows_check*.py`, `kepler_refind*.py`, `veto_*.py`, `accept_v2.py`, `timing_s98.py`, `recover_cbp.py`.
- **STANLEY** (Martin and Fabrycky 2021, an external N-body based search): our scripts are `pipeline/stanley/inject_cbp.py`, `run_detrend.py`, `run_search.py`; outputs in `data/stanley`. It was used to time injected planets and to run one demonstration search of TOI-1338. It is NOT part of the production chain.
- **Proposals not built:** per-star bootstrap false-alarm level (no valid null), version 8 (longer detrending window for long boxes, weaker-dip storage, alias check), second target list G2, pixel and centroid vetting, planet-size completeness, any machine-learning engine (decided against on 28 Oct).

Frozen versions (hash first 12 characters read from each `research/stage3/SETTINGS_FROZEN*.json`; CONFIRMED):

| Version | Hash | Tier 1 real | Tier 1 upside-down | Change |
|---|---|---|---|---|
| v1 | 04e917e5a7e9 | 186 | 174 | first full search |
| v2 | 14c896421028 | 64 | 90 | eclipse overlap and repeater flags (chosen after seeing v1) |
| v3 | 23a74c021d8a | 15 | 38 | flat-baseline step test |
| v4 | d5767e66c4d2 | 12 | 33 | dominated, ramp, measured eclipse widths |
| v5 | 5392f864e810 | 14 | 35 | 20 hour box |
| v6 | f366d3682843 | 33 | 36 | raw (SAP) twin search |
| v7 | fd788be04650 | 21 | 32 | pooled common moment, cleaned-light check on raw-only dips |

These counts are not a progress curve: the rules change what tier 1 means.

## 4. Completed experiments and exact results

Sources are under `research/` unless noted. Details for v1 to v7 are in `research/stage3/learnings-2026-10-27.md` (sections 1 to 17).

1. **Stage 1 audit (23 Oct, not a search):** 549 stars, 8,100 light-curve files downloaded (SPOC 2 minute 1,304 sectors, TESS-SPOC 1,715, QLP 5,081), 5.4 GB; log `data\g1\manifest.csv` and `research/downloads.csv`. Target list `targets/g1_targets.csv`: Villanova Kepler EB catalogue, detached, binary period above 5 d, TESS magnitude 13.5 or brighter, 552 rows, 549 stars; 136 rows have morphology -1 (kept by accident). CONFIRMED (RESUME.md, `research/deep-research-brief-2026-10-23.md`).
2. **Stage 2 trial (23 Oct, machine only, 50 stars including 5 known hosts as controls):** 474 groups, 949 files. Events at SNR 7 or more on the best product: real 36, upside-down 84; after the cuts real 1 against upside-down 2 at the strict level. Three survivors were kept locally and are untouched (`data/stage2/survivors_LOCAL.csv`, local only). `research/stage2-2026-10-23/aggregate.txt`. CONFIRMED.
3. **TOI-1338 b validation (known circumbinary planet):** quality-mask experiment (20 Oct): the cleaned-light baseline recovers 4 of the 8 published transits that have data near them, the raw (SAP) light 7 of 8, and the union (v6 code) 8 of 8 (claims F-054, F-073). The depths are about the same in both fluxes; the raw light has the quieter noise estimate in several sectors (F-055, cause unknown). A milder quality filter found two more crossings but added noise (F-056, F-057). Injection recovery with STANLEY-timed planets into TOI-1338 sectors: 0 of 10 at 4 Earth radii, 8 of 10 at 6, 10 of 10 at 8 (F-029; read the claim for the exact set-up). Limits: one star only; the injections test box detection, not the later flags. CONFIRMED as measurements.
4. **STANLEY demonstration search of TOI-1338 (20 Oct):** 40 sectors, circular orbits, 173 trial periods from 90.05 to 100.03 d times up to 123 angles (20,482 orbits), 33 minutes; best score 18.4 sigma at 96.11 d; median score 4.2 sigma; 28% of orbits above 5 sigma, so the sigma scale is NOT calibrated (F-045). STANLEY's calibration is a pending decision for Ahmed (RESUME status row 9). The first reading of the best period (93.8 d) was wrong and corrected.
5. **Stage 3 full search and versions v1 to v7:** see section 3 and `VESPER-BRIEFING.md` sections 5 to 8. Key numbers for v7 in `research/stage3/aggregate_v7.txt`.
6. **Upside-down asymmetry:** `research/stage3/asymmetry.txt`, `asymmetry_v5.txt`, `asymmetry_v6sap.txt`. The upside-down side finds 1.25 to 2.5 times as many raw dips as the real side in the cleaned light; the raw light is lopsided the other way at low strength.
7. **Faint-dip recovery:** `faint_recovery_v5.txt`, `sap_recovery_v6.txt`, `sap_recovery_v7.txt`. Ceilings only; the flags and second-product check are not modelled.
8. **Pair search:** `pair_search_v5.txt` to `_v7.txt`: no excess of real pairs. It sees only dips at SNR 7 or more.
9. **mono-cbp yardstick on the 30 shared stars:** `research/monocbp-b-lite-2026-10-28.md`, `research/stage3/monocbp_compare_30stars.txt`. Event counts under the two tools' definitions are not comparable; on TOI-1338 b mono-cbp finds 7 of 8 transits but its own vetting labels 6 as sinusoids (F-075).
10. **Eyes mode training (Ahmed's own skill, a gate for any later real-data human review):** starter test day 1 (24 Oct): clear dips 102 of 110, quiet curves called a dip 10 of 88 (RESUME.md). The harder test was built 24 Oct. Ahmed says he keeps practising both and is improving. Current scores were deliberately NOT fetched for this handoff (he said it wastes tokens); the daily pull lands in `research/eyes-scores/rounds.jsonl`.

## 5. Sessions, agents and outstanding delegated work

- **Subagents:** none. This session made 0 Agent tool calls (CONFIRMED by counting `tool_use` entries named Agent in the 150 MB transcript `C:\Users\hanzl\.claude\projects\C--CLaudeCode\a8dcae12-19ed-4849-9f4f-b33134757b00.jsonl`; no `subagents` folder exists for it). Standing rule: ask Ahmed before using helpers.
- **Linked sessions started from this one (all CONFIRMED by `list_sessions`; none running; last activity 19 to 20 Oct):** `local_a9f84931...` wave 1a (circumbinary census), `local_3b3c90f9...` wave 1b (published searches), `local_dcb18709...` wave 1c (EB catalogues and coverage), `local_e039cd6e...` burn 2 (rivals watch and coverage reading), `local_6e62f940...` burn 1 (TOI-1338 ephemeris and recovery), `local_fe4a9c04...` burn 3 (book tech and learning track), `local_388d01da...` and `local_ba910456...` (earlier forks of this thread). Their outputs are saved files, not transcripts I re-read: `research/WAVE-QUEUE.md`, `research/burn-1-science/DONE.md`, `research/burn-2-reading/`, `research/burn-3-book/` (including `open-questions.md`), `research/key-reads.md`. I did NOT re-open their transcripts (they are reachable through the session tools). Accepted and rejected recommendations from them are recorded in `research/decisions.md` and `research/mistakes.md`.
- **Messages this session sent (3):** all to the burn 3 session on 19 to 20 Oct: the book's look ("professional and clean, not a full gamey look"), adoption of `research/SITE-BLUEPRINT.md` (status ADOPTED 19 Oct), and "extended orders" for the prototype. The burn 3 session has been idle since 20 Oct 07:35 UTC; nothing is delegated and outstanding.
- **Scheduled tasks (CONFIRMED by `list_scheduled_tasks`):** `eyes-scores-daily` is the only enabled one (cron `30 21 * * *`, pulls Ahmed's Eyes rounds from his private cloud into the repo). Its five recorded runs: succeeded 24 Oct (twice), 26 Oct 13:06 UTC, 27 Oct 18:42 UTC; failed 26 Oct 18:42 UTC with "weekly limit"; no run is recorded for 25 Oct; the next is due 28 Oct about 18:42 UTC. Seven older one-time tasks (`second-sun-runner-1` to `-5`, `second-sun-window-b-timer`, `second-sun-overnight-resume`) are disabled; runners 3 to 5 show no run time.
- **Outside AIs:** Claude AI (chat), Gemini and ChatGPT were used for outside advice and reviewed through Compass (`research/compass-reviews/`). An outside "very strong AI" is about to receive `VESPER-BRIEFING.md`; its reply, when pasted, is a Compass input and builds nothing by itself.

## 6. Known bugs, limitations and unresolved questions

The full lists are in `VESPER-BRIEFING.md` section 10 (science), section 11 (scripts), section 12 (my mistakes) and section 13 (not tested). The ones most likely to bite a new session:

1. `stage3.py run` now refuses to run frozen v7 because the report code is inside the freeze hash and `stage3_report.py` was edited after freezing (display fix only; FIX-QUEUE 21b). Nothing in the data or tiers changed.
2. The v5 "cleaned light" half contains raw light in cadences PDC dropped (`detect_v2.load` fills them); not measured over the whole run (FIX-QUEUE 21a).
3. `stage3.add_pdc` swallows per-file exceptions; they show only as "not measurable" counts (10 real, 9 upside-down).
4. No fair control exists for the raw-light half; its 7 tier-1 dips are not evidence either way.
5. The search is blind to faint dips and the target list is faint (median TESS magnitude 12.45; 237 of 549 stars have QLP data only).
6. Mutation checks for v7 ran from a scratch script that is not in the repo.
7. `pipeline/eyes_rules_test.py` writes to Ahmed's real database.
8. Readiness number in `book/progress/mission.yml` (48.0) is stale (last edited 23 Oct, 18 or more work commits since; `book/tools/teach_check.py` prompts for it). The book itself is 0 commits behind on field notes.
9. The usage ledger (`research/usage-ledger.md`) has no rows yet for: the plain-language explanation, the VESPER-BRIEFING build, the Compass pass on the handoff prompt, and this handoff. A fresh session should add one bundled row (weekly usage went from 33% to 38% across those; exact split NOT measured).
10. UNCERTAIN: the Prsa catalogue total of about 4,584 binaries (from memory); how many scripts assume the G1 layout; whether the paused visual-identity Artifact (section 14) was superseded by the Design canvas of 27 Oct.

## 7. Decisions, constraints, rejected approaches and hazards

**Decisions by Ahmed that stand (sources in RESUME.md, the TODO file, memory):**
- The pipeline's name is Vesper (28 Oct). Eyes mode and the project name Second Sun keep their names.
- Everything goes in the public book; no private split. Real events stay local; aggregates only. Human review of real events is gated behind his own Eyes practice and his explicit yes.
- Two keys: Claude's analysis and Ahmed's own check, then a write-up; ExoFOP now accepts community candidates only after publication, so the order is vetting, two keys, write-up, then upload (`book/docs/book/10-vetting.md`, row C11 and line 88). The submission path is still an open decision (`research/burn-3-book/open-questions.md` item 1).
- Terms: a detection is a dip over the threshold; a lead is a flagged dip; a candidate (SS-0001 style ID) passed first checks and needs two keys; validated and confirmed need independent evidence and publication. Nothing in the real search is above "lead". No SS ID has been issued from the real search (UNCERTAIN: confirm in `book/docs/candidates.md` before saying so to Ahmed).
- The full-search rule: v1 to v7 ran after Ahmed's explicit "go" on 27 and 28 Oct. Any new search, G2 run or version needs a new go.
- Daily cap: 10 weekly points per day (set 27 Oct); all PC layout fixes belong to the F4 redesign; auto-compact at 500K.
- Ahmed dropped the Compass upgrade item H1 and cancelled pushing exposed client repos.

**Rejected or withdrawn approaches (do not silently reintroduce):**
- A scrambled control (cannot remove single dips); a "red-noise corrected SNR" (the SNR already uses the measured box-statistic scatter); a repeater period test (vacuous); a per-star bootstrap false-alarm level (no valid null); equal-pass-rate re-weighting for the raw-light half (no survivors); a time-reversed copy (keeps dips); a machine-learning engine (VARnet and VarWISE are the wrong scale and have no planet class); copying mono-cbp code or its target table into the repo (GPL); XP, ranks and badges in the learning track; any manual copy, paste, export or "send me your scores" step for Ahmed's data; labs forced into the main reading path.

**Hazards and do-not-run list:**
- Do not run `pipeline/eyes_rules_test.py` (writes to the real database). Never click answers on the live Eyes page; verify with the local copy or `site_check.mjs eyes`.
- `python - <<EOF` heredocs hang in this shell; write scripts to files. The system Python lacks pandas; use `D:\second-sun\.venv\Scripts\python.exe` (docs tools use `.venv-docs`).
- Frozen versions are never tuned on the 549 stars. Do not open event files under `data\` or real event plots.
- Publishing the book: push main first, then run `research\burn-3-book\tools\publish_book.ps1` (it builds a fresh clone of committed main and runs the gate).
- No en or em dashes in book text or replies.

## 8. Ahmed's open decisions (do not choose for him)

| # | Decision | Status | Cost / note |
|---|---|---|---|
| 1 | A blind, shuffled look at the 7 raw-light-only tier-1 dips (with decoys), lifting the "nobody looks" rule for that set only | asked, NOT answered | 0.5 to 1 point; briefing plan step 6 |
| 2 | Start briefing plan steps 1 and 2 (planet-size completeness through the whole chain; build a second target list from the TESS binary catalogue) | asked, NOT answered | 1.5 to 2.5 plus 0.5 to 1 points; wait for the 5-hour reset |
| 3 | Rename "pipeline" to Vesper in the book, glossary and notes | pending (small, mine to do with the next publish) | batch with another book change |
| 4 | Go for F4, the real book redesign (`research/redesign-f4-plan-2026-10-27.md`): type and symbols, chapter layout on PC, Eyes layout on PC with the "smarter lines" results screen, full gate and publish | plan only, waiting for his go | calibrated 3 to 8 points |
| 5 | "Continue this" for the paused visual-identity Artifact (`D:\ss-artifact-work\RESUME-HERE.md`) | UNCERTAIN whether superseded (Design canvas v12, 27 Oct) | ask |
| 6 | The submission path to ExoFOP and a venue; STANLEY calibration; the 136 rows with morphology -1 | old pending items (RESUME status row 9, burn 3 open questions) | not urgent |
| 7 | Run the outside AI's review of `VESPER-BRIEFING.md` through Compass when it returns | expected | review only |

**My recommendation (clearly mine, not a decision):** plan step 1, the full-chain injection and recovery experiment in planet size, before anything else. Reason: it converts our blind spot into physical units, tells us which of the 549 stars are worth keeping, replaces my gut chance figure (8 in 100 for a lead worth a look in six months, 1 in 100 for a confirmed planet; both UNCERTAIN) with a measured one, and needs no new search or data. About 1.5 to 2.5 weekly points and an hour of machine time (an estimate from the ledger, UNCERTAIN).

## 9. Next-step plan with acceptance criteria

Order is the briefing's (`VESPER-BRIEFING.md` section 15). Each step waits for Ahmed's yes; none has started.

0. **Housekeeping (mine, tiny):** add the missing ledger row; rename to Vesper in the book and notes with the next publish; update `book/progress/mission.yml` only if a credit or status cell changed. Acceptance: ledger row with before and after usage; strict build passes; glossary and first-search say Vesper. Must not touch: any frozen result.
1. **Planet-size completeness through the whole v7 chain.** Extend `faint_recovery.py` and `sap_recovery.py`; convert depth to radius per brightness class using the TIC radius. Acceptance: injections off reproduces `aggregate_v7.txt`; fixed seeds; a table of the smallest radius found half the time per class; the chance model re-run with it. Must not touch: frozen settings, real event files.
2. **Second target list G2** rebuilt from the primary TESS binary catalogue (VizieR), not from the GPL tool's table; Kepler leftovers in a separate pool. Acceptance: reproducible script; counts by brightness and product; overlap with G1 and with the professionals' 591-star table reported; verify the catalogue size. No download beyond a catalogue and a coverage query without Ahmed's yes.
3. **Script clean-up behind a regression guard.** Acceptance: v7 reproduces `aggregate_v7.txt` and all tiers exactly; Stage 2 regression (74 and 298 events) identical; report outside the freeze hash; errors counted loudly; mutation scripts committed; `ARCHITECTURE.md`.
4. **Version 8** (longer window for long boxes, events stored down to SNR 5, alias check). Acceptance: recovery gain shown in planet size; false alarms not rising faster than real ones in the cleaned-light half; regression first; new freeze. G2 stays out of tuning.
5. **Run frozen v8 on G2** (fresh stars, rules frozen first).
6. **Blind look** at the 7 raw-light dips with shuffled decoys, only after Ahmed's explicit yes.

## 10. Files to read first (in this order)

1. `D:\second-sun\CLAUDE.md` (standing rules) and `D:\second-sun\RESUME.md` (top paragraphs; the newest UPDATE is first).
2. This file.
3. `D:\second-sun\VESPER-BRIEFING.md`.
4. `D:\second-sun\research\COMPASS.md` and `research\compass-reviews\2026-10-28-session-handoff-prompt.md` (contains the fresh-session opener, "Prompt B").
5. `research\stage3\FIX-QUEUE.md` (items 11 to 21 are the open weaknesses) and `research\stage3\aggregate_v7.txt`.
6. `research\stage3\learnings-2026-10-27.md` sections 11 to 17.
7. `research\TODO-after-weekly-reset-2026-10-26.md` (rules and daily budget log) and `research\usage-ledger.md`.
8. `research\redesign-f4-plan-2026-10-27.md` if the book redesign comes up.
9. The memory entries in section 16.

## 11. Commands and tests that verify the current state (all cheap and read-only)

```text
cd D:\second-sun
git rev-parse HEAD origin/main        # both should be equal; 4100fca or later
git status --short                    # expect nothing (or only this handoff before it is committed)
git ls-remote origin gh-pages main    # gh-pages c07f73d unless the book was republished
.venv\Scripts\python.exe pipeline\test_stage3_prep.py     # expect 20 "pass:" lines; dry runs 74 and 298 events identical to Stage 2 (about 40 seconds)
.venv-docs\Scripts\python.exe book\tools\teach_check.py   # expect "Book is 0 commits behind" until new work lands
```

Then: compare the first 12 characters of `hash` in each `research/stage3/SETTINGS_FROZEN*.json` with the table in section 3; read `research/stage3/aggregate_v7.txt` section 5 (tier 1: real 21, upside-down 32); list scheduled tasks and `get_usage`. Result today: 20 of 20 tests pass, 0 failures; the dry runs match.

## 12. Claims the next session must not assume are true

- That any dip in the real search is a planet, a candidate or "looks like" anything: nobody looked.
- That the 7 raw-light-only dips are camera effects (LIKELY from counts only), or that the 21 are noise.
- That "real below upside-down" shows there is no planet; the control overstates false alarms.
- That tier-1 counts across versions measure progress.
- That the faint-dip numbers are planet sizes (they are multiples of the 8 hour noise) or include the flags (they do not).
- That my chance figures (8 in 100, 1 in 100, 70% and 5% progress) are measured (they are gut).
- That the Prsa catalogue holds about 4,584 binaries (memory only).
- That the paused visual-identity Artifact is still needed, or that it is not.
- That the book says "Vesper" yet (it does not).
- That the daily Eyes pull ran today (it was due about 18:42 UTC on 28 Oct).
- That the Stage 2 survivors, STANLEY results or mono-cbp counts are comparable with the Stage 3 numbers without reading their definitions.

## 13. Working agreements and how to talk to Ahmed

- **Phone-first.** Ahmed reads on an iPhone. Put the answer in chat, plain words, short; give pushed GitHub links or the live book for longer material; prompts to copy go in a fenced block. Never say "open the file at path".
- **Questions go in plain chat text, never in popups.** No `AskUserQuestion`, no `wrap_up` ask or action buttons. Numbered text questions are fine.
- **End every finished-work reply with a "Next:" line:** the step, why it is next, its cost, and whether it starts now or needs him.
- **Tiny edits are mine** (wording, claim rows, field notes, ledger rows); big decisions are Ahmed's. Obvious follow-ups go in `FIX-QUEUE.md` and are done when best inside the cap.
- **Ask before using subagents,** each time.
- **Be straight.** Ahmed called out an implied look ("look like camera effects") that had not happened. Say "inferred from counts, not looked at". Narrate friction when it happens.
- **Verify science with sources;** label every finding; a search summary is a lead, not a source.
- **Usage ledger:** read `get_usage` before and after a task, write the estimate first, fill actuals the same day. Quote ranges from the ledger; pipeline code and Compass reviews are "uncalibrated, wide range".
- **Compass** for big proposals: review only, verdict APPROVE, REVISE or REJECT.
- **Same-day lessons:** every Second Sun work block ends with a teaching-format field note, then publish (push main first).
- **Never** make Ahmed copy his own data; never click the live Eyes page; do not fetch his Eyes scores unless he asks.
- **Ahmed's level:** he has not started the book's learning track; he practises the easy and hard Eyes tests; he understands many terms but cannot yet say them aloud, so explain simply and offer a say-it-out-loud glossary. The long-term shape: after a real planet, the book becomes his notebook with exact credit, so keep credit and authorship honest in both directions.
- Remote Control should be switched on at the start of a session (it is on for this one).
- No en or em dashes in book text or replies.

## 14. Non-science threads

- **Book and publishing:** MkDocs Material, live at `https://m1smacker.github.io/second-sun/`. Publish with `research\burn-3-book\tools\publish_book.ps1` after pushing main; last publish 28 Oct (`gh-pages c07f73d`). Claims register `book/data/claims.csv` (F-001 to F-085, 85 rows).
- **Eyes mode:** the training game in `book/docs/assets/eyes-*.js`; every round goes automatically to Ahmed's private cloud database and is pulled daily by `pipeline/eyes_scores.py`; a test device is ignored there. The readiness ladder (starter test, harder test built 24 Oct, a rehearsal in the real layout not yet built, then a first small real batch scored against hidden fakes) is in `RESUME.md`; "do not move these goalposts". The real-data tab waits for Claude's judgement of his scores.
- **F4 real redesign:** plan only (`research/redesign-f4-plan-2026-10-27.md`); includes the "smarter lines" results screen (verdict first, each fact once, a test that fails if two lines state the same count).
- **Paused visual-identity Artifact:** `D:\ss-artifact-work\RESUME-HERE.md`; resume only on "continue this"; build only the Artifact, then stop. Possibly superseded (section 8, row 5).
- **After-reset TODO:** `research/TODO-after-weekly-reset-2026-10-26.md` (phases A to H; days 1 to 3 done on 27 Oct).
- **Usage on 28 Oct:** at the start of this handoff, weekly 38% and 5-hour 31% (5-hour resets at 19:40 UTC); context of the writing session 57% of 500K.
- **Side sessions:** none active (section 5). Other sessions in the list (Morgue, V8, client websites, cricket, fitness) are other projects and are not part of this handoff.

## 15. Where we left off, step by step (28 Oct)

1. Ahmed gave the last task of the day: find and fix bugs in the book and the pipeline, no cap. He corrected the order: first the fair check for the raw-light half (FIX-QUEUE 17 and 18), then the bug hunt.
2. v7 was built, frozen, measured, documented and published; the bug hunt found and fixed several mistakes (section 6 of the briefing, section 12 there). Usage for that task: 4 weekly points against an estimate of 1.5 to 3.0 (ledger).
3. Ahmed asked for a plain-language account. I explained the pipeline as an assembly line, what we learned, what was wrong, how good it is, and gave rough percentages; I proposed the name Penumbra.
4. Ahmed pushed back: why is the search nearly blind to faint dips, why have we not worked on the weaknesses, did I look at the 7 raw-light dips, why was I not straight with him, are there more than the 549 stars, how can the scripts improve, and he did not like Penumbra. I answered: I had not looked (my "look like camera effects" was inferred from counts and badly worded); we kept re-running the same 549 because I chose to repair the judge before widening the search and never put the breadth question to him; the fix queue had no item for more stars; the scripts grew by accretion. I gave a six-step plan and six names, and asked three questions (name; blind look; start steps 1 and 2).
5. Ahmed chose **Vesper** and asked for a detailed Markdown file for a very strong outside AI. I wrote `VESPER-BRIEFING.md` (commit `1848a6b`), saved the name to memory (`project_vesper_name.md`) and sent the file. He has not yet answered the blind-look and step 1 and 2 questions.
6. Ahmed pasted several prompts. Two were withdrawn as "wrong". One of them was a review-only prompt for an outside AI that lists seven priorities: audit the SAP-filled cadences and swallowed exceptions; design a full-chain injection and recovery experiment (depth first, then planet radius with dilution and stellar-component corrections); design G2 independently from the primary TESS binary catalogue with Kepler additions in a separate pool; an empirical false-alarm calibration using several controls (matched comparison stars, block bootstrap of residuals, injected up and down signals); the smallest engineering changes that preserve v7 exactly; v8 acceptance criteria that keep G2 out of tuning and protect the final test from selection bias; and a blind inspection protocol with fair control material for the 7 raw-light-only events. He withdrew it, so treat it as context only: it shows what the outside review is likely to ask. The other withdrawn prompt was a new-session opener. The third, the handoff-writing prompt, he asked me to run through Compass.
7. Compass verdict on the handoff prompt: **REVISE** (`research/compass-reviews/2026-10-28-session-handoff-prompt.md`, commit `4100fca`): wrong premise about nested agents, a commit and push exception needed, a privacy block, memory does not carry over to a new folder, label mismatch, missing non-science state. It contains Prompt A (this handoff) and Prompt B (the fresh-session opener).
8. Ahmed said "sure": run Prompt A here, give him the handoff and show Prompt B. This file is the result.

What is waiting: Ahmed's answers to the blind look and steps 1 and 2; the outside AI's review of the briefing; the book rename; the F4 go; the missing ledger row.

## 16. Memory carry-over

Memory is stored per start folder. The originals are in `C:\Users\hanzl\.claude\projects\C--CLaudeCode\memory\`. UPDATE (28 Oct, evening, after this file was first committed): those entries (28 files: the list below plus `feedback_narrate_friction_live` and `feedback_unverified_is_not_fixed`) were COPIED, with their own `MEMORY.md` index, into `C:\Users\hanzl\.claude\projects\D--second-sun\memory\`, so a session started in `D:\second-sun` loads them. Start the new session in `D:\second-sun` WITHOUT a worktree (a worktree has a different path, so it would have no memory, no `data\` and no `.venv`). The two copies are independent: an edit in one does not reach the other. If the D-folder memory is not visible to you, read the originals explicitly (about 25 apply to Second Sun; the index is `MEMORY.md` there):

`project_second_sun`, `project_vesper_name`, `project_second_sun_becomes_his_notebook`, `project_visual_identity_artifact_paused`, `project_todo_after_reset_2026_10_26`, `feedback_daily_usage_cap`, `feedback_usage_ledger_calibration`, `feedback_autocompact_500k`, `feedback_results_clarity_smarter_lines`, `feedback_book_learn_first`, `feedback_same_day_lessons`, `feedback_no_manual_data_copy`, `feedback_no_clicking_live_eyes_page`, `feedback_phone_first`, `feedback_ask_before_helpers`, `feedback_remote_control_always_on`, `feedback_compass_review`, `feedback_verify_science_with_sources`, `feedback_always_say_whats_next`, `feedback_ask_in_text_chat_not_popups`, `feedback_small_edits_do_yourself`, `feedback_file_obvious_followups`, `feedback_dont_end_overnight_on_a_question`, `feedback_hidden_pane_throttles_timers`, `user_name_ahmed`, `user_nickname_cc` (Ahmed calls Claude Code "cc"). Their rules are copied in section 13. `D:\second-sun\CLAUDE.md` holds only part of them.

## 17. Appendix: claim ledger (claim, value, source, label)

| Claim | Value | Source | Label |
|---|---|---|---|
| HEAD equals origin/main | `4100fca6b73db11bc259aa785b94926f1875f826` | `git rev-parse`, `git ls-remote` on 28 Oct | CONFIRMED |
| gh-pages head | `c07f73dbf937b85578031807b352275f5ee7c78e` | `git ls-remote origin gh-pages` | CONFIRMED |
| Live pages return 200 | first-search, field note 28 Oct | `curl` on 28 Oct | CONFIRMED |
| Working tree clean, no stash, one worktree, 0 unpushed | as stated | git commands on 28 Oct | CONFIRMED |
| Frozen hashes v1 to v7 | table in section 3 | `research/stage3/SETTINGS_FROZEN*.json` (first 12 characters) | CONFIRMED |
| Tier 1 in v7 | real 21, upside-down 32 | `research/stage3/aggregate_v7.txt` section 5 | CONFIRMED |
| Raw-light-only tier 1 | 7 real, 0 upside-down | `aggregate_v7.txt` section 7 | CONFIRMED |
| Events, best product | 1,192 real, 1,398 upside-down | `aggregate_v7.txt` section 1 | CONFIRMED |
| Faint-dip recovery | 61%, 22%, 2% at 10, 8, 6 times the 8 h noise | `research/stage3/faint_recovery_v5.txt`, claim F-084 | CONFIRMED (ceiling) |
| Unit tests | 20 pass, 0 failures; dry runs 54 groups 74 events and 474 groups 298 events identical to Stage 2 | run on 28 Oct with the repo venv | CONFIRMED |
| Claims register size | 85 rows, last F-085 | `book/data/claims.csv` | CONFIRMED |
| This session made no Agent calls | 0 | transcript count | CONFIRMED |
| Linked sessions | 8 listed, all idle since 19 to 20 Oct | `list_sessions` | CONFIRMED |
| Scheduled task state | one enabled (`eyes-scores-daily`), 5 recorded runs, 1 failed | `list_scheduled_tasks`, `list_task_runs` | CONFIRMED |
| Usage | weekly 38%, 5-hour 31%, weekly resets 2 Nov 21:59 UTC | `get_usage` on 28 Oct | CONFIRMED |
| Stage 1 audit | 549 stars, 8,100 files, 5.4 GB | `RESUME.md` | CONFIRMED (not recounted) |
| Stage 2 trial | 474 groups, 949 files; real 36 and upside-down 84 events at SNR 7 or more | `research/stage2-2026-10-23/aggregate.txt` | CONFIRMED |
| TOI-1338 b recovery | 4 of 8 cleaned light, 7 of 8 raw, 8 of 8 union | claims F-054, F-073 | CONFIRMED |
| STANLEY search of TOI-1338 | best 18.4 sigma at 96.11 d; 28% of orbits above 5 sigma | claim F-045 | CONFIRMED (scale not calibrated) |
| Eyes starter test day 1 | clear dips 102 of 110; quiet curves called a dip 10 of 88 | `RESUME.md` | CONFIRMED (24 Oct; current scores not fetched) |
| Gut figures (8 in 100, 1 in 100, 70%, 5%) | judgment | my own, not measured | UNCERTAIN |
| Prsa catalogue size | about 4,584 | memory | UNCERTAIN |

**NOT RECOVERED / not done:** the transcripts of the eight linked sessions (only their saved files were used); Ahmed's current Eyes scores (deliberately not fetched); whether the paused Artifact was superseded; the exact usage split between the plain-language answer, the briefing, the Compass pass and this handoff; whether a Stage 2 or Stage 3 candidate ID (SS-xxxx) was ever issued; whether any script other than the five checked still assumes the G1 layout.
