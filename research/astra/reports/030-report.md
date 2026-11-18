**Plain verdict: PARTIAL. The amended design-background count runs successfully; the remaining bench and full T109 gate were not run in this continuation.**

# 030 lower-flank notch continuation

Codex, GPT-6-Astra; effort not independently verified in this continuation. Brief specifies neither. Branch `astra/030c-notch-continue`, unchanged. No git writes or commits. Tree nodes 1.3, 1.5 and 1.6.

## Findings

1. CONFIRMED: amended `030_known.py` now records both design-background counts and the exact note "design background holds 2 of 13 sectors". Runtime result: B 1 match, N1 2 matches. These are design-background results, not the full T109 rule (g) test. Evidence: `data/astra/030/known.json`.

2. CONFIRMED: threshold remains 6.5. Saved alarm curves select it as the lowest eligible threshold. These counts were read from the completed prior run, not regenerated in this continuation.

| Threshold | Real tier 1 | Upside-down tier 1 | Eligible |
|---:|---:|---:|---|
| 4.5 | 353 | 239 | False |
| 5 | 270 | 169 | False |
| 5.5 | 222 | 116 | False |
| 6 | 182 | 89 | False |
| 6.5 | 165 | 77 | True |
| 7 | 144 | 71 | True |

3. CONFIRMED: rule (g) is explicitly unknown (`pass: null`) in the design-only output. `030_summary.py` refuses to turn unknown evidence into a final PASS or FAIL. A focused runtime check rejected None and accepted both boolean outcomes. This is a producer guard check, not full-summary execution or independent review.

4. CONFIRMED: the source lock changed only for the two files below. Old and new SHA-256 values are preserved in `data/astra/030/030b-source-amendment.json`. Existing completion markers were preserved. The chosen threshold, seeds and rules (a) to (f) were not changed.

| File | Old SHA-256 | New SHA-256 |
|---|---|---|
| 030_known.py | `c3d949d68674cb47c066e3d0bfcf1302ce916396dbc7987c7b5a0a1b99eb6274` | `51a71919f392cfb0f0918d742b2bd021c07c500a636c01b7de59284043d95001` |
| 030_summary.py | `94ae929e70c450d3015422ba258eef30825cb2bab8e8fc6478ab4bade62f3c30` | `e05df7e08746b68e4f8017ca2d7ccec270992a0aacb1cc74d5417ea8ac9d7d7e` |

## Written gates and current evidence

| Gate | Number or evidence | Status |
|---|---|---|
| (a) Fresh gain at least 2 points, lower 95% bound above zero | Fresh replay not completed here | NOT TESTED |
| (b) Untouched alarms at most 174 / 79 | Saved chosen result 165 / 77 | PASS on saved counts |
| (c) Dip/bump 99% interval contains zero in every required bin | Paired scoring pending | NOT TESTED |
| (d) Off-switch identity and N1-only changes | Earlier checks and baseline records exist; not rerun here | NOT REVERIFIED |
| (e) New real minus 2.3 times new upside-down at most 5 | Final comparison pending | NOT TESTED |
| (f) T156 R at least B 34.207% | N1 T156 pending | NOT TESTED |
| (g) Full T109 TOI-1338 b at least 6 of 13 | Design-only counts cannot judge this gate | NOT TESTED |

Flags holding new detections, choosing/fresh P, paired intervals and per-crossing rates remain pending. No overall scientific verdict is supported.

## Checks actually performed

Ran `030_known.py` with the required interpreter, parsed both changed Python files, tested the summary evidence guard, checked the updated source-lock equality, and compared every frozen-file hash against `frozen-before.json`. `git diff --check` passed. Evidence: `data/astra/030/030b-checks.json`. Hash equality establishes byte identity only. Earlier 030 synthetic and baseline verification is recorded in the saved artifacts and original worklog; those suites were not rerun here.

## Remaining work and checkpoint

No long job was launched in this continuation. `progress.json` remains at the prior failed checkpoint; its old known-count failure message describes the pre-amendment code. Completed markers remain available. Before parallel replay, rerun `030_layout.py` to pre-create shared directories and check process load. Then resume the authorized three-worker foreground `030_run.py`.

The full T109/Q5 N1 implementation is still required after the bench phases. It must use the published system and all 13 crossing windows, reproduce B 6 of 13 on that path, and evaluate N1 at fixed 6.5. Wire its separate result into the summary while retaining design-background counts separately, update source-lock provenance before resuming, then run summary, verification and `030_finish.py`. The current summary deliberately stops until that full-path result is wired in. `030_finish.py` also still needs its branch and known-path wording updated before the final report is generated.

## What I did NOT check

No remaining planet, fresh or T156 replay; no full T109 N1 run; no full summary, verification or finish run. No fresh source research, download, fenced-star experiment, sky search, independent review, freeze, book edit or publication. Existing shared folder completeness was not checked again.

## STOP SIGNS hit

AGENTS.md section 7 says to stop near 80% of the five-hour bar. The first meter read in this continuation was already 87% five-hour / 79% weekly. It was read late, after initial source inspection. This continuation therefore saved a safe correction and stopped before the long replay. The original nine-versus-ten grid wording remains resolved by retaining the actual nine-length frozen grid. No new scientific tuning occurred.

## QUEUE PROPOSALS

None. Node 1.3 continuation remains unfinished.

## IDEAS

None outside the brief.

## Disagreements with Claude

None. The 030b amendment resolves the former scope mismatch.

## Questions for Ahmed

None; the remaining work is already authorized.

## Usage

Continuation checkpoint prediction: 3 five-hour / 1 weekly point, logged late after initial reads and the two-line correction. First observed 87% / 79%; latest observed 92% / 80%. These rounded account-wide readings do not isolate this task. Original full-task prediction was 60 five-hour / 10 weekly points. Lesson: read the meter before implementation files, and distinguish missing evidence from a failed scientific gate.

Next: Codex resumes the already-authorized 030b work after the five-hour allowance resets, to finish the remaining replay and full T109 test; remaining machine and usage cost are unmeasured, no new permission needed.
