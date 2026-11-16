**Found something: M4 fails its acceptance rule. None of the three M4 configurations passes. Keep the existing mask for class B; do not adopt this M4.**

# 026 FIX 101 / FIX 94, completed bench

Requested model: GPT-6-Astra high. Runtime model and effort independently unverified in this headless session.
Report rendered 2026-11-16 19:47 Kuwait. Branch astra/026c-fix101-m4-bench, unchanged throughout this continuation. Tree node 1.2.

No git writes, commit, branch switch, push, frozen-source edit or quality-bit-4096 trial. The existing runner lock was preserved. Code and report files remain for the runner to commit.

## Plain result

CONFIRMED as computed on the fixed design-star bench. B+M4 reduces P from 48.105% to 42.509%, a loss of 5.596 percentage points (paired 95% interval -8.552 to -2.830). On the same 968 possible planets used by F1, it reduces P from 48.404% to 44.003%, a loss of 4.401 points (-7.424 to -1.648). T156 reference R falls from 34.207% to 31.915%. Upside-down background rises from 79 to 80. These independently fail the prewritten acceptance gates, regardless of the control results.

A narrower mask can preserve light while a later hold still removes its eligibility for tier 1. M4 applies that hold to the whole star on each arm. The bench measures the combined result. Equal event files on a class A sector alone do not prove that its final tiers survive a hold triggered in another sector.

## What was reused and what finished now

The current branch tip was 9eaca87d and had no 026 implementation files. The 22 saved scripts and report files were restored from d5f3b884 using read-only git show. Run 2's actual progress records show the main six-configuration bench completed at 15:14, contrary to the run-3 launch note. The real-host controls failed during preparation. Existing main outputs were reused after verification rather than regenerated.

This continuation fixed control input authorization: all of the selected design host's product files are registered before preparing any product, matching the main generator. The previous loop prepared one product before registering the own-SPOC file it could consult. The data-reader error called the product unsupported or possibly corrupt; no file was deleted or repaired. Control generation and scoring then completed in this session. Scientific rules, eligibility thresholds, host order and mask settings were unchanged.

## Star lists and trace

CONFIRMED. The permitted three drift witnesses from run 1 all reproduced windows larger than a quarter orbit. The revised brief explicitly accepts this evidence. The old trace-summary passed=false records the superseded requirement for all five named witnesses, two of which were fenced; it has not been rewritten into a new experiment.

| Campaign | Saved 010 list | Full-window quarter-orbit list | Drift-only list | Overlap with 010 | 010 only | Full-window only | Difference |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| G2 | 112 | 100 | 87 | 87 | 25 | 13 | 38 |
| G3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The corrected 010 selection reproduces all 112 G2 hosts and zero G3 hosts, with zero membership differences. These are actual stored-sector catalogue calculations, using a representative design-file FITS-header midpoint per sector. Full-window coverage includes both eclipse widths and uncertainty terms, with the historical overlap approximation. It is not a measured light-loss fraction.

The separate width-based M4 rule selects 143 G2 class B hosts, 45 outside the historical replay roster. G2 has 1,289 B sectors, 5,633 A sectors and 331 unclassifiable sectors. G3 has 2,476 A sectors and no B sectors under its available catalogue uncertainties. Missing finite width/epoch data stays unclassifiable and keeps frozen behavior. Evidence: 026_inventory.py, inventory-summary.json; historical trace-summary.json.

## Controls (a) to (d)

(a) PASS within the predeclared scope: 50 class A sectors on hosts without any class B sector reproduce every event exactly. Runtime producer verification passed. This does not establish final-tier identity on mixed A/B hosts.

Real-host controls selected 3 hosts after examining 7 sectors and produced 15 trials. Selection was fixed before outcomes: historical-M2 class B hosts, prepared best product, scatter at most 1,000 ppm, host cap at least 4,000 and below 20,000 ppm, 80% cadence coverage in the fixed boxes, first three distinct eligible hosts, at most 200 sectors examined. Injections enter raw loaded flux before masking, windows, detrending and vetting.

