# Claims: burn-2-reading

All checked 2026-10-19 (UTC). ADS = NASA ADS API record fetched by `ads_watch.py` (outputs in this folder).

| # | Claim | Source ID + link | Label |
|---|---|---|---|
| R1 | Martin's 2024 NASA XRP proposal plans to run STANLEY on "almost 3,000 Kepler binaries" (archival Kepler data) and "over 10,000 TESS binaries" over two years | 2024xrp..prop..113M https://ui.adsabs.harvard.edu/abs/2024xrp..prop..113M | LIKELY (proposal abstract) |
| R2 | No ADS record (paper/abstract/proposal) describes a CBP transit search of Kepler-field EBs using TESS data | 3 ADS queries, ads_adhoc_1.txt and ads_adhoc_2.txt | VERIFIED (query run; absence of evidence only) |
| R3 | Davies+ 2026 is published in MNRAS 548 (June 2026) | 2026MNRAS.548ag743D / arXiv:2604.09435 | VERIFIED (ADS record) |
| R4 | Oddo+ "Occurrence of CBPs around TESS M-dwarf EBs" is an Oct 2026 eprint; Oddo+ AAS 243 (2024) abstract described the search; Dragomir FINESST 2022 funded "Finding the Frequency of Tatooines" | arXiv:2610.22625; 2024AAS...24344504O; 2022fine.prop..258D | VERIFIED (ADS records) |
| R5 | Dunning+ (AAS 245, Jan 2025): visual CBP search of >11,000 TESS EBs with P > 6 d, 1 new candidate | 2025AAS...24516010D https://ui.adsabs.harvard.edu/abs/2025AAS...24516010D | LIKELY (abstract) |
| R6 | Zhang (AAS 246, 2025): BLS+CNN "BLSiNet" blind search of the whole Kepler EB catalog, 2 strong candidates | 2025AAS...24614414Z | LIKELY (abstract) |
| R7 | Esmer+ (AAS 247, Jan 2026): ETV survey of a majority of TESS EBs in all released sectors; >2,000 targets with FAP < 1e-6 periodicities | 2026AAS...24713506E | LIKELY (abstract) |
| R8 | Haghighipour 2022 XRP proposal: apply the "multiple transits in one conjunction" method to 300,000 TESS EB light curves; no CBP-search results by him found in ADS 2023-2026 | 2022xrp..prop..190H; author query in ads_adhoc_5.txt | LIKELY (proposal) / VERIFIED (query) |
| R9 | Mullally+ (AAS 246, 2025): transit search of Kepler-observed stars with TGLC TESS light curves on AWS, using KOIs/EBs as ground truth; not a CBP search | 2025AAS...24633707M | LIKELY (abstract) |
| R10 | Thornton+ 2026 MNRAS 548: 27 candidate CBPs via apsidal precession of TESS EBs | 2026MNRAS.548ag515T / arXiv:2512.07934 | VERIFIED (ADS record, title) |
| R11 | No refereed 2026 ADS record announces a new confirmed circumbinary planet | ADS queries in ads_adhoc_1.txt, ads_adhoc_2.txt | LIKELY (ADS lag; no arXiv sweep) |
| R12 | SPOC TPS declares a TCE with MES > 7.1, passing consistency tests and at least two transits (Kepler needed three) | Guerrero+ 2021 arXiv:2103.12538 §5.1.1 | VERIFIED (full text) |
| R13 | Prime-mission SPOC multi-sector runs: S1-2, 1-3, 1-6, 1-9, 1-13, 14-16, 14-19, 14-23, 14-26; a target joins a later run only with new sectors | Guerrero+ 2021 §5.1.2 | VERIFIED (full text) |
| R13b | QLP and SPOC both need ≥2 transits for a TCE and do not purposely produce single-transit candidates | Guerrero+ 2021 §10.6 | VERIFIED (full text) |
| R14 | SPOC multi-sector S14-78 (DR113): 2-min targets only, 27,374 targets, 6,631 with TCEs, 12,595 TCEs, 7.1σ, ≥2 transits, periods up to the 1,769-d baseline, 10-min binned search | NASA NTRS 20250008654, tess_multisector_14_78_drn113_v04.pdf | VERIFIED (full text) |
| R15 | Published SPOC multi-sector TCE ranges include S1-96 and S14-86 as the newest; single-sector TCEs to S107 | https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_tce.html (raw HTML grep) | VERIFIED |
| R16 | Norazman+ 2025 searched 15,477,322 eleanor-lite 30-min light curves (9,224,280 TICs), T < 13, S1-26 | arXiv:2508.04673 §2, §4 | VERIFIED (full text) |
| R17 | Their vetting funnel ends at 6 candidates (incl. β Pic); cuts: SNR > 5, duration > 0.4 d, depth < 1%, common-time cut, skew > 0, α > 1.02, skew < 8 | arXiv:2508.04673 Table 1, §4 | VERIFIED (full text) |
| R18 | Method: 2.5-d sliding median (wotan), T-statistic over 0.1-2.5 d windows, single strongest event per LC, Gaussian vs skew-Gaussian asymmetry ratio | arXiv:2508.04673 §3 | VERIFIED (full text) |
| R19 | Occurrence rate 2.64e-4 per star per year vs Kepler 6.7e-6 | arXiv:2508.04673 abstract, §6.3 | VERIFIED (full text) |
| R20 | Authors estimate ~2.6 million more star-years in S27-82 to T = 13 from the QLP target list | arXiv:2508.04673 §7.2 | VERIFIED (full text) |
| R21 | Code at github.com/azibn/automated_exocomet_hunt; repo has no licence (API license: null), last push 2026-06-25 | paper Data Availability; GitHub API | VERIFIED |
| R22 | Authors are exploring CNNs; Cody+ (in prep) ran parallel work and Cody holds a 2020 XRP "hidden occulters" project | arXiv:2508.04673 §4, §7.2; 2020xrp..prop..135C | VERIFIED (text) / LIKELY (proposal) |
| R23 | Zieba+ 2019: three asymmetric dips 0.5-2 mmag, up to ~2 d, at β Pic after pre-whitening 54 δ Scuti modes over 105 d | 2019A&A...625L..13Z / arXiv:1903.11071 | LIKELY (abstract) |
| R24 | Capistrant+ 2022: 293 TESS dipper stars (234 new) from visual survey | 2022ApJS..263...14C / arXiv:2209.03379 | LIKELY (abstract) |
| R25 | Tajiri+ 2020: 35 dippers from year-1 TESS FFIs via CNN | 2020ApJS..251...18T / arXiv:2009.12830 | LIKELY (abstract) |
| R26 | QLP stitches all sectors, BLS 0.1 d to half baseline, TCE at SNR > 9 and BLS significance > 9 | Guerrero+ 2021 §5.2.1 | VERIFIED (full text) |
| R27 | KIC 8610483 b: non-transiting CBP via ETVs from Kepler + TESS + ground data (P ~390 d, ~45 Earth masses) | 2025AAS...24524910M | LIKELY (abstract) |
