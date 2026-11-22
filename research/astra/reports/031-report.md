**Plain verdict: BLOCKED in 031c by the usage stop. The exclusion is authorized but has not been implemented or run.**

## 031c checkpoint, 22 November 2026, 22:58 Kuwait

Codex, runtime model and effort unverified. Branch confirmed: `astra/031c-duration-notch-resume`. Tree nodes 1.3, 1.5 and 1.6. No git writes, branch switches or commits.

**CONFIRMED: authority is resolved.** Brief `031c-duration-notch-resume.md` supersedes the policy blocker in the historical 031b report below. It authorizes excluding empty selected-product draws from B, N1 and D1 in the records step and reporting exclusions by campaign and bin. Its expected new T156 population is 1,998, an authorized target count, not a newly measured completed-record count.

**CONFIRMED: usage prevents continuation.** The first observed current-session meter was 88% five-hour and 14% weekly, after initial reads. AGENTS.md section 7 requires stopping near 80% five-hour. The meter's reset timestamp converts to **23 November 2026, 02:34:14 Kuwait**. No source edit, source-lock update or supervisor restart was made. This is a usage stop, not a scientific failure or a request for another sampling rule.

**CONFIRMED: checkpoint inspection.** `progress.json` reports the prior failed records stage. The G3 records completion marker and earlier checks remain present. No data file or marker was changed. Read-only SHA256 checks returned:

| File | Old and current SHA256, unchanged |
|---|---|
| `031_records.py` | `1fbe3918b1608816ce76bff51ab4607dd40d7948cf3e29ba6adb13b7df9254b0` |
| `run-source-hashes.json` | `e6b201917023d674f44a1d78b1d8156fafdd81888e00dea9d35912d1f39c66de` |

Hash equality establishes unchanged bytes for these two files only. It is not semantic verification or independent review. Keeping completed markers lets the supervisor skip completed phases when it resumes.

**NOT TESTED in 031c:** exclusion implementation, new records totals, fresh-bench exclusions, resumed scoring, rules (a) to (g), duration bands, holding flags, per-crossing rates and choosing-bench unscored-notch counts. No runtime tests ran. Earlier evidence below remains historical. The earlier queue proposal for an authorized rule is resolved by 031c. No new queue proposals, ideas, disagreements or questions for Ahmed.

Usage: predicted 2 five-hour / 1 weekly points for this safe checkpoint from the first observed 88% / 14%; close-out observation is in USAGE.md. Lesson: inspect the meter before implementation files.

Next: Claude relaunches brief 031c after the five-hour reset to implement and test the authorized exclusion and resume the bench; Claude required, continuation usage unmeasured.

## Historical 031b report, policy blocker superseded by 031c

**Plain verdict: 2 new draws have empty raw spans. BLOCKED: the original bench has no replacement rule, so 031b requires stopping.**

# 031 duration-aware notch D1, continuation report

Codex, runtime model and effort independently unverified; brief specifies neither. Updated 22 November 2026, 22:54 Kuwait, from the observed clock. Branch `astra/031b-duration-notch-continue`. No git writes, commits, pushes, or branch switches. Tree nodes 1.3, 1.5 and 1.6.

## Findings

1. **CONFIRMED: original T156 stops on an empty raw span.** `research/astra/scripts/003_worker.py:116` selects the best product, falling back to the first metadata entry only if no matching product exists. Line 120 raises `RuntimeError('Empty raw span: input failure requires separate diagnosis')` when the selected product loads no times. It does not try another product, redraw, or exclude the trial. `research/astra/reports/003-recovery-sprint.md:130` explicitly says missing raw spans are input failures, not replacements. The fallback for an absent best-product entry is not a fallback for an empty loaded product.

2. **CONFIRMED: all 2,000 original saved trials match their original design fields exactly, with no missing or duplicate trials.** G2 has 1,579 results and G3 has 421. Each contains the time and both arm results, which the original worker writes only after the empty-span stop. Thus there was no empty-span case among those completed original draws. The 421 existing G3 old-record entries also equal their archived results after removing the added archive-folder field. G2 old-record output was never written before the stop, so no corresponding file identity is claimed. This is an archive comparison, not a fresh raw replay of the original 2,000 injections.

3. **CONFIRMED: the new seed has two empty selected-product spans.** The diagnostic loaded the selected primary product once per distinct new star-sector group, behind the existing design-only read and output guards. No masks, detrending, injection, searches or re-tiering ran.

| Campaign | New draws | Distinct groups loaded | Empty draws | Distinct empty groups |
|---|---:|---:|---:|---:|
| G2 | 1,552 | 1,336 | 2 | 2 |
| G3 | 448 | 399 | 0 | 0 |
| Total | 2,000 | 1,735 | 2 | 2 |

Both affected draws fall in the 5 to 10 day binary-period bin. No nonempty selected group has a zero-length time span. Zero draws were replaced, redrawn or excluded. The original design remains 2,000 draws; the affected draws remain unresolved input failures, not measured recovery failures.

Evidence for findings 2 and 3: `research/astra/scripts/audit_031b_spans.py`, private `data/astra/031/031b-span-audit.json` and `031b-span-audit.log`. The script checked every original draw field against the saved journals and loaded all 1,735 distinct new selected products. These are producer checks, not independent review.

