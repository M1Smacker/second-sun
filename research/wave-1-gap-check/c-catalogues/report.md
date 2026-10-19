# Wave 1c: eclipsing-binary catalogues and TESS data coverage

*Session 1c of Wave 1, 2026-10-19. Research only. Claims are numbered in `claims.md` (C1-C41), sources in `sources.md`, problems in `friction.md`, unknowns in `open-questions.md`.*

---

## In plain words (read this first)

**TESS is alive and still taking data.** It is in its *third extended mission* (EM3), which started with Sector 97 in September 2025. Right now (19 Oct 2026) it is shooting Sector 109. The newest data you can download is Sector 107 for the specially-watched stars, and Sector 108 for the big full-frame pictures. NASA's TESS office has the pointing plan written out to Sector 134 (September 2028). The money is less certain: the White House's 2027 budget request cuts NASA astrophysics by about two thirds, Congress is pushing back, and I could not find a document that says what happens to TESS specifically. **(C1-C10)**

**The list of known binary stars stops in 2024.** Binary-star catalogues are the "shopping list" for our hunt: we only search for circumbinary planets around stars we know are eclipsing binaries. The newest big list is the **TESS Ten Thousand** (Kostov et al. 2025): 10,001 checked binaries found by a neural network plus citizen scientists, from Sectors 1-82 (up to September 2024), stars brighter than magnitude 15. It also publishes ~873,000 *unchecked* stars the network flagged. The classic list (Prša et al. 2022) only covers Sectors 1-26 (up to July 2020). Every other list is smaller and specialised (hot stars, red dwarfs, eccentric orbits). **(C11-C24)**

**So there is a two-year hole.** TESS has delivered **26 more sectors (83-108, Sept 2024 to Oct 2026)** that no binary catalogue has used. And the two systematic circumbinary searches published so far (both 2026, found by session 1b) stop at Sector 79 and Sector 83. I sampled 200 stars from each list and asked MAST which sectors cover them: **about 80% of the checked TTT binaries (~8,000 stars) and ~62% of its unchecked candidates (~540,000 stars) already have at least one newer sector that nobody has catalogued or searched**, typically 1-2 sectors each, up to 10 for stars near the poles. **(C37-C40)**

**The newest sectors are unusually good for our quest.** Circumbinary planets cross their stars at irregular times, so the longer TESS stares at one spot, the better our odds. In EM3, TESS did two double-length sectors (97-98, about 8 weeks each) and then **nine overlapping "rolled" sectors (99-107)** that NASA says were "designed to detect longer period planets". In my sample about a third of known binaries fall in that block, but any one star got at most 4 of those sectors, so it is "longer than usual", not "months on end". Nobody has published a circumbinary search of any of them. **(C2, C3, C27, C40)**

**Our test set ("ground truth").** All ten Kepler circumbinary systems were re-observed by TESS, but only up to Sector 83; TESS hasn't been back to the Kepler field since. TOI-1338 has been watched in 45 sectors, most recently Sectors 97-98. TIC 172900988 has just 5 sectors (21, 44-47). So we have real TESS data, at 2-minute and often 20-second cadence, to check that our pipeline can find planets we know are there. **(C28-C31)**

**Faint stars are where the ready-made data runs out.** 63% of the binaries TTT newly discovered are fainter than magnitude 13.5 (C41). The two main ready-made light-curve sets (QLP and TESS-SPOC) stop at magnitude 13.5. TGLC and eleanor-lite go to magnitude 16, but on MAST eleanor-lite covers only Sectors 1-26 and TGLC only up to Sector 65. For fainter binaries in the newest sectors, we would have to make our own light curves from the full-frame images (TESScut makes that free and light). **(C32-C36)**

---

## 1. TESS status (as of 2026-10-19)

