**0 GO candidates.** Highest P is B+DS at 49.9803%, 95% interval 45.70% to 54.11%. Every configuration misses the fixed 50% P rule.

# 023 candidate matrix

Codex, model and effort independently unverified in the headless runner. Report generated 2026-11-15 18:04 Kuwait. The brief names Astra in its weekend context, with no separate effort line. A model match is unverified.

**Branch** astra/023-candidate-matrix. Local worktree changes only. The runner handles the eventual commit. The report filename follows the current user instruction.

## Pass rule recorded before scoring

A configuration is a GO candidate only if ALL hold. (a) P at least 0.50 and lower bound at least 0.40. (b) Upside-down background at most 79. (c) The paired control passes in every bin. (d) Real background at most 174. (e) New real events in the dump excess window or at eclipse leftovers number at most 5. Rank GO candidates by the P lower bound.

All five numerical conditions were recorded in this report before scoring. No setting, denominator or gate changed after outcomes. The union counts each event once. B includes repeater b, symmetric FIX 91, OAE and K. C96 uses the measured event depth and the TIC-radius cap from 014, with 2 Jupiter radii equal to 0.2009 solar radii. Missing radii leave the cap inactive.

## Findings

### 1. Matrix, CONFIRMED

P uses 1,098 observable reference planets on 506 campaign-star clusters, with fixed bin counts 242, 229, 221, 187 and 219. R uses the original 222 T156 reference trials on 158 clusters, with bin counts 48, 35, 46, 47 and 46. Each number gives equal weight to the five period bins. Intervals use 10,000 whole-star bootstrap replicates with fixed seed 2026111523. Both arms and campaigns were scored. Evidence is 023_score.py, 023_summary.py and data/astra/023/summary.json.

Planet recovery uses the adopted 013 novelty definition, excluding crossings already matched by an uninjected tier-1 event under that same configuration. T156 keeps the original frozen journal exclusion. Mask variants also exclude matches already present in their own uninjected background, following 011. The raw-injection replay groups and observable-trial denominator are fixed inputs.

| Configuration | P %, 95% interval | R %, 95% interval | Real | Upside-down | Spare | Control bins failed | New real | Dump exact / 12h screen | Eclipse catalogue / refit |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| B | 48.105 [43.91, 52.15] | 34.207 [27.03, 40.75] | 174 | 79 | 0 | 0 | 0 | N/A / 0 | 0 / 0 |
| B+C96 | 43.437 [39.07, 47.74] | 32.061 [24.72, 38.74] | 124 | 53 | 26 | 0 | 0 | N/A / 0 | 0 / 0 |
| B+DS | 49.980 [45.70, 54.11] | 35.502 [28.26, 42.19] | 204 | 83 | -4 | 0 | 30 | N/A / 30 | 0 / 0 |
| B+C96+DS | 45.115 [40.71, 49.45] | 32.921 [25.60, 39.71] | 143 | 56 | 23 | 0 | 19 | N/A / 19 | 0 / 0 |
| B+C96+M1 | 44.575 [40.24, 48.85] | 32.061 [24.68, 38.70] | 141 | 56 | 23 | 0 | 29 | N/A / 0 | 2 / 0 |
| B+C96+M2 | 44.801 [40.50, 49.06] | 32.486 [25.20, 39.12] | 139 | 56 | 23 | 0 | 24 | N/A / 1 | 1 / 0 |
| B+C96+DS+M1 | 46.332 [41.92, 50.64] | 32.486 [25.16, 39.12] | 158 | 59 | 20 | 0 | 46 | N/A / 17 | 2 / 0 |
| B+C96+DS+M2 | 46.491 [42.08, 50.77] | 32.912 [25.70, 39.58] | 156 | 59 | 20 | 0 | 41 | N/A / 18 | 1 / 0 |

### 2. Failure margins, CONFIRMED for rules (a) to (d)

Margins are percentage points for P and its lower bound, and event counts for background. Zero means the limit is met. All 40 planet paired-control intervals include zero. All configurations fail rule (a), so the zero-GO conclusion holds with the exact dump-window rule unresolved.

| Configuration | P short of 50 | Lower bound short of 40 | Upside-down above 79 | Real above 174 | Rule (e) evidence |
|---|---:|---:|---:|---:|---|
| B | 1.8950 | 0.0000 | 0 | 0 | sufficient upper bound 0, passes |
| B+C96 | 6.5630 | 0.9280 | 0 | 0 | sufficient upper bound 0, passes |
| B+DS | 0.0197 | 0.0000 | 4 | 30 | exact window unresolved, conservative upper bound 30 |
| B+C96+DS | 4.8852 | 0.0000 | 0 | 0 | exact window unresolved, conservative upper bound 19 |
| B+C96+M1 | 5.4248 | 0.0000 | 0 | 0 | sufficient upper bound 2, passes |
| B+C96+M2 | 5.1990 | 0.0000 | 0 | 0 | sufficient upper bound 2, passes |
| B+C96+DS+M1 | 3.6684 | 0.0000 | 0 | 0 | exact window unresolved, conservative upper bound 19 |
| B+C96+DS+M2 | 3.5088 | 0.0000 | 0 | 0 | exact window unresolved, conservative upper bound 19 |

