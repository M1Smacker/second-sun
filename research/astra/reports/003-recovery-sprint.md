# 003 recovery sprint (Codex; runtime model/effort unverified, Astra High requested)

**Plain verdict: R = 27.47% [20.72%, 33.71%]: FIX FIRST. The chain recovers about one in four reference transits.**

**Branch:** astra/003-recovery-sprint. Final reading of completed T156/T158, 13 Nov 2026. Claude completed the resumed execution; Codex completed this interpretation. G1 preparation waits under the filed bar. The 5 to 10 day bin is a named blind spot, 6/48 = 12.5%. No frozen source, filed verdict, decision bar or Tree entry was changed here.

## Bugs found

**CONFIRMED, Tree node 1.1, FIX 91:** opposite-sign coincidence handling is asymmetric. pipeline/stage2_search.py:194 passes opposite-arm events into the dip veto, while :195 passes an empty list for the bump. pipeline/detect_v2.py:274 flags the coincidence; pipeline/stage3_core.py:65 and :254 turn it into tier 2. The earlier runtime synthetic counterexample in 003_checks.py gives dip tier 2 and bump tier 1B. Aggregate recovery agreement does not erase a code counterexample. The measured net recovery cost of this flag is not established by that synthetic test. Claude already filed FIX 91; do not create a duplicate.

**CONFIRMED, Tree node 1.3, reporting correction:** 22 to 55 in the multi-window output counts matched **injected bump recoveries**, not additional noise-only false alarms. See 003_study.py's bump_baseline/bump_union expressions and 003_worker.py's sign=-1 injection and matching rule. This bench contains deliberately planted positive signals; recovering them cannot by itself be called a false alarm. Nevertheless the selected-failure study also cannot establish unchanged background alarms. The Tree's adoption criterion is not demonstrated.

Harness bookkeeping issues fixed before completion: stale supervisor progress at startup and commented-header handling in the metadata census. Node 3.2. Neither changed trial design or thresholds. The resume path was subsequently exercised by Claude, completing 1011 remaining pairs, according to the follow-up and completed journals. This supersedes the earlier NOT TESTED resume label. No new injections or search runs were made in this follow-up.

## Part 1: what the measurement establishes

CONFIRMED: 2000 unique paired trials, 400 per period bin, 510 sampled stars and 1753 distinct groups. Independent aggregation in 003_followup.py reproduces R exactly from the journals. There are 222 reference trials, with 61 dip recoveries and 62 bump recoveries. R is the equal-weight mean of five bin rates, not simply 61/222. The stored 10000-draw star-cluster bootstrap gives the interval above, with no empty-bin redraws. Its arithmetic was previously checked against 200 explicit synthetic resamples; this follow-up did not independently regenerate the confidence interval.

Across the entire broader depth/duration range, 394/2000 dips and 400/2000 bumps recover. Conditional reference R, given a centre inside the searched window, is 35.81% with equal bin weights. Keeping gaps and missing windows in the denominator lowers it to 27.47%. This difference is why the old conditional figures cannot stand in for raw-span sensitivity. These are injected single-transit rates on design data, not planet occurrence, transit geometry, G1 sensitivity or the probability of discovering a whole multi-transit planet.

The first 20 timed pairs averaged 4.992 seconds per pair, median 4.130 seconds, excluding campaign setup. The completed journals average 3.626 seconds per pair; that is worker processing time, not total wall-clock time. Timing justified retaining all 2000 preselected draws. No recovery outcome determined sample size.

Completed-run source parity and successful process exits are reported by Claude's follow-up. The saved results contain no diagnostic inconsistencies between final recovery and stage progression; 15 full-band dip trials were conservatively excluded because a baseline event already matched. Zero-difference checks support reproduction, not semantic correctness or an independent audit of the harness.

## Losses in Tree order

### Node 1.1: detected events held below tier 1

CONFIRMED: 53/222 reference trials (23.9%) stop here, the largest individual reference loss. The broad-band count is 443/2000; the strong-depth count is 158/439. The reference table below was newly computed from existing saved injected-event files, with their allowed design context reassembled for final flags. This is metadata-only tier attribution, not a rerun of light-curve detection. Script: 003_reference_flags.py; private outputs reference-flags-g2.json and reference-flags-g3.json.

