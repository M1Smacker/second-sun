**Usage overrun:** final pre-commit meter 25% five-hour / 4% weekly, versus first reading 5% / 1%: +20 and +3 points. The 15-point task cap was exceeded during an oversized wrap-up. This is my error, not authorization to continue.

Model/effort verification: requested GPT-6 Astra medium; exact runtime model and effort were not exposed to this agent, so compliance is unverified.
# 001 Onboarding checkpoint (Codex, 12 Nov 2026, 23:22 Kuwait)

**Plain verdict:** Partial onboarding, not "I know the whole project". Three documentation issues and one execution hazard identified by static inspection. No science result re-derived.
**Branch:** astra/001-onboarding (one local delivery commit).
**Cap:** target 10 percentage points of five-hour usage, stop at 15. First available reading after initial instructions was 5% five-hour / 1% weekly; wrap-up began at 19% / 3%. Initial reading overhead is not captured by that delta.

## Findings
1. CONFIRMED documentation contradiction: AGENTS.md:3 calls the repository private; RESUME.md:6 and its following block say the repository is public and copied private memories must not be pushed. Live repository visibility NOT TESTED. Followed the no-push rule. Claude should reconcile the wording without publishing the memory copies.
2. CONFIRMED stale status: book/docs/versions.md:30 and research/stage3/VESPER-VERSIONS.md:16 still say 0.8.1 was not used for a search. book/docs/field-notes/2026-11-04.md:13 records the completed G3 search with that version. This is a documentation fix, not a reason to rerun G3.
3. CONFIRMED stale version definition: research/stage3/VESPER-VERSIONS.md:3 reserves 1.0.0 for sealed G2, but book/docs/versions.md:7 identifies Petrova 1.0.0 as the current filter and 0.8.0 as the sealed G2 version. Historical prose needs a superseded label.
4. CONFIRMED static execution hazard: pipeline/dataset.py:5 and pipeline/stage3_core.py:9 hard-code Claude's checkout as ROOT. Running from the helper worktree does not redirect those paths. I did not import or run the pipeline. Frozen code stays untouched; any later audit needs a separately authorized isolated harness.
5. CONFIRMED catalogue row counts from an independent standard-library CSV count: G1 unseen 552; G2 unseen 475, seen 420; G3 unseen 328, seen 284. Thus G2/G3 unseen total 803, design-seen total 704. G1's 549 unique-star count was not independently counted here. Rows and stars must not be conflated.

## Ten things that surprised me
These are observations about the inspected records, not new experimental findings.
1. The strongest audit lesson is about where fake dips enter the pipeline: after-mask tests cannot reveal losses caused by that mask.
2. Amendment 3 explicitly says even the newer raw-light injections choose times from kept light, so completeness remains conditional.
3. Recovered light is a union of old-mask removals on both orientations, not just the original flux (petrova_mask.py:206).
4. The final S1 question compares unseen stars with design stars inside period bins, rather than assuming equal real and flipped counts.
5. Failed exchangeability bins did not automatically prohibit the search; the amended rule required narrower verdict wording.
6. Tier 1B means no second product is available, not independent confirmation.
7. A veto generally demotes to tier 2 rather than deleting the stored event.
8. The legacy injection inside stage2_search.do_group still happens after prepare; it must not be mistaken for the newer gate harness.
9. A worktree alone does not isolate absolute runtime paths.
10. Older memories contain permissions to publish and update the book, but the Codex rules and this brief expressly restrict my work to three files.

## Five places I would audit first
This ranks reviews, not new builds or permission to run them.
1. r1_gate.install / _run_group: separate raw-flux insertion from selection of injection times. Measure what the conditional denominator excludes.
2. r1_readout.strat_exact / strat_block: independently reproduce amended S1 counts and probability calculation, then check bin coverage and correlated events without changing the filed verdict.
3. petrova_mask.mask_runs / veto_events: synthetic arm-swap checks and design-only injections, including recovered-light selection and cross-sector partner handling.
4. detect_v2.load / stage2_search.prepare: quality bits, product eras and missing-window denominators. Do not call a skipped product a successful test.
5. dataset and run guards: verify every effective path, manifest and dependency hash before executing helper experiments. Equality to a previous version proves compatibility, not scientific validity.

## What I did NOT check
The full brief is NOT complete. Required remaining work: reread truncated memory sections; finish the complete folder-by-folder inventory; read the full audit report and research registers; finish detailed C-check provenance and runner/readout source tracing; inspect book build/test implementation and full required field notes; obtain directory sizes safely. All 63 indexed memory files were opened by a read-only script, but tool output truncation prevented a complete model-level reading. Selected headings are not full reads.
No real light or event contents opened. No search, mask, injection, scientific runtime test, book build, live site, literature verification, remote visibility check, frozen-hash verification or independent review performed. Scientific numbers in the map are attributed to existing reports, not validated results.

## STOP SIGNS hit
Usage stop line approached. New investigation stopped at a measured +14 five-hour points; only checkpoint writing and validation followed. Exact task-start usage and runtime model/effort are unavailable.
A recursive directory-size metadata scan ran longer than the remaining budget and was interrupted using its own session. It produced no usable size totals. No file contents were opened by that scan. Two earlier read commands failed: Windows stdout encoding, then a CSV comment header. Both were corrected; neither failure counted as a successful check.
No known forbidden path access or frozen-file mutation. Source text contained forbidden path strings, which were read as code, not followed.

## QUEUE PROPOSALS
FIX: reconcile repository privacy wording in AGENTS.md with current RESUME.
FIX: mark obsolete 0.8.1 status and 1.0.0 naming definition superseded in version records.
BUILD: before executing brief 002 experiments, establish a helper-safe harness with explicit path checks; do not patch frozen files silently.
Claude files these after review, including checking for existing queue entries.

