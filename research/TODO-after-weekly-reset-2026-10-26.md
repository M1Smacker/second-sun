# To-do list in phases A to H, with a daily usage budget (updated 27 Oct 2026, 01:37 Kuwait)

## Rules (Ahmed, 27 Oct)
1. **Nothing starts until Ahmed says so.** "continue this" resumes the visual Artifact (see `D:\ss-artifact-work\RESUME-HERE.md`).
2. **The full 549-star search stays OFF.** All of Phase E waits for Ahmed to say "start the search". It is not in the daily plan.
3. **Daily usage budget: 10 points of weekly usage per day.** Safe-stop protocol below. This replaces the old "cap 97 percent" rule for this plan.
4. **All PC layout, sizing and scrolling fixes belong to the book redesign (Phase F).** Eyes PC layout, the wide book layout, Next without scrolling: designed once in the Artifact, built once in the real redesign. They are not fixed separately.

## Safe-stop protocol
- **Day cap = the weekly percent at the start of the day plus 10.** Day 1 (Tue 27 Oct) starts at 0, so the cap is 10 percent weekly. Unused points do not carry over unless Ahmed says so.
- Everything that moves the weekly meter counts, including Ahmed's other Claude work. The meter itself (`get_usage`) is the judge, not my estimate.
- **Before each item:** read usage. If usage plus the item's high estimate would pass the cap minus 1, do not start it. Split it or leave it for tomorrow.
- **Long items:** read usage again about every 2 points of expected work. The meter shows whole percents, so keep a 1 point buffer.
- **Never leave half-done work.** Every item ends in a checkpoint: tests pass, committed, pushed, and the status line at the top of this file updated.
- **At the cap minus 1:** finish the current checkpoint only if it fits, then stop: commit, push, write "stopped here, continue with X" below, and tell Ahmed in chat. At the cap: no new work.
- Also stop at the next checkpoint if the 5 hour window passes about 80 percent.
- Ahmed can raise or lower the cap by saying so.

## Daily budget log
| Day | Start % | Cap % | End % | Done |
|---|---|---|---|---|
| Tue 27 Oct | 0 | 10 | 5 | Day 1 done: A1, A2, B1, C1, D1, D2, F1a, H3 (A3 cancelled by Ahmed) |
| Tue 27 Oct (Day 2) | 5 | 15 | 7 | F1b learning spine built; then stop and ask for Claude AI's report (H1) |
| Tue 27 Oct (Day 3) | 7 | 17 | 8 | F2 redesign plan canvas (private), field note item; H1 dropped by Ahmed |
| Tue 27 Oct (Day 3 night run) | 8 | 14 (Ahmed set 15, then 14) | 10 so far | F2 redesign plan version 2 after Ahmed's feedback (seven boards), type and symbol tests; 5-hour stop at 98% |

## Status 27 Oct
Ahmed emailed the astronomer (26 Oct), no reply. The search no longer waits for a reply, but it is OFF until he says "start the search". The font report was reviewed by Compass (`research/compass-reviews/2026-10-27-font-advice-report.md`): approve with addendum; main finding: the fonts served today have no Greek or math symbols, so σ and ≈ come from the phone's fallback font.

"was N" means the item number in an earlier version of this file.

## Day 3 results (Tue 27 Oct; start 7 percent, cap 17, weekly usage 8 at the end; book published, gh-pages 587be84)
- **Decision (Ahmed):** drop H1, the Compass upgrade. It is revisited only if Claude judges it deserves one. For the redesign, show the plan in an Artifact.
- **F2 built as a plan canvas, not the full prototype.** Private Design canvas: https://claude.ai/artifact/D5a9xdG1NFnDVHrCJUXyTQ . Four boards: the plan page (what changes, how, choices made for Ahmed, build steps and points, what was and was not checked), a phone chapter, a PC chapter (three zones: path rail 248 px, text 600 px, margin 296 px) and PC Eyes (curve left, answers, banner and Next right, 1366 by 650, no scrolling). Real material only: Chapter 2 text, claims F-012 and F-013 (both VERIFIED), glossary entries, the TOI-1338 sector 98 curve (4 hour averages in the chart, 30 minute in the Eyes illustration).
- **Choices made for Ahmed (he can change any):** Atkinson Hyperlegible Next for everything including titles; night default (day follows the device in the boards); margin column only at 1100 px and wider; page max width 1400 px; code in system monospace and IBM Plex Mono dropped (30 KB); Greek and maths cut from Inter (has Greek) and tested before publishing.
- **Checked with a script:** contrast of every text colour on all three surfaces in both schemes (text 14.5 or better, secondary 8.8 or better, accent 7.1 or better; day brass ornament 3.5 or better); no en or em dashes in the canvas files.
- **Not checked:** how the boards look on an iPhone; the PC boards are drawings at fixed sizes, not tested layouts; fonts load from Google in the canvas only. The type's own instructions say not to open or screenshot the canvas, so none of it was rendered.
- **Next:** Ahmed approves or changes the plan (F3). F4, the real build, gets its own plan and go; rough 6 to 11 points (steps: type and Greek file 1.5 to 2.5, chapter and note PC layout 2 to 4, Eyes PC 1 to 1.5, look pass and tests 1.5 to 3).

