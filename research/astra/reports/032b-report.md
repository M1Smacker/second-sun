# 032b held-out-sector judge, partial handoff

Codex, runtime model and effort independently unverified; brief specifies neither. Written 23 Nov 2026, 11:37 am Kuwait, from Get-Date.

**Plain verdict: found a failure.** The affected G2 set fails H1: **70 of 90 eligible primary tracks are usable, 77.8%, below the required 80% (72 tracks)**. H2 passes, 67 of 70 predict the held-out sector, 95.7%. H3 passes, 30/30. **Part B must not run.** G3 measurement is running detached, so the requested Part A reporting is not yet complete.

**Branch:** `astra/032b-v3-holdout`, unchanged. No Git write commands, commits, pushes, branch switches or frozen-file edits. The pre-existing `.codex_run.lock` was left alone. Code and notes are under `research/astra/`; every data write is under `data/astra/032b/`. Tree node **1.4, FIX 94**, with conditional relevance to Census node 2.1.

## Findings

1. **CONFIRMED: sample fixed before fitting.** `032b_select.py` selected the following counts using catalogue/design metadata. G3 has 269 eligible design-seen stars with at least three stored sector groups; the unchanged stratified allocator selected 60 with seed 2026112318. No star is replaced after measurement failure. The 53 seen controls are exactly 032's usable primary tracks, including its six catalogue disagreements.

   | Sample | Selected | Below 10 d | 10 to below 14 d | 14 to below 20 d | 20 to below 27.4 d | At least 27.4 d |
   | --- | ---: | ---: | ---: | ---: | ---: | ---: |
   | Affected G2 | 112 | 30 | 25 | 28 | 14 | 15 |
   | New G3 | 60 | 15 | 14 | 14 | 14 | 3 |
   | Seen controls | 53 | 35 | 8 | 10 | 0 | 0 |

   Before fitting, 106 affected stars, all 60 G3 stars and all 53 seen controls had at least three stored sector groups. The judging denominator instead requires measured eclipses in three sectors. Evidence: private `samples.json` and the prefit console output.

2. **CONFIRMED: affected-set H1 fails.** Saved 014 eclipse measurements were reused as allowed, with the frozen product-error scales and unchanged `032_error_model.py`. The largest sector number with measured eclipses was held out. Only earlier-sector measurements entered the v3 fit, clipping and usability decision. Held-out measurements were never clipped. These counts are producer-recounted:

   | Primary period bin | Eligible | Usable training fit | Predicts |
   | --- | ---: | ---: | ---: |
   | Below 10 d | 24 | 21 | 21 |
   | 10 to below 14 d | 20 | 17 | 17 |
   | 14 to below 20 d | 22 | 16 | 13 |
   | 20 to below 27.4 d | 10 | 7 | 7 |
   | At least 27.4 d | 14 | 9 | 9 |
   | Total | 90 | 70 | 67 |

   This separates two different questions: how often the method provides a usable fit, and how well those usable fits predict future measurements. Good predictions among the usable subset do not override the failed usability gate. Evidence: `032b_holdout.py`, private `judged-affected.json`, `cached-summary.json` and `cached-recount.json`. No threshold or verdict was retuned.

3. **CONFIRMED: requested non-judging results for cached G2 data.** All **53/53 seen controls** have eligible, usable training fits and predict the held-out sector. This is explicitly a seen-sample result. On all-sector primary fits, catalogue agreement is **8/76 usable affected tracks** and **47/53 seen controls**. Period agreement within three combined sigmas is 63/76 and 39/53, respectively. Neither catalogue statistic judges 032b. The previous 032 FAIL remains unchanged.

   Secondary tracks: affected stars have **72 eligible, 48 usable, 43 predicting**; seen controls have **50 eligible, 48 usable, 47 predicting**. The training fits drop 25 primary and 19 secondary times in the affected set, and 67 primary and 67 secondary times in the seen set. All-sector fits drop 28 primary and 20 secondary affected times, and 69 primary and 72 secondary seen-control times. Detailed period bins and all failures remain in private outputs.

4. **CONFIRMED: verification performed, with a numerical exclusion.** `032b_test.py` passed six groups covering held-out leakage and a deliberately shifted held sector, inclusive prediction boundaries, sector/training usability guards, H1/H2/H3 and empty-denominator failures, AST identity of measurement/alias/trap/allocation functions with 032, and four simulated forbidden access attempts. The forbidden files were not opened. The copied modules also passed their hash checks. The 30-case trap was actually rerun using the unchanged code, seed and original noise library: **30/30**.

   `032b_recount.py --cached-only` checked **528 training/all-sector fits** by closed-form weighted regression without importing the v3 fitter. It checked clipping membership, final slope and epoch, covariance, extra-scatter solution, final residual scatter, usability, held-out offsets, catalogue comparisons, counts and period bins. A deliberately changed prediction verdict was rejected. This is producer verification using a different arithmetic method, **not independent review**.

   The first recount stopped on an initial chi-square comparison. Inspection found sub-resolution saved timing errors: some are smaller than one floating-point spacing of their measured times. **Seven initial chi-square diagnostics across the affected and seen samples are therefore NOT VERIFIED by the second arithmetic method.** Three were first identified among affected secondary fits; four more occur in the seen sample. The recount explicitly records these numerical exclusions. All final-fit and gate checks remained strict and passed. No measurement, error-model parameter, fitted result or judging threshold was changed. The numerical cause is LIKELY roundoff amplification; no deeper investigation or fix is claimed.

