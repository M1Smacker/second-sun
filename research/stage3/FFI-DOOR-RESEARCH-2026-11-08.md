# FFI door: research findings (RS-012), 8 Nov 2026

Stint RS-012, cap 0.6 weekly points (written before the start, `research/research-sessions.md`). Model Sonnet 5.5 Extra. Method `research/RESEARCH-BLUEPRINT.md`. Saved texts of every page read: `data\ffi_door_papers_2026-11-08\` (git-ignored; logged in `research/downloads.csv`). No light curve was read or downloaded. Labels: CONFIRMED (read in the primary text, or our own query/data), LIKELY, UNCERTAIN, NOT TESTED.

**Plain verdict.** The door is real but narrower than "all FFI light": for bright slow binaries the usable products are QLP (to Tmag 13.5, sectors 1 to 104) and TESS-SPOC FFI (to Tmag 13.5, sectors 1 to 85, capped at 10,000 targets per CCD); the others are either clusters only or not readable by our frozen loader. Gaia's slow-period solutions are weaker than "93% agree" sounds. Three things nobody here had looked at are in section 6.

## 1. QLP full-frame light curves (Huang 2020, Kunimoto 2021 and 2022; MAST HLSP page)
| Fact | Value | Label | Source |
|---|---|---|---|
| Tmag limit | 13.5; also stars with proper motion over 200 mas/yr between 13.5 and 15 (Huang); from Sector 41 also M dwarfs to Tmag 15 (Teff under 4000 K, R under 0.8 Rsun, about 370,000 stars) | CONFIRMED | arXiv:2011.06459 section II; arXiv:2211.04386 section II |
| Cadence | 30 min (S1 to 26), 10 min (S27 to 55), 200 s (S56 on) | CONFIRMED | MAST QLP page https://archive.stsci.edu/hlsp/qlp |
| Sectors on MAST | 1 to 104 (target list for every sector present, none missing; page updated 2026-08-12) | CONFIRMED (counted by script on the page) | same |
| Method | FIPHOT difference imaging until Sector 93; "as of Sector 94" the TGLC PSF method | CONFIRMED (page text) | MAST page; https://tess.mit.edu/qlp/ |
| File name | `hlsp_qlp_tess_ffi_s####-<16-digit TIC>_tess_v01_llc.fits` | CONFIRMED | MAST page |
| Per-sector target lists | `https://archive.stsci.edu/hlsps/qlp/target_lists/s####.csv` (TIC, RA, Dec of every star with a light curve); 16 to 29 MB each (HEAD requests on S1, 30, 60, 98), so about 2.3 GB for 104 sectors (extrapolated) | CONFIRMED (sizes of four) | same |
| Flux columns | S1 to 55: `SAP_FLUX` (raw, best of 5 apertures), `KSPSAP_FLUX` (B-spline, knot spacing at least 0.3 d; the paper says more aggressive splines would distort long-duration transits). From S56: `SYS_RM_FLUX` added, "KSP" renamed "DET" (`DET_FLUX`) | CONFIRMED | Huang section III; tess.mit.edu/qlp (change note of 21 Nov 2023) |
| Quality flag | QLP's own "poor exposure" flag was bit 13 (value 4096); from Extended Mission 2 it is bit 31 (value 2^30) | CONFIRMED | tess.mit.edu/qlp |
| Noise | follows the pre-launch prediction; floor about 20 ppm for the brightest; amplitudes depend on TIC Tmag (deblending), smallest aperture can under-estimate amplitudes | CONFIRMED | Huang section IV |
| Known timing bugs | S74 to 79 up to +-3 min (fixed, v02 files); S99 to 104 wrong barycentric correction from orbit 210 (partly redelivered) | CONFIRMED | MAST page |
**Plan change:** the existence census can use the QLP per-sector target lists (exact, offline matching by TIC) instead of MAST CAOM queries; and the 400 are measured in all three cadence eras.

## 2. TESS-SPOC full-frame HLSP (Caldwell 2020; MAST page)
- Targets chosen from the FFIs: all 2-minute targets, H at most 10, within 100 pc, and field stars with **Tmag at most 13.5, log g at least 3.5 (dwarfs and sub-giants only) and crowding metric at least 0.8** (stars that dominate the flux in their aperture), taken in order of Tmag until **10,000 targets per CCD** or the list runs out, up to 160,000 per sector. The fixed cap makes the magnitude cut-off vary over the focal plane because of crowding. Example, Sector 14: 156,217 targets (20,000 two-minute, 31,175 IR-bright or nearby, 105,042 chosen by magnitude). CONFIRMED (Caldwell et al. 2020, arXiv:2011.05495 HTML, read, and the MAST page). **New for us:** giants (log g under 3.5) and blended stars (crowding under 0.8) are NOT in the SPOC FFI field-star list unless they pass the other rules (H at most 10, within 100 pc). Long-period EBs often contain giants, so SPOC FFI will under-represent them (LIKELY; share in the 400 is measured in stage C).
- Sectors with target lists on the page: 1 to 85 (counted by script; page updated 2026-07-23). The lists give targets that have target pixel files; "most, but not all" have light curves, so the list is an upper bound for light-curve existence. CONFIRMED.
- Files `hlsp_tess-spoc_tess_phot_<TIC>-s####_tess_v1_lc.fits`; same products as 2-minute data (SAP, PDCSAP); cadence follows the FFI era. CONFIRMED.
- Consequence (LIKELY, effect NOT TESTED): the 10,000-per-CCD cap means crowded low-latitude fields lose bright-enough stars, so SPOC FFI can be incomplete where QLP is not.

