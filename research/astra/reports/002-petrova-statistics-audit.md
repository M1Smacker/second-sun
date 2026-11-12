# 002 Petrova statistics audit, Part 0 (GPT-6.1 Sol, effort unverified, 13 Nov 2026, 00:01 Kuwait)

**Plain verdict:** Guarded harness built and smoke-tested. The three design-seen star-sector replay is blocked by the shared audit inputs. Part 0 is partial.
**Branch:** astra/002-petrova-audit. Source base c173b11c70b18d5bde81565d26157d80503af8e9.
**Handling note:** A source diagnostic surfaced pre-existing identifiers in its tool output while locating the copied lines. The staged payload omits those identifiers. No event file or light curve was opened.

## Bugs found
- **CONFIRMED, high severity for fence isolation.** pipeline/stage2_search.py:110 to 133 initializes burst state from the campaign-wide audit event table and may open a reference FITS chosen without a design-seen restriction. This is a blocker for a faithful helper replay under the current authorization. It does not establish a scientific error in the production run. The checks below cover source, manifest selection and access refusal. Production behavior was not run.

## Part 0
1. **CONFIRMED, source provenance.** Copied the 12 pinned modules for masking, detection, SAP, tiering and the readout. scripts/harness/provenance.json records every original Git blob and the frozen and copied SHA-256 values. The comparison reconstructed the frozen bytes from the Git blobs: nine LF, three CRLF. All 12 matched. See [the source diff](002-part0-source-diff.md). Alongside path edits, the copies remove an identifier from a comment and empty the control table used by the unused legacy G1 selector. The original files remain unchanged. These are byte and source checks.
2. **CONFIRMED, limited runtime check.** From the helper root, run the approved project venv interpreter with arguments `-I -B research/astra/scripts/002_harness.py`. It prints the configured paths, verifies the copies, and runs Petrova's existing synthetic self-test. Actual output: `petrova_mask selftest passed` and `Verified 12 copied source hashes, 3 rejected access events and one allowed write.` The probes exercise Python audit events for a write outside the output directory, a G1 input and the mixed G2 audit table. A real probe file was written and read back inside data/astra/002. This checks the guarded entry point for ordinary Python file operations. It is not an OS sandbox or a guarantee for direct module execution, native extensions or future multiprocessing. Later runners must enter the guard before loading copies and validate worker startup separately.
3. **CONFIRMED, manifest selection.** A standard-library CSV check reproduced the deduplicate-file then first-SPOC-per-sector selection in stage2_search.py:112 to 116 using filenames and the design-seen catalogue. G2 returned 52 selected references on the design list and 56 outside it. G3 returned 56 on the design list and zero outside. These are sector reference counts, not event counts. Even choosing G3 leaves the separate mixed burst-table dependency at lines 117 to 122. No FITS was opened.
4. **NOT TESTED, zero difference.** Ran zero of the requested three star-sector replays. The guard rejects the campaign-wide audit event table. Dropping the burst state or taking its answers from the stored target groups would not independently verify identical events. No selection of three star-sectors or comparison with stored results was performed.

## What I did NOT check
Real-light parity, full-chain runtime behavior, inputs for additional parts, or any scientific result. No later part started.

## STOP SIGNS hit
The brief permits design-seen light and excludes hold-out events. The default initializer is not fenced by star. A faithful replay needs a Claude-provided fence-safe fixture or adapter that supplies the original burst and momentum-dump context for three approved groups without exposing fenced event records or light. The current guard deliberately blocks that mixed input.

## QUEUE PROPOSALS
BUILD: prepare the three-group replay fixture or adapter, with a documented provenance check and the exact context needed for the event comparison.

## IDEAS
None beyond the replay fixture.

## Disagreements with Claude
None established. The parity requirement remains open.

## Questions for Ahmed
None. Claude can resolve the input dependency.

## Usage
Prediction 10 to 15 five-hour points and 1 to 2 weekly points. Meter baseline 21% five-hour and 8% weekly. See USAGE.md for the final pre-commit reading. Lesson: inspect mixed reference inputs before budgeting a replay.

Next: Claude provides a fence-safe replay fixture so the three-group identity check can run. Setup cost unmeasured, requires Claude.
