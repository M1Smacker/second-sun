# Area P findings (Petrova, frozen Vesper 0.8.1). Read at commit c9b9aca. Counts only.

## F-01 URGENT. The eclipse mask cuts planet dips out of slow binaries before the search. CONFIRMED (mechanism, synthetic, real counts). Fable used: yes.

**What.** `pipeline/detect_v2.py` `eclipse_mask_auto` (lines 129 to 161) folds ONE sector at the binary period into 600 phase bins and masks every bin more than 4 robust sigmas low (plus 1.5 widths each side). It never asks whether the low bin repeats. When the period is longer than about half a sector, a phase bin holds one visit, so any strong dip is "an eclipse" and is deleted. `stage2_search.mask_runs` calls it for every file (line 163); nothing downstream can see the deleted light.

**Why nobody saw it.** Every recovery test injects AFTER the mask: `stage2_search.do_group` line 212, `chain_recovery.py` line 38 to 42 (wraps `S2.prepare` and adds the dip to the prepared, already masked flux), `faint_recovery.py`, `sap_recovery.py`, `paired_recovery.py`, `audit_all.audit` line 153. So completeness, the c = 0.9 trim and Horizon E are all blind to this loss.

**Evidence 1, synthetic** (`scripts/p01_mask_eats_transits.py`, output `evidence/p01_synthetic.txt`, 30 trials per cell, 8 h dip injected BEFORE the mask):

| Binary period | dip SNR 9 found | SNR 12 found | SNR 20 found | (perfect mask) |
|---|---|---|---|---|
| 5.5 to 14 d | 0.73 to 0.83 | 0.97 to 1.00 | 0.97 to 1.00 | same |
| 20 d | 0.70 | 0.90 | 0.37 | 0.83 / 1.00 / 1.00 |
| 30 d | 0.53 | 0.57 | 0.00 | 0.83 / 1.00 / 1.00 |
| 50 d | 0.60 | 0.17 | 0.00 | 0.90 / 1.00 / 1.00 |

The stronger the dip, the more surely it is cut. Bumps of the same size on the upside-down arm are never cut (found 1.00 at every period).

**Evidence 2, real stored events** (`scripts/p01b_real_vs_flip_by_period.py`, `evidence/p01b_real_vs_flip.txt`). G2 sealed, all events, real / upside-down:
- period under 10 d: 1,780 / 1,684 (ratio 0.95, equal at every SNR);
- 20 to 27 d: 115 / 322; over 27 d: 190 / 618 (ratio about 3);
- over 20 d and SNR over 12: 40 real against 260 upside-down.
G3 shows the same direction from 10 d up (10 to 14 d: 230 / 378; SNR over 20: 11 / 44). The G3 result note already recorded "upside-down over real 1.08 at bar 4.5 rising to 1.58 at bar 10, cause not studied (UNCERTAIN)". This is the cause: LIKELY for the whole ratio, CONFIRMED as a contributor.

**Evidence 3, real light** (`scripts/p01c_real_light_premask_injection.py`, `evidence/p01c_real_light.txt`; G2 SPOC 2-minute files, 25 random files per period bin, seed 1, 8 h box dip, same time injected before and after the mask). Real light is worse than the synthetic case because gaps leave fewer visits per phase bin:

| Binary period | K 12 found: before mask / after mask | K 25 found: before / after | dip cadences cut (K 12 / K 25) |
|---|---|---|---|
| 5 to 10 d | 0.84 / 0.96 | 0.80 / 1.00 | 0.14 / 0.21 |
| 10 to 14 d | 0.68 / 1.00 | 0.28 / 1.00 | 0.39 / 0.80 |
| 14 to 20 d | 0.52 / 0.92 | 0.12 / 1.00 | 0.47 / 0.87 |
| 20 to 27 d | 0.08 / 1.00 | 0.00 / 1.00 | 0.94 / 1.00 |
| over 27 d | 0.04 / 0.96 | 0.00 / 1.00 | 0.94 / 1.00 |

(K = depth in units of the 8 h noise. "After mask" is what every recovery test of ours measures. Small samples: each share is good to about plus or minus 0.15.) So the loss starts at 5 d, is about a third to two thirds at 10 to 20 d, and is nearly total from 20 d. Deep dips (giants on bright stars) are lost most.

**What it does to our results.**
- Star-sectors with binary period over 14 d: G2 sealed 2,609 of 6,877 (38%); G3 670 of 4,080 (16%). Over 20 d: G2 sealed 1,375 (20%); G3 135 (3%).
- In those star-sectors a giant planet's transit (SNR far above 20) was deleted with probability about 0.25 at 14 d, 0.6 to 1.0 from 20 d. The G1 to G3 nulls say almost nothing about deep transits in binaries slower than about 20 d, and less than claimed from 14 d.
- 8 of the 12 known transiting circumbinary hosts have binary periods over 18 d (Kepler-16 41 d, -34 28 d, -35 21 d, -38 19 d, -64 20 d, -453 27 d, -1661 28 d, TIC 172900988 19.7 d). We are weakest exactly where the known planets live.
- S1 compares the real arm with a noise expectation built from the upside-down arm. The mask thins the real arm only, so S1 was biased toward "no excess".
- S2 (too many upside-down first-tier dips): the mask removes real-arm dips, so upside-down events are less often "dominated" (`stage3_core.enrich_group`, line 291 to 294) and more reach tier 1. Stored first-tier upside-down rate in G2 sealed: 44 per 1,000 star-sectors over 20 d against 12 to 23 below. LIKELY a main cause of the S2 failure in G2; in G3 the excess is also present under 10 d (4 real against 19 upside-down first-tier), so a second cause exists there (NOT TESTED; QLP bumps are the suspect).
- Horizon E and the Census odds overstate our reach for slow binaries and understate what the three empty hunts leave open. Direction: the posterior from "three empty hunts" is too pessimistic about the planet rate, and future E per star is too optimistic until the mask is fixed.

