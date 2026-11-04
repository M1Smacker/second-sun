# RS-010 Q1: how many planets should our hunts have found, and what does Census need? (night of 4 Nov 2026; research stint RS-011; nothing in Petrova changed)

Method (`research/stage3/census_step1/q1_expected.py`, full output `q1-expected.txt`): expected detections E = (occurrence per star in a cell) x (Horizon sum of detection chance in that cell), added over the cells the occurrence anchor covers. Horizon = `pipeline/horizon_reach.py`, rule R0 unchanged (main scenario: stability floor 5.6, no dilution). Sources opened: Armstrong et al. 2014 (abstract and ar5iv full text), Oddo et al. 2026 (abstract and arXiv HTML full text).

## Plain verdict
**On paper our three hunts should have found planets if the Kepler rate applied. They found none. So one of the numbers is wrong, and the most likely culprit is our own reach map, which leaves out a geometry factor.** This is not a finding about planets.

- Armstrong et al. 2014 give 10.0 (+18, -6.5)% (95% limits) for planets above 6 Earth radii with periods under 300 days, if planets are coplanar with their binaries (abstract, CONFIRMED). Spread over the 6 to 16 Earth radius and 13 to 250 day cells, our G2 development, G2 sealed and G3 searches together would expect **13 to 22 detections** (Horizon unchanged, g = 1). Seeing none would then have a chance around one in a million. Taken at face value that would mean the true rate for our kind of binary is under about 1% to 2%, far below Kepler's 10%.
- That cannot be taken at face value. Horizon counts the chance that a transit falls inside the observed days (window function W = covered days over period) but **not the chance that the planet transits at all**. Oddo et al. 2026 do include it: their completeness is the window function times recovery, they say the window function falls with "the decreasing geometric transit probability", and that a planet aligned with a binary which is itself tilted to our view "is unlikely to transit" (HTML text read, CONFIRMED). Horizon's code has no such term (`W = min(1, covered_d / P)`, CONFIRMED in the file). Our earlier note that g is "near 1 for coplanar planets" (`horizon-literature-2026-11-03.md`, section 3) was an unchecked assumption and looks wrong at long planet periods.
- Cross-check from Kepler itself (LIKELY): Armstrong's sample was 1,735 Kepler binaries and 7 known systems gave the 10%; so 4 to 7 detections divided by 0.10 means Kepler's whole sensitivity for this region was only about 40 to 70 star-equivalents (which of the 7 planets exceed 6 Earth radii is from memory, UNCERTAIN). Horizon says our three hunts alone hold 135 to 223. Four years of continuous Kepler data on 1,735 binaries should beat 1 or 2 sectors on about 1,500 stars, not trail them by a factor of 2 to 5. So Horizon is over-generous, very probably by several times.

## Numbers (CONFIRMED as arithmetic on our files; how the rate is spread over cells is my assumption)
Rule A spreads the 10% evenly over all 30 cells (5 radius bins from 7 to 15 Earth radii x 6 period bins from 13 to 250 days, even where no star could be stable); rule B only over the 15 cells where at least half the stars are allowed; rule C puts it in the four cells at 6 to 10 Earth radii and 77 to 139 days. E at g = 1:

| set | stars | rule A E | rule B E | rule C E |
|---|---|---|---|---|
| G2 sealed | 594 | 7.0 | 11.6 | 10.1 |
| G2 development | 301 | 3.4 | 5.6 | 4.6 |
| G3 | 612 | 3.1 | 5.1 | 3.0 |
| all three | 1,507 | 13.5 | 22.4 | 17.7 |

(G1 has no reach map.) At the low end of Armstrong's range, 3.5%, the three sets together give 4.7, 7.8 and 6.2.

With a geometry factor g applied (my range, NOT looked up: for a planet at about 10 binary periods the allowed tilt is roughly a_bin/a_planet = 0.2 to 0.3 of the binary's, plus the binary's own tilt):

| g | E at 10% (rule A / B) | chance of none (A / B) | 95% ceiling on the total rate from our zero (A / B) |
|---|---|---|---|
| 1 | 13.5 / 22.4 | 0.0% / 0.0% | 2.2% / 1.3% |
| 0.5 | 6.7 / 11.2 | 0.1% / 0.0% | 4.5% / 2.7% |
| 0.25 | 3.4 / 5.6 | 3.4% / 0.4% | 8.9% / 5.4% |
| 0.1 | 1.3 / 2.2 | 26% / 11% | 22% / 13% |

So with g between 0.1 and 0.25 our null is unremarkable to mildly surprising, and our three hunts together could not have excluded Kepler's 10% (they reach a ceiling of 9% to 22%). With g = 1 they would have excluded it, which no honest reading allows.

## What Census needs (the decision this feeds)
Stars like the G2 sealed set (bright, 2-minute data, about 0.12 star-equivalents per star in this region) needed to push the 95% ceiling on the total rate down if nothing is found:

| g | ceiling 10% (A / B) | ceiling 5% (A / B) | ceiling 3.5% (A / B) |
|---|---|---|---|
| 1 | 254 / 153 | 509 / 307 | 727 / 438 |
| 0.5 | 509 / 307 | 1,018 / 614 | 1,454 / 877 |
| 0.25 | 1,018 / 614 | 2,036 / 1,227 | 2,908 / 1,753 |

(The output file prints the last column as "3%"; it is 3.5%.) At g = 0.25, **about 1,000 G2-type stars is the size at which a null first tests Kepler's central 10%, and about 2,000 to 3,000 would test the low end of its range.** That fits the Census size Ahmed asked for (over 1,000, likely several thousand) and says the stars should be bright with 2-minute data, because star-equivalents per star decide it (G3's faint stars gave about a fifth of that per star). With 1,000 G2-type stars the expected number of detections at the central rate is about 3 at g = 0.25 (rule A), so a real planet is more likely than not to appear if Kepler's rate holds.

## Plan changes
1. New build item T138: add the geometric transit probability to Horizon (needs the transit-geometry formula from Martin and Fabrycky or Armstrong 2013, to be opened, and each binary's inclination from the eclipse data), re-run all three maps and redo this note. The reach numbers quoted so far (about 87 and 18 to 20 star-equivalents, the 3.4% ceiling) are upper bounds that probably shrink by a factor of 3 to 10. The ranking of pools by value is probably unchanged because g affects them in the same direction (NOT tested).
2. Do not present Horizon ceilings as limits on planets until T138 is done. The book already calls them upper bounds; its wording needs a check (follow-up fix item).
3. For Census the target is "bright, 2-minute, long coverage"; planet-count targets come from the table above, after T138.

## Labels
- CONFIRMED: Armstrong abstract numbers; Oddo includes a geometric transit probability that falls with period; Horizon's W has none; all E and ceilings as arithmetic on our reach files.
- LIKELY: Horizon is over-generous by several times (Kepler cross-check); Kepler's sensitivity of 40 to 70 star-equivalents.
- UNCERTAIN: the size of g; how the 10% spreads over cells; whether Armstrong's rate applies to our binaries and in which direction (the paper says its rates are "skewed towards these shorter period binaries" and that all known planets orbit binaries above 7 days, full text read); the exact count of the 7 planets above 6 Earth radii.
- NOT TESTED: g from first principles; the effect of later vetting (real planets can fail checks); Gaia or other binary populations.
