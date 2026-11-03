# Horizon: the reach map and null meter (design saved 2 Nov 2026)

**Status: idea only. Designed in chat with Ahmed on 2 Nov 2026. NOT started. Nothing in the pipeline or the book changed.** Queue entry: T119 in `BUILD-QUEUE.md` (section H). To resume: Ahmed says go, plus two answers (section 7). Memory pointer: `project_horizon_reach_map.md`.

## 1. Why: the gap, from our own files (all read this session)

Ahmed's rule: a clean measured null is the win (decisions of 29 Oct 2026). Today our null says "no more signals than the upside-down control". It does not say which planets we could have seen.

- `pipeline/scorecard_plus.py` lines 3 and 71: gives the upper limit AND the detectable excess of tier-1 real over the upside-down control, in star counts, with a star bootstrap (items T38, T39). That is a limit on signals, not on planets.
- `book/docs/book/08-our-detector.md` line 137: "Limits (honest): only 33 crossings, one star, one orbit angle per planet, and STANLEY never makes crossings of the **smaller** star. A proper sensitivity map needs hundreds of fake planets." STANLEY is the book's name for the existing fake-planet maker.
- `research/burn-1-science/open-questions.md` item 6: "Injection test used one sector, 8 times per size, one duration (6.4 h), one impact parameter. A real completeness map needs durations 3-15 h and more trials."
- Closest published model: a 2026 TESS search of M-dwarf eclipsing binaries with one candidate and an occurrence upper limit (Oddo et al., said to be arXiv:2610.22625). UNCERTAIN: the arXiv entry was not found on 29 Oct (`research/stage3/vesper-study-literature-2026-10-29.md` line 21). First task of R0: find and open it.

## 2. What Horizon is

Two outputs from one machine.
1. **Reach map:** for each cell of planet radius by orbital period (and star brightness), the chance that Vesper (frozen 0.8.0 rules) would have found at least one event, summed over a star set.
2. **Null meter:** given the number found (zero if it stays a clean null), a one-sided 95% ceiling on how common such planets can be, cell by cell. For zero found: ceiling = 3.0 divided by the summed detection chance (Poisson, minus the natural log of 0.05 is about 3.0). For k found, use the standard Poisson upper limit for k events.

Publish ceilings per cell, never one big occurrence number: the conversion depends on assumptions that stay UNCERTAIN.

## 3. Design in four steps