| Control case | Trials per arm | M2 real / upside-down recovered | M4 real / upside-down recovered | Extra M4 losses real / upside-down | M4 timing holds real / upside-down |
|---|---:|---:|---:|---:|---:|
| eclipse2 | 3 | 2 / 1 | 0 / 0 | 2 / 1 | 3 / 2 |
| eclipse5 | 3 | 1 / 1 | 0 / 0 | 1 / 1 | 2 / 2 |
| planet2 | 3 | 1 / 1 | 1 / 1 | 0 / 0 | 2 / 0 |
| planet3_regular | 3 | 1 / 1 | 0 / 0 | 1 / 1 | 3 / 2 |
| planet3_irregular | 3 | 2 / 1 | 1 / 1 | 1 / 0 | 2 / 0 |

(b) FAIL under the prewritten failing-first rule: each depth and arm needs at least one M2 tier-1 recovery, zero M4 recoveries and all three hosts marked by M4. M2 did admit planted eclipses at each depth on both arms, and M4 removed all those recoveries. The stricter marking requirement fails: one upside-down 2% case and one case per arm at 5% lack the timing hold. Zero final recoveries alone does not prove that the new guard caught every injection.

(c) FAIL: two-crossing and regular-three-crossing trials together are six per arm. One extra regular-triple loss on each arm is 16.667 percentage points in this small control, above the 0.5-point allowance. The two-crossing case loses no additional recoveries. Irregular triples are diagnostic only. Counts are paired recoveries, not the number of detected boxes.

CONFIRMED, reused synthetic falsification: M2 left both shifted 2% and 5% eclipses available, and M4 held them on both arms. Two planet crossings and an irregular triple survived the timing guard; a regular triple was held on both arms. All planted crossings were detected. Seven synthetic assertions passed, including a disabled-guard mutation. This narrower detector-level test does not substitute for full tier-1 acceptance on real hosts.

| Configuration | New class B real | New class B upside-down | Allowed real (2.3 x upside-down + 5) | Control (d) |
|---|---:|---:|---:|---|
| B+M2 | 36 | 4 | 14.2 | FAIL |
| B+M4 | 12 | 3 | 11.9 | FAIL |
| B+C96+DS+M4 | 17 | 4 | 14.2 | FAIL |
| cap+R2+M4 | 20 | 4 | 14.2 | FAIL |

New means unmatched to B on the same campaign, host, sector and arm, within the existing centre/duration matching tolerance. It counts additions, not net background change. Evidence: 026_control_generate.py, 026_control_run.py, real-controls-summary.json and 026_summary.py.

## Six configurations

P and R give equal weight to the five fixed binary-period bins. Square brackets are 95% whole-star bootstrap intervals, 10,000 draws with seed 2026111523. Paired change uses the same resampled stars for each configuration and B. Fixed P uses 1,098 trials; possible P retains F1's exact 968-trial membership, even after adding fallback radii. R uses the original 222 Saturn-like trials from the 2,000-trial T156 bench.

| Configuration | Fixed P % [95%] | Change from B [95%], points | Possible P % [95%] | Change from B [95%], points |
|---|---|---|---|---|
| B | 48.105 [43.915, 52.151] | 0.000 [0.000, 0.000] | 48.404 [43.894, 52.738] | 0.000 [0.000, 0.000] |
| B+M2 | 49.474 [45.345, 53.491] | 1.369 [0.561, 2.340] | 49.855 [45.446, 54.040] | 1.451 [0.558, 2.534] |
| B+M4 | 42.509 [38.200, 46.893] | -5.596 [-8.552, -2.830] | 44.003 [39.328, 48.610] | -4.401 [-7.424, -1.648] |
| B+C96fallback | 43.163 [38.809, 47.481] | -4.942 [-7.217, -3.008] | 47.995 [43.435, 52.345] | -0.409 [-1.211, 0.000] |
| B+C96+DS+M4 | 40.602 [36.096, 45.091] | -7.503 [-10.935, -4.236] | 45.191 [40.421, 49.960] | -3.214 [-6.400, -0.200] |
| cap+R2+M4 | 41.239 [36.665, 45.807] | -6.866 [-10.380, -3.525] | 45.916 [41.079, 50.748] | -2.488 [-5.772, 0.609] |

