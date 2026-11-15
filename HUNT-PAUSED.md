# The hunt is paused (15 Nov 2026, 3:33 am Kuwait)

Ahmed paused the star hunt and the Petrova filter fixes so he can learn first (decisions: `research/stage3/REDESIGN-DECISIONS-2026-11-15.md`). Book 3.0 (the Tree and the learning app) is built instead. **The hunt resumes at a learning milestone:** when Ahmed has finished the units that explain the filter and the hunt, and he says so. This file is everything needed to pick it up again exactly where it stopped. Nothing here is lost by waiting: TESS data does not expire.

## Where the hunt stands, in plain words
- **The search tool** is Petrova 1.0 (frozen code, the Vesper chain plus the eclipse mask `pipeline/petrova_mask.py`). It ran Re-search 1 on 11 Nov 2026: no planets, which is a valid result.
- **Next big search:** G1 (Kepler eclipsing binaries that TESS also watched). It has not started. It waits for Petrova 1.1 (a set of fixes) to be chosen, frozen and tested, and for Ahmed's G1 preregistration decisions.
- **Nothing is running.** No search, no bench, no Codex job. No watcher.

## Petrova 1.1: the fix list as it stands
Measured on the bench (T156: how many planted planets are caught; the upside-down arm counts false alarms). Baseline "B" = what is adopted so far.

| Item (plain name, id) | State | Numbers |
|---|---|---|
| Repeater rule b, FIX 91 (opposite-sign flag on both arms), OAE (fair one-arm rule) | ADOPTED, not frozen | part of B |
| Known spacecraft events flag (FIX 95) | ADOPTED (Ahmed, 14 Nov) | B = P 48.11%, background 174 real / 79 upside-down |
| Dump-shape rule DS | HELD for Fable | frees 30 real vs 4 upside-down events, LIKELY dump artefacts |
| Depth cap, events deeper than any planet (FIX 96) | READY for Fable | loses 0 of 264 planted dips; background 174/79 to 124/53; radius check PASS |
| Eclipse mask timing (FIX 94) | NEEDS DESIGN (Fable) | own eclipse times v2 failed controls: error model about 2x too tight (RS-034) |
| 3-hour box (T35) | DECIDED: keep | holding it would cost 40 planets |
| Broken-light guards nd, dg (T31, T32) | priced: no change | safe, no gain |
| Wobble guard (RS-032), pointing record (RS-033, T164) | NOT USEFUL / not worth it | |
| Second-product noise check (FIX 92) | FAILED its bench | |
| Dominated rule (FIX 93) | OPEN, price unknown | |

Files: `research/stage3/FIX-QUEUE.md` (node 1.x), `research/TREE.md`, the research write-ups under `research/stage3/rs024` to `rs034` and `fix96/`.

## The Fable round (planned Mon 16 Nov, before the 17 Nov 1:00 am reset)
Brief ready: `research/fable-method/FABLE-BRIEF-2026-11-16.md` (task 1: the eclipse mask timing design, FIX 94; task 2: what goes into Petrova 1.1; task 3: the shortest safe path to a G1 go, including the new G1 runner T165 and the FIX 70 file-list risk). **Ahmed decides whether it still runs Monday or waits for the restart.**

## Codex
- **Queued:** addendum 014a (`research/astra/inbox/014a-reconcile-15.md`): reconcile 15 G2 real events near momentum dumps where Claude's count and Codex's differ. Not started.
- **Unmerged branches** (all fence-checked clean, reports read): astra/010 to astra/014. Nothing merges without a reason; their results are recorded in the files above.
- **How Codex runs now:** `research/astra/tools/codex_run.py` (headless, new chat each job, watchdog, limit wait). The app chat is not needed.

## Decisions waiting for Ahmed (from `research/stage3/G1-PREREGISTRATION.md`)
1. Is G1 blind? (default yes)
2. Carry Re-search 1's stratified excess rule, or another?
3. Reference counts: design stars under Petrova 1.1, hashed before the run? (default yes)
4. Which known limits must be fixed before G1 rather than stated? (default: only FIX 94 if its design validates in time)
Also: the T130 number-audit wording flag (10 Nov field note, line 19); FIX 83 step 2 (tests on GitHub) needs his go.

## How to resume, step by step
1. Ahmed says the learning milestone is reached and gives the go.
2. Run the Fable round (if not run yet) with the brief above; Claude merges its verdicts into the Tree and the fix queue.
3. Codex 014a, then any Codex job Fable asks for (through `codex_run.py`).
4. Build the chosen fixes as Petrova 1.1; run the bench (T156) and the paired controls; freeze; record the hash.
5. Ahmed answers the four G1 decisions; Claude finishes `G1-PREREGISTRATION.md`; Ahmed locks it.
6. Build the G1 runner (BUILD T165: settings from the run file, run record, manifest hash pinned, exporter label quoted and checked); dev gates on design stars.
7. Prepare the Search window page (`research/SEARCH-WINDOW-BLUEPRINT.md`), ask for the go, run G1 once.
Start state for a fresh session: read this file, then `RESUME.md`, then `research/TREE.md`.