**Not a reason to re-open sealed results.** The preregistered verdicts stand as filed. This is a completeness error to state, and a Petrova 1.0 change.

**Petrova 1.0 candidate.** Mask eclipses from the catalogue ephemeris and width where we have them (`eb_widths()` already loads them for G2 and G3), or build the mask from all sectors folded together and require a low bin to be low in at least 2 cycles; mirror the mask logic on the upside-down arm (mask bumps by the same rule) so the two arms stay exchangeable; inject before the mask in every recovery test. Work order WO-F01.

## F-02. FIX 84 measured: no flagged cadence enters from Sectors 56 to 93; a NEW unmasked flag (bit 29) rides on 11.9% of kept cadences from Sector 94. CONFIRMED (counts); meaning of bit 29 UNCERTAIN. Fable used: yes (small).

`scripts/p02_fix84_qlp_bits.py`, `evidence/p02_fix84.txt`: 240 random G3 QLP files (seed 84).
- Sectors under 56: 118 files, 0 kept cadences carry a flag.
- Sectors 56 to 93: 98 files, 0 of 982,103 kept cadences carry a flag. lightkurve 2.6.0 (`io/qlp.py` lines 65 to 73) adds bit 30 for "hard" from Sector 56. FIX 84 as written (bit 31 leaking) does not happen with this lightkurve version. The G3 null is not changed by it.
- Sectors 94 and later (TGLC-based QLP): 24 files, 27,672 of 232,998 kept cadences (11.9%) have bit 29 set, in 17 of 24 files. About 10% of G3 QLP files are from this era.
Work order WO-F02: read the QLP data product description for the Sector 94+ flags, then compare upside-down and real event rates inside and outside bit-29 cadences.

## F-03. The flip-match flag is one-sided in code but harmless in practice. CONFIRMED. Fable used: yes (small).
`stage2_search.do_group` lines 190 to 191: real events get the flag from upside-down events; upside-down events are checked against an empty list. `scripts/p03_flipmatch_asymmetry.py`: only 1 of 35 (G3) and 1 of 146 (G2 sealed) stored first-tier upside-down events has a real event within 0.3 d; 1 real event in total sits in tier 2 for this flag alone. No effect on S2. Fix it in Petrova 1.0 for symmetry only (part of WO-F01).

## F-04. FIX 70 lost reads: the neighbour-window rule is a proxy we no longer need in most sectors. LIKELY (reasoning, not run). Fable used: yes (judgement only).
`stage2_search.prepare` lines 150 to 159 drops a QLP read unless the star has its own SPOC file or at least 2 SPOC neighbours on the same sector, camera and CCD. The rule was made on one star (TOI-1338 S98) to remove scattered light. Three cheaper sources of the same information exist: (a) QLP's own quality flags, which lightkurve now applies from Sector 56 (F-02 shows they remove 9% to 19% of cadences already); (b) the QLP background column `sap_bkg`, which measures scattered light on the star itself; (c) windows from the same sector and camera on ANY CCD, since scattered light and momentum dumps are orbit and camera level. Work order WO-F04 measures how many of the 13.9% to 16.1% lost reads each option rescues and whether the upside-down rate in rescued reads matches the rest.

## F-05. Tests do not test the science path. LIKELY (from H2 and code reading; not run). Fable used: no (routine).
Beyond FIX 83 ("pass" after "skip"): no test injects before the mask (F-01); the zero-diff proofs prove sameness, not rightness; `chain_recovery_test.py` mutations cover "injection ignored" and "sign flipped" only. Work order WO-F05: add the three missing tests (inject before mask at long period; arm exchangeability on noise; a known planet end to end).

## F-06. Known planets on real light: NOT DONE (budget). Work order WO-F06 for Sonnet.
`data\known` holds the light. The test that matters after F-01: run `mask_runs` on TIC 172900988 (19.7 d binary) and TOI-1338 (14.6 d) real sectors and count how many in-transit cadences of the known planet transits survive the mask. Then the Kepler-host injections, injected BEFORE the mask.

## Question everything (half page)
- Transits remain the right main method for us: they need only public photometry and one event is informative. But our reach is single transits of giants; F-01 means we have not yet truly searched slow binaries, which is the best-supported place to look. Fixing the mask is worth more than any new star list.
- Eclipse timing variations: need many eclipses at good timing precision; TESS gives few cycles for slow binaries. Useful as a second key on a lead, not as a search (LIKELY).
- Apsidal motion: confounded by tides and third stars; no.
- Single-transit stacking across sectors: circumbinary transits are not periodic, so plain stacking fails; a "transit-count excess per star across sectors" statistic (several sub-threshold dips in one star) is the honest version and is a Petrova 1.0 candidate.
- A learned vetter (T150, T151): only after the two arms are exchangeable (F-01), otherwise it learns the mask artefact.