## Day 2 results (Tue 27 Oct, after Ahmed's answers; weekly usage 6 percent at the end of the build)
- **Decisions (Ahmed):** all three spine recommendations; font = Atkinson Hyperlegible Next at 16 px; do NOT push the exposed client repos (A3 cancelled); stop after the spine and ask for Claude AI's Compass report (H1).
- **F1b done: one learning path.** `data/path.yml` has a `track:` list, the only reading order: L0 (chapters 1, 2, 3), L1 and L2 (no chapter of their own: the L1 lesson page and parts of chapters 2 and 11), L3 (7, 8), L4 (4, 5, 6), L5 (9, 10), L6 (11, 12), then "After Level 6" (13, 14, 15, unscored). Chapter numbers stay as labels. The build refuses a chapter that is missing, doubled, out of level order, or not linked in its level's section of `docs/learn/index.md`.
- **What the reader sees:** the chapter strip shows level, step "n of 15 on your path" and chapter; Next goes to the next chapter, and the last chapter of a level leads to the start of the next level (chapter 3 leads to the Level 1 lesson); the Journey/By topic buttons are gone; the Learning track page is first in the Read menu, with a "path at a glance" list generated from the data (chapters and the field notes that taught them); Start here and How to read were rewritten to point at Level 0; the old Journey page is "How the project unfolded", a story. Chapters link to the field note that taught them and the 19 and 20 Oct notes list their chapters (from the journey data only, so only 6 chapters have a note).
- **Not changed:** `levels.yml` and the readiness bar (the last step is not a scored level); the L1 lesson page is reached from the track page (it left the menu).
- **Tests added:** 5 refusals plus path checks in `test_shape.py`; `check_site.py` now expects the single pager.
- **Open for later (the redesign):** chapter 10 is split across Levels 5 and 6 and says so on the track page; the new strip text is long on a narrow phone and has not been seen on a real iPhone.

## Day 1 results (Tue 27 Oct)
- **A1 done.** `D:\Backup-from-C\Backup-C-to-D.bat`: copy only, never deletes, re-runnable. First run copied about 6 GB (client work, Claude Code data, V8, Codex, gstack). Checked: Claude's memory folder 56 of 56 files identical by hash; sign-in files left out on purpose; the repos' `.git` folders are included. A first PowerShell version was blocked by the auto-mode classifier (it used an execution-policy bypass), so it is a plain batch file now. The Claude desktop app's own data folder is not copied (it holds sign-in data).
- **A2 done.** `D:\Backup-from-C\LAPTOP-GUIDE.txt`; `requirements.txt` (main environment) and `requirements-tools/` in the repo. The LEO-Vetter and mono-cbp environments contain only pip, so there is nothing to record for them.
- **A3 not done:** pushing the client repos needs Ahmed's OK.
- **B1 done.** The finish screen says "You got N of 30 right" first, for hard rounds too; unit test and browser checks added.
- **C1 done.** Font test Artifact (private): https://claude.ai/artifact/4ZzWK4p451xZN2xp5PZ6gv. Script syntax checked; not looked at on a phone.
- **D1 done.** Reference pages "For astronomers" and "Prior work", three reading-list rows. Thornton et al. and Oddo et al. are described by their titles only, and the pages say so.
- **D2 done.** Visitor guard: visitors can play and nothing they do is sent; a device that already holds rounds stays an owner; a brand-new device of Ahmed's opens `https://m1smacker.github.io/second-sun/eyes/#owner` once. This keeps casual visitors out; it is not a lock (the Firebase rules were not changed). `eyes_scores.py` now prints which devices uploaded.
- **F1a done.** `research/compass-reviews/2026-10-27-learning-spine.md`: REVISE, three questions for Ahmed before the build (F1b).
- **H3 done.** Field note 27 Oct.
- Commit `3ff0db4`. Every gate passed (20 + 14 + 17 + 5 + 16 unit checks, strict build, 73 pages of links, colour contrast, and the five browser tests: layout, offline, JS off, eyes, eyes cloud). Published to gh-pages (`158c61a`) and checked live: the two new pages and the field note answer 200, and the live Eyes scripts contain the score line and the owner check. Not done on a real phone: reading the new pages and the score line on the iPhone (reload the book once so it updates).

