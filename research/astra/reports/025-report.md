**Found something. The 21 load losses and 16 usable-before-window losses are traced. Full candidate scoring is pending.**

# 025 Load losses, partial handoff

Codex runtime model and effort are independently unverified. The brief specifies neither.
Written 2026-11-15 23:43 Kuwait. Branch astra/025-load-losses. Tree node 1.2.

The requested report filename and prohibition on git writes take precedence over the older brief. The runner handles the commit. The pre-existing runner lock is preserved.

## CONFIRMED causes

The 005 roster reproduces exactly. Of 52 fixed reference-window losses, 21 lack loaded centre support, 15 have no recorded cadence near the centre, ten lie outside safe windows, and six lack safe windows. Twenty load cases have finite archived flux. The remaining case also lacks finite archived flux.

| Blocking bits across nearby finite samples, or archived-flux limitation | Load cases |
|---|---:|
| 4096 | 14 |
| 128+4096 | 1 |
| 128 | 1 |
| 1073741824 | 3 |
| nonfinite archived flux | 1 |
| 2048+1073741824 | 1 |

The blocking-bit entries are unions across nearby samples. detect_v2.load(), pipeline/detect_v2.py line 44, calls Lightkurve with the hard quality mask. The installed QLP reader adds its low-precision mask. Individual sample counts, quality words, files and exact source conditions are in data/astra/025/case-evidence.json. The private roster carries the predeclared hypothesis checklist for each original case.

Bit 4096 is labelled Straylight2 by Lightkurve for SPOC-family files. QLP uses it for low precision before sector 56 and adds bit 1073741824 from sector 56. Bit 128 is manual exclusion, and bit 2048 is stray light. The installed reader and actual returned timestamps supply the evidence.

Zero of the 21 has a whole-sector FIX 101 mask. One also lacks safe windows. Three have another product with centre support after masking. Those three demonstrate that a best-product support loss can coexist with alternate search input. Recovery through detection and vetting is still pending.

| Rule removing the 16 usable cases | Cases | Source condition |
|---|---:|---|
| Own SPOC support | 3 | stage2_search.py line 154 |
| Neighbour intersection | 5 | stage2_search.py line 156 |
| Half-day start trim | 2 | detect_v2.py line 111 |
| Fewer than two neighbours and no own SPOC | 6 | stage2_search.py line 158 |

These branches implement the recorded comments. One of the 16 has usable alternate-product support. Safety of widening their intervals remains NOT TESTED.

## Across all 2,000 fixed T156 draws

The dip is planted before eclipse masking in the final trace. First-loss accounting assigns each draw to its earliest classified support loss, preventing double counting of overlapping causes.

| First classified loss or retained input | Draws |
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

Missing selected files and missing manifest entries are both zero. FITS header sectors have zero mismatches over 4,613 traced trial/product rows. Every inspected header uses BJDREFI 2457000 and TIMESYS TDB. The full injected trace gives 94 drift-window first losses. Drift covers a selected product's complete retained sector in 64 draws. This supplies new T156 evidence for the existing FIX 101 work. It supplies zero whole-sector cases among the original 21 load losses.

RS-038's separate 006 replay counts are cited as supplied, with no recount. Its 1,292 never-scored crossings comprise 526 mask, 248 no-finite-score, 235 safe-window, 192 best-product-table gaps, 60 capture mismatches and 31 load cases. [RS-038](../../stage3/rs038/KEEP-PLANETS-THROUGH-VETTING-2026-11-15.md)

## Candidate and tests completed

The predeclared bench prototype admits quality bit 4096 in the primary and SAP/PDC loaders. It retains the other blocking bits and existing borrowed windows. No frozen pipeline file is edited. The candidate specification was saved before its outcomes. The proposed bench change is research/astra/scripts/025-loader-prototype.patch.

CONFIRMED. 15 archived 4096 cases fail loaded centre support before the change, pass after it, and fail again under the reverted-policy mutation. This measures loaded support. Searched support still requires windows and masking.

CONFIRMED on constructed light. Three wrong-epoch deep-eclipse controls, at 30-minute, 10-minute and 200-second sampling, become detected events when the quality bit is admitted. Both campaign workers reproduce this hazard. It demonstrates why recovery alone cannot establish safety.

Runtime checks exercise 12 distinct product/era/median-cadence paths. The actual-quality audit covers 22 file/path instances. In two tested QLP files from sector 94 onward, 9,755 returned cadences retain bit 536870912. Four tested SPOC-family files retain 871 cadences with bit 32768. The physical meaning and safety of the QLP high bit remain UNCERTAIN here.

Thirteen inherited rule/access checks pass, including a rejected dump-shape mutation. The Petrova synthetic mask self-test passes. The guard verifies twelve copied source hashes, three denied access events and one permitted output write. Final static checks parse 29 Python sources and confirm twelve frozen source byte identities, zero target-identifier matches in the new payload, and zero authored trailing-whitespace lines. Git diff --check completes with an LF-to-CRLF advisory on USAGE.md. This is producer verification. Independent review and the running bench verdict remain pending.

## Pending deliverables

NOT TESTED TO COMPLETION. The two-worker candidate generation and scoring run remains active after the authorized terminal waits. Its complete T156 R, planet P, both untouched-background arms, restored searched-centre count and 50-sector event identity are pending. No adoption verdict is supported yet. Its progress.json records the launch time and a three-hour planning estimate. Machine outputs and logs remain under data/astra/025.

The acceptance rule requires at least 11 of the original 21 cases to gain searched centre support, higher T156 reference R, no extra upside-down tier-1 background and exact identity on 50 unaffected star-sectors. The fixed 006 planet P must also be measured. No setting will be changed from these outcomes.

After terminal completion, 025_report.py renders the full report from summary.json and verification.json. 025_run.py is the existing bench entry point. It includes fresh generation, historical baseline scoring, candidate scoring, summary and verification. The worklog records execution order and the supplementary injection-before-mask trace.

## What I did NOT check

- Completed R/P/background/identity acceptance results. The run is still active.
- SPOC 20-second data, absent from this fixed trace.
- A drift-cap prototype, conditional on FIX 101 explaining the original 21 load losses.
- Safety of relaxing other bits or widening the 16 windows.
- G1 or fence-B light, sealed searches, independent scientific review, publication, or complete runner-log fence review.
- Actual usage-panel percentages, unavailable in the headless runner.

## STOP SIGNS hit

No scientific adoption decision is made from an incomplete bench. The two capped terminal waits allowed by AGENTS are exhausted. The background job continues. Frozen files and sealed results received no edits or reinterpretation.

## QUEUE PROPOSALS

Node 1.2. Attach the cause table to the existing load/window and FIX 101 work. Hold any adoption decision until the requested bench gates are measured.

## IDEAS

None beyond the requested prototype.

## Disagreements with Claude

The original 21 label is best-product centre support. Three cases retain alternate-product search input. The private case rows support this scope correction.

## Questions for Ahmed

None.

## Usage

Predicted 40 five-hour points and 8 weekly points, cap 50 five-hour points. Actual bars are unavailable in the headless runner. AS-025 quality-policy provenance used installed primary source and runtime data, with a cap of two local calls and zero web calls. Lesson, keep loaded support, searched support and tier-1 recovery separate.

Next action is Claude running 025_report.py after progress.json reaches complete, to render the verified bench verdict. This uses one local command, with model usage unmeasured.
