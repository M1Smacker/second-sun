"""Render final report from completed, counts-only analyses; no scientific execution."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(r'D:\second-sun-astra');OUT=ROOT/'data/astra/003';REPORT=ROOT/'research/astra/reports/003-recovery-sprint.md'
old=REPORT.read_text(encoding='utf-8')
if '## Part 1: frozen design\n' in old:
    design=old.split('## Part 1: frozen design\n',1)[1].split('## Published-reference check',1)[0]
else:
    design=old.split('## Frozen design retained for provenance\n',1)[1].split('## Final result tables',1)[0].strip()
data=[json.loads((OUT/f'reference-flags-{n}.json').read_text(encoding='utf-8')) for n in ('g2','g3')]
present=Counter();freed=Counter();combos=Counter()
for d in data:present.update(d['flags_present']);freed.update(d['single_flag_removal_static']);combos.update(d['combinations'])
flagtable='| Flag or reason | Reference trials carrying it | Released if only this flag is cleared |\n|---|---:|---:|\n'
for k in ['repeater','step','gap_dump','ramp','dominated','c5','ecl_overlap','common','orbit_lock','p1_veto','flipmatch','second_product_disagreement','no_primary_snr7','preexisting']:
    flagtable+=f'| {k} | {present[k]} | {freed[k] if k not in ("second_product_disagreement","no_primary_snr7","preexisting") else "not evaluated"} |\n'
combotable='| Combination present on matched primary candidates | Trials |\n|---|---:|\n'+''.join(f'| {k} | {v} |\n' for k,v in combos.most_common())
text=f'''# 003 recovery sprint (Codex; runtime model/effort unverified, Astra High requested)

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

{flagtable}

Counts overlap. A trial can carry several flags; the last column clears one flag on the matched candidates while holding every other feature fixed. It is a static release count, not the measured gain of a new filter, and cannot be summed across flags. Combination rows are unions across a trial's matched primary candidates, not necessarily one event's exact combination. Trials lacking a primary SNR>=7 event or with prior matching events are kept separately.

{combotable}

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

1. **Node 1.1, repeater association candidate first.** Replace indiscriminate same-kind event counting with a predeclared association test for repeated binary structure, retaining independent step/gap/other safeguards. The reference static ceiling for clearing repeater alone is {freed['repeater']} of 222 trials, not a promised gain. Price on the same 2000 draws and unchanged matching rule, report reference and all-bin gains and losses, paired bumps, and un-injected upside-down alarm counts. Risk: releasing genuine recurring systematics. Claude designs one concrete candidate; Ahmed decides.
2. **Node 1.1, symmetric FIX 91, then coverage-aware step handling.** Symmetric coincidence handling has a confirmed correctness motive; its reference static clear-flag release is {freed['flipmatch']}. Clearing step alone releases {freed['step']} reference trials with other features frozen. Do not equate clearing the whole step flag with a coverage-only fix. Test each change separately on the unchanged full bench and un-injected controls; risk is admitting steps, ramps or paired instrumental features. A symmetry fix may reject additional bumps rather than gain dips, so it must be priced honestly.
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

{design}

'''
tables=(ROOT/'research/astra/reports/003-tables.md').read_text(encoding='utf-8')
REPORT.write_text(text+tables.replace('# 003 final tables','## Final result tables',1),encoding='utf-8')
print(json.dumps(dict(reference_flags=dict(present),reference_static_releases=dict(freed),reference_combinations=dict(combos)),indent=2))
