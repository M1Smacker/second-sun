**Plain verdict: PARTIAL. The archived B numbers are reproduced independently and the N1 implementation tests pass; the full copied-chain reproduction and scientific bench do not yet have observed terminal results.**

# 030 lower-flank notch tier bench

Codex, GPT-6-Astra high, confirmed from this runner's own session metadata. Brief 030 specifies no model or effort. Started 18 November 2026. Branch astra/030-notch-tier-bench, unchanged. No git writes, commits, pushes or publication. Tree nodes 1.3, 1.5 and 1.6.

## Findings

1. **CONFIRMED, independent archived-outcome recount:** B is 48.1050309103% on 1,098 observed planets, 48.4044435302% on the 968 possible planets, and 174 real / 79 upside-down untouched tier-1 events. `030_recount.py` joins archived 027 outcomes to the 006 injection journals and the host-radius catalogue without importing the pipeline. Evidence: `data/astra/030/independent-recount.json`. This verifies the archived counts, not the new chain's runtime identity.

   | Binary-period bin, days | All: hits / n | Possible: hits / n |
   |---|---:|---:|
   | 5 to 10 | 99 / 242 | 87 / 210 |
   | 10 to 14 | 102 / 229 | 88 / 198 |
   | 14 to 20 | 90 / 221 | 86 / 202 |
   | 20 to 27.4 | 96 / 187 | 83 / 167 |
   | 27.4 and up | 138 / 219 | 122 / 191 |

2. **CONFIRMED, implemented and synthetic-tested:** N1 is a switch installed only into the redirected bench copies. The off switch leaves detector objects unchanged. The on switch implements the five-day detrend, lower-flank statistic and quarter-box mirror rule. Exact N1 scores and centres are retained to avoid rounding across a threshold or mirror boundary. Frozen source files were not edited.

3. **CONFIRMED, runtime checks:** all 27 cadence/duration cases agree with the isolated `notch_scores` reference function, and a separately implemented direct-window mean calculation agrees with the new prefix-sum calculation. The deliberately wrong upper-flank choice is detected at 11,414 tested windows. Three mirror-boundary checks, 15 threshold-nesting checks, zero-scale handling, a threshold-context mutation and a one-arm-budget mutation pass. Evidence: `030_checks.py`, `data/astra/030/notch-checks.json`. A test-output serialization error was fixed and the checks reran successfully. These are producer checks, not independent review.

4. **CONFIRMED, specification discrepancy:** the executable frozen grid and RS-039 reference initialization use nine box lengths, not the brief's ten: 3, 4, 5, 6.5, 8, 10, 12, 15 and 20 hours. The draft preserves those nine. Evidence: `pipeline/stage3_core.py` GRID_V4/GRID_V5 and `data/fable/f2/x4_faint.py` init, read only. No tenth length was invented.

5. **NOT TESTED to completion:** full B scoring, raw off-switch identity, N1 alarm curves, chosen threshold, choosing/fresh P, paired intervals, new-event excess, flags, T156 R and TOI-1338 counts. No claim of a gain or pass is supported yet. The foreground baseline job started at 11:30:43 Kuwait, with an estimated finish recorded near 12:00:44. This is an estimate, not observed completion.

## Implementation and run protocol

`030-worklog.md` records decisions before any N1 science result. `030_run.py` requires the B reproduction output, pre-creates shared folders, checks 50 raw off-switch star-sectors, and then runs at most three workers with two Numba threads each. All data, logs, source copies and progress files stay under `data/astra/030/`. Its source fingerprint prevents silent reuse of checkpoints after code changes.

The N1 scorer filters the candidate pool before recalculating mirror/repeater flags, SAP union, cross-star flags, OAE and FIX 95. This matters because a weak event removed by a higher threshold must no longer flag a stronger neighbour. Choosing the threshold after tiering an unchanged low-threshold pool would price a different detector.

The threshold remains the lowest of 4.5, 5, 5.5, 6, 6.5 and 7 with at most 174 real AND 79 upside-down alarms. It is locked before planet scoring. If none qualifies, no fresh N1 is scored. Otherwise the script uses the fixed 006 draws, Fable X1 seed 2026111601, 10,000 whole-host bootstrap draws with seed 2026111830, the T156 reference subset and the existing T109 matching windows. Whole-host resampling keeps correlated planets on one star together rather than pretending each is independent.

Prepared commands, using the required interpreter:

```powershell
& D:\second-sun\.venv\Scripts\python.exe -I -B research/astra/scripts/030_baseline_run.py
# Only after the baseline reaches baseline_complete:
& D:\second-sun\.venv\Scripts\python.exe -I -B research/astra/scripts/030_run.py
# Only after the full run reaches complete and verification.json passes:
& D:\second-sun\.venv\Scripts\python.exe -I -B research/astra/scripts/030_finish.py
```

The foreground chained command was launched at 11:49:19 Kuwait on 18 November. It uses one blocking wait, capped at 60 minutes, for successful B completion and then invokes `030_run.py`. The command is attached to execution session 86358; the original baseline command is session 96382. No detached process was launched. Terminal completion has not been observed at this handoff.

Do not launch a duplicate while `progress.json` says running. The full replay's 16-hour runtime allowance is a conservative, unmeasured estimate; the actual start and estimated finish are written by the runner. A failed baseline or off-switch comparison stops before N1 light-curve work. Inspect a failed terminal log before resuming; never bypass the source lock or a scientific gate. If the external runner closes the foreground sessions at handoff, verify that the owned processes have exited before recording the interruption and resuming checkpoints.

## What I did NOT check

No final scientific result exists in this report. No fenced-star search, real-sky hunt, witness-star meter, independent review, download, freeze, book edit or publication. The new N1 generator and end-to-end scorer still need their real-light execution. All 20 new Python scripts were statically parsed; the final summary/report paths are not yet exercised on completed N1 outputs. `git diff --check` found no tracked whitespace errors and `git diff --name-only -- pipeline targets` returned no changes. The preexisting `.codex_run.lock` was preserved. Syntax checks do not establish scientific correctness.

## STOP SIGNS hit

- The nine-versus-ten grid wording was resolved by preserving the actual frozen grid and reference initialization. No scientific threshold was altered.
- One early terminal-status poll returned no output before the 30-minute interval. No healthy-run logs were inspected and no scientific setting was chosen from it. Subsequent waiting must use the authorized single blocking terminal wait or handoff.
- The first synthetic-check result writer could not serialize a NumPy integer. The counter was converted to a Python integer and the full check reran, passing. This was a harness-output error, not a scientific result.

## QUEUE PROPOSALS

None. The existing node 1.3 bench remains active.

## IDEAS

None outside the brief.

## Disagreements with Claude

Only the documented grid-count wording; no scientific decision is changed or challenged without evidence.

## Questions for Ahmed

None. The current brief already authorizes the work.

## Usage

Predicted before implementation: 60 five-hour points / 10 weekly points. The initial local rate-limit record shows 38% five-hour / 71% weekly. The latest observed record, at 11:49:28 Kuwait, shows 68% / 76%: approximately 30 five-hour points and 5 weekly points so far, half the predicted full-task weekly cost. This is a partial-task measurement, not the final cost. Runtime metadata confirms GPT-6-Astra high. See `research/astra/USAGE.md`.

Lesson: an archived-count recount, a synthetic detector test and a full raw-light bench answer different questions; none can substitute for the others.

Next: continue the authorized foreground chain after the B gate, then review its terminal evidence; machine time is estimated at up to 16 hours, remaining model usage is unmeasured, Codex can continue without new permission.