B+DS misses P by 0.0197 percentage points and exceeds the upside-down and real limits by 4 and 30 events. No GO ranking exists. The highest P lower bound also belongs to B+DS, at 45.703%.

### 3. C96 costs recovery on this fixed bench, CONFIRMED

C96 removes 50 real and 26 upside-down background events, exactly reproducing 014. On the original planet bench it also removes 51 dip recoveries and 54 bump recoveries, reducing P by 4.668 percentage points. Of the 51 lost dips, 50 were planted deeper than their host cap and one was planted within it. Among all 1,098 fixed trials, 130 have above-cap assigned depths, 902 are within cap and 66 lack a usable radius. All five reference T156 dip losses have above-cap planted depths.

The 014 deep bench drew its input depths below each host cap and retained all 264 recovered dips in that sample. The original 006 reference bench assigns 3,000 to 6,000 ppm independently of the host cap. These different input populations explain most of the new loss. The one within-cap lost dip was planted at 97.24% of its cap. Three nearby SNR-7 detector boxes span 75.36% to 104.83% of the cap. A hard boundary on measured depth can reject an allowed injected depth because the fitted depth differs from the injected depth. The qualifying-box attribution has not been independently reimplemented. Evidence is 023_cap_diagnostic.py and cap-diagnostic.json. The original denominator and pass rule remain the ones scored.

### 4. Dump and eclipse screens, mixed CONFIRMED and UNCERTAIN evidence

CONFIRMED. The 014 map established zero replicated tier-1 dump-excess windows. Its only positive all-event G2 precursor, 6 to 3 hours before a dump, failed replication in G3. Exact counts inside an established excess window are N/A. I fixed a conservative diagnostic before matrix outputs, covering every mapped near-dump bin through centre distance at most 12 hours OR box containment. The upper bound also includes unknown timing and the union of catalogue-only and stored frozen-refit eclipse classifications. A bound at most five is sufficient for rule (e) for any window within those mapped bins. A larger bound leaves that rule unresolved.

Eclipse distance uses the event centre, catalogue period and epoch, and one full catalogue width. The secondary uses its catalogue phase and width where available, with a half-phase and primary-width fallback otherwise. The alternative refit calculation adds the stored frozen primary offset. The failed 014 fitted ephemerides were excluded. These classifications measure proximity to predicted eclipses. Physical attribution to eclipse leftovers is UNCERTAIN.

| Configuration | G2 precursor | Catalogue eclipse | Refit eclipse | Conservative union | Unknown classifications | Secondary fallback among new real |
|---|---:|---:|---:|---:|---:|---:|
| B | 0 | 0 | 0 | 0 | 0 | 0 |
| B+C96 | 0 | 0 | 0 | 0 | 0 | 0 |
| B+DS | 2 | 0 | 0 | 30 | 1 | 13 |
| B+C96+DS | 1 | 0 | 0 | 19 | 0 | 12 |
| B+C96+M1 | 0 | 2 | 0 | 2 | 0 | 24 |
| B+C96+M2 | 0 | 1 | 0 | 2 | 0 | 21 |
| B+C96+DS+M1 | 2 | 2 | 0 | 19 | 0 | 35 |
| B+C96+DS+M2 | 1 | 1 | 0 | 19 | 0 | 31 |

Every new real event has its signed hours from the nearest design-only momentum-dump reference and both eclipse classifications in data/astra/023/new-real-events.csv. Dump references cover 108 sectors, with 271 of 321 sampled files agreeing with the selected sector reference. The map had complete sampled-file agreement in 58 sectors. Reference disagreement limits fine timing interpretation. One B+DS new event lacks a complete eclipse classification and is already inside the dump screen.

## Planet gains and losses against B

Each cell is gained / lost planets, in binary-period days. The fixed bin definitions are those of 006 and 013, with edges 5, 10, 14, 20 and 27.4 days.

