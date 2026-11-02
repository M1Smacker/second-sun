# Horizon research, RS-002 (3 Nov 2026, Sonnet 5.5 Extra, cap 3 weekly points)

Method: `research/RESEARCH-BLUEPRINT.md`. Brief: `NEW-SYSTEMS-RESEARCH-BRIEF-2026-11-02.md` section 4 (H-1 to H-14). Design under test: `HORIZON-DESIGN.md`. Scripts and outputs: `research/stage3/horizon-research/`. Nothing in the pipeline, the frozen files or the book was changed. Labels as in `vigil-literature-2026-11-03.md`.

## 0. Plain verdict: Horizon is GO, and cheaper than planned, with one new warning

- **Cheaper:** the injection engine already exists (`pipeline/chain_recovery.py` plants a trapezoid through the whole frozen chain) and the ceiling calculator already exists in a crude form (section C of `scorecard_plus.py`). Horizon is an upgrade and a mapping layer, not a new machine. New estimate about 3.0 points (range 2.5 to 4), down from about 4.0, plus task T107 (host radii, about 0.3) which must come first.
- **The same method is now published:** Oddo et al. 2026 (arXiv:2610.22625, submitted 15 Oct 2026) do the same thing for TESS M-dwarf binaries, so our map will be comparable.
- **New warning:** our first honest ceilings will probably be far below Kepler's occurrence rate. That is more likely a sign that the reach is over-generous (or the geometry factor is not 1) than a finding about planets, so the reality check in section 4 is part of the design, not an extra.

## 1. H-1 [P1] Oddo et al. 2026: answered, CONFIRMED (abstract and HTML text read)

