# X2: orbit vouching, prototyped and rejected (Fable, 16 Nov 2026; bench copy)

**Verdict in one line: found nothing to adopt. Orbit vouching as designed in F4 FAILS its own pass rule: it frees 19 planets (+1.9 points of P) but promotes 16 upside-down events and 52 real ones on the untouched background, where the rule allowed 2 upside-down. Two strong, lightly flagged events on the same star are common by chance. Its price (1.2 planets per upside-down alarm) is five times worse than the dump-shape rule.**

## What was tested
Rule fixed in `F4-VETTING-VOUCHING.md` section 3 before any number, with two stricter changes forced by the saved event lists (written in `WORK-LOG-X2.md` before the run): an event at SNR 7 or more that is held ONLY by soft flags (dump or gap edge, ramp, dominated; depth cap respected) is promoted to tier 1 when the same star and arm has another primary-product event at SNR 7 or more that is tier 1 or soft-held, at least 3.5 binary periods away, not within 1 hour of a whole number of binary periods, with depths within a factor 2.
Scorer: `data/fable/f4/x2_prepare.py`, `x2_score.py`, `x2_summary.py`; same identity checks as F4 (all 1,098 trials verified, B reproduces 174 / 79).

## Result (CONFIRMED as computed), planets that can exist
| Rule | Planets found | P % | Change against B (95%) | Real alarms | Upside-down alarms |
|---|---|---|---|---|---|
| B + depth cap | 465 | 48.31 | -0.10 | 124 | 53 |
| + vouching | 484 | 50.25 | +1.84 (+0.88 to +2.92) | 176 | 69 |
| B + cap + R2 | 491 | 51.02 | +2.61 (+1.57 to +3.73) | 158 | 63 |
| + vouching | 502 | 52.14 | +3.73 (+2.49 to +5.04) | 195 | 77 |
| All soft flags released (for scale) | 524 | 54.42 | +6.01 (+4.48 to +7.63) | 263 | 111 |

Pass rule: promoted upside-down at most 2 (measured 16: FAIL); promoted real at most 2.3 x 2 + 5 = 9.6 (measured 52: FAIL); planets at least +1.0 with interval above zero (PASS).

## Why it fails
The work log predicted the risk by arithmetic before the run: about 225 real and 100 upside-down events are tier 1 or soft-held over about 650 stars, and they cluster on a few busy stars, so chance pairs are common. The pair test has no power for two events: any two times fit some planet period. RS-037's small null rate (0.15%) was measured only at the true planet times, not over all pairs a search would try.

## What would have to change (NOT TESTED)
- Three events, not two, with the times required to fit one circumbinary orbit: that has real power, but only about a quarter of the held planets have three scored crossings.
- A voucher that is itself tier 1 (clean), not soft-held: fewer chance pairs, fewer planets. The saved outputs in `data/astra/fable-f4/x2-planets-*.json` hold every flag needed to price this without a new run.
- The last row of the table is the ceiling of everything behind the soft flags: +6.0 points for 139 more real and 58 more upside-down alarms. There is no cheap way to it.

## The other F4 design
The three-signal dump hold (shape, star-position jitter, cross-star moment) was not built: it needs star-position data per event, which the saved event lists do not carry. It stays a design with its pass rule in F4 section 2.

## Fresh bench
Not run for vouching: it failed on the alarm side, which does not depend on the planted planets.