| Configuration | 5 to 10 | 10 to 14 | 14 to 20 | 20 to 27.4 | 27.4+ |
|---|---|---|---|---|---|
| B | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| B+C96 | 0 / 11 | 0 / 12 | 0 / 3 | 0 / 10 | 0 / 15 |
| B+DS | 0 / 0 | 2 / 0 | 7 / 0 | 4 / 0 | 7 / 0 |
| B+C96+DS | 0 / 11 | 2 / 12 | 6 / 3 | 3 / 10 | 7 / 15 |
| B+C96+M1 | 4 / 10 | 1 / 12 | 2 / 3 | 2 / 12 | 5 / 15 |
| B+C96+M2 | 3 / 10 | 0 / 12 | 3 / 3 | 5 / 13 | 6 / 15 |
| B+C96+DS+M1 | 5 / 10 | 4 / 12 | 8 / 3 | 5 / 12 | 11 / 15 |
| B+C96+DS+M2 | 3 / 10 | 3 / 12 | 8 / 3 | 9 / 13 | 12 / 15 |

## Paired control by bin

Each cell gives the planet-bench 99% whole-star bootstrap interval for dip recovery minus bump recovery, in percentage points. Every cell passes the fixed zero-in-interval rule. The all-2,000 T156 and 222-trial reference controls also pass every bin for all eight configurations, with their interval endpoints retained in summary.json. These are pointwise intervals for the five predeclared bins.

| Configuration | 5 to 10 | 10 to 14 | 14 to 20 | 20 to 27.4 | 27.4+ |
|---|---|---|---|---|---|
| B | [-4.21, 5.53] | [-3.85, 5.12] | [-7.92, 3.86] | [-1.72, 14.94] | [-3.14, 5.05] |
| B+C96 | [-4.37, 4.30] | [-1.83, 7.24] | [-7.42, 4.19] | [-1.71, 13.87] | [-2.42, 5.32] |
| B+DS | [-4.82, 4.67] | [-3.46, 5.74] | [-7.46, 5.49] | [-1.30, 14.71] | [-2.92, 6.00] |
| B+C96+DS | [-5.29, 3.43] | [-1.50, 7.92] | [-6.83, 5.83] | [-1.26, 13.58] | [-2.24, 6.25] |
| B+C96+M1 | [-3.45, 5.14] | [-1.79, 7.14] | [-8.21, 3.23] | [-2.87, 13.00] | [-3.73, 4.76] |
| B+C96+M2 | [-3.45, 5.14] | [-2.45, 6.91] | [-8.21, 3.11] | [-2.42, 13.48] | [-3.00, 5.05] |
| B+C96+DS+M1 | [-4.33, 4.19] | [-1.46, 7.83] | [-7.66, 4.66] | [-2.47, 12.72] | [-2.91, 5.91] |
| B+C96+DS+M2 | [-4.33, 4.19] | [-2.16, 7.52] | [-7.72, 4.68] | [-1.72, 13.92] | [-2.24, 6.25] |

## Untouched background by campaign and period bin

Each cell gives real / upside-down tier-1 events. Every allowed design star was included in its campaign, with zero-event stars retained in the eligibility policy.

| Campaign, period bin | B | B+C96 | B+DS | B+C96+DS | B+C96+M1 | B+C96+M2 | B+C96+DS+M1 | B+C96+DS+M2 |
|---|---|---|---|---|---|---|---|---|
| g2, 5 to 10 | 18 / 14 | 16 / 7 | 28 / 14 | 19 / 7 | 22 / 8 | 21 / 8 | 27 / 8 | 24 / 8 |
| g2, 10 to 14 | 15 / 10 | 9 / 9 | 17 / 10 | 11 / 9 | 14 / 9 | 13 / 9 | 15 / 9 | 15 / 9 |
| g2, 14 to 20 | 35 / 8 | 30 / 4 | 40 / 9 | 34 / 5 | 33 / 5 | 33 / 5 | 36 / 6 | 37 / 6 |
| g2, 20 to 27.4 | 5 / 6 | 5 / 5 | 9 / 7 | 8 / 5 | 5 / 5 | 4 / 5 | 7 / 5 | 6 / 5 |
| g2, 27.4+ | 38 / 16 | 38 / 15 | 44 / 18 | 44 / 17 | 41 / 16 | 42 / 16 | 46 / 18 | 47 / 18 |
| g3, 5 to 10 | 15 / 13 | 7 / 8 | 15 / 13 | 7 / 8 | 7 / 8 | 7 / 8 | 7 / 8 | 7 / 8 |
| g3, 10 to 14 | 13 / 7 | 10 / 2 | 13 / 7 | 10 / 2 | 10 / 2 | 10 / 2 | 10 / 2 | 10 / 2 |
| g3, 14 to 20 | 20 / 3 | 4 / 2 | 21 / 3 | 5 / 2 | 4 / 2 | 4 / 2 | 5 / 2 | 5 / 2 |
| g3, 20 to 27.4 | 7 / 2 | 3 / 1 | 7 / 2 | 3 / 1 | 3 / 1 | 3 / 1 | 3 / 1 | 3 / 1 |
| g3, 27.4+ | 8 / 0 | 2 / 0 | 10 / 0 | 2 / 0 | 2 / 0 | 2 / 0 | 2 / 0 | 2 / 0 |

