# 032 eclipse times v3, partial handoff

Codex, runtime model and effort independently unverified; brief specifies neither. Written 23 Nov 2026, 11:01 am Kuwait, from Get-Date.

**Plain verdict: PARTIAL.** The new control sample and verification are ready. Part A is running detached; there is no v3 scientific verdict yet. Part B has not started.

**Branch:** astra/032-eclipse-times-v3, unchanged. No Git write commands, commits, pushes or frozen-file edits. The existing .codex_run.lock was left alone. Tree node 1.4, FIX 94; relevance to Census node 2.1 is conditional on validation.

## Findings and completed work

1. **CONFIRMED, sample fixed before fitting.** The unchanged 014 eligibility rule gives 165 eligible design-seen G2 controls. Excluding the 100 spent seed-12 and seed-14 controls leaves 65. Seed 2026112316 selected 60 using 014's stratified allocation. Counts by its five period bins are **41, 9, 10, 0, 0** (below 10, 10 to below 14, 14 to below 20, 20 to below 27.4, and at least 27.4 days). No affected stars enter this sample. Evidence: `032_select.py`, private `fresh-controls.json`, and design-membership assertions in `032_verify.py`. The two longest-period bins have no fresh controls, which limits the eventual result.

2. **CONFIRMED, implementation prepared and synthetic checks run.** Recovered 014 code using read-only `git show` on its unmerged branch, then copied it under `research/astra/scripts/032_*`. The measurement and alias functions are unchanged. `032_error_model.py` adds the specified quadrature scatter and one capped robust clipping pass, computes the inflated-error covariance, and replaces the old formal-sigma flags with the stated sector and width requirements. `032_methods.md` records numerical conventions before fitting. Frozen 014 product-family scales are reused; no fresh-control calibration is performed.

   Extra scatter means allowing more timing uncertainty when individual eclipses disagree with a straight-line prediction. Making reduced chi-square equal to one does not establish correct eclipse timing. The separate catalogue agreement gate must still pass.

3. **CONFIRMED, nine verification groups passed.** `032_test.py` checked independent slope, epoch and covariance arithmetic; an independent scatter grid; zero-extra-scatter behavior; the one-pass 10% clipping cap; sector, width and count guards; every-sector agreement and its boundary; the gate boundaries and empty denominators; rejection of an omitted-scatter mutation; and AST identity of 014 timing, alias, trap and selection functions. This is synthetic runtime and source-comparison evidence, not a real-light result or independent review. Output: private `tests.json`.

4. **CONFIRMED, static and access checks.** `032_verify.py` parsed 26 Python files, verified 12 copied-module hashes, rejected four simulated out-of-scope access events, and checked all 60 selected stars against the design-seen list. The forbidden files were not opened. Source hashes are recorded after launch, not claimed as a prelaunch lock; worker and timing code have not changed since launch. Hash equality proves source identity only. `git diff --check` reported no whitespace errors in the tracked diff; the new untracked files were covered by Python parsing, not that Git check.

## Running work and continuation

- Supervisor launched at **10:58:07 am Kuwait**, process 6776. Two measurement workers, each with NUMBA_NUM_THREADS=2 and one BLAS/OpenMP thread. Six Python processes existed before launch; the unrelated 031 run and outputs were not accessed or changed.
- Precreated shared directories and per-star atomic checkpoints live only under `data/astra/032/`. All other data outputs also stay there. Source and notes stay under `research/astra/`.
- `data/astra/032/progress.json` was still `running`, phase `measure`, when the single 55-second terminal wait ended. No worker logs were read while healthy. No process was stopped.
- **Expected finish: 12:28 pm Kuwait, 23 Nov 2026.** This is a conservative 90-minute planning allowance, not a measured runtime or promise. It is also saved in progress.json.
- After measurement, the supervisor runs `032_summary.py`. This reruns the exact 014 30-case trap with its original design-noise library and seed, applies v3, and saves private `ephemerides-v3.csv`, `eclipse-times-v3.csv`, `sector-offsets-v3.csv` and `summary.json`.
- Before the supervisor marks completion, the summary runs `032_recount.py`. This independently recomputes weighted fits, covariance, reduced chi-square, width scatter, every-sector agreement and gate counts from saved measurements, without importing the v3 fitter. Its output is `recount.json`. This remains producer verification, not Claude's independent review. The recount is prepared and syntax-checked but **NOT YET RUN on real outputs** at this handoff.
- The supervisor does not launch Part B. If any A gate fails, stop with that fixed verdict, as briefed. If all pass, Part B implementation and benches remain required. No v3 threshold has been changed after results.

Resume Part A only after a terminal failure or interrupted process has been established, using:

```powershell
& D:/second-sun/.venv/Scripts/python.exe -I -B research/astra/scripts/032_run.py
```

Do not start a second supervisor alongside the current one. Completed per-star measurements are reused. `032_prepare.py` is the source-recovery utility, not the continuation command.

## What I did NOT check

No completed fresh-control A1, A2, A3 or period-error calibration results are available at this handoff. No real-data recount has run yet. No development-sample v3 results, affected-star v3 fits, Part B mask, fresh planet bench, T156 draw, untouched backgrounds, T109 recovery, identity replays or deep-event removal counts were computed. No independent reviewer has reviewed these changes. No fenced light, production filter or outside service was used.

## STOP SIGNS hit

No scientific stop sign established yet. The running task is handed back under AGENTS section 7's detached-job/no-polling rule after one bounded terminal wait. Part B stays gated on Part A. A failed judging gate is a required stop, not authorization to tune.

## QUEUE PROPOSALS

None yet. Keep node 1.4 / FIX 94 unresolved until the fixed control gates and, if permitted, the mask benches finish. Claude files the eventual result.

## IDEAS

None added outside the brief.

## Disagreements with Claude

None. Missing long-period controls are a measured sample limitation, not a changed pass rule.

## Questions for Ahmed

None. The next dependent work is already authorized by the brief if Part A passes.

## Usage

Predicted before implementation: 45 five-hour points / 8 weekly points. First observed after initial reads: 3% five-hour / 18% weekly. Pre-handoff observation: 26% / 22%, approximately +23 / +4 rounded account-wide points, weekly actual/predicted about 0.5 so far. Initial reads and later close-out usage are not fully included. Lesson: exclude spent controls before promising bin coverage, and distinguish prepared recounts from executed evidence.

**Next:** Claude or the runner checks the terminal Part A summary and recount after completion, to establish the gate verdict before any Part B work; this is a small review with no heavy rerun needed, usage not yet measured.
