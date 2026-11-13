# Brief 005: new baseline, then three studies, each with its own full report and one combined summary

**From:** Claude, 13 Nov 2026, after Ahmed's question round on your brief 004. **Branch:** `astra/005-three-diagnoses` (made from main at dab2b74: your 004 work is merged).
**Ahmed's decisions:** the binary-locked repeater (004 rule b) is **adopted** for the next Petrova version, with its real-side rise tracked as a known cost; FIX 91 is adopted too (it passed alone); **no freeze yet** (keep improving; one freeze later with a combined bench run and an outside audit). Next work: **all three studies below, each with its own full report, plus one combined report.**
**Model:** Sol, as in 004 (Ahmed sets it; say which one you are on). If a part needs harder judgement, say so in the report rather than switching.
**Writes allowed:** `research/astra/reports/005-*.md`, `research/astra/scripts/005_*.py`, harness copies in a new `research/astra/scripts/harness/sprint005` (note every change), `data\astra\005\`, `research/astra/USAGE.md`. Never edit `pipeline/`. Design-seen stars only; fences as in AGENTS.md; no star ids, times or depths of real events in any report.
**Budget:** 20 weekly points of your bar in total (part 0: 1, part A: 4, part B: 7, part C: 6, combined report: 2). Saved-data replay first everywhere; new detection runs only where a part needs them, predeclared in the report and committed before they run.
**Run mode:** one working session, commit after each part, stop only at a stop sign, the total cap, or the five-hour bar near 90% (then write RESUME HERE at the top of the combined report so "continue" resumes exactly there). A part that hits its own cap: write what is left and move on to the next part.

## Part 0: the new baseline (saved-event replay, cheap)
Replay the 2,000 T156 trials and the un-injected design groups with BOTH adopted changes together (binary-locked repeater plus symmetric FIX 91), as you did in 004. Report the combined reference R with its star-cluster interval, background real and upside-down tier-1 counts, and the paired per-bin dip and bump test, against Petrova 1.0.0 and against each change alone. **This combined configuration is the baseline for parts B and C.** If the combined run fails any of the three 004 acceptance conditions, stop that line and report it (a stop sign).
Report: `reports/005-0-baseline.md`.

## Part A: what are the 53 extra real-side events? (Tree node 1.1, the tracked cost)
The repeater change raised background real tier-1 events on normal design data from 123 to 176 (+53) and upside-down from 70 to 85 (+15). From saved data only:
- Where do the extra real events sit against the binary's own orbit (phase distance from primary and secondary eclipse, using the catalogue period and epoch the chain already uses)? Compare with the extra upside-down events and with the old tier-1 events.
- How many stars carry them (clustered on a few stars or spread out), which products and eras, what depths and durations relative to the eclipse depth and width?
- Do they repeat at a period near a simple fraction or multiple of the binary period (half, twice), which the 1-hour binary lock would miss?
- Your reading, labelled CONFIRMED / LIKELY / UNCERTAIN: binary leftovers, instrument, or unexplained. If a physical cause is LIKELY and a narrower lock would catch it, write that as a **candidate for a later bench run**, not a change now.
Report: `reports/005-A-real-side-rise.md` (counts and bins only).

## Part B: the 5 to 10 day blind spot (Tree node 1.5, T161)
In 003, 19 of 48 Saturn-like test planets in that bin gave no event at all (40%, against 13% elsewhere). Find out why:
1. **Predeclare first (commit before running):** which stage-level measurements you will save, on which trials (all 400 trials of the 5 to 10 d bin, plus a matched sample of 400 from the 20 to 27.4 d bin as the comparison), and what each would show. Suggested: the transit depth kept after detrending, the best-box SNR before the 7 bar, whether the event was merged into a neighbour, how far the found centre shifted, and the binary's own variability around the transit (the scatter of the detrended light, and how much eclipse residual remains).
2. Rerun detection with that instrumentation on the same frozen draws (new runs on design data are allowed here; the progress file goes in `data\astra\005\`).
3. Explain the loss with numbers, and only then propose at most two candidate changes (for example a different detrending treatment for short binaries), each predeclared with the 004 acceptance rule. If one is cheap to bench on the same draws, bench it against the part 0 baseline and report PASS or FAIL per condition. No threshold tuned from outcomes.
Report: `reports/005-B-short-period-blind-spot.md`.

## Part C: the windows (Tree node 1.2, T155, FIX 26 and 70)
In 003, 45 of 222 Saturn-like test planets fell outside every searched window or in a gap, and 7 had no safe windows (52, about 23%). Find the recoverable part:
1. From saved traces, split the 52 into: true gaps (no recorded data at that time), data that exists but sits outside the safe windows, and files with no safe windows (QLP neighbour rule, `stage2_search.py` 150 to 160).
2. For the part with real data outside the windows: why was it excluded (momentum dump, scattered light, quality flags, too few neighbours)? Which exclusions protect against false alarms and which only lose light?
3. Predeclare at most two coverage-repair candidates (for example a QLP-only star-sector that can use its own quality flags when neighbours are missing), each with the 004 acceptance rule, and bench the cheaper one against the part 0 baseline if it fits the cap. Never loosen a safety rule just to recover injections; every candidate must be justified by what the excluded light really is.
Report: `reports/005-C-windows.md`.

## Combined report
`reports/005-combined.md`: verdict lines first (one per part, plain words), then the new baseline R, what each part found, any candidates that PASSED or FAILED on the bench, bugs found (each with its Tree node), and your ranked next steps toward the 50% G1 bar, with an honest estimate of how far the remaining nodes can take us. Your final message to Ahmed: the verdict lines in a few short lines.
