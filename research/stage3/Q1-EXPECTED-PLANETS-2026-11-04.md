# RS-010 Q1: how many planets should our hunts have found, and what does Census need? (night of 4 Nov 2026; research stint RS-011; nothing in Petrova changed)

Method (`research/stage3/census_step1/q1_expected.py`, full output `q1-expected.txt`): expected detections E = (occurrence per star in a cell) x (Horizon sum of detection chance in that cell), added over the cells the occurrence anchor covers. Horizon = `pipeline/horizon_reach.py`, rule R0 unchanged (main scenario: stability floor 5.6, no dilution). Sources opened: Armstrong et al. 2014 (abstract and ar5iv full text), Oddo et al. 2026 (abstract and arXiv HTML full text).

> **READ THE UPDATE AT THE END FIRST.** After this was written, the geometry factor was looked up (Martin and Triaud 2015) and probed on every star. It is about 0.05 to 0.2, so the 13-to-22 tension below mostly disappears: the null is consistent with Kepler's rate, and our hunts could not have excluded it. The body below is kept as written (the first pass).

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

## UPDATE (same night, after opening Martin and Triaud 2015): the geometry factor is looked up and probed

Sources opened (arXiv full text): Martin and Triaud 2015, "Circumbinary planets - why they are so likely to transit" (arXiv:1501.03631, abstract and Section 4 read); Oddo et al. 2026 section V.2 (window function and binary inclination from the eclipse width and depth, Eq. 7 and 8). Script `census_step1/t138_geometry_probe.py`, output `t138-geometry-probe.txt`. Exploratory and report-only: Horizon rule R0 is NOT amended by this (T138 does that, with Ahmed's OK).

**CONFIRMED (text read):** for a coplanar planet around a randomly oriented binary the probability of transitability is R/(a_p - a_A) (Martin and Triaud Eq. 26), the same as Welsh et al. 2012; it is almost period-independent, and it rises steeply with a little mutual inclination (their example: certain eventual transit at 1 AU around a 0.3 AU eclipsing binary if the mutual inclination exceeds 0.6 degrees). **LIKELY (my step from their Eq. 26, not checked against the known systems):** for a binary that is known to eclipse with impact parameter b (in units of R_sum, from the eclipse width as in Oddo Eq. 7 and 8), an exactly coplanar planet transits star A if b < R_A a_b / (R_sum (a_p - a_A)). The probe applies this star by star with the real eclipse width of every G2 and G3 star (width known for 1,392 of 1,507) and sums Horizon's detection chance only where the condition holds.

**Result (R_sum is the one unknown that matters; a_A = a_b / 2, total mass 2 Msun as Horizon):**
| R_sum | effective g (G2 sealed / G2 dev / G3) | all three hunts at the central 10%: E (rule A / B) | chance of none (A / B) | 95% ceiling on the total rate (A / B) |
|---|---|---|---|---|
| 1.5 x R_A | 0.15 / 0.14 / 0.23 | 2.3 / 3.6 | 10% / 3% | 13% / 8% |
| 1.8 x R_A | 0.11 / 0.10 / 0.06 | 1.3 / 2.1 | 28% / 12% | 24% / 14% |
| 2.2 x R_A | 0.06 / 0.06 / 0.01 | 0.7 / 1.2 | 50% / 29% | 43% / 24% |

**What changes:**
1. The tension above (13 to 22 expected, none found) mostly disappears. With the geometry in, the three hunts expected about 1 to 4 planets at Kepler's central rate and had a 3% to 50% chance of finding none. **Our null is consistent with Kepler's 10%.** It also could not exclude it: the 95% ceiling on the total rate for planets above 6 Earth radii inside 300 days is 8% to 43% depending on R_sum, above Armstrong's 3.5% to 28% range centre.
2. My guessed g of 0.1 to 0.25 in the tables above was in the right range (the probe gives 0.05 to 0.23), but it was a guess then and is a probe now. The Kepler cross-check (Horizon 135 to 223 star-equivalents against Kepler's 40 to 70) is explained by this factor, not by a defect in the recovery tables (LIKELY: with g the Horizon sums fall to 15 to 36).
3. G3 loses most because its stars are bigger (median TIC radius 1.64 against a smaller G2 set) and the effect compounds with the R_sum assumption; effective g for G3 drops to 0.01 at R_sum = 2.2 R_A. The R_sum guess (the companion's size) is the largest unknown. A real value per star needs the eclipse depth ratio or the TIC radii of both stars (T138).
4. Census sizing (rule B / rule A, R_sum = 1.5 to 1.8): to push the 95% ceiling on the total rate down to 10% needs about 1,000 to 2,400 stars of the G2-sealed kind; to 5%, about 2,800 to 4,800; to 3.5%, about 4,000 to 6,800. If the 10% rate is real, 2,000 such stars would expect about 3 to 4 detections (chance of none about 2% to 8%). So Census at 2,000 or more G2-type stars could both find planets and test Kepler's rate. At 1,000 stars it would find about 1 to 2.
5. Armstrong's 10% is for a sample dominated by shorter-period binaries; the paper says the shortfall around short binaries is real, so the rate for our long binaries may be higher (UNCERTAIN, direction only).

**NOT TESTED:** the condition against the known Kepler systems (Kepler-16, -34, -35, -38, -64, -413, -1647) which transit; a few degrees of mutual inclination (raises g, per Martin and Triaud); the transit of star B (adds some); eccentricity; masses other than 2 Msun in total.

## UPDATE 2 (same night): a few degrees of mutual inclination (`t138_incl_probe.py`, output `t138-incl-probe.txt`)
Adding a mutual inclination Delta between the planet's plane and the binary's (small-angle argument, my own, LIKELY; Martin and Triaud 2015 show transitability rises with it, Li, Holman and Tao 2016 find known systems within about 3 degrees of coplanar), the geometry factor at 77 to 139 days rises from 0.07 to 0.15 for R_sum = 1.8 and Delta = 0 to 3 degrees (0.13 to 0.28 for R_sum = 1.5; 0.05 to 0.08 for R_sum = 2.2). All three hunts at Kepler's central 10%:
| R_sum | Delta | E (rule A / B) | chance of none (A / B) | 95% ceiling on the total rate (A / B) |
|---|---|---|---|---|
| 1.5 | 0 / 1 / 2 / 3 degrees | 2.3 / 2.5 / 3.1 / 4.3 and 3.6 / 4.1 / 5.1 / 7.2 | 11% / 8% / 5% / 1% and 3% / 2% / 1% / 0% | 13% to 7% and 8% to 4% |
| 1.8 | 0 / 1 / 2 / 3 degrees | 1.3 / 1.4 / 1.8 / 2.4 and 2.1 / 2.4 / 2.9 / 3.9 | 28% / 24% / 17% / 9% and 12% / 9% / 5% / 2% | 24% to 13% and 14% to 8% |
| 2.2 | 0 / 1 / 2 / 3 degrees | 0.7 / 0.7 / 0.9 / 1.1 and 1.2 / 1.3 / 1.5 / 1.9 | 50% / 48% / 41% / 34% and 29% / 27% / 21% / 15% | 43% to 28% and 24% to 16% |
**Corrected reading:** in most of the grid the null is consistent with Kepler's rate (chance of none 5% to 50%). In the most optimistic corner (a small companion, 2 to 3 degrees of tilt, the 10% spread over stable cells only) the chance of none falls to about 1%, which would point to a lower rate around our binaries. The honest summary is a range, not "consistent": **the null is consistent with Kepler's rate unless several optimistic assumptions all hold together.** The book sentence was softened to match (2.9.10). Still not checked: the geometry condition and Delta on real systems (T138).

## UPDATE 3 (same night): G1 added (`census_step1/g1_reach.py`, output `g1-reach.txt`)
G1 (549 Kepler-field binaries, searched with an older Vesper than 0.8, so the 0.8 recovery table is generous for it, UNCERTAIN) has no per-star eclipse widths, so it gets the mean effective g of G2 sealed (0.15 at R_sum 1.5, 0.11 at 1.8). Its mean cell sum without geometry is 18.4 (rule A) and 29.9 (rule B), the Kepler-16 cell 13.8 and 12.3; with geometry it adds 2.0 to 4.5 to the sums, i.e. E of 0.2 to 0.45 at Kepler's 10%. All four hunts (2,056 stars) together, exactly coplanar: E = 2.5 and 4.1 (R_sum 1.5, rule A and B), 1.5 and 2.4 (R_sum 1.8); chance of none 8% and 2%, 23% and 9%; 95% ceiling on the total rate 11.9% and 7.3%, 20.5% and 12.3%. The Census numbers in `CENSUS-WORTH-2026-11-04.md` left G1 out, so "all hunts" there is low by 0.2 to 0.45 expected planets (a small shift, no change of reading).

## UPDATE 4 (4 Nov 2026, morning): Kepler-16 opened in the primary source
Source: Doyle et al. 2011, Science (arXiv:1109.3432), PDF fetched into `data\census_papers\` (334 KB, logged in downloads.csv) and read as text; Table 1 (stellar radii, binary semi-major axis, inclinations) did not come out of the PDF text, so the radii I used before are still remembered values (UNCERTAIN).
- **CONFIRMED (abstract and text):** the three bodies lie within 0.5 degrees of one plane; the text puts the binary and planet orbital planes within 0.4 degrees of each other. Supports the 0 to 3 degree tilt range used above for this system, and the low end of it.
- **CONFIRMED (text):** the planet's line-of-sight inclination changes by 0.2 degrees (precession), "large enough that transits are only visible from Earth about 40% of the time (averaged over 5 centuries)"; the transits across star A should cease in early 2018 and return around 2042. So even a planet that transits now is a snapshot: a time-averaged visibility factor of about 0.4 belongs on top of the geometry factor for systems like this one. This is a NEW point for T138 (our factor g is a snapshot; the chance that a planet transits during our 27-day look is further reduced by precession in the tilted cases, or raised by the chance that it will start to). LIKELY the same order of size for other systems, NOT TESTED.
- **CONFIRMED (text):** planet radius 0.7538 Jupiter radii, mass 0.333 Jupiter masses.
- **Consequence:** T138's check on the known planets now has one primary-source anchor (Kepler-16: coplanar within 0.4 degrees, transiting now, visible 40% of the time). The condition check with radii needs Table 1 (use the NASA Exoplanet Archive or the SOM) before it is quoted.