| Flag or reason | Reference trials carrying it | Released if only this flag is cleared |
|---|---:|---:|
| repeater | 17 | 13 |
| step | 18 | 1 |
| gap_dump | 17 | 5 |
| ramp | 9 | 5 |
| dominated | 5 | 3 |
| c5 | 4 | 0 |
| ecl_overlap | 3 | 0 |
| common | 1 | 1 |
| orbit_lock | 1 | 0 |
| p1_veto | 5 | 2 |
| flipmatch | 1 | 0 |
| second_product_disagreement | 0 | not evaluated |
| no_primary_snr7 | 0 | not evaluated |
| preexisting | 3 | not evaluated |


Counts overlap. A trial can carry several flags; the last column clears one flag on the matched candidates while holding every other feature fixed. It is a static release count, not the measured gain of a new filter, and cannot be summed across flags. Combination rows are unions across a trial's matched primary candidates, not necessarily one event's exact combination. Trials lacking a primary SNR>=7 event or with prior matching events are kept separately.

| Combination present on matched primary candidates | Trials |
|---|---:|
| repeater | 13 |
| gap_dump+step | 7 |
| gap_dump | 5 |
| ramp | 5 |
| dominated | 3 |
| gap_dump+ramp+step | 2 |
| p1_veto | 2 |
| c5+ecl_overlap+step | 2 |
| p1_veto+repeater+step | 1 |
| gap_dump+repeater+step | 1 |
| p1_veto+ramp | 1 |
| c5+ecl_overlap | 1 |
| c5+gap_dump+ramp+step | 1 |
| step | 1 |
| orbit_lock+p1_veto | 1 |
| dominated+step | 1 |
| common | 1 |
| flipmatch+gap_dump+repeater+step | 1 |
| dominated+repeater+step | 1 |


Repeater first: pipeline/stage3_core.py:21 sets the count threshold to three, :272 flags on that count, and :284 counts all same-kind events in the product/sector. It does not establish that those events belong to the same physical periodic source. Thus unrelated excursions can demote an otherwise valid injected transit. CONFIRMED mechanism; attributing every repeated real event to eclipse leftovers is UNCERTAIN. The same-period physical test would be a future candidate, not a silent alteration of this result.

Other mechanisms: step checks reject inadequate side coverage or a lifted baseline (stage3_core.py:116-129); gap/dump proximity comes from detect_v2.py:278-281; the one-day ramp is stage3_core.py:70 and :273; dominance compares with the strongest opposite-arm event (:291-295). Multiple safeguards can veto the same transit. Removing all safeguards is not the recommendation.

### Node 1.2: windows and gaps

CONFIRMED: 45/222 outside-window/gap losses plus 7/222 no-safe-window losses, 52/222 combined (23.4%). The broad-band counts are 316 and 59. stage2_search.py:150-160 restricts products requiring windows to own SPOC coverage or at least two neighbours and returns no product otherwise. Input time gaps also remain in the trial denominator. The 45 cannot all be restored by changing that rule: some are genuinely absent samples. Existing summary diagnostics do not separate every true missing-cadence gap from deliberately discarded light, so the recoverable subset is UNCERTAIN. A 52/222 release is only an impossible-best-case bound, not a gain forecast.

### Node 1.3: detection

CONFIRMED: 41/222 reference trials survive support checks but produce no matched event; across the full range this is 570/2000, the largest broad-band loss. stage2_search.py:48-78 detrends, bins, scores a fixed duration grid, applies SNR>=7 and merges nearby candidates. detect_v2.py:173 supplies the 2-day biweight default. Existing journals do not separate insufficient SNR, detrending attenuation, event merging and shifted centres outside the half-duration match tolerance. Detrending alone as the cause is UNCERTAIN. The window experiment below tests one limited intervention.

### Node 1.4: mask and sample support

CONFIRMED: 15/222 reference trials fail this diagnostic, 218/2000 over the full range. petrova_mask.py:164-173 removes catalogue windows and a repeat-based complement; :197-211 returns the retained samples. stage2_search.py:161-170 requires adequate samples before and after masking. The harness additionally requires at least half the nominal transit samples, minimum three. This label therefore includes inadequate support/preparation, not a causal proof that the eclipse mask alone destroyed every one of the 15 transits. No proposed gain assumes all are recoverable.

### Node 1.5: why the 5 to 10 day bin is worse

CONFIRMED: its 48 reference trials split into 3 no-window, 9 outside/gap, 5 mask/support, 19 no-event, 6 tier losses and 6 recovered. No-event losses are 39.6%, versus 22/174 = 12.6% in all other bins. Tier losses are only 12.5% here versus 47/174 = 27.0% elsewhere; window losses are 25.0% versus 23.0%. The excess short-period loss is therefore primarily before event detection, not unusually harsh final flags. Mask/support contributes a smaller excess, 10.4% versus 5.7%.

