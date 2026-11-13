# 002 Petrova statistics audit, Part 0 (GPT-6.1 Sol, effort unverified, 13 Nov 2026, 00:01 Kuwait)

**RUN-MODE RESUME POINT:** stopped after Part E at the authorized five-hour speed limit, observed 89% five-hour / 18% weekly. Start Part A next: inspect mask and call sites, run predefined synthetic dip/bump grid (periods 5, 10, 14, 20, 30, 50 d; one, two, four sectors), off-switch comparison and single-visit veto checks. Then D, C, F, G. Only an introductory mask-source read occurred; no Part A experiment has run. B's anonymous cluster intervals and E's gate/loss audit are now filed below. The old moved-number review stop is lifted by run mode. No final ranking is yet justified. Full audit remains incomplete.

**Current verdict:** Three primary groups replay identically. Part B independently reproduces all eight filed S1 chances. The sensitivity wording needs correction; the G2 conditional planting calculation changes a decision number by more than 10%, triggering the brief's review stop. SAP/union replay and Parts E, A, D, C, F, G remain untested. Earlier checkpoints below are retained as history and superseded where stated.
**Branch:** astra/002-petrova-audit. Source base c173b11c70b18d5bde81565d26157d80503af8e9.
**Handling note:** A source diagnostic surfaced pre-existing identifiers in its tool output while locating the copied lines. The staged payload omits those identifiers. No event file or light curve was opened.

## Bugs found
- **CONFIRMED, medium, gate coverage reporting:** `pipeline/r1_gate.py:180` to 187 treats absent or undefined comparisons as preserving PASS. Four missing-bin/arm checks occur in sealed G3; no development injection verdict depended on a missing bin, and no filed ratio used the undefined zero-recovery branch. Part E supplies executed counts and a proposed explicit INCOMPLETE status, without changing a filed verdict.
- **CONFIRMED, reporting/statistical interpretation, material to planning.** `pipeline/r1_readout.py:84` to 92 uses unstratified Fisher thresholds for the stratified verdict's power line. A deterministic significance threshold is also presented as an exclusion limit, without a sampling-power calculation. Part B below verifies the filed verdict probabilities but does not support that exclusion claim. Proposed correction only; filed results untouched.
- **CONFIRMED, helper setup only, fixed.** The guard initially left scientific-library temporary files and Numba cache paths outside the writable subtree. Full traceback identified the Numba failure; redirected storage enabled three primary replays. No production-filter defect follows from this.
- **SUPERSEDED authorization issue, not a production bug:** the following original shared-input finding was lifted by updated AGENTS rule 2.
- **CONFIRMED, high severity for fence isolation.** pipeline/stage2_search.py:110 to 133 initializes burst state from the campaign-wide audit event table and may open a reference FITS chosen without a design-seen restriction. This is a blocker for a faithful helper replay under the current authorization. It does not establish a scientific error in the production run. The checks below cover source, manifest selection and access refusal. Production behavior was not run.

