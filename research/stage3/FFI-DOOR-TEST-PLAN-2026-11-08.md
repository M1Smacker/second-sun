# The full-frame door: can bright binaries with no 2-minute data feed our search? Test plan (PREREGISTRATION v1, final 8 Nov 2026, after research stint RS-012 and before any light curve was read or any sample was drawn)

**Status.** Approved by Ahmed on 8 Nov 2026 ("You have my yes, and the cap is 87%, and yeah, do this in a fresh nested one. Don't half-ass your research. Go. Take as long as you need."). This file was first drafted at 02:46 Kuwait, then amended once after research stint RS-012 (`FFI-DOOR-RESEARCH-2026-11-08.md`). The commit that carries this text is the preregistration. After it: thresholds and the sample rule do not change; a metric may be ADDED only if it is labelled "added after" with the date, and it never changes the verdict. At the moment of this commit the Gaia pixel download (catalogue rows only) was running and no catalogue row of the pool had been read; no light curve had been read or downloaded. The positions of the 111 target lists and of G1/G2/G3/Prsa/TTC/CALNet are used only for exclusions.

## Why (Ahmed, 8 Nov 2026)
"Sooner or later we are going to run out of things to search." The 2-minute lists are the easy fuel. Census (G4) uses most of the bright slow detached binaries that were ever 2-minute targets; G5 (5,000 to 10,000 stars to about G 14) needs more than that. The full-frame images (FFIs, 30, 10 or 3.3 minute light curves from QLP and TESS-SPOC) are the other door.

## What we already know (CONFIRMED from our own files and from RS-012)
- G3 already went through this door for 611 stars of the TESS Ten Thousand Catalog: 4,075 QLP files, 830 TESS-SPOC full-frame files and only 126 SPOC 2-minute files; 4,080 star-sectors searched; 13.9% to 16.1% of reads had no safe windows (`G3-PREREGISTRATION.md`, `G4-GATHER-2026-11-04.md`, `Q5-LOST-READS-2026-11-04.md`). So reading FFI light with unchanged Vesper works.
- The loader (`detect_v2.load`) reads QLP and TESS-SPOC only (flux: SPOC PDCSAP; QLP `sys_rm_flux` from Sector 56, `sap_flux` before). TGLC and ELEANOR-LITE are NOT readable (NOT TESTED).
- RS-012: QLP covers Tmag 13.5 and brighter (plus proper motion over 200 mas/yr to Tmag 15, M dwarfs to Tmag 15 from Sector 41), Sectors 1 to 104, 30 min / 10 min / 200 s by era. TESS-SPOC FFI field stars need Tmag at most 13.5, log g at least 3.5 and crowding at least 0.8, at most 10,000 per CCD; Sectors 1 to 85. Gaia periods above 5 d carry known alias peaks and the "93% agree" statistic only means less than one cycle of drift over 34 months.
- So the open questions are: (1) how many NEW bright slow binaries does the full-frame door hold that no list of ours has, (2) do usable QLP/SPOC light curves exist for them, (3) are the Gaia periods and ephemerides good enough to mask their eclipses, (4) does a known circumbinary transit survive in FFI light.

