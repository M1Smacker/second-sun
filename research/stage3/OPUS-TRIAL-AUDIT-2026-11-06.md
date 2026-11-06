# Opus trial audit of the T138 groundwork (6 Nov 2026)

**Verdict: found 9 reproducible issues, 2 of them change a conclusion.** The headline "our null is consistent with Kepler's 10%" survives and gets firmer. What does not survive: the tilt rows (UPDATE 2) and their "about 1% in the optimistic corner" reading, and the claim that G3 loses most because its stars are bigger.

Model: Opus 5.5. Report only; no other file touched, nothing committed.
Usage: weekly 50% at start, 51% at the end; 5-hour 33% at start, 40% at the end (get_usage, before and after; other sessions on the account also move these). About 20 tool rounds in 4 turns.
My scripts (scratchpad, not in the repo): `audit_overlap.py`, `audit_data.py`, `audit_mc.py`. Their outputs are quoted below.

## Findings, most severe first

### F-1. The tilt probe's rule is wrong for a 27-day look (changes a conclusion, CONFIRMED)
- `t138_incl_probe.py` line 22: `bmax = (Rs / (ap - aA) + 0.5 * np.radians(delta_deg)) * ab / Rsum`. This makes every star with b below a widened bound transit with certainty. That is the long-run picture (Martin and Triaud: with precession, given enough time). The docstring (line 3) fixes the node angle "over the observation", so it is a snapshot. Q1 UPDATE 5 also says the snapshot is the right size for one sector.
- In a snapshot, Li, Holman and Tao 2016 eq. 9 (local text) allow a transit only for node angles where the planet's offset stays inside R/a_p. A tilt pushes some planets into the band and others out of it.
- 3D Monte Carlo (`audit_mc.py`: median G2 star, P_bin 9.5 d, 2 Msun, R_A 1.3, R_sum 1.8 R_A, 3,000 isotropic eclipsing binaries per row). Quoted output:
  - "P_p 77.8 d, tilt 0 deg: ... mean h (snapshot, one conjunction) 0.135"
  - "P_p 77.8 d, tilt 3 deg: ... mean h (snapshot, one conjunction) 0.143 | ... tilt-probe rule min(1,(eps+0.5 delta)/C) 0.422"
  - "P_p 139.8 d, tilt 3 deg: ... mean h ... 0.093 | ... tilt-probe rule ... 0.367"
  - With tilts of 1 and 2 degrees the snapshot share stays at 0.124 to 0.136 (77.8 d) and 0.089 to 0.097 (139.8 d).
- So a 0 to 3 degree tilt leaves the snapshot chance flat. The probe's rule makes it about 3 times too big at 3 degrees. Even the "ever transits" share rises only from 0.162 to 0.221.
- Consequence: drop the UPDATE 2 rows with Delta > 0 (E up to 7.2; "chance of none ... about 1%") and the sentence "the null is consistent with Kepler's rate unless several optimistic assumptions all hold together". The Delta = 0 row is the right snapshot.

### F-2. The per-star impact parameter is not a measurement (changes a conclusion, CONFIRMED)
- b comes from x = sqrt(1 - b^2) = pi a_b T / (P R_sum) (probe line 27). The test b < bmax needs bmax of about 0.10 to 0.19, which means x above about 0.98 to 0.995. So the inputs (TIC radius of a blended pair, a fixed 2 Msun mass, the unknown R_sum, two different width definitions) would have to be right to about 1%. They are uncertain by 10 to 30%.
- What actually passes is almost entirely stars with x >= 1. These are widths too long for a central eclipse, which line 28 silently clips to b = 0. Output of `audit_data.py`:
  - "g2sealed f=1.8: x known 522, x>=1 (b set to 0) 0.117, x in 0.97..1 (b<0.24) 0.008, median x 0.511"
  - "g3 f=1.5: ... x>=1 (b set to 0) 0.121 ..." ; "g3 f=1.8: ... 0.029" ; "g3 f=2.2: ... 0.011"
