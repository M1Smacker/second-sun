**Plain verdict: six rules pass; rule (f) fails. N1 does not qualify under the written rules.**

# 030 lower-flank notch tier bench

Codex, runtime model and effort not independently verified for this continuation. Brief specifies neither. Branch astra/030d-notch-finish. No git writes or commits. Tree nodes 1.3, 1.5 and 1.6.

## Findings

CONFIRMED as computed: chosen detection threshold 6.5, selected only by the prewritten alarm limits. No filter was frozen or published.

| Threshold | Real tier 1 | Upside-down tier 1 |
|---:|---:|---:|
| 4.5 | 353 | 239 |
| 5 | 270 | 169 |
| 5.5 | 222 | 116 |
| 6 | 182 | 89 |
| 6.5 | 165 | 77 |
| 7 | 144 | 71 |

| Population | n | B % | N1 % | Paired gain, points (95%) |
|---|---:|---:|---:|---:|
| choosing_all | 1098 | 48.105 | 49.942 | +1.837 [-0.309, +4.012] |
| choosing_possible | 968 | 48.404 | 51.343 | +2.939 [+0.748, +5.215] |
| fresh_all | 1064 | 51.827 | 53.772 | +1.945 [+0.178, +3.753] |
| fresh_possible | 941 | 52.182 | 54.276 | +2.094 [+0.161, +4.105] |
| T156_all | 2000 | 24.950 | 24.900 | -0.050 [-1.181, +1.061] |
| T156_reference | 222 | 34.207 | 31.653 | -2.554 [-6.274, +0.986] |
| T156_reference_possible | 203 | 34.782 | 32.940 | -1.841 [-5.709, +1.956] |

P gives each of the five binary-period bins equal weight. A whole-star bootstrap keeps all planted planets on the same host together when resampling, avoiding falsely narrow intervals. There are 10,000 draws with seed 2026111830. Fable X1 seed is 2026111601.

| Gate | Number or evidence | Outcome |
|---|---|---|
| (a): Fresh gain at least 2 points and lower 95% bound above zero | +2.094 points, 95% [+0.161, +4.105] | PASS |
| (b): Both untouched alarm budgets | 165 real <= 174; 77 upside-down <= 79 | PASS |
| (c): Dip/bump 99% interval contains zero in all possible-planet bins | 10 of 10 choosing/fresh period-bin intervals include zero | PASS |
| (d): Off-switch and unchanged preprocessing checks | 50 off-switch sector replays; saved N1 preprocessing comparisons; source checks | PASS |
| (e): New real minus 2.3 times new upside-down at most 5 | 64 - 2.3 x 44 = -37.2 <= 5 | PASS |
| (f): Reference T156 R does not fall | B 34.207% to N1 31.653% | FAIL |
| (g): TOI-1338 b at least six of thirteen | B 6/13; N1 7/13 | PASS |

CONFIRMED: new alarms against B are 64 real and 44 upside-down; rule 4 excess is -37.2. Matching uses the existing bench tolerance, not exact event identity.

CONFIRMED: TOI-1338 b is 7 of 13 under N1, versus 6 under B. The denominator includes nine observed and four forecast epochs from T109.

Rule (g) uses the amended T109/Q5 sector-local context. B matches the historical six successful windows individually, with 10 of 10 O0 flag identities. N1 gives four observed-window and three forecast-window matches. Both versions assess all 13 windows; one has no stored data, as in historical Q5. The 19 existing N1 raw-light group replays cover the other 12 windows and were reused, then re-tiered at 6.5. No heavy phase was rerun. Design-background counts remain separately in known.json: B 1, N1 2. They are not rule (g).

## Per-crossing and paired-control counts

| Population | Period bin | Planets | Dip/bump planets | Crossings | Dip/bump crossings | Planet dip-minus-bump 99%, points | Control |
|---|---|---:|---:|---:|---:|---:|---|
| choosing_possible | 5 to 10 | 210 | 99/101 | 1757 | 248/249 | [-7.247, +5.702] | PASS |
| choosing_possible | 10 to 14 | 198 | 92/93 | 1084 | 242/242 | [-5.000, +3.743] | PASS |
| choosing_possible | 14 to 20 | 202 | 99/98 | 951 | 239/253 | [-3.030, +3.792] | PASS |
| choosing_possible | 20 to 27.4 | 167 | 83/81 | 478 | 158/155 | [-5.797, +8.772] | PASS |
| choosing_possible | 27.4 and up | 191 | 123/123 | 588 | 258/263 | [-5.073, +5.294] | PASS |

choosing_possible pooled per-crossing tier-1 rate: 23.569%.

| Population | Period bin | Planets | Dip/bump planets | Crossings | Dip/bump crossings | Planet dip-minus-bump 99%, points | Control |
|---|---|---:|---:|---:|---:|---:|---|
| fresh_possible | 5 to 10 | 217 | 93/92 | 1662 | 240/234 | [-4.412, +5.310] | PASS |
| fresh_possible | 10 to 14 | 203 | 96/99 | 1177 | 299/286 | [-7.212, +4.500] | PASS |
| fresh_possible | 14 to 20 | 187 | 102/104 | 816 | 269/284 | [-7.653, +4.762] | PASS |
| fresh_possible | 20 to 27.4 | 153 | 100/93 | 554 | 219/217 | [-1.399, +10.280] | PASS |
| fresh_possible | 27.4 and up | 181 | 111/107 | 589 | 227/224 | [-2.339, +8.383] | PASS |

fresh_possible pooled per-crossing tier-1 rate: 26.136%.

## Flags holding new untouched detections

Counts overlap; they are not additive causes.