The tables show lower short-bin recovery within each of QLP, SPOC and TESS-SPOC and within each campaign. Product/campaign mix alone does not remove the pattern, but the within-cell counts are small. Increased binary variability or residual structure interfering with detrending/detection is LIKELY as a hypothesis, not established causally by these traces. Isolating it needs saved stage-level signal measurements or a predeclared intervention. Do not tune a special short-period threshold from these outcomes.

## Part 2: multi-window verdict

CONFIRMED: the original three-window union gains 41 dips among 570 selected detection failures. Planted-bump recoveries rise from 22 to 55, an additional 33. The 375 window/gap failures are not repaired. This is a sensitivity exploration on selected failures, not a new unconditional R or an unbiased arm comparison. Originally recovered dip trials were not all reprocessed, so cross-event interactions of a production multi-window filter remain unmeasured.

Existing-results-only alternatives: adding 1 day gains 40 dips and 30 planted bumps; adding 3 days gains 2 and 3. Requiring both alternatives to agree, while retaining the original 2-day route, gains **one dip and zero additional planted bumps** in this selected sample. That is an exploratory post hoc combination of saved outcomes, not a chosen setting or an independently validated success. No un-injected alternate-window background-alarm comparison exists here. Verdict: **no demonstrated production-ready win**. Keep the one-dip agreement observation as a low-priority lead, do not promote the 41-dip union.

Primary method/licence review and the one-page STANLEY feasibility note remain in [003-methods.md](003-methods.md). Availability is 703 multi-sector design stars, not 703 systems with adequate orbital solutions. No external method was installed or run. Published-reference coverage limitations and exact archive links remain in [003-published-reference.md](003-published-reference.md): the fixed injection range misses the available 500-ppm Kepler-38 value and cannot be verified for missing archive fields. Historical conditional recovery comparisons remain in [003-history.md](003-history.md); their original results are not overwritten.

## What I would do next and why

1. **Node 1.1, repeater association candidate first.** Replace indiscriminate same-kind event counting with a predeclared association test for repeated binary structure, retaining independent step/gap/other safeguards. The reference static ceiling for clearing repeater alone is 13 of 222 trials, not a promised gain. Price on the same 2000 draws and unchanged matching rule, report reference and all-bin gains and losses, paired bumps, and un-injected upside-down alarm counts. Risk: releasing genuine recurring systematics. Claude designs one concrete candidate; Ahmed decides.
2. **Node 1.1, symmetric FIX 91, then coverage-aware step handling.** Symmetric coincidence handling has a confirmed correctness motive; its reference static clear-flag release is 0. Clearing step alone releases 1 reference trials with other features frozen. Do not equate clearing the whole step flag with a coverage-only fix. Test each change separately on the unchanged full bench and un-injected controls; risk is admitting steps, ramps or paired instrumental features. A symmetry fix may reject additional bumps rather than gain dips, so it must be priced honestly.
3. **Node 1.2, coverage repair before arbitrary window widening.** Trace which of the 52 window/gap reference failures have usable recorded data and missing safe-window evidence. Restore only independently justified safe coverage; its actual gain is NOT TESTED and bounded by that count. Reuse all 2000 draws including irreparable gaps and compare background controls. Risk: scattered-light systematics. Do not loosen safety just to recover injections.

Node 1.5/1.3 remains a separate diagnosis after the active flag candidate: the short-period detection weakness is real, but the current multi-window union is not a justified production fix. Node 1.4 follows later; its measured reference loss is smaller and not mask-only. These rankings advise Claude and Ahmed; they do not authorize a version change.

## Checks, exclusions, stop signs and handoff

CONFIRMED checks in this follow-up: unique journal count and exact R re-derivation without pipeline imports; per-bin stage totals sum to their denominators; saved-window alternative counts; metadata-only reference flag attribution. Full final tables follow. The stored confidence intervals are reused, not independently recomputed. No new FITS search, injection, threshold tuning, external upload, dependency installation or frozen edit.

STOP SIGNS: the earlier usage stop is historical and resolved by Claude's completed run. No new stop sign encountered. Wording disagreement for review: planted-bump recovery is not an observed noise-only alarm rate; this changes interpretation of the study, not the filed FIX FIRST decision. No claim of an independently validated Petrova patch.