| Configuration | T156 R % [95%] | Real background | Upside-down background |
|---|---|---:|---:|
| B | 34.207 [27.034, 40.754] | 174 | 79 |
| B+M2 | 34.633 [27.520, 41.214] | 203 | 83 |
| B+M4 | 31.915 [24.432, 38.747] | 144 | 80 |
| B+C96fallback | 32.061 [24.725, 38.738] | 117 | 53 |
| B+C96+DS+M4 | 31.064 [23.476, 37.898] | 111 | 59 |
| cap+R2+M4 | 31.064 [23.476, 37.898] | 123 | 66 |

Full period-bin counts, both-arm rates and intervals for both P populations and T156 are in [026-tables.md](026-tables.md). B+M2 reuses 010/011 raw replays, rescored under adopted B; M1 was not rerun. Fresh generation fills missing M4 class B coverage and the 50 class A identities.

## Fallback radius alone

CONFIRMED. Of 47 design hosts lacking a header radius, five receive a radius from the four existing sources; 42 still lack one. The smallest positive finite radius is the most generous depth cap. No new radius was fetched, and existing known radii were not replaced. B+C96fallback is C96 with that missing-radius fallback, without M4 or DS.

Against saved 023 C96 without fallback, the fallback loses three additional recovered planets on each arm and gains none. Fixed P changes from 43.437% to 43.163%; possible P from F1's 48.31% to 47.995%. Real background falls from 124 to 117; upside-down stays 53. This is a measured tradeoff, not an adoption decision. Evidence: fallback-radii.json, 026_recount.py and recount-m4.json.

## Acceptance and safe fallback

CONFIRMED. B+M4, B+C96+DS+M4 and cap+R2+M4 all miss the required positive gain on both populations and reduce T156 reference R. B+M4 also exceeds the upside-down limit by one. All three fail control (d), including B+M4 with 12 new real events against a limit of 11.9. No M4 configuration qualifies. No threshold, denominator, period tolerance or star selection was tuned after these results.

The safe answer is to leave class B under the existing frozen mask, including its blanking losses. The foregone mask-only gain is about 1.4 percentage points: reused B+M2 gives +1.369 points on the fixed bench and +1.451 on the possible population. F1's cap-adjusted M2 estimate was +1.36 points. These are comparisons with the historical M2 roster, not a fresh cost measurement of deliberately blanking every new M4-class-B sector. Rejecting M4 does not authorize the unguarded M2, which also fails background/control gates.

## Checks actually performed

- Runtime: 1,098 baseline planet identities; 2,000 T156 baseline identities; 50 complete class A sector event identities; exact 010 roster reconciliation; 180 independent bin recounts including the 968 membership; six configuration scores on both campaigns and arms; real-host raw controls and the reused synthetic controls.
- 026_recount.py uses saved trial outcomes and independent counting logic without pipeline imports. It checks aggregation and fixed populations; it does not independently validate the original detector or vetting implementation.
- Producer checks reject an arithmetic count mutation and the synthetic disabled-guard mutation. These are targeted checks, not independent review or proof against every possible defect.
- Frozen pipeline files remain untouched. Copied-source hashes record provenance only; they do not prove scientific correctness. Final static checks are recorded in the worklog and validation-final.json.

## What I did NOT check

No fresh-seed population, known-planet replay, production exporter/freeze, new radius download or exhaustive session-log fence review. No brightness/product/era recovery sensitivity estimates were produced; period-bin and campaign event counts are available. No G1 or held-out target light was inspected. The harness retains the frozen shared machine-reference selection permitted by AGENTS section 4.2; those references were not summarized by star. Main generation/scoring was reused from run 2 and verified from saved evidence, not rerun in this continuation. The reader error's corruption suggestion was not tested as a physical file defect. Statistical intervals describe this fixed development population.

## STOP SIGNS hit

The regular-three-crossing synthetic failure and large measured recovery loss are retained as rejection evidence. No alternative M4 was designed. The predeclared interpretation resolves an underspecified strict period as a consecutive-cycle triple with a one-hour midpoint tolerance; arbitrary skipped-cycle fits were not added. Class A sector identity conflicts with a star-wide hold on mixed A/B hosts; the 50-sector control excludes mixed hosts, as fixed in run 2. These limitations prevent treating this prototype as an exact production specification.

The continuation made one process-query attempt with Get-CimInstance, which the sandbox denied. Its subsequent no-process text was not treated as evidence. One 60-second terminal wait elapsed without opening healthy-run logs. The original control launch result was not retained by the tool wrapper; completion was established through terminal progress and output verification. No process was killed, and no permission escalation was attempted.