real: 571 new detections, 535 below tier 1. c5 43, common 14, dominated 103, dump 60, ecl_overlap 87, flipmatch 1, gap_edge 48, known 8, orbit_lock 66, p1_veto 58, ramp 55, repeater 40, step 325.

flip: 330 new detections, 305 below tier 1. c5 19, common 18, dominated 58, dump 58, ecl_overlap 21, flipmatch 1, gap_edge 26, known 9, orbit_lock 5, p1_veto 8, ramp 34, step 247.

## Background by brightness, product, era and period

```json
{
  "period_bin:2:flip": 10,
  "brightness:<11:flip": 28,
  "product:SPOC:flip": 22,
  "era:56-93:flip": 38,
  "period_bin:2:real": 48,
  "brightness:<11:real": 74,
  "product:SPOC:real": 37,
  "era:56-93:real": 67,
  "period_bin:1:real": 23,
  "product:QLP:real": 74,
  "era:27-55:real": 39,
  "period_bin:1:flip": 19,
  "brightness:11-12:flip": 15,
  "product:TESS-SPOC:real": 43,
  "product:TESS-SPOC-SAP:real": 5,
  "period_bin:0:real": 31,
  "brightness:12-14:real": 55,
  "era:1-26:real": 47,
  "period_bin:4:flip": 15,
  "era:1-26:flip": 16,
  "era:94+:real": 12,
  "brightness:11-12:real": 36,
  "period_bin:4:real": 43,
  "period_bin:0:flip": 24,
  "product:SPOC-SAP:flip": 4,
  "product:SPOC-SAP:real": 6,
  "era:94+:flip": 6,
  "product:QLP:flip": 25,
  "era:27-55:flip": 17,
  "period_bin:3:real": 20,
  "brightness:12-14:flip": 34,
  "product:TESS-SPOC:flip": 25,
  "period_bin:3:flip": 9,
  "product:TESS-SPOC-SAP:flip": 1
}
```

## Verification and evidence

CONFIRMED: full saved-outcome B scoring matches both arms trial by trial, including P 48.105% / 48.404%, R 34.207%, and alarms 174 / 79. Independent 030_recount.py joins archived outcomes to raw injection journals without importing the pipeline. Raw off-switch event identity covers 50 untouched star-sectors. N1 untouched preprocessing metadata is checked against B for every regenerated group.

N1 reference parity and a separate direct-window oracle cover 27 cadence/duration cases. Deliberate wrong-flank, threshold-context and one-arm-budget mutations are rejected. Three mirror boundary checks, 15 candidate-nesting checks, zero-scale handling, source hashes, worker completion and population assertions also ran. These are producer checks, not independent review.

Evidence: data/astra/030/summary.json, verification.json, notch-checks.json, baseline-check.json, independent-recount.json, known.json, chosen.json and worker logs. This continuation ran 030_t109.py, 030_summary.py, 030_verify.py and 030_finish.py with the required interpreter and -I -B. Do not restart 030_run.py. Frozen source files were not edited.

030d verification independently recounts the saved final T109 tiers, checks the historical B windows, checks 38 input hashes, checks all saved worker completion records, and validates the summary populations and threshold rule. A mutation removing N1 tier-1 hits from the private scored rows is rejected; restoration passes. Earlier raw identity and synthetic checks are saved evidence, not rerun here. Hash equality proves byte identity only. Claude independently recounted the bench in research/stage3/rs039/RECOUNT-030-2026-11-18.md; point estimates and gate verdicts agree. His fresh 95% interval is +0.12 to +4.15; the prescribed 030 bootstrap gives +0.161 to +4.105. The interval difference does not change rule (a). That recount does not independently review the new T109 implementation.

Source amendment: only 030_finish.py and 030_verify.py changed among the locked existing scripts; 030_t109.py was added. Full old/new SHA-256 maps are in data/astra/030/030d-source-amendment.json. The scoring, generation, threshold selection and summary sources remain unchanged from the 030b lock. The prior report is preserved privately as 030d-prior-report.md. Earlier 030b amendment provenance remains in 030b-source-amendment.json.

The preserved design-background note says two of thirteen sectors. It must not be read as raw-input coverage: the archive and N1 replays cover twelve crossing sectors. The amended sector-local test and full campaign background use different event contexts.

## What I did NOT check

No fenced-star searches, witness-star meter, sky search, new downloads, frozen release, book edits or publication. No independent reviewer has assessed this implementation. The benchmark does not establish sensitivity for all planets in the sky. Per-crossing rates are pooled within the reported populations; alarms have brightness/product/era splits, while planet P uses the specified period-bin weighting.

## STOP SIGNS hit

No scientific gate was relaxed. Rule (f) fails, so N1 does not qualify for adoption under this brief. An initial 030d availability assertion demanded stored data in every window; historical Q5 explicitly includes one missing window. That implementation assertion was corrected to preserve the historical missing outcome before B or N1 was scored. B then reproduced 6/13 before N1 was evaluated. The earlier 030b meter stop and nine-versus-ten grid wording are preserved in the prior report; the actual nine-length grid was retained.

## QUEUE PROPOSALS

None. This is the requested node 1.3 bench, not a filter adoption.

## IDEAS

None outside the brief.

## Disagreements with Claude

None on the completed verdict. The source uses nine grid lengths despite the original brief saying ten. No scientific decision was silently changed.

## Questions for Ahmed

None.

## Usage

030d predicted 35 five-hour points / 6 weekly points. Latest observed actual: 3% to 28% five-hour (+25); 81% to 85% weekly (+4); weekly actual/predicted about 0.67. Account-wide rounded meter, measured before final handoff. Earlier 030 and 030b usage rows remain separate. Lesson: reproduce the historical context and missing-data outcomes before judging a known-system gate.

Next: Claude reviews the report and producer checks before any adoption decision; review cost unmeasured, Claude required.
