**Partial: the orbit search is implemented and the full batch is running; no scientific pass or fail is available yet.**

# 028 Orbit-consistent search

Requested GPT-6-Astra high; runtime model/effort independently unverified. Branch astra/028-orbit-search, no git writes or commits. Tree nodes 1.1 and 1.3.

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

## Usage

Predicted 60 five-hour / 10 weekly points; meter unavailable. Actual and ratio cannot be measured from tool-call counts or elapsed time.

## Completed evidence at handoff

1. CONFIRMED, archived baseline recount: B P 48.10503091%, T156 reference R 34.20700630%, background 174 real / 79 upside-down; K2 all-planet P 45.83487382%, reference R 32.92115986%, background 158 / 63. Evidence: 028_inventory.py and data/astra/028/inventory.json. This is a recount of saved outcomes, not a new raw baseline scoring run. The refreshed inventory will additionally assert the possible-planet K2 result; that assertion was not observed at this handoff.
2. CONFIRMED, multiplicity inventory: all 1,098 reference planets have capture files; 474 have at least three scored crossing centres. Of 573 B misses, 143 have at least three. This is a necessary-condition ceiling on possible gains, not a soft-held classification. Per-bin totals and missing counts are in inventory.json. The old RS-037 summary joined only 1,075; this inventory uses the exact journal glob and trial membership of 027.
3. CONFIRMED, runtime synthetic geometry: eight checks, including independent forward coordinate roots, duration derivatives, translation invariance, two-event exclusion and duplicate exclusion. Deliberately bypassing orbit timing changes a synthetic null from zero to one accepted set. Evidence: 028_checks.py, checks.json. This does not substitute for the requested mutation on untouched design light, which is queued.
4. CONFIRMED, file guard: twelve private source-copy hashes checked; three forbidden access events rejected; allowed write and copied mask self-test passed. Byte identity is not semantic correctness. All copies and machine outputs are under data/astra/028; frozen files untouched.
5. CONFIRMED, small real-light preflight: first two design sectors in each campaign, six product groups, eight candidates, all eight below SNR 7; lower-threshold generation and null scorer completed. Evidence: 028_preflight.py and preflight.json. High-threshold candidate equality was asserted but is uninformative in this sample because it contains no high-threshold candidates. The separate 25-sector-per-campaign raw identity check is part of the full batch and has not yet been observed. Static syntax parsing passed for sixteen new Python scripts; static parsing does not establish runtime correctness of unexercised branches.

## Running batch and resumption

Launched 2026-11-17 17:55:11 Kuwait, clock read with Get-Date. Supervisor PID 2332. Estimate only: 2026-11-17 23:55:11 Kuwait. Three existing Python processes were present before launch; the batch uses at most three compute workers, each with NUMBA_NUM_THREADS=2. Its supervisor only coordinates workers and prints a heartbeat every five minutes.

Command: `D:/second-sun/.venv/Scripts/python.exe -I -B research/astra/scripts/028_run.py all` from the worktree. Do not launch a duplicate while this supervisor is alive. Checkpoints, source fingerprints, private logs and progress.json are under data/astra/028. After a failed or interrupted terminal state, the same command resumes completed work and refuses changed source fingerprints. No package installation or external write was performed.

Execution order: raw orbit-off identity, complete SNR-4 untouched candidate bank, full null orbit search on both arms/campaigns and mutation, freeze the floor, raw planet injections and orbit scoring, T156 injections and scoring, bootstrap summary, terminal verification, report rendering. The report renderer replaces this checkpoint only after verification. A passing initial variant stops with `needs_fresh_seed`; fresh-seed replay is not yet implemented. An insensitive real-null mutation stops with `needs_null_mutation_review`. Neither state is full completion.

The engineering point: trying more orbits gives noise more chances to look convincing. Calibration therefore uses the best score over the entire declared blind search, not scores at the known planted times. Selecting the floor above the same null sample's maximum guarantees zero additions on that sample; it does not establish the future false-alarm rate.

## What I did NOT check

NOT TESTED at this handoff: complete null calibration; real-null mutation sensitivity; full injected planet and T156 orbit results; confidence intervals for the new configurations; rules (a) to (e); final background additions and their dump/eclipse screens; terminal full-bank coverage; fresh seed. No fresh scientific result is inferred from process launch or elapsed time. No M2 low-threshold replay, eccentric or inclined orbits, secondary transits, different mass ratios, periods outside 4 to 8 binary periods, candidates below SNR 4, independent null-validation set, G1 or sealed data.

## STOP SIGNS hit

The brief's foreground requirement conflicts with AGENTS.md section 4 rule 10, "Long runs go in the background with a log file", and section 7, "Never poll a long run". The brief explicitly says AGENTS wins. I followed the permitted background-and-end-turn route; no healthy full-batch logs or progress have been polled. This leaves the task PARTIAL. The full-chain runtime paths beyond the preflight remain unverified, so a failed supervisor must be diagnosed before its checkpoints are treated as results.

## QUEUE PROPOSALS

None yet. Nodes 1.1 and 1.3 await the experiment's verified result. Do not infer an adoption proposal from this implementation.

## IDEAS

None beyond the requested experiment.

## Disagreements with Claude

None. The saved planted-time scores cannot be used as a blind-search null; the new raw replay addresses that limitation.

## Questions for Ahmed

None. This headless run needs no human decision at this stage.

Next: Claude reviews the terminal report and verification after the batch finishes, to assess the measured result; review usage is unmeasured and requires Claude.