## QUEUE PROPOSALS

Node 1.2, existing FIX 101 / FIX 94: record M4 rejected, the 45 additional class B hosts, the whole-star-hold planet loss, and the class A/mixed-host specification conflict. Preserve the existing mask until a separately specified design passes its controls. Claude files this; the queues were not edited.

## IDEAS

No replacement rule built. A future design would need to distinguish planet triples from residual eclipses before any new bench; cost and scientific specification remain unestimated, so this is not an authorized follow-up run.

## Disagreements with Claude

The launch note said no full outputs completed; saved terminal records and the successful recount establish that the main bench did complete. The proposed M4 fails the tests above. No technical decision or production setting was silently overridden.

## Questions for Ahmed

None. The rejected configuration can be handed back without a new decision.

## Usage

Continuation prediction: 40 five-hour / 6 weekly points; brief cap 60 five-hour points. Actual meter and model/effort unavailable in this headless session. No numeric actual or cap-compliance claim. Lesson: inspect terminal artifacts before rerunning a bench, and distinguish restored light from final planet eligibility.

## Rules fixed before computing

Historical run-2 plan follows unchanged. Its initial sector-median wording was clarified to representative FITS-header midpoint before the new computation, as recorded in 026-worklog.md. That implementation convention and the identity-sample restriction remain explicit limitations.
Reuse run 1's three permitted drift witnesses and its catalogue comparison. The revised brief explicitly permits this. Compare saved 010 membership against actual sector classification as well as the fixed-epoch counts. No fenced light may be opened.

M4 class A: retain the frozen mask exactly when the sector-median drift term is at most one primary catalogue width. Class B: use the historical M2 mask, refit-centred and width-capped; preserve the repeat lane. Missing finite catalogue width keeps frozen behavior and is counted separately. Class B cannot deliberately be blanked by an uncapped uncertainty term; genuine eclipse/repeat masks may still leave too little data.

On each arm separately, use SNR >= 7 primary leftover events across all sectors of a class B host. Hold all its events at tier 2, retain them with timing_unverified, if an event exceeds the host cap or a triple has max depth <= 1.3 times min depth and fits a strict period. Deduplicate overlapping detections before counting crossings. Two crossings alone never trigger the periodic rule. Numerical strict-period interpretation: consecutive cycles, middle event within one hour of the midpoint of the first and third. This adopts the existing repeater's one-hour tolerance without searching arbitrarily short alias periods. It is a conservative operational interpretation, not a uniquely specified rule in F1. Class A identity applies to hosts without a class B trigger elsewhere; the requested sector-only and star-wide rules otherwise conflict, which must be disclosed.

C96 fallback applies only when the existing header radius is unavailable: smallest finite positive radius among the four already checked sources, maximizing the allowed depth. Keep .2009 solar radii for twice Jupiter's radius, matching 023. No new cap margin or quality-bit policy.

Controls: (a) zero changed events on 50 class A star-sectors; (b) shifted raw 2% and 5% eclipses, M2 must fail first and M4 hold; (c) raw two- and three-crossing equal-depth planets, additional M4 cost <= 0.5 percentage point; (d) new class B real events <= 2.3 times new upside-down events + 5. Periodic and irregular three-crossing cases are kept distinct. Synthetic controls may falsify the rule but do not substitute for the requested real-host controls.

Acceptance requires all controls; P gain >= 0.5 point with paired whole-star 95% interval above zero on both fixed 1,098 and possible 968 populations; T156 R not down; untouched upside-down background <= 79. Real background reported. Required configurations: B, reused B+M2, B+M4, B+C96fallback, B+C96+DS+M4, cap+R2+M4. Preserve 023 denominators, equal period-bin weights and 10,000 whole-star bootstrap draws. No thresholds change after outcomes. On rejection, report the historical roughly 1.4-point cost of keeping class B blanked as an estimate, not a fresh measurement.

Predicted usage: 50 five-hour points / 8 weekly points, cap 60 five-hour points. Actual meter unavailable in headless runner. No helpers.

Next: Claude reviews the rejection and fence-checks the handoff for node 1.2; no additional Codex run is needed for this brief, and review usage is unmeasured.