The engineering issue is the sampling rule: dropping or replacing an unusable draw changes what population the bench measures. There is no authority here to make that choice after seeing the new draw.

## Source lock and checkpoints

**CONFIRMED: every existing `031*.py` source still matches `run-source-hashes.json`.** No bench source patch was made, so the old and new hashes are identical. The standalone diagnostic is named `audit_031b_spans.py` and is not part of the supervisor's `031*.py` lock. A future resumed run must explicitly review any actual source changes.

| File | Old SHA256 | New SHA256 |
|---|---|---|
| `031_records.py` | `1fbe3918b1608816ce76bff51ab4607dd40d7948cf3e29ba6adb13b7df9254b0` | `1fbe3918b1608816ce76bff51ab4607dd40d7948cf3e29ba6adb13b7df9254b0` |
| `run-source-hashes.json` | `e6b201917023d674f44a1d78b1d8156fafdd81888e00dea9d35912d1f39c66de` | `e6b201917023d674f44a1d78b1d8156fafdd81888e00dea9d35912d1f39c66de` |

Original worker SHA256: `6b45e8a103caaaf2e1af3eaf6f0fe8d538cf4d6c00485c60d4b2a9b2eab8269f`.
Executed diagnostic SHA256: `0e429c364df5a3d737f1655f3d19ab14839e60db01c8bbad13287094090ff264`.
Hash equality establishes unchanged bytes, not scientific correctness.

The supervisor remains failed at fixed draw observability and historical replay validation. Its progress file, all completed markers, and the completed G3 records were preserved. `031_run.py` was not resumed. No replacement policy was added to the source lock. The original 24-hour completion estimate is obsolete because this requires a decision, not more compute.

## Existing endpoint evidence and scientific rules

**CONFIRMED as saved producer evidence, not rerun in this continuation:** `identity-progress.json` is complete and `identity-checks.json` passed eight endpoint comparisons. B reproduces P 48.105 on 1,098, background 174 real / 79 upside-down, and old reference R 34.207. N1 reproduces background 165 / 77 and old reference R 31.653. The endpoint checks reuse complete saved pre-tier events and replay tiers; raw endpoint dispatch was tested on synthetic light. They are not full raw-light replays of every historical endpoint trial.

| Rule | Status |
|---|---|
| (a) New fresh paired gain and interval | NOT TESTED, full bench blocked |
| (b) D1 untouched background limits | NOT TESTED |
| (c) D1 dip-against-bump control | NOT TESTED |
| (d) Endpoint identity | Saved producer checks PASS, scope above |
| (e) D1 new-event excess | NOT TESTED |
| (f) New T156 R against B | NOT TESTED, two unresolved input failures |
| (g) D1 TOI-1338 b recovery | NOT TESTED |

No scientific D1 pass or fail verdict is available. This tooling stop is not evidence that D1 fails a scientific rule.

## What I did NOT check

No D1 scientific scores were generated in this continuation. Requested B/N1/D1 duration-band comparisons, holding flags, per-crossing rates, and new T156 R remain pending. The additional choosing-bench counts of crossings with NO notch score for D1 and N1 are NOT TESTED here; Claude's reported A12 count is not substituted for those bench measurements. Completing those requests would require proceeding past the explicit stop.

No new raw replay of old T156, fresh confidence intervals, independent review, frozen-file edits, downloads, publications, or fenced-star analysis. Only the source-lock comparison and archive reconciliation were performed here in addition to raw loading.

The diagnostic reached and wrote its terminal JSON after all assertions. The PowerShell invocation returned exit code 1 while logging native stderr warnings, including a docstring escape warning and a Lightkurve optional-module warning. A clean shell exit is not claimed; terminal data and the full log are retained for review. The diagnostic's results do not depend on those warnings.

## STOP SIGNS hit

Brief 031b item 2: if 003 had no such case and no rule exists, stop and report the count. Original code has an input-failure stop, but no rule permitting replacement or continued scoring. This condition is met. No implementation change or supervisor restart is authorized by the evidence found.

Usage reached the project stop-near-80% five-hour line during close-out. Several short session-output checks were made while the diagnostic ran, contrary to the project's no-polling practice. No live scientific logs were read while it was running. Future diagnostics should use a detached job and a single terminal wait or handoff.

## QUEUE PROPOSALS

Node 1.5, BUILD decision for Claude: define and authorize handling of empty selected-product spans before resuming the new T156 bench. This report proposes no particular replacement or exclusion policy.

## IDEAS

None outside the brief.

## Disagreements with Claude

None. The continuation explicitly anticipates this stop.

## Questions for Ahmed

None at this stage; Claude can review the evidence and prepare a concrete handling rule.

## Usage

Prediction logged before the diagnostic: 10 five-hour / 2 weekly points from first observed meter. First observed after initial reads: 68% / 11%. Latest observed at close-out: 80% / 12%, approximately +12 / +1, rounded account-wide values, excluding initial reads before the first observation. Weekly actual/predicted ratio approximately 0.5 on that observed interval. Prior 031 usage remains in USAGE.md.

Lesson: an absent best-product entry and an empty loaded best product are different cases; never extend one fallback to the other without evidence.

Next: Claude reviews these two input failures and supplies an authorized handling rule so the bench can resume; Claude required, review usage unmeasured.
