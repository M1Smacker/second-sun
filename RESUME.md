# RESUME: how to pick Second Sun up again (read this first)

*Created 2026-10-20 21:55 UTC by Claude. Keep the "Status" table below current; it is the single source of truth for what is done and what is next. If the weekly limit stops work, anyone (including a fresh session a week later) can continue from here.*

## TODAY (2026-10-23, day): weekly cap raised to 65% for today (Ahmed: "put the weekly cap for today at around 65%"). Gemini's research answer was Compass-reviewed: `research/compass-reviews/2026-10-23-gemini-answer.md`. Next steps wait for his go.

## HUNT APPROVED IN STAGES (2026-10-23 evening, Ahmed: "go with your pick"): Stage 0 + Stage 1 only
**Ahmed approved Stages 0 and 1 and said to keep the book updated and explain well at the end. The limit may cut work off: he has set the session to auto-continue after the reset, so resume from this checklist. Do NOT start Stage 2 (trial search) or Stage 3 (full search) without his new go. Candidates, if ever found, stay local; two-key rule; nothing is sent to anyone.**
- **Stage 0 (preparation, no real search):** (a) B3: mask every catalogue period of a star (`mask_all_periods` in `detect_v2.py`, list from `research/wave-3-pipeline/g1_tmag.csv`, KIC 4150611 and 7622486 are the two stars affected) + test; (b) B4: `veto(..., flip_action="flag")` for the hunt (default stays "reject" so Lab 9 is unchanged) + test; (c) same-moment filter `common_time_flags()` (events from many stars in one sector+camera within 0.1 d are flagged, never deleted) + test; (d) borrowing good-time windows for QLP-only stars: SPOC G1 stars on the same sector+camera+CCD (headers CAMERA, CCD), checked leave-one-out against stars that have both.
- **Stage 1 (audit all 549 stars, NOT a search):** download every G1 SPOC 2-min, TESS-SPOC and QLP light curve (about 8,400 files, about 6.3 GB, to `D:\second-sun\data\g1\<tic>\`, resumable, logged in `research\downloads.csv`, stop and ask if the total passes 20 GB); run `pipeline/audit_paths.py` on all of them in parallel (resumable); summarise per star-sector the best product, noise, smallest findable planet, injection recovery, and refresh the odds. Real-data events are NOT recorded or looked at.
- Usage: today's cap 65% (weekly 59% when approved). If the limit stops work, continue from the first unchecked item; every script skips what is already done.

## LATEST (2026-10-23, afternoon): outside deep review found two real detector bugs
A separate research Claude answered our brief (`research/deep-review-2026-10-23/review.md`); Compass review: `research/compass-reviews/2026-10-23-deep-review.md` (verdict: APPROVE findings, REVISE odds). Re-checked here:
- **B1**: `detect_v2` finds NOTHING on 30-minute data (S14-26 FFIs; 890 of 5,081 QLP star-sectors; also Kepler long cadence). **B2**: QLP before S56 silently uses `kspsap_flux` (the transit-eating spline column), 2,845 of 5,081. Both VERIFIED on this machine. Also B3 (KIC 4150611, 7622486 extra periods unmasked), B5 (all-NaN PDCSAP returns nothing), B4 (flipped-match deletion untested; make it a flag).
- **Odds: about 20% (range 5 to 45%)**, up from 15%; mostly decided by G1's real noise (17% if like Kepler-16, 29% if like TOI-1338).
- **DONE same afternoon (Ahmed: "Apply all of the ordered changes... make sure nothing breaks"):** B1, B2, B5 fixed in `detect_v2.py` with `pipeline/test_detect_v2_paths.py` (fails on the old code); regression on all 51 local light curves: 50 identical, 1 changed by design; audit script `pipeline/audit_paths.py` + `audit_summary.py`, pilot on 7 G1 stars on disk: injection behaves, red-noise factor median 1.76 (most stars 1.2 to 2.0), pre-56 QLP SAP is about 6x noisier than SPOC. Details: `research/audit-2026-10-23/README.md`. **Next:** full audit over all G1 star-sectors (needs ~6.3 GB download, log it), B3 and B4, then the Kepler re-find test.
- **Kepler re-find test DONE (Ahmed: "Do kepler test first"):** 18 of 18 eye-confirmed transits of Kepler-16 b, 34 b, 35 b found in PDCSAP and SAP (SNR 13 to 320); extras mostly at Kepler's monthly gap edges. Key is ours (LIKELY) and holds the easier transits (7/7, 7/9, 4/7 of Davies' counts), so not yet a fair comparison with Davies. Record: `research/kepler-refind-2026-10-23/README.md`. Next: Kepler-47 d and Kepler-64 b (hard cases), then the full 549-star audit, B3, B4.
- **Original proposal (kept for the record):** fix B1/B2/B5 with self-checks that fail on the old code, then a data-path audit over all G1 star-sectors (cadence, column, noise per box, one injected transit back out), then the Kepler re-find test. TESS returns to the Kepler field in sectors 119-120 (July-August 2027): a candidate published with a prediction before then can be tested.

## NEWEST (2026-10-23, night): the book was rebuilt overnight under Ahmed's approval; cap is 50%
Ahmed said "approve, font B and start building" (23 Oct, going to sleep): build, then stress test, polish, make the home constellation realistic, stop at **50% of the weekly limit** and pause cleanly. Brief: `research/BOOK-REDESIGN-BRIEF.md`.

**Built and published (Phase 1 complete, Phase 2 partly):**
- Home page = a real-sky map (Bright Star Catalogue + the 546 plottable G1 stars from the Villanova catalog, Milky Way, chart grid, the real Cygnus cross; Albireo drawn double), `Start here` button, "where you stopped" card, readiness / candidates / latest field note. Generated by `book/shape.py` from `book/data/sky.json` (made once by `book/tools/make_sky.py`, needs internet).
- Three tabs (Read, Hunt, Reference), flat chapter list with Part dividers, Part overview pages (`docs/parts/partN/index.md`), review page per Part (`review.md`, the 48 questions moved out of the chapters), "Try it yourself" per Part (`labs.md`; labs are out of the reading line, real output first, commands in a fold).
- Everything about order lives in **`book/data/path.yml`** (Parts, 15 chapters, 3-line summaries, "why read this" lines, journey order). Chapter template (strip, 1-minute summary, story slot, mark as read, Next with reason, journey/topic switch) is added by `hooks.py` + `shape.py`; chapter files hold only their own content.
- Every chapter opens with a story (see `path.yml`); stories over 130 words fail the build.
- Glossary words auto-link at first mention and open a popup (`assets/glossary.json` built from `glossary.md`). Inter font (self-hosted), colours at 7:1 contrast (`tools/test_contrast.py`), gentle motion (reduced-motion respected).
- Gates (all run by `publish_book.ps1`, which also runs the browser layout, offline and JavaScript-off tests): `tools/test_shape.py`, `tools/test_contrast.py`, `tools/test_mission.py`, `hooks.py` self-check, strict build, `tools/check_site.py` (every link and anchor, template present, no orphans, no dashes). `book/data/path.yml` and the nav in `mkdocs.yml` must agree or the build fails.

**NOT built yet (next, in this order, each phase = publish + Field Note + Ahmed's 15-minute read):**
1. Phase 2 rest: the 15 chapter diagrams are DONE (`book/diagrams.py`, one function per chapter, a test requires one per chapter). NASA images for Parts 1 to 3 are DONE (credited in `path.yml`, files in `docs/assets/img/nasa/`, logged in downloads.csv). LEFT: pictures for Parts 4 to 6.
2. Phase 3 is DONE for the facts we hold: 15 short stories (average 69 words) in the `story:` fields of `path.yml`, each fact with a claim chip. The PH1 b story is DONE (on the Eyes mode page, claim F-059 from the ADS abstract). LEFT: any story Ahmed wants rewritten in his own voice.
3. Phase 4: DONE for three of four: planet size vs dip (the L1 lesson, existing), two stars and a planet (Chapter 5, `data-demo="orbit"`), noise (Chapter 7, `data-demo="noise"`), all in `assets/demos.js`. The fourth, the real light-curve explorer, is also DONE (Chapter 2, `data-demo="explorer"`, data `assets/data/toi1338-s98.json` made by `book/tools/make_explorer_data.py`). Phase 4 is complete. Note: in the preview pane, `requestAnimationFrame` does not run while the pane is hidden, so test animation with a stubbed rAF or the headless `site_check.mjs`.
4. Phase 5: eyes mode PRACTICE version is DONE (`data-demo="eyes"` in `assets/demos.js`, page `docs/eyes.md`, known answers only, TOI-1338 sector 98). LEFT: connect it to the hunt's real G1 stars, only after Ahmed says start (then unknown stars are mixed with the known ones). Extras DONE: cheat sheets (`parts/partN/cheat.md`, built by `cheat_page` in hooks.py) and Listen (read aloud with the device voice, section 6 of `assets/book.js`). LEFT: a recorded or better-quality voice if Ahmed wants one.
Ahmed's real read-through of the new book has NOT happened. When he reports where he got lost, that is the top fix list.

**Still true:** the star hunt and science follow-ups are on hold until Ahmed says start. Weekly cap 50%, stop exactly at 50%. Helpers: reading and checking only. Replies: short, a number with a range, no teaching in chat. Same-day Field Note rule (23 Oct note written). Nothing was rebuilt that touches science.

## STANDING INSTRUCTION FROM AHMED (2026-10-21, newest, overrides the queue below)
**The star hunt and all science follow-ups are on hold until Ahmed says to start them** ("I will only come to you and tell you to start this star hunt when I tell you to do"). That includes the next science step (task 10) and the `accept_v2.py` / `recover_cbp.py` safety fix (task 7): do NOT run them on your own, even if an earlier "go" seems to cover them. Ahmed's date predictions are logged in `research/predictions.md` (2026-10-21 row): score each date when it arrives. Allowed meanwhile, only when Ahmed asks: the mission progress bar for the book (plan first, with him), reviews of the research tools, the noise filtering and the book. He wants to save weekly usage for his other projects: keep every block small and check usage first.

## When can work continue?
- **Ahmed's weekly cap: 35%** of the weekly limit (his words, 2026-10-20: "Weekly limit cap is 35% and that's it"). Work stops at 35%, finished or not.
- The weekly window resets **2026-10-26 22:00 UTC** (27 October, 01:00 Kuwait). After that, say **"resume Second Sun"** in a new session. Nothing restarts by itself (timed tasks froze before: they need the PC and Auto mode).
- Check usage between tasks with the `get_usage` tool before starting each new step.

## What Ahmed approved (2026-10-20, in his words: "Go with whatever u recommended")
- **A. Bounded autonomy: yes.** Claude runs the frozen quality-mask experiment without asking at each step, writes the Field Note, and reports confirmed results, uncertainties and the next decision. **Stop and tell Ahmed if:** (1) the baseline reproduction does not match the saved results; (2) a step would change a tracked result or production file; (3) the usage cap is reached.
- **B. Weekly cap 35%.**
- **C. Labels: option 1.** The register keeps VERIFIED / LIKELY / UNVERIFIED. Test progress is written as plain words ("not tested yet"). CONFIRMED in the book becomes VERIFIED. (Compass reports to Ahmed may still say CONFIRMED; it means VERIFIED.)
- **Unchanged rules:** the star hunt stays paused (no G1 run, no 549 targets); the 136 unmeasured-morphology rows stay as they are (default: keep them and measure their eclipses ourselves, decide before a larger search); no helper sessions without asking; nothing outward-facing; no tokens or keys in the repo; nothing written to C:; every download logged in `research/downloads.csv` (this experiment needs none); same-day Field Note for every block of work; no dashes in book text.
- **Ahmed reads the book tonight (20/21 Oct) for the first time.** He will report "Lab N done" with results, or "LN done, 3/3". When he does: check it, then set the date in `book/progress/levels.yml`. Any friction he reports is the top fix.

## Status (update as you go)
| # | Task | Status |
|---|---|---|
| 1 | Save approvals and this file | done 2026-10-20 |
| 2 | Fix stale text and label vocabulary in the book | done 2026-10-20 (logged in mistakes.md) |
| 3 | Experiment manifest tool and frozen spec (`experiments/quality_mask/`) | done 2026-10-20 (SPEC.md + qmask.py, commits 03cbfbe, e4b1eb0; smoke-tested) |
| 4 | Reproduce the baseline (arm A0) against `pipeline/accept_v2_results.json`; stop if it does not match | done 2026-10-20: matched exactly |
| 5 | Run the SAP arms A1 (SAP + HARD) and A2 (SAP + DEFAULT) | done 2026-10-20: results in `experiments/quality_mask/results/20261020T215121Z_e40982b/` (summary.md); post-hoc diagnostics in `post_hoc/` |
| 6 | Field Note, publish book, update this file | done 2026-10-20 (Field Note evening section; Chapter 8 seventh test; claims F-054 to F-058) |
| 7 | **ON HOLD (Ahmed, 2026-10-21):** later: guard `accept_v2.py` (`__main__` guard, never overwrite tracked results); make `recover_cbp.py` save timestamped output | not started |
| 8 | Later: QLP recipe automation (OVERNIGHT.md task 12), then scale-up injection tests (about 200 trials per size, random timings, SPOC vs QLP, real fainter stars) | not started |
| 9 | Later, Ahmed's decisions: the 136 morph = -1 rows; ExoFOP publish-first path; STANLEY calibration | pending Ahmed |
| 11 | Mission readiness bar built 2026-10-21 (`book/progress/mission.yml`, `book/mission.py`, tests in `book/tools/test_mission.py`; shows on the home page and the Progress page). **When anything in the project changes, update the credits, proof, status cells and the `changes` log in mission.yml in the same commit** (the build fails if proof is missing or a change is unlogged). The search stage fills itself from `targets/g1_searched.csv` (one row per star searched, plus a header): write that file when the G1 search runs | done |
| 10 | **Next scientific question (my recommendation, needs Ahmed's go because it changes the plan):** the experiment says (a) restored SAP cadences find S62 and S30 but add noise and maybe false alarms; (b) SAP gave a quieter noise estimate than PDCSAP in several sectors. Smallest follow-ups: (i) search restored stretches separately with their own noise estimate instead of pooling; (ii) run PDCSAP and SAP both and require agreement (rule C8) instead of choosing; (iii) replicate on a second star (Kepler-16, 94 light curves) before any production change; (iv) find out why PDCSAP's noise estimate is higher (e.g. S6) | **ON HOLD (Ahmed, 2026-10-21)** |

## Result of the experiment (2026-10-20, one star; read `experiments/quality_mask/results/20261020T215121Z_e40982b/summary.md`)
Baseline reproduced exactly. Milder filter (SAP + DEFAULT) found both missing crossings (S62 SNR 12.1, S30 SNR 10.5) but lowered SNR elsewhere (median -0.54) and 6 R_earth injections went 2/7 to 0/7; flipped-data events inconclusive (restored 6.8 vs 1.0 per 100 d, intervals overlap). Separately, SAP + HARD found 7 of 8 published transits vs PDCSAP's 4, because PDCSAP's noise estimate is larger (depths equal; cause unknown). Nothing in production changed.

## The experiment in one paragraph
The question: does our HARD quality filter throw away useful cadences? Facts already verified (2026-10-20, read-only): HARD (24319) and DEFAULT (17087) differ only in bits 64, 1024, 2048 and 4096; across the 10 TOI-1338 sectors DEFAULT would restore 45,502 cadences, all bit 4096 only; **PDCSAP flux is NaN on every one of them**, SAP is finite. So PDCSAP + HARD vs PDCSAP + DEFAULT is identical (a no-op), and the old loader would silently turn DEFAULT into SAP. Valid design: **A0** = existing PDCSAP + HARD (reproduce), **A1** = SAP + HARD, **A2** = SAP + DEFAULT. A0 vs A1 isolates the flux choice; A1 vs A2 isolates the mask. Same sectors, published times (Wang and Liu 2024), hand-tuned eclipse mask geometry (held fixed from A0), 2-day detrend, SNR 7 bar, flipped (2 - f) control, S98 injections at the baseline's retained 7 times. Full review text: Compass report of 2026-10-20 (to be filed as `research/compass-reviews/2026-10-20-quality-mask.md`).

## Where things live
- Experiment code, spec, results: `experiments/quality_mask/` (new; results in timestamped folders, never overwritten).
- Frozen baseline (never touch): `pipeline/accept_v2_results.json`, `pipeline/accept_v2_log.txt`, other `pipeline/*_results.json`.
- Never import or run `pipeline/accept_v2.py` or `pipeline/diag_v2.py` (they overwrite or write to the current folder when imported or run).
- Detector (read only, import from it): `pipeline/detect_v2.py`. Book: `book/`; publish with `research/burn-3-book/tools/publish_book.ps1`. "Is the book behind?": `.venv-docs\Scripts\python.exe book\tools\teach_check.py`.
- Python for everything: `D:\second-sun\.venv\Scripts\python.exe` (caches forced to D: by `labs/_env.py` for lab-style scripts).

## Resume checklist (a fresh session)
1. Read this file, then `research/decisions.md` (last entries) and `OVERNIGHT.md`.
2. `git log --oneline -8` and `git status --short`; the book should say "0 commits behind" from `teach_check.py`.
3. Check usage; confirm the weekly figure is under 35% (after the reset it will be near 0).
4. Continue with the first task above that is not done. Update the table and write the Field Note as you finish each one.
