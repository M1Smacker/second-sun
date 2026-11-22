# 031c: amendment to brief 031 (empty-span draws) and resume D1 (Claude, 22 Nov 2026, 10:58 pm; continuation of Ahmed's 9:30 pm go)

## Amendment (dated BEFORE any D1, B or N1 score on the new benches exists)
Codex 031b found 2 of the 2,000 new T156 draws (seed 2026112202, both G2, both in the 5 to 10 d bin) whose selected product loads no times; the original 003 bench never met this case and has no rule. **Rule, written now: a new-bench draw whose selected product loads no times is EXCLUDED from both B and D1 (and N1), exactly like a fresh-bench planet with no observed crossing. The new T156 draw is then 1,998 draws; the reference subset and its equal-bin R use the remaining draws.** Apply the same rule to the new fresh bench if it meets any such draw; report every exclusion by campaign and bin. Paired comparisons use the same draws on both sides, so the rule cannot favour either recipe. Nothing else in brief 031 changes.

## Task
1. Implement the exclusion in the records step only (smallest change), record old and new source hashes in the report, and resume `031_run.py` from its checkpoints (finished markers stay). 3 workers x NUMBA_NUM_THREADS=2; a detached supervisor with progress.json as before.
2. When the bench ends, finish the report as brief 031 asks (rules (a) to (g), duration bands, flags, per-crossing rate, the unscored-notch count from 031b, counts only).
If anything else stops the run, stop and report; do not invent rules.

Branch `astra/031c-duration-notch-resume`; data in `data/astra/031/`; usage in `research/astra/USAGE.md`.