**Found something. The load losses are traced. The predeclared quality candidate fails its acceptance rule.**

# 025 Load losses

Codex runtime model and effort are independently unverified. The brief specifies neither.
Completed 2026-11-16 14:34 Kuwait. Branch astra/025-load-losses. Tree node 1.2.

This report follows the filename and no-git-write instructions in the current user request. The pre-existing runner lock was preserved. The runner handles the commit.

## What was found

CONFIRMED. The 005 roster reproduces exactly. Twenty-one of the 52 reference window losses lack loaded centre support, 15 have an archive gap, ten lie outside safe windows, and six lack safe windows. Twenty of the 21 load cases have finite archived flux. The remaining case also lacks finite archived flux.

| Blocking bits among nearby finite samples, or archived-flux condition | Reference load cases |
|---|---:|
| 4096 | 14 |
| 128+4096 | 1 |
| 128 | 1 |
| 1073741824 | 3 |
| nonfinite archived flux | 1 |
| 2048+1073741824 | 1 |

Bit combinations in that table are unions across nearby samples. Each exact quality word, cadence count, filename, selected column, hypothesis checklist and exact source condition is saved privately in roster.json, case-evidence.json and the trace files. Bit 4096 means Straylight2 for SPOC-family files. The installed QLP reader also uses it for low precision before sector 56. QLP adds bit 1073741824 from sector 56. Bit 128 is manual exclusion, and bit 2048 is stray light. These meanings were checked in the installed reader and quality definitions.

CONFIRMED. detect_v2.load() applies Lightkurve hard quality screening before finite-time and flux selection. The QLP reader adds its product-specific quality mask. The no-finite-flux category records an additional archived-data limitation. Quality screening can also precede rejection of those nonfinite samples.

CONFIRMED. Zero of the original 21 has a whole-sector FIX 101 mask. 1 also lacks safe windows. 3 retain centre support through masking in another product. That support establishes alternate search input, with recovery measured separately below.

## The 16 usable-before-window cases

| Rule | Cases | Source condition |
|---|---:|---|
| Own SPOC support | 3 | stage2_search.py line 154, use good_windows(own) |
| Neighbour intersection | 5 | stage2_search.py line 156, use audit_all.neighbour_windows() |
| Half-day start trim | 2 | detect_v2.py line 111, retain from start + 0.5 d |
| No safe windows | 6 | stage2_search.py line 158, own SPOC absent and fewer than two neighbours |

CONFIRMED. These branches implement their comments, including the intersection and start trim. The six absent-window cases fail a minimum-reference requirement. 1 of the 16 has usable alternate-product centre support. The trace establishes the removing condition. Safety of expanding each interval remains NOT TESTED.

## Across all 2,000 fixed T156 draws

First-loss accounting assigns each draw to the earliest classified data-support loss. This keeps overlapping quality, window and mask problems from being added together as separate planets. The final mask trace includes each planted dip before eclipse masking.

| First classified loss or retained support | Draws |
|---|---:|
| retained to score input | 1413 |
| archive gap | 99 |
| catalogue drift mask | 94 |
| quality exclusion | 148 |
| other eclipse or repeat mask | 118 |
| neighbour intersection | 42 |
| no safe windows | 50 |
| half-day start trim | 16 |
| own SPOC | 16 |
| nonfinite archived flux | 4 |

CONFIRMED. Missing selected files 0. Missing manifest entries 0. FITS header sectors have zero mismatches across the 4,613 traced trial/product rows. Every inspected header uses BJDREFI 2457000 and TIMESYS TDB. The archive, loader and centre-support timestamps therefore share the expected reference in this sample.

The drift overlap counts are separate from first losses. 64 draws have a selected product whose catalogue window covers its full retained sector. 98 intersect a drift-added catalogue window near the planted centre. A drift-cap prototype was conditional in Claude's update. The original 21 load cases supply zero whole-sector FIX 101 cases, so this brief tests the largest measured load cause.

RS-038 supplies its own 006 replay results, cited here without recounting. Its 1,292 never-scored crossings comprise 526 mask, 248 no-finite-score, 235 safe-window, 192 best-product-table gaps, 60 capture mismatches and 31 load cases. Its bench-capture qualifications also apply when interpreting single-product diagnostics. [RS-038](../../stage3/rs038/KEEP-PLANETS-THROUGH-VETTING-2026-11-15.md)

## Fixed candidate and measured performance

The candidate admits bit 4096 in the loader and SAP/PDC twin loaders. Every other existing blocking bit, QLP late-sector low-precision bit, finite-flux rule and borrowed-window rule stays active. The bench copy uses 025_loader.py. The proposed bench diff is 025-loader-prototype.patch. The frozen pipeline files retain their original bytes.

The pass rule was written before candidate computation. Restore searched centre support for at least 11 of the original 21, increase T156 reference R, add no upside-down tier-1 background, and reproduce events exactly on 50 unaffected star-sectors. The fixed 006 planet P is also measured.

| Configuration | Reference R | Planet P | Background real | Background upside-down |
|---|---:|---:|---:|---:|
| B | 34.207% | 48.105% | 174 | 79 |
| B+C96 | 32.061% | 43.437% | 124 | 53 |
| B+admit4096 | 31.519% | 45.244% | 254 | 172 |
| B+C96+admit4096 | 28.948% | 40.822% | 169 | 136 |

R uses the 222 reference draws. P uses the unchanged 1,098 observable planet trials. Both scores give equal weight to the five fixed period bins. Raw counts and within-star dependence are retained. Intervals use 10,000 paired whole-star bootstrap draws, seed 2026111525.

CONFIRMED. Searched centre support restored for 12/21. Exact event identity checked on 50 unaffected star-sectors. Both primary and available SAP group events are compared with the saved development groups.

| Acceptance check | Outcome |
|---|---|
| restores_half | PASS |
| reference_gain | FAIL |
| upside_down_ceiling | FAIL |
| identity_50 | PASS |

| Binary period | Reference draws | B dip / bump | Candidate dip / bump | Candidate paired 99% interval |
|---|---:|---:|---:|---|
| 5 to 10 d | 48 | 7 / 7 | 5 / 6 | -12.96 to 7.14 points |
| 10 to 14 d | 35 | 11 / 12 | 13 / 12 | -16.67 to 21.21 points |
| 14 to 20 d | 46 | 15 / 13 | 13 / 15 | -15.38 to 7.14 points |
| 20 to 27.4 d | 47 | 23 / 24 | 18 / 21 | -20.00 to 9.26 points |
| 27.4 d onward | 46 | 20 / 18 | 20 / 16 | -3.64 to 24.32 points |

The following pooled counts within each fixed stratum are descriptive. The official scores above retain equal period-bin weights.

| T156 stratum | Draws | B dip / bump | Candidate dip / bump |
|---|---:|---:|---:|
| brightness/11to12 | 476 | 121 / 122 | 105 / 109 |
| brightness/12plus | 486 | 37 / 36 | 37 / 35 |
| brightness/<11 | 1038 | 341 / 349 | 309 / 315 |
| era/1to26 | 566 | 171 / 164 | 154 / 156 |
| era/27to55 | 504 | 130 / 137 | 98 / 99 |
| era/56to93 | 757 | 167 / 174 | 172 / 178 |
| era/94plus | 173 | 31 / 32 | 27 / 26 |
| product/QLP | 852 | 158 / 171 | 126 / 134 |
| product/SPOC | 470 | 144 / 148 | 135 / 138 |
| product/TESS-SPOC | 599 | 197 / 188 | 190 / 187 |
| product/nan | 79 | 0 / 0 | 0 / 0 |

## Falsifiers and eclipse-residue control

