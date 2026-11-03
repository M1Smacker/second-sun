# Search Window 2.0: audit and design proposal (4 Nov 2026, early morning)

Answer to the pasted prompt "Search Window 2.0, personal astronomical mission control, deep audit and design proposal". REVIEW ONLY: nothing of the redesign is built. Compass: `research/compass-reviews/2026-11-04-search-window-2.md` (REVISE). Separate from the review, Ahmed asked tonight for the CURRENT page to be made ready for the G3 search; that small change is described in section 0 and is the only code touched. Waits for his explicit approval. Labels: CONFIRMED (read in a file, counted by script, or seen in the published feed), LIKELY, UNCERTAIN, NOT TESTED.

Read in full: `book/docs/watch.md`, `book/docs/assets/watch.js`, `pipeline/watch_export.py`, `pipeline/leads_export.py`, `pipeline/g3_run.py`, `pipeline/g3_go.ps1`, `pipeline/sealed_run.py` (launch lines), `pipeline/stage3_core.py` (tier rule), `research/stage3/benchmark-g2-sealed.txt`, `research/stage3/LEADS-RULES.md`, the live feed (`origin/watch-data:watch.json`) and the book snapshot. Skimmed by search: the 30 Oct and 3 Nov field notes (Search window passages only), `book/data/claims.csv` (not needed for the page). NOT read: the rest of the field notes, `shape.css`, service-worker caching of the snapshot. Real events were not inspected beyond the fields the published feed already carries; the live Eyes page was not touched.

