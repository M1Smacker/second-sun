# 005 B. Short-period blind spot, node 1.5 (GPT-6.1 Sol)

**Verdict: short-period reference misses are below the detection bar. The measured fitted depths show little median change through detrending.** Predeclared measurement, 13 Nov 2026. Use all 400 fixed draws in each of bins 0 and 3, compared by draw order (same stratified design, no claim of matching stellar covariates). Replay the dip in the exact stored input products with fixed original windows, mask, detrend and detection. Both adopted baseline changes are downstream of detection. Check exact saved injected event dictionaries, including SAP and its PDC check. Stop on identity mismatch.

For each available best-product primary or SAP path, record signed fitted transit template depth before and after detrending on the retained cadences, relative to the injected depth. Use least squares with an intercept within plus/minus one transit duration, a diagnostic of apparent signal including underlying flux, not an isolated attenuation measurement. Record robust scatter (1.4826 MAD) in the same local band, maximum finite searched box SNR inside the original half-duration matching radius, and count of SNR >= 7 candidates there before merging. Record whether a selected peak remains inside the match radius, and nearest selected peak displacement in units of duration. Primary/SAP measured separately, missing measurements explicit. A lower apparent-depth ratio supports attenuation or local structure, comparable ratios with worse scatter/SNR support higher noise, and above-bar candidates without matched retained events identify merging loss. Eclipse-phase association uses nearest catalogue eclipse distance in units of width where available, and compares local scatter near/far as a residual proxy. Summarize all and reference-only, using original window/mask-qualified trials. No candidate setting will be chosen from this run.

STOP SIGN, resolved before retry: first instrumentation attempt stopped on a SAP parity mismatch. Counts-only comparison found three identical files and one differing SAP file. Its saved product labels were SAP twins, but the diagnostic reconstructed unsuffixed paths from metadata. The loader dispatches on ::sap (pipeline/sap_twin.py:65), which metadata strips. Restore that suffix for SAP groups, preserve failed artifacts, and retry exact parity before using any measurement. No measurement definition or draw changed.

## Results

CONFIRMED runtime parity after the SAP dispatch correction. All 800 dip trials completed, 400 per bin, with exact saved event dictionaries in 800 primary and 413 SAP group files. The instrumented replay used the fixed T156 trials and did not search hold-out stars. The combined baseline affects tiering downstream of these measurements.

| Reference-band measurement | 5 to 10 days | 20 to 27.4 days |
|---|---:|---:|
| Fixed reference draws | 48 | 47 |
| Reached detection after support checks | 31 | 33 |
| Below SNR 7 in all measured eligible paths, no retained match | 19 | 5 |
| Match retained in eligible paths | 12 | 28 |
| Primary median maximum matched-radius box SNR | 4.21 | 15.10 |
| Median apparent primary depth ratio before detrending | 1.006 | 1.002 |
| Median apparent primary depth ratio after detrending | 1.006 | 1.005 |
| Median paired change in apparent depth ratio | -0.00374 | -0.00083 |
| Primary median local robust scatter, ppm | 3083 | 2803 |
| Median matched primary centre displacement, fraction of duration | 0.0172 (12) | 0.0191 (28) |
| Median local scatter within two catalogue widths, ppm | 4222 (7) | 2952 (2) |
| Median local scatter at least two widths away, ppm | 2961 (24) | 2803 (31) |

All above-bar reference candidates in the matching radius retained a match in at least one eligible path. In the full 400-trial samples, primary median maximum SNR was 6.24 versus 9.34 and local scatter 3070 versus 2221 ppm. The 261 short-bin support-qualified trials yielded 120 retained matches, 140 below-bar cases and one without a finite box. The 277 comparison-bin trials yielded 164 retained matches, 104 below-bar cases, one above-bar candidate without a retained match and eight without an eligible path measurement. This diagnostic limits the score to the selected primary/SAP paths. T156's original any-product event stage can therefore differ in the full-band sample. Primary depth ratios are available for 258 short and 269 comparison trials. Median paired changes were -0.00127 and +0.00056. Matched centre displacement medians were 0.0331 and 0.0214 durations (117 and 161). The whole-reference recovery counts after both tier changes are 7/48 and 23/47.

**CONFIRMED** low box SNR is the immediate cause of the 19 short-period reference detection misses. In pipeline/detect_v2.py:202-220, SNR uses the robust scatter of duration-specific box means across the prepared file, with coverage requirements. Local scatter is a different observable. In pipeline/stage2_search.py:65-76, the detector applies 7 and merges nearby candidate boxes. Merging and large centre shifts are not supported as the main reference failure. Apparent depth fits include the underlying flux, and a median near unity can coexist with severe attenuation in individual files.

**LIKELY** higher variability/noise and the resulting low box scores are more important than median detrending attenuation here. **UNCERTAIN** whether binary-phase structure is the source. The phase split is small and unadjusted for product, brightness and cadence. It measures local scatter as a residual proxy rather than an isolated eclipse residual. The short and long bins are matched in draw count and design, with distinct stars and product mixes.

## Candidate for a later bench

Node 1.5, test one cross-cycle binary-phase baseline removal in the 5 to 10 day bin. Keep the present masks and 2-day biweight. On its output, group finite samples into phase cells with nominal time width equal to the existing detector bin width. Estimate a cell's correction as the median flux from other binary cycles using the same catalogue period and epoch. Require support from at least two distinct other cycles so one other transit cannot set the entire template. Leave cells without that support unchanged and leave the path unchanged when the catalogue ephemeris is missing. Apply the same procedure to each sign. This targets coherent variation and avoids using the evaluated cycle to build its own correction. Residual improvement and protection against multi-cycle transit attenuation need a separate test. No parameters were selected by trying variants on this bench.

Predeclared acceptance for that future trial is the 004 rule: equal-bin reference R must rise above the combined baseline, background upside-down tier-1 at most old + 2 x sqrt(old + 1), all five paired 99% intervals contain zero. Reuse the fixed 2,000 draws and equivalent background population, with the only new treatment in the short bin. This is a detection change requiring new short-bin paired and un-injected processing. The 800 dip-only diagnostic took about nine minutes elapsed after launch of the corrected G2 workers. A defensible background and paired rerun is materially larger. No candidate was run. Scope the phase-coherence check before committing to that run.

Evidence: 005_detection.py, 005_diagnostic_summary.py, private diagnostic-summary.json and per-worker progress.json. No new pipeline bug established. Harness issue above is resolved by full parity, Tree node 3.2. STOP SIGNS: the recorded SAP mismatch stopped the first attempt. QUEUE PROPOSALS: node 1.5 T161, file the below-threshold diagnosis and phase-coherence question. IDEAS: the one test above. Questions for Ahmed: none for this diagnosis. Branch astra/005-three-diagnoses. Usage in combined ledger.
