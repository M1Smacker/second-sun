# Second Sun: independent deep review (answer to the 2026-10-23 brief)

*Written 2026-10-23 by Claude (research session with web search, a clone of the public repo at commit `210218e`, and a Python sandbox). Nothing was posted, submitted or sent anywhere. No GPL code is reproduced here.*

**How to read the tags.** `[READ]` means I opened the primary source in this session and it says this. `[MEMORY]` means it comes from my training and I did not open it now. `[INFERRED]` means my own reasoning or my own calculation (the scripts are attached, so every `[INFERRED]` number can be re-run). `[RAN]` means I executed code in this session and this is the output. Where a journal reference is `[MEMORY]` but the arXiv paper is `[READ]`, check the bibcode in ADS before citing.

**What I could and could not reach.** I could clone GitHub repos (yours, `bdrdavies/mono-cbp`, `TKleanthousT/stanley_cbp`, `lightkurve`, `tessgi/ticgen`) and read arXiv, HEASARC, MIT TESS, AAS and NASA NTRS pages. ExoFOP, VizieR/CDS and the Villanova site refused automated access (robots), so anything that needed them is listed in section 9 with the exact search for you to run.

---

## 1. Top 10 findings, ranked by how much they change your odds of a real, credited result

### 1.1 The detector returns zero events on every 30-minute light curve (a silent bug)
`detect_v2.bin10` bins to 10 minutes and marks empty bins NaN; `box_scores` then refuses any box with less than 80% bin coverage (`min_cover=0.8`). With 30-minute cadence only one 10-minute bin in three has data, so coverage is about 33% and every box is NaN `[INFERRED from the code, lines 152-181]`. I tested it: the same 8-hour, 1,500 ppm dip (SNR about 23) is found at 2-minute, 200-second and 10-minute cadence and gives **no event at all** at 30-minute cadence `[RAN: test_cadence.py]`. TESS full-frame images were 30-minute in sectors 1 to 26 (your claim F-012) `[READ: your register]`. In G1 that is sectors 14, 15, 16, 19 and 26: **890 of 5,081 QLP star-sectors (17.5%)**, 333 TESS-SPOC star-sectors, and 596 star-sectors where no SPOC 2-minute file exists to fall back on `[RAN: on targets/g1_coverage.csv]`. It would also kill your planned Kepler re-find test, because Kepler long cadence is 29.4 minutes `[MEMORY]`. No error is raised; the star simply looks quiet. This is the single most important thing in this review.

### 1.2 For QLP sectors before 56 the loader silently uses the flux that eats long transits
`detect_v2.load` (line 46) picks the first of `sys_rm_flux`, `det_flux`, `kspsap_flux` that exists. lightkurve's own QLP reader documents that the detrended columns are called `kspsap_` in sectors 1 to 55 and `det_` from 56, and that `sys_rm_flux` exists only from sector 56 `[READ: lightkurve src/lightkurve/io/qlp.py, commit f762d52]`. So for every QLP file before sector 56 your loader falls through to `kspsap_flux`, which is the same spline detrending you measured eating about 70% of a 6-hour dip in `det_flux` (overnight report section 9) `[READ: your report]`. Huang et al. say QLP's spline uses a minimum break-point spacing of 0.3 days and warn that "more aggressive splines would lead to the distortion of long-duration transits" `[READ: arXiv:2011.06459]`. In G1 that is **2,845 of 5,081 QLP star-sectors (56%)** `[RAN]`. Your QLP recipe was validated on one sector (S98), which is post-56 and so had `sys_rm_flux` `[READ: your report 9c]`. Together with 1.1, roughly half of the QLP data would be searched with a depth-killing flux or not at all.