| Item | Value | Label | Claim |
|---|---|---|---|
| Operating? | Yes. Sector 109 (2026-10-05 to 10-31) in progress | VERIFIED (schedule) | C6 |
| Mission phase | Third extended mission (EM3), from Sector 97 (2025-09-15) | VERIFIED | C1 |
| Cycle | Cycle 9 began at Sector 108 (2026-09-07); Cycle 10 planned from S122 (2027-09-19) | LIKELY | C6 |
| Newest 2-min/20-s data in MAST | Sector 107 (ingest started 2026-10-01, completed) | VERIFIED | C4 |
| Newest FFIs | TESScut through Sector 108 orbit 2b; S109 orbit 1a early release in progress (2026-10-16); MAST now gets FFIs about weekly | VERIFIED | C4 |
| Newest Data Release Note | Sector 104, DR142, dated 2026-09-03 | VERIFIED | C5 |
| EM3 observing pattern | S97-98: 4-orbit (~8-week) sectors. S99-107: nine overlapping "rolled" sectors over the southern ecliptic mid-latitudes, "designed to detect longer period planets" | VERIFIED | C2, C3 |
| Special event | Sector 99 split around a 3I/ATLAS comet campaign ("Sector 1751", DR136) | VERIFIED | C7 |
| Targets per sector (EM3) | 13,000 at 2-min; ~2,500 at 20-s (S99, S104) | VERIFIED | C8 |
| FFI cadence | 30 min (S1-26), 10 min (S27-55), 200 s (S56+) | VERIFIED (DRN text for 200 s from EM2 on) | DRN index |
| Planned schedule | Pointings published to Sector 134 (ends 2028-09-13) | LIKELY | C6 |
| Budget | FY26 request proposed a TESS cut (~26% per one summary); Congress rejected mission terminations; FY26 enacted astrophysics ~$1.595B. FY27 request: Astrophysics -65% to ~$552M; House bill rejects that. **TESS's FY27 line not found.** | LIKELY / UNVERIFIED | C9, C10 |

**Why it matters:** the data keeps growing by about one sector a month, so any catalogue or search goes stale fast. A funding cut would freeze the archive, not delete it; everything taken so far stays public.

## 2. TESS eclipsing-binary catalogues

