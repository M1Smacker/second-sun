# Compass review: "Search Window 2.0, personal astronomical mission control" prompt (4 Nov 2026, early morning)

Review only. The prompt came from ChatGPT via Ahmed (pasted in chat). Checked against the real files, the published feed and the G2 scorecard. Labels: CONFIRMED (read in a file, counted by script or seen in the published feed), LIKELY, UNCERTAIN, NOT TESTED. Full answer: `research/stage3/SEARCH-WINDOW-2-PROPOSAL-2026-11-04.md`.

## 1. Verdict: REVISE (approve the vision; change seven points before any build)

## 2. What is correct
- The data journey is as described: search group files (`groups/`, `groups_sap/`) to `pipeline/watch_export.py` to `book/docs/assets/data/watch.json` and, with `--push`, to the data branch `watch-data`, to `watch.js` (GitHub API, then raw, then the shipped snapshot). CONFIRMED.
- The 12,261 and 2,764 are different populations. CONFIRMED in the published feed: `events.found` 12,261 (every event record, every product, both passes, first-pass) against funnel stage 1 2,764 (scorecard sample: best product per star-sector, cleaned-light half). A third unit, stars, sits in the last funnel row (31 = 6 real + 25 upside-down).
- The page lists eight named flags plus "No flag fired", and calls them "nine safety checks". CONFIRMED (`FLAGS` in `watch_export.py` has 8 entries; `watch.js` and `watch.md` said nine).
- 96.4% is the second-product visibility of pasted-in fakes: 34,965 of 36,278 = 96.38% (published feed, `selftest`). End-to-end recovery is a separate measure: scorecard S4, 41.0 / 46.8 / 34.1 / 28.0% for 4 / 8 / 14 / 20 h boxes, 1,184 injections each, K 8 to 14 pooled; the 20 h line is marked DID NOT GENERALISE (development slice 21.3%). CONFIRMED.
- False alarms: 60 upside-down tier-1 in 6,734 star-sectors = 8.91 per 1,000 (95% interval 6.80 to 11.47), mark 8 or fewer, filed as FAIL (S2). CONFIRMED.
- The G2 scorecard has eight entries, S1 to S8. Only S1, S2 and S3 carry a preregistered mark; S4 to S8 are reported without one. CONFIRMED (`research/stage3/benchmark-g2-sealed.txt`).

## 3. What needs changing, and why it matters
1. **There is no "evaluation order" of safety checks to show.** `tier_of()` in `pipeline/stage3_core.py` (line 254) is an OR of independent flags: every flag is computed for every event, and none stops the others. The "first stop" on the page is the exporter's own listing order, used to file each event under one row. The old page sentence "a dip stopped by the first one never reaches the next" was false as a statement about the machine (corrected in this change). CONFIRMED.
2. **The check list is incomplete and "nine" was wrong.** Tier 2 can also come from the burst check (first pass) and the orbit-locked check (c6, final report); the page lists neither. Arithmetic from the published feed: 564 records are filed under "No flag fired", but only 446 are tier 1 and 79 are tier 3, leaving 39 tier-2 records with none of the 8 listed flags. CONFIRMED arithmetic; the cause (burst, and the orbit-locked step) is LIKELY. Two more conditions in `tier_of` (too deep, flare) belong to the dormant 0.9 switches and are off under c6 (LIKELY, from `g3_run.py` header). The prompt's instruction "reconcile the exact number" therefore gives: 8 listed + burst + orbit-locked = 10 active conditions, plus tier 3 for a disagreeing second light curve. Do not invent a ninth check.
3. **"Failed" and "reviewed" cannot be read from any file today.** No status file exists; a crash leaves the last JSON in place. "Failed" needs a `run_state` written by `g3_go.ps1` (it logs `STOP:` lines in `data\g3_steps_log.txt`); "reviewed" has no source and must be a manually kept record. CONFIRMED absence.
4. **A static site cannot say whether a process "is actually running".** It can say "as of its last update, N workers". The page already does this and turns red when the numbers stop (CONFIRMED in `light()`), but a finished campaign shows FINISHED forever with no date. Add an unmistakable historical state with its dates.
5. **Observation inspection (original, detrended and second-product curves, per event) cannot be published for real events.** The current gallery draws one binned PDCSAP curve (10-minute bins, 36 h) and already exposes TIC, sector and time for G2. More fields means more public event metadata (section H). Recommend known public objects and injected fakes for the public version, and a local-only bench for real events.
6. **Campaign history without copying data is feasible, but the scorecards are text.** `benchmark-g2-sealed.txt` is parsed today by one string match. A read-only parser (new file, no pipeline change) with the source file's sha256 keeps the archive traceable.
7. **Too many projects in one prompt.** Dashboard, funnel, safety panel, scorecard, archive, personal status and an inspection tool with zoom. Stage it; the order is in the proposal.

## 4. Duplicates (reuse, do not rebuild)
The light logic and stale timer, blind mode, lead rules (`LEADS-RULES.md`), `leads_export.py`, the verdict sentences, the notes feature (`--note`), the `?src=` override in `watch.js`, `look_event.py` (a single-event viewer already in `pipeline/`), the page sweep test, the design tokens.

## 5. Risks
Scientific: showing two samples as one funnel; showing S2 as a bare pass or fail; mixing the 96.4% with end-to-end recovery; showing G3 events before the preregistered analysis. Practical: JSON size if per-event curves grow; the one-minute exporter loop and GitHub's 60 requests an hour per address (FIX 66); the page has no way to detect an exporter that died while a search runs except by the stale timer. Privacy: section H of the proposal. Usage: about 13 to 22 points for stages 1 to 5 (UNCERTAIN).

## 6. Disagreements with the prompt (with evidence)
- "Evaluation order" and "currently enabled" per check: only the c6 orbit-locked flag is a switch (`VESPER_OPTS`); the other flags have no on/off in 0.8.x. Show "always on (frozen)" and the c6 flag as "on".
- "Last integrity check": `g3_run.py check` prints to the terminal only. It must be saved to a file before the page can show it.
- "Petrova version": the rename is not approved yet (Option A waits for Ahmed's go); the page uses the display name chosen then.
- "The false-alarm result should not be simplified into failure or success": agreed, with one limit. The filed word is FAIL by a preregistered point-estimate mark; the page shows that word as filed, with the interval beside it (the interval includes the mark), and never rewrites the filed verdict.
- "Observation inspection where data is available and authorized": for G3 nothing is authorized (the preregistration, line 15: "no looking at any event or picture").

## 7. The single best next step
After the G3 result is read: build stage 1 of the proposal (campaign registry, scorecard parser, run state, schema 2) because the G3 scorecard needs a home, then stages 2 to 4 in order. Stage 0 (the G3 page ready, counts only) was done tonight at Ahmed's request.
