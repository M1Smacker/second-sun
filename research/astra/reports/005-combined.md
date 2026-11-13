# 005 combined report (GPT-6.1 Sol, effort unverified)

- **Part 0 PASS.** The adopted rules together recover 33.34% [25.88%, 40.10%] of reference transits, with 176 real and 83 upside-down background tier-1 events.
- **Part A cause UNCERTAIN.** The repeater adds 59 real events and loses six. Fifty-four of 56 classifiable additions are at least two eclipse widths away. No narrower lock is supported.
- **Part B diagnosis CONFIRMED.** All 19 short-period reference detection misses are below SNR 7 in the measured paths. Median fitted depth changes little during detrending.
- **Part C diagnosis CONFIRMED.** Sixteen of the 52 reference window losses have usable centre support before the window rule. Safe recovery is NOT TESTED.

Branch `astra/005-three-diagnoses`. The combined result passes the prior 004 acceptance criteria. The G1 bar remains FIX FIRST. The baseline uses both adopted changes and preserves the prior sample and match rule. The only candidate evaluated for acceptance in 005 was the already adopted combination. The phase detrending and expanded coverage candidates are specified for future tests, with no measured gains claimed for either.

| Full report | Evidence |
|---|---|
| [Combined baseline](005-0-baseline.md) | Per-bin recovery, background counts, all three gates and parity |
| [Real-side rise](005-A-real-side-rise.md) | Phase, product, era, clustering, amplitudes, widths and cycle partners |
| [Short-period blind spot](005-B-short-period-blind-spot.md) | 800 fixed dip replays, stage-level scores, depth retention and phase split |
| [Window losses](005-C-windows.md) | Archive and loaded cadence support on 52 fixed reference trials |

## Ranked work toward the G1 bar

1. **Node 1.5, test whether the short-bin excess noise follows binary phase.** The 19 below-bar cases represent at most 7.92 percentage points of equal-bin R if every one reaches tier 1. Establish repeatable structure before the cross-cycle detrending candidate. The phase scatter split suggests a direction but is too small and confounded for a gain forecast. All five bins together have a 18.80-point detection-loss ceiling. The measured short-bin weakness accounts for less than half of that ceiling.
2. **Node 1.2, verify independent safe coverage for the six usable missing-window trials.** Full recovery of those six would add at most 2.55 points. The wider set of 16 quality-selected window losses gives a 6.97-point ceiling. This requires evidence about actual coverage and false alarms. The 15 archival gaps cannot be recovered by rewriting windows. The 21 load losses need their own quality/flux justification.
3. **Node 1.1, keep the real-side increase visible and price specific tier blockers.** The 59 gains and six losses make a narrow eclipse-phase adjustment low priority. Prioritize single-flag cases and exact downstream replay. The prior 003 static step-only release was one reference trial, so the frequency of that flag is a poor estimate of its removable loss. The combined configuration itself has not been separately repriced flag by flag.
4. **Node 1.4, isolate mask from insufficient cadence support.** Perfect recovery of the original 15 mask/support losses adds at most 6.68 points. None of that is a measured improvement. A real change must preserve false-alarm protection.

The point estimate needs another 16.66 percentage points to reach 50%, plus a lower interval bound of at least 40%. The short-bin detection and usable-window ceilings together add 14.88 points even with perfect downstream survival. These ceilings use fixed original loss bins and equal-bin weights. They describe available headroom without predicting what repairs will deliver. The current evidence cannot establish a route to GO from one change.

## Verification and handoff

CONFIRMED: saved baseline parity at the stored tier and recovery-decision levels, whole-star interval replay, exact injected event parity in 1,213 diagnostic group files, archive support classification for 52 trials. The first diagnostic attempt stopped on a SAP mismatch caused by reconstructing the path without the SAP suffix. The saved input routing identified the cause and the corrected replay passed on the entire prescribed sample. This is a harness bug at node 3.2. No new frozen pipeline bug was established. The artifacts are producer verification for Claude's review. No candidate detection rerun beyond the preregistered unchanged diagnostic, no change to the original decision bar and no freeze.

STOP SIGNS: the Part B identity stop was recorded, diagnosed and resolved before retry. No unresolved stop. QUEUE PROPOSALS: node 1.1 track baseline and real-side transitions, node 1.5 file score and phase diagnosis under T161, node 1.2 file measured support under T155 and FIX 26/70. IDEAS: one short-bin treatment and one coverage repair, each described in its report. Questions for Ahmed: none for this handoff.

Usage predicted 1/3/5/4/1 weekly points for baseline/A/B/C/report. Account snapshot before the final report was 71% five-hour and 58% weekly, from 54% and 55% at start. This is +17 five-hour and approximately +3 weekly points, below the total cap of 20 weekly points. The baseline, detection and short saved-data analyses overlapped, so part-specific increments are not identifiable. Lesson: reconstruct SAP dispatch from the saved group role, since the saved filename drops the suffix.

Next: Claude reviews the four reports and scopes the phase-coherence check at node 1.5. The check's cost should be sized before a candidate bench run.
