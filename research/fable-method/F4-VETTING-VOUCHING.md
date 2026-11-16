# F4: which guard flags cost planets, and what to do about it (Fable, 16 Nov 2026; design plus one measured price list, nothing adopted)

**Verdict in one line: the hold that loses the most planets for the fewest prevented false alarms is the thruster-firing ("dump") hold. Releasing it by shape (the DS rule) frees 18 planets (+1.9 points of P) for 3 more upside-down alarms; no other flag comes close. The step flag holds even more planets (23) but stands in front of 113 upside-down alarms, so it cannot be released, only replaced by a better test. Four guards (repeater, common moment, mirror match, near-eclipse) hold zero planets and should be left alone.**

## 1. The price list (CONFIRMED as computed)
Method: a private copy of Codex 023's scorer (`data/fable/f4/f4_prepare.py`, `f4_score.py`, `f4_summary.py`) scored the same 1,098 planted planets and the same untouched background 12 more times, each time with ONE guard flag no longer able to hold an event at tier 2. Everything else is the adopted set B with the depth cap (FIX 96). The copy keeps 023's identity checks: B and DS match the saved outcomes on all 1,098 trials, background 174 / 79 and P 48.11 reproduce exactly.

Change against B with the depth cap (124 real / 53 upside-down), planets that can exist (968):

| Flag released | Planets freed | Points of P (95%) | Real alarms added | Upside-down alarms added | Planets per upside-down alarm |
|---|---|---|---|---|---|
| Dump hold, by shape (DS) | +18 | +1.89 (+1.06 to +2.79) | +19 | +3 | 6.0 |
| Dump hold, fully | +19 | +1.98 (+1.13 to +2.92) | +46 | +5 | 3.8 |
| Gap-edge hold | +8 | +0.82 (+0.31 to +1.41) | +14 | +5 | 1.6 |
| Dump and gap-edge, fully | +27 | +2.80 (+1.78 to +3.91) | +61 | +12 | 2.3 |
| Ramp | +13 | +1.32 (+0.66 to +2.09) | +15 | +11 | 1.2 |
| Dominated (a stronger event nearby) | +15 | +1.54 (+0.82 to +2.33) | +26 | +24 | 0.6 |
| Step | +23 | +2.39 (+1.41 to +3.41) | +155 | +113 | 0.2 |
| Step and ramp together | +36 | +3.71 (+2.51 to +4.99) | +183 | +143 | 0.25 |
| Eclipse overlap | +3 | +0.32 (0.00 to +0.72) | +2 | 0 | free, tiny |
| Near a catalogue eclipse (c5) | 0 | 0 | +20 | 0 | holds no planets |
| Repeater | 0 | 0 | +7 | 0 | holds no planets |
| Common moment (cross-star) | 0 | 0 | +16 | +5 | holds no planets |
| Mirror match | 0 | 0 | 0 | +1 | holds no planets |

How to read it:
- **Planted dips and planted bumps move together in every row** (for example DS +18 dips, +16 bumps), so the test planets are treated alike on both arms. The alarms are not: the dump hold, c5 and the repeater release far more real events than upside-down ones. Those guards are catching dips that have no mirror (pointing dips, eclipse leftovers), which is their job.
- Single-flag pool: step 23, ramp 13, dominated 15, dump and gap 27, eclipse overlap 3: about 80 planets, 8 points, if every hold were free. RS-037's 11.6 points also counts planets held by two flags at once. The part that can be harvested at a fair price is about 2 to 4 points.
- **Correction to RS-037's ranking:** it listed step (49), gap edge (34), ramp (33) and repeater (32) as big planet holders on the older chain. Under B the repeater holds zero planets, and step is by far the most expensive to touch.

## 2. Design (a): replacing the blanket dump hold
What the list says about the idea "use the cross-star flag instead of the dump hold": that is exactly the row "dump hold, fully" (the cross-star flag stays on). It lets 46 real events through for 5 upside-down. So **the existing cross-star flag does not replace the dump hold** (CONFIRMED). The shape rule DS does better (19 real for 3), and RS-038 measured that star-position jitter alone separates only partly (a cut at J 8 removes about 27% of dump false alarms and 11% of planted dips).

