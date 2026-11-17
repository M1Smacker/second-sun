**Fails: 0 of 4 orbit configurations passes all five rules.**

# 028 Orbit-consistent search

Requested GPT-6-Astra high; runtime model/effort independently unverified. Branch astra/028-orbit-search. No commits or git writes. Tree nodes 1.1 and 1.3.

## Pass rule recorded BEFORE scoring

All five conditions must hold for each orbit configuration against its own B or K2 base: (a) P on 968 possible planets gains at least 1.0 percentage point and the paired 95% interval is wholly above zero; (b) upside-down background does not exceed that base and real background is at most 174; (c) dip-minus-bump 99% whole-star intervals include zero in every binary-period bin, on both planet populations; (d) T156 reference R does not fall below its base; (e) new real minus 2.3 times new upside-down is at most 5 against that base. Also report K2 against B separately; it is not automatically a freeze recommendation.

Population weighting: five binary-period bins with edges 5, 10, 14, 20, 27.4 days, equal weights. 10,000 whole-star bootstrap draws, seed 2026111523, paired differences. Same fixed 1,098 observed planets and 968 physically possible subset as 027, and 222 reference T156 injections from 2,000 trials. Pre-existing crossing exclusions remain the historical definitions for B/K2. Novel orbit hits must also be absent at the matching crossing in the untouched orbit search. No planted time enters template generation.

## Design recorded BEFORE scoring

Candidate bank: raw loaded flux, injections before windows, eclipse mask and detrending; frozen B processing copied into the 028 harness. Search each arm at candidate SNR 4, same box grid, greedy non-overlap merge and primary-product selection as the original detector. Scores below 4 are excluded: this is an explicit computational restriction, not a complete coherent flux search. Preserve archived B and K2 results separately so adding weak candidates cannot change their baseline holds.

Geometry: circular coplanar edge-on central primary crossings. Binary period and primary epoch come from the design catalogue, with the same first-row convention as 006; secondary mass fraction mu=1/3 is fixed from the bench model, not estimated from results. Let rho=mu*(Pb/P)^(2/3). At a crossing t, sin(2*pi*(t-E)/P)=rho*sin(2*pi*(t-Tb)/Pb), on the inferior-conjunction branch. Therefore corrected time u(t,P)=t-P/(2*pi)*asin(rho*sin(2*pi*(t-Tb)/Pb)) equals E+n*P. The maximum timing displacement is P/(2*pi)*asin(rho), derived from the projected stellar excursion. No free timing jitter independently assigned to crossings.

