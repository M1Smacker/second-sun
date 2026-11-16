# X6: a release rule for the guard flags (Fable, 16 Nov 2026; bench copy, nothing adopted)

**Verdict in one line: under the rule written before scoring, the proposal is R2 (dump hold by shape plus the gap-edge hold released, with the depth cap): +26 planets, +2.7 points of P (95% +1.7 to +3.8), background 158 real / 63 upside-down, both under B's 174 / 79. The larger rule R1 (R2 plus the ramp hold released) frees +45 planets, +4.7 points (+3.3 to +6.1) and stays inside the upside-down limit (78 of 79), but its real alarms rise to 193, over the 174 limit, so it FAILS the rule I wrote. Whether the real-alarm limit should bind is Ahmed's call.**

The price of each single flag is in `F4-VETTING-VOUCHING.md` (section 1). This file is the second half of X6: the combined rule.

## What was fixed before scoring (`WORK-LOG-X6.md`, 11:34 am)
- R2 = depth cap + dump hold by shape (DS) + gap-edge hold released.
- R1 = R2 + ramp hold released.
- R3 = R1 + eclipse-overlap hold released.
- Step and dominated stay: their price is far too high (F4).
- Pass: untouched background upside-down at most 79 AND real at most 174; paired gain in P against B on planets that can exist with its 95% interval above zero; planted dips and bumps both rise. The passing rule with the most planets is the proposal.

## Result (CONFIRMED as computed; same scorer copy as F4, identity checks passed on all 1,098 trials, B reproduces 174 / 79 and P 48.11)
Planets that can exist (968); alarms on the untouched background.

| Rule (all with the depth cap) | Planets freed | P | Change against B (95%) | Real alarms | Upside-down alarms | Passes? |
|---|---|---|---|---|---|---|
| B today (no cap) | | 48.40 | | 174 | 79 | |
| Depth cap only | -1 | 48.31 | -0.10 | 124 | 53 | |
| DS only (F1 candidate, without mask timing) | +18 | 50.20 | +1.89 (+1.06 to +2.79) | 143 | 56 | yes |
| **R2** | **+26** | **51.02** | **+2.71 (+1.70 to +3.79)** | **158** | **63** | **yes** |
| R1 | +45 | 52.95 | +4.65 (+3.32 to +6.10) | 193 | 78 | no: real 193 over 174 |
| R3 | +48 | 53.27 | +4.96 (+3.59 to +6.46) | 195 | 78 | no: real 195 over 174 |

Planted bumps rise with planted dips in every row (R2 +24, R1 +46, R3 +49), so the test planets are treated alike on both arms.

## Reading
- Flags overlap. Releasing gap edge and ramp together frees 45 planets, more than the 39 the single prices add up to, and also more alarms (25 upside-down against 19). Single-flag prices understate both sides.
- R1 is the largest fair step available in the vetting pool: it uses the whole upside-down budget the depth cap frees (53 back up to 78) to buy 4.7 points. It passes Tree rule 1 as the Tree words it (upside-down only). It fails once real alarms are also limited, which F1 argues they should be, because the extra real events are mostly dips with no mirror.
- The choice for Ahmed, in plain terms: **R2** = +2.7 points and a cleaner list than today on both arms. **R1** = +4.7 points, upside-down as today, about 19 more real events to look at than today (193 against 174). There is no version that gives R1's planets at R2's price.
- Winner's curse: three rules were scored on one bench and the rule that picks among them was written first, so the bias is small; the fresh-seed bench (`X1-FRESH-SEED.md`) is the check.

## What this does to the Petrova 1.1 candidate
F1's candidate was B + cap + DS + mask timing (M2): about 51.7. Replacing DS by R2 (and by R1 as the upper case), with M2, is scored in `X10-COMBINED.md`.

## Not done
No guard was built for the gap-edge release (the F4 three-signal idea would apply to it too). No per-era split of the freed planets and alarms. The ramp flag was released whole; a narrower ramp rule might keep most of the 19 planets it adds at fewer alarms (NOT TESTED).