## 3. Other FFI products (MAST HLSP pages read)
| Product | Coverage | Tmag | Usable here? |
|---|---|---|---|
| TGLC (Han and Brandt 2023, arXiv:2301.03704) | HLSP, target lists S1 to 55 on the page; files named by Gaia DR3 id plus camera and CCD; S12 to 55 not in the MAST portal/API, only bulk scripts | to 16 | not readable by the frozen loader (NOT TESTED); the Gaia id in the file name joins directly to our Gaia sample |
| GSFC-ELEANOR-LITE (Powell 2022) | HLSP, primary mission S1 to 26 only, over 150 million light curves; S14 to 26 not in portal/API | to 16 | not readable by the loader (NOT TESTED) |
| DIAmante (Montalto 2020) | HLSP, 1.4 million light curves from S1 to 26, FGKM dwarfs and sub-giants | not stated on page | no (multi-sector products, different format) |
| CDIPS (Bouma 2019) | HLSP to S55 (DR6) but only cluster and young-star candidates, Gaia RP under 16 | | no (not a general product) |
| PATHOS (Nardiello) | clusters only | | no |
| eleanor (Feinstein 2019) | software, not an HLSP product | | no |
All CONFIRMED from the MAST pages. **Plan change:** U1 and U6 count only QLP and TESS-SPOC (the two products the frozen loader reads); TGLC and ELEANOR-LITE are reported as extra counts only.

## 4. Gaia DR3 eclipsing binaries beyond 5 days (Mowlavi et al. 2023, A&A 674, A16, arXiv:2211.00929, HTML read)
- Period agreement: of about 600,000 literature cross-matches, 88% are EBs in the literature; Gaia and literature periods agree for 86% of those, 93% if a factor of two counts. CONFIRMED. But "agree" means the literature period would drift by less than one cycle over the Gaia baseline (their eq. 6, r_P,lit under 1), which is generous and says nothing about a phase accurate to 0.25 d years later. CONFIRMED (text).
- Completeness 25% to 50% against OGLE4 in the Bulge and the Magellanic Clouds (faint, crowded fields); nothing is said about bright slow field binaries. CONFIRMED for what they measured; our case NOT TESTED by them.
- Long periods: the paper says peaks above about 5 d, "especially above 20 days", are aliases and search artefacts from the scanning law; at global ranking above 0.54 unexpected peaks at 53.7, 107.2 and 34.1 d; and for well-detached long-period systems an incorrect, much shorter period may be chosen. CONFIRMED (text).
- Non-EB share among cross-matches: 78,614 of 606,393 (13.0%) are classed as something else in the literature (Table 4). Blends are not quantified. CONFIRMED arithmetic from Table 4.
- Baseline 34 months (DR3); DR4 66 months. CONFIRMED.
- Ephemeris fields: `reference_time` is "barycentric JD in TCB minus 2455197.5 d" and the model phase is (t minus reference_time) mod period; `derived_primary_ecl_phase` is the phase of the geometrically deepest point; durations are in phase fractions, depth in G magnitude (Gaia TAP metadata, read today). `frequency_error` is bounded: at least 0.001 over the observation span (0.1% phase drift) and models above 0.6 over the span were rejected, so the stated period error allows anything from 0.1% to 60% of a cycle of drift at the END of the Gaia data. CONFIRMED (text). **Whether the Gaia ephemeris predicts a TESS eclipse within 0.25 d is NOT TESTED yet:** it needs frequency_error times the time from the Gaia reference to TESS, which I compute from the catalogue itself in stage B (new metric U8, no light curves needed).
- Model types (Table 2): TWOGAUSSIANS (8 parameters) 1,587,926 of 2,184,477 (72.7%); with an ellipsoidal term on eclipse 1: 389,725; on eclipse 2: 85,400; one-Gaussian types 36,984 and up. Mowlavi states that the light curve alone cannot separate detached from semi-detached systems, so TWOGAUSSIANS is a proxy only. CONFIRMED.
- Gaia non-single-star orbits: `gaiadr3.nss_two_body_orbit` holds 86,918 EclipsingBinary solutions (our own count query today); only 1,532 have a period over 5 d, 605 over 7 d, 75 over 20 d. CONFIRMED (own query). Too few to matter for the pool, useful as a clean-period subset.
- Gaia DR4: ESA's content page (last updated 14 Sep 2026) lists `vari_eclipsing_binary` with 2,392,500 rows (DR3 has 2,184,477, so only 9.5% more) and data from 25 Jul 2014 to 20 Jan 2020 (66 months). The release date is NOT on the page (UNCERTAIN). Plan consequence: the G5 pool built on DR3 will be refreshed when DR4 arrives; do not spend effort polishing DR3 ephemerides.

