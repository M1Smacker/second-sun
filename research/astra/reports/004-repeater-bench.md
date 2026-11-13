# 004 repeater bench, Tree node 1.1 (GPT-6.1 Sol, effort unverified)

**Repeater bench: PASS on all three gates. R 27.47% to 33.34% [25.88%, 40.10%]. Background flips 70 to 85. FIX 91 pending.** Branch `astra/004-repeater-bench`.

## Part 1: frozen rule

Use candidate (b), binary-locked repetition. Within each saved star-sector, product and sign, flag only members of a triple of events in three distinct binary cycles. Use the first design catalogue period per campaign/star, as T156 did. For every pair in the triple, the absolute separation must be within one hour inclusive of a positive integer multiple of the catalogue period, using the nearest integer. Missing cycles are allowed. An event belongs if any triple qualifies. The common epoch cancels in time differences. This tests repeated orbital phase, and one hour borrows the fixed timing slack from Petrova's existing phase veto (pipeline/petrova_mask.py:25,236), allowing finite box-centre precision without giving unrelated events an entire transit width. No extra depth or duration gate. Use saved centres. Missing, nonfinite or nonpositive period retains the old count rule. Both signs use the same calculation. The three-cycle requirement preserves the original purpose of identifying multiple repeats within one sector.

Replay the frozen tier rules with only the chosen flag changed, including re-evaluation of cross-sector orbit lock. Keep matching, products, sample, reference band and previously matched-event exclusion fixed. Validate every stored pre-union tier and all saved final recovery decisions against the old rule. Saved group files contain pre-union tiers. The final T156 journals store outcomes, not every final event tier.

**Acceptance rule (Claude, written before any result; do not change it):** the change counts only if (1) reference-band R rises; (2) the background upside-down tier-1 count does not rise by more than its counting error (new count at most old + 2 x sqrt(old + 1)); (3) planted-bump recovery stays within the paired 99% intervals of dip recovery per bin, as in 003. Report each condition as PASS or FAIL. Anything else is not adopted.

FIX 91 is evaluated alone, with condition (1) replaced by R does not fall. Saved centres are rounded to 0.0001 day. A coincidence decision inside the resulting uncertainty band around the frozen 0.3-day boundary must be resolved from saved information or treated as unverified. No threshold changes. Use 10,000 whole-star bootstrap draws, seeded as in 003. Condition (3) uses per-bin paired differences with 99% intervals, as in 003.

## Part 2 checkpoint

CONFIRMED by saved-event replay. All 37,105 stored pre-union event tiers and 4,000 saved final recovery decisions agree with the original rule, across 14,835 baseline group files and 2,000 paired trials. Old R and its bootstrap interval reproduce 003. Reference dips gained 13, lost zero. Across all depths, dips 394 to 496 and bumps 400 to 483. Background real 123 to 176, flips 70 to 85. The counting allowance is 86.85 and each paired 99% interval includes zero. Full tables follow in the final report.
