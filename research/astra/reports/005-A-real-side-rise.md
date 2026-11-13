# 005 A. Real-side rise, node 1.1 (GPT-6.1 Sol)

**Verdict: 59 real events enter tier 1 and six leave, for the reported net rise of 53. Cause UNCERTAIN.** The repeater-only replay reproduces the isolated 004 counts. All 15 added upside-down events are gains. The six losses are consistent with the downstream orbit-lock test re-evaluating newly eligible partners. This report compares cohort membership using campaign, star, sector, product, sign and saved event properties privately. It reports only aggregates.

| Cohort | Events | Campaign-star groups | Maximum per group | Within 1 to 2 nearest eclipse widths | At least 2 widths away | Missing widths |
|---|---:|---:|---:|---:|---:|---:|
| Added real | 59 | 33 | 4 | 2 | 54 | 3 |
| Added upside-down | 15 | 12 | 2 | 0 | 15 | 0 |
| Original real | 123 | 64 | 16 | 11 | 102 | 10 |
| Original upside-down | 70 | 44 | 11 | 2 | 68 | 0 |

**CONFIRMED.** Using the Petrova catalogue epoch and period, all 56 classifiable added real events are at least two primary widths away. Relative to secondary, two are between one and two widths and 54 at least two. The original real cohort has five at one to two primary widths and eight at one to two secondary widths. No cohort has an event centre inside one width. Phase uses the catalogue windows convention, including the phase-0.5 and primary-width fallback for missing secondary information (pipeline/petrova_mask.py:28-93). These are centre distances, not event overlap or distances to a refitted eclipse. Relative widths depend on catalogue definitions.

| Cohort | QLP | SPOC | TESS-SPOC | SPOC SAP | TESS-SPOC SAP | Era <56 / 56 to 93 / 94+ |
|---|---:|---:|---:|---:|---:|---|
| Added real | 31 | 6 | 14 | 4 | 4 | 24 / 23 / 12 |
| Added upside-down | 10 | 3 | 0 | 0 | 2 | 7 / 5 / 3 |
| Original real | 44 | 35 | 37 | 1 | 6 | 71 / 48 / 4 |
| Original upside-down | 31 | 21 | 16 | 2 | 0 | 34 / 32 / 4 |

| Cohort | Duration / eclipse width, <0.5 / 0.5 to 1 / 1 to 2 / 2+ / missing | Amplitude / eclipse depth, same bins |
|---|---|---|
| Added real | 9 / 24 / 16 / 7 / 3 | 16 / 16 / 5 / 4 / 18 |
| Added upside-down | 1 / 5 / 5 / 4 / 0 | 10 / 3 / 0 / 0 / 2 |
| Original real | 17 / 66 / 25 / 5 / 10 | 35 / 20 / 16 / 2 / 50 |
| Original upside-down | 20 / 14 / 24 / 12 / 0 | 53 / 3 / 2 / 1 / 11 |

Width and amplitude refer to the nearest eclipse in units of width. G2 uses catalogue fit depths, with the alternate fit when the preferred width is missing. G3 uses the matching TTC catalogue row and the archived byte descriptions (primary bytes 65 to 67, secondary 89 to 94, parts per thousand). Missing catalogue depths and fallback secondary depths stay unavailable. Depth ratios describe heterogeneous fitted and detected signals.

**CONFIRMED.** Within the same sector, product and arm, four of 59 added real events have a saved candidate within one hour of half the catalogue period, four have one near a full period, and zero near twice the period. Two have two distinct other half-period-grid positions relative to the event. This is a partner screen, not a new qualifying triple rule. Added upside-down events have zero such partners. Original real has one half-period, one full-period and two twice-period partners. Original upside-down has one half-period partner. All comparisons reuse saved events and do not infer significance from these small counts.

**UNCERTAIN.** The rise spans products and stars. Direct catalogue eclipse proximity and simple period aliases explain few events. QLP and late-era counts are prominent among additions, but these are event counts without exposure standardization or an instrument-only control. Instrument and off-eclipse binary structure remain plausible. Evidence does not justify narrowing the adopted lock. No possible-planet inference was made from aggregate features.

Evidence: 005_replay.py and 005_phase.py, private counts phase-summary-g2.json and phase-summary-g3.json. No new FITS reads in this part. No new pipeline bug established. STOP SIGNS: none in A. QUEUE PROPOSALS: node 1.1, retain 59 gains and six losses in the tracked real-side cost. IDEAS: none supported for a narrower lock. Questions for Ahmed: none. Usage shared with baseline replay and logged in combined report. Branch astra/005-three-diagnoses.