QUEUE PROPOSALS: node 1.1, append these reference-band prices to the existing repeater/T34 work and FIX 91; node 1.3, correct the planted-bump/alarm wording and retain the post hoc one-dip agreement observation without promoting it; node 1.5, file the 19/48 detection-stage concentration as a diagnostic question. No queue or Tree files edited. IDEAS: only the ranked candidates above, costs are future full-bench and background-control runs; runtime and model usage are not yet sized. Questions for Ahmed: none needed to finish this report; the first candidate remains his and Claude's decision.

## Usage

Initial 003 baseline 32% weekly; prior stop 46% before its final checkpoint overhead. Follow-up baseline 15% five-hour / 49% weekly, prediction 20 five-hour points / 4 weekly. Conservative cap remains weekly 57%, accounting for all intervening account use. Final actual is recorded in USAGE.md and the closing entry below. Separate part costs cannot be recovered from overlapping execution and research. Lesson: record matched injected-control recovery separately from un-injected false alarms.

Follow-up pre-commit actual, 22:20 Kuwait: 15% to 32% five-hour (+17 points), 49% to 52% weekly (+3 points). Whole-brief account-window span is 32% to 52% weekly (+20), including unallocated account/checkpoint overhead, not a precise task-only charge. Remains below the conservative 25-point cap.

## Frozen design retained for provenance

Seed 2026111303. Draw with replacement uniformly from eligible stored design-seen groups within each binary-period bin, pooled G2/G3. One catalogue period per star/campaign, first target-list row, matching the catalogue loader's deduplication convention. Pool sizes: 3423,2354,1856,740,1356. 400 paired trials per bin, 2000 dip trials plus their 2000 bump controls; the first 20 are four per bin in interleaved order. Private draws: data/astra/003/design.json, SHA256 2952bbd022a3697e242700fad1283ee3785ca4b60e53dd822e973d2b47549eff. All group selections, time fractions, depths and durations are fixed before outcomes. Keep the first 20 in the final analysis. Trial count may be reduced only by measured runtime/available resources, taking a balanced prefix, never recovery results.

Time is uniform between first and last raw-loaded timestamps of the frozen best product; if the best row/file is unavailable, use the first sorted stored primary file to define the span and retain missing-best status in the denominator. Missing raw spans are recorded as input failures, not replaced with other groups. Uniform means continuous time, including internal gaps. Depth is log-uniform 1000 to 10000 ppm, duration log-uniform 3 to 18 h. Trapezoid ingress and egress are each 10% of total duration (20% combined, as the brief states); this differs from the 002 pilot's 20%-per-side shape. Both signs use the same draw. Raw injection uses S2.load, after its quality/finite-value selection, before windows, eclipse masks and detrending. Quality-rejected timestamps before loading are outside the input definition; internal gaps remain in the denominator.

Zero injection on every distinct drawn group must exactly reproduce stored primary and SAP event dictionaries including the PDC check before its injections run. Repeated draws may reuse an already-verified baseline only if source-file hashes and settings are unchanged; this is the same group, not another untested group. A real mismatch stops all trials. Private full traces preserve errors; no event details or identifiers are printed in reports.

The union/tiering context includes the star's other design sectors plus other design stars in the same sector/camera, exactly the dependencies of common-moment, c6 and Petrova veto rules. Shared frozen burst/window/reference inputs remain machine-only reads. All sampled files must pass the existing design allowlist. Full-campaign context is prepared from allowed groups only, never fenced events.

Stages, fixed before trials: (1) at least one eligible best primary/SAP product has a defined safe-window route; (2) the centre is within 1.5 median raw cadences of a windowed timestamp (counts gaps as loss); (3) at least half the nominal in-transit cadence count, and at least three points, remain after eclipse masking; (4) a same-arm event at any tier is found within half the injected duration of its true centre; (5) a matched primary event reaches tier 1A/1L/1B with SNR>=7. Record the earliest failed stage for the sequential loss table and the stage flags separately. Do not use a wider event-match radius. If a baseline event already meets the match criterion, mark attribution ambiguous, retain the denominator and conservatively do not claim a recovered injection. Technical exceptions are recorded separately and repaired/retried, never counted as scientific failures without diagnosis.

