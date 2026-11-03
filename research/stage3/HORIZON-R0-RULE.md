# Horizon R0: the rule, written BEFORE any injection runs and BEFORE the G3 result is opened (3 Nov 2026)

Status: **LOCKED by this commit.** A change needs a dated amendment at the bottom, never an edit above. Design: `HORIZON-DESIGN.md`. Reading behind it: `horizon-literature-2026-11-03.md` (RS-002), `open-items-closed-2026-11-03.md` (RS-005). Ahmed's words (3 Nov 2026): Horizon GO and cheaper, T107 first; the default radius range and the name Horizon stay; "Frozen 0.8.0" for G3 (so Horizon measures the 0.8.0 rules, run as Vesper 0.8.1, which behaves as 0.8.0).

## 0. What this is, in one line
Horizon measures how big a planet, how far out, the frozen search could have found, per cell, and turns a clean null into a ceiling per cell. **It is an upper bound on what the search could have seen, not a measurement of how common planets are.** Every page that shows it says so.

## 1. Grid (copied from Oddo et al. 2026, arXiv:2610.22625, for comparability)
- 7 planet-radius bins, uniform, 2 to 16 Earth radii (edges 2, 4, 6, 8, 10, 12, 14, 16). Neptune (3.9) to Jupiter (11.2) is marked on the map; nothing is dropped outside it.
- 7 orbital-period bins, log-uniform, 10 to 600 days (edges 10 x 60^(i/7)).
- Event duration is not a grid axis: it follows from the cell (section 5).
- Star brightness is not an axis; the noise of each star-sector carries it.

## 2. Star sets and the split
- **R1 (recovery, planted dips): the G2 DEVELOPMENT split only (301 stars).** The runner filters `slice == "dev"` and asserts 301 stars and no sealed star. The sealed G2 stars and their result are not touched.
- **Ceilings for G2 sealed and G3:** the recovery table of R1 is applied to the star-sectors of the set (their noise, windows and binary periods), without planting in their light. G3's own completeness table (`chain_recovery.py` after the search, G3 preregistration section 3) is reported beside it; if the two disagree by more than a factor of 2 at the same depth, both are shown and the map uses the G3 one.

## 3. The stability floor (a stated choice, with its sensitivity)
A planet is possible in a cell for a star only if its period is at least F times the star's binary period. **Published map: F = 5.6** (the smallest ratio observed among transiting circumbinary planets, Kepler-16 b at 5.57; the ten shortest observed ratios are 5.57 to 12.87, own table `horizon-research/h2_stability_numbers.txt`). Sensitivity maps: F = 3 (below the theoretical limit of 2.75 to 6.16 of Holman and Wiegert 1999 eq. 3 for e up to 0.3 and mass ratio 0.1 to 0.5) and F = 6.9 (seven of the ten shortest observed ratios lie below it; a pessimistic floor). Stars where the cell is below the floor add nothing to that cell's sum and are not counted as stars that "could have shown" it.

## 4. Geometry
Coplanar, circular planet orbits: the binary is an eclipsing pair, so the plane is edge on and a planet in that plane crosses a star at each pass. A planet at epoch T0 (uniform over one planet period) transits at T0 + k P; the transit is seen if a transit time falls inside the star-sector's good-time windows (section 7). That fraction, from folding the windows modulo the planet period, is the window function W(P) per star-sector. Isotropic planets (Martin 2018, abstract) are NOT in the published map; they get a second map only if time allows, labelled as a scenario.

## 5. Depth and duration of a planted dip
- Depth = (Rp / R_star)^2 with R_star the TIC radius of the star (`targets/host_radii_g2_g3.csv`; 822 of 895 G2 and 562 of 612 G3 positive). **Dilution assumption, stated: the crossed star gives all the light (no dilution).** This makes planets look easier to see than they are: the map is generous, the label says "upper bound". Sensitivity map: the crossed star gives half the light (depth halved). Stars with no valid radius use the median of the set (1.62 solar radii) and are counted separately.
- Duration = P_planet / pi x (R_star + Rp) / a, with a from Kepler's third law for a total mass of 2 solar masses (the same physics as the frozen eclipse-length rule, constants `ECL_MTOT`), capped to Vesper's box range (3 to 20 h). Circumbinary transits vary in timing and duration; the planting spreads duration by a factor drawn log-uniformly from 0.7 to 1.4 (stated, not tuned).
- Shape: trapezoid, 20% ingress and egress, as `chain_recovery.signal` (the frozen planting code, unchanged).

## 6. Recovery rule
Recovered = the planted dip is a **tier 1 event (1A, 1L or 1B) after all flags**, primary product, found by the whole frozen chain (search, second-product check, flags, SAP twin pass, v7 PDCSAP check, union, v7 flags) with `VESPER_OPTS=c6` and nothing else; SNR 7 or more; centre within the match window of the planted time. Exactly as frozen. No new switch, no new threshold. A run that plants nothing must recover nothing (control first).

## 7. Chance and ceiling
- Recovery fraction S(depth x noise, duration) comes from R1 (planted dips at K = 6 to 18 times the 8 h box noise, durations 4, 8, 14, 20 h, as in the frozen completeness runs), interpolated in log K and log duration.
- Detection chance of a star-sector in a cell = W x S. For a star: P(i, c) = 1 minus the product over its star-sectors of (1 minus W x S).
- **Ceiling for zero found: f = -ln(0.05) / sum_i P(i, c) = 3.0 / sum_i P(i, c)** (one-sided 95%, Poisson), the same formula Oddo et al. use. For k found: the standard Poisson upper limit for k events. Ceilings are published per cell; no single occurrence number.
- Window coverage per star-sector: SPOC star-sectors use their own windows; QLP-only star-sectors use the hashed reference windows table (union of G3, G2 and G1 SPOC 2-minute files, `research/stage3/g3-union-windows.json`), as in the search. Star-sectors with no safe windows contribute zero.

## 8. The reality check (before anything is published)
Compare the planted recovery with the real recovery of the known planet TOI-1338 b: 4 of 10 sectors at tier 1 in the sealed run, against the planted completeness at its depth (about 20%, `chain_recovery` sealed table). Pass: planted recovery does not overstate real recovery by more than a factor of 2 at its depth. **Kill rule (written now):** if the planted recovery overstates the real one by more than a factor of 2 for at least 2 known planets and the realism arm (timing and duration spread already in section 5) cannot close the gap, Horizon is stopped and the finding is published as the result. With one known planet in our sets, a pass is weak evidence and is worded that way.

## 9. What is NOT allowed
No tuning on results; if the map looks poor it is published as it is. No edit of the 11 fingerprinted files. No sealed or G3 light is planted into. No event lists, no candidate claims. Labels CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED on every statement; no en or em dashes in book text.

## 10. UNCERTAIN, said now
- Whether circumbinary transit probability for non-coplanar planets (Li et al. 2016, cited in Martin 2018) matters: not read; the published map is coplanar only.
- The depth-to-radius step assumes the TIC radius is the crossed star's and that no light is diluted; both are generous.
- The sealed-run completeness at TOI-1338 b's depth is a 4-of-10 count on one planet.
- Compute time is unknown until one star is timed (R1 begins with that).

## Lock record
Written and committed 3 Nov 2026 before any Horizon injection and before the G3 result is opened. The commit that contains this file is the lock commit: find it with `git log -- research/stage3/HORIZON-R0-RULE.md`. Amendments go below, dated.