## Sample (rule fixed before looking)
1. **Frame.** Gaia DR3 `vari_eclipsing_binary` with `frequency` under 0.2 (period over 5 d) joined to `gaia_source` by 768 per-HEALPix-pixel queries (level 3; `research/stage3/ffi_door/gaia_pixels.py`). Keep rows with a G magnitude and 8 at most G under 14. Stars brighter than G 8 are left out (saturation in the FFI). This pool is also the exact bright slow pool for G5.
2. **Exclusions.** Remove any star that (a) was a 2-minute target in Sectors 1 to 111 (111 lists in `data\census_targets_2m`; Gaia position moved from 2016.0 back to the TIC epoch J2000 with pmra and pmdec, match radius 3 arcsec, and a magnitude sanity check: G minus Tmag between -0.3 and 1.8, otherwise the match must be within 1 arcsec), or (b) appears in `targets\g1_targets.csv`, `g2_targets.csv`, `g3_targets.csv`, Prsa 2022 (`data\xmatch\ebs.csv`), TTC (`data\g3\catalog_ttc\`) or CALNet (`data\calnet_2026-11-07\newecl.dat`, parsed by `census_step1/calnet_check.py`). Each exclusion is applied with every key the list has (Gaia id, position, TIC id after the TIC lookup). A star that is found in a list only after the TIC lookup is replaced by the next star of its cell reserve.
3. **Strata and quotas.** 15 cells: Gaia G bin (8 to 10, 10 to 11, 11 to 12, 12 to 13, 13 to 14) times Gaia period class (5 to 10 d, 10 to 30 d, over 30 d). The stratification uses Gaia G, not Tmag, because the pool has no Tmag before the TIC lookup. Quota 80 per G bin, split 27, 27, 26 over the period classes in that order (total 400). A cell that cannot fill its quota gives the shortfall first to the other period classes of the same G bin (nearest period class first), then to the next fainter G bin.
4. **Draw.** Within each cell, pool stars sorted by `source_id` ascending; order = `numpy.random.default_rng(20261108 + cell_index).permutation`, with `cell_index = 3 * g_bin_index + period_class_index` (both 0-based, as listed above). The first quota stars are the sample, the rest the ordered reserve. The draw script is stored in the repo before it is run (`research/stage3/ffi_door/draw_sample.py`).
5. **TIC ids.** From the MAST TIC (v8.2) by position: nearest entry within 3 arcsec of the J2000-epoch position that passes the G minus Tmag sanity window; if several, the brightest. Sample file with star ids ONLY under `data\ffi_door_2026-11-08\` (git-ignored, never public). In the repo: counts, scripts and the SHA-256 of the sample file.
6. **Pool statistics reported (counts only, from the same file).** Exact all-sky pools for period over 5 d and over 7 d at G under 12, 13, 13.5, 14, TWOGAUSSIANS against other model types, share within 1% of the Gaia alias periods 34.1, 53.7 and 107.2 d, the red-dwarf stratum (G 14 to 17, BP minus RP over 2.0 and an absolute G magnitude proxy for small radius) for the M-dwarf question of idea 1, and the survivors after each exclusion. Positive recall check (own data): of the Prsa 2022 EBs with period over 5 d and G under 14, what share is in the Gaia pool (Gaia's completeness for our class).

## Metrics (a star-sector counts as usable only if U2 and U4 hold)
Products counted for U1, U4, U6 are the two the frozen loader reads: **QLP and TESS-SPOC FFI**. TGLC and ELEANOR-LITE are reported as extra counts only.
- **U1 existence:** at least one QLP or TESS-SPOC FFI light curve in at least 2 sectors (from the per-sector target lists and MAST; counts only in stage C).
- **U2 quality:** at least 70% good cadences (finite flux after the loader's own quality mask); median 8-hour noise within 1.5 times the G3 fit at the star's Tmag (log10 noise8 = 0.26 + 0.211 x Tmag; noise8 defined as in `pipeline/horizon_reach.py` lines 36 to 60: the 6.5-hour noise of the audit scaled to 8 h).
- **U3 eclipses and ephemeris:** among "testable" stars (stars whose downloaded sectors contain at least one Gaia-predicted primary or secondary eclipse, and whose propagated Gaia ephemeris error is at most 0.25 d, see U8): the share with at least one eclipse found at SNR 7 or more, and the share whose observed eclipse time lies within 0.25 d of the Gaia prediction. Reported separately: the same on all 400, and the share of Gaia candidates with no eclipse at all in the sectors (Gaia false or blended).
- **U4 pipeline-ready:** loads with the unchanged frozen loader.
- **U5 safe windows:** share of star-sectors with safe windows under the current neighbour-window rule (G3: 83.9% to 86.1%).
- **U6 second product:** share of star-sectors with both QLP and TESS-SPOC (tier 1A or 1L possible) against one (tier 1B).
- **U7 dilution flag:** TIC contamination ratio.
- **U8 Gaia ephemeris quality (catalogue only, added from research):** propagated error of the Gaia eclipse time at the middle of each downloaded sector = frequency_error x (t_sector minus reference_time), in days (reference_time is BJD TCB minus 2455197.5), combined with `derived_primary_ecl_phase_error`; reported for the whole pool and the 400 (share with error at most 0.25 d).
- **U9 QLP quality flag exposure (added from research, report only):** in Sector 56 and later QLP files, the share of cadences whose QUALITY has bit 31 set and that survive the loader's mask (lightkurve "hard" mask misses bit 31). Never changes the verdict; FIX 84 candidate.

## Decision rule (unchanged from the draft)
Door **OPEN** if U1 at least 80% of the 400 stars, U2 and U4 at least 70% of star-sectors, U3 at least 50% of testable stars, U5 at least 80%, U6 at least 50%. **PARTIAL** if all are at least half of those thresholds; **CLOSED** otherwise. Numbers are reported whatever the verdict. Nothing about Petrova is tuned. **Stated expectation, written before the data:** the frame (Gaia G under 14) is wider than QLP's Tmag limit of 13.5, so stars with Tmag over 13.5 (and no large proper motion) cannot have QLP or SPOC light curves; the verdict is on all 400, and the second line (Tmag at most 13.5) is given to read it. SPOC is expected to miss giants (log g under 3.5) and crowded stars.

## Sector choice for stage D (fixed now)
For each star, among sectors in which a loader-readable product exists, choose 2 sectors: prefer sectors where BOTH QLP and TESS-SPOC exist; among those, rank by the number of Gaia-predicted eclipses (primary plus secondary) in the sector span, then by a seeded random key (sha256 of `20261108` and the TIC id and the sector); take the two highest. If fewer than two sectors have both products, fill from sectors with one product. Download both products for the chosen sectors. About 1,600 files at most.

## Positive control
TOI-1338 (TIC 260128333) in sectors where it has FFI light but no 2-minute light curve (sectors found in stage C from MAST): QLP and TESS-SPOC full-frame light; is a known circumbinary transit still visible (the 2-minute result of earlier work is the comparison)? Cheap, reported separately, not part of the verdict.

## Stages, cost in weekly points (UNCERTAIN; the meter moves in whole points)
| Stage | What | Points |
|---|---|---|
| A | Research stint RS-012 (cap 0.6), this plan committed as the preregistration | 0.8 |
| B | Gaia pixel queries in the background, exclusions, seeded draw of 400, TIC ids, pool counts | 0.5 |
| C | Existence census for the 400 (QLP and SPOC per-sector target lists plus MAST for sector spans), counts only | 0.3 |
| CHECKPOINT 1 | Report to Ahmed before any light-curve download | |
| K2 | RS-013 (cap 0.4), K2 archive literature | 0.3 |
| D | Download about 2 sectors per star per product (about 1,600 files, hours, MAST time-outs expected) into a new empty folder under `data\`, compute U2 to U9, positive control | 1.0 |
| E | Write-up, queue and plan changes, RESUME, ledger | 0.3 |
| Idea 1 | RS-014 (cap 0.4) plus the G5 plan note; reuses the pool of stage B | 0.5 |
Order: A, B, C, K2, checkpoint, D, E, idea 1.

## Not part of this test
Planting fakes in FFI light (completeness) is the next step if the door is OPEN; any search; any change to Petrova or the frozen loader; idea 4 (Ahmed: no).

## Risks
Gaia slow-period solutions are weaker than they look (RS-012: loose agreement test, alias peaks, completeness 25% to 50% measured only in faint crowded fields); Gaia EBs include blends (13% of literature cross-matches are not EBs); MAST time-outs (the G3 download stalled about 20 hours); a 400-star sample gives shares good to about plus or minus 5 points; Gaia DR4 (66 months) will replace DR3 and may change the pool.