## 5. Independent period sources for bright slow EBs (counts only)
- ZTF periodic variables (Chen et al. 2020, VizieR J/ApJS/249/18 table2, read through the Harvard VizieR mirror): 10,912 stars with period over 5 d and g under 14.5; type EA: 186; EA with period over 5 d and g under 14: 103, under 13.5: 58, under 13: 21 (over 7 d: 52, 32, 14). ZTF is northern only. CONFIRMED (own query, table saved in `data\ffi_door_2026-11-08\extra\`). So ZTF adds at most about 100 slow EAs at our brightness, a small number next to the Gaia pool; the ZTF table also gives the time of minimum (T0, MJD 58257 to 58653 in the first rows, i.e. 2018 to 2019), which would be a much better ephemeris epoch than Gaia's. Overlap with the Gaia pool is computed in stage B.
- ASAS-SN variable stars (Jayasinghe, VizieR II/366): NOT TESTED. The CDS hosts (Strasbourg) do not answer from this PC and the Harvard mirror's database was down when tried.
- Hipparcos/Tycho EB flags: NOT TESTED (first query returned no rows; bright Hipparcos stars are mostly 2-minute targets or saturated in the FFI; low value).

## 6. New things found while reading (nobody here had looked)
1. **QLP's quality flag moved and our loader may miss it.** From Sector 56 QLP flags poor exposures in bit 31 (value 2^30). The loader reads files with lightkurve's "hard" mask; I checked lightkurve 2.6.0 in the project environment: hard mask = 24319, which includes bit 13 (4096, the old QLP flag) but NOT bit 31. CONFIRMED (mask arithmetic). Whether QLP-flagged cadences really survive into G3 and into a future search is NOT TESTED (needs one real S56+ file; stage D). Filed as FIX 84 candidate (report only; the frozen loader is not touched).
2. **Exact existence without the MAST archive load:** per-sector QLP and SPOC target lists (TIC, RA, Dec) are on MAST; cross-matching them gives star-sector existence offline (CONFIRMED that they exist; size about 2.3 GB for QLP).
3. **QLP now is TGLC** (from Sector 94), and TGLC file names carry the Gaia DR3 id; the PSF-based method removes neighbour light, which matters for blended Gaia EBs (UNCERTAIN how much).
4. **M-dwarf extension:** QLP covers M dwarfs (R under 0.8 Rsun, Teff under 4000 K) to Tmag 15 from Sector 41. That is exactly the "fainter only for M-dwarf hosts" exception of idea 1, and it means the red-dwarf stratum can have light curves down to Tmag 15 (CONFIRMED text; counts in stage B).
5. **Gaia alias artefacts at 34.1, 53.7, 107.2 d** are named in the paper; I will report how many of the pool sit within 1% of them (stage B, counts).
6. **Gaia DR4 timing** (above): the DR3 pool is a stopgap.

## 7. What changes in the plan (each item is applied in FFI-DOOR-TEST-PLAN-2026-11-08.md)
| Finding | Plan change |
|---|---|
| Only QLP and SPOC are loader-readable | U1, U6 count those two; TGLC and ELEANOR-LITE are extra counts only |
| QLP and SPOC lists are on MAST per sector | stage C uses the per-sector target lists (and CAOM only for sector time spans and TESS-observed sectors) |
| Gaia "agree" is a loose test; ephemeris unproven | new metric U8 (propagated Gaia ephemeris error at the TESS epoch, catalogue-only); U3 is judged on stars whose chosen sectors contain a predicted eclipse |
| SPOC FFI field stars need log g at least 3.5 and crowding at least 0.8, 10,000 per CCD | U6 reported by TIC log g (dwarf vs giant) and by galactic latitude band (post hoc, labelled); expect SPOC to miss giants |
| Tmag 13.5 limit vs Gaia G under 14 | the frame is wider than the QLP limit: stars with Tmag over 13.5 cannot have QLP or SPOC light (except pm over 200 mas/yr); the preregistration states this expectation and reports the primary verdict on all 400 and a second line for Tmag at most 13.5 |
| QLP flag bit 31 | metric U9 (report only), FIX 84 candidate |
| Alias peaks 34.1, 53.7, 107.2 d | counts reported; no filter |
