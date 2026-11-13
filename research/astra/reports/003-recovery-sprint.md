# 003 recovery sprint (Codex; runtime model/effort unverified, Astra High requested for judgement)

**Plain verdict: NOT MEASURED. Design frozen before any injection trial.** Branch `astra/003-recovery-sprint`. No frozen source or decision bar is edited.

## Bugs found
None established yet. Missing evidence is not silently replaced with an assumption.

## Part 1: frozen design

Seed 2026111303. Draw with replacement uniformly from eligible stored design-seen groups within each binary-period bin, pooled G2/G3. One catalogue period per star/campaign, first target-list row, matching the catalogue loader's deduplication convention. Pool sizes: 3423,2354,1856,740,1356. 400 paired trials per bin, 2000 dip trials plus their 2000 bump controls; the first 20 are four per bin in interleaved order. Private draws: data/astra/003/design.json, SHA256 2952bbd022a3697e242700fad1283ee3785ca4b60e53dd822e973d2b47549eff. All group selections, time fractions, depths and durations are fixed before outcomes. Keep the first 20 in the final analysis. Trial count may be reduced only by measured runtime/available resources, taking a balanced prefix, never recovery results.

Time is uniform between first and last raw-loaded timestamps of the frozen best product; if the best row/file is unavailable, use the first sorted stored primary file to define the span and retain missing-best status in the denominator. Missing raw spans are recorded as input failures, not replaced with other groups. Uniform means continuous time, including internal gaps. Depth is log-uniform 1000 to 10000 ppm, duration log-uniform 3 to 18 h. Trapezoid ingress and egress are each 10% of total duration (20% combined, as the brief states); this differs from the 002 pilot's 20%-per-side shape. Both signs use the same draw. Raw injection uses S2.load, after its quality/finite-value selection, before windows, eclipse masks and detrending. Quality-rejected timestamps before loading are outside the input definition; internal gaps remain in the denominator.

Zero injection on every distinct drawn group must exactly reproduce stored primary and SAP event dictionaries including the PDC check before its injections run. Repeated draws may reuse an already-verified baseline only if source-file hashes and settings are unchanged; this is the same group, not another untested group. A real mismatch stops all trials. Private full traces preserve errors; no event details or identifiers are printed in reports.

The union/tiering context includes the star's other design sectors plus other design stars in the same sector/camera, exactly the dependencies of common-moment, c6 and Petrova veto rules. Shared frozen burst/window/reference inputs remain machine-only reads. All sampled files must pass the existing design allowlist. Full-campaign context is prepared from allowed groups only, never fenced events.

Stages, fixed before trials: (1) at least one eligible best primary/SAP product has a defined safe-window route; (2) the centre is within 1.5 median raw cadences of a windowed timestamp (counts gaps as loss); (3) at least half the nominal in-transit cadence count, and at least three points, remain after eclipse masking; (4) a same-arm event at any tier is found within half the injected duration of its true centre; (5) a matched primary event reaches tier 1A/1L/1B with SNR>=7. Record the earliest failed stage for the sequential loss table and the stage flags separately. Do not use a wider event-match radius. If a baseline event already meets the match criterion, mark attribution ambiguous, retain the denominator and conservatively do not claim a recovered injection. Technical exceptions are recorded separately and repaired/retried, never counted as scientific failures without diagnosis.

R uses only depths 3000 to 6000 ppm and durations 6 to 12 h, with equal weight for the five period-bin rates. The interval uses 10000 bootstrap draws of whole stars (campaign plus star key), retaining all of each star's trials and recomputing bin means then equal weighting. Redraw bootstrap realizations with an empty reference bin; report their frequency. If an original bin has no reference trials, R is unavailable rather than imputed. Binned depth edges: 1000,2000,3000,6000,10000 ppm; duration edges: 3,6,12,18 h. Product and era splits follow the brief; brightness edges 11,12,14 magnitudes. For dip/bump comparison use paired differences with the same star-cluster bootstrap, simultaneous 99% per-bin intervals (Bonferroni across five bins); flag a difference excluding zero as an arm concern, not an automatic causal attribution to a particular line. Report discordant-pair counts as well.

Time the first 20 paired trials, including zero checks/context setup separately. Choose worker count after inspecting existing Python load, at most four workers with two Numba threads each, at most three if other jobs exist. No worker changes global system settings. Progress JSON under data/astra/003 records completed/planned dip draws, paired-arm counts, phase, status and UTC update. Runtime, not observed recovery, determines whether the 2000-pair target fits. No fixed two-hour ceiling is imposed by this brief; report the projection and continue within the usage/speed limits.

Harness addition: 12 verified copies under scripts/harness/sprint003; only output path literals changed from 002 to 003 in audit_all, dataset, stage2_search and stage3_report. New 003_harness reuses the same guard scoped to 003. Smoke runtime passed the existing synthetic mask test, verified 12 hashes, rejected three forbidden probes and completed an allowed write. This is a Python audit hook, not an OS sandbox.

## Published-reference check, before trials

NASA Exoplanet Archive composite-table API returned 14 transiting circumbinary planets, only two with a populated transit-depth field and one with a populated duration field. Exact query and extracted rows are retained in data/astra/003/published-reference.json. The brief's fixed range is retained; missing archive fields cannot establish that it covers all published transits. A composite scalar also cannot represent all variable-duration transits of a circumbinary planet. No values will be invented and the trial range will not be retuned after results.

## Part 2 plan

Use only Part 1 failures before detection for the multi-window design study. Preserve their original masks, windows and all downstream rules; compare the union of detection candidates from independently detrended 1,2,3-day windows against the frozen route, with the same bump controls and matching rules. Do not claim this repairs absent windows: those remain unavailable. This is a minimal multi-window idea, not a faithful implementation or benchmark of all mono-cbp. Diagnose stage-specific losses before choosing any production proposal. STANLEY is a feasibility note only, no implementation or installs.

## What I did NOT check
No real injection or recovery outcome has been inspected at this design commit. No claim of a calibrated rate, published-planet coverage, external-method performance or G1 readiness.

## STOP SIGNS / QUEUE PROPOSALS / IDEAS / Questions
None active at design freeze. No extra build outside the brief. No question for Ahmed is needed to execute the fixed experiment.

## Usage
Baseline 5% five-hour / 32% weekly. Part 1 predicted 12 weekly points within its 18-point guide; total brief cap 25 points. Actual recorded after work. Skills: auditor, mailbox, research.
# Timing and full-run launch

CONFIRMED: first 20 paired trials completed, with zero-injection identity on all 20 distinct groups. Mean paired-trial processing time 4.992 seconds, median 4.130 seconds, summed worker processing 99.839 seconds. Campaign startup added 40.729 and 12.953 seconds; these are separate from per-trial timing. This permits the originally planned 2,000 pairs, 400 per period bin. Four workers with two Numba threads each are planned for the remaining 1,980 pairs, approximately 42 minutes of ideally balanced processing at the measured mean, plus startup and workload imbalance. This estimate controls runtime only. No recovery number changed the sample or thresholds.