- An isotropic sample would put about 24% of stars in b < 0.24. The data put about 1% there, plus a separate clipped pile. So g tracks the clipped share, which tracks input calibration, not geometry.
- Robust cross-check: for isotropic eclipsing binaries, P(coplanar transit of A | eclipse) = (R_A/R_sum) a_b/(a_p - a_A). The mass cancels and no width is needed. Same Horizon sums, same cells:
  - "f=1.5: probe E A=2.25 B=3.64 | isotropic-population E A=2.13 B=3.24"
  - "f=1.8: probe E A=1.26 B=2.11 | isotropic-population E A=1.77 B=2.70"
  - "f=2.2: probe E A=0.70 B=1.23 | isotropic-population E A=1.45 B=2.21"
  - Per set at f=2.2, rule A: "g3 0.04/0.35".
- Q1 UPDATE 1 item 3 says "G3 loses most because its stars are bigger (median TIC radius 1.64 against a smaller G2 set)". The radii are nearly equal ("g2sealed: median rad 1.61", "g2dev: median rad 1.60", "g3: median rad 1.64"). Also, in the population formula R_A cancels. G3's collapse to g = 0.01 is the clipped share falling from 12% to 1%: an artifact, not a property of G3.
- Consequence: the probe's E range 0.7 to 3.6 is too wide at the low end. Per-hunt g, including G3's "0.01", should not be quoted.

### F-3. Transitable is not the same as transiting in this window (small, CONFIRMED)
- Horizon's W x S assumes every conjunction in the window is a transit. The coplanar g counts "some binary phase works".
- Monte Carlo: the mean per-conjunction share is 0.135 against 0.162 transitable (77.8 d), and 0.084 against 0.097 (139.8 d). So g is about 15% too high. This matches Li's first-order R/a_p (0.137, 0.093).

### F-4. The R_sum choices imply a bright companion, but the map assumes no dilution (small, CONFIRMED)
- R_sum = 1.8 to 2.2 R_A means a companion of 0.8 to 1.2 R_A, yet the probe uses the undiluted main scenario (`H.reach(..., 5.6, 1.0)`). Rerun with dilution: "f=1.8 probe g with dilution 0.7: E A=1.12 B=1.90"; "dilution 0.5: E A=0.98 B=1.68". That is 10 to 22% lower. At R_sum 2.2 star B is the bigger star and its transits are ignored (adds about 20% back for that case only, by the same b; NOT TESTED).

### F-A. "Could not exclude it" is too strong (small, CONFIRMED)
- Q1 UPDATE 1 item 1 says this flat. Its own R_sum 1.5, rule B row gives chance of none 2.6% and a ceiling of 8.2% (`t138-geometry-probe.txt` line 18), which excludes 10% at 95%. After F-1 to F-4 this corner disappears, so the sentence ends up right for a different reason.

### F-B. "15 to 36" is not in the output (small, CONFIRMED)
- Q1 UPDATE 1 item 2 says "with g the Horizon sums fall to 15 to 36". The probe output gives 22.5/36.4 (R_sum 1.5), 12.6/21.1 (1.8) and 7.0/12.3 (2.2). The comparison with Kepler's 40 to 70 gets stronger, not weaker.

### F-C. The Census sizing rows are not like for like (small, CONFIRMED)
- Q1 UPDATE 1 item 4: the 10% row uses rule B at R_sum 1.5 for its low end (1,001 stars). The 5% and 3.5% rows use rule B at R_sum 1.8 (2,784; 3,977). Like for like, the low ends are 2,002 (5%) and 2,860 (3.5%) at R_sum 1.5, or 1,392 (10%) at R_sum 1.8.

### F-D. "Roughly double our evidence" overstates (cosmetic, CONFIRMED)
- CENSUS-WORTH says this for 1,400 stars. `census-worth.txt` gives 8.0 against 12.6, 13.6 against 21.1 and 11.5 against 22.5, which is +51% to +65%.