## Part 0
1. **CONFIRMED, source provenance.** Copied the 12 pinned modules for masking, detection, SAP, tiering and the readout. scripts/harness/provenance.json records every original Git blob and the frozen and copied SHA-256 values. The comparison reconstructed the frozen bytes from the Git blobs: nine LF, three CRLF. All 12 matched. See [the source diff](002-part0-source-diff.md). Alongside path edits, the copies remove an identifier from a comment and empty the control table used by the unused legacy G1 selector. The original files remain unchanged. These are byte and source checks.
2. **CONFIRMED, limited runtime check.** From the helper root, run the approved project venv interpreter with arguments `-I -B research/astra/scripts/002_harness.py`. It prints the configured paths, verifies the copies, and runs Petrova's existing synthetic self-test. Actual output: `petrova_mask selftest passed` and `Verified 12 copied source hashes, 3 rejected access events and one allowed write.` The probes exercise Python audit events for a write outside the output directory, a G1 input and the mixed G2 audit table. A real probe file was written and read back inside data/astra/002. This checks the guarded entry point for ordinary Python file operations. It is not an OS sandbox or a guarantee for direct module execution, native extensions or future multiprocessing. Later runners must enter the guard before loading copies and validate worker startup separately.
3. **CONFIRMED, manifest selection.** A standard-library CSV check reproduced the deduplicate-file then first-SPOC-per-sector selection in stage2_search.py:112 to 116 using filenames and the design-seen catalogue. G2 returned 52 selected references on the design list and 56 outside it. G3 returned 56 on the design list and zero outside. These are sector reference counts, not event counts. Even choosing G3 leaves the separate mixed burst-table dependency at lines 117 to 122. No FITS was opened.
4. **NOT TESTED, zero difference.** Ran zero of the requested three star-sector replays. The guard rejects the campaign-wide audit event table. Dropping the burst state or taking its answers from the stored target groups would not independently verify identical events. No selection of three star-sectors or comparison with stored results was performed.

## What I did NOT check
Real-light parity, full-chain runtime behavior, inputs for additional parts, or any scientific result. No later part started.

## STOP SIGNS hit
The brief permits design-seen light and excludes hold-out events. The default initializer is not fenced by star. A faithful replay needs a Claude-provided fence-safe fixture or adapter that supplies the original burst and momentum-dump context for three approved groups without exposing fenced event records or light. The current guard deliberately blocks that mixed input.

## QUEUE PROPOSALS
BUILD: prepare the three-group replay fixture or adapter, with a documented provenance check and the exact context needed for the event comparison.

## IDEAS
None beyond the replay fixture.

## Disagreements with Claude
None established. The parity requirement remains open.

## Questions for Ahmed
None. Claude can resolve the input dependency.

## Usage
Prediction 10 to 15 five-hour points and 1 to 2 weekly points. Meter baseline 21% five-hour and 8% weekly. See USAGE.md for the final pre-commit reading. Lesson: inspect mixed reference inputs before budgeting a replay.

Next: Claude provides a fence-safe replay fixture so the three-group identity check can run. Setup cost unmeasured, requires Claude.

## Part 0 follow-up, 13 Nov 2026, 00:15 Kuwait

Model GPT-6 Astra, effort unverified. Part 0 names Sol Medium, and the follow-up authorizes carrying on with the app-selected model.

**Verdict: replay failed before the first comparison.** Updated AGENTS rule 2 lifts the previous shared-input blocker. The guard now allows exact campaign manifest, audit, window and best-product inputs plus the frozen manifest's per-sector SPOC references. Reference paths are remapped through the helper data junction. Reads are enabled explicitly and remain subject to the output guard.

Added scripts/002_replay.py. It selects the first three sorted stored development group filenames belonging to design-seen stars, with selection preceding event reads. It writes fresh outputs under a unique data/astra/002 replay folder, compares every stored event field using canonical JSON, and stops on mismatch or recorded processing error. This initial runner covers the primary product groups. SAP replay and final union comparison still need implementation after startup succeeds.

Actual command used the approved venv interpreter with -I -B and redirected output to data/astra/002/replay-followup.log. It ended with exit code 1 and 'Replay stopped: FileNotFoundError', alongside a SciPy MessageStream temporary-file cleanup TypeError. Zero group comparisons completed. The root cause is UNCERTAIN. The restrictive output guard and library temporary-file handling need investigation. The generic exception handler does not preserve enough diagnostic detail to establish the exact missing file. Do not interpret this as a detected science regression.

**STOP SIGNS:** failed replay and follow-up budget reached. The brief explicitly requires stopping at either. Parts B through G have not begun. No sealed verdict or frozen source was changed. No new scientific claim follows from this attempt.

Checks performed were source inspection, scoped machine-input permission wiring, and the failed runtime attempt. No successful full-chain parity test occurred. No further tests were run after the failure.

