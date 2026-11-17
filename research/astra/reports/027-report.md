**Fails: 0 of 2 c1a configurations passes the prewritten fixed-setting rule.**

# 027 c1a tier-level bench

Requested model GPT-6-Astra high; runtime model and effort independently unverified. Branch astra/027-c1a-tier-bench. Tree nodes 1.3, 1.5 and 1.6.

## Pass rule recorded BEFORE scoring

A c1a configuration passes only if ALL hold: (a) on the 968 possible planets, P gain against the same configuration without c1a at least +2.0 points, paired 95% interval above zero; (b) untouched upside-down background at most 79 and real at most 174 (the adopted limits, whatever the base reads); (c) paired control passes in every bin; (d) T156 R not below the base; (e) the F1 new-real rule holds: (new real) minus 2.3 x (new upside-down) at most 5.

Configurations: B, B+c1a, K2=B+C96+R2, K2+c1a. M2 excluded. Same fixed inputs and populations, all 1,098 and 968 possible planets. Equal-weight five binary-period bins; 10,000 whole-star bootstrap draws, seed 2026111523; 95% paired changes and 99% dip-minus-bump controls. Control passes when its per-bin 99% interval includes zero, as in 023. New events are compared both with B and with the same configuration without c1a. The F1 rule binds against B, as in F1 section 5 and 023; the matching-base comparison is diagnostic. This reference clarification was made before reading any c1a outcomes.

Equal-alarm analysis is conditional on failure of (b) ONLY. Even host identifiers choose the smallest SNR floor from 7.0, 7.5, 8.0, 8.5, 9.0, 10.0 with upside-down background no higher than the base on that half. Odd hosts are held out. Floor applies to all candidate events on both arms. Report held-out and pooled results; label the floor 'chosen on half the stars, a proposal, not a frozen setting'. No other threshold tuning.

Fresh-seed confirmation only after passing, subject to the cap. No claims of a new frozen setting or permission to search G1.


## Findings, CONFIRMED as computed

P is the mean recovery across five binary-period bins, not the fraction after pooling all trials. A whole-star bootstrap resamples hosts together, preserving dependence among planets placed on the same host. All intervals below are 95% unless marked 99%. Seed 2026111523, 10,000 draws. A count replay and source-copy checks are producer verification, not an independent scientific review.

| Configuration | P all 1,098 %, 95% | P possible 968 %, 95% | T156 R %, 95% | Real | Upside-down |
|---|---:|---:|---:|---:|---:|
| B | 48.105 [43.91, 52.15] | 48.404 [43.89, 52.74] | 34.207 [27.03, 40.75] | 174 | 79 |
| B+c1a | 45.316 [41.31, 49.15] | 46.078 [41.76, 50.17] | 21.903 [15.91, 27.62] | 186 | 111 |
| K2 | 45.835 [41.35, 50.18] | 51.018 [46.36, 55.40] | 32.921 [25.60, 39.71] | 158 | 63 |
| K2+c1a | 44.033 [39.81, 48.09] | 48.530 [44.14, 52.72] | 22.049 [15.48, 28.29] | 184 | 98 |

The reference T156 subset contains 222 Saturn-like trials from the full 2,000. Full-T156 and physically allowed subset intervals are retained in the machine summary and the tables below. M2 was not applied.

| Population | Configuration | Gain against B, points (95%) | Gain against matching base, points (95%) |
|---|---|---:|---:|
| fixed1098 | B | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| fixed1098 | B+c1a | -2.789 [-5.576, -0.065] | -2.789 [-5.576, -0.065] |
| fixed1098 | K2 | -2.270 [-4.802, -0.053] | -2.270 [-4.802, -0.053] |
| fixed1098 | K2+c1a | -4.072 [-7.395, -0.855] | -1.802 [-4.450, +0.844] |
| possible968 | B | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| possible968 | B+c1a | -2.326 [-5.301, +0.706] | -2.326 [-5.301, +0.706] |
| possible968 | K2 | +2.614 [+1.577, +3.731] | +2.614 [+1.577, +3.731] |
| possible968 | K2+c1a | +0.125 [-2.795, +3.060] | -2.489 [-5.394, +0.461] |

## Rule-by-rule outcome

Rule (c) requires controls on both planet populations. Rule (e) binds against B, following F1 and 023. The comparison against the corresponding c1a-off configuration is also shown as a diagnostic.