5. **CONFIRMED: G3 continuation launched and startup observed.** `032b_run.py` is running two measurement workers with `NUMBA_NUM_THREADS=2`, one BLAS/OpenMP thread each, atomic per-star checkpoints, private logs and precreated output folders. Ten Python processes were present before launch; none was stopped or modified. The launcher process was 17852; the actual Python supervisor recorded in progress is **11900**.

   Started **11:36:56 am Kuwait, 23 Nov**. Expected finish **1:36:56 pm Kuwait, 23 Nov**, a conservative unmeasured two-hour allowance, not a runtime prediction. This is saved in `data/astra/032b/progress.json`. The one startup inspection showed `running`, phase `G3 measurement`. No healthy worker log was read and no repeated progress polling was performed.

   After both workers finish, the same supervisor runs the full `032b_summary.py` and `032b_recount.py`. It records code hashes before the run and checks them again at the end, including the unchanged v3 error model and the production frozen-module snapshot. Those end checks are **pending**. Hash equality will establish source identity only. The supervisor marks completion only after the full recount and end checks succeed. It cannot launch Part B because the affected H1 failure is already established.

## Continuation and evidence

The running job writes `summary.json`, `recount.json` and terminal `progress.json` under `data/astra/032b/`. This report is a handoff snapshot; it is not automatically rewritten when the job finishes. The new G3 figures and full recount must be added after terminal completion, without rerunning completed healthy work.

Only after a terminal failure or interrupted process is established, resume with:

```powershell
& D:/second-sun/.venv/Scripts/python.exe -I -B research/astra/scripts/032b_run.py
```

The supervisor rejects overlap and already-complete progress, locks source hashes, and reuses completed per-star checkpoints. A stale running marker requires inspection by the next session, not a second launch. All prior 032 and 014 outputs are read-only.

## What I did NOT check

- G3 measurement outcomes, its H1/H2 result, catalogue agreement, secondary tracks and full recount are pending. A passing G3 result cannot reverse the affected-set H1 failure.
- Part B mask, new planet bench, T156, both mask endpoint identities, untouched background, TOI-1338 b recovery and RS-027 event removal were not implemented or run: the fixed gate forbids Part B.
- The held-out experiment withholds times from the linear ephemeris fit. Discovery, cycle labels and measurement templates still use all-sector light, as in the unchanged 032 method. This is not a fully blind raw-flux extrapolation experiment.
- No independent reviewer has checked this work. No fence-check tool was run; Claude's fence review remains required. No claims are made about brightness/product/era-specific validation, unseen fenced stars, or a production filter improvement.
- Final static checks at 11:40 am Kuwait parsed 25 new Python files, checked the report for forbidden dash characters, and ran `git diff --check` with no tracked whitespace errors. New untracked files are not covered by that Git whitespace check. No blanket all-checks-passed claim is made.

## STOP SIGNS hit

**Part B gate closed:** affected H1 fails by two usable tracks. No tuning and no Part B. The initial chi-square verification exception is disclosed above; final decision counts were verified. The remaining G3 work is handed back as requested under the detached-run/no-polling rule.

## QUEUE PROPOSALS

None added. Keep node 1.4 / FIX 94 unresolved. The numerical diagnostic is evidence for Claude's review, not an authorized change to the fixed method.

## IDEAS

None outside the brief.

## Disagreements with Claude

None. This is the preregistered H1 outcome, not a reinterpretation of 032 or permission to change v3.

## Questions for Ahmed

None. Completion and recount of the selected G3 sample are already authorized and running.

## Usage

Predicted before implementation: 40 five-hour points / 7 weekly points. First observed after initial reads: 34% five-hour / 23% weekly. Close-out observation: 61% / 27%, approximately **+27 / +4** rounded account-wide points, weekly actual/predicted about 0.57. Initial reads and the final response are not fully included. The UI meter was not available; figures came from the latest rate-limit record in this runner's local session log. Lesson: cached measurements can establish a mandatory stop before launching expensive downstream benches; disclose numerical exclusions instead of calling identity or producer arithmetic an independent review.

**Next:** Claude or the runner reads the terminal G3 summary and recount, then completes this report and independently checks the Part A verdict; a small review with no healthy-job rerun, usage not measured, and no new Ahmed decision needed.
