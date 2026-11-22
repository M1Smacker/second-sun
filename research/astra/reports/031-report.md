**Plain verdict: PARTIAL, the checkpointed bench has been launched. No D1 scientific verdict is available yet.**

# 031 duration-aware notch D1

Codex, runtime model and effort not independently verified; brief specifies neither. Branch `astra/031-duration-notch`. No git writes or commits. Tree nodes 1.3, 1.5 and 1.6.

## Completed checks

CONFIRMED: the original 003 T156 design and the old fresh design reproduce exactly. New fixed seeds 2026112202 and 2026112201 produce repeatable designs of 2,000 and 1,250 draws. Evidence: `031_draws.py`, `data/astra/031/draw-checks.json`. No new bench was scored before this check.

CONFIRMED on synthetic light for the initial detector revision: both endpoint detector event identities, 27 duration-score array identities, merged-candidate oracle, and two duration-specific diagnostic curves pass. Wrong raw-SNR ranking and a shared diagnostic curve are detectable mutations. Evidence: `031_checks.py`, `data/astra/031/detector-checks.json`. The checks were subsequently expanded to exercise the actual controlled merger and mixed mirror flags; the supervisor must rerun the expanded checks before any new scoring. These are producer checks, not independent review.

CONFIRMED: five runtime checks of the actual mixed re-tiering function passed, including short/long thresholds, mixed mirrors and a threshold mutation (`retier-checks.json`). Static syntax and dash checks passed for all 23 brief scripts. `git diff --check` found no whitespace errors in the tracked diff; it excludes the new untracked files. Read-only git status showed no pipeline changes. No full runtime or independent-review claim is made.

The actual bench grid is 3, 4, 5, 6.5, 8, 10, 12, 15 and 20 hours. D1 retains all nine, with N1 through 8 hours. The all-N1 endpoint uses a cut of 21 hours, above the actual maximum, as permitted by the brief's differing-grid rule.

## Running and planned

The full historical endpoint tier identity supervisor was launched at 21:40 Kuwait on 22 November, with a conservative, unmeasured expected finish around 22:10 Kuwait. Exact start and expected finish are recorded in `data/astra/031/identity-progress.json`.

The full bench supervisor was launched at 21:50 Kuwait, with an unmeasured 24-hour allowance, approximately 21:50 Kuwait on 23 November. Its exact expected finish is in `data/astra/031/progress.json`. It waits for terminal identity success before starting workers, so the two supervisors do not overlap scoring workers. Three workers maximum, each with NUMBA_NUM_THREADS=2. Launch commands succeeded; terminal process health and outcomes have not been polled.

The remaining sequence is: rerun expanded synthetic checks; reproduce T109 B; prepare new observability journals; verify the adapted scorer against old B/N1 trial outcomes; generate untouched D1 light; score T109; replay old D1 and new B/N1/D1 planted light; bootstrap; independently recount saved point estimates; verify source hashes and worker completion; render the final counts-only report and companion tables. Failure stops the supervisor and appends a terminal checkpoint to this report. These are planned checks, not completed evidence.

The detector keeps both detrended curves and uses an event's duration to select its score and its shape diagnostics. Changing only the score would leave the later shape checks measuring a different curve.

For the requested exploratory duration splits, a planet is assigned by its median observed crossing duration; T156 uses its single duration. Bands are half-open. Rates give equal weight to populated period bins and list missing bins. This reporting convention was set before any D1 result was read.

## What I did NOT check

Full endpoint tier identity is pending. No D1 background count, new fresh gain, new T156 R, control interval, or T109 D1 result is available. No fenced-star search, frozen-file edit, publication, download or external write.

## STOP SIGNS hit

None yet. Identity failure is a mandatory stop. No threshold or cut may be adjusted after scoring.

## QUEUE PROPOSALS

None.

## IDEAS

None outside the brief.

## Disagreements with Claude

None. The extra 20-hour grid length is retained.

## Questions for Ahmed

None.

## Usage

Predicted 60 five-hour points / 10 weekly points. Initial meter 1% / 0%; latest observed at 21:51 Kuwait 53% / 8%, approximately +52 five-hour and +8 weekly points. Weekly actual/predicted ratio about 0.8 at handoff. Account-wide rounded values. Lesson: duration routing must also select the diagnostic detrend, not only the detection score.

Next: Codex resumes after terminal completion or failure to review the saved outcome; no polling while healthy, expected small review usage but unmeasured, Ahmed or Claude must trigger the continuation.
