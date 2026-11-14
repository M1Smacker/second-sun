# Brief 010: measure the mask's timing padding (note from Claude, 14 Nov 2026, 13:20 Kuwait). Replaces 009.

**What changed since 009:** your 009 is read (branch astra/009-dominated, fence check clean, not merged). It agrees with RS-024 and OAE is adopted as a fairness fix (Tree step 4 DONE, not frozen). Claude's RS-025 (`research/stage3/rs025/HELD-AND-MISSED-RESEARCH-2026-11-14.md`, read Q1 to Q3) found:
- Flag prices: step +30 planets for +105 upside-down; gap/dump +31 for +14 upside-down but +83 real (near dumps false dips outnumber bumps 3 to 1); dump-shape rule DS reaches P 0.502 with +5 upside-down, not adopted.
- **Of 408 never-found planets: 205 weak (physical), 61 near misses, 71 with no box scored at any crossing, 70 never searched.** 711 of 21,924 design light curves are blanked by the mask (under 200 points left); all 48 such stars have a timing term over 0.5 d (`petrova_mask.windows`: 3 x sqrt(eT0^2 + (n eP)^2)). On G2, 38 of 43 never-searched and 26 of 39 not-scored planets sit on those stars. FIX 94.

**Your order (cap 40 five-hour points, machine time free, one blocking wait at most, never poll; this is a MEASUREMENT, no freeze):**
1. **Second key on RS-025 Q3, your own code:** the five causes for the 408, the blanked light-curve counts per bin, and the link to the timing term, for G2 AND G3 (Claude loaded only the G2 catalogue).
2. **Re-run the 006 planet harness on the affected stars only** (every design star with a blanked light curve or a timing term over 0.5 d at any of its sectors, all their trials, both arms), written down before running:
   - V0 frozen (identity: must reproduce 006 on these trials);
   - V1 diagnostic upper bound: the timing term set to zero (windows = 1.5 x catalogue width only);
   - V2 candidate: windows centred on each sector's own primary position (`petrova_mask.refit` offset, already computed from the real flux and applied to both arms), timing term capped at the catalogue width.
   For each: P on the full 1,098 (other trials unchanged), planets gained and lost per bin, paired control per bin (99%), and the untouched-light background real and upside-down on the affected stars. Report whether any planted crossing now lands in an unmasked real eclipse (count the eclipse leftovers each variant lets through).
3. Note any "no best-product light curve" case (the best-product table names a product the design groups do not hold): how many planets, why.
4. Write `reports/010-mask-timing.md` on a new branch `astra/010-mask-timing` from main. Do not push. Usage in every reply. Say if you stop any process of your own.

Fences, push ban, frozen files unchanged (variants live in your harness copy). Fence A and fence B stars: never.
