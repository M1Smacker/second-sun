# Horizon first reach maps (3 Nov 2026; R0 rule `HORIZON-R0-RULE.md` and its Amendment 1)

Plain line: **a first reach map and zero-found ceilings now exist for the G2 development stars, the sealed G2 stars and G3, in four scenarios.** They are an UPPER BOUND on what the frozen search could have seen, not a measurement of how common planets are. Nothing in the pipeline's 11 fingerprinted files changed; the calculator is `pipeline/horizon_reach.py` (new file). Cost: no new injection run, because the 0.9 study had already planted dips with the 0.8.0 rules on the development split.

## What was built
- Recovery table (R1, reused): share of planted dips ending as tier 1, by duration (4, 8, 14, 20 h) and depth K (6 to 18 x the 8 h box noise), SPOC family 177 and QLP 107 injections per cell (dev split only, asserted). Example, 8 h dips: K6 11% (SPOC family) and 21% (QLP), K10 45% and 53%, K18 62% and 58%. Dips of 20 h are recovered about half as often.
- Calculator (R2): per cell of 7 radius bins (2 to 16 Earth radii) by 7 log-spaced period bins (10 to 600 d), with the stability floor F x binary period, the TIC host radius (822 of 895 G2 and 562 of 612 G3 stars positive; the rest use the set median 1.6 solar radii), a physical duration, the window function and the table. Ceiling for zero found = 3.0 / sum of detection chance.
- Checked: calculated 8 h noise matches the planting's own to a median ratio 0.98 (16 to 84%: 0.94 to 1.04, n = 284). **CONFIRMED** (own data).

## Key numbers (G2 sealed, 594 stars; one cell is 7 Earth radii at 77 to 139 d, the Kepler-16 size and range)
| Scenario | Sum of chance | 95% ceiling, zero found |
|---|---|---|
| main (F = 5.6, no dilution) | about 87 stars | about 3.4% to 3.5% of stars |
| floor F = 3 | about 120 | about 2.4% |
| floor F = 6.9 | about 65 | about 3.6% to 4.7% |
| dilution 0.5 (half the light from the crossed star) | about 50 | about 5.9% |
For 11 Earth radii the main ceiling is 2.2% to 2.3% at 77 to 139 d. The ceiling is for ONE cell; a statement about all planets above 6 Earth radii inside 300 d (Armstrong 2014's 10%) needs an integration over cells that has not been done (UNCERTAIN). With the known planet counted (k = 1: Poisson 95% factor 4.74 instead of 3.0) the same cells read about 1.6 times higher.
G3 (provisional): the same 7 Earth radii cell reads 15% to 17% (faint stars, larger noise), 11 Earth radii 4% to 5%: G3 tests large planets, as its preregistration said.

## Reality check (R0 section 8): PASSED on one planet, a weak test
TOI-1338 b, as seen (median depth of its events 2,300 ppm, K 7.0): planted tier-1 completeness about 20% (sealed scorecard section C; the dev table gives 18% to 28% at K 7); **real tier-1 recovery 4 of 10 sectors with an updated predicted transit** (scorecard section E; 3 more at tier 2 only, 3 none). Planted does not overstate real (20% against 40%, 4 of 10 has a 95% interval of about 12% to 74%). The kill rule (planted more than twice real on two planets) cannot trigger on one planet. UNCERTAIN: one planet, and the real transits have known times.

## What these numbers do NOT say
Coplanar, circular orbits only (isotropic scenario not run); the depth uses the TIC radius and no dilution (generous; the dilute 0.5 scenario shows the cost); S = 0 below K 6 (understates); the window function and independent epochs are approximations; the G3 table is borrowed from brighter stars until G3's own completeness exists. Li et al. 2016 not read.

## Plan change
R1 and R2 are done at first-version level. What remains for Horizon: an integration over cells for the Armstrong comparison, the isotropic scenario, a bootstrap error on the table, the page and the learning-track entry (R3), and replacing the G3 table by G3's own after the search.