## IDEAS
None beyond the reviews requested by the brief.

## Disagreements with Claude
No scientific disagreement established. Documentation contradictions above have direct file evidence.

## Questions for Ahmed
None required for this checkpoint. Completing the scan needs a later authorized usage allocation because the brief's stop cap is binding.

## Usage
Predicted: 10% five-hour, weekly unknown. Observed at wrap-up start: 5% to 19% five-hour, 1% to 3% weekly. Final snapshot is in USAGE.md. Lesson: full memory dumps consume the cap and truncate; future reads should be small, numbered chunks with an explicit coverage checklist.

Next: Claude reviews this partial checkpoint before a continuation, to preserve the cap and resolve the documentation issues; review cost unmeasured, requires Claude.

## Continuation

Requested model: GPT-6 Sol, Medium. Runtime model/effort remains unverified by this agent. This continuation supersedes the earlier stop policy: the budget is at most 2 weekly points; the five-hour stop is near 80%. Branch switched to astra/001-onboarding and merged main: already up to date, initially clean. Claude's fixes and prior independent review are recorded in the latest RESUME; I did not rerun his fence checker.

### Coverage checklist
- [x] Current AGENTS.md, latest RESUME block, mailbox README and continuation instructions read. Auditor/mailbox skills retained from the first part of this chat.
- [x] Fable REPORT.md fully read: lines 1 to 45, then numbered lines 46 to 94. Its labels and estimates are historical findings, not my revalidation.
- [x] R1-PREREGISTRATION.md fully read in numbered chunks 1 to 59 and 60 to 78, including all three amendments.
- [x] MORNING-REPORT-2026-11-11.md fully read, numbered lines 1 to 59.
- [x] pipeline/r1_gate.py fully read, numbered lines 1 to 96 and 97 to 219.
- [x] pipeline/r1_readout.py fully read, numbered lines 1 to 114 and 115 to 175.
- [x] Four previously truncated memory files fully reread in small numbered chunks: feedback_verify_science_with_sources.md (1 to 15), feedback_always_say_whats_next.md (1 to 15), project_keystone_exam.md (1 to 12), feedback_learning_track_ui_preferences.md (1 to 12), all under research/astra/claude-memory/.
- [ ] Remaining skimmed memories not exhaustively reread. Stopped to reserve allowance for delivery. The continuation explicitly permits stopping near the cap.
- [ ] Directory sizes and complete inventory intentionally skipped as instructed.

### New contradictions and audit leads
1. **CONFIRMED path typo:** continuation item (3) names research/stage3/r1_gate.py and r1_readout.py; neither exists there. Both exist under pipeline and were read there. No scripts were imported or executed. QUEUE PROPOSAL, FIX: correct the brief's source paths.
2. **CONFIRMED static mismatch, scientific effect NOT TESTED:** pipeline/r1_readout.py:84 to 92 calculates the displayed "power" threshold using unstratified Fisher counts. main:141 to 144 attaches that line to the stratified Amendment 3 verdict and says only an excess of that size would have been seen. The function's own docstring acknowledges the unstratified test. It is a threshold calculation with fixed flipped counts, not a measured probability of detecting an alternative. Brief 002 should independently establish what that line can support before relying on the morning report's multiples. No replacement number or reinterpretation of the filed verdict is proposed here.
3. **CONFIRMED wording conflict:** MORNING-REPORT-2026-11-11.md:27 calls the surplus eclipse leftovers as fact; R1-PREREGISTRATION.md:62 calls that cause suspected and NOT TESTED. QUEUE PROPOSAL, FIX: retain the uncertainty in the narrative. This identifies a confidence-label inconsistency, not a finding about what generated the events.
4. **CONFIRMED static implementation difference, impact NOT TESTED:** preregistration:34 specifies a star-level S2 interval; Amendment 2:65 and :68 leave S2 unchanged. r1_readout.py:164 to 166 calls B.pois and explicitly labels its interval a floor because stars are correlated. Brief 002 should trace that helper and the saved results to establish the deviation's extent. Do not silently change the filed result.
5. **CONFIRMED static audit lead:** r1_gate.py:180 to 187 skips bins with no injections and accepts an undefined before/after ratio without turning the overall gate to FAIL. This does not prove a real run passed incorrectly. It makes coverage and denominators essential parts of the next review. Likewise _run_group:117 chooses injection times from prepared light; this agrees with Amendment 3's conditional-completeness warning.

### Readiness and limits
**Ready for brief 002: yes, to begin its scoped audit after Claude's review.** I can distinguish the original S1, Amendment 2 reference comparison and final stratified Amendment 3 rule; the PDCSAP-half S1 counts from whole-union totals; raw insertion from kept-time selection; and gate failure from the required not-covered wording. The primary audit targets are mapped. This is readiness to investigate, not validation of the pipeline or its statistics.
No brief 002 work started: no independent science calculations, real data reads, tests, experiments, code modifications, external research or verdict changes. The full original onboarding remains incomplete by design under the narrowed continuation. Other references and dependencies should be read only as the next audit needs them.
No new operational stop sign or forbidden path action. Existing pipeline absolute-path restriction respected. No disagreements with Claude's scientific decisions established; the source discrepancies above are for review. No new system ideas or questions for Ahmed.

Usage: baseline after instruction reading was 3% five-hour / 5% weekly; prediction 8 to 12 five-hour points and 1 weekly point, hard stop at 7% weekly. Final measured snapshot is in USAGE.md; bars are account-wide and rounded, not an exact task bill. Lesson: prioritize full reads of a few decision-bearing documents and reserve delivery headroom.

Next: Claude reviews this continuation and its audit leads before brief 002; review cost unmeasured, requires Claude.
