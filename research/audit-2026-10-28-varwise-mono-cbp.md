# Audit notes: VarWISE, VARnet and mono-cbp (started 28 Oct 2026)

Working notes for the three-pass audit Ahmed asked for. Labels: VERIFIED (read in the source or recomputed here), LIKELY (read through a summary or reasoned), UNCERTAIN, NOT TESTED. The audit's final report (pass 3) is not written yet.

## Pass 1: mono-cbp (Davies et al. 2026)
- VERIFIED: GPL-3.0 licence (LICENSE file), pip-installable, command-line driven. Paper arXiv:2604.09435, code github.com/bdrdavies/mono-cbp (version 0.1.9 at the time of reading).
- VERIFIED: sample cuts 4,584 eclipsing binaries, minus 588 ambiguous, detached with morph under 0.5 gives 1,790, period over 7 d gives 591, minus 6 circumstellar hosts and visual inspection gives 512. 3,808 TESS-SPOC full-frame light curves (30-minute SAP flux). One candidate (TIC 319011894), not confirmed.
- VERIFIED (recomputed 28 Oct with a 6-line check): 30 of our 549 stars are in their 591-star table (`TEBC_morph_05_P_7.csv` from their repository). Our median Tmag is 12.45; 70 of our stars have binary periods under 7 d. Only Kepler-1647 is a known circumbinary host in both lists.
- LIKELY: the repository's model comparison uses a least-squares fit (lmfit) where the paper describes MCMC (read through a summary of the source).
- LIKELY: it needs scipy below 1.13 and our environment has 1.13.1, so it would need a separate environment (not installed).
- UNCERTAIN: real versus upside-down event ratio about 2.3 in their numbers (my arithmetic) against fewer real than upside-down in ours.

## Pass 2: VarWISE and VARnet
- VERIFIED: the audit prompt had the two paper numbers swapped. arXiv:2409.15499 is VARnet (Paz 2024, AJ, DOI 10.3847/1538-3881/ad7fe6). arXiv:2605.19059 is the VarWISE catalogue (Paz, Kirkpatrick, Uttamchandani, Raen, Cutri 2026; the abstract page says ApJS 284, 41, which one fetch did not show, so LIKELY). IRSA DOIs 10.26131/IRSA656, 657, 658.
- VERIFIED: VarWISE is a catalogue of NEOWISE single-exposure infrared photometry (3.4 and 4.6 micrometres): Pure 457,080 objects (49.81% new), Extended 1,918,082 (82.02% new). Variable detection by VARnet, classification by XGBoost (macro F1 0.95 on 113,840 validation objects, drawn from the same literature sources as the training set, which the paper cautions does not guarantee out-of-distribution performance).
- VERIFIED: cadence is one epoch about every six months, each of a few days with 12 or more observations, about 0.115 d apart; baseline late 2013 to mid 2024. No stated minimum detectable timescale.
- VERIFIED: classes are cep, rr, lpv, cv, ea, ew, yso, agn, sn plus "unclear". No planet or transit class. Eclipsing binaries are ea (Algol-type) and ew (W UMa-type). Sampled contamination by eye: ea 262 objects 100% eclipsing, ew 110 objects 97%.
- VERIFIED: period recovery for ea 92% direct (241 of 262); alias problems near 6 months and 1 year. Completeness is not quantified by the paper.
- VERIFIED: VARnet (§II, §IV): 4 classes null, transient, pulsator, transit; "transit" is mostly eclipsing binaries; trained on about 1.06 million synthetic light curves (trapezoid transits, periods 0.1 to 25 d); validated on 231 real objects (48 EBs, 49 pulsators, 34 transients, 100 nulls); macro precision 0.918, recall 0.910, F1 0.914; no false-positive rate; about 52 microseconds per source on a 22 GB GPU; clustering is the bottleneck (91 hours on 308 cores for the catalogue).
- VERIFIED: the paper licences are CC BY-NC-ND 4.0 (VARnet) and CC BY 4.0 (VarWISE). The IRSA overview states no licence for the catalogue itself; the code is not released as far as the papers and one search show (UNCERTAIN that none exists).
- NOT READ: the last 58,707 characters of the VarWISE HTML paper; IRSA column description pages; the PDF in the IRSA docs folder.
- Reasoned, LIKELY: speed is not our bottleneck. The v4 re-search of all 549 stars took about 40 minutes of machine time (usage ledger, 28 Oct). A learning-based search for our job would have only six known hosts (mono-cbp tested 14) to learn from, so it would train on injected fakes, which carries the lopsided-noise risk we already measured.

## Open for pass 3
Decision matrix A (improve our pipeline) / B (benchmark and adapt mono-cbp) / C (VarWISE-inspired ML), small benchmark plan, architecture, learning topics, roadmap.