### 1.3 Your search is still mostly novel: at most 30 of the 549 stars were in Davies et al.
Davies et al. drew their sample from the TESS Eclipsing Binary Catalogue of Prša et al. 2022 (4,584 EBs), kept morphology < 0.5 and P > 7 d (591 systems), removed six with known planets and vetted by eye down to 512; they searched TESS-SPOC FFI light curves "up to and including Sector 79", preferring SAP flux `[READ: arXiv:2604.09435]`. They did not publish the 512 TIC list in the paper `[READ]`, but their GitHub repo ships `catalogues/TEBC_morph_05_P_7.csv` (592 rows, 591 TICs), which is the pre-vetting cut `[READ: mono-cbp commit 8d373b4]`. **Cross-matched with `targets/g1_targets.csv`: 30 G1 stars appear in it** (list in section 3), so the overlap with the final 512 is at most 30, about 5.5% of G1 `[RAN]`. The reason is structural: the TESS EB catalogue was built from 2-minute targets in the primary mission (the catalogue's Kepler-field members list only sectors 14, 15, 26) `[READ: the CSV's sectors column]`. Three things remain open: the by-eye survey of more than 11,000 TESS EBs with P > 6 d (Dunning et al. 2025 AAS abstract, from your burn-2 report, which I did not re-open); the Tufts/Martin programme, whose TESS GI proposals G06010 and G07004 ("A Next Generation Circumbinary Planet Search With TESS") use STANLEY but do not state their sample `[READ: HEASARC G06010.txt, G07004.txt]`; and the TESS Ten Thousand catalogue (10,001 EBs from FFI sectors 1 to 82), whose neural network recovered 1,371 of 2,458 Kepler EBs with T < 15 as candidates `[READ: arXiv:2506.05631]`. Martin is a co-author of the new Oddo et al. occurrence-rate paper, so his group is actively running single-transit TESS searches `[READ: astrobiology.com summary of arXiv:2610.22625]`.

### 1.4 A defensible expected yield is about 0.2 to 0.5 detectable new planets, so roughly 20 to 40% for at least one candidate
My arithmetic is in section 4. In short: Martin (2017) estimates that the Kepler EBs hide about 17 to 30 more circumbinary planets like the known ones that were not transiting during Kepler `[READ: arXiv:1611.00526, abstract and Table 2]`; 43% of the CBP-eligible Kepler EBs (detached, P > 5 d) are in G1 `[RAN]`; a Monte Carlo over precession, TESS's actual Kepler-field sector dates, transit chance and your measured noise gives 0.47 to 0.71 expected detectable switch-ons `[RAN: yield.py]`; after vetting losses and a discount for the Saturn-sized term that visual surveys would probably already have seen, λ ≈ 0.23 to 0.5, so P(at least one) ≈ 21 to 39%, with a plausible range of about 8 to 55% `[INFERRED]`. Your 15% (4 to 35%) is on the pessimistic side but not unreasonable. The biggest single contribution is a Kepler-16-b-like planet, which is the kind most likely to have been noticed by eye already.

### 1.5 Five known CBP hosts are in G1, and they are your best built-in negative controls
Kepler-16 (TIC 299096355, T 10.94), Kepler-38 (TIC 158316612, T 13.43), Kepler-64/PH1 (TIC 170348142, T 13.31), Kepler-453 (TIC 164457525, T 13.03) and Kepler-1647 (TIC 170344769, T 13.11) are all in `g1_targets.csv` `[RAN]`. Martin (2017) predicts no TESS transits for Kepler-16, -64, -453 and -1647, and 3 TESS transits for Kepler-38 b `[READ: arXiv:1611.00526 Table 2]`, whose 0.05% mean depth `[READ: Davies Table 2]` is far below your floor at T 13.4 `[INFERRED]`. Battley et al. note Kepler-34's transits are not expected again until 2066 `[READ: arXiv:2103.03259]`. So any event your pipeline finds on these five stars is, with high probability, a false alarm: a free measurement of your false-alarm behaviour on real Kepler-field CBP hosts.

### 1.6 The false-alarm budget will swamp human vetting unless you add a cross-star "common-time" veto
Your flipped-data rates are 0.6 per sector on TOI-1338 PDCSAP, 0.25 to 0.3 per sector on Kepler-16, and about 0.25 per sector for TOI-1338 SAP + HARD `[READ: your results files and F-016, F-058]`. G1 has about 5,100 star-sectors, so expect roughly **1,200 to 3,000 flipped-type events at SNR 7**, plus as many again in the real data `[INFERRED]`. Gaussian statistics are irrelevant at this threshold: about 800 independent box trials per star-sector, about 4 million in the campaign, give an expected 5 × 10⁻⁶ pure-noise exceedances at 7σ and about 1 at 5σ `[INFERRED]`. Your threshold is set entirely by systematics. Davies et al. handle this with the "Skye" metric: group events within 0.1 d in each sector and flag groups that are >3σ outliers across the sector `[READ: arXiv:2604.09435]`; STANLEY did the same on Kepler by finding 35 times where many of 270 binaries dipped and cutting them from every light curve `[READ: arXiv:2101.03186 §2.8.3; the list ships as stanley_cbp/Databases/common_false_positives.csv]`. With 549 stars spread over a few cameras per sector, a common-time veto is cheap and is standard practice.

### 1.7 Your sensitivity on G1 will be worse than on TOI-1338, and about 120 to 170 rows are a poor match to the method
TOI-1338 is T ≈ 11.5, R ≈ 1.3 R☉, uncrowded, in the southern continuous viewing zone with 40 sectors `[READ: your files]`. G1's median T is about 12.5, half the stars have one or zero SPOC sectors, and the median QLP coverage is 9 sectors `[RAN]`. Using the Stassun et al. 1-hour noise model scaled by your measured red-noise factor (β ≈ 1.4 reproduces your 6 R⊕ floor on TOI-1338), the single-transit floor at SNR 7 for a 6-hour transit across a 1 R☉ star is about 4.0 R⊕ at T 11, 6.2 at T 12.5 and 8.7 at T 13.5; for a 1.5 R☉ primary in an equal-light twin it is 8.5, 13.2 and 18.4 R⊕ `[INFERRED: sens.py]`. About 40% of the 14 known transiting CBPs would be detectable in a single transit if placed around G1-like stars at G1's magnitudes `[INFERRED]`. Separately, 170 G1 rows have a catalogued primary eclipse longer than 15 hours (127 longer than 24 h) and 121 have a TIC radius above 3 R☉ `[RAN, using the Villanova table shipped in STANLEY]`: mostly giants or long-period systems where a 2-day biweight cannot follow the eclipses and any planet transit would be shallow and longer than your 15-hour maximum box `[INFERRED]`. These deserve their own track or a low rank.

### 1.8 The literature backs your SAP result, and SPOC's bit 4096 is brightness-dependent
Davies et al. preferred SAP "owing to spurious transit-like features appearing in the PDCSAP flux" and say "the PDC process increases the scatter of the photometry" `[READ: arXiv:2604.09435 §3]`. The Kepler EB catalogue team wrote that because PDC is optimised for transits "its effects on eclipsing binary data are found to be adverse" and used calibrated (SAP) flux only `[READ: Slawson et al., arXiv:1103.1659]`. SPOC's bit 13 (value 4096, "Scattered Light Exclude") is set per target when the background exceeds twice its baseline **and** exceeds a fraction (0.25 in that release) of the target's flux, and it is applied only to PDCSAP, whose flagged cadences remain available in SAP `[READ: TESS DRN for the S14-19 reprocessing, NTRS 20205007589, §2.4.1, §2.5]`. That second criterion means faint stars lose more PDCSAP cadences than bright ones `[INFERRED]`, which matters for G1, where half the sample is fainter than T 12.5.

### 1.9 Box durations: add 1.5 to 2.5 hours and 18 to 24 hours; search for pairs, not just singles
Kepler-47 d's transits last 0.10 to 0.20 d (2.4 to 4.8 h) and Kepler-47 b's and Kepler-413 b's go down to 0.12 d (2.9 h) `[READ: Davies Table 2]`. For a G1-like binary (P_bin 7 d, 1.2 + 0.8 M☉, R_A 1.2 R☉, planet at 5 P_bin) the fastest central transit lasts about 3.4 h and a b = 0.7 one about 2.4 h; the slowest central transit lasts about 18 h `[INFERRED: section 5.4]`. Your grid stops at 3 and 15 hours. Kostov et al. 2020 found that 4 of 11 Kepler CBP systems show multiple transits in one conjunction, typically a few days apart, and proposed finding TESS CBPs from such pairs within one sector `[READ: arXiv:2008.02756]`. A pair search at a lower per-event threshold is a real sensitivity gain at almost no cost (section 5).

### 1.10 G1 has two unique assets nobody else has: Kepler's four years and TESS's return in 2027
A planet that transits now but was not seen during Kepler constrains its precession phase (Martin 2017's whole framework) `[READ: arXiv:1611.00526]`, and Kepler's 4-arcsecond pixels and its EB catalogue let you check whether a neighbour inside TESS's 21-arcsecond pixels is itself a known eclipsing binary `[INFERRED]`. And the Kepler field comes back: TESS has not observed it since sector 86 (December 2024), with sectors 87 to 110 all southern or ecliptic `[READ: HEASARC sector table]`, but sector 119 (3 to 29 July 2027) has camera 2 at RA 280.4°, Dec +50.4° and sector 120 (29 July to 23 August 2027) has camera 2 at RA 291.1°, Dec +53.0°, both within about 9° of the Kepler field centre, so at least part of the field is very likely inside a 24° camera; confirm star by star with tess-point before relying on it `[READ: tess.mit.edu sector pages; coverage INFERRED]`, and Cycle 10 (sectors 122 to 132, from September 2027) is northern again `[READ: HEASARC Cycle 10 page]`. A candidate published with a predicted window before mid-2027 can be tested by TESS itself. That is a strong argument for not letting the hold run past early 2027.

---

## 2. Bugs or likely bugs in the code

I separate **bugs** (wrong result against your own stated intent) from **design choices**. Line numbers refer to commit `210218e`.

### 2.1 Bugs

**B1. `detect_v2.bin10` + `box_scores`: no events on 30-minute data (high).** Explained in 1.1. Test: `test_cadence.py` (attached; stubs out lightkurve, imports your module, runs `find_events` on synthetic 2-min, 200-s, 10-min and 30-min data). Output `[RAN]`: 2-min SNR 21.0, 200-s 24.0, 10-min 24.7, 30-min no event, finite-bin fraction 0.33. Fix options: bin to `max(10 min, cadence)`, or define `min_cover` against the expected number of cadences in the box rather than 10-minute bins. Re-run the test after the fix and add it to your self-check.

**B2. `detect_v2.load`, line 46: QLP column choice is sector-dependent and wrong before S56 (high).** Explained in 1.2. Test: for one G1 star with QLP files in S40 and S80, print the column `load` chooses; inject the same 8-h transit into `sap_flux` and compare the depth recovered through each column. Fix: for S < 56 use `sap_flux` plus your own detrend plus the borrowed SPOC windows (your 9d recipe), and write the chosen column into every results row so it can never change silently.

**B3. `targets_g1.py`: extra catalogue periods are dropped, so their eclipses are never masked (medium).** The selection keeps only rows that pass the cut. Two G1 stars have another catalogue period that fails it: **KIC 4150611** (1.5223 d, dropped by P > 5; its 8.653 d and 94.198 d rows are kept) and **KIC 7622486** (2.28 d, morph 0.59, dropped; its 40.2465 d row is kept) `[RAN: on research/wave-3-pipeline/g1_tmag.csv]`. In a synthetic test, an unmasked 1.52-d, 0.4% binary on top of an 8.65-d one gives 175 SNR ≥ 7 events in 12 sectors `[RAN: test_mask2.py]`. Loud, but it will waste vetting time and could hide a real event. Fix: build the mask per star from **all** catalogue periods.

**B4. `detect_v2.veto`, lines 231-232: flipped-match events are auto-rejected, contrary to the "flags, not deletions" rule in brief §4.7 (medium).** A real transit within 0.3 d of a positive bump (a flare, a scattered-light ripple, a momentum-dump excursion) is deleted with no human ever seeing it. Test: inject 6 to 8 R⊕ transits at 0.05 to 0.3 d from each flipped-data event in your TOI-1338 and Kepler-16 runs and count how many `veto` rejects. Fix: make it a flag until that test shows the loss is negligible.

**B5. `detect_v2.load`: a SPOC file whose PDCSAP column is entirely NaN returns no data, silently (low).** If PDCSAP is all NaN (for example bit 32768, "Insufficient Targets for Error Correction", which nulls PDCSAP per the DRN `[READ: NTRS 20205007589 §1]`), the code takes the QLP branch, finds none of the QLP columns, falls back to `"flux"`, which lightkurve fills from `pdcsap_flux` for SPOC files `[READ: lightkurve io/tess.py line 11]`, and returns empty arrays. Fix: fall back explicitly to SAP and log it.

### 2.2 Design choices I would make differently

**D1. One global noise value per sector and duration (`box_scores`, line 180).** Boxes with 80 to 99% coverage get the same σ as full boxes, although their white-noise σ is larger by up to √(1/0.8) ≈ 1.12, and noise near orbit starts and gaps is higher than mid-orbit `[INFERRED]`. For a 15-hour box a 25-day sector holds only about 40 independent boxes, so the MAD itself scatters by roughly ±20% sector to sector `[INFERRED]`. Davies use a MAD in a sliding 4-day window `[READ]`. A local σ (for example per 13.7-day orbit, or a 3 to 4 day sliding window) and a coverage correction √(w/n) are cheap.

**D2. Duration grid 3 to 15 h (`DURS_H`).** See 1.9 and 5.4.

**D3. `eclipse_mask_auto` folds after a 2-day biweight.** I tried hard to break it with white noise: it masked every in-eclipse point for P = 12, 60, 150 and 300 d, for 0.2 to 0.3% secondaries at 3,000 ppm noise, for an eccentric secondary at phase 0.37, and for catalogue period errors of 0.0005 to 0.002 d at P = 12 d over 12 G1-like sectors `[RAN: test_mask.py, test_mask2.py]`. It fails, loudly (40 to 115 events of SNR about 500), only when the accumulated drift over 2019 to 2024 exceeds roughly an eclipse width (0.01 d error at P = 12 d, 0.004 d at P = 5.5 d) `[RAN]`. So I no longer think this is your weakest link for ordinary stars. It is weak for the 127 rows with eclipses longer than 24 hours, where a 2-day biweight follows the eclipse itself `[INFERRED]`. Use the catalogue's own `pwidth`, `swidth` and `sep` for those (section 5.3).

**D4. Kepler-16 dry-run uncertainty resolved.** Your global fold found runs at phases 0.472-0.478, 0.638-0.640 and 0.962-0.967 (dry-run report) `[READ]`. The Villanova table gives Kepler-16 a secondary 0.4885 of an orbit after the primary, 1.7% deep and 0.0043 of an orbit wide `[READ: stanley_cbp/Databases/villanova_orbit_data_kepler.csv]`. 0.475 + 0.4885 = 0.9635, so the 0.962-0.967 run is the secondary and the 0.638-0.640 run is not an eclipse `[INFERRED]`.

**D5. `systematics()` needs a SPOC file.** 237 G1 stars have neither SPOC nor TESS-SPOC `[RAN]`. Momentum dumps are spacecraft-wide events `[MEMORY]`, so borrow dump times from any SPOC file of the same sector rather than skipping rule C7.

**D6. Injection tests are not G1-shaped.** Your realistic N-body test used TOI-1338's 40 CVZ sectors `[READ: F-029]`. A G1 star typically has 9 QLP sectors spread over 5.4 years (a duty cycle of about 12%) `[RAN]`. Run injections on real G1 stars with their actual products and sectors, through the full chain including `veto`, or every "nothing found" will be over-interpreted.

---

## 3. Overlap and novelty (brief 6.1)

**Davies et al. 2026.** Method and sample are in 1.3 `[READ]`. The 30 G1 stars present in the mono-cbp pre-vetting list (TIC, Kepler period, TEBC period):

| TIC | KIC | Tmag | P Kepler (d) | P TEBC (d) | TEBC sectors |
|---|---|---|---|---|---|
| 268380299 | 9851142 | 7.32 | 8.4803 | 8.4808 | 14,15 |
| 63126950 | 8560861 | 8.28 | 31.9732 | **30.2993** | 14,15 |
| 27915909 | 10987439 | 10.39 | 10.6746 | 10.6742 | 14,15 |
| 137549183 | 3120320 | 10.39 | 10.2656 | 10.2660 | 14 |
| 269031095 | 9913481 | 10.57 | 7.0095 | 7.0094 | 14,15 |
| 169467727 | 5982353 | 10.79 | 19.5631 | 19.6333 | 14,15 |
| 272720444 | 8703887 | 10.89 | 14.1710 | 14.1690 | 14,15 |
| 63071165 | 10274244 | 11.00 | 13.6837 | 13.6839 | 14,15 |
| 63291675 | 10601579 | 11.19 | 8.0988 | 8.0982 | 14,15 |
| 121866154 | 4737302 | 11.19 | 9.4556 | 9.4557 | 14 |
| 270700608 | 8823868 | 11.32 | 23.8761 | 23.8711 | 14,15 |
| 27845677 | 11923819 | 11.34 | 33.1595 | 33.1609 | 14,15 |
| 138639253 | 6131659 | 11.54 | 17.5278 | 17.5281 | 14,15 |
| 159573299 | 6859813 | 11.59 | 10.8824 | 10.8828 | 14 |
| 121122016 | 4142768 | 11.61 | 27.9916 | **13.8503** | 14 |
| 184008771 | 5632781 | 11.65 | 11.0252 | 11.0251 | 14,15 |
| 394179202 | 3335816 | 11.66 | 7.4220 | 7.4242 | 14 |
| 184298625 | 4281895 | 11.70 | 9.5436 | 9.5412 | 14 |
| 273376048 | 10616656 | 11.72 | 25.2853 | **12.5689** | 14,15 |
| 27397122 | 11820830 | 11.75 | 12.7319 | 12.7336 | 14,15 |
| 159720778 | 8364119 | 11.89 | 7.7359 | 7.7360 | 15 |
| 27006880 | 11817750 | 11.90 | 9.7626 | 9.7631 | 14,15 |
| 271040947 | 9777062 | 11.92 | 19.2300 | 19.2308 | 14,15 |
| 170246850 | 6228703 | 11.95 | 8.4004 | 8.4002 | 14,15 |
| 272074664 | 9353182 | 11.96 | 10.4763 | 10.4761 | 14,15 |
| 158491288 | 9579192 | 11.99 | 12.0835 | 12.0835 | 14,15,26 |
| 275576176 | 9834257 | 12.02 | 15.6514 | 15.6441 | 14,15 |
| 271773721 | 9474969 | 12.04 | 21.5705 | 21.5732 | 14,15 |
| 416635004 | 10753734 | 13.03 | 19.4067 | 19.4063 | 14,15 |
| 170344769 | 5473556 | 13.11 | 11.2588 | 11.2593 | 14,15 |

`[RAN: cross-match of g1_targets.csv with mono-cbp/catalogues/TEBC_morph_05_P_7.csv]`. The last row is Kepler-1647, which Davies may have removed as a known planet host `[INFERRED]`. Three TEBC periods disagree with Kepler's (bold): two are almost exactly half and one is 5% short `[RAN]`, which is a reminder to trust Kepler's 4-year periods over TESS-catalogue ones `[INFERRED]`. For these 30 stars, Davies covered sectors up to 79 `[READ]`, so your new data for them is sectors 80 to 83 and 86 `[INFERRED]`. Note that mono-cbp is GPL-3.0 `[READ: its LICENSE]`, so read it, run it as a separate tool if useful, but do not copy it into your MIT repo.

**Tufts / Martin.** The cycle 6 and 7 GI programmes are titled "A Next Generation Circumbinary Planet Search With TESS" and aim to "more than double" the known CBPs with STANLEY `[READ: G06010.txt, G07004.txt]`. I could not establish their targets: the sector 81 GI list (`GI_S081.csv`) shows no G06010 or G07004 rows in the first part I could read, which is inconclusive `[READ, partial]`. "Over 10,000 TESS binaries" matches the size of the TESS Ten Thousand catalogue (10,001 EBs, sectors 1 to 82, includes Kepler-field recoveries as a benchmark) `[READ: arXiv:2506.05631]`, so assume the Kepler field is at least partly in their sample until shown otherwise `[INFERRED]`. Martin's group has also just published the first TESS CBP occurrence upper limit (M-dwarf EBs, 33% at 95% for coplanar 2 to 16 R⊕ planets up to 600 d, one new candidate) `[READ: astrobiology.com summary of arXiv:2610.22625; I was rate-limited on arXiv itself]`. I found no Tufts results paper on Kepler-field EBs.

**Others.** Kostov's group found TIC 172900988 b by eye in the GSFC TESS EB catalogue and reports that "nearly all" transit-like events in that EB catalogue were false alarms after vetting `[READ: arXiv:2105.08614, paraphrased by the fetch tool]`. Planet Hunters TESS is finished ("out of data") `[READ: Zooniverse FAQ]`. The Borkovits group has already measured eclipse timing for the whole Kepler EB sample with TESS through sectors 80 to 83 (243 triple candidates) `[READ: arXiv:2502.09480]`. I found no announced CBP candidate around a G1 star in these sources; I could not check ExoFOP CTOIs (section 9).

**Sector coverage and where your edge is.** From your own coverage file the Kepler-field sectors present are 14, 15, 16, 19, 26, 40, 41, 53, 54, 55, 56, 60, 73, 74, 75, 76, 78, 80, 81, 82, 83 and 86 (some only for a few stars) `[RAN]`, and nothing after 86 until mid-2027 `[READ: HEASARC sector table]`. Your edge: (a) the roughly 519 G1 stars outside Davies' sample; (b) sectors 80 to 83 and 86 for everyone; (c) QLP-only and fainter stars (Davies used TESS-SPOC only); (d) the Kepler-era constraint and the 2027 return (1.10) `[INFERRED]`. NASA's SPOC and QLP pipelines need at least two transits `[READ: your burn-2 summary of Guerrero et al. 2021]`, so single circumbinary transits are outside their reach by design.

---

## 4. Sensitivity and expected yield (brief 6.2)

### 4.1 Detectable size versus magnitude
Model: 1-hour noise σ₁ₕ(T) from the Stassun et al. polynomial (coefficients as coded in `tessgi/ticgen`, which cites "arxiv.org/pdf/1706.00495" `[READ]`), multiplied by a red-noise factor β; box noise σ_D = β σ₁ₕ / √(D / 1 h); detection if depth ≥ 7 σ_D; depth = dilution × (R_p/R★)². σ₁ₕ = 203, 336, 431, 595, 810, 1,122 and 1,584 ppm at T = 10, 11, 11.5, 12, 12.5, 13 and 13.5 `[RAN]`. β = 1.37 reproduces your TOI-1338 result (6 R⊕, 6.4 h, 1.31 R☉, recovered at SNR 7.2 to 7.9) `[INFERRED]`; Kepler-16's 908 ppm per hour after your 2-day flatten (F-039 and brief) implies β ≈ 2.8 on that star `[INFERRED]`.

Minimum single-transit radius in R⊕ (β = 1.4, 6-hour transit) `[RAN: sens.py]`:

| Host | T = 10 | 11 | 11.5 | 12 | 12.5 | 13 | 13.5 |
|---|---|---|---|---|---|---|---|
| 1.0 R☉, no dilution | 3.1 | 4.0 | 4.6 | 5.3 | 6.2 | 7.3 | 8.7 |
| 1.0 R☉, equal-light twin | 4.4 | 5.7 | 6.5 | 7.5 | 8.8 | 10.3 | 12.3 |
| 1.5 R☉, no dilution | 4.7 | 6.0 | 6.9 | 8.0 | 9.3 | 11.0 | 13.0 |
| 1.5 R☉, equal-light twin | 6.6 | 8.5 | 9.7 | 11.3 | 13.2 | 15.5 | 18.4 |

With β = 1.0 (what your SAP numbers suggest is possible in some sectors) divide by about 1.18 `[INFERRED]`. QLP: the same photon-noise model applies to FFI photometry `[INFERRED]`; your one QLP test recovered TOI-1338 b at SNR 10.9 versus 9.0 in SPOC once SPOC's good-time windows were imposed `[READ: your report 9d]`, so QLP is not intrinsically worse; its systematics are the problem.

### 4.2 Fraction of the known population detectable
Using the 14 planets' actual mean depths and duration ranges `[READ: Davies Table 2]`, a single transit at SNR ≥ 7 with β = 1.4 is detectable for 12 to 14 of 14 at T = 10, 10 to 12 at T = 11, 5 to 8 at T = 12 and 2 to 3 at T = 13 `[RAN]`. Weighted by G1's magnitude distribution that is about 40%; if G1 primaries are about 1.3 times larger than the Kepler hosts (depth ∝ R★⁻², √duration ∝ R★^½, so SNR ∝ R★^-1.5) it drops to about 30% `[INFERRED]`.

### 4.3 Expected number of new planets (show the arithmetic)
1. **Hidden planets.** Martin (2017) Table 2 gives, per known system, the expected number E of similar planets around Kepler EBs that were not transiting during Kepler: Kepler-16 0.9, -34 3.4, -35 0.8, -38 0, -47b 0, -47c 3.9, -64 1.5, -413 0.7, -453 6.0, -1647 13.2 `[READ]`. Sum: 30.4, or 17.2 without Kepler-1647 `[INFERRED]`. Caveat: the paper's F = max(1 − D, 1) is written so it always equals 1, probably a typo, so treat E with caution `[READ: the fetch tool flagged this; I agree INFERRED]`.
2. **Share in G1.** Of 961 Kepler EBs with measured morphology 0 to 0.5 and P > 5 d, 416 (43.3%) have T ≤ 13.5 `[RAN: g1_tmag.csv]`. Hidden planets around G1 stars: 0.433 × 30.4 ≈ 13.2 (7.4 without Kepler-1647) `[INFERRED]`.
3. **Switch-on and observation.** For each analogue I drew a random precession phase, gave it two transitable windows per cycle of length f T_prec / 2 (Martin's T_prec and primary-star percentage), kept only cases not transitable during Kepler (2009.37 to 2013.36), required a transitable window to overlap TESS's Kepler-field era (2019.54 to 2024.97), placed it on a random G1 star with that star's real QLP sectors (HEASARC dates), assumed a 70% chance of a transit at each conjunction inside a window, and required SNR ≥ 7 with the noise model above `[INFERRED: yield.py]`. Probability per hidden analogue `[RAN]`: Kepler-16-like 0.45 to 0.48, -35-like 0.11 to 0.23, -34-like 0.04 to 0.09, -64-like 0.04 to 0.13, -453-like 0.06 to 0.08, -47c-like about 0.005, -1647-like 0 (precession 7,189 yr). Expected detectable switch-ons: **0.47 to 0.71** depending on β (1.0 or 1.4) and host size (1.0 or 1.3 times) `[RAN]`.
4. **Vetting and discount.** Multiply by 0.6 to 0.8 for surviving vetting `[INFERRED]`. The Kepler-16-like term (about 0.18 of the total) is a 1.8%-deep Saturn `[READ: Davies Table 2]`, which visual surveys of TESS EBs would very likely have noticed; halving it gives λ ≈ 0.23 to 0.5 `[INFERRED]`.
5. **Result.** P(at least one) = 1 − e^(−λ) ≈ **21 to 39%**; with E halved and pessimistic choices about 8%, with E × 1.5 and β = 1 about 55% `[INFERRED]`.

Cross-check from the other direction: Armstrong et al. give 10.0 (+18, −6.5)% for R > 6 R⊕, P < 300 d if coplanar `[READ: arXiv:1404.5617, MNRAS 444, 1873 per RERO]`. 549 × 10% ≈ 55 such planets, of which a quarter or so would have been transitable during Kepler `[INFERRED]`, about 11 to 14 visible; G1 actually has 4 known planets of ≥ 6 R⊕ (Kepler-16, -64, -453, -1647) `[RAN membership; radii MEMORY]`. G1 therefore looks like the lower part of Armstrong's range, consistent with Martin's ratio of roughly 2 to 3 hidden per visible `[INFERRED]`. Two warnings: if B1 and B2 are not fixed, cut λ roughly in half; and the yield counts only primary-star transits `[INFERRED]`.

---

## 5. Method improvements (brief 6.3 to 6.6)

Each item: expected gain, effort, risk, and whether it is **standard** practice or **my idea**.

### 5.1 Noise and data choices (6.3)

**Search SAP with the DEFAULT mask, use PDCSAP and QLP as confirmation, not as an AND gate.** Gain: on TOI-1338 SAP + HARD recovered 7 of 8 published transits against PDCSAP's 4 `[READ: F-054]`. Effort: small. Risk: SAP keeps scattered-light ramps; handle with 5.1.3. Standard (Davies, Slawson; 1.8). Requiring two products to both exceed SNR 7 multiplies two detection probabilities and loses real planets; instead require the second product to show a consistent dip at the same time (for example SNR ≥ 3 to 4 and consistent depth) `[INFERRED, my idea]`. Your C8 rule already does the vetting version of this.

**Why PDCSAP can be noisier for EBs.** Published statements: PDC "increases the scatter" and creates "spurious transit-like features" `[READ: Davies]`; PDC is "adverse" for EBs `[READ: Slawson]`. Plausible mechanisms (not proven): the cotrending fit is driven by the eclipses, which dominate the variance, and imprints basis-vector structure on hour-to-day scales `[INFERRED]`; crowding correction scales depth and noise equally, so it cannot change SNR on its own `[INFERRED]`. Cheap test: compute PDCSAP minus scaled SAP for S6, S34, S37 versus S65, S98 and look at its power on 3 to 15 hour scales; also read the PDC header keywords (`PDCMETHD`, and the PDC goodness metrics such as `PDC_TOT`, `PDC_NOI`) for those sectors `[MEMORY: keyword names; check one header]`.

**Quality bits.** Bit 12 (2048, "Stray light from Earth or Moon in camera FOV") is predicted, disabled in 2-minute products since the 2020 reprocessing, and the DRN asks users to inspect FFIs before removing bit-12 images `[READ: NTRS 20205007589 §2.4.1]`. Bit 13 (4096, "Scattered Light Exclude", SPOC ≥ 4.0.5) is per target, background-based, PDCSAP-only `[READ: DRN; MAST "2.0 Data Product Overview" table]`. MAST's suggested starting mask is bits 1, 2, 3, 4, 5, 6, 8, 10, 13 and 15 `[READ: MAST page]`; lightkurve's DEFAULT is the same minus bit 13, and HARD adds bits 7, 11, 12 and 13 (values 64, 1024, 2048, 4096) `[READ: lightkurve utils.py]`. In QLP files bit 13 means something else, "low precision" across a CCD (sectors 1 to 55), and lightkurve uses bit 31 for that from sector 56 `[READ: lightkurve io/qlp.py; arXiv:2011.06459]`. Professionals searching EBs: Davies used SAP with lightkurve "hard" `[READ]`; Norazman et al. added their own per-camera MAD flag for scattered light (from your burn-2 report, not re-opened). My suggestion: SAP + DEFAULT + your own cross-star "bad time" mask built per sector and camera (the Skye idea, 5.6) `[INFERRED]`. Gain: recovers the S30/S62-type crossings without letting scattered light through blindly. Effort: medium. Risk: low.

**Detrending window.** Your own numbers show strong noise between 0.25 and 2 days on Kepler-16 (573 versus 908 ppm per hour) `[READ: F-039, brief]`. Option: detrend separately per searched duration with a window of about three times that duration (minimum 0.5 d) and run each box length on its own detrended curve `[my idea, close to standard]`. Wōtan's authors conclude that a time-windowed biweight is "the ideal method" for transit searches `[READ: arXiv:1906.00966]`; I believe the paper recommends a window of about three times the transit duration, but the fetched text did not show that sentence `[MEMORY]`. Davies run 21 windows from 1 to 3 days and keep events found in at least 18 `[READ]`. Gain: up to about 1.6× lower noise for 3 to 6 hour boxes on active stars `[INFERRED]`. Effort: small (wotan is fast). Risk: about 10% depth loss at 3 × duration; measure it with injections. Masking eclipses before detrending, which you already do, is right; full binary modelling is unnecessary for detached P > 5 d systems, and a GP is expensive with little expected gain `[INFERRED]`.

**QLP pitfalls.** QLP's spline detrending suppresses long transits (min spacing 0.3 d) `[READ: arXiv:2011.06459]`, apertures are chosen by magnitude, the TIC version changed at sector 14, and scattered-light residuals remain after background subtraction `[READ: same]`. Your window-borrowing recipe is good; extend it to pre-56 sectors with `sap_flux` (B2).

**Noise estimate.** Sound in principle (it includes red noise), but see D1 for coverage and non-stationarity. With few independent long boxes it is also noisy itself; a per-orbit or sliding-window σ helps `[INFERRED]`.

### 5.2 Eclipse masking (6.4)

**Ephemeris drift.** Drift after N cycles is N σ_P (plus σ_T0). The Kepler EB catalogue has a period-error column ranging up to 0.0147 d `[READ: VizieR J/AJ/151/68 ReadMe, e_Per]`. Because `eclipse_mask_auto` folds TESS data only (about 1,950 days), what matters is (1,950 / P) × ΔP against the eclipse width. My tests: safe up to at least 0.002 d at P = 12 d; fails loudly at 0.01 d `[RAN]`. Action: compute (1,950/P) × e_Per for every G1 row from your local Villanova CSV (if it has the error column) and list rows where it exceeds a quarter of the eclipse width `[INFERRED]`.

**ETVs and apsidal motion.** Light-travel-time amplitudes for a solar-mass triple are at most about 4 minutes for a 1-year outer orbit and about 18 minutes for a 10-year one `[READ: Borkovits et al. 2016, arXiv:1510.08272]`, small against your 1.5-width padding. About 9% of Kepler EBs (243) are triple candidates, and the newer study used TESS through sectors 80 to 83 `[READ: arXiv:2502.09480]`. In the TESS northern CVZ the same group saw two EBs whose eclipses vanished and seven with depth changes, caused by inclination change from non-coplanar third bodies `[READ: arXiv:2604.04004]`. 145 of the 249 G1 rows with a catalogued secondary are eccentric by more than 0.02 in phase separation and 94 by more than 0.1 `[RAN]`, so apsidal motion is relevant for many; per-sector re-finding of each eclipse's phase (as `eclipse_mask` does for the primary) handles it.

**Use the catalogue's own eclipse geometry.** The Villanova table distributed with STANLEY (MIT) has `pdepth`, `sdepth`, `pwidth`, `swidth` and `sep` for 2,909 Kepler EBs, and matches 551 of your 552 rows `[READ, RAN]`. That gives you widths and the secondary phase without auto-detection, and an independent check on `eclipse_mask_auto`. Standard. Effort: small. Your own downloaded Villanova CSV may already contain these columns `[INFERRED]`.

**The "morph = -1" rows.** Of 136, 70 have no positive primary depth in that table (for example KIC 8112039, which I recognise as the heartbeat star KOI-54 `[MEMORY]`), and only 11 are deeper than 1% `[RAN]`. These are probably non-eclipsing or heartbeat systems, where the binary inclination is not guaranteed near 90°, so CBP transits are less likely `[INFERRED]`. Keep them, rank them low.

**The right control for eclipse leakage.** Your flipped test cannot see leakage, as you say `[INFERRED, agree]`. Two cheap controls: (1) histogram all events by distance to the nearest eclipse in units of eclipse width, against the same histogram for the searched exposure, and look for excess near the mask edges; (2) inject transits uniformly in binary phase, including just outside the mask, and measure recovery and false-event rate versus phase `[my idea, standard in spirit]`. A third, harsher one: rerun with the mask built from a deliberately wrong period (for example P × 1.07) and confirm the pipeline screams; that tells you how a missed eclipse would look `[my idea]`.

**Half or double periods; one visible eclipse.** Folding at P/2 or 2P still places all eclipses at fixed phases, so masking works `[INFERRED]`. A non-integer period error (like TEBC's 30.30 versus Kepler's 31.97 d for KIC 8560861) is what breaks it `[RAN, INFERRED]`. Eccentric systems with one visible eclipse need nothing extra unless the second eclipse appears later through apsidal or inclination change, which the leakage histogram would catch `[INFERRED]`.

### 5.3 Long eclipses and giants
For the 127 rows with eclipses longer than 24 hours, either mask from catalogue widths with a detrend window of at least three times the eclipse width, or treat them as a separate, low-priority track `[INFERRED]`. Their planet transits would also be long and shallow `[INFERRED]`.

### 5.4 Detection method (6.5)

**Minimum duration.** For circular orbits, duration ≈ 2R_A √(1 − b²) / v_rel, with v_rel between v_p − v_A and v_p + v_A. Worked case (P_bin 7 d, 1.2 + 0.8 M☉, R_A 1.2 R☉, P_p 35 d): v_p ≈ 82 km/s, v_A ≈ 56 km/s, so 3.4 h (b = 0) or 2.4 h (b = 0.7) at the fast extreme and about 18 h at the slow extreme `[INFERRED]`. Add 1.5, 2 and 2.5 h boxes and 18, 21 and 24 h boxes (with a 3-day window for those) `[INFERRED]`. Gain: Kepler-47 d-like short transits become reachable; Davies found recovery depends strongly on duration `[READ via your review of their abstract]`. Risk: more trials, slightly more false alarms.

**Pairs within one conjunction.** Published: Kostov et al. 2020 (4 of 11 Kepler systems; few-day spacing; method for single TESS sectors) `[READ]`; Haghighipour's 2022 XRP proposal (from your burn-2 report). Implementation: for each event, search ±(1 to 2) P_bin at a lower threshold (SNR ≥ 4 to 5) for a second dip consistent with crossing either star; combined SNR ≈ √(SNR₁² + SNR₂²), so two SNR-5 dips give about 7.1 `[INFERRED]`. Gain: probably the cheapest sensitivity improvement available. Effort: small.

**Single transits.** Best practice in this exact niche is Davies' chain: event detection, detrending robustness, model comparison against sinusoid, step and line (ΔAIC ≤ −2), duration < 1 d, and manual inspection `[READ]`. Add your C4 test (duration allowed by circumbinary geometry) and, uniquely for G1, the Kepler non-detection constraint `[INFERRED]`.

**STANLEY calibration.** STANLEY's significance is an SDE: SNR divided by its standard deviation in rolling segments across the period grid, with SDE ≳ 8 taken as significant, at least three roughly consistent transits required, and injections done by scaling known Kepler transits, a planet counting as detected if more than half its transits are found `[READ: arXiv:2101.03186 §3.4, §3.5, §4.2]`. The current package computes this in its analysis module by detrending the per-period maximum σ and normalising by a robust scatter `[READ: stanley_cbp Stanley_Functions.py, Search_Create1dSDE_wotanPoly]`. Your 90 to 100 d grid is too narrow for an SDE to mean anything; run a broad grid (about 4 P_bin to several hundred days) and calibrate the maximum SDE per star with flipped or time-scrambled data and with injections `[INFERRED]`. Bigger point: with G1's roughly 12% duty cycle a 150-day planet transiting throughout 2019 to 2024 gives about 1.6 observed transits on average `[INFERRED]`, so the three-transit requirement makes STANLEY useful mainly for short-period planets around short-period binaries in G1 `[INFERRED]`.

**SNR 7 and look-elsewhere.** See 1.6. Set the threshold so that the expected flipped-data count after automated vetoes is something a human can review (for example under 100 events for the campaign), measured on a 50-star pilot `[INFERRED]`.

### 5.5 Vetting a candidate around two stars (6.6)
Standard tests and how they behave here `[INFERRED unless tagged]`: odd-even and secondary-eclipse tests are meaningless for a single CBP event; replace them with "duration and depth consistent with crossing star A or B at this binary phase" (shorter near primary-eclipse phase for crossings of the primary; your F-023 `[READ: your register citing Kostov 2020]`). Centroid and difference images are essential: TESS pixels are about 21 arcseconds `[READ: your F-024]` and Kepler-16 alone has 15 catalogued stars within 1 arcminute `[READ: your F-035]`. Kostov et al. vetted TIC 172900988 b with photocentre, PSF-width and background checks, four independent eleanor extractions, a contamination estimate and AO imaging `[READ: arXiv:2105.08614]`. Tools: triceratops needs a period and assumes a single host `[READ: your wave-4 note; INFERRED]`, so treat its FPP as unreliable here; LATTE (LGPL, per your wave 4) is built for inspecting single TESS events (dumps, centroids, nearby stars, per-pixel light curves) `[MEMORY]`; DAVE is stale. The Kepler-field-specific test: cross-match every Gaia source inside the TESS aperture against the Kepler EB catalogue and the Kepler target list; a known Kepler EB neighbour whose ephemeris matches the event kills it `[my idea]`. A published false-positive fraction for CBP single-transit candidates: I did not find one; the best statement is Kostov's "nearly all" `[READ]`. A pixel or difference-image test should be required before anything is called a candidate `[INFERRED]`.

### 5.6 Cross-star systematics veto (the Skye idea)
Group all events (and flipped events) from all G1 stars by sector and camera in 0.1-day bins; flag bins whose count is an outlier `[READ: Davies' method]`. Build a "common false-positive times" list as STANLEY did for Kepler `[READ: arXiv:2101.03186]`. Gain: probably removes most of the 1,200 to 3,000 false alarms. Effort: small. Risk: a real event coinciding with a bad time is flagged, not deleted.

---

## 6. Validation design: re-finding Kepler CBPs (brief 6.7)

**Fix B1 first.** Kepler long cadence (29.4 min) hits exactly the 30-minute bug.

**Data.** Kepler long-cadence light curves, all quarters, via lightkurve (`author="Kepler"`, 1,800 s exposure) `[MEMORY: parameter names]`. Run two arms: SAP (what Davies and the Kepler EB team used `[READ]`) and PDCSAP. Davies split each quarter into four equal pieces `[READ]`; at minimum detrend per quarter, because the spacecraft rolls every quarter and the target lands on a different CCD with a different aperture and crowding `[MEMORY]`.

**Systems and answer key.** From Davies Table 2 `[READ]`:

| Planet | P_bin (d) | Mean depth (%) | Duration (d) | Transits in Kepler (N_tr) |
|---|---|---|---|---|
| Kepler-16 b | 41.08 | 1.80 | 0.31-0.43 | 7 |
| Kepler-34 b | 27.80 | 0.28 | 0.16-0.47 | 9 |
| Kepler-35 b | 20.73 | 0.40 | 0.18-0.49 | 7 |
| Kepler-47 b | 7.45 | 0.08 | 0.12-0.37 | 25 |
| Kepler-47 d | 7.45 | 0.16 | 0.10-0.20 | 7 |
| Kepler-38 b | 18.80 | 0.05 | 0.35-0.84 | 13 |
| Kepler-64 b | 20.00 | 0.11 | 0.45-0.51 | 10 |

Start with Kepler-16, 34, 35 as you planned; add Kepler-47 d (short durations) and Kepler-64 b (long, shallow) as hard cases. **Transit times:** the arXiv versions of Doyle et al. 2011 and Welsh et al. 2012 contain no per-transit time table (Welsh's supplement tabulates stellar eclipse times only; it gives Kepler-35's primary-transit intervals as 127.3, 122.1 and 126.2 d) `[READ: arXiv:1109.3432, arXiv:1204.3955]`. Options: (a) the journal supplements (Science 333, 1602 for Doyle 2011 `[MEMORY]`; Nature 481, 475 for Welsh 2012 `[READ: IPAC record 2012Natur.481..475W]`), which I could not open; (b) build your own key: these transits are high SNR in Kepler, so locate each by eye near the dates implied by the discovery figures, fit a trapezoid, and label the result as your measurement, checking the count against N_tr above. Option (b) is honest and quick if labelled correctly `[INFERRED]`.

**Score.** Per planet: fraction of answer-key transits recovered within half a duration (Davies' TESS criterion `[READ]`). Compare with Davies: at least 50% for each planet and above 75% for 9 of 14 `[READ via your verified review of their abstract]`; they report ≲80% for Kepler-38 b, -413 b, -47 d and -47 b (SNR ≲ 8), 2 of 3 for Kepler-1647 b and low efficiency for Kepler-64 b `[READ: arXiv:2604.09435 §5, via fetch tool]`. I could not extract their per-planet bar chart (Figure 7) as numbers `[READ: it is an image]`. Also count false events per 90-day quarter, for comparison with your TESS rates.

**Pitfalls.** The 30-minute bug; a 3-hour box is only 6 Kepler cadences; Kepler quality flags differ from TESS (use lightkurve's Kepler bitmask); four years means about 15 times more trials than one TESS sector; crowding changes by quarter, so depths do too `[INFERRED, MEMORY]`.

**The more useful variant (my idea).** Cut each real Kepler CBP transit out of the Kepler light curve (after removing the binary) and inject that real shape into real G1 TESS light curves at G1 magnitudes and sector coverage. That tests your actual problem: realistic CBP transit shapes in realistic G1 noise.

**Negative controls.** Run the five G1 known-host stars (1.5) and KIC 7289157 (catalogue periods 5.27 d and 242.71 d `[RAN]`; the long one is CBP-like timing from a third star `[INFERRED]`).

---

## 7. Target ranking (brief 6.8)

Rules with sources, then a suggested score.

| Factor | Direction | Source |
|---|---|---|
| P_bin 7 to about 45 d | favour | All known Kepler CBPs orbit binaries with P > 7 d; a third star may explain the lack around tighter ones `[READ: Martin, Mazeh and Fabrycky 2015, MNRAS 453, 3554 per RERO]`; hosts span 7.45 to 41.08 d `[READ: Davies Table 2]` |
| Shorter P_bin within that range | favour | Precession period T_prec = (4/3)(P_p⁷/P_bin⁴)^(1/3) × (M_A+M_B)²/(M_A M_B) × (1−e_p²)²/cos ΔI `[READ: Martin 2017 Eq. 15]`; with P_p ≈ 5 P_bin, T_prec scales with P_bin, so short binaries switch on and off faster, and have more conjunctions in TESS's duty cycle `[INFERRED]` |
| Brighter T, more sectors, SPOC 2-min available | favour | section 4 `[INFERRED]` |
| Small primary radius | favour | depth ∝ R★⁻² `[INFERRED]`; TIC radii of unresolved binaries are biased high `[INFERRED]` |
| Giant or eclipse > 24 h | strongly disfavour | 1.7, 5.3 `[INFERRED]` |
| morph = −1 with no positive depth | disfavour | 5.2 `[INFERRED]` |
| Known tertiary (ETV) | mild disfavour, never exclude | Martin et al. 2015 third-star argument `[READ abstract]`; PH1 b is in a quadruple `[READ: your F-059 and the VSG paper]` |
| High Gaia RUWE | flag only | your settled rule |
| Mass ratio, eccentricity | no rule | hosts range q 0.20 to 0.97 `[READ: Davies Table 2]`; no evidence for a cut |
| Kepler-era CBP or ETV claims (e.g. KIC 5095269 and KIC 7177553 are in G1 `[RAN]`) | look first | individual papers not checked here |

Suggested score (my idea, to be tuned on injections): expected number of detectable transits = (TESS days observed / P_p,typ) × P(transit per conjunction) × P(SNR ≥ 7 at this T, R★, dilution), with P_p,typ = 5 P_bin, multiplied by a prior of 1 for P_bin 7 to 45 d, 0.3 for 5 to 7 d or 45 to 100 d, 0.1 beyond, and 0.2 for giants or long eclipses. Use it to order the work, not to drop stars.

---

## 8. Credited outcomes even without a planet (brief 6.9)

| Outcome | What it needs | Time | Who publishes | Precedent | My view |
|---|---|---|---|---|---|
| **Upper-limit / null-result paper**: "no CBP larger than X R⊕ crossed in sectors 14 to 86 for N Kepler EBs" | Fixed pipeline, injection-recovery on real G1 stars, false-alarm budget, honest completeness | 2 to 4 months after the search | RNAAS (short) or MNRAS/AJ (full) | Oddo et al. 2026, the first TESS CBP occurrence limit `[READ]`; Martin and Fabrycky 2021 published "no new planets in existing systems" `[READ: title]` | **Best credited outcome.** G1's Kepler pedigree makes the limit unusual |
| **RNAAS note** on one result (e.g. the TOI-1338 b sector 98 transit time) | One clean measurement with honest errors | weeks | RNAAS: free, up to 1,500 words, one figure or table, editor-moderated not peer-reviewed, DOI and ADS-indexed `[READ: AAS guidelines]` | many | Check first whether the BEBOP or Kostov teams have already reported S98 |
| **Updated Kepler EB ephemerides / ETVs** | eclipse timing | months | | Borkovits et al. 2025 already did the Kepler EB sample with TESS to sectors 80 to 83 `[READ: arXiv:2502.09480]` | **Low novelty now.** Use their results as an input instead |
| **AAVSO VSX submissions** | new variables in your apertures | ongoing | AAVSO | not researched here | Possible but low impact; TESS EB catalogues cover many neighbours `[INFERRED]` |
| **Planet Hunters TESS** | | | | Project finished `[READ]` | Not available |
| **Visual Survey Group / EB Patrol** | Track record of good finds | open-ended | VSG papers are usually led by its professionals; 72 papers, 69 refereed; they "welcome other experienced surveyors" `[READ: arXiv:2205.07832]` | 7 citizen scientists | Realistic later, once you have vetted finds to show. You may not contact them now (your rule 6) |
| **Candidate with a 2027 prediction** | One strong single or pair event plus Kepler constraint | 2 to 3 months | RNAAS or a short paper | TIC 172900988 b was confirmed from one sector `[READ]` | Highest value if it happens; see 1.10 |

On ExoFOP: your register says community uploads now need publication first (B9, B10) `[READ: your register]`; I could not open ExoFOP to confirm (section 9).

---

## 9. What I could not open or verify

ExoFOP (robots): current CTOI upload rule and any CTOIs or TOIs on G1 TICs. Search: ExoFOP TESS "News" page; then the CTOI table filtered by your TIC list. VizieR and CDS (robots): the Kepler EB catalogue table itself (period errors per star) and the TESS EB catalogue; use your local Villanova CSV for `period_err`. Villanova site (robots). The GI target lists beyond the first part of `GI_S081.csv`: grep `GI_S073` to `GI_S083` for G06010 and cross-match TICs. The TESS Ten Thousand machine-readable table (to count G1 members). Doyle 2011 and Welsh 2012 journal supplements (transit times). Davies Figure 7 numbers. arXiv:2610.22625 itself (rate-limited; I used a summary page). Not verified, from memory: journal references for Martin 2017 (MNRAS 465, 3235), Martin and Fabrycky 2021 (AJ 162, 84), Hippke et al. 2019 (AJ 158, 143) and the "3 × duration" sentence, Huang et al. 2020 (RNAAS 4, 204), Slawson et al. 2011 (AJ 142, 160), Borkovits et al. 2016 (MNRAS 455, 4136), Kostov et al. 2021 (AJ 162, 234), Kristiansen et al. 2022 (PASP 134, 074401), Prša et al. 2022 (ApJS 258, 16), Stassun et al. 2018 (AJ 156, 102), Doyle et al. 2011 (Science 333, 1602), Battley et al. 2021 (MNRAS 503, 4092), KOI-54 = KIC 8112039, and the PDC header keyword names. Not checked: whether QLP has reprocessed sectors 1 to 55 with a `sys_rm_flux` column (lightkurve says no as of 20 October 2026 `[READ]`; check one of your own S40 files), AAVSO VSX rules, and the Dunning et al. 2025 abstract.

**On your records (6.10).** F-009 says "about 8%" and "about 12 not transiting"; Welsh et al. say 8.9% and about 11.5 (your own Gemini review), so update the wording `[READ: your review file]`. F-018 is right on Martin's abstract `[READ]`, but most of the 17 to 30 hidden planets switch on over centuries (Kepler-1647-like: 13.2 of them, 7,189-year precession), so "possibly during TESS" should say "a small fraction during TESS" `[READ, INFERRED]`. The brief's §4.7 "flags, not deletions" contradicts `veto()` (B4). The Kepler-16 "UNCERTAIN" secondary-phase note in the overnight report can be closed (D4). I found nothing else wrong in the claims register.

---

## 10. The one thing I would do next

**Write and run one "data-path audit" script before any search.** For every G1 star-sector it would record product, cadence, flux column chosen, cadences kept, finite box means per duration and the PDCSAP/SAP noise ratio, then inject one standard transit (8 h, 3,000 ppm) and record whether it comes out. This single script would have caught B1, B2 and B5 immediately, turns your one-star sensitivity into a per-star map for all 549, and gives you the denominator you need for the upper-limit paper, which is the most likely credited outcome. It costs only CPU on data you already plan to download (about 6.3 GB), changes no science decision, and should come before the eclipse-phase control, the Skye veto and the Kepler re-find test, because all three depend on a data path you can trust. With TESS back over the Kepler field in July and August 2027, starting this in November or December 2026 leaves time for a prediction to be tested.

---

## Sources

- [Davies et al. 2026, arXiv:2604.09435](https://arxiv.org/pdf/2604.09435) · [mono-cbp repo](https://github.com/bdrdavies/mono-cbp) (GPL-3.0; commit 8d373b4)
- [Martin 2017, "Circumbinary planets II: when transits come and go", arXiv:1611.00526](https://arxiv.org/pdf/1611.00526)
- [Armstrong et al. 2014, arXiv:1404.5617](https://arxiv.org/pdf/1404.5617) · [RERO record with journal reference](https://doc.rero.ch/record/291128?ln=en)
- [Martin and Fabrycky 2021 (STANLEY), arXiv:2101.03186](https://arxiv.org/pdf/2101.03186) · STANLEY repo `github.com/TKleanthousT/stanley_cbp` (MIT; commit 2feaabf)
- [Kostov et al. 2020, multiple transits per conjunction, arXiv:2008.02756](https://ar5iv.arxiv.org/html/2008.02756)
- [Kostov et al. 2021, TIC 172900988, arXiv:2105.08614](https://arxiv.org/pdf/2105.08614)
- [Kostov et al. 2025, TESS Ten Thousand catalogue, arXiv:2506.05631](https://arxiv.org/pdf/2506.05631)
- [Oddo et al. 2026, arXiv:2610.22625 (summary page read)](https://astrobiology.com/2026/10/19/the-occurrence-of-circumbinary-planets-around-tess-m-dwarf-eclipsing-binaries/)
- [Martin, Mazeh and Fabrycky 2015, RERO record](https://doc.rero.ch/record/299170?ln=de)
- [Borkovits et al. 2016, arXiv:1510.08272](https://ar5iv.labs.arxiv.org/html/1510.08272) · [Borkovits et al. 2025, arXiv:2502.09480](https://www.arxiv.org/pdf/2502.09480) · [Borkovits et al. 2026, arXiv:2604.04004](https://arxiv.org/pdf/2604.04004)
- [Slawson et al. 2011, arXiv:1103.1659](https://arxiv.org/pdf/1103.1659)
- [Huang et al. 2020 (QLP), arXiv:2011.06459](https://arxiv.org/pdf/2011.06459)
- [Hippke et al. 2019 (wotan), arXiv:1906.00966](https://ar5iv.arxiv.org/html/1906.00966)
- [Battley et al. 2021, arXiv:2103.03259](https://arxiv.org/pdf/2103.03259)
- [Welsh et al. 2012, arXiv:1204.3955](https://arxiv.org/pdf/1204.3955) · [Doyle et al. 2011, arXiv:1109.3432](https://arxiv.org/pdf/1109.3432)
- [Kristiansen et al. 2022 (Visual Survey Group), arXiv:2205.07832](https://ar5iv.arxiv.org/html/2205.07832)
- [TESS DRN, sectors 14-19 reprocessing (NTRS 20205007589)](https://ntrs.nasa.gov/api/citations/20205007589/downloads/tess_reprocessing_sector_14_19_drn30_v2.pdf)
- [MAST TESS Archive Manual, 2.0 Data Product Overview](https://outerspace.stsci.edu/display/TESS/2.0+-+Data+Product+Overview)
- [Kepler EB catalogue ReadMe, VizieR J/AJ/151/68](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/AJ/151/68?format=html&tex=true)
- [HEASARC TESS sector table](https://heasarc.gsfc.nasa.gov/docs/tess/sector.html) · [MIT sector 119](https://tess.mit.edu/observations/sector-119/) · [MIT sector 120](https://tess.mit.edu/observations/sector-120/) · [HEASARC Cycle 10 pointings](https://heasarc.gsfc.nasa.gov/docs/tess/tess-cycle-10-pointings-are-available-now.html)
- [TESS GI G06010](https://heasarc.gsfc.nasa.gov/docs/tess/data/approved-programs/cycle6/G06010.txt) · [TESS GI G07004](https://heasarc.gsfc.nasa.gov/docs/tess/data/approved-programs/cycle7/G07004.txt)
- [AAS Research Note guidelines](https://journals.aas.org/research-note-preparation-guidelines) · [Planet Hunters TESS FAQ](https://zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/about/faq)
- lightkurve source, commit f762d52 (`src/lightkurve/utils.py`, `io/qlp.py`, `io/tess.py`) · tessgi/ticgen source (MIT), `ticgen/ticgen.py`

## Attached scripts (MIT, mine; run from any folder with your repo at `../second-sun`)
`test_cadence.py` (B1), `test_mask.py` and `test_mask2.py` (D3, B3), `sens.py` (4.1, 4.2), `yield.py` (4.3). Paths inside point to `/home/claude/...`; change them to your D: paths.