CONFIRMED. 15 archived bit-4096 cases fail centre support under the original loader, pass under the candidate, and fail again when the original policy is restored as a mutation. 12 distinct product/era/median-cadence paths were exercised. These include 30-minute, 10-minute and 200-second data, SPOC 2-minute data, and the three requested QLP eras.

CONFIRMED on the 22 audited file/path instances. In two tested sector-94-onward QLP files, 9,755 returned cadences carry bit 536870912. Four tested SPOC-family files retain 871 cadences carrying bit 32768. Thus the installed hard policy retains some nonzero quality words. The physical meaning and safety of the QLP high bit remain UNCERTAIN in this brief. The prototype retains the inherited treatment of these bits.

CONFIRMED on constructed light. All three wrong-epoch deep-eclipse controls become detected events when bit 4096 is admitted. The original quality policy excludes their flagged eclipse samples. The controls have 30-minute, 10-minute and 200-second sampling. They demonstrate the eclipse-residue hazard of this quality relaxation. They do not measure real contamination rates.

The candidate introduces 150 new real-arm and 125 new upside-down tier-1 background events, using event identity at the stored centre and duration. 68 new real events meet RS-027's existing 8,000-ppm-or-SNR-50 diagnostic. Their physical origin remains UNCERTAIN without independent eclipse-time measurements. [RS-027](../../stage3/rs027/NEW-EVENTS-ROOT-CAUSE-2026-11-14.md)

## Checks actually performed

Producer verification completed 6 check groups. These include direct trial and transition recounts, complete generated replay coverage, design membership, preparation exception counts, denied-access probes, 50-sector event identity and twelve frozen-source byte identities. Static Python parsing and worktree checks are recorded in the worklog. Source hashes establish the measured bytes. Scientific review remains with Claude.

## What I did NOT check

- G1 light, fence-B light, new sealed searches, external services and publication.
- A drift-cap or refit-centred-window prototype, because FIX 101 supplies zero whole-sector cases among the 21 load losses.
- SPOC 20-second data. This fixed T156 trace contains no such runtime path.
- Whether relaxing any other quality flag or widening any borrowed window is safe.
- Independent scientific review, the complete runner-log fence check, or the physical origin of every new real-background event.
- Usage-panel percentages. The headless runner exposes no meter.

## STOP SIGNS hit

The candidate acceptance rule governs adoption. Any failed check leaves the prototype on the bench. No frozen-file edit, sealed-run reinterpretation or result-driven threshold change was made.

## QUEUE PROPOSALS

Node 1.2. Attach the measured cause table and the tested bit-4096 result to the existing load/window and FIX 101 work. The direct trace supports an intentional-quality-cut mechanism for the dominant load loss. Adoption requires the full acceptance rule.

## IDEAS

None beyond the requested prototype.

## Disagreements with Claude

The original 21 label is a best-product centre-support diagnosis. Three cases have alternate-product search input. This is a measured scope correction, with its private row evidence retained for review.

## Questions for Ahmed

None.

## Reproduction and evidence

Run the scripts with D:\second-sun\.venv\Scripts\python.exe -I -B. Setup order is 025_prepare.py, the two 025_trace.py CAMPAIGN --roster-only calls, roster merge, baseline traces, 025_install.py, 025_score_prepare.py, the two injected traces, then 025_run.py. 025_report.py renders this completed report. Existing private outputs must be preserved when rerunning.

Private evidence lives under data/astra/025. It includes roster.json, candidate-spec.json, per-trial injected traces, generated raw-injection groups, combined score tables, background events, checks, source snapshots, verification.json, summary.json and terminal progress.json. The tracked worklog records the order of decisions and actual execution.

## Usage

Predicted 40 five-hour points and 8 weekly points, cap 50 five-hour points. Actual bars are unavailable in the headless runner. Lesson, distinguish best-product centre support, all-product search input and tier-1 recovery before naming a loss.

Next action is Claude reviewing this report to validate the cause accounting and candidate verdict. It uses Claude's review budget, with the amount unmeasured.
