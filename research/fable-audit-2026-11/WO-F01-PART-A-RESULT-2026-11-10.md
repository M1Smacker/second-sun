# WO-F01 Part A result (10 Nov 2026, Sonnet 5.5 Extra): how much of a real dip the frozen eclipse mask deletes

**Plain verdict: the frozen 0.8.1 mask deletes a large share of real dips in G2 and G3, growing steeply with the binary period, and the earlier recovery tests (injected after the mask) could not see it. Bumps on the upside-down arm are not lost (the proof test passes). STOP SIGN REACHED (see the end): nothing public is written, Ahmed decides the wording.**

Labels: CONFIRMED = measured by a script that could have contradicted it, on our own data. Nothing in `pipeline/` was edited. Rows with star ids stay private in `data\fable_audit_mask\`; the evidence files carry counts only (plus the two published, public systems).

## What was measured
Script `scripts/wo_f01a_mask_loss.py` (a copy of `stage2_search.prepare` with an inject hook between the windows and the mask). For every sampled file (one product of one star-sector): a trapezoid dip of K x the 8 h noise (noise measured after the baseline mask) is put in light the baseline mask KEEPS, then either BEFORE the mask (what a real planet does) or AFTER it (what every earlier recovery test did). Found = an event at SNR 7 or more (v5 box grid) within the usual window of the injection. m = found before / found after.
- Sample: 100 files per period bin (5-10, 10-14, 14-20, 20-27.4, over 27.4 d) per product family (SPOC family, QLP) for G2 (1,000 files, 971 usable) and G3 (774 files, 689 usable; fewer where the cell has fewer files: G3 over 27.4 d has 8 SPOC-family and 30 QLP usable files). Skips are counted: no safe windows (G2 20, G3 77, files the real run also never searched), no clean slot, noise not finite.
- Reduced against the work order to keep it cheap: K = 8, 12, 18, 25 (not 6 values), durations 4, 8, 14, 20 h, one injection time per file, bumps only at 8 h with K 12 and 25. Run time 5 min (G2) and 2.5 min (G3), 6 workers.
- Proof tests (CONFIRMED): (1) zero-injection identity: the copy of `prepare` gives the same status and `n_searched` as the stored group JSON for 53 of 53 G2 files and 23 of 23 G3 files (20 star-sectors each). (2) Bumps: before/after agree in every bin, both sets (K 25: 1.00 everywhere; K 12: 0.93 to 0.97 on both sides). A wrong injection would have lost bumps too. The deliberate mutation test was run later the same day (3 mutants, each fails exactly its check): see `BOOK-SENTENCES-AFFECTED-2026-11-10.md` and `evidence/wo_f01a_mutation_test.txt`.

## Result 1: dips lost, G2 (SPOC family and QLP behave alike; before/after, 8 h dip, both families pooled)
| K (x 8 h noise) | 5-10 d | 10-14 d | 14-20 d | 20-27.4 d | over 27.4 d |
|---|---|---|---|---|---|
| 12, 8 h | 0.73 / 0.96 | 0.57 / 0.96 | 0.33 / 0.96 | 0.13 / 0.97 | 0.11 / 0.95 |
| 25, 8 h | 0.66 / 1.00 | 0.26 / 1.00 | 0.07 / 1.00 | 0.01 / 1.00 | 0.02 / 0.99 |
Share of the dip's cadences the mask removes: 0.22 to 0.33 at 5-10 d, 0.52 at 10-14, 0.70 at 14-20, 0.84 to 0.86 at 20-27, 0.85 to 0.88 beyond. Standard error of one cell about 0.05. Full tables: `evidence/wo_f01a_mask_loss_g2.txt` and `_g3.txt` (all K and durations, per family).
G3 shows the same shape (K 25, 8 h: 0.45 / 0.16 / 0.09 / 0.04 / 0.00 against 1.00 after), and it is lost EARLIER than G2 in the 5-10 d bin (0.45 against 0.66). Even at 5 to 10 d a quarter to a half of strong dips is gone. Cause of the 5-10 d loss: NOT TESTED (Fable's mechanism, one visit per phase bin, only explains the slow bins).

## Result 2: one number per hunt (CONFIRMED as arithmetic, UNCERTAIN as a weighting)
m = sum(w x before) / sum(w x after), w = files of the cell in the hunt's manifest x usable share. It weights by file count, NOT by each star's planet-detection value (Horizon's per-star E was not read), so it is the share of injected dips lost over the star-sectors actually read.
| K | G2 m (dips lost) | G3 m (dips lost) |
|---|---|---|
| 12, all durations | 0.60 (40%) | 0.69 (31%) |
| 18, all durations | 0.48 (52%) | 0.54 (46%) |
| 25, all durations | 0.40 (60%) | 0.40 (60%) |
| 12, 8 h only | 0.53 (47%) | 0.63 (37%) |
| 25, 8 h only | 0.37 (63%) | 0.29 (71%) |
Rough uncertainty about +-0.04 to 0.05 (cells independent, n = 100 each); not computed exactly. K = 8 is not used for conclusions (found after only 0.2 to 0.3).
What m does NOT include: the veto, flags, tiers and the SAP-twin pass (only the detection step is measured), the QLP window rules beyond what `prepare` already does, planets whose dips fall inside masked eclipses anyway, and any weighting by value. So it is the mask's loss alone, not the chain's total recovery.

## Result 3: the two known TESS circumbinary planets (K-02 to K-04; sources opened 10 Nov 2026, text extracted from the arXiv PDFs)
**TOI-1338 b** (Kostov et al. 2020, arXiv 2004.07783, Table 6, predicted transit times; BTJD = BJD - 2455000 - 2000): of 10 predicted transits that fall in our 2-minute light, the frozen mask removed 0% of the window in 7, 31% in one (S68), 100% in one (S98, window sits inside an eclipse), and one has no data (S62). Five events found by the frozen mask (S65 3085.40, S89 3744.48, S93 3836.96, S96 3932.76, S98 4025.64; SNR 8.4 to 15.2) sit 0.6 to 1.3 d after the predicted times, and the spacing of these five events (659.1, 92.5, 95.8, 92.9 d) matches the predicted spacing (658.8, 92.4, 95.4, 93.2 d) within 0.5 d. LIKELY these are planet b transits (offsets of 0.6 to 1.3 d are larger than the table's formal error for these five, 0.07 to 0.22 d, so the 2020 model has drifted: UNCERTAIN why; I did not check the later photodynamical fits, e.g. arXiv 2404.18415). The Fable repeat-rule extras at S27 to S32 and S4 do NOT match any prediction (S27 2047.86 is 1.8 d from 2049.69; S31 and S32 events are not near any prediction): UNCERTAIN what they are, NOT planet b by this test. The predicted S27 transit (2049.69) has best SNR 6.7 near 2049.95 with the mask, just under the threshold, mask removal 0%: it is a detection-threshold miss, not a mask loss.
**TIC 172900988 b** (Kostov et al. 2021, arXiv 2105.08614, section 2: two transits in Sector 21 at BTJD 1883.37, about 0.4 d, and 1888.30, about 0.27 d, depth about 3000 ppm, one before and one after the downlink gap). Two different reasons, CONFIRMED by script:
- TESS-SPOC 30-min product (the one in our known-star folder): per-cadence scatter 6,000 to 8,500 ppm, so the transits are far below SNR 7 with or without any mask (best SNR 2.8 and 2.0 masked). Noise, not the mask.
- QLP 30-min product (scatter 265 to 460 ppm per cadence, naive SNR 34 and 20): the dips are clear in the data, but the frozen mask (P 19.658 d) removes **100% of the cadences of BOTH transit windows**; without the mask the first transit is at SNR 7.0 and the second is hidden by the neighbouring eclipse. So on the product where the planet is visible, the mask deletes both published transits (one star, n = 1; windows borrowed from SPOC were not applied, so this is the best case for QLP; the star is not in G2 or G3).
Files: `evidence/k02_known_transits_mask_share.txt`, `k03_s21_diagnose.txt`, `k03_s21_diagnose_qlp.txt`, `k04_s21_qlp_search.txt`; scripts beside them. Downloads: two papers (7.5 MB and 9.6 MB, arXiv) in `data\known_papers_2026-11-10`, logged in `research/downloads.csv`.

## What this changes (plan changes, not done without his go)
1. The mask redesign (Part B, Amendment A steps 1 to 4) is confirmed as the top item; the target to beat is in Result 1 (m at least 0.9 in every bin at K 12 and K 25) plus the real/upside-down ratio check.
2. Every recovery table of Vesper 0.8.1 (K50/K90, "smallest planet", Horizon's E, Census odds) was measured after the mask. Anything built on them overstates detection chance for binaries slower than about 10 d. Which published sentences quote them: NOT CHECKED (a grep of the book and notes is a cheap next step).
3. The G1 to G3 nulls stay as filed (verdicts stand). What they exclude is much weaker for slow binaries, and the book wording about "what a null excludes" needs his decision (stop sign below).

## STOP SIGN (WO-F01): m under 0.5 for a hunt as a whole
Reached for strong dips (K 18 or more: G2 0.48 and 0.40, G3 0.54 and 0.40; K 12 is 0.60 and 0.69). The work order says stop and ask Ahmed: the nulls then need a public correction note and the wording is his. I wrote no public text, changed no book page and re-scored nothing. Not pushed.
