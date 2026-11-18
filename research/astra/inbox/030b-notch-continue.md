# 030b: continue Codex 030 after the TOI-1338 b gate (Claude, 18 Nov 2026, 1:17 pm; continuation of Ahmed's 11:28 am go)

## What happened
Codex 030 part 1 is merged (main). Claude resumed `030_run.py` after your session ended; it ran to completion of the alarm curves and the written rule chose **threshold 6.5** (`data/astra/030/chosen.json`: tier-1 untouched 165 real / 77 upside-down; 4.5 to 6 not eligible). Then `030_known.py` stopped on its own gate: "TOI-1338 B must reproduce six of thirteen".

## Cause (Claude's, CONFIRMED by a read-only count)
The design background holds TOI-1338 (TIC 260128333) in only sectors 10 and 93 (B: 1 tier-1 real event there). The "6 of 13" comes from the T109 known-planet path, which reads all 13 crossing sectors. So brief 030's rule (g) asked for a number this bench cannot produce. The fault is in Claude's brief, not in your script.

## Amendment to brief 030 (dated 18 Nov 2026, 1:17 pm, BEFORE any planet, fresh or T156 score is read)
- Rule (g) is measured on the **T109 path** (the same code and windows that gave B's 6 of 13), with N1 at the chosen threshold 6.5, as a separate step after the bench. Inside the bench, `030_known.py` reports the design-background counts for both B and N1 but does not assert 6.
- Nothing else changes: threshold 6.5 stays (already locked), rules (a) to (f) stay word for word, seeds stay.

## Task
1. Make the smallest change to `030_known.py` that implements the amendment (no assert on 6; record both counts and the note "design background holds 2 of 13 sectors"), update the source lock honestly (record old and new hashes in the report), and resume `030_run.py` from its checkpoints (`progress.json` is `failed` now; the completed markers stay).
2. Run the remaining phases (planets, fresh, T156, summary, verify) and `030_finish.py`, in the foreground, 3 workers x NUMBA_NUM_THREADS=2. Pre-create shared folders first (the 028 race).
3. Rule (g) on the T109 path: run TOI-1338 b with N1 at 6.5 the way T109/Q5 did for B (`research/stage3/t109/`, RS-025 Q5), report N1's tier-1 count of 13.
4. Report: every pass rule with its number and PASS or FAIL, flag counts for new detections, alarm curves, per-crossing rate. Counts only.
Branch `astra/030b-notch-continue`; data stays in `data/astra/030/`; usage prediction and actual in `research/astra/USAGE.md`.
