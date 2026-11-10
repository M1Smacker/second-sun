# Step 1 result (10 Nov 2026, Sonnet 5.5 Extra): which book sentences rest on a recovery test that skipped the mask's loss

**Plain verdict: 16 places in the book quote a "floor", a "found X percent" or a "hidden by eclipses" number from tests that built the eclipse mask from CLEAN light or injected the fake dip after the mask. None of them can see the loss measured in Part A. Nothing was changed in the book; this is the worklist for the one book correction (step 5).**

Labels: CONFIRMED = I read the code line that decides the order. LIKELY = inferred from the report text, code not opened. NOT CHECKED = said so.

## How each test builds the mask (CONFIRMED from the code, 10 Nov)
| Test | Where | Mask built from | Injection | Counts as "after" (blind to the loss)? |
|---|---|---|---|---|
| Lab 6 | `labs/lab6_fake_planets.py` line 10 and 28 to 29 | `eclipse_mask_auto(t, f, 14.6086)` on the CLEAN light, `keep` reused on the injected light | `fi = f * transit(...)`, then `find_events(t[keep], fi[keep])` | YES |
| STANLEY realistic test (Chapter 8 and 9, F-029) | `pipeline/recover_cbp.py` line 21 | `eclipse_mask_auto(t, f0, PBIN)` on the clean `flux_orig` ("as the real search would") | injected light is cut with that `keep` | YES |
| Whole-chain test v7 (F-088, F-089, 4 Nov numbers) | `pipeline/chain_recovery.py` lines 1 to 7, 38 to 49 | the frozen `S2.prepare` runs first; the fake dip is added to the PREPARED (masked, windowed) flux | after the mask | YES |
| First injection test (S98, 7 times, F-015) | `research/overnight-science/report.md` section 3 (before section 10 introduced the auto mask) | a hand mask from the known eclipse widths (4.7 and 6.1 h) | after the hand mask | LIKELY NOT AFFECTED by the auto-mask loss, but it tested a different mask from the one the hunts used. Code not opened (no script is saved beside the report) |

## The sentences (file, what it says, test behind it, proposed handling)
Handling codes: **U** = add "upper limit, measured before the mask problem was found" and a pointer; **S** = scope sentence only (the statement stays true); **R** = rewrite the sentence.

| # | Place | What it says | Test behind it | Handling |
|---|---|---|---|---|
| 1 | `book/docs/book/09-fake-planets.md` lines 68 to 74 (table in 9.5, "Three different tests agree ... reliably finds ... 6 Earth radii") | the floor is 6 Earth radii | all three tests above | R |
| 2 | same file line 94 (9.6 "We can say") | "nothing bigger than about 6 Earth radii ... about 1 crossing in 11 hidden by eclipses" | clean-light mask | R |
| 3 | `book/docs/book/08-our-detector.md` lines 74 to 75 (Figure 8.3 caption), 130 to 135, 181 | v2 reaches 6 Earth radii; "same floor as before"; single-sector floor about 6 Earth radii | `recover_cbp.py` | U |
| 4 | same file line 103 | smallest planet in one crossing below 10 Earth radii for 143 of 549 stars; "the hidden dip came back in 73% of sectors" brighter than magnitude 11 | noise-based table from the G1 run; which injection order the 73% used: NOT CHECKED | U (flag as ceiling) |
| 5 | `book/docs/labs/lab6-fake-planets.md` lines 41, 49 to 50 | "6 and 8 Earth radii: found every time"; "Loads sector 98 and masks the stars' eclipses" | Lab 6 script (CONFIRMED after-type) | U |
| 6 | `book/docs/labs/lab9-your-star.md` line 48 | "no single crossing bigger than roughly 5 to 6 Earth radii (Chapter 9's floor) in the unmasked 80%" | borrows Chapter 9's floor | U |
| 7 | `book/data/path.yml` line 117 (story, F-015) | "found 5 times in 7 ... nothing bigger than about 6 Earth sizes crossed here" | first injection test (hand mask, LIKELY not affected) but quoted as the search's floor | S |
| 8 | `book/docs/parts/part3/review.md` line 35 | "roughly nothing bigger than ~6 Earth radii for a TOI-1338-like star" | same | S |
| 9 | `book/docs/field-notes/2026-10-20.md` lines 11, 19, 34 | 6 Earth radii floor; "3 of 33 crossings were lost inside the stars' eclipses"; "a 9% hidden loss inside eclipses" | recover_cbp (clean-light mask): the 9% is the share the CLEAN mask removes, not the loss for a dip present while the mask is built | U |
| 10 | `book/docs/field-notes/2026-10-29.md` lines 13, 41 (F-088, F-089) | chain recovers at most 44% to 64% of very deep dips; half at about 11 times the noise; a dip and its mirror bump pass the chain "almost equally" | `chain_recovery.py` (after-type). The dip-versus-bump equality is true AFTER the mask only; Part A shows the mask removes dips and not bumps | U, and a sentence that the equality does not hold through the mask |
| 11 | `book/docs/field-notes/2026-11-04.md` lines 19, 47 to 49 | "found and kept 44% of the time", "Jupiter-size dip kept about 60%", reach map | `chain_recovery.py` and Horizon | U (already says the reach map is "too generous" for transit chance) |
| 12 | `book/docs/learn/index.md` line 129 | repeats 60% and 6% | same | U |
| 13 | `book/docs/field-notes/2026-11-03.md` line 26 | the faint list tests only large planets (smallest planet above 10 Earth radii in two thirds of star-sectors) | noise-based, ignores the mask; the true reach is even smaller | S |
| 14 | `book/data/claims.csv` rows F-015, F-029, F-048, F-088, F-089 (and F-078 already labelled a ceiling) | the numbers above | see the table | U (move to LIKELY, upper limit) |
| 15 | `book/data/claims.csv` row F-057 (SAP versus PDCSAP on S98, 6 Earth radii 2 of 7 against 0 of 7) | a comparison of two products | injection order NOT CHECKED | check before touching |
| 16 | `book/docs/book/08-our-detector.md` and Chapter 9 prose that cites F-015 or F-029 elsewhere | repeats | not grepped line by line | cover by the claim relabel |