All counts below are from `SELECT COUNT(*)` queries I ran on VizieR, unless marked. "Downloaded" files are in `D:\second-sun\data\wave-1\<folder>\` and logged in `downloads.csv` (wave `1c`), with sizes measured on disk.

| Catalogue | Paper ID | Sectors | # EBs | Brightness | Light curves used | Where | Size (measured) | Downloaded |
|---|---|---|---|---|---|---|---|---|
| **TESS Ten Thousand (TTT)** | arXiv:2506.05631; ApJS 279, 50 (Kostov+ 2025) | **1-82** | **10,001** vetted (7,936 new + 2,065 known) + **872,720** unvetted NN candidates | Tmag < 15 (range 6.6-15) | FFI, local eleanor, 30 min / 10 min / 200 s | VizieR J/ApJS/279/50 | table2 12,823,459 B (gz); table3 398,259 B (gz); table4 221,406 B | yes, `kostov2025_ttt` |
| **TESS-EBs (TEBC)** | arXiv:2110.13382; ApJS 258, 16 (Prša+ 2022) | 1-26 | 4,584 (live site: 4,573 rows) | 2-min targets (no explicit cut) | SPOC 2-min LCFs | VizieR J/ApJS/258/16; MAST HLSP tess-ebs v1.0; tessebs.villanova.edu | 866,632 B (gz) | yes, `prsa2022_tess-ebs` |
| OBAF EBs | arXiv:2409.20540; A&A 691, A242 (IJspeert+ 2024) | first 4 years (~1-55) | 14,573 well characterised; 69,057 candidate rows | Tmag < 15, O-F stars | FFI: SPOC + QLP, years 1-4 | VizieR J/A+A/691/A242 | obaf-eb1 38,534,845 B (gz); full CSV 103 MB and parent 1.5 GB **not** downloaded | partial, `ijspeert2024_obaf` |
| OBA EBs | arXiv:2107.10005; A&A 652, A120 (IJspeert+ 2021) | 1-26 (30-min FFI) | 3,155 (VizieR corrected 2024 version: 3,425 rows) | Tmag < 15 + colour cuts | 30-min FFI (two pipelines) | VizieR J/A+A/652/A120 | 755,948 B (gz) | yes, `ijspeert2021_oba` |
| Southern EBs | arXiv:2103.09216; ApJ 912, 123 (Justesen & Albrecht 2021) | 1-13 | 748 lines in table2 | 2-min targets | SPOC 2-min | VizieR J/ApJ/912/123 | 91,256 + 53,746 B | yes, `justesen2021_south` |
| EA-type (Algol) EBs | ApJS 259, 50 (Shi+ 2022) | 1-45 | 1,626 | 2-min targets | SPOC 2-min | VizieR J/ApJS/259/50 | 199,998 B | yes, `shi2022_ea` |
| Eccentric EBs | AJ 170, 356 (Tang+ 2025) | 1-26 | 514 | 2-min targets | SPOC 2-min | VizieR J/AJ/170/356 | 176,302 B | yes, `tang2025_eccentric` |
| M+M EBs | arXiv:2508.13941 (Oddo+ 2025) | not checked here | 1,292 | low-mass pairs | (1b: TGLC FFI for their 2026 search) | not on VizieR yet | n/a | no |
| Classification of TESS EBs | arXiv:2604.26398 (Liu+ 2026) | compiled from other catalogues | 20,196 classified (13,376 EA / 2,114 EB / 4,706 EW) | n/a | ML classifier | not on VizieR yet | n/a | no |
| Gaia DR3 EB candidates | arXiv:2211.00929 (Mowlavi+ 2023) | (Gaia, not TESS) | 2,184,477 | Gaia G to ~20 | Gaia epoch photometry | VizieR I/358/veb | 393 MB gz, **not** downloaded (over limit; TAP-queryable) | no |

Smaller or older items seen in passing (not downloaded): Kostov+ 2022/2023/2025 eclipsing *quadruple* candidates from FFIs (arXiv:2202.05790, 2309.14200, 2510.27470); Battley+ 2022 CDIPS EB candidates (VizieR J/MNRAS/511/4285); Kliapets+ 2026 PLATO LOPS2 variability catalogue from TGLC light curves (G ≲ 17, 3.6 M variables incl. EBs; arXiv:2604.12758).

**Newest TESS EB catalogue cutoff: Sector 82 (TTT), ending 2024-09-05.** The TEBC on MAST is still the S1-26 v1.0 file, though its page promises FFI and newer-sector updates. **(C11-C14)**

## 3. Kepler and K2

| Catalogue | ID | Version | # EBs | Size | Downloaded |
|---|---|---|---|---|---|
| Kepler EB Catalog (Villanova), live | keplerebs.villanova.edu | **Third Revision, last update 2019-08-08** | **2,920** (CSV rows counted) | 279,027 B | yes, `villanova_kepler-ebs_live` |
| Kirk+ 2016 (paper version of rev. 3) | arXiv:1512.08830; AJ 151, 68 | 2016-08-18 snapshot | 2,876 | 103,749 B (gz) | yes, `kirk2016_kepler-ebs` |
| K2 engineering EBs | arXiv:1407.3780 (Conroy+ 2014) | | 31 | 2,016 B | yes |
| K2 Campaign 0 EBs | arXiv:1503.01829 (LaCourse+ 2015) | | (tables 1-2) | 10,256 + 7,499 B | yes |
| K2 Variable Catalogue | arXiv:1502.04004, 1512.01246 (Armstrong+ 2015, 2016) | C0-4, ML classes | not counted | | no |
| K2 C0-8 EBs + candidates | arXiv:1907.10806 (Kruse+ 2019) | | not counted | | no |

No single, maintained K2 EB catalogue exists that I could find; the Villanova K2 page returns HTTP 400. **(C25, C26)**

## 4. Coverage gap math

Cutoffs (all VERIFIED, dates from the HEASARC sector table, C27):

| Line | Last sector | Ends |
|---|---|---|
| Prša 2022 TEBC (MAST v1.0) | S26 | 2020-07-04 |
| IJspeert 2024 OBAF | ~S55 ("first 4 years", LIKELY) | ~2022-09-01 |
| Davies+ 2026 CBP search (1b) | S79 | 2024-06-18 |
| **TTT (newest EB catalogue)** | **S82** | **2024-09-05** |
| Oddo+ 2026 M+M CBP search (1b) | S83 | 2024-10-01 |
| **TESS data now public** | **S107 (2-min/20-s), S108 (FFIs via TESScut), S109 partial** | 2026-10-05 (S108 end) |

**Sectors since the newest catalogue: S83-S108 = 26 sectors (~25 months)**, plus the 7-day comet pointing "S1751" and a partial S109. Since the newest published search of normal-star EBs (S79): 29 sectors.

**How many catalogued EBs got new data since?** Seeded random samples of 200 stars per list, sector lists from the TESScut API (`coverage_sample.py`, `coverage_summary.py`, raw per-star results in `coverage_sample_*.csv`, summary in `coverage_summary_final.txt`). "New" = S83-S108. Errors are 1-sigma binomial.

| List (size) | ≥1 new sector | ≥5 new sectors | Mean new sectors / star | In EM3 block S97-107 (max per star) | Scaled to the full list |
|---|---|---|---|---|---|
| TTT vetted EBs (10,001) | 80% ± 3 | 4% ± 1 | 1.68 | 32% ± 3 (max 4) | ~8,000 EBs, ~17,000 EB-sectors never catalogued or searched |
| TTT unvetted candidates (872,720) | 62% ± 3 | 2% ± 1 | 1.37 | 24% ± 3 (max 4) | ~540,000 stars, ~1.2 M star-sectors |
| Prša TEBC (4,584), after S26 | 100% | 56% ± 4 | 7.76 | | ~4,580 EBs with data newer than the catalogue |
| Prša TEBC, after S82 | 76% ± 3 | 10% ± 2 | 2.12 | 36% ± 3 (max 4) | ~3,500 EBs; ~460 with ≥5 new sectors |

No sampled star was missing from TESS entirely (0/600). The scaled numbers are sample fraction × list size, so treat them as ±4% estimates (LIKELY), not counts.

**Stars observed per sector (for scale):** TTT says ~3 million stars brighter than Tmag 15 fall in an average sector (VERIFIED, as the paper's statement); EM3 sectors carry 13,000 2-min targets each (C8). Over 26 new sectors that is tens of millions of star-sectors of FFI data, most of it repeat visits.

**Brightness of the backlog:** 63% of TTT's 7,936 new EBs and 70% of its unvetted candidates have 13.5 < Tmag ≤ 15, i.e. fainter than QLP and TESS-SPOC's general limit (C41). For sectors after S65 they need DIY light curves.

**Concrete gap slice, with evidence:** TTT EBs (and Prša EBs) observed in Sectors 84-108, especially the 13.5-15 mag majority. No EB catalogue covers those sectors, no published circumbinary search covers them (1b), and no ready-made faint light curves exist for them on MAST. Caveat: the Tufts STANLEY GI programme (1b) may be searching part of this privately.

## 5. Ground-truth set: TESS data for known transiting CBP hosts

Queried with `ground_truth.py` (TESScut sector API for FFIs; MAST CAOM for 2-min/20-s SPOC and HLSP light curves). No light curves downloaded. Host list = the 14 transiting CBP hosts from 1a's NASA Exoplanet Archive pull, plus the Davies+ 2026 candidate.

| Host | TIC | FFI sectors (TESScut) | 2-min SPOC sectors | 20-s sectors | HLSP light curves (sectors) |
|---|---|---|---|---|---|
| Kepler-34 | 272369124 | 14, 15, 41, 54, 55, 74, 75, 81, 82 | 14, 15, 41, 54, 55, 74, 75, 81, 82 | 74, 75, 81, 82 | CDIPS: 14,15,41,54,55; TASOC: 15; TESS-SPOC: 14,15,41,54,55,74,75,81,82 |
| Kepler-16 | 299096355 | 14, 15, 26, 40, 41, 53, 54, 55, 56, 73, 74, 75, 76, 80, 81, 82, 83 | 14, 15, 26, 40, 41, 53, 54, 55, 56, 73, 74, 75, 76, 80, 81, 82, 83 | 56, 73, 74, 75, 76, 80, 81, 82, 83 | CDIPS: 14,15,26,40,41,53,54,55; QLP: 14,15,26,40,41,53,54,55,56,73,74,75,76,80,81,82,83; TARS: 14,15,26,40,41,53,54,55,56,73,74,75,76,80,81,82,83; TASOC: 14,15,26; TESS-SPOC: 14,15,26,40,41,53,54,55,56,73,74,75,76,80,81,82,83 |
| Kepler-35 | 271040768 | 14, 15, 40, 41, 54, 55, 74, 75, 81, 82 | 14, 15, 40, 41, 54, 55, 74, 75, 81, 82 | 74, 75, 81, 82 | CDIPS: 14,15,40,41,54,55; TESS-SPOC: 14,15,40,41,54,55,74,75,81,82 |
| Kepler-47 | 271548206 | 14, 15, 40, 41, 54, 55, 74, 75, 81, 82 | 14, 15, 40, 41, 54, 55, 74, 75, 81, 82 | 74, 75, 81, 82 | CDIPS: 14,15,40,41,54,55; TASOC: 14,15; TESS-SPOC: 14,15,40,41,54,55,74,75,81,82 |
| Kepler-38 | 158316612 | 14, 26, 40, 41, 53, 54, 55, 74, 75, 80, 81, 82 | 14, 40, 41, 53, 55, 74, 75, 80, 81 | 74, 75, 80, 81 | CDIPS: 40,41,53,55; QLP: 14,40,41,53,55,74,75,80,81; TESS-SPOC: 14,40,41,53,55,74,75,80,81 |
| PH1 | 170348142 | 14, 15, 41, 54, 55, 75, 81, 82 | 14, 15, 75, 81, 82 | 75, 81, 82 | CDIPS: 14,15,54,55; QLP: 14,15,41,54,55,75,81,82; TESS-SPOC: 14,15,75,81,82 |
| Kepler-413 | 298969838 | 14, 15, 26, 40, 41, 53, 54, 55, 56, 74, 75, 76, 80, 81, 82, 83 | 14, 15, 26, 40, 41, 53, 54, 55, 56, 74, 75, 80, 81, 82, 83 | 74, 75, 80, 81, 82, 83 | CDIPS: 14,15,26,40,41,53,54,55; TASOC: 14,15,26; TESS-SPOC: 14,15,26,40,41,53,54,55,56,74,75,80,81,82,83 |
| Kepler-453 | 164457525 | 14, 26, 40, 41, 53, 54, 55, 74, 75, 80, 81, 82 | 14, 26, 40, 41, 53, 54, 55, 75, 80, 81, 82 | 75, 80, 81, 82 | CDIPS: 26,40,41,53,54,55; QLP: 14,40,41,53,54,55,75,80,81,82; TARS: 14,26,40,41,53,54,55,75,80,81,82; TASOC: 14,26; TESS-SPOC: 14,26,40,41,53,54,55,75,80,81,82 |
| Kepler-1647 | 170344769 | 14, 15, 41, 54, 55, 74, 75, 81, 82 | 14, 15, 41, 54, 55, 74, 75, 81, 82 | none | CDIPS: 14,15,41,54,55; QLP: 14,15,41,54,55,74,75,81,82; TESS-SPOC: 14,15,41,54,55,74,75,81,82 |
| Kepler-1661 | 164886585 | 14, 26, 40, 41, 53, 54, 74, 75, 80, 81 | 14, 26, 40, 41, 53, 54, 80, 81 | none | CDIPS: 26,40,41,53,54; TARS: 14,26,40,41,53,54,75,80,81; TASOC: 14,26; TESS-SPOC: 14,26,40,41,53,54,80,81 |
| TOI-1338 A | 260128333 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 61, 62, 63, 64, 65, 66, 67, 68, 69, 87, 88, 89, 90, 93, 94, 95, 96, 97, 98 | 4, 5, 6, 7, 8, 9, 10, 11, 12, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 61, 62, 63, 64, 65, 66, 67, 68, 69, 87, 88, 89, 90, 93, 94, 95, 96, 97, 98 | 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 97, 98 | CDIPS: 27,28,29,30,31,32,34,35,36,37,38,39; GSFC-ELEANOR-LITE: 1,2,3,4,5,6,7,8,9,10,11,12; QLP: 1,2,4,5,6,7,8,9,10,11,12,27,28,29,30,31,32,34,35,36,37,38,39,61,62,63,64,65,66,67,68,69,87,88,89,90,93,94,95,96,97,98; T16: 1,2,4,5,6,7,8,9,10; TARS: 1,2,3,4,5,6,7,8,9,10,11,12,27,28,29,30,31,32,34,35,36,37,38,39,61,62,63,64,65,66,67,68,69,87,88,89,90,93,94,95,96; TASOC: 1,2,3,4,5,6; TESS-SPOC: 1,2,4,5,6,7,8,9,10,11,12,27,28,29,30,31,32,34,35,36,37,38,39,61,62,63,64,65,66,67,68,69; TGLC: 1,2,4,5,6,7,8,9,10,11 |
| TIC 172900988 Aa | 172900988 | 21, 44, 45, 46, 47 | 44, 45, 46, 47 | none | QLP: 21,44,45,46,47; TARS: 21,44,45,46,47; TESS-SPOC: 21,44,45,46,47 |
| TIC 319011894 (Davies+2026 candidate) | 319011894 | 7, 87 | 7 | none | GSFC-ELEANOR-LITE: 7; QLP: 7; T16: 7; TESS-SPOC: 7; TGLC: 7 |

FFI cadence by sector: 30 min (S1-26), 10 min (S27-55), 200 s (S56 on).

**What it means:** every known transiting CBP host has TESS data at 2-min cadence, and most at 20-s, so the ground-truth test is possible today. But the Kepler hosts have no data after Sector 83, and TIC 172900988 none after Sector 47. TOI-1338 is the one host with data from the newest era (S87-98). **(C28-C31)**

## 6. Light curves for faint EBs

| Product | Brightness limit | Sectors on MAST | Notes | Label |
|---|---|---|---|---|
| SPOC 2-min / 20-s | selected targets only (13,000 + ~2,500 per EM3 sector) | 1-107 | the "watched stars" | VERIFIED |
| QLP | **Tmag < 13.5** | tables through Year 8 (S97-107) | MIT; the bulk FFI set most people use | VERIFIED limit / LIKELY latest |
| TESS-SPOC FFI | ≤ 10,000 targets per CCD per sector; Tmag ≤ 13.5 plus special cases | tables through Year 7 (S84-96) | SPOC-quality FFI light curves | VERIFIED as stated |
| **TGLC** | **Tmag ≤ 16**, ~2% precision at 16 even in crowded fields | Years 1-5 (S1-65) listed; S12-55 bulk curl only | Gaia-informed PSF fits; best ready-made faint product | VERIFIED as stated |
| **GSFC eleanor-lite** | **Tmag < 16** | **S1-26 only** (S14-26 bulk only) | >150 M light curves | VERIFIED |
| T16 | T < 16 | Cycle 1 only | difference imaging | VERIFIED |
| CDIPS | cluster members | S1-55 | young-cluster stars only | LIKELY |
| DIY from TESScut | any | through S108 orbit 2b | what TTT did (local eleanor to Tmag 15) | VERIFIED (TESScut range) |

**Gap:** for EBs with 13.5 < Tmag < 16 observed after Sector 65, no ready-made light curve exists on MAST that I could find. TTT's paper states the same for its motivation (QLP stops at 13.5). **(C15, C32-C36)**

## 7. Search cutoffs seen in passing (session 1b has the details)

- Davies et al. 2026 (arXiv:2604.09435): 512 detached TEBC EBs, TESS-SPOC FFI, through **Sector 79**.
- Oddo et al. 2026 (arXiv:2610.22625): 1,291 M+M EBs, TGLC, **Sectors 1-83**.
- TTT itself (catalogue, not a planet search) through **Sector 82**.

So the newest data any published circumbinary search used ends at **Sector 83 (2024-10-01)**, and only for red-dwarf pairs.

## 8. Method notes and limits

- Counts: VizieR TAP `COUNT(*)`, run 2026-10-19. Sizes: bytes on disk after download.
- 14 data files first came back as a 4,396-byte CDS bot-challenge page; caught because every size was identical, deleted, re-fetched (see friction.md). Every file in the table above was checked to be real data (gzip opened, line counts match VizieR).
- Coverage estimate is from random samples (seeded, reproducible), not the full catalogues.
- Not checked: ADS-only items (conference abstracts), journal machine-readable tables not mirrored at VizieR.