R uses only depths 3000 to 6000 ppm and durations 6 to 12 h, with equal weight for the five period-bin rates. The interval uses 10000 bootstrap draws of whole stars (campaign plus star key), retaining all of each star's trials and recomputing bin means then equal weighting. Redraw bootstrap realizations with an empty reference bin; report their frequency. If an original bin has no reference trials, R is unavailable rather than imputed. Binned depth edges: 1000,2000,3000,6000,10000 ppm; duration edges: 3,6,12,18 h. Product and era splits follow the brief; brightness edges 11,12,14 magnitudes. For dip/bump comparison use paired differences with the same star-cluster bootstrap, simultaneous 99% per-bin intervals (Bonferroni across five bins); flag a difference excluding zero as an arm concern, not an automatic causal attribution to a particular line. Report discordant-pair counts as well.

Time the first 20 paired trials, including zero checks/context setup separately. Choose worker count after inspecting existing Python load, at most four workers with two Numba threads each, at most three if other jobs exist. No worker changes global system settings. Progress JSON under data/astra/003 records completed/planned dip draws, paired-arm counts, phase, status and UTC update. Runtime, not observed recovery, determines whether the 2000-pair target fits. No fixed two-hour ceiling is imposed by this brief; report the projection and continue within the usage/speed limits.

Harness addition: 12 verified copies under scripts/harness/sprint003; only output path literals changed from 002 to 003 in audit_all, dataset, stage2_search and stage3_report. New 003_harness reuses the same guard scoped to 003. Smoke runtime passed the existing synthetic mask test, verified 12 hashes, rejected three forbidden probes and completed an allowed write. This is a Python audit hook, not an OS sandbox.

## Final result tables

CONFIRMED: independent journal aggregation, no pipeline imports or new searches. Counts are dip recoveries unless stated. Intervals are the saved star-cluster bootstrap, not independently recomputed.

## Period and paired control

| Period d | Ref recovered/n | Ref R, 95% CI | All dip/bump (n=400) | Dip-only / bump-only | Paired difference 99% CI, points |
|---|---|---|---|---|---|
| 5 to 10 | 6/48 | 12.5% [4.0%, 23.1%] | 47/55 | 9/17 | [-5.25, 1.26] |
| 10 to 14 | 9/35 | 25.7% [11.1%, 40.0%] | 78/69 | 15/6 | [-0.78, 5.21] |
| 14 to 20 | 12/46 | 26.1% [14.0%, 39.0%] | 71/80 | 10/19 | [-5.53, 1.18] |
| 20 to 27.4 | 19/47 | 40.4% [20.0%, 57.9%] | 91/80 | 21/10 | [-1.41, 8.26] |
| 27.4+ | 15/46 | 32.6% [18.9%, 46.2%] | 107/116 | 12/21 | [-6.93, 2.52] |

All five paired, star-clustered 99% intervals include zero (Bonferroni across five bins). This is no detected aggregate difference, not proof of equivalence or absence of a structural bug. Reference totals: 61 dips, 62 bumps.

## Sequential losses

### Reference

| Period d | n | No windows | Outside/gap | Mask/support | No event | Below tier 1 | Caught |
|---|---|---|---|---|---|---|---|
| 5 to 10 | 48 | 3 (6.2%) | 9 (18.8%) | 5 (10.4%) | 19 (39.6%) | 6 (12.5%) | 6 |
| 10 to 14 | 35 | 1 (2.9%) | 6 (17.1%) | 2 (5.7%) | 10 (28.6%) | 7 (20.0%) | 9 |
| 14 to 20 | 46 | 2 (4.3%) | 8 (17.4%) | 2 (4.3%) | 6 (13.0%) | 16 (34.8%) | 12 |
| 20 to 27.4 | 47 | 1 (2.1%) | 10 (21.3%) | 3 (6.4%) | 5 (10.6%) | 9 (19.1%) | 19 |
| 27.4+ | 46 | 0 (0.0%) | 12 (26.1%) | 3 (6.5%) | 1 (2.2%) | 15 (32.6%) | 15 |

### All depths/durations

| Period d | n | No windows | Outside/gap | Mask/support | No event | Below tier 1 | Caught |
|---|---|---|---|---|---|---|---|
| 5 to 10 | 400 | 16 (4.0%) | 66 (16.5%) | 57 (14.2%) | 137 (34.2%) | 77 (19.2%) | 47 |
| 10 to 14 | 400 | 16 (4.0%) | 68 (17.0%) | 36 (9.0%) | 119 (29.8%) | 83 (20.8%) | 78 |
| 14 to 20 | 400 | 10 (2.5%) | 61 (15.2%) | 32 (8.0%) | 126 (31.5%) | 100 (25.0%) | 71 |
| 20 to 27.4 | 400 | 17 (4.2%) | 55 (13.8%) | 51 (12.8%) | 107 (26.8%) | 79 (19.8%) | 91 |
| 27.4+ | 400 | 0 (0.0%) | 66 (16.5%) | 42 (10.5%) | 81 (20.2%) | 104 (26.0%) | 107 |