Not found in the book (grep 10 Nov): any sentence quoting K50 or K90 by name. The reach map (Horizon) appears in five more places, all read: `field-notes/2026-11-03.md` line 16 (already labelled an upper bound, scope fine), `field-notes/2026-11-04.md` line 47 (row 11), `learn/index.md` line 131 (quiz check 10 asks for the likeliest reason a map says 13 to 22 planets and none were found: the answer should gain a third reason, the mask, S), `index.md` line 12 (home recap: "four nulls ... cannot test [Kepler's rate]": still true and now stronger, no change), `versions.md` line 108 (history row, no change).

## Findings the correction note must carry (all CONFIRMED by script, Part A and the mutation test)
- The auto mask removes dips present in the light while it is built; fakes added afterwards never see it. TOI-1338 itself: found 0.58 before against 0.95 after (K-05).
- A dip and a bump differ at the mask: bumps are not removed. So the "mirror bump is recovered equally" statement is only true downstream of the mask.
- The hand-mask first test (F-015) is probably still valid for the hand mask; it is not the mask the hunts used.

## Mutation test of the Part A harness (CONFIRMED, closes the open item in WO-F01-PART-A-RESULT)
Script `scripts/wo_f01a_mutation_test.py`, output `evidence/wo_f01a_mutation_test.txt` (G2, 6 files per period bin and product family, 58 usable files, 138 s). Three checks: T1 the loss is visible in the two slowest bins, T2 a deep dip is found after the mask in every bin, T3 bumps agree before and after.
- Unmodified copy: dips K 25 before/after 0.75/1.00, 0.27/1.00, 0.08/1.00, 0.00/1.00, 0.02/1.00 by bin (close to the 100-file run, 0.66, 0.26, 0.07, 0.01, 0.02); bumps 1.00/1.00; T1, T2, T3 all PASS.
- Mutant A (dip injected after the mask in the "before" case): before = after everywhere; T1 FAILS, as it should.
- Mutant B (injection sign flipped): found about 0.00 to 0.07 everywhere; T1 and T2 FAIL.
- Mutant C (bump injected as a dip in the "before" case): bumps before 0.00 to 0.08 against 1.00 after; T3 FAILS.
So each check can go red, and the real Part A numbers are not a constant of the harness. Caveat: 58 files, so each cell has 8 to 12 files; this shows the checks react, not the size of the effect.