QUEUE PROPOSAL: diagnose startup using a private traceback and route any required temporary files into data/astra/002, then complete primary, SAP and final union parity before advancing. No new system idea or decision for Ahmed is required.

Usage baseline 40% five-hour / 11% weekly, final observed 46% / 12%. Delta +6 five-hour and +1 weekly, account-wide rounded meters, excluding final checkpoint overhead. Prediction 5 to 8 five-hour, at most 1 weekly. Lesson: native-library startup needs a controlled temporary directory and private exception diagnostics when all writes are guarded.

Next: resume Part 0 with startup diagnostics and the remaining parity steps under a renewed allowance. Requires Ahmed's continuation because the explicit follow-up cap is reached.

## Part 0 follow-up 2, 13 Nov 2026, 00:23 Kuwait

Model GPT-6 Astra, effort unverified; Part 0 requests Sol Medium, continuation on the app-selected model is authorized.

**Verdict: primary replay matched 3 of 3 groups.** This supersedes the earlier startup failure and shared-input stop. The shared-input issue above is an authorization history, not a confirmed filter bug; updated rule 2 permits those machine reads. Its fixture proposal is no longer needed.

**CONFIRMED, harness setup defects fixed.** `002_harness.py` now creates temporary and Numba cache directories under `data/astra/002` before scientific imports. TMP, TEMP, tempfile.tempdir and NUMBA_CACHE_DIR are process-local settings. `002_replay.py` preserves full tracebacks in redirected private logs. The first retry passed the prior SciPy failure but failed at Numba cache initialization; the second completed after cache redirection. No frozen source or copied filter algorithm changed.

**CONFIRMED, runtime evidence:** `replay-followup2b.log` records expected/actual primary event counts 0/0, 1/1, 0/0, all canonical event dictionaries identical, and zero recorded processing errors in all three groups. Selection used the first three eligible sorted filenames before opening event contents. Empty groups make this limited coverage: only one event was compared. This is replay identity, not proof of scientific correctness. SAP and union parity are NOT TESTED and explicitly deferred to Part C.

The separate harness smoke command passed the synthetic mask self-test, verified all 12 copied hashes, rejected three forbidden access probes and completed one allowed write. The guard remains a Python audit hook, not an OS sandbox. Native-extension access is not independently verified. A nonfatal optional lightkurve dependency warning occurred; no package was installed.

STOP SIGNS: none active. QUEUE PROPOSALS: none new. IDEAS: none new. Questions for Ahmed: none. Parts B through G remain pending at this checkpoint.

Usage: baseline 60% five-hour / 14% weekly, observed finish 67% / 15%, +7 and +1 account-wide rounded points before checkpoint overhead. Cap 2 weekly points respected at this reading. Lesson: scientific-library temp and compilation caches must be redirected before import.

Next: begin Part B's independent count statistics, within its four-weekly-point cap; authorized for Codex now.

## Part B simulation design, before calculation

Use only the four filed count tables. Exact test: integer combinatorial weights, enumerated independently without importing pipeline code. Check with 100,000 conditional random label permutations per threshold, fixed seed. For the requested planting calculation, freeze the filed background and distribute a fixed number of added real events among bins in proportion to their sealed bar-7 total event counts. Use 500 placements per dose, doses 0 to 200 in steps of 5. Assume every planted event clears bar 12, hence all four thresholds; this is an optimistic strong-event scenario, not a distribution of astrophysical depths. Evaluate the full filed rule. Report the first grid doses with at least 50% and 90% firing; these are conditional placement probabilities, not unconditional survey power or confidence exclusions. Denominator for comparison is the original bar-7 stratified expected count, fixed before planting. Bin weights, dose grid and scenario will not be tuned to outputs.

A star-cluster bootstrap requires per-star event counts and exposure, including zero-event stars. The supplied aggregate files cannot identify those. Do not open hold-out event files to manufacture them; check for an authorized pre-aggregated input, otherwise mark this subtask unavailable.

