# 004 repeater bench, Tree node 1.1 (GPT-6.1 Sol, effort unverified)

**Repeater bench: PASS on all three gates. R 27.47% to 33.34% [25.88%, 40.10%]. Background flips 70 to 85. FIX 91 alone also passes all three gates.** Branch `astra/004-repeater-bench`.

## Part 1: frozen rule

Use candidate (b), binary-locked repetition. Within each saved star-sector, product and sign, flag only members of a triple of events in three distinct binary cycles. Use the first design catalogue period per campaign/star, as T156 did. For every pair in the triple, the absolute separation must be within one hour inclusive of a positive integer multiple of the catalogue period, using the nearest integer. Missing cycles are allowed. An event belongs if any triple qualifies. The common epoch cancels in time differences. This tests repeated orbital phase, and one hour borrows the fixed timing slack from Petrova's existing phase veto (pipeline/petrova_mask.py:25,236), allowing finite box-centre precision without giving unrelated events an entire transit width. No extra depth or duration gate. Use saved centres. Missing, nonfinite or nonpositive period retains the old count rule. Both signs use the same calculation. The three-cycle requirement preserves the original purpose of identifying multiple repeats within one sector.

Replay the frozen tier rules with only the chosen flag changed, including re-evaluation of cross-sector orbit lock. Keep matching, products, sample, reference band and previously matched-event exclusion fixed. Validate every stored pre-union tier and all saved final recovery decisions against the old rule. Saved group files contain pre-union tiers. The final T156 journals store outcomes, not every final event tier.

**Acceptance rule (Claude, written before any result; do not change it):** the change counts only if (1) reference-band R rises; (2) the background upside-down tier-1 count does not rise by more than its counting error (new count at most old + 2 x sqrt(old + 1)); (3) planted-bump recovery stays within the paired 99% intervals of dip recovery per bin, as in 003. Report each condition as PASS or FAIL. Anything else is not adopted.

FIX 91 is evaluated alone, with condition (1) replaced by R does not fall. Saved centres are rounded to 0.0001 day. A coincidence decision inside the resulting uncertainty band around the frozen 0.3-day boundary must be resolved from saved information or treated as unverified. No threshold changes. Use 10,000 whole-star bootstrap draws, seeded as in 003. Condition (3) uses per-bin paired differences with 99% intervals, as in 003.

## Part 2 checkpoint

CONFIRMED by saved-event replay. All 37,105 stored pre-union event tiers and 4,000 saved final recovery decisions agree with the original rule, across 14,835 baseline group files and 2,000 paired trials. Old R and its bootstrap interval reproduce 003. Reference dips gained 13, lost zero. Across all depths, dips 394 to 496 and bumps 400 to 483. Background real 123 to 176, flips 70 to 85. The counting allowance is 86.85 and each paired 99% interval includes zero. Full tables follow in the final report.

## Part 3 and verification

CONFIRMED. FIX 91 alone preserves every recovered dip and reduces background flips from 70 to 68. It loses one planted bump outside the reference band. Both trials and background are compared against Petrova 1.0.0 independently of the repeater change.

The sprint004 harness uses the 12 verified sprint003 copies. Output paths point to 004 in audit_all.py, dataset.py, stage2_search.py and stage3_report.py. The only science-code edit in those copies is the symmetric veto call in stage2_search.py. The bench executes saved-event replay. It applies the equivalent reverse coincidence flag on the stored event records, then reruns SAP merging and downstream tiers, including cross-sector orbit lock and Petrova veto. Saved forward flags resolve any single possible rounded-centre partner. There were zero unresolved boundary decisions. The edited Stage 2 call was checked statically. No new FITS search was required.

Both replays matched all 37,105 stored pre-union tiers, with the original repeater predicate checked separately, and all 4,000 saved final arm recovery decisions. The files supply no event-by-event final-tier oracle beyond the saved outcomes, so this proof covers stored tiers and final recovery decisions at their respective levels. The whole-star bootstrap reproduced the old interval exactly. A separate count of gained and lost outcomes reconciled all five bins. Eight synthetic cases exercised phase alignment, skipped cycles, same-cycle and inconsistent-phase rejection, missing-period fallback and rounded coincidence boundary handling. These are producer checks.

## Binary-locked repeater

Reference R 27.47% to 33.34%. Whole-star bootstrap 95% intervals [20.72, 33.71]% to [25.88, 40.10]%.

| Binary period (days) | Reference dip recovered (old to new) | Reference dip R (old to new) | Reference R 95% intervals (%) | All dips (old to new) | All bumps (old to new) | New paired 99% CI (points) |
|---|---|---|---|---|---|---|
| 5 to 10 | 6 to 7 / 48 | 12.50% to 14.58% | [4.00, 23.08] to [5.36, 25.00] | 47 to 60 | 55 to 64 | [-4.16, 2.07] |
| 10 to 14 | 9 to 11 / 35 | 25.71% to 31.43% | [11.11, 40.01] to [11.76, 51.72] | 78 to 97 | 69 to 93 | [-2.32, 4.27] |
| 14 to 20 | 12 to 16 / 46 | 26.09% to 34.78% | [14.00, 39.02] to [20.93, 49.02] | 71 to 92 | 80 to 95 | [-4.41, 2.98] |
| 20 to 27.4 | 19 to 23 / 47 | 40.43% to 48.94% | [20.00, 57.89] to [28.57, 65.71] | 91 to 113 | 80 to 94 | [-0.67, 12.21] |
| 27.4 and above | 15 to 17 / 46 | 32.61% to 36.96% | [18.92, 46.15] to [22.64, 50.00] | 107 to 134 | 116 to 137 | [-5.11, 3.84] |

