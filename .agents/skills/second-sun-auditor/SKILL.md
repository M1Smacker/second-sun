---
name: second-sun-auditor
description: Use in the Second Sun project (D:\second-sun, TESS circumbinary planet search, filter Vesper/Petrova) whenever you audit or review code, hunt for bugs, fix a bug, write or run a test, check or re-derive a number, plan or size a task, do research, or report a result. Checklists, stop signs and worked examples left by the Fable audit of 10 Nov 2026.
---

> **Reading this as Codex (added by `research/astra/tools/sync_kit.py`; the original is Claude's skill).**
> This skill was written for Claude Code and is copied here unchanged below this box. Read it with these swaps:
> "the usage meter" / `get_usage` / "weekly points" means your own Codex usage panel (five-hour and weekly bars);
> log your rows in `research/astra/USAGE.md`, never in `research/usage-ledger.md` (that one is Claude's).
> "Opus", "Fable", "Sonnet" and "helpers" mean other models: you do not start helper agents unless the brief says so.
> "Flag for Opus or Fable" or "ask Ahmed" at a stop sign means: stop, write it under STOP SIGNS in your report, do not continue that line.
> Every rule marked [core] binds you exactly as it binds Claude. You never edit the frozen files, never push, never publish.

# Second Sun auditor (lessons from the Fable audit, 10 Nov 2026)

Private. One set of rules for every model. Rules marked **[core]** are never weakened or removed without Ahmed's yes. Worked examples: `examples.md` beside this file. Full audit: `D:\second-sun\research\fable-audit-2026-11\REPORT.md`.

## 0. The one idea
**Nothing here is true until a script that could have contradicted it has run on our own data.** Every serious error in this project was a statement, a review or a test that could not fail. Reading finds little; a 40-line script finds a lot. Before you read more than about 20 KB, ask: "which script will this reading let me write?" If none, stop reading.

## 1. How to scan for bugs here
Walk the path a real planet's light takes, from the FITS file to the tier, and at every step ask "what does this step do to a real dip, and has anyone measured that with the dip present BEFORE this step?"

Where bugs hide, and what to check:
- **Steps before the search (masks, windows, detrending).** [core] Inject into the RAW loaded flux, before `eclipse_mask_auto`, before windows, before detrending. Until 10 Nov 2026 every recovery test injected after the mask and missed that the mask deletes dips in slow binaries (example 1).
- **Arm symmetry.** [core] The upside-down arm is only a fair control if every step treats `f` and `2 - f` the same. Any step that looks for LOW flux (eclipse mask, depth guard, flare shape, flags fed by the other arm) breaks it. Test: on pure noise and on real light, real and upside-down event counts must agree within counting error in every period, brightness and product bin. Bin the ratio; a pooled ratio hides it.
- **Quality masks and flag bits.** Never trust a mask name ("hard"). Count, on real files of each era and product, how many KEPT cadences have a non-zero QUALITY, and which bits. QLP changes at Sector 56 and again at Sector 94 (bit 29 appears, meaning not yet known).
- **Products and eras.** One test file per path: SPOC 2-min, 20-s, TESS-SPOC FFI, QLP before 56, 56 to 93, 94 on; 30-min, 10-min, 200-s cadence. A path with no test is broken until shown otherwise (the 30-min path once returned nothing, silently).
- **Time systems.** BTJD = BJD minus 2457000. Villanova `bjd0` is BJD minus 2400000 (so minus 57000 to get BTJD). Kepler BKJD = BJD minus 2454833. Gaia reference time is BJD(TCB) minus 2455197.5. Check one known eclipse by eye-number after any conversion.
- **Units.** Phase against days; hours against days (`dur_h / 24`, `dur_h / 48` for a half width); ppm against fraction; Earth against solar radii (109.08).
- **Period-dependent behaviour.** Anything that folds at the binary period behaves differently when the period is longer than half a sector (one visit per phase). Always test at 5, 10, 14, 20, 30 and 50 d.
- **Silent skips.** `return None`, `continue`, `except Exception: continue`, "skip" then "pass". Count how many items took the skip path and print it.
- **Sentinels and selection.** -1, NaN, empty string passing a `<` test; `drop_duplicates` choosing a row; a regex reading `s2019` as a sector.
- **Counts that share a name.** 4,080 (G3 groups searched) and 3,425 (G3 star-sectors scored) are both "G3 star-sectors". Say which.
- **Hard paths, wrong venv.** `D:\second-sun\.venv\Scripts\python.exe` has lightkurve; plain `python` does not. A check that never ran looks like a pass.
- **Blind and fences, not privacy.** Star ids and star data may be published (Ahmed, 14 Nov 2026). Before a push, still check the payload does not unblind a sealed run, touch fence A or B stars, or show a named lead before two keys. A commit message is not evidence.

## 2. How to fix without making new bugs
1. Write the failing test first and watch it fail on the unfixed code.
2. Smallest change that makes it pass. One fix per commit.
3. **[core] The frozen filter is never edited.** A change to anything in the hashed file list is a new version (see `research/stage3/VESPER-VERSIONS.md`), with its own freeze, and never re-scores a sealed run.
4. After the fix run: the new test, the old tests, and a zero-injection identity check (same events as before on untouched star-sectors) so you know what else moved.
5. **[core] Unverified is not fixed.** "Done" means you ran it and pasted the output. Three of twelve untested fixes here had failed.
6. Show the test can fail: break the code on purpose once (a mutation) and see the test go red.

## 3. How to check numbers
- **[core] Re-derive by a different method, in a new script, without importing ours.** Grid sum against Monte Carlo; formula against simulation; count from raw files against count from a table.
- Write the expected size before you compute (order of magnitude, units). A surprise is a finding.
- Ask what the number does NOT include. The Census odds were arithmetically right and still wrong in meaning, twice: once for counting spent hunts as future chance, once for using recovery tables measured after the mask.
- Forecasts count only what is still to come.
- Never scale a small sky sample to the whole sky (27% to 40% too high here). Count exactly or label UNCERTAIN.
- Intervals: star-sectors of one star are correlated; a binomial interval is too narrow. A rate inside its interval of the mark is "borderline", not "fail" or "pass".
- One star is not a rate (n = 1).

## 4. How to research and plan
- Follow `research/RESEARCH-BLUEPRINT.md`: a question tied to a decision; our own data first; then the primary source; pull the exact sentence; label; turn it into a plan change.
- Size the stint by tool calls, not minutes: about 0.02 weekly points per call under 300K context, 0.05 or more above 600K. Write the cap before starting. Stop at the cap.
- A search summary is a lead, not a source. Open the page. Dates of releases and launches go stale: re-check them (Gaia DR4: 2 December 2026, ESA release page, read 10 Nov 2026).
- Planning order: what decision does this serve; cheapest check that could kill it; then build.
- Helpers: never an expensive model for reading. One at a time. A tight question, a call cap, a one-page answer.

## 5. Using the usage meter
- Read the meter before and after every task and write the row, even if nothing else is logged.
- Predict first. Typical ratios here: plans and notes cost 0.3 to 0.6 of the guess; pipeline code plus runs 0.9 to 1.3; research overruns unless capped by calls.
- Machine time is free; polling is not. Run long jobs in the background and do not watch them.
- Keep context small: write STATE to a file, start a fresh session for a new task.
- Batch: one script that prints ten counts beats ten commands.

## 6. Mistakes Claude keeps making here (blunt)
| Mistake | The rule that stops it |
|---|---|
| Quoting a number from a formula or an assumption as if measured | Run the injection or the count. Label it otherwise. |
| A test that cannot fail, or tests a path the planet never takes | Mutation check; inject before every step. |
| Calling a fix done without running it | Paste the output or say "not run". |
| Reading for hours, then guessing | Script first (section 0). |
| Fix guesses after fixes fail, cause unknown (dominated, 14 Nov 2026: three blind fixes, Ahmed had to order research) | Two failed fixes or cause UNCERTAIN on a decision item: open a research stint on the root cause myself, before any more fixes. |
| Budget overruns on research | Cap by tool calls, written first. |
| Guessing the clock | `Get-Date`. `resetsAt` is UTC; Kuwait is UTC+3. |
| Expensive helpers for cheap reading (cost 10 points on 10 Nov 2026) | Cheapest model that can do it; one at a time. |
| Treating "equal to the last version" as "correct" | Zero-difference proofs carry old bugs forward. |
| Pooled statistics hiding a split | Always bin by binary period, brightness, product, era. |
| Old numbers left standing in RESUME after a correction | Mark the old line "superseded by" in the same commit. |
| Commit messages or labels that describe the intent, not the content | Check the payload. |
| Writing a "LIKELY" mechanism into the queue before testing it (14 Nov 2026: "dominated holds bumps because of eclipse leftovers" was refuted by a 12-minute run, `research/stage3/006-check/p_competitor.py`) | Run the cheap test first, or file it as "idea, untested". |

## 7. Stop signs (Petrova and statistics only) [core]
Stop, label UNCERTAIN, and ask Ahmed or flag for Opus or Fable when:
- a change would touch any file in the frozen hash list, or alter what a sealed or one-shot run reads;
- you are about to choose a threshold, window or mark after seeing the events it will judge;
- real and upside-down counts differ and you want to explain it with a story instead of a binned test;
- a decision number changes by more than about 10% under your re-derivation, in either direction;
- a "possible planet" appears: it is a private lead under the two-key rule; write it only under `data\`, claim nothing;
- you would re-interpret a preregistered verdict (S1, S2, the FFI door). The verdict stands as filed; a new design gets a new preregistration.

## 8. Merged rules (source in brackets; the originals are unchanged)
- Verify before concluding; label CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED; never invent a check [CLAUDE.md].
- Cheapest check first: our data and code, then the web, then nothing [CLAUDE.md].
- Never click the live Eyes page; real events stay under `data\`; no star ids, event times or lead details in the repo or the book [CLAUDE.md, memory].
- Second Sun downloads need no yes, but every download is told and logged in `research/downloads.csv`, into a new empty folder under `data\` [CLAUDE.md].
- No en or em dashes; phone-first, short; end finished work with "Next:" [CLAUDE.md].
- Read the clock, never guess times [memory read-the-clock].
- Unverified is not fixed [memory].
- A clean measured null is a win; settings frozen per version, never tuned on results [memory, CLAUDE.md].
- "Your take" means a plain honest opinion [my-take skill].
- An outside re-derivation for every number that reaches Ahmed as a decision [8 Nov proposal; Fable recommends yes].

## 9. Upkeep
Any model may ADD a lesson when a new mistake is caught: one line in section 6 or a short example in `examples.md`, dated, with the file that shows it. Do not delete or soften a [core] rule without Ahmed's yes.

- (10 Nov 2026, Fable audit ledger) Never resume a large session after a long pause: re-reading a 400K context uncached cost about 4 weekly points before any work. Save state to a file, start a fresh session, read the state file.
