# 031 duration-aware notch D1, 031d resume checkpoint

Codex, runtime model and effort independently unverified; brief specifies neither. Updated 23 November 2026, 02:40 Kuwait, from the observed clock.

**Plain verdict: PARTIAL. The authorized empty-span exclusion is implemented and tested. The detached bench has resumed; no new scientific verdict is available.**

**Branch:** `astra/031d-duration-notch-resume`, as requested in chat. No branch switches, commits, git writes, pushes or publications. Tree nodes 1.3, 1.5 and 1.6. The existing `.codex_run.lock` was left untouched.

## Findings

1. **CONFIRMED: the amendment is implemented in the records step only.** `031_records.py` now counts and skips a new T156 draw when its selected product loads no times. It does not redraw or try another product. B, N1 and D1 read the same resulting records, so excluded draws cannot enter one recipe's denominator but not another's. This paired denominator is the engineering safeguard against favouring a recipe. No cut, threshold, seed, frozen source or scoring code changed.
2. **CONFIRMED: the focused runtime test failed before the patch and passed after it.** `audit_031c_records_checks.py` executes the actual T156 loop and fresh-record function extracted with Python AST, without importing the pipeline. Two synthetic empty spans in distinct bins are excluded; a nonempty draw retains its expected centre and paired preexisting flags; another campaign is ignored. Fresh tests cover empty times, nonempty times with no crossing, and an observed crossing. Disabling the exclusion causes the test to fail. Evidence: `data/astra/031/031c-records-checks.json`. This is a synthetic producer test, not a full real-light replay or independent review.
3. **CONFIRMED: fresh empty-time draws already follow the authorized exclusion path.** They produce `observed=[]`, just like a planet with no observed crossing. Existing layout, generation, scoring and summary logic omit these records from the measured population. Their records remain in the journal for accounting. The patch additionally reports all fresh unobserved exclusions by bin; it does not invent a new fresh sampling rule. The focused fresh test checks the records behavior; downstream omission was inspected statically.
4. **CONFIRMED: source lock updated honestly and checkpoints preserved.** Only `031_records.py` changed among locked `031*.py` sources. All 12 existing completion markers were retained. The completed G3 records were not rerun or rewritten. Before the update, the old source lock, failed progress, G2 terminal log and previous report were copied into private `data/astra/031/031c-before/`. Marker hashes and change provenance are in `031c-resume-provenance.json`.
5. **CONFIRMED at launch only: supervisor resumed.** Startup observed `status=running`, stage `fixed draw observability and historical replay validation`, supervisor PID 2732; the Windows launcher returned PID 11748. It started **23 November 2026, 02:40:08 Kuwait**, with expected finish **24 November 2026, 02:40:08 Kuwait**. This is the supervisor's conservative, unmeasured 24-hour allowance, not a measured completion forecast. Two Python processes existed before launch. The supervisor permits at most three worker subprocesses, each with `NUMBA_NUM_THREADS=2`, as requested. Logs: `supervisor-031d.log`, `supervisor-031d-error.log`; status: `progress.json`. No healthy-run logs were read or repeated progress checks made after startup.

## Exclusion accounting

The historical 031b raw-load audit found two empty new T156 draws, both G2 in the 5 to 10 day bin; G3 had zero. Those are prior measured inputs, not a newly completed amended-record count. Expected new T156 totals after this patch: G2 1,550, G3 448, total 1,998. The resumed records step must confirm them before a scientific verdict.

| Period bin (days) | G2 T156 empty spans, prior audit | G3 T156 empty spans, prior audit | G3 fresh unobserved exclusions, saved records |
|---|---:|---:|---:|
| 5 to 10 | 2 | 0 | 6 |
| 10 to 14 | 0 | 0 | 14 |
| 14 to 20 | 0 | 0 | 16 |
| 20 to 27.4 | 0 | 0 | 31 |
| 27.4 and above | 0 | 0 | 9 |
| Total | 2 | 0 | 76 |