Proposal, three signals, hold a dump-time event if ANY fires (same code on both arms):
1. uneven shape (DS as benched: light before or after the dip differs by more than 0.25 of the depth);
2. star-position excursion J of 8 or more during the event (RS-038 metric, fixed there before its run);
3. cross-star moment at 0.03 d counted over ALL stars of the campaign on that sector and camera, at SNR 5 or more, either sign (today's flag only sees stars that produced events; the full G1 list gives more neighbours).

Pass rule, written before any run (against B with the depth cap, fresh planet bench):
- planets: paired change at least +1.5 points with the 95% interval above zero;
- upside-down alarms added: at most 3; real alarms added minus 2.3 x upside-down added: at most 5 (DS alone is at 19 - 7 = 12, so signals 2 and 3 must remove about 7 dip-only events to pass);
- a planted dip is lost to signal 2 only when the REAL star-position data at the planted time shows the excursion (fair bench, RS-038);
- zero-planet identity: events with no dump note are unchanged.
Honest expectation (LIKELY): signals 2 and 3 cut the dip-only events by a quarter to a half and cost 1 to 3 of the 18 planets. It may fail the real-alarm line by a little. If it does, the choice goes to Ahmed: accept about 10 extra dip-only leads near dumps (each then needs a pixel check by eye) for +1.9 points, or keep the hold.

Second, cheaper candidate (NOT TESTED): shorten the pre-dump window after Sector 56, where the release notes say the one dump per orbit happens before data collection resumes (RS-038). It needs the per-era split of the 18 planets and the 19 alarms, which the saved outputs in `data/astra/fable-f4` already contain.

## 3. Design (b): orbit vouching
Idea (RS-037): a held dip is promoted when a second crossing of the same planet exists. Fixed here before any measurement:
- **Who can be vouched for:** an event at SNR 7 or more held ONLY by soft flags: dump, gap edge, ramp, dominated. Never step, common moment, mirror match, c5, eclipse overlap, repeater or too deep: the price list shows those stand in front of the false alarms.
- **Who can vouch:** a second event on the same star, any sector or product, SNR 5 or more (not 4: RS-037 found the no-planet score has a heavy tail), itself not at a common moment and not a mirror match.
- **Orbit test for the pair:** (i) separation not within 1 hour of a whole number of binary periods (that is the binary, not a planet); (ii) separation at least 3.5 binary periods (stable planets do not come closer); (iii) depths within a factor 2; (iv) each length no longer than the longest crossing the binary allows; (v) with three or more candidates, the times must fit one circumbinary orbit of the 006 kind within 0.2 d.
- **Pass rule:** run the identical rule on the upside-down arm of the untouched background. Promoted upside-down pairs at most 2 in the whole background, promoted real pairs at most 2.3 x that plus 5, planets paired change at least +1.0 point with interval above zero, fresh-seed confirmation, zero-planet identity for stars with fewer than two events.
- **Ceiling (LIKELY):** soft flags alone hold about 55 planets (5.6 points). RS-037 found a second crossing at score 4 or more for about half of the held pool, fewer at 5. So about 2 to 2.5 points before the orbit test, less after. NOT TESTED: the false-alarm side, which decides it.
- Cost: no orbit grid is needed for pairs (rules i to iv are arithmetic), so this is a scoring change, cheap to bench with the 023 machinery.

## 4. The step flag: the largest pool, the hardest
23 planets (2.4 points) sit behind it, and 113 upside-down alarms. mono-cbp replaced its step flag by a model comparison (transit, sinusoid, line, two-part step, by AIC) and still loses long transits there (RS-038). A replacement here would have to keep at least 95% of the 113 to be worth 2 points. Recommendation: a study after 1.1, not a 1.1 lever.

## 5. Quality bits and planted crossings (the brief's last question)
Answered in F2 (`F2-SILENT-LOSSES.md`): yes. 404 planted crossings with raw data are removed at load, 269 of them by the scattered-light bit (value 4096), and the same bit removes 175 more in QLP through the safe windows.

## 6. Order of work I recommend
1. DS with the two extra signals (section 2), benched under its pass rule: the only vetting lever with a good price.
2. Vouching limited to soft flags (section 3): cheap to bench, about 2 points at most.
3. Leave repeater, common moment, mirror match and c5 untouched. Do not release step, ramp or dominated.
Together with F1's candidate this puts a realistic Petrova 1.1 at about P 0.52 to 0.55 (LIKELY), not near 0.75.

## Labels
CONFIRMED: the price list (computed, identity checks passed). LIKELY: expectations in sections 2 and 3. NOT TESTED: the three-signal hold, vouching, the shorter window.