| Candidate | Rule | Number | Pass? |
|---|---|---|---|
| B+c1a | a | gain -2.326, lower 95% -5.301 | FAIL |
| B+c1a | b | real 186 / 174, upside-down 111 / 79 | FAIL |
| B+c1a | c | all-bin control: full True, possible True | PASS |
| B+c1a | d | reference R 21.903 vs base 34.207 | FAIL |
| B+c1a | e | new-real excess vs B -58.6, vs base -58.6; limit 5 | PASS |
| K2+c1a | a | gain -2.489, lower 95% -5.394 | FAIL |
| K2+c1a | b | real 184 / 174, upside-down 98 / 79 | FAIL |
| K2+c1a | c | all-bin control: full True, possible True | PASS |
| K2+c1a | d | reference R 22.049 vs base 32.921 | FAIL |
| K2+c1a | e | new-real excess vs B -23.0, vs base -35.7; limit 5 | PASS |

## Equal-alarm analysis

Not triggered. Neither candidate fails background rule (b) alone. The preregistration therefore does not authorize trying higher SNR floors on these results.

## Gains and losses by binary-period bin

Counts are paired with the same configuration without c1a. A planet with any novel tier-1 crossing counts once. B and K2 use the saved 013/023 novelty definitions; c1a uses its own untouched background for that comparison.

| Population | Candidate | Bin (days) | n | Dip gained / lost | Bump gained / lost | Dip-minus-bump 99%, points | Pass? |
|---|---|---|---:|---:|---:|---:|---|
| fixed1098 | B+c1a | 5 to 10 | 242 | 29 / 15 | 30 / 11 | -7.17, +4.56 | PASS |
| fixed1098 | B+c1a | 10 to 14 | 229 | 13 / 12 | 13 / 15 | -3.42, +7.14 | PASS |
| fixed1098 | B+c1a | 14 to 20 | 221 | 22 / 15 | 14 / 16 | -2.30, +7.17 | PASS |
| fixed1098 | B+c1a | 20 to 27.4 | 187 | 7 / 31 | 7 / 24 | -5.26, +10.13 | PASS |
| fixed1098 | B+c1a | 27.4 and up | 219 | 6 / 29 | 7 / 25 | -6.25, +3.55 | PASS |
| fixed1098 | K2+c1a | 5 to 10 | 242 | 32 / 14 | 33 / 9 | -9.41, +2.55 | PASS |
| fixed1098 | K2+c1a | 10 to 14 | 229 | 15 / 13 | 16 / 13 | -2.46, +8.26 | PASS |
| fixed1098 | K2+c1a | 14 to 20 | 221 | 21 / 18 | 14 / 15 | -4.04, +5.11 | PASS |
| fixed1098 | K2+c1a | 20 to 27.4 | 187 | 8 / 25 | 9 / 19 | -3.89, +9.18 | PASS |
| fixed1098 | K2+c1a | 27.4 and up | 219 | 4 / 25 | 9 / 24 | -6.19, +4.46 | PASS |
| possible968 | B+c1a | 5 to 10 | 210 | 26 / 13 | 29 / 9 | -9.60, +3.43 | PASS |
| possible968 | B+c1a | 10 to 14 | 198 | 13 / 11 | 12 / 12 | -3.79, +8.11 | PASS |
| possible968 | B+c1a | 14 to 20 | 202 | 21 / 14 | 14 / 16 | -2.02, +7.89 | PASS |
| possible968 | B+c1a | 20 to 27.4 | 167 | 7 / 25 | 5 / 20 | -5.26, +11.52 | PASS |
| possible968 | B+c1a | 27.4 and up | 191 | 5 / 27 | 7 / 23 | -7.07, +4.20 | PASS |
| possible968 | K2+c1a | 5 to 10 | 210 | 28 / 13 | 30 / 8 | -11.46, +2.00 | PASS |
| possible968 | K2+c1a | 10 to 14 | 198 | 12 / 12 | 15 / 13 | -4.09, +7.46 | PASS |
| possible968 | K2+c1a | 14 to 20 | 202 | 20 / 18 | 13 / 15 | -4.52, +5.58 | PASS |
| possible968 | K2+c1a | 20 to 27.4 | 167 | 8 / 24 | 7 / 18 | -4.00, +10.53 | PASS |
| possible968 | K2+c1a | 27.4 and up | 191 | 4 / 25 | 9 / 24 | -7.08, +5.07 | PASS |

## Background and blind spots

New-event matching follows 023: same campaign, host, sector and arm, within 0.1 day plus half the larger box duration. This is a tolerance match, not exact event identity. Every new real event has private dump-distance and eclipse-width evidence in data/astra/027/new-real-events.json. Missing geometry is reported, never treated as clean.

