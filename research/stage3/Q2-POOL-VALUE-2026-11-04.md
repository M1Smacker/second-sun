# RS-010 Q2: which pool is worth its gigabytes? (night of 4 Nov 2026; research stint RS-011; report only, nothing chosen, nothing downloaded)

Script `research/stage3/census_step1/q2_pool_value.py`, output `q2-pool-value.txt` and `q2-pool-value.csv` (same folder). It re-uses the Horizon reach rule R0 unchanged (`pipeline/horizon_reach.py`) on real G3 and G2 sealed star-sectors and changes only what a pool really changes: brightness (through the noise-versus-magnitude slope fitted on G3 itself: log10 noise = 0.26 + 0.211 x Tmag, photon-noise expectation 0.2), binary period, and the number of sectors per star. Disk cost is measured on our own disk: 0.54 MB per star-sector for G3-type files (QLP, 10 to 30 minute) and 2.12 MB for G2-sealed-type files (mostly 2-minute SPOC, several products). "Region" means the mean Horizon sum over the 15 cells with planets above 6 Earth radii, periods under 300 days, and at least half the stars allowed (the same cells as rule B in Q1).

## Plain verdict
**Brightness and coverage decide the value; star count does not.** Three simple rules fall out: (1) drop the faint stars, (2) a short-period binary scores well on reach but has no planets to find, so reach alone is the wrong ruler, (3) among bright stars, the more sectors a star has the better, and disk cost per unit of value stays about the same. The Horizon numbers are upper bounds that miss the transit geometry (Q1, T138), but that factor multiplies every pool alike, so the ranking should hold (LIKELY, not tested).

## Table (region star-equivalents; Horizon unchanged; CONFIRMED as arithmetic, inputs labelled)
| pool | per 1,000 stars | GB per 1,000 stars | per GB |
|---|---|---|---|
| G3 as searched (faint TTC, Tmag up to 13.5, QLP) | 84 | 3.0 | 27.9 |
| G2 sealed as searched (bright, 2-minute, about 11.6 sectors per star) | 196 | 24.1 | 8.1 |
| A. TTC fainter, Tmag 13.5 to 15.5 (G3 stars made 1.36 magnitudes fainter), 785 stars | 42 | 3.0 | 14.0 |
| B. TTC 5 to 7 day binaries (binary period set to 6 d, G3 light), 495 stars | 128 | 3.0 | 42.5 |
| C. TTC 2 to 5 day binaries (3.5 d), 1,205 stars | 164 | 3.0 | 54.4 |
| D. TTC under 2 day binaries (1.2 d), 634 stars | 195 | 3.0 | 64.7 |
| E3. bright 2-minute stars of the G2 type with 3 sectors each (post-sector-26 pool, ASSUMED) | 89 | 6.1 | 14.5 |
| E6. same with 6 sectors each | 133 | 10.1 | 13.1 |

## What it says
- **A (fainter TTC) is the worst buy:** half of G3's value per star and per GB. G3 already showed it (a fifth of G2's per star in the Kepler-16 cell). Do not spend the download.
- **B, C, D look best on reach, and that is a trap.** A shorter binary lets a planet sit stably closer in, so more cells open. But Kepler found no transiting circumbinary planet around a binary shorter than 7 days (Hamers, Perets and Portegies Zwart 2016, abstract CONFIRMED in RS-010; Armstrong 2014 calls the shortfall around shorter binaries real, 96 to 98% probability for coplanar planets, full text read). So the value of B, C and D is reach times a prior that is about zero. Value is reach times prior, and Horizon only has the first factor.
- **The post-sector-26 two-minute pool (E) keeps its worth if it has many sectors:** 3 sectors give 89 per 1,000 stars, 6 sectors 133, and the G2 sealed set at about 11.6 sectors gives 196. Per GB it is flat (13 to 15), so choosing stars with more sectors is free value. The target lists say 39,646 of the stars at magnitude 10 or brighter have 4 or more sectors in S27 to 109 (Step 1 counts).
- **QLP/FFI light for stars brighter than 13.5 is as good per star as a 3-sector 2-minute star and twice as good per GB** (G3-type 84 per 1,000 at 3 GB per 1,000, against E3 89 at 6.1 GB). That is a point for using FFI-derived light curves in Census for the bulk and 2-minute files where they exist, once the window gap is fixed (T137, Q5).

## Limits (read before using)
- LIKELY: the ranking. UNCERTAIN: the exact ratios, because the pools are built from existing star-sectors, not from the real pool stars (their radii, periods and noise are not known); the G3 radius median (1.64 solar radii) is reused.
- ASSUMED, not measured: E needs a real list (the 1,000 G2-type stars of Step 1 is a guess) and 3 or 6 sectors per star is a choice.
- NOT TESTED: the occurrence prior as a number; MB per star-sector for the S27+ files (the 2.12 MB figure comes from G2 sealed, which is S1 to 26 plus extras); how many extra false alarms short-binary pools would add.
- Pools B, C, D and A are scaled from 612 stars in the table; multiply per-1,000 values by the pool size /1,000 for totals (A 785 stars: 33 region units; B 495: 63; C 1,205: 197; D 634: 123).

## Plan change
Census value ranking should be reach x prior, with the prior from the literature (zero below 7 days, Hamers 2016; rate from Armstrong 2014 depending on period). Add to the Census plan stage 3: score by (Horizon reach with g) x (prior by binary period), not reach alone. Filed in the Census plan (see its section 4, step 3).
