# Is Census worth running? What 1,400 to 6,000 G2-type stars would add (night of 4 Nov 2026; research stint RS-011; arithmetic on earlier outputs; report only)

Script `research/stage3/census_step1/census_worth.py`, output `census-worth.txt`. Inputs (all produced tonight): Horizon-with-geometry sums per search (`t138-geometry-probe.txt`), the value of a star with 3 or 6 sectors against the G2 sealed set (`q2-pool-value.txt`: 88.5 and 133.0 against 195.6 star-equivalents per 1,000 stars), the expected number of G2-type stars among the new bright 2-minute stars (about 1,400, `CENSUS-STEP2-RESEARCH`, LIKELY, factor 2), and Armstrong 2014's central 10% (abstract CONFIRMED). The geometry factor and the companion size (R_sum) are the big unknowns, so three cases are shown: R_sum 1.5 (more optimistic), 1.8 and rule A or B for how the 10% spreads over cells (A pessimistic, B middle).

## Plain verdict
**Yes, with a caveat: a Census of about 1,400 G2-type stars with 3 sectors each would roughly double our evidence. All hunts together would expect about 2 to 5.5 planets if Kepler's 10% holds, a chance of finding at least one of 87% to 100%, and a null would cap the total rate near 5% to 15%.** A Census of 3,000 to 6,000 stars would be a real test (ceiling 2.5% to 10%). It cannot be a decisive test of anything below about 5% without the 6,000-star size, and everything depends on the geometry factor, which is a probe, not a measurement.

## Numbers (R_sum 1.8 x R_A, the middle case; existing hunts alone E = 1.3 to 2.1, chance of none 12% to 28%)
| Census stars (3 sectors each) | rule A: all hunts E, at least one, ceiling if none | rule B: all hunts E, at least one, ceiling if none |
|---|---|---|
| 1,400 | 2.1, 87%, 14.6% | 3.5, 97%, 8.6% |
| 3,000 | 3.0, 95%, 10.1% | 5.0, 99%, 6.0% |
| 6,000 | 4.7, 99%, 6.4% | 8.0, 100%, 3.8% |
With R_sum 1.5 (optimistic): 1,400 stars give E 3.4 to 5.5 and a ceiling of 5.4% to 8.8%; 6 sectors per star instead of 3 adds about one third (1,400 stars: E 4.0 to 6.5).

## What it means
- The Census list size that matters is the number of **G2-type** stars (long period, detached, bright), not the 258,858 scanned: about 0.4% of the scanned stars. Scanning is cheap (days); the yield is small.
- Brightness and sectors each matter: a 6-sector star is worth 1.5 times a 3-sector star, and a star of Tmag 11.5 or fainter is worth about half of a bright one (Q2). Spend the download on the bright, long-coverage end first.
- The null of our existing hunts is not yet strong: with the geometry in, a Kepler-like rate would have shown about 1 to 4 planets and had a 3% to 50% chance of none. Census is how the evidence gets decisive. If planets are as common as Kepler found, Census at 1,400 stars very likely finds one; if none appears, the cap on the total rate falls to about 5% to 15%.
- Not a case for or against Census: the cost. The scan is 23 to 46 hours of download, the finder and vetting are the unknown work, and Ahmed decides.

## Labels
LIKELY: all sums (probe with an assumed condition and R_sum), the 1,400 count, the 3 and 6 sector ratios. UNCERTAIN: Armstrong's rate for long-period binaries (direction probably higher), factor 2 on each count. NOT TESTED: g on known Kepler planets; the finder's recall; false alarms in a hunt this size (S2 is already near its mark).