### F-E. Dead line and mixed width sources (cosmetic, CONFIRMED)
- `t138_geometry_probe.py` line 19 reads `g2_chain_targets.csv` and never uses it.
- G2 widths are the Prsa polyfit width (`Wp-pf` x `Per` x 24); G3 widths are TTC median durations rounded to 0.1 h (`g3_chain_targets.csv` header). These are different definitions feeding one formula, and part of why F-2 differs by set.

### What the corrected numbers look like (LIKELY: the factors are multiplied as if independent)
- Coplanar, all three hunts, Kepler's 10%:
  - R_sum 1.5: about 1.7 to 2.6 expected (isotropic E x 0.85 for F-3 x about 0.95 dilution).
  - R_sum 1.8: about 1.3 to 2.1 (x 0.85 x 0.89).
  - R_sum 2.2: about 0.9 to 1.3.
- So E is about 0.9 to 2.6, the chance of none 7% to 40%, and the 95% ceiling about 12% to 33%.
- The headline holds: **the null is consistent with Kepler's 10% everywhere in the grid, and our hunts cannot test it.**
- The CENSUS-WORTH numbers at R_sum 1.8 move by about 10% (the effects partly cancel); at R_sum 1.5 they fall by about 20%. Its plain verdict stands.

## Checks that passed (no issue)
- Q1 coplanar condition: CONFIRMED by independent algebra and by the Monte Carlo ("tilt 0 deg: ever-transits (h>0) 0.162 | ... coplanar formula R_A/(a_p-a_A)/C 0.156"; 0.097 against 0.101 at 139.8 d). The frame, sign, star A, a_p from the barycentre, units and the R_sum factor are right. Li 2016 eq. 7 agrees at first order. Leftovers: R_p is left out (conservative); a_A = a_b/2 is slightly optimistic for unequal masses.
- Q2 conversions: a = 215.03 (M P_yr^2)^(1/3) is right, with the planet's a about the barycentre. The duration-to-b formula is the standard small-angle one. G2 catalogue period matches pbin ("Per/pbin median 1.000, share outside 0.99..1.01: 0.000"). Missing widths take the median b (printed counts: 522 of 594, 258 of 301, 612 of 612). Unstable cells are already removed by Horizon's 5.6 x P_bin floor.
- Q4 arithmetic: every E, exp(-E) and 0.3/E in the Q1 tables, all UPDATEs and CENSUS-WORTH reproduces from the outputs. The four hunts share no star (`audit_overlap.py`: all six overlaps 0), so adding E is allowed.

## What I checked
Q1 to Q4 fully; Q5 in part (dilution, B transits, per-conjunction factor, width sources).

## What I did not check
- I did not open Martin and Triaud 2015 eq. 26 or Oddo 2026 (I relied on algebra, the Monte Carlo and Li's local text).
- Whether `Wp-pf` is a first-to-fourth-contact width.
- Horizon's recovery tables, R0 rule text and the window function itself.
- The q2 pool-value ratios used by CENSUS-WORTH.
- Armstrong 2014.
- Eccentric binaries, and precession over multi-sector spans.
- Monte Carlo cases other than the median star.

## Estimate for a full-project audit
- This trial cost 1 weekly point (the meter is in whole points, so the true cost is somewhere between a fraction of a point and nearly 2). It read about 60 KB of science-critical material in depth and ran 3 small scripts. The 5-hour meter moved 7 points.
- At this depth, 3.7 MB would cost about 50 to 60 points, which is not possible. A 20-point audit can do about 1 MB in depth: Vesper's core, the recovery tables, Horizon, and the G2 and G3 result notes. A skim of the rest of the research notes would cost about 3 to 5 points. The book pages would get spot checks only.
- At about 7 five-hour points per weekly point, 20 points needs at least 3 five-hour windows. It is best split into about 8 sessions by area, so no single context has to hold 3.7 MB.
- Hit rate here: 2 conclusion-level and 7 minor issues in about 60 KB.

Next: Ahmed decides whether the 20-point audit goes ahead, given 1 weekly point for this trial. Separately, the T138 build should take F-1 and F-2 on board: use the isotropic population g, or a per-star b with a check for x >= 1; drop the tilt rule; apply the F-3 factor and dilution. That is the parent session's work, not mine.