## Verification actually performed

- CONFIRMED. All 12 scoring tasks completed with two scoring workers. Both arms, both campaigns, all three mask modes and both benches ran. B and DS reproduced all saved 013 trial outcomes in each bench. Aggregate B reproduced P 48.1050%, R 34.2070%, and background 174 / 79. There is no baseline numerical discrepancy.
- CONFIRMED. Twelve redirected source hashes, the copied mask selftest, three rejected access attempts and an allowed private write passed the harness smoke. Thirteen small rule/access checks passed and a deliberately broken dump-shape threshold was rejected.
- CONFIRMED. Independent direct trial iteration checked denominators, rates and gained/lost counts for the planet bench, all 2,000 T156 trials and the 222-trial reference subset. Three explicit whole-star resamples matched the vectorized bootstrap aggregation. Source fingerprints and the five verification groups are in verification.json.
- Static Python parsing ran separately from runtime scoring. It caught one unmatched parenthesis before launch. The verifier correction passed before the run. Git diff --check covered tracked changes, with an LF-to-CRLF advisory on USAGE.md. A separate whitespace scan covered the newly authored scripts and reports. The preserved historical source copies retain their own byte provenance.
- Producer verification was performed in this session. Independent review by Claude or Fable is pending. Source hashes establish byte provenance. Semantic evidence comes from identity checks, rule checks and trial recounts.

## Reproduction and output locations

Run D:/second-sun/.venv/Scripts/python.exe -I -B research/astra/scripts/023_run.py from this worktree. It runs the rule checks, scoring, bootstrap summary, cap diagnostic and verifier with two scoring workers. 023_prepare.py recovers the historical copies with read-only git show if rebuilding the source bundle is required. 023_report.py renders this handoff from verified outputs.

Machine outputs, temporary files, caches, historical reference source, trial rows and event details are under data/astra/023. The final aggregate is summary.json. Combined trial files are combined-planets.json and combined-T156.json. Every private event-group read is checked against campaign design membership before opening. New report and script files contain counts only.

## What I did NOT check

- NOT TESTED. A production Petrova implementation, a new freeze, G1 or sealed light, fresh raw-light searches, new injections, known-planet recovery, diluted-depth physics, limb darkening or stellar-radius uncertainty.
- NOT TESTED. Brightness, product and era sensitivity splits. The requested period/campaign breakdowns are provided. Bootstrap intervals describe the fixed design-star bench.
- UNCERTAIN. The exact dump-excess window, physical cause of individual new events and the truth of catalogue timing predictions. The conservative screen and secondary fallback are explicit assumptions.
- NOT TESTED. Claude's full session-log fence checker. The runner owns its logs and git metadata. Frozen-file changes were checked with read-only git inspection. The pre-existing .codex_run.lock belongs to the runner.

## STOP SIGNS hit

No new filter was adopted or tuned. The missing replicated dump window limits rule (e). The fixed P rule rejects all eight rows independently of that gap. The original 006 bench contains above-cap injections, so the 014 zero-loss observation has limited transfer to this denominator. These issues are handed to Claude and Fable. No process was stopped. No fitted 014 eclipse files were used.

## QUEUE PROPOSALS

- Node 1.6, FIX 96. Attach the priced loss, including one within-cap planet, to the existing review item. No cap margin has been selected.
- Node 1.7, bench specification. Record the 130 above-cap inputs and the unchanged denominator for Fable's decision. A future bench change would need its own predeclared specification.
- Node 1.1, DS. Attach the failed P and background limits and the unresolved exact dump-window gate to the existing design review.

## IDEAS

None built beyond the requested matrix and the diagnostic needed to explain its cap losses.

## Disagreements with Claude

The brief assumes that 014 supplies an excess window. The saved map and its report say none replicated. This report preserves that result and provides a conservative sufficient bound. The 014 zero-of-264 cap loss remains correct for its depth-limited sample. It does not predict zero loss on the original 006 sample.

## Questions for Ahmed

None. The headless instruction was followed and review decisions are left to Claude and Fable.

## Usage and run timing

Predicted 50 five-hour points and 8 weekly points, with the brief cap of 60 five-hour points. Actual usage meters are unavailable in this headless runner. No numerical actual is inferred. The supervisor ran from 17:39:44 to 17:54:49 Kuwait on 15 Nov 2026. Its planning estimate was 18:39:44. One terminal shell wait was used. No healthy-run logs were read during that wait.

Lesson. A depth cap priced on host-limited injections can have a different cost on a fixed-depth reference bench. Record the input population before transferring a zero-loss result.

**Next:** Claude reviews report 023 and runs the fence check before the Fable design round. This needs Claude. Review usage is unmeasured and no further Codex run is pending.