| Configuration | Compared with | New real / upside-down | New real within 12 h of dump | Within one catalogue eclipse width | Unknown geometry |
|---|---|---:|---:|---:|---:|
| B+c1a | B | 84 / 62 | 8 | 0 | 7 |
| B+c1a | base | 84 / 62 | 8 | 0 | 7 |
| K2 | B | 34 / 10 | 21 | 0 | 1 |
| K2 | base | 0 / 0 | 0 | 0 | 0 |
| K2+c1a | B | 115 / 60 | 35 | 0 | 9 |
| K2+c1a | base | 100 / 59 | 27 | 0 | 8 |

New SNR-7 candidates are matched to all old SNR-7 candidates before counting hold flags. Counts overlap because one event can have several flags; they are not an additive attribution.

| Configuration | Campaign | Arm | New candidates | Held at tier 2 | Tier 1 | Dump | Step | Gap edge | Ramp | Repeater | Dominated |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| B+c1a | g2 | real | 2602 | 2528 | 48 | 788 | 1959 | 738 | 545 | 99 | 817 |
| B+c1a | g2 | flip | 2060 | 2010 | 44 | 666 | 1947 | 714 | 515 | 47 | 715 |
| B+c1a | g3 | real | 265 | 250 | 12 | 27 | 222 | 90 | 73 | 9 | 82 |
| B+c1a | g3 | flip | 312 | 300 | 10 | 35 | 287 | 126 | 99 | 0 | 105 |
| K2+c1a | g2 | real | 2602 | 2505 | 68 | 724 | 1959 | 0 | 545 | 99 | 817 |
| K2+c1a | g2 | flip | 2060 | 2015 | 38 | 656 | 1947 | 0 | 515 | 47 | 715 |
| K2+c1a | g3 | real | 265 | 255 | 7 | 26 | 222 | 0 | 73 | 9 | 82 |
| K2+c1a | g3 | flip | 312 | 300 | 10 | 35 | 287 | 0 | 99 | 0 | 105 |

## T156 supplementary measures

| Population | n | B % | B+c1a % | K2 % | K2+c1a % |
|---|---:|---:|---:|---:|---:|
| T156all | 2000 | 24.950 [22.37, 27.65] | 21.850 [19.61, 24.17] | 23.900 [21.22, 26.75] | 20.900 [18.60, 23.26] |
| T156possible | 1824 | 23.785 [21.07, 26.57] | 21.006 [18.58, 23.44] | 25.885 [23.01, 28.81] | 22.551 [20.06, 25.08] |
| T156reference_possible | 203 | 34.782 [26.91, 41.57] | 21.861 [15.26, 27.86] | 35.747 [27.85, 42.72] | 23.408 [16.24, 30.01] |

## Identity and verification

B reproduced P 48.105%, R 34.207%, and background 174 / 79. K2 reproduced possible P 51.02% and background 158 / 63. Both arms of every saved B planet/T156 trial and every saved K2 planet trial were compared, with assertions that can fail. K2 T156 is newly scored here, not an archived K2 identity claim. Raw c1a-off replay identity covered 50 untouched star-sectors, not every injected light curve.

Runtime rule checks compared 288 synthetic combinations against the extracted pure X10 rule, including 8 detections of a deliberately omitted cap. The access guard rejected three forbidden access events, allowed an authorized write, and checked 12 copy hashes. These hashes establish byte identity only. The copied mask self-test passed. The final verification file records coverage and arithmetic checks actually completed.

## What I did NOT check

No G1 or sealed-star search. No M2 combination, new mask design, quality change, production filter edit, freeze, known-planet replay or external publication. Fresh-seed confirmation is conditional on passing the prewritten rule. The machine data preserve both-arm trial results; this is producer verification, not an independent second key. The origin of any new background event is not established by proximity to a dump or an eclipse.

## STOP SIGNS hit

Usage meter and runtime model identification were unavailable. Any runtime access failure or scientific identity failure is documented in the work log; no bypass of the access guard is authorized.

## QUEUE PROPOSALS

Claude should file the measured c1a result under Tree node 1.3, with background and control evidence under nodes 1.5 and 1.6. No frozen setting is changed.

## IDEAS

None beyond the brief. M2 is a subsequent conditional test only if K2+c1a passes. It was not run.

## Disagreements with Claude

No technical direction was silently changed. Conservative interpretations are recorded in the pre-scoring pass rule.

## Questions for Ahmed

None required for this bench.

## Usage

Predicted 50 five-hour / 8 weekly points; cap 60 five-hour. Actual use and runtime model/effort are unverified because the headless meter is unavailable. Lesson: a detector change must be priced using new detections and new untouched context at the final tier.

**Next:** Claude reviews this report and the private verification evidence before deciding whether c1a deserves further work. Review only; no additional Codex compute is requested, and its usage cost is unmeasured.