## Phase A. Safety: copy to D (copy only, not a move; may be outdated)
- A1. One-click backup script on D (robocopy, never deletes old copies, skips node_modules and caches): client work `C:\CLaudeCode`, `C:\Users\hanzl\.claude` (memory of Ahmed, settings, transcripts), V8 (where `V8-LOCATION.txt` points), Al Mundhir Voucher Books, templates, Second Sun's untracked bits. Me. 0.5 to 1.
- A2. Laptop guide: what to install (Claude Code, Python, Node, Git), requirements files for the two Python environments that have none, how to point Claude at the copy (memory is filed under the folder path; copy it to the new key). Me. 0.3 to 0.5.
- A3. CANCELLED (Ahmed, 27 Oct: do not push the exposed client repos). Was: push or commit the exposed client repos (almundhir-website 1 unpushed, nexo-website 2 uncommitted, project-morgue 4 uncommitted), only after Ahmed's OK. Me. 0.1.
- A4. Ahmed: choose a small encrypted cloud copy of the critical set (memory, secrets, private leads, notes); restrict the Firebase web key to the site address; consider BitLocker on D and a small UPS.

**Phase A: 1 to 2 points.**

## Phase B. Eyes finish line
- B1. After every practice or test round, say plainly at the top of the finish screen "You got N of 30 (or 50) right", with the Dip, No dip, Odd, Not sure split, so Ahmed never has to open My results. Tests plus browser check. Me. 0.3 to 0.5.
- (The Eyes PC layout, was B2, moved to Phase F on 27 Oct.)

**Phase B: 0.3 to 0.5 points.**

## Phase C. Fonts
- C1. **Font test page**: a private Artifact, outside the book, nothing downloaded, nothing in the repo changes. Ahmed's real paragraph, a number table, "σ" labels, dark and light, 17 px / line height 1.7, a switcher: Inter and Source Serif 4 (controls), Literata, Plex Sans, Plex Serif, Atkinson. Me. 0.5 to 1.
- C2. DONE 27 Oct: Ahmed picked **Atkinson Hyperlegible Next at the smallest size (16 px)**. It has no Greek in the Google Fonts build, so the redesign must add a small Greek and math subset (σ μ λ Δ θ ≈ ≥ ≤ → √ and a few more) and test it offline. Original wording: Ahmed reads it on the iPhone at night and picks; the pick feeds F2 and F4. If Greek or math symbols are missing in the pick, add a tiny Greek and math subset (a few KB, not yet tested).
- Addendum from the Compass review to honour in the build: remove Inter's `"cv11", "ss03"` setting, lining figures in prose and tabular figures in tables, keep Literata's optical-size axis, measure real file sizes against today's 130 KB, test offline caching.

**Phase C: 0.5 to 1 point.**

## Phase D. Ready for an expert reader
- D1. A "Prior work and how we differ" page (Thornton, Montet and colleagues at UNSW on eclipse-timing precession, 27 candidates; Davies and colleagues at Warwick on mono-cbp, one candidate; Oddo and others), plus a one-page "for astronomers" start page. Me. 1 to 1.5.
- D2. Visitor guard: only Ahmed's devices count in his results and only they upload (visitors can play without any upload). Me. 0.5 to 0.8.
- D3. DONE 26 Oct: Ahmed emailed the astronomer himself. If a reply comes, share it; Compass runs on it before anything changes.

**Phase D: 1.5 to 2.3 points.**

## Phase E. The 549-star search: OFF until Ahmed says "start the search"
- E1. Pre-fixes before Stage 3: (a) put the catalogue-phase eclipse check (C5) into the pipeline; (b) mark the 237 QLP-only stars as "no second product"; (c) use real-curve false-alarm rates for list sizing; (d) cheap eclipse fold-check of the 136 stars with no measured shape (clear eclipse joins the main run, the rest become a "shape unknown" batch searched last); (e) freeze the settings and hash them; (f) emit panel data for the review page. Me. 2 to 3.
- E2. Run Stage 3 on all 5,064 usable star-sectors (machine about 2.5 to 3 hours, estimated from Stage 2: 474 groups in 15 minutes on 8 cores; the light curves are already on D) and babysit it. Me. 0.5 to 1.
- E3. Aggregates, first-tier list (about 60 events expected, factor of 2 uncertain), contact sheets. Me. 1 to 2.

