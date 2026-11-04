# RS-010 Q5: what did the 784 "no safe windows" G3 reads cost? (night of 4 Nov 2026; own data only; nothing in Petrova changed)

Script `research/stage3/census_step1/q5_lost_reads.py`, full output `q5-lost-reads.txt` (same folder). Counts and the Horizon reach rule R0 unchanged (`pipeline/horizon_reach.py`). No star ID is printed.

## Plain verdict
**The loss is real but modest: about 16% of the star-sectors were never searched, and that costs about 8% of the reach at the Kepler-16-size cell.** Recovering them would have bought roughly 1.7 star-equivalents on top of about 20. The cause is a data-supply gap after sector 26, the same gap Census is built to close.

## Numbers (CONFIRMED: counted from `data/g3/audit`)
- 5,031 files in the audit; 784 of them (15.6%) have no safe windows: 283 with no neighbouring 2-minute star and 501 with only one weak neighbour (the borrowed-windows rule needs at least 2). This is the 784 in the result file, so the earlier "784 of 5,634 reads" and this "784 of 5,031 files" are two ways of counting the same 784 (the 5,634 includes second-pass SAP reads; the ratio 13.9% vs 15.6% comes from that).
- Star-sectors: 4,080 in the audit; 3,425 had at least one safe-window product; **655 (16.1%) had none** and were not searched. **16 of 611 stars were lost completely** (no usable star-sector at all).
- By cadence era: 30-minute files (sectors 1 to 26) 48 of 1,136 lost (4.2%); 10-minute files (sectors 27 to 55) 254 of 950 (26.7%); 3.33-minute files (sectors 56+) 351 of 1,981 (17.7%). The two later eras are exactly where no eclipsing-binary list exists, so our supply of 2-minute neighbour stars (the G1, G2 and G3 pools) is thin there.
- Neighbour count of the lost reads: 238 with none, 414 with one. 24 of 105 sectors have more than 30% lost. By camera 1/2/3/4: 217/247/147/44.
- The lost star-sectors are slightly noisier (median 6.5 h noise 1,003 ppm against 843 ppm) and about as bright (Tmag 12.95 vs 12.80).

## What it cost (Horizon, main scenario, floor 5.6; LIKELY: the lost star-sectors are scored as if their whole light curve had been searched, which is generous)
Sum of detection chance over stars, as searched, and if the 637 scorable lost star-sectors had been searched:
- R = 7 Earth radii: P=77 d 20.10 to 21.77 (+8.3%); P=139 d 18.05 to 19.40 (+7.5%).
- R = 11: P=77 d 73.0 to 82.5 (+13%); R = 15: P=77 d 115.8 to 133.8 (+15.5%). Largest gain over cells with sum above 1: +15.8%.
- Meaning: the 95% ceiling for zero found at the Kepler-16 cell would move from about 15% to about 14% for G3. Not decisive for G3.

## Why this matters for Census (the real point)
Census stars will mostly sit in sectors 27 to 109. That is the era with the highest loss (18% to 27%). Without a fix, a Census search would lose a fifth of its star-sectors before it begins, and the cause (borrowed windows from our own pool) gets worse the more the list leaves the old catalogues. A proper fix is a table of safe time windows for every sector, camera and CCD, built from SPOC 2-minute light curves. The target lists downloaded tonight say which stars sit on which camera and CCD, so picking 2 or 3 bright 2-minute targets per (sector, camera, CCD) is possible without guessing. Size and design of that: queue entry T137 below. It is a build, so it waits for his word; it changes the search, so it needs a new frozen version.

## Labels
- CONFIRMED: all counts above (our own audit tables).
- LIKELY: reach gains (assumes full coverage for the lost star-sectors; recovery tables from the G2 development split reused unchanged).
- UNCERTAIN: whether a different window rule (not just more neighbours) would be as safe: scattered light is per camera and CCD, so same-CCD neighbours are the right idea; a sector-wide fallback would be weaker.
- NOT TESTED: how many extra false alarms the recovered star-sectors would add (S2 is already over its mark).

## Independent re-check (same night, `census_step1/crosscheck_counts.py`, plain csv/json, no pandas, from the RUN output rather than the audit tables)
G3 run output: 4,080 star-sector groups; 5,634 product reads; 784 with status "no safe windows"; 655 groups with no ok product; 611 stars, 595 with at least one ok group. Every figure matches the audit-based counts above (784 reads, 655 lost star-sectors, 16 stars lost). The 5,634 reads against 5,031 audit files differ because some files are read as more than one product (a TESS-SPOC file gives PDCSAP and SAP). CONFIRMED by two routes. The target-list counts of Step 1 were re-counted the same way: 232,764 and 476,784 stars, 364,656 new, 258,858 new at Tmag 13.5 or brighter: all match.