## Part B results and review stop

**CONFIRMED: filed S1 arithmetic reproduced.** `scripts/002_statistics.py` imports no pipeline module. It enumerates integer combinatorial weights for reference-sample real counts and sums the lower tail, complementary to counting the sealed upper tail. Separately, NumPy hypergeometric draws simulate conditional label permutation, 100,000 trials per row. Three tiny cases were also checked against exhaustive individual-label subset enumeration, including an empty sealed bin and degenerate reference counts. All three matched within 1e-14. These are independent arithmetic checks, not a validation of event independence.

| Campaign | SNR bar | Filed chance | Independent exact | Permutation estimate |
|---|---:|---:|---:|---:|
| G3 | 7 | 0.4071 | 0.4070997261 | 0.40488 |
| G3 | 8 | 0.5150 | 0.5150324453 | 0.51637 |
| G3 | 10 | 0.5583 | 0.5583333333 | 0.55769 |
| G3 | 12 | 0.8846 | 0.8846153846 | 0.88353 |
| G2 | 7 | 0.3141 | 0.3141222953 | 0.31298 |
| G2 | 8 | 0.4966 | 0.4965963529 | 0.49508 |
| G2 | 10 | 0.4638 | 0.4638007849 | 0.46613 |
| G2 | 12 | 0.1023 | 0.1023391813 | 0.10411 |

All exact values round to the filed values. All permutation estimates lie within the prespecified five Monte Carlo standard-error check. No verdict is reinterpreted: both remain NO EXCESS as filed.

**CONFIRMED within the declared scenario: conditional planting results.** The full stratified rule, including bars 8, 10 and 12, was evaluated for 500 randomized bin placements per dose. Full curves and checks are in private `data/astra/002/statistics.json`; counts-only console output is in `statistics.log`, with an empty error log. Run with the approved venv interpreter and `-I -B research/astra/scripts/002_statistics.py`.

| Campaign | Target firing rate | Last grid dose below / first above | Rate at first above | Total real count at first above | Multiple of original stratified expectation |
|---|---:|---:|---:|---:|---:|
| G3 | 50% | 50 / 55 added | 79.8% | 71 | 4.778 |
| G3 | 90% | 55 / 60 added | 98.6% | 76 | 5.114 |
| G2 | 50% | 55 / 60 added | 54.6% | 92 | 3.293 |
| G2 | 90% | 65 / 70 added | 97.4% | 102 | 3.651 |

The grid spacing is five events; these are first grid crossings, not precise threshold estimates. At 500 trials the largest possible Monte Carlo standard error is 2.24 percentage points. The original stratified expectations are 14.8611 for G3 and 27.9357 for G2. The filed Fisher figures use different denominators, 6*31/8=23.25 and 13*64/31=26.8387, so the multiples are not directly interchangeable. The G3 numerical resemblance between 5.114 and 5.2 does not validate its filed method. G2's 3.293 and 3.651 differ from the quoted 2.7 by about 22% and 35%, respectively. Its grid crossing real counts 92 and 102 also exceed the filed 73 by about 26% and 40%.

**LIMITATION / NOT TESTED:** This is conditional injection-placement sensitivity with the observed background fixed. It is not unconditional statistical power: noise counts, design-reference uncertainty and star correlations were not resampled. Every added event was assumed to exceed SNR 12 and to reach tier 1 already. Real raw-light completeness, depth distributions and astrophysical occurrence rates are absent. Full 50%/90% population-power inference remains incomplete. A null result cannot be described as excluding a particular excess merely because one hypothetical count table would cross a significance threshold. The new simulation does not establish an exclusion either.