## 0. Done tonight (not part of the redesign): the current page made ready for G3
CONFIRMED by test on a local copy; live after the book publish and the feed push, see the ledger and field note.
- New phase `ready`: "PREPARED, NOT STARTED" (a ring, no pulse, no stale alarm), shows 612 stars on the list, 611 with light-curve files, 4,080 star-sectors, all numbers zero. One star of the 612 has no light-curve file (CONFIRMED: no .fits file in its folder; it is outside the search by the same rule for every campaign).
- New `--counts-only` mode for the exporter: no gallery, no lead cards, no ticker, no per-star counts. Tested on the finished G2 run: 8.3 KB, zero `tic` keys, same funnel (2,764 / 85 / 65 / 31) as the full feed. The G3 launch script starts it with `--blind --counts-only --push`, so the page fills in by itself when Ahmed gives the go.
- Bug found and fixed before it could bite: the version label said "Vesper 0.8.0" for any run with option c6, so G3 would have been labelled 0.8.0. It now reads `frozen_v81` from the run's settings and says 0.8.1.
- Wording fixed: eight safety checks, not nine; the rows are first-listed-flag counts, not independent rejections; the 12,261 and 2,764 are named as different samples; the self-test is labelled as not the search's sensitivity.
- The finished G2 sealed run is kept as published, one click away: `watch/?src=../assets/data/watch-g2-sealed.json` (a copy of the feed as it stood on 30 Oct, 165 KB; it holds the G2 pictures and star details Ahmed allowed on 30 Oct).
- The G3 launch script saves the library versions (`pip freeze`, 125 lines, T128, Ahmed's yes on 4 Nov) to `data\g3_pip_freeze.txt` before the search and into the run folder after it; the guard `g3_run.py check` still passes (hash e7886a71a61f).
- G3 itself has NOT started: `research/stage3/G3-GO.txt` does not exist.

## A. Current Search Window architecture
Data journey (CONFIRMED):
1. `S3.search` writes one JSON per star-sector group into `data/stage3_g*/<run>/groups` (cleaned-light and QLP products, flags, tiers) and `groups_sap` (raw-light twins), then `pdc_pass` adds the third pass. The run folder also holds `settings.json` (hash, provenance, data hashes), `watch_plan.json` (group counts), `starts.log`.
2. `pipeline/watch_export.py` (loop every 60 s) reads every group file, caches by modification time, and builds one aggregate JSON: progress, flag counts, tiers, box and strength histograms, self-test counts, history, notes, a gallery, the funnel from `pipeline/leads_export.py`, a ticker. Blind mode pools real and upside-down.
3. It writes `book/docs/assets/data/watch.json` (the snapshot that ships with each book build) and, with `--push`, copies the file to a scratch clone (`D:\ss-watch-data`) and pushes it to the branch `watch-data` (80 commits so far).
4. `book/docs/assets/watch.js` fetches every 90 s: GitHub API first, then raw.githubusercontent, then the shipped snapshot; `?src=URL` overrides. It draws 13 sections and the light.
5. Launch: `sealed_run.py --watch` started the exporter for the sealed run; `g3_go.ps1` now starts it for G3. No scheduler; the feed exists only while the exporter runs on Ahmed's PC.

Where each value comes from:
- CALCULATED: counts, rates, ETA (last 10 minutes), histograms, the funnel, lead rules, self-test counts.
- COPIED from a filed report: the scored line (string match on `VERDICT S1` in `benchmark-g2-sealed.txt`), run settings and hash (`settings.json`), the known-host lists (`data/xmatch/*.csv`).
- GENERATED during execution: `updated` (exporter build time, not search progress time), workers and CPU (a PowerShell query of Python processes), the history chart, `started` (earliest group-file time, not the real start in `starts.log`).
- DISPLAY ONLY: phase and stage texts in `watch.js`, including "9 box lengths" (true today: 3, 4, 5, 6.5, 8, 10, 12, 15, 20 h) and "10-minute bins" (true: 0.00694 d); "2-day smoothing" was not checked against settings; the 90-second refresh text; the notes (hand-written by Claude).

## B. Assessment of the existing interface
Works (CONFIRMED): the light never pulses unless the phase is live (glow only on a stage that matches the phase; the pulse is disabled under reduced motion); blind mode really pools (tested tonight); a plain verdict sits first; the funnel shows real beside upside-down; the page survives instant navigation (FIX 64, 71).
Weak: one long page of 13 sections with no hierarchy beyond order; the single light mixes three different states (search, feed, science); a finished run shows FINISHED with no date and no word "historical"; the same word "found" carries three numbers in two places; stage texts are hard-coded; no campaign identity beyond a label string; the scorecard is reduced to one line (S1); nothing says what the checks protect against; "Technical details" is a collapsed table of raw settings.

## C. Scientific-data audit: inconsistencies and misleading metrics
1. Check count and order (Compass section 3, items 1 and 2). 564 under "No flag fired" against 446 tier 1 plus 79 tier 3: 39 tier-2 records hidden under "clean".
2. Three samples under one word. Event records 12,261 (all products, both passes, first pass); scorecard detections 2,764 (best product per star-sector, cleaned-light half, after the union and v7 flags); stars 31 (last funnel row). Never consecutive stages.
3. "Kept: no safety check fired" (85, scorecard sample) and "No flag fired" (564, event records) share words and differ in sample.
4. The last funnel row counts upside-down "leads" (25) next to real leads (6). The 25 are control counts, not objects; the label must say "control stars" and the real/control columns must be named "real direction" and "control (flipped)".
5. First-pass tiers (12,261 records: tier 2 11,736; 1A 374; 3 79; 1B 52; 1L 20) are not the final tiers; the page title says first pass but the next section does not.
6. The self-test 96.4% is a visibility check of pasted-in dips by the second light curve at signal-to-noise 4; it is not completeness. The page never shows S4. Show both, separately (section G).
7. S2 (FAIL, 8.91 per 1,000, interval 6.80 to 11.47) and S3 (PASS, mirror test) are not on the page.
8. TOI-1338 b: scorecard S6 finds 1 of 11 expected transits in the sealed run (tier 1L in sector 37; 1 of the 7 "strong" tests); the book's status panel says "7 of 10 passes, 4 of 10 kept as strong". Different tests (UNCERTAIN which definitions); reconcile before showing both.
9. 80 commits on `watch-data` are titled "watch: counts only" although the G2 feeds carried pictures with TIC, sector and time. New pushes name their content honestly.
10. `started` and `updated` are not the run's start and last progress times.
11. The scorecard S8 says 4,796 events written; the feed counts 12,261 event records. LIKELY pass 1 only against passes 1 and 2 together (the page counts the group files and the raw-light twins); NOT verified.

## D. Proposed personal mission-control dashboard
Same URL (`/watch/`), same MkDocs page, same design tokens (Atkinson for reading, Plex Sans for labels, Plex Mono for hashes), day and night themes, no animation except the live pulse.
Top band, always visible, three separate state chips with their own source:
- SEARCH STATE: not started / running / stalled / completed / failed. From run files and a `run_state.json` written by `g3_go.ps1` (steps, exit codes, `STOP:` lines).
- FEED STATE: fresh (under 3 min) / delayed (3 to 15 min) / stale (over 15 min while the search is running) / unavailable (fetch failed, showing the shipped snapshot with its age) / archive (a finished campaign; never "stale"). Computed in the browser from `updated` and fetch errors only.
- SCIENCE STATE: blind / scorecard filed / reviewed / unblinded. From `book/data/campaigns.yml` (manual, changed only on Ahmed's word) plus the existence of the scorecard file; "reviewed" is a manually kept record and is labelled as such.
Overview row: campaign id and name, version and hash (12 characters), stars on the list and with files, star-sector groups, files read, stage completion (search pass, raw-light pass, second look, completeness, scorecard), latest result line, next campaign and its readiness (today: none planned after G3).
Below: (1) three funnel blocks (D1); (2) the safety-check panel (D2); (3) scorecard and reliability (section G); (4) personal status (D3); (5) technical details and provenance (hashes, commit, files, settings), collapsed.
D1, the funnel, as three separate blocks each with unit and denominator, never joined by arrows across blocks:
- "Event records" (unit: one dip record in one product and pass; 12,261): by first-listed flag, then by first-pass tier.
- "Scorecard sample" (unit: one event, best product per star-sector, cleaned light; 2,764): kept 85, confirmed 65, real direction beside control.
- "Stars" (unit: one star; 31): stars with a confirmed dip and no known planet, real direction 6 and control 25, with the sentence that the control stars are noise counts.
Each block has a two-line "how to read this" and the file the numbers came from.
D2, safety checks, a table: name; priority of the first-listed count (1 to 8) and a note that the pipeline tests all of them; records filed under it and its share of the sample; why it exists; what it protects against (the C-rule in Chapter 10: C5 not an eclipse, C6 not a neighbour, C7 not the spacecraft, and so on); enabled (always on in the frozen version, except the c6 orbit-locked flag, on); limits. Plus rows for the two unlisted conditions (burst; orbit-locked) and for tier 3. The text lives in `book/data/checks.yml`, one place, linked to the chapter.
D3, personal status (manual and derived, each line labelled): current campaign; latest finished task (last git commit and the last ledger row); open investigations (count from `FIX-QUEUE.md` and `BUILD-QUEUE.md`, titles only); pending decisions that need Ahmed (a short manual list kept in `research/status-notes.yml`, updated with the daily recap); known blockers; next recommended action; last successful run and last integrity check (`g3_run.py check` saved as a file); warnings (feed stale, hash mismatch, exporter not running). No line says Claude is working unless a process is. No start or stop controls.

## E. Proposed observation inspection interface
- Public tier: known public objects and injected fakes only (TOI-1338 b transits, the injection harness). One panel, tabs inside it: original light (SAP), flattened light (PDCSAP), second product, with the detected interval, gaps (dashed), signal-to-noise, duration, depth, flags, product, tier and a plain-language processing history. SVG with pointer zoom (wheel, drag, keyboard arrows) and axis labels in hours and ppm. Size LIKELY 30 to 50 KB per event; 20 events under 1 MB.
- G2 archive: exactly the 22 pictures already published, unchanged, no new fields.
- Real events (G3 and later): local only. `pipeline/look_event.py` already exists; the bench would write to `data\` and open on the PC. Ahmed reads on an iPhone, so he could not open it there: UNCERTAIN, his decision.
- G3: no inspection of any event before the preregistered analysis (`G3-PREREGISTRATION.md` line 15).

## F. Proposed campaign archive
`book/data/campaigns.yml` is the registry (source of truth, newest first): id (g1-first, g2-dev, g2-sealed, g3), target-list file and sha256, version and settings hash, code commit, start and end, counts of targets and star-sector groups, search products, scorecard file with sha256, outcome, limitations. A read-only `pipeline/campaign_export.py` (new file; it reads the filed result files, never a pipeline output being written) builds one small `campaigns/<id>.json` per campaign (about 10 to 30 KB: counts, funnel blocks, scorecard rows, reliability rows) with the sha256 of each source, so a test can recompute it. No event data is copied. The live feed carries only the active campaign. The page selects with `?c=g2-sealed`, default the newest, works offline (the summaries ship with the book). G2 keeps its current full feed as the `?src` copy.

## G. Scientific scorecard and reliability layout
Scorecard table, one row per filed entry (CONFIRMED, `benchmark-g2-sealed.txt`): metric; value; preregistered mark (only where one exists); interval; result as filed; one sentence; file link.
- S1 excess of real tier-1 dips over noise: real 26, upside-down 59, noise-expected real 41.8, chance of at least the observed 0.997 at bar 7 (rule: 0.01 or less at bar 7 and real above expected at bars 8, 10, 12). Filed: NO EXCESS. Sentence: real dips are fewer than the control produces, so there is no excess. SAP-only half (real 12, upside-down 1) is shown on its own line as not evidence.
- S2 false alarms: 60 in 6,734 star-sectors = 8.91 per 1,000, 95% interval 6.80 to 11.47, mark 8 or fewer. Filed: FAIL (v8 did not generalise). Sentence: the filed rule compared the point estimate with the mark; the interval includes the mark. Neither a clean fail nor a pass; the filed word stays.
- S3 mirror test: dips 37.5%, bumps 37.3%, gap +0.1 points, mark within 3. Filed: PASS.
- S4 completeness (planted dips, tier-1 recovery, K 8 to 14 pooled, n 1,184 per box, Wilson 95%): 4 h 41.0% (38.2 to 43.8); 8 h 46.8% (44.0 to 49.6); 14 h 34.1% (31.5 to 36.9); 20 h 28.0% (25.5 to 30.6), "DID NOT GENERALISE" (development slice 21.3%). By depth: 8 h box 27% at 8x, 46% at 10x, 56% at 12x, 58% at 14x. No mark.
- S5 orbit-locked flag: 13 events moved to tier 2 (13 real, 0 upside-down) on 4 stars; cost on planted dips 0.51%. No mark.
- S6 TOI-1338 b: 1 of 11 expected transits found (tier 1L, sector 37); the other ten missed or lost in an eclipse or gap. No mark.
- S7 label split: pointer file. S8 machine health: 6,877 star-sectors read, 24,639 files ok, 4,796 events written (statuses listed).
Reliability layer, two separate blocks that are never merged: A. PIPELINE SELF-TEST (second-product visibility of pasted-in dips: 34,965 of 36,278 = 96.4%; a check that the machine still works). B. END-TO-END SEARCH SENSITIVITY (S4, through the whole chain), by box length with n and the Wilson interval, by depth where the source has it, and by brightness only if a source file exists (none seen tonight: NOT TESTED). Limits stated beside B: trapezoid fakes; planet size not measured; the harness cannot see other sectors, so the orbit-locked flag is costed offline; the second-product check and the SAP twin are in the chain; the 20 h line did not generalise; these are Vesper 0.8.0 numbers on G2, and G3 completeness will be a new measurement on 300 random G3 star-sectors.
Why the overall result was NO EXCESS: because the control (59) outnumbers the real (26) at the preregistered bar, not because every other entry passed; the dashboard says that sentence once, under S1.

## H. Data privacy and publication scope (CONFIRMED unless marked)
The site is public hosting: the page fetches `watch.json` from GitHub without credentials, and the book's `noindex` tag asks search engines to skip it but is not access control (the comment in `overrides/main.html` says so).
What is published today for G2 sealed (live feed and snapshot, identical in content): 6 lead cards each with TIC, sector, event time (BTJD), duration, depth, signal-to-noise and a 36 h binned light curve; 16 gallery pictures each with TIC, sector, UTC time and light curve; a 12-row ticker of TIC, sector and event counts; the funnel and aggregates. Ahmed allowed star details on 30 Oct ("the book may show star details while nothing is serious", `LEADS-RULES.md`). The data branch keeps 80 earlier versions.
Findings: (1) the scorecard is NO EXCESS, so these 6 are noise-like leads, but they are named stars with times in a public repository; (2) removing them from the live view does not remove the history on `watch-data` (the recipe is in `LEADS-RULES.md`: delete and recreate the branch); (3) G3 is counts only by construction (tested); (4) no G3 event detail may be published before the preregistered analysis, and after it only on his yes per set; (5) personal status lines must come from a curated file, not from raw `decisions.md` or RESUME text; (6) password gating on a static site is client-side and weak (UNCERTAIN; not recommended without his decision).
Decision for Ahmed: keep the G2 star details public as authorised on 30 Oct, or have me strip them from the current files (history stays unless the branch is recreated).

## I. Exact repository files that would change (stages 1 to 5; inspection later)
New: `book/data/campaigns.yml`, `book/data/checks.yml`, `research/status-notes.yml`, `pipeline/campaign_export.py`, `pipeline/test_watch_numbers.py`, `book/docs/assets/data/campaigns/*.json`, `book/docs/assets/watch2.js` and `watch2.css` (or a split of `watch.js`), `book/tools/test_watch_page.mjs`.
Changed: `book/docs/watch.md`, `book/docs/assets/watch.js`, `pipeline/watch_export.py` (schema 2, `run_state`, status block), `pipeline/leads_export.py` (three populations, control labels), `pipeline/g3_go.ps1` (write `run_state.json` and the check result), `book/mkdocs.yml` (assets, footer), `book/docs/versions.md`, `book/hooks.py` (validate `campaigns.yml` and `checks.yml`; precache the summaries), `book/tools/page_sweep.js`.
Not touched: the 11 fingerprinted pipeline files, any scorecard or filed result, `book/progress/mission.yml`.

## J. Recommended implementation sequence (after the G3 result is read)
Stage 1: data layer (registry, scorecard parser, run state, schema 2, privacy test). Stage 2: top band with three states, three funnel blocks, safety-check panel. Stage 3: scorecard and reliability. Stage 4: campaign archive selector (G1, G2 dev, G2 sealed, G3). Stage 5: personal status. Stage 6: inspection (public known objects first; a local bench only on his word). Each stage ends with its tests, a book publish and a field note.

## K. Acceptance tests
1. Every number on the page equals the value in its source file (a script reads both; fails on any mismatch).
2. Three funnel blocks never share a total or an arrow; each shows unit and denominator.
3. State matrix with fixtures: 5 search states x 5 feed states x 4 science states render the right chips; no pulse, glow or "RUNNING" unless search state is running (assertion).
4. Privacy: the published JSON of a counts-only campaign has no `tic`, `center`, `x`, `y`, ticker or gallery key (done tonight for G2 counts-only: 0 keys, 8.3 KB); the archive summaries pass the same test.
5. Archive summaries recompute from their source files and sha256 values; a campaign switch changes every number.
6. Offline: the shipped snapshot and summaries open with the network off (NOT TESTED on iOS).
7. Keyboard walk, visible focus, 44 px targets, reduced motion, 375 and 1440 px, day and night; no horizontal overflow (375 px checked tonight for the ready page).
8. The existing page sweep and the publish gate pass.
9. After a G3 run: the scorecard rows on the page equal `benchmark_g3.py` output.
10. Ahmed's acceptance on his iPhone icon app (standalone Back works; see the Learning Space note).

## L. Estimated Claude usage (LIKELY, from the ledger; UNCERTAIN where marked)
Calibration: the 30 Oct Search window steps are logged at about 1 point each for the page and for the pictures (bundled rows; the leads step was not looked up); the ready change tonight about 1.
Stage 1: 2.5 to 4. Stage 2: 3 to 4.5. Stage 3: 2 to 3. Stage 4: 1 to 1.5. Stage 5: 1.5 to 2.5. Stages 1 to 5: about 10 to 15.5. Stage 6: public known objects 3 to 5; local bench 2 to 3 (UNCERTAIN). Whole vision about 15 to 24.

## M. What I disagree with in the prompt, with evidence
See the Compass review, section 6: no evaluation order exists; "enabled" is a switch only for c6; "last integrity check" needs a saved file; "Petrova" waits for the rename go; the FAIL word is shown as filed; inspection of real events is not authorised for G3 and not safe to publish beyond what is already out. One more: "Do not modify the scientific pipeline" is respected, but the exporter and `g3_go.ps1` live in `pipeline/` and a dirty tree there blocks a G3 start (`provenance()`), so every change to them must be committed before the go.
