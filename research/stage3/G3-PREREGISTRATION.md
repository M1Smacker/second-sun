# G3 preregistration (written 2 Nov 2026 BEFORE any G3 light curve exists on this PC)

**Status: LOCKED FOR THE DOWNLOAD by Ahmed's words below; the SEARCH is a separate step that needs his explicit go and a frozen version (section 4).** A change now needs a new dated amendment at the bottom, never an edit of the rules above it.

## 1. Purpose
The G2 sealed slice (594 stars) is spent for Vesper 0.8.0, and the G2 development slice was used for tuning. G3 is a third set of stars, defined before any of its light is downloaded or read, so that a frozen version is tested once on stars it never saw. Win condition (Ahmed, 29 Oct 2026, unchanged): a clean measured null, that is, how small a planet the chain could have found plus an honest count of what was found. A candidate would be welcome but is not the target. Interesting signals are not discoveries.

## 2. The star list (fixed by these hashes)
- Source: table 3 (7,936 new eclipsing binaries) of the TESS Ten Thousand Catalog, Kostov et al. 2025, ApJS 279, 50 ([arXiv:2506.05631](https://arxiv.org/abs/2506.05631)), CC BY 4.0, downloaded 2 Nov 2026 (`data/g3/catalog_ttc/table3_new_ebs.txt`, 2,002,473 bytes, sha256 e197c05c167225bf9d5ca1bb3a5b9e672d76b9b938168b7a44c7382768fd0fb6).
- Rule: one row per TIC; binary period over 7 days; Tmag 13.5 or brighter; TIC not in `targets/g1_targets.csv` (sha256 38ad01b2d1ceca7abb6e30bbf984f5debe1cdff10fcbc5910e341269b8ce87c9), `targets/g2_targets.csv` (sha256 809212e5ef3ac1ecd77de99989aab89ba935cc97cebbb62d3fe6e651641f8bb6) or the saved Prsa 2022 table `data/xmatch/ebs.csv` (sha256 933e635c0370ee436fafbca250869e13067ddad22b13aecfd1d9e44f1e5d4087). The period bar is the one the G2 search used for its long-period emphasis; the magnitude bar is the G2 one. The catalogue has no morphology column, so no detachedness cut is applied (for these stars the primary eclipse lasts a median 2% of the orbit, so none would be removed by a duration cut of 10% of the orbit).
- The list is `targets/g3_targets.csv`, made by `pipeline/targets_g3.py`: **612 stars**, sha256 **38b04f11d5e6b9085d2ba7e8a472288b7cb0540dfd2cc5a29ccc977ea458b8ef** (hash of the file as written, with LF line endings). It contains no light curve, no event and no search result. The catalogue counts 3,718 star-sectors for these stars (median 4 sectors per star); 451 of the 612 have Gaia RUWE 1.4 or less (RUWE is kept as a covariate, not a cut).
- Known circumbinary hosts and TOIs inside the list are labelled, never removed; their counts are measured after the download, from `data/xmatch` tables, and reported.

## 3. No split
All 612 stars are the untouched test. There is no development slice: no tuning, no looking at any event or picture, and no search before the version is frozen. Completeness (`chain_recovery.py`, unchanged logic) is run on 300 random star-sectors of G3 AFTER the search, as for the G2 sealed slice, and the null is stated together with that table.

## 4. The version and the one-shot rule
The search uses ONE frozen version, decided by Ahmed before any G3 file is opened: Vesper 0.8.0 (frozen, hash 5f73692944aad8ee9df795100488ee1522b8e7f0c8cfeb3d898fc2e9bf653d0a) or Vesper 0.9 (0.8.0 plus dg, nd and fl at 0.5, accepted on the development slice by `V9-STUDY-PLAN.md`, NOT yet frozen). Freezing 0.9 changes the code hash (the `FLARE_ASYM` constant and the data-path switch for G3 in `dataset.py`); for that reason neither file is edited tonight. The regression (zero difference 300 of 300 on G1) is re-proved after the last code change and before any G3 file is read. The search runs once; if a bug is found afterwards, the fixed version is run again and BOTH results are reported with the reason.

## 5. What counts as an excess (unchanged from G2 section 5, decided before any G3 result exists)
Per flux half and per SNR bar (7, 8, 10, 12): the real tier 1 count against the noise-expected count (upside-down count divided by the real-to-upside-down ratio measured by `asymmetry_test.py` on the G3 run itself). An **excess** needs the Poisson chance of at least the observed real count to be 0.01 or less at the SNR 7 bar, with the real count above the noise-expected count at the other bars. Anything less is **no excess**. Report lines S1 to S8 of `G2-SEALED-PLAN.md` keep their pass marks, and the scorecard-plus lines A to E of `SCORECARD-AMENDMENTS.md` (Amendment 2) are printed with them, in stars and not only in events, as pre-specified reporting, not as new decisions.

## 6. Reporting rules
Aggregates only. No real event is opened or plotted without Ahmed's explicit yes. Labels CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED. Each result is also split by labels (TOI, NASA-listed circumbinary host, none) as in G2.

## 7. Known limits of this design (said now)
- **Faint stars.** Median Tmag 12.8. Most star-sectors will have only QLP or TESS-SPOC full-frame light, no 2-minute SPOC product, so most events cannot be confirmed by a second product (tier 1B) and the completeness floor is higher than for G2: G3 tests larger planets. The completeness table will say how large.
- **QLP windows depend on the manifest** (FIX-QUEUE item 70): QLP-only star-sectors borrow good-time windows from neighbouring stars in the run's manifest. The manifest hash of the G3 run is recorded; a fix (a hashed windows table per star list) is a separate change before the freeze.
- **Catalogue caveats (the paper's own):** ephemerides may be slightly off for shallow, few-eclipse targets; the sector range is stated two ways (1 to 82 in the abstract, 1 through 26 in the summary; UNCERTAIN); no completeness or false-positive rate is given; about one in four of the new binaries has Gaia RUWE above 1.4, so many sit in multiple systems.
- **The same star can have different files later** (MAST reprocessing); the download manifest and file hashes are kept.

## Lock record
Written and committed 2 Nov 2026 BEFORE the first G3 light-curve download. Ahmed's words, 2 Nov 2026, about 05:00 Kuwait, answering my night question 2 ("may I treat that list as locked by you and download the G3 light curves tonight?"; my default had been no): "All of your questions go with what you think is right. I have read all of them. And you can download them tonight. It's fine." and "Download it when you can, when you like." The commit that contains this record is the lock commit: find it with `git log -- research/stage3/G3-PREREGISTRATION.md`. His go for the SEARCH has NOT been given. Amendments go below this line, dated.