**Phase E: 3.5 to 6 points.** When Ahmed says start: E1 and E2 fit one day (2.5 to 4), E3 the next.

## Phase F. The book itself: spine, look, and every PC layout fix
- F1a. Compass review of the learning spine proposal below. Me. 0.5 to 1.
- F1b. DONE 27 Oct (Day 2, see below). **Learning spine.** Today three orders disagree: topic order (1 to 15), learning-track order (L0 uses Ch 1 to 2, L3 uses Ch 7 to 8, L4 uses Ch 4 to 6, L5 to L6 use Ch 9 to 12) and journey order (starts at Ch 4). Proposal: one spine, the levels drive the order; each level shows its chapters, labs, questions and the field notes that taught it; the topic list stays as browse; the Journey page becomes "how the project unfolded"; every field note lists the chapters it touched and every chapter lists the notes that taught it. Me. 2.5 to 5.
- F2. **Visual identity Artifact** (Phase 1 only, then stop). The brief gets these additions: the one-spine structure; the chosen font (C2); and **the PC layout, designed once for the whole book and for Eyes**: a wide horizontal reading layout that uses the sides (contents rail and margin column), and for Eyes on PC a smaller, wider curve with the answer buttons, the feedback and Next in one screen with no scrolling, plus Next reachable without scrolling everywhere. Me. 4 to 7.
- F3. Ahmed approves, changes or rejects the Artifact.
- F4. **The real redesign on the live book** (Phase 2): its own plan and its own go. Includes the new look, the fonts, the wide PC layout for the whole book, the Eyes PC layout (was B2, 1 to 1.5), the spine layout, tests and the offline gate. Me. 7 to 13, a rough guess made before the design exists.
- Not planned: an interim CSS widening of the book on PC (1.5 to 3). Only if Ahmed asks for it.

**Phase F: 14 to 26 points.**

## Phase G. Vetting and publication (only if the search gives something)
- G1. Vet the first tier: automatic checks, a locked real-candidate page for the blind human key, pixel and neighbour tools if needed. Needs Ahmed's hard-test pass. Me. 5 to 9.
- G2. Publication path (ExoFOP accepts candidates only after publication): decide only when a candidate survives both keys; publish first, then pick the venue and the AI-use wording. Me. 0.5 to 1.

**Phase G: 5.5 to 10 points.**

## Phase H. Compass and housekeeping (slot in whenever)
- H1. DROPPED by Ahmed 27 Oct (revisit only if Claude judges Compass deserves an upgrade). Was: Compass upgrade: review Claude AI's report (Ahmed shares it later), then fold the useful parts into `COMPASS.md`. Me. 1 to 1.5.
- H2. Ahmed's saved prompts: a Compass review each, 0.5 to 1 each.
- H3. Field note for 25 to 27 Oct (same-day rule). Me. 0.3.

**Phase H: 1.3 to 1.8 points, plus 0.5 to 1 per saved prompt.**

## Totals
A 1 to 2, B 0.3 to 0.5, C 0.5 to 1, D 1.5 to 2.3, E 3.5 to 6, F 14 to 26, G 5.5 to 10, H 1.3 to 1.8.
**Everything: about 28 to 50 points**, plus or minus 50 percent. **Without the search and vetting (E and G): about 19 to 34**, which is what the daily plan schedules.

## Daily plan (proposed; a plan, not a promise; each day stops at its cap)
| Day | Cap | Work | Expected |
|---|---|---|---|
| Tue 27 Oct | 10 | A, B1, C1 (font test page), D, F1a (Compass on the spine), H3 | 4.1 to 7.1 |
| Wed 28 Oct | start + 10 | F1b spine build; H1 if Claude AI's report has arrived | 2.5 to 6.5 |
| Thu 29 Oct | start + 10 | F2 visual identity Artifact (needs the font pick from C2) | 4 to 7 |
| Fri 30 Oct | start + 10 | Artifact revisions after Ahmed's review (F3); plan for F4 | 1.5 to 3 |
| Sat 31 Oct to Mon 2 Nov | start + 10 each | F4 real redesign, after approval and a separate go, split across days | 7 to 13 |
| Tue 3 Nov, 01:00 | | the weekly meter resets | |

Not scheduled: Phase E (search) and Phase G (vetting), until Ahmed says. The scheduled work uses about 19 to 34 points over six days, so most days stay well under the cap.

## Ahmed's own actions
Three official starter rounds on a date after 24 Oct; hard practice (the vetting key needs it); check the new feedback lines on the iPhone (reload the book once); Firebase key restriction; choose the cloud copy; tell me which group the astronomer you emailed belongs to (UNSW or Warwick) so the prior-work page names the right one; share any reply; read the font test page on the phone and pick; share Claude AI's Compass answer.