## Product, era, campaign and brightness

Equal-bin R standardizes over five period bins; pooled reference fractions are also shown. Missing-best groups stay in the denominator. Sparse subgroup rates are descriptive, not separately calibrated decisions.

### product

| Group | All n | Dip / bump | Ref recovered/n | Equal-bin R |
|---|---|---|---|---|
| QLP | 852 | 114/123 | 19/90 | 22.4% |
| SPOC | 470 | 120/125 | 17/57 | 32.5% |
| TESS-SPOC | 599 | 160/152 | 25/68 | 34.9% |
| nan | 79 | 0/0 | 0/7 | Unavailable |

### campaign

| Group | All n | Dip / bump | Ref recovered/n | Equal-bin R |
|---|---|---|---|---|
| g3 | 421 | 35/35 | 9/45 | 20.3% |
| g2 | 1579 | 359/365 | 52/177 | 28.5% |

### era

| Group | All n | Dip / bump | Ref recovered/n | Equal-bin R |
|---|---|---|---|---|
| 56-93 | 757 | 132/137 | 22/87 | 26.8% |
| <56 | 1070 | 240/241 | 36/114 | 30.4% |
| >=94 | 173 | 22/22 | 3/21 | 15.7% |

### brightness

| Group | All n | Dip / bump | Ref recovered/n | Equal-bin R |
|---|---|---|---|---|
| 12-14 | 486 | 29/33 | 5/49 | 12.3% |
| 11-12 | 476 | 98/100 | 23/57 | 37.4% |
| <11 | 1038 | 267/267 | 33/116 | 28.4% |

## Depth and duration cells

| Depth ppm | Duration h | n | Dip | Bump | Dip rate |
|---|---|---|---|---|---|
| 1000 to 2000 | 3 to 6 | 232 | 23 | 20 | 9.9% |
| 1000 to 2000 | 6 to 12 | 231 | 28 | 24 | 12.1% |
| 1000 to 2000 | 12 to 18 | 158 | 18 | 16 | 11.4% |
| 2000 to 3000 | 3 to 6 | 147 | 20 | 22 | 13.6% |
| 2000 to 3000 | 6 to 12 | 136 | 32 | 33 | 23.5% |
| 2000 to 3000 | 12 to 18 | 77 | 14 | 14 | 18.2% |
| 3000 to 6000 | 3 to 6 | 224 | 64 | 64 | 28.6% |
| 3000 to 6000 | 6 to 12 | 222 | 61 | 62 | 27.5% |
| 3000 to 6000 | 12 to 18 | 134 | 15 | 19 | 11.2% |
| 6000 to 10000 | 3 to 6 | 173 | 68 | 65 | 39.3% |
| 6000 to 10000 | 6 to 12 | 174 | 44 | 52 | 25.3% |
| 6000 to 10000 | 12 to 18 | 92 | 7 | 9 | 7.6% |

## Saved-window alternatives (exploratory post hoc reading)

No new settings were run. Agreement is a post hoc diagnostic, not a validated selected rule. Bump gains below are newly recovered injected bumps, not background false alarms.

| Rule on selected failures | New dips | New planted bumps |
|---|---|---|
| 2+1 day union | 40 | 30 |
| 2+3 day union | 2 | 3 |
| 2+1+3 day union | 41 | 33 |
| 2 plus agreement of 1 and 3 | 1 | 0 |

## Short-period context

| Split | Group | 5 to 10 d recovery | Other bins pooled |
|---|---|---|---|
| product | QLP | 2/25 | 17/65 |
| product | SPOC | 3/12 | 14/45 |
| product | TESS-SPOC | 1/8 | 24/60 |
| product | nan | 0/3 | 0/4 |
| campaign | g2 | 5/32 | 47/145 |
| campaign | g3 | 1/16 | 8/29 |
| brightness | 11-12 | 0/7 | 23/50 |
| brightness | 12+ | 1/15 | 4/34 |
| brightness | <11 | 5/26 | 28/90 |

