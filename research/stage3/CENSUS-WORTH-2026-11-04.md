# Is Census worth running? What 1,400 to 6,000 G2-type stars would add (night of 4 Nov 2026; research stint RS-011; arithmetic on earlier outputs; report only)

## CORRECTED AGAIN 8 Nov 2026: forward-looking odds (found by an outside review, `research/handoff-2026-11-07`, WO-1; reproduced here)
**Plain verdict:** the "chance of at least one" in the tables below counts our three finished searches, which found nothing, as if they were still to come. That is wrong as a forecast, so "very likely finds one" is withdrawn. Census alone, with the planet rate updated by the three nulls and completeness trimmed 10% (FIX 28): **1,400 G2-type stars (3 sectors each): 36% to 52%** if planets are Kepler-like (prior median 10%), **21% to 31%** under a broad prior (1% to 20%). **3,000 stars: 59% to 76% and 37% to 52%.** The believed rate itself falls to about 5% to 7% (Kepler-like prior) or 2% to 3% (broad prior). The 95% ceilings in the tables below are unchanged and correct, because a ceiling uses all hunts together. Script `census_step1/census_worth3.py`, output `census_step1/census-worth3.txt`. Labels: arithmetic on earlier outputs (LIKELY); the two priors are a choice, not data (UNCERTAIN). Adding G1 (about E 0.3) lowers each number by 1 to 2 points.

## CORRECTED 6 Nov 2026 (supersedes the numbers below; kept for the record)
Recomputed with the transit chance of Horizon R0 Amendment 4 (`census_step1/census_worth2.py`, output `census-worth2.txt`; inputs `t138-g-reach.txt`, main scenario). The 4 Nov table used the withdrawn per-star-width probe (Opus audit F-2).
**Plain verdict:** 1,400 G2-type stars with 3 sectors each add about 55% to our evidence, not double (the audit's F-D was right). About 3,000 stars (3 sectors) roughly double it (plus 118%); 6,000 add about 235%. Existing three hunts: E 1.3 to 2.9 at Kepler's 10%.

| Census | All hunts E | Chance of at least one | 95% ceiling if none |
|---|---|---|---|
| 1,400 stars, 3 sectors | 2.0 to 4.5 | 86% to 99% | 6.7% to 15.1% |
| 3,000 stars, 3 sectors | 2.8 to 6.3 | 94% to 100% | 4.8% to 10.8% |
| 6,000 stars, 3 sectors | 4.3 to 9.7 | 99% to 100% | 3.1% to 7.0% |

(ranges over companion size f 1.5 to 2.2 and rules A and B). With 6 sectors per star instead of 3, 1,400 stars add about 83%. So Census at its expected size of 1,400 would be a decent but not decisive test: a null would cap the total rate near 7% to 15%, and only about 3,000 or more G2-type stars would push the ceiling near 5% to 10%. LIKELY at best (the G2-type count is a factor of 2 estimate; the meaning of Armstrong's 10% per binary is UNCERTAIN).

--- below: the 4 Nov version, SUPERSEDED ---

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