## Day 3 night run: redesign plan version 2 (27 Oct, Ahmed asleep)
- Ahmed did not approve version 1. He asked for: Atkinson Hyperlegible Next against Literata (reading text and headings) with IBM Plex Sans for the interface and Plex Mono kept as a label candidate; a real type scale; a contextual, unobtrusive right margin; the 15 chapters kept apart from the 7 level track; Eyes without a rigid no-scroll fit; a tested self-hosted symbol font; a fair comparison with a realistic phone view. No implementation, no deployment.
- Built: seven boards in the same private canvas (Main, Type-Compare, Symbols, Phone, PC-Chapter, PC-Eyes, Zoomed), version 7, https://claude.ai/artifact/D5a9xdG1NFnDVHrCJUXyTQ. Tools and numbers: `research/redesign-type-tests/REPORT.md`.
- Decided without asking (all reversible, listed on the plan page): Option A is Atkinson for text and headings, Option B is Literata, Plex Sans for the interface in both; label face left open (Plex Mono, Plex Sans or the reading face); PC reading column 540 px (a 600 px column gave 72 to 75 characters a line); the margin opens only the note for what is on screen; Next pinned after answering on Eyes.
- Findings: Inter has no maths signs, so it is not a good fallback; Noto Sans Math cut to 23 glyphs is 1,876 bytes and a 876 byte file supplies the ballot x; Plex Mono has no Greek in the Google and Fontsource build.
- Waiting for Ahmed: pick A or B, the label face, approve or change the PC chapter, Eyes and zoom layouts. Then F4 (real redesign) gets its own plan and go. Phase E stays off.

## Ahmed's picks on the redesign plan v2 (27 Oct, about 05:00 Kuwait)
- Decision 1, reading face: **A, Atkinson Hyperlegible Next** for text and headings (Plex Sans for the interface).
- Decisions 2 to 5 he left to me ("whatever you think is best"). My picks: (2) labels and plot notes in **Plex Sans with tabular figures**, because it has Greek natively and keeps number columns aligned; Plex Mono stays for code only; (3) the right margin stays **contextual** as drawn, folding to inline notes under 1100 px and at zoom; (4) a **pinned Next bar** on Eyes after answering; (5) the **Noto Sans Math cut (1.9 KB) plus the 0.9 KB one-glyph file**.
- Still true: nothing is built; F4 (the real redesign) gets its own plan and go. Ahmed also asked for the usage ledger, now in `research/usage-ledger.md`.

## Phase E1 status (27 Oct night, Ahmed said "go 1 and then 4"): DONE except the freeze
- Done: (a) C5 in every event (`ph_d`, `c5`); (b) QLP-only label and tiers 1A, 1L, 1B, 2, 3; (c) the real-curve tier-1 count is the planning number in `stage3_report.py`; (d) shape check of the 136 stars with morph = -1: 80 clear, 56 unknown (searched last); (f) panel data deferred (no spec yet, needs the Eyes-on-real-events plan).
- Proof: `pipeline/test_stage3_prep.py` (7 checks); the Stage 2 waterfall is rebuilt exactly (real 36, 12, 7, 7, 4, 4, 4, 1; upside-down 84, 30, 21, 21, 12, 10, 9, 2); the dry run of the 5 known hosts equals Stage 2 on 54 groups and 74 events (45 s); the report's projection matches Stage 2 (about 61 tier-1 and 443 real events across the campaign).
- Not done by design: (e) the freeze (`python stage3.py freeze` writes `research/stage3/SETTINGS_FROZEN.json` and refuses if the pipeline has uncommitted changes), the search, pair search (needs Ahmed's decision, see the Compass review).
- To start when Ahmed says "start the search": from `D:\second-sun\pipeline` run `..\.venv\Scripts\python.exe stage3.py freeze` (the star list was already built once; rebuild with `stage3.py stars` if the shape check is rerun, then commit), then `stage3.py run 8` (resumable; results go to `data\stage3\<hash>\groups`; estimate 70 to 160 minutes: the dry run took 0.8 s a group, Stage 2 took 1.9 s), then `stage3_report.py <groups_dir> <label>`. Real events stay in `data\` (git-ignored). Draft settings hash today: 41f7a000 (changes if any pipeline file changes).
- Also done: F4 written plan `research/redesign-f4-plan-2026-10-27.md` (calibrated 3 to 8 points, 4 steps); same-day field note and book published (gh-pages 7650f3f, all gates passed); usage ledger `research/usage-ledger.md`.