Period range: P from 4*Pb to 8*Pb, inclusive, a restricted search matching the reference population, not all possible planets. For circular binaries the Holman-Wiegert empirical boundary at mu=1/3 is acrit/ab=1.60+4.12*mu-5.09*mu^2, converted to period ratio by power 3/2, which is below 4. This is not a stability certification for eccentric binaries. Source: [Holman and Wiegert](https://arxiv.org/html/astro-ph/9809315v1), empirical coplanar test-particle integrations; [STANLEY](https://arxiv.org/html/2101.03186v1), sections II.4 and IV.2.3, motivates transverse-velocity durations and calls 4*Pb an approximate stability limit.

Generate trial periods from every candidate pair and every integer cycle separation compatible with that period range; solve u(t2,P)-u(t1,P)=k*P. Check all candidates against each resulting common epoch. A crossing matches when its corrected-time residual is no greater than 0.1 day (the existing detector's merge padding), and there must be at least three distinct orbital cycles. This pair-anchored finite template search is not an exhaustive continuum grid. Search all its templates on null and injected light identically. Duplicate products/times cannot provide extra crossings. Approximate durations satisfy d_i*abs(vp-vstar) within a factor of two across members, using the same orbit; near-zero relative velocities are excluded.

Soft eligibility: honor depth cap for all new orbit members, including B. Only dump, gap edge, ramp and dominated may be overridden. Step, common/burst, flip match, c5, eclipse overlap, repeater, orbit lock, p1 veto, too-deep, flare, known spacecraft event and failed second-product check remain hard holds. A promotes eligible SNR>=7 members. B adds eligible lower-threshold members of a qualifying stack. Neither removes existing base detections. Score=sum(min(SNR,7))/sqrt(n), preventing one huge systematic from dominating a set. Duration-compatible subsets and unique-cycle alternatives are part of the trial search; calibration uses the best score over all trials.

Null calibration: before any injected orbit scoring, take the maximum best-stack score over untouched design hosts, both arms and campaigns, then use max(7, maximum+1) as the common floor for A and A+B, B and K2. This conservative empirical threshold is chosen only from null data. The resulting same-sample alarm count is training calibration, not independent false-alarm validation. Preserve the pre-floor set counts and per-star best scores privately. Mutation: disable the common-orbit timing requirement, retain multiplicity/duration restrictions, and require a changed null set count (otherwise record an insensitive mutation check).

Optional M2: skipped if the new SNR-4 candidate bank would require a second complete mask replay; existing SNR-7 mask replays alone do not price weak stacks. Fresh-seed confirmation is conditional on passing all five rules.


## Findings, CONFIRMED as computed

This is producer verification, not independent review. Bootstrap intervals quantify host sampling variability within this restricted experiment. The score is an empirically calibrated ranking statistic, not a Gaussian significance.

| Configuration | P all 1,098 %, 95% | P possible 968 %, 95% | T156 R %, 95% | Real / upside-down |
|---|---:|---:|---:|---:|
| B | 48.105 [43.91, 52.15] | 48.404 [43.89, 52.74] | 34.207 [27.03, 40.75] | 174 / 79 |
| K2 | 45.835 [41.35, 50.18] | 51.018 [46.36, 55.40] | 32.921 [25.60, 39.71] | 158 / 63 |
| B+A | 48.105 [43.91, 52.15] | 48.404 [43.89, 52.74] | 34.207 [27.03, 40.75] | 174 / 79 |
| B+A+B | 48.105 [43.91, 52.15] | 48.404 [43.89, 52.74] | 34.207 [27.03, 40.75] | 174 / 79 |
| K2+A | 45.835 [41.35, 50.18] | 51.018 [46.36, 55.40] | 32.921 [25.60, 39.71] | 158 / 63 |
| K2+A+B | 45.835 [41.35, 50.18] | 51.018 [46.36, 55.40] | 32.921 [25.60, 39.71] | 158 / 63 |

| Population | Configuration | Paired gain vs matching base, points (95%) |
|---|---|---:|
| fixed1098 | B+A | +0.000 [+0.000, +0.000] |
| fixed1098 | B+A+B | +0.000 [+0.000, +0.000] |
| fixed1098 | K2+A | +0.000 [+0.000, +0.000] |
| fixed1098 | K2+A+B | +0.000 [+0.000, +0.000] |
| possible968 | B+A | +0.000 [+0.000, +0.000] |
| possible968 | B+A+B | +0.000 [+0.000, +0.000] |
| possible968 | K2+A | +0.000 [+0.000, +0.000] |
| possible968 | K2+A+B | +0.000 [+0.000, +0.000] |
| T156reference | B+A | +0.000 [+0.000, +0.000] |
| T156reference | B+A+B | +0.000 [+0.000, +0.000] |
| T156reference | K2+A | +0.000 [+0.000, +0.000] |
| T156reference | K2+A+B | +0.000 [+0.000, +0.000] |

## Null calibration

Both campaigns and arms: 1408 host-arms, 20118 pair-anchored templates, 152 distinct sets before the floor. Best null score 13.760762; floor 14.760762. Zero sets above the floor. The floor was written to calibration.json before injected orbit scoring. Missing-epoch host-arms excluded from orbit fits: 2.

Mutation removing orbit timing: 152 to 3296 sets. Sensitive: True. Synthetic independent forward-root test also rejected two-event sets and duplicate crossings.

Same-sample background adds zero A or B events by construction. This is training calibration, not independent evidence of zero future false alarms. There are zero new real events requiring dump or eclipse blind-spot checks against either matching base. Background splits by brightness, product and era are saved in summary.json; all additions in each split are zero.

| Campaign | Arm | Bin | Hosts | Hosts with sets | Sets before floor | Sets per host |
|---|---|---:|---:|---:|---:|---:|
| g2 | real | 1 | 146 | 5 | 94 | 0.6438 |
| g2 | real | 2 | 88 | 1 | 2 | 0.0227 |
| g2 | real | 3 | 97 | 1 | 3 | 0.0309 |
| g2 | real | 4 | 42 | 0 | 0 | 0.0000 |
| g2 | real | 5 | 47 | 1 | 2 | 0.0426 |
| g2 | flip | 1 | 146 | 3 | 18 | 0.1233 |
| g2 | flip | 2 | 88 | 2 | 16 | 0.1818 |
| g2 | flip | 3 | 97 | 0 | 0 | 0.0000 |
| g2 | flip | 4 | 42 | 0 | 0 | 0.0000 |
| g2 | flip | 5 | 47 | 1 | 3 | 0.0638 |
| g3 | real | 1 | 119 | 0 | 0 | 0.0000 |
| g3 | real | 2 | 88 | 1 | 10 | 0.1136 |
| g3 | real | 3 | 54 | 0 | 0 | 0.0000 |
| g3 | real | 4 | 19 | 0 | 0 | 0.0000 |
| g3 | real | 5 | 4 | 0 | 0 | 0.0000 |
| g3 | flip | 1 | 119 | 2 | 3 | 0.0252 |
| g3 | flip | 2 | 88 | 1 | 1 | 0.0114 |
| g3 | flip | 3 | 54 | 0 | 0 | 0.0000 |
| g3 | flip | 4 | 19 | 0 | 0 | 0.0000 |
| g3 | flip | 5 | 4 | 0 | 0 | 0.0000 |

## Rules against the matching base

| Configuration | a: possible gain, 95% points | b: real / upside-down | c: both-population controls | d: R vs base % | e: new-real excess | Verdict |
|---|---|---|---|---|---|---|
| B+A | +0.000 [+0.000, +0.000], False | 174 / 79, True | True | 34.207 vs 34.207, True | 0.0, True | FAIL |
| B+A+B | +0.000 [+0.000, +0.000], False | 174 / 79, True | True | 34.207 vs 34.207, True | 0.0, True | FAIL |
| K2+A | +0.000 [+0.000, +0.000], False | 158 / 63, True | True | 32.921 vs 32.921, True | 0.0, True | FAIL |
| K2+A+B | +0.000 [+0.000, +0.000], False | 158 / 63, True | True | 32.921 vs 32.921, True | 0.0, True | FAIL |

## Paired changes, counts and controls

| Population | Configuration | Bin | n | Dip gained / lost | Bump gained / lost | Dip-minus-bump 99%, points |
|---|---|---:|---:|---:|---:|---|
| fixed1098 | B+A | 1 | 242 | 0 / 0 | 0 / 0 | [-4.206, 5.530] |
| fixed1098 | B+A | 2 | 229 | 0 / 0 | 1 / 0 | [-4.098, 4.464] |
| fixed1098 | B+A | 3 | 221 | 0 / 0 | 0 / 0 | [-7.917, 3.861] |
| fixed1098 | B+A | 4 | 187 | 0 / 0 | 0 / 0 | [-1.724, 14.943] |
| fixed1098 | B+A | 5 | 219 | 0 / 0 | 0 / 0 | [-3.141, 5.051] |
| fixed1098 | B+A+B | 1 | 242 | 0 / 0 | 0 / 0 | [-4.206, 5.530] |
| fixed1098 | B+A+B | 2 | 229 | 0 / 0 | 1 / 0 | [-4.098, 4.464] |
| fixed1098 | B+A+B | 3 | 221 | 0 / 0 | 0 / 0 | [-7.917, 3.861] |
| fixed1098 | B+A+B | 4 | 187 | 0 / 0 | 0 / 0 | [-1.724, 14.943] |
| fixed1098 | B+A+B | 5 | 219 | 0 / 0 | 0 / 0 | [-3.141, 5.051] |
| fixed1098 | K2+A | 1 | 242 | 0 / 0 | 0 / 0 | [-5.286, 3.434] |
| fixed1098 | K2+A | 2 | 229 | 0 / 0 | 1 / 0 | [-1.527, 7.595] |
| fixed1098 | K2+A | 3 | 221 | 0 / 0 | 0 / 0 | [-7.692, 4.546] |
| fixed1098 | K2+A | 4 | 187 | 0 / 0 | 0 / 0 | [-0.578, 13.846] |
| fixed1098 | K2+A | 5 | 219 | 0 / 0 | 0 / 0 | [-2.484, 7.054] |
| fixed1098 | K2+A+B | 1 | 242 | 0 / 0 | 0 / 0 | [-5.286, 3.434] |
| fixed1098 | K2+A+B | 2 | 229 | 0 / 0 | 1 / 0 | [-1.527, 7.595] |
| fixed1098 | K2+A+B | 3 | 221 | 0 / 0 | 0 / 0 | [-7.692, 4.546] |
| fixed1098 | K2+A+B | 4 | 187 | 0 / 0 | 0 / 0 | [-0.578, 13.846] |
| fixed1098 | K2+A+B | 5 | 219 | 0 / 0 | 0 / 0 | [-2.484, 7.054] |
| possible968 | B+A | 1 | 210 | 0 / 0 | 0 / 0 | [-4.878, 5.505] |
| possible968 | B+A | 2 | 198 | 0 / 0 | 1 / 0 | [-3.871, 5.381] |
| possible968 | B+A | 3 | 202 | 0 / 0 | 0 / 0 | [-7.853, 4.348] |
| possible968 | B+A | 4 | 167 | 0 / 0 | 0 / 0 | [-3.521, 13.131] |
| possible968 | B+A | 5 | 191 | 0 / 0 | 0 / 0 | [-2.791, 6.111] |
| possible968 | B+A+B | 1 | 210 | 0 / 0 | 0 / 0 | [-4.878, 5.505] |
| possible968 | B+A+B | 2 | 198 | 0 / 0 | 1 / 0 | [-3.871, 5.381] |
| possible968 | B+A+B | 3 | 202 | 0 / 0 | 0 / 0 | [-7.853, 4.348] |
| possible968 | B+A+B | 4 | 167 | 0 / 0 | 0 / 0 | [-3.521, 13.131] |
| possible968 | B+A+B | 5 | 191 | 0 / 0 | 0 / 0 | [-2.791, 6.111] |
| possible968 | K2+A | 1 | 210 | 0 / 0 | 0 / 0 | [-6.135, 3.830] |
| possible968 | K2+A | 2 | 198 | 0 / 0 | 1 / 0 | [-2.186, 6.915] |
| possible968 | K2+A | 3 | 202 | 0 / 0 | 0 / 0 | [-8.411, 4.762] |
| possible968 | K2+A | 4 | 167 | 0 / 0 | 0 / 0 | [-1.639, 13.971] |
| possible968 | K2+A | 5 | 191 | 0 / 0 | 0 / 0 | [-3.087, 7.870] |
| possible968 | K2+A+B | 1 | 210 | 0 / 0 | 0 / 0 | [-6.135, 3.830] |
| possible968 | K2+A+B | 2 | 198 | 0 / 0 | 1 / 0 | [-2.186, 6.915] |
| possible968 | K2+A+B | 3 | 202 | 0 / 0 | 0 / 0 | [-8.411, 4.762] |
| possible968 | K2+A+B | 4 | 167 | 0 / 0 | 0 / 0 | [-1.639, 13.971] |
| possible968 | K2+A+B | 5 | 191 | 0 / 0 | 0 / 0 | [-3.087, 7.870] |

## Multiplicity and limitations

Capture inventory joins all 1098 observed planets. 474 have at least three scored crossings at their own template times. Among B misses, 143 of 573 do. This is a necessary multiplicity ceiling, not proof they are soft-held or orbit-search eligible.

Restricting further to detected but unrecovered planets: B has 49 with three scored crossings out of 165; K2 has 64 out of 190. This includes novelty exclusions, so it is not an exact count of soft-held planets.

## What I did NOT check

Eccentric or mutually inclined orbits, secondary-star transits, true stellar mass ratios, N-body dynamics, periods outside 4 to 8 binary periods, candidates below SNR 4, continuum completeness between pair-anchored templates, independent null validation, pixel-level evidence or G1. M2 was skipped because its SNR-7 replays do not supply the lower-threshold candidate bank. No frozen filter was changed.

Fresh-seed confirmation was not triggered because no variant passed all five rules.

## Verification

Terminal runtime verification: {"background_groups": 14835, "baseline_trial_identity": 3098, "completed_workers": 20, "independent_rates": 24, "static_parse": 16}. The historical B and K2 baseline outcomes are copied by identity and independently recounted, not a new from-scratch baseline fit. Raw zero-injection identity is checked on 25 design sectors in each campaign. Hashes establish source byte identity only.

## STOP SIGNS hit

No scientific fence breach identified. The foreground request conflicts with the explicit AGENTS background/no-polling rule; the latter was followed. Runtime results are usable only after terminal verification, never from checkpoints.

## QUEUE PROPOSALS

Tree nodes 1.1 and 1.3: Claude should review this restricted-orbit experiment and its same-sample calibration before any adoption. No production change proposed by this report.

## IDEAS

None beyond the requested experiment.

## Disagreements with Claude

None. A failed restricted search does not reject orbit searches in general.

## Questions for Ahmed

None.

## Usage

Predicted 60 five-hour / 10 weekly points. Actual meter unavailable in the headless runner, so actual/predicted ratio is unavailable. Lesson: candidate-score coverage must be audited before promising reuse of an injected-time cache.

Next: Claude reviews the report and private verification output before deciding whether this experiment warrants more work; review usage is unmeasured.