**NOT TESTED: S2 star-clustered intervals.** The four supplied files give totals, not the joint per-star recovered exposure and flip count including zero-event stars. A filename search in research/astra and research/stage3 for cluster/bootstrap/S2/per-star inputs found no suitable R1 table (only an unrelated Q6 S2 evidence filename). No hold-out event files were opened. The reported rates 6/1152 and 13/2381 are arithmetically usable, but many different allocations across stars share these totals and yield different bootstrap intervals. The quoted Poisson intervals cannot be replaced honestly from these aggregates. A safe input is an anonymous frequency table of (recovered star-sector exposure, tier-1 flip count), including eligible zero-event stars, produced by Claude. No identifiers need enter the report or repository.

**Interpretation, conditional on the test assumptions:** Stratification makes a fairer comparison of real/flip shares when the period mixtures differ. It tests for an excess beyond the design-star imbalance within those bins, not whether any planets exist. It can miss a population present similarly in both samples, signals removed by masking or rejected before tier 1, effects inside broad bins, and weak excesses. Event-level exchangeability between design and hold-out samples, within-bin comparability, and independence across correlated events are not established by this arithmetic reproduction. Thus the filed null is a defensible narrow statement of failure to reject this model, not proof of no planets or a calibrated exclusion limit.

**STOP SIGNS:** material movement of a planning number under the requested stratified planting calculation. Finish this part's report and start nothing based on it, as instructed. The clustered interval also lacks an authorized sufficient aggregate. No fenced light or event inspection was used to fill that gap.

**QUEUE PROPOSALS:** FIX: replace `power_note`'s unstratified threshold/exclusion wording with a clearly scoped, matching-rule sensitivity analysis. Acceptance check: reproduce the eight exact probabilities, compare the full rule under a specified stochastic background and signal model, report uncertainty and clustering assumptions, and avoid claiming exclusion without coverage evidence. BUILD: generate the anonymous S2 exposure/count frequency table for cluster resampling. These are proposals for Claude, not edits to the project queues.

**IDEAS:** no additional build beyond those two scoped proposals. **Questions for Ahmed:** none needed to understand this checkpoint; Claude should review the changed sensitivity interpretation before work proceeds.

**What I did not check:** population-power calibration; star-cluster intervals; SAP or union parity; Parts E, A, D, C, F, G; astrophysical literature or filter-ranking recommendations. Ranking G1, Petrova 1.1.0 and Census now would exceed the evidence gathered.

Next: Claude reviews the Part B sensitivity correction and missing cluster input before the audit resumes; review costs Claude time, no further Codex computation is required for this handoff.
Usage, Part B: predicted 12 five-hour points and 2 weekly, cap 4 weekly. Observed 67 to 73% five-hour and 15 to 16% weekly before commit, account-wide rounded. Whole continuation baseline 60% / 14%, final observed 73% / 16%. Static whitespace check passed; runtime arithmetic and simulation checks are described above. These are producer checks of the new audit script, not a separate review of that script.

## Part B review continuation, run mode

Model/effort not independently exposed; requested Astra High. CONFIRMED: `002_cluster.py` checks both anonymous input tables against filed totals, then resamples whole stars 100,000 times (fixed seed 2026111301), preserving each star's exposure/count pair. The estimator is total flips divided by total recovered star-sectors, times 1,000; percentile endpoints are 2.5% and 97.5%.

| Campaign | Eligible stars | Flips / exposure | Rate per 1,000 | Filed Poisson 95% | Star-bootstrap percentile 95% |
|---|---:|---:|---:|---:|---:|
| G3 | 311 | 6 / 1152 | 5.2083 | 1.91 to 11.34 | 0.8897 to 10.5634 |
| G2 | 446 | 13 / 2381 | 5.4599 | 2.91 to 9.34 | 2.4116 to 9.2296 |