[arXiv:2610.22625](https://arxiv.org/abs/2610.22625), "The Occurrence of Circumbinary Planets Around TESS M-dwarf Eclipsing Binaries" (Oddo, Dragomir, Martin, Tubthong, Han). The first entry that was missing on 29 Oct now exists.
- Result: a 95% upper limit on the occurrence of **coplanar** circumbinary planets of 2 to 16 Earth radii with periods up to 600 days of **33.0%**; **40.2%** if mutual inclinations are isotropic. One new candidate found.
- Method: a custom single-transit search; completeness per grid cell is the product of a **recovery fraction S(Rp, P) and a window function W(P)** (their formula, epsilon = S x W), the window function from N-body (REBOUND) simulations of the probability that a transit falls in TESS's coverage for each binary; inverse detection efficiency weighting.
- Injections: more than 1 million; radii uniform 2 to 16 Earth radii, periods log-uniform 10 to 600 days; the critical stability period of each binary from Holman and Wiegert is checked; the sensitivity map is **7 uniform radius bins by 7 log-uniform period bins**. "Recovered" = passes the search threshold (SNR 10) AND a trapezoid fit within 0.05 d of the injected time matches depth and duration within 40% AND passes vetting. Sensitivity tops out near 60%.
- Zero-detection ceiling: they solve exp(-lambda) = alpha, so f_up = -ln(alpha) / (N x eta) (their equations 13 and 14). **This is exactly our design's rule** (ceiling = 3.0 divided by the summed detection chance at 95%).
- Plan change: copy their cell layout (7 by 7, radius 2 to 16, period 10 to 600 days) for comparability, and also publish coplanar and isotropic scenarios. Ahmed's default radius range was Neptune to Jupiter; showing 2 to 16 with the Neptune to Jupiter rows marked costs no extra compute (his call, small).

## 2. H-2 [P1] Stability floor: answered, CONFIRMED

[Holman and Wiegert 1999, arXiv:astro-ph/9809315](https://arxiv.org/abs/astro-ph/9809315), equation 3 (ar5iv text read): the smallest stable circumbinary orbit, in units of the binary semi-major axis, is a_c = 1.60 + 5.10 e - 2.22 e^2 + 4.12 mu - 4.27 e mu - 5.09 mu^2 + 4.61 e^2 mu^2 (mu = M2 / (M1 + M2)), "good to 3% typically, and to 6% worst-case" for 0 <= e <= 0.7 and 0.1 <= mu <= 0.9; test particles survive 10^4 binary periods. This matches my memory, so that UNCERTAIN line in `HORIZON-DESIGN.md` is closed.
- Numbers (`h2_stability_numbers.py`): critical period ratio P_c / P_bin = a_c^1.5 runs from **2.75 to 6.16** over e 0 to 0.3 and mu 0.1 to 0.5 (circular equal-ish masses about 3.7; e = 0.3 about 6.0).
- Observed (our own table, `vigil-research/v_b4_period_ratios.py`, CONFIRMED): the transiting circumbinary planets sit at ratios 5.57 (Kepler-16 b), 5.62, 6.34, 6.53, 6.55, 6.64, 6.92, then 8.8, 10.4, 12.9. For Kepler-16 with e = 0.159 and mu = 0.226 (values from memory, UNCERTAIN) the floor is 4.88, so the planet sits about 14% above it. This settles the earlier "ratio near 5.6" line: it is the observed minimum, not the stability floor.
- Our star tables have no binary eccentricity or mass ratio (the Prsa table has morphology and widths, the TTC table has Teff and depths). Plan change for R0: floor ratio is a stated choice, not a lookup. Recommendation (my reasoning): map with a floor of 4.0 and publish the sensitivity to floors 3 and 5.6; in each star, cells below its own floor period (ratio x P_bin) do not count in its detection chance. A lower floor makes the ceilings look better than they are, so the published map uses the pessimistic (higher) floor.

## 3. H-3 [P1], H-4 [P1], V-B7: occurrence and geometry: answered with limits

- **H-4, CONFIRMED (abstract read):** [Armstrong et al. 2014, arXiv:1404.5617](https://arxiv.org/abs/1404.5617): from Kepler, occurrence of planets with R > 6 Earth radii and P < 300 d is **10.0 (+18, -6.5)%** (95% limits) if planets are preferentially coplanar with the binary, and a **lower limit of 47%** if isotropic; giant planets (> 10 Earth radii) are significantly less common than smaller ones; the shortfall around short-period binaries is real. Oddo: 33.0% and 40.2% (above). Not found: a Li 2016 abstract and the "Martin and Fabrycky 2021" paper I had in the brief; titles remain unverified, so no numbers are taken from them.
- **H-3, partial:** both papers show the result depends on the mutual-inclination assumption, and Oddo reports both scenarios. Plan change: Horizon always prints the coplanar ceiling and says plainly that the isotropic one is higher (Oddo's ratio of the two limits is 40.2 / 33.0 = 1.22 for their sample; ours would differ). The transit-probability formula itself was not opened.
- **V-B7 (Vigil yield):** with our crude section C numbers (below) no honest yield can be quoted before Horizon runs. Open until R2.

## 4. The reality check (new): will our ceilings contradict Kepler?

Own data, CONFIRMED (`scorecard-plus-sealed.txt` section C, 594 sealed stars, host radius fixed at 1 solar radius until T107): at 4000 ppm (about 6.85 Earth radii undiluted) tier-1 completeness is 57%, expected tier-1 detections per planet-bearing star 1.76 at P = 95 d, and the 95% limit on (planets per binary times geometry factor g) is **0.8% at P = 95 d**. If g is near 1 for coplanar planets, that is about 12 times below Armstrong's 10% (which spans P < 300 d, so one period bin should hold a few percent, not all of it). Three explanations, in the order I think likely (reasoning, UNCERTAIN): (1) the trapezoid injection is easier to find than a real transit (no timing shift, no duration change, one fixed shape), so the reach is over-generous; (2) the geometry factor is well below 1 (non-coplanar, or the planet misses the star); (3) these TESS binaries truly host fewer such planets.
One check that already exists: TOI-1338 b, a real circumbinary planet. Our run recovered it at tier 1 in 4 of 10 sectors with updated times (3 more at tier 2, 3 none; section E), where the injected-trapezoid completeness at its depth (K = 7.0) is 20%. So in this one case reality was **easier**, not harder, than the injections. One planet is thin evidence. Plan change: R0 states the reality check (compare real recovery of TOI-1338 b with planted recovery at the same depth) and the page labels the map "upper bound on reach" until a second known planet is tested; Kepler-field known hosts on G1 are the candidates (T-list for later).

## 5. H-5 [P2] Host radii and dilution: answered, CONFIRMED

The TTC table 3 columns (MRT header read) are TIC, position, Tmag, Per, T0-pri, Depth-pri (ppt), Dur-pri (h), T0-sec, Phase, Depth-sec, Dur-sec, Sectors, RUWE, AEN, AENS, Teff, Comments. **No stellar radius and no light ratio.** `targets/g2_chain_targets.csv` has a TIC radius column filled for **1 row** of 897. So the depth-to-radius step needs task **T107** (TIC radius from the FITS headers of the files we already hold, about 0.3 point) first, plus an explicit dilution assumption (share of the light the crossed star gives). Dilution stays an assumption and is stated on the page (UNCERTAIN).

## 6. H-6 [P2] Window coverage to detection chance: answered by formula

Write as Oddo does: for star i and cell c, P(i,c) = W(i,P) x S(i,c), where W is the chance that at least one transit falls inside the star's good-time windows (window table, Loom phase 0; QLP-only star-sectors borrow windows, item 70) and S is the recovery fraction from planted dips at that depth and duration. Simple version (mine, NOT TESTED): W = 1 - product over sectors of (1 - covered fraction x min(1, 26 d / P)) for random phase; N-body windows are optional. Ceiling for zero found = 3.0 / sum over stars of P(i,c).

## 7. H-7 [P1] Injection realism: answered, CONFIRMED (code docstring and own data)

`pipeline/chain_recovery.py` plants a **trapezoid with 20% ingress and egress**, the same time and the same ppm depth in **every** file of a star-sector, at a **random cadence** not within the match window of an existing event, depth K x the 8 h box noise of that light curve, then runs the unchanged frozen chain (search, flags, second-product check, SAP twin, v7 check, tiers). Recovered means primary event in tier 1. The dev run used 284 star-sectors and 13,632 injections. A zero-injection test reproduces the real run exactly. Gaps versus a real circumbinary transit: no timing shift between conjunctions, no duration change, one fixed shape. **Share of time inside eclipses** (`h7_eclipse_fraction.py`): G2 dev median 3.4% (mean 4.9%), G2 sealed 3.6%, G3 3.7%, so random-time injections land on an eclipse only about 4% of the time and the `ecl_overlap` flag is rarely the issue. Plan change: R1 reuses this engine and adds only the radius/period-to-depth/duration mapping; an optional realism arm adds a timing shift and a duration spread, to put a number on risk 1 of the design.

## 8. H-8 to H-12

- **H-8 answered, CONFIRMED:** the unit is already the measured noise of each light curve (K x 8 h box noise), not Tmag.
- **H-9 answered, LIKELY:** zero found: Poisson ceiling as Oddo (above). With a measured control background: [Feldman and Cousins](https://arxiv.org/abs/physics/9711021) (abstract read: a unified classical construction for upper limits and intervals, for Poisson processes with background) is the textbook choice; our `scorecard_plus.py` already uses a star-level bootstrap of the real-versus-upside-down ratio (deff 1.9 to 2.6 from clustering). Recommendation (reasoning): take the star-level upper limit on the excess from the scorecard (floored at the detectable excess if negative), then divide by the summed detection chance; do not use event-level Poisson (events cluster on stars).
- **H-10 answered by arithmetic:** a binomial 95% half-width of 0.05 at p = 0.5 needs 384 injections per cell, 0.10 needs 96; at p = 0.2 about 246 for 0.05. For 49 cells at about 400 each that is about 20,000 injections, about 1.5 times the dev run. Oddo used over a million.
- **H-11 OPEN:** compute time. The dev run's wall time was not found in the ledger or jobs file; R1 begins by timing one star.
- **H-12 partial:** the comparable published map is Oddo's 7 by 7 grid; Armstrong 2014 gives a debiased Kepler detection efficiency; not otherwise surveyed.

## 9. H-13, H-14

- **H-13:** Ahmed said go with the default (Neptune to Jupiter, name Horizon). Suggestion above for 2 to 16 in the grid.
- **H-14 answered, CONFIRMED:** the chain target list holds both slices (301 dev, 594 sealed). The existing recovery run for G2 used the dev run only; R1 must filter `slice == "dev"` and assert it. Nothing sealed is touched by Horizon. The G3 preregistration addendum text is still to be written in R0.

## 10. What changes in the Horizon plan

1. Reuse `chain_recovery.py` and `scorecard_plus.py` section C; new files only (a mapping layer and a grid runner); about 3.0 points, T107 first.
2. Grid and scenarios as Oddo (7 by 7, coplanar and isotropic) for comparability; radius range 2 to 16 with Neptune to Jupiter marked (Ahmed's call).
3. Floor ratio is a stated choice; pessimistic floor published, sensitivity to floors 3 and 5.6 shown.
4. Ceiling rule: Poisson for zero found (confirmed in the literature), star-level bootstrap for the excess otherwise.
5. Reality check against TOI-1338 b is part of R0; the page says "upper bound on reach".
6. Dev slice only, asserted in code.
7. Closed UNCERTAIN lines: Holman and Wiegert formula; observed Kepler-16 b ratio (5.57, not a floor).

## 11. Not done in this pass

Transit-probability formula for a given mutual inclination (Martin and Fabrycky) not opened; Li 2016 not found; no run of the planting code; compute time not measured; published sensitivity maps beyond Oddo and Armstrong not surveyed; TIC radii not yet extracted (T107).