All-depth columns have 400 pairs per bin. The paired interval is dip recovery minus bump recovery.

| Sample and arm | Old to new | Gained | Lost |
|---|---:|---:|---:|
| Reference dip | 61 to 74 | 13 | 0 |
| Reference bump | 62 to 70 | 8 | 0 |
| dip | 394 to 496 | 102 | 0 |
| bump | 400 to 483 | 83 | 0 |

Background primary tier-1 at SNR at least 7: real 123 to 176, upside-down 70 to 85. Upside-down ceiling 86.85.

| Acceptance condition | Verdict |
|---|---|
| R rises | PASS |
| Background upside-down count at or below ceiling | PASS |
| All paired 99% intervals contain zero | PASS |

## FIX 91 alone

Reference R 27.47% to 27.47%. Whole-star bootstrap 95% intervals [20.72, 33.71]% to [20.72, 33.71]%.

| Binary period (days) | Reference dip recovered (old to new) | Reference dip R (old to new) | Reference R 95% intervals (%) | All dips (old to new) | All bumps (old to new) | New paired 99% CI (points) |
|---|---|---|---|---|---|---|
| 5 to 10 | 6 to 6 / 48 | 12.50% to 12.50% | [4.00, 23.08] to [4.00, 23.08] | 47 to 47 | 55 to 54 | [-4.93, 1.46] |
| 10 to 14 | 9 to 9 / 35 | 25.71% to 25.71% | [11.11, 40.01] to [11.11, 40.01] | 78 to 78 | 69 to 69 | [-0.78, 5.21] |
| 14 to 20 | 12 to 12 / 46 | 26.09% to 26.09% | [14.00, 39.02] to [14.00, 39.02] | 71 to 71 | 80 to 80 | [-5.53, 1.18] |
| 20 to 27.4 | 19 to 19 / 47 | 40.43% to 40.43% | [20.00, 57.89] to [20.00, 57.89] | 91 to 91 | 80 to 80 | [-1.41, 8.26] |
| 27.4 and above | 15 to 15 / 46 | 32.61% to 32.61% | [18.92, 46.15] to [18.92, 46.15] | 107 to 107 | 116 to 116 | [-6.93, 2.52] |

All-depth columns have 400 pairs per bin. The paired interval is dip recovery minus bump recovery.

| Sample and arm | Old to new | Gained | Lost |
|---|---:|---:|---:|
| Reference dip | 61 to 61 | 0 | 0 |
| Reference bump | 62 to 62 | 0 | 0 |
| dip | 394 to 394 | 0 | 0 |
| bump | 400 to 399 | 0 | 1 |

Background primary tier-1 at SNR at least 7: real 123 to 123, upside-down 70 to 68. Upside-down ceiling 86.85.

| Acceptance condition | Verdict |
|---|---|
| R does not fall | PASS |
| Background upside-down count at or below ceiling | PASS |
| All paired 99% intervals contain zero | PASS |

## Bugs found and limitations

CONFIRMED, Tree node 1.1, FIX 91. The original coincidence rule checks only the real arm for opposite-sign neighbours. The symmetric replay removes two background control events at tier 1 and one planted bump. This is the isolated price of the correction.

CONFIRMED, Tree node 1.1. The old repeater treats unrelated same-kind excursions as one repeating source. The new rule recovers all 13 reference dips that the 003 static diagnosis suggested could be released, with five-bin R up 5.87 percentage points. Short-period reference recovery remains 7/48, below 20%. The 15 additional background flips pass this brief's explicit counting allowance. Background real events rise by 53. Those counts are design-set events and do not establish the nature of individual detections. The two fixes' joint behaviour and the production implementation remain NOT TESTED. No claim that the G1 decision bar has been met.

STOP SIGNS: none triggered. QUEUE PROPOSALS: Tree node 1.1, record both isolated bench prices under the existing repeater and FIX 91 entries. IDEAS: none beyond the tested rule. Questions for Ahmed: none for this handoff.

## Usage

GPT-6.1 Sol, effort unverified. Predicted 35 five-hour points and 6 weekly points. The pre-commit meter moved 41% to 53% five-hour and 53% to 55% weekly, about 2 weekly points against a 10-point cap. Account bars are rounded and include account-wide use. Saved-event replay completed each comparison in about four to six minutes. Lesson: preserve the original forward coincidence flag so rounded saved centres can still support a reverse check.

Next: Claude reviews both isolated passes before building the Petrova candidate. A combined bench check would require a further saved-event replay, with usage to be sized for that review.