Only five G3 stars and eleven G2 stars have positive flip counts. Zero-event bootstrap replicates comprise 0.614% and 0.001%, respectively. The clustered intervals are not necessarily wider than the Poisson intervals; the estimators, conditioning and interval constructions differ. The word 'floor' should not be interpreted as a mathematical bound on every alternative interval. These percentile intervals account for within-star clustering empirically but their repeated-sampling 95% coverage is NOT TESTED, particularly with so few positive clusters. They condition on stars with recovered exposure, not all catalogue stars. No unseen event or light file was opened. Input provenance is Claude's anonymous table construction, not independently reconstructed from fenced events.

Run: approved venv Python with `-I -B research/astra/scripts/002_cluster.py`. Output: `data/astra/002/cluster.json`. Checks actually run: exact totals assertions and 100,000 cluster resamples per campaign. No separate coverage simulation or independent review of this new script was performed. This completes the requested empirical S2 interval calculation; unconditional S1 power remains explicitly untested as previously reported.

QUEUE PROPOSAL: clarify that the filed Poisson interval ignores clustering, rather than claiming all clustered interval constructions must be wider. STOP SIGNS: no active run-mode stop; changed numbers are reported and work continues. IDEAS: none new. Questions: none. Usage: 78% to 81% five-hour, 17% to 17% weekly, rounded account-wide before commit.

## Part E: gate coverage and design-only losses

**CONFIRMED, coverage reporting defect:** `pipeline/r1_gate.py:180` to 187 leaves the initial PASS unchanged when a bin has no after injections; zero after recovery also leaves PASS unchanged through the NaN branch. `002_gates.py` parsed all four filed R1 gate reports: four missing-bin/arm checks, all in G3 sealed (20 to 27.4 d and over 27.4 d, each in dips and bumps); zero undefined-ratio entries. The other three reports have zero missing injection bins. Thus both sealed G3 (a)/(b) labels pass only the evaluated bins, not all five. No development (a)/(b) verdict depended on missing bins, and no filed verdict depended on the zero-recovery NaN branch. A missing test is NOT a measured failure either. Proposed status: PASS ON TESTED BINS plus explicit coverage, or INCOMPLETE when all-bin coverage is required. Do not alter filed verdicts. Severity: medium, coverage interpretation. The branch behavior is static source evidence; file counts are executed evidence. No injected mutation of the frozen summary was run.

**CONFIRMED, gate scope:** `_run_group`, lines 116 to 117, chooses centers using already-prepared `a['t']`. Amendment 3 explicitly acknowledges this. Gate (a) tests whether adding a dip grows the mask near surviving light, not full-time retention. Its near-unity ratio can coexist with poor absolute recovery. A meaningful unconditional test chooses times over raw-sector time before masks and windows, includes gaps as a separately reported geometric loss, injects before preparation, and scores against identical zero-injection controls. Keep the current conditional comparison as a diagnostic, but add unconditional recovery by period, brightness, product and era. This is a test design, not a completed completeness measurement.

**CONFIRMED, gate (c) policy:** G2 development failed 14 to 20 d and over 27.4 d; G2 sealed additionally has 5 to 10 d OUTSIDE, as does G3 sealed. Amendment 3 paragraph 4 and section 5 authorize continuing the search while labelling failed bins not covered. That is faithful policy for exploration, not evidence of a calibrated false-positive control in those bins. The adjusted S1 test asks whether the imbalance exceeds the design reference; it does not restore real/flip symmetry. Do not reinterpret the filed NO EXCESS. The known/under-20 exceptions mean G3 development PASS provides limited coverage.

**CONFIRMED, metadata-only G3 design losses:** `002_gates.py` opens only group filenames on the design-seen target list, then reads metadata, not event values. 2,476 groups, 3,312 file records: 2,964 ok, 345 no safe windows, 3 too little data. No-safe-window fraction is 10.42% of files, compared with the separately FILED unseen total 439/1796 = 24.44%; no unseen metadata files were opened. Different populations mean this difference cannot establish a cause.