The 76 G3 fresh exclusions were recounted from its completed 430 records, leaving 354 observable planets. They include every no-observed-crossing case; the subset caused specifically by empty loaded times was NOT separately measured. G2 fresh counts await its resumed records step. Evidence: `031b-span-audit.json`, `records/g3-complete.json`, `031c-resume-provenance.json`.

## Source hashes

| File | Old SHA256 | New SHA256 |
|---|---|---|
| `031_records.py` | `1fbe3918b1608816ce76bff51ab4607dd40d7948cf3e29ba6adb13b7df9254b0` | `27cfc9130df58a4597f65a178c8f3bdfd5b6416397e1af131ea8a75b9a6a9bf8` |
| `run-source-hashes.json` | `e6b201917023d674f44a1d78b1d8156fafdd81888e00dea9d35912d1f39c66de` | `cf0132e40c03608266edce5d94b832edacbf0e91652a9111ca41917920163759` |

Hash comparisons establish byte identity or change, not semantic correctness. The standalone test is outside the supervisor's `031*.py` lock. `git diff --check` passed before report close-out; Git emitted line-ending and inaccessible global-ignore warnings, which did not prevent the diff inspection.

## Scientific rules and remaining evidence

| Rule | Status at this handoff |
|---|---|
| (a) New fresh paired gain and interval | NOT TESTED here, bench pending |
| (b) D1 untouched background limits | NOT TESTED here |
| (c) D1 dip-against-bump control | NOT TESTED here |
| (d) Endpoint identity | Prior saved producer checks passed; not rerun here |
| (e) D1 new-event excess | NOT TESTED here |
| (f) New T156 R against paired B | NOT TESTED here, amended records and scoring pending |
| (g) D1 TOI-1338 b recovery | NOT TESTED here; prior B 6/13 check retained |

Earlier endpoint evidence, as recorded in the previous report: eight endpoint comparisons passed; B P 48.105 on 1,098, background 174/79 and old R 34.207; N1 background 165/77 and old R 31.653. These reuse saved pre-tier events and tier replay, with synthetic raw endpoint dispatch tests. They are not full raw endpoint replays. No new claim of independently verified identities is made.

After terminal completion, the requested final synthesis still needs rules (a) to (g), B/N1/D1 period and duration bands, holding flags, per-crossing rates, old and new T156 R, and amended exclusion totals. The additional 031b choosing-bench counts of crossings with no notch score for D1 and N1 remain **NOT TESTED**. Claude's A12 count must not substitute for that measurement. The current automatic report renderer does not include these supplementary counts or this resume provenance; final synthesis must retain them explicitly.

## What I did NOT check

No completed amended G2 real-data records, final 1,998-row reconciliation, new full science scores, final source invariance, terminal worker coverage, choosing-bench unscored-notch diagnostic, or independent review. No new raw replay of the original 2,000 T156 draws; prior 031b archive reconciliation remains historical. No frozen-file edits, fenced-star analysis, downloads, book changes or publication.

## STOP SIGNS hit

None newly encountered. The original 031b sampling-policy stop is resolved by amendment 031c; the previous usage stop cleared after reset. If any further run failure occurs, the existing supervisor records failure and stops; do not invent another rule. Handoff while the detached job runs follows AGENTS section 7, which permits ending the turn instead of polling.

## QUEUE PROPOSALS

None. The earlier request for an authorized empty-span rule is resolved by 031c.

## IDEAS

None outside the brief.

## Disagreements with Claude

None.

## Questions for Ahmed

None.

## Usage

Prediction logged before implementation: 35 five-hour / 6 weekly points. First observed meter after initial reads: 2% five-hour / 15% weekly. Pre-handoff meter: 12% / 17%, approximately +10 / +2 rounded account-wide points; weekly actual/predicted about 0.33 for this continuation only. Background compute and later final synthesis are not included. Lesson: test the authorized input exclusion without changing the scoring path, preserve checkpoints, and hand back rather than poll a multi-hour run.

Next: Claude resumes final synthesis after `progress.json` is terminal, to review the amended counts and complete the scientific report; Claude required, continuation usage unmeasured.