**R0. Write the rule first (about 1.0 point).** A short dated file, committed before any injection runs, fixing:
- the grid: planet radius bins (default Neptune to Jupiter, Ahmed to confirm), period bins, event durations 3 to 20 h (Vesper's box range), star brightness bins, window coverage per star;
- the stability floor: the planet must orbit outside the binary's dynamical stability limit. From memory, NOT verified now (UNCERTAIN): Holman and Wiegert 1999 gives the critical orbit; Kepler-16 b has about 229 d around a 41 d binary, a ratio near 5.6. If right, a binary over 7 d has planets at about 40 d or more, so at most about one transit per 27 d sector, which is why Vesper matches single events. Verify both in a primary source in R0;
- the geometry assumption (coplanar planets; the chance a planet transits) and where it comes from;
- the depth step: depth is roughly (planet radius / radius of the star crossed) squared times the share of the total light that star gives. Whether star radii and light ratios are in the TESS Ten Thousand Catalog tables we hold (`data/g3/catalog_ttc`) is UNCERTAIN; check first;
- the detection rule: tier 1 or better after flags, exactly as frozen in 0.8.0 (no new switches).

**R1. Planted-dip grid on the G2 DEV split only (about 1.5 points).** Reuse the existing planting code (a grep shows planting or building functions in `pipeline/audit_all.py`, `chain_recovery.py`, `scorecard_plus.py`, `stage3.py`; exact names not read yet). New code goes in new files; do NOT edit the 11 fingerprinted files (frozen 0.8.0, hash 5f73692944aad8ee9df795100488ee1522b8e7f0c8cfeb3d898fc2e9bf653d0a). Each planted dip is run through the real search chain. Control first, then fix: a test that plants nothing must recover nothing. Machine hours: run detached at 8 workers, NUMBA_NUM_THREADS=1, 70% CPU only when Ahmed is away. Time one star before launching.

**R2. Chance and ceiling calculator (about 0.8 point).** For star i and cell c: P(i,c) = 1 minus the product over that star's usable events of (1 minus the recovery chance at that depth and duration). Window coverage comes from the reference windows table (Loom phase 0, `spoc_windows.pkl`; QLP stars borrow windows, bug 70). Sum over stars, then the ceiling. Unit tests on a toy set with a known answer.

**R3. Book page and publish (about 0.7 point).** Page "What we could have seen": one map, one sentence per row, no event lists, no candidate claims. Add the learning track entry and quiz check the same day (standing rule), a field note, bump the book version, run `publish_book.ps1 -Test`.

Total about 4.0 weekly points, range 3 to 6. The calibration from the ledger: ported work runs 0.2 to 0.4 of the estimate, new pages run near it. Most of R1 is ported.

## 4. Rules that bind it

- Dev split only for planting. The sealed S2 data and the sealed result are not touched.
- Preregister before the G3 search (G3 search is one-shot): add a dated addendum to `G3-PREREGISTRATION.md` pointing at the R0 file and its hash.
- No tuning on results; if the map looks bad, publish it as it is.
- No event lists, no candidate claims. Label every statement CONFIRMED, LIKELY, UNCERTAIN or NOT TESTED. No en or em dashes.

## 5. Risks

1. Fake dips may be easier than real circumbinary transits (real ones shift in time, change duration, may sit on eclipses; flag `ecl_overlap`). The map could be too generous. Mitigation: plant with timing and duration spread and say so on the page; label the map "upper bound on reach".
2. Planet size conversion (depth to radius) in a blended pair is uncertain.
3. Compute time unknown until one star is timed.
4. Scope creep into a new detector. It is not one: it only measures the frozen one.

## 6. Why it is worth doing

It turns "we found nothing" into "we could have seen planets this big, this far out, in this fraction of the stars". That is the difference between a null nobody can use and a measurement. It also gives G3 its ceiling, and it is the missing step the book already calls out.

## 7. Open items needing Ahmed

1. Planet radius range of the grid (default Neptune to Jupiter).
2. Does the name Horizon stay.
3. His yes to start, after the 3 Nov 01:00 Kuwait reset (new-week default: stop at 25% and wait for his word).

## 8. Resume checklist

1. Read this file and T119.
2. Open Oddo et al. 2026 and the stability sources; fill the two UNCERTAIN lines in section 3.
3. Write the R0 rule file and commit it, then add the G3 preregistration addendum, before any run.
4. Time one star; then R1.

## 9. Related

Loom phase 0 windows table; bug 70; `g3-window-feasibility-2026-11-02.txt`; V9 study rules (nothing in Horizon changes frozen settings); `research/learning-and-checking-literature-2026-11-02.md` (negative controls and known-answer tests are the same family of checks).

## 10. Addendum 3 Nov 2026: what RS-002 found (full file: `horizon-literature-2026-11-03.md`)

- Verdict: GO, cheaper. `pipeline/chain_recovery.py` already plants a trapezoid (20% ingress and egress) through the whole frozen chain and `scorecard_plus.py` section C already holds a crude ceiling calculator. Horizon becomes a mapping layer plus a grid runner in new files; estimate about 3.0 points (range 2.5 to 4), after task T107 (host radii from the FITS headers, about 0.3), because `g2_chain_targets.csv` has a TIC radius for 1 of 897 rows and the TTC table has no radii or light ratios.
- Closed UNCERTAIN lines: Holman and Wiegert 1999 equation 3 read (ar5iv); critical period ratio runs 2.75 to 6.16 for e up to 0.3 and mu 0.1 to 0.5; the observed minimum ratio is 5.57 (Kepler-16 b), seven of ten transiting planets sit at 5.6 to 6.9 (own table). The "ratio near 5.6" in section 3 is the observed minimum, not the stability floor.
- Oddo et al. 2026 (arXiv:2610.22625) found and read: same method, 7 by 7 grid (radius 2 to 16 Earth radii, period 10 to 600 d), completeness = recovery fraction times window function, zero-detection ceiling f = -ln(alpha) / sum of detection chance (our rule), limits 33.0% coplanar and 40.2% isotropic. Copy the grid for comparability.
- New requirement for R0: the reality check. Section C of the sealed scorecard implies 0.8% (planets per binary times g) at P = 95 d for 6.85 Earth radii, about 12 times below Armstrong 2014's 10% (R > 6 Earth radii, P < 300 d, coplanar). Before publishing, compare the planted recovery with the real recovery of TOI-1338 b (4 of 10 sectors at tier 1 against 20% planted completeness at its depth) and label the map "upper bound on reach".
- Floor ratio is a stated choice (publish the pessimistic one, show sensitivity to floors 3 and 5.6). R1 must filter `slice == "dev"` and assert it (the chain target list holds 301 dev and 594 sealed).
- Still open: compute time (time one star first), the transit-probability formula for non-coplanar planets, Li 2016.
- **T107 radii done 3 Nov 2026:** `targets/host_radii_g2_g3.csv` (script `horizon-research/t107_host_radii.py`), TIC radius from FITS headers: positive for 822 of 895 G2 and 562 of 612 G3 stars (73 headers say -1, meaning none; the first count, 846 and 611, wrongly counted them; corrected 3 Nov 2026). **Median host radius of the positive ones 1.62 solar radii (10th to 90th percentile 0.88 to 3.36).** The scorecard section C assumed 1 solar radius, so for a given depth the planet is about 1.6 times larger than that table said (4000 ppm is about 11.2 Earth radii at the median host, not 6.85). That moves the earlier "0.8% against Armstrong's 10%" comparison to larger planets, where Armstrong also finds giants (above 10 Earth radii) significantly rarer, so the tension is smaller than first written. Dilution (share of light from the crossed star) is still an assumption for R0.