| Split | No safe windows / file records |
|---|---:|
| QLP | 345 / 2471 |
| SPOC | 0 / 125 |
| TESS-SPOC | 0 / 716 |
| Magnitude below 11 | 16 / 324 |
| Magnitude 11 to 12 | 52 / 551 |
| Magnitude 12 to 14 | 277 / 2437 |
| Sectors below 56 | 190 / 1857 |
| Sectors 56 to 93 | 103 / 1263 |
| Sectors 94 onward | 52 / 192 |
| Binary period 5 to 10 d | 152 / 1425 |
| Binary period 10 to 14 d | 95 / 1159 |
| Binary period 14 to 20 d | 70 / 552 |
| Binary period 20 to 27.4 d | 25 / 135 |
| Binary period above 27.4 d | 3 / 41 |

The sector table is [002-g3-sector-losses.md](002-g3-sector-losses.md): 105 sectors, 75 with skips; sector totals sum to 3312 and skip counts to 345. All listed products have no safe windows in 248/2476 groups, 10.02%. This is group availability loss, not a planet-completeness percentage: other sectors may still cover the star, products overlap, and observing durations differ. No exposure weighting or transit recovery was measured. These splits describe associations only, not causes or a license to change quality rules. Initial script used the wrong period-column name and reported unknown; corrected to p_bin_d and rerun before this report. No selection was changed based on results.

Run: approved venv Python `-I -B research/astra/scripts/002_gates.py`. Private full counts: data/astra/002/gates.json. QUEUE PROPOSALS: FIX explicit missing/undefined gate coverage; BUILD compare conservative QLP window alternatives on design data with raw injections and flip controls before changing any window rule. IDEAS: none beyond those tests. NOT TESTED: unseen per-sector/product losses, exposure-time loss, unconditional completeness, causal source of QLP skips. No new fence or replay stop. No questions for Ahmed. Part E complete at this scope; proceed to A.
Part E usage: predicted 5 five-hour points and 1 weekly; observed 81 to 89% and 17 to 18%, account-wide rounded. Run-mode speed stop now active at 89%; no later experiment launched. Next: resume Part A after the five-hour reset, then D, C, F, G under the remaining total budget; Codex is authorized to continue when resumed.

## Part A synthetic checkpoint

CONFIRMED: `002_mask_grid.py` ran 18 cases (periods 5,10,14,20,30,50 d; 1,2,4 sectors processed separately), 2-minute cadence, fixed noise seed, catalogue eclipses and fixed-position 8-hour injections. All 18 masks had zero changed cadences under full flux inversion. Across each period's three sector-count scenarios, 240/240, 480/480 and 960/960 injected cadences survived for both dip and bump on the same eclipsing baseline. This tests one injection location per sector, not unconditional completeness. Full counts including kept cadences are private in mask-grid.json. No real-light claim follows.

CONFIRMED: synthetic veto scenarios at periods 12.9,13,20 d preserve real/flip label symmetry. Single-sector events survive. At 13 and 20 d two same-phase sectors veto both events; adding two unrelated-phase event sectors changes the same pair to no veto. Adding a third matching phase restores veto for the matching three. `petrova_mask.py:232` counts other sectors WITH EVENTS in the arm, not all observed sectors, and lowers NMIN to one when fewer than three other event-bearing sectors exist. The module description states NMIN other sectors without that exception. Documentation mismatch CONFIRMED; scientific harm NOT TESTED. A denser event list can change the threshold without changing the original matching pair. Proposed FIX: document actual rule and test whether event-dependent availability is intended before any version change.

Static call-site check: stage2_search applies one preparation to both detection arms; recovered-light definition uses the union of old-mask removals on f and 2-f. The primary offset is nevertheless fitted to low real flux and is reused by the veto; complete end-to-end inversion invariance is not proven. No independent 0.8.1 source fixture/replay has yet been built; the requested three real-light off-switch comparisons remain NOT TESTED. This is a Part A checkpoint, not completion of that requirement. No frozen code was edited.
