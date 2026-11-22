# 031b: continue Codex 031 (D1) after the new-T156 records stop (Claude, 22 Nov 2026, 10:50 pm; continuation of Ahmed's 9:30 pm go)

## State
- 031 part 1 is merged into main (116ebb82; fence check: 0 fence ids, 0 frozen files). Draws reproduced, endpoint identities passed (identity-progress.json complete 9:53 pm).
- Your detached supervisor `031_run.py` stopped at 10:45 pm: `031_records.py g2` hit its own assert "Empty raw span in new T156 draw" (line 109). g3 records completed. `progress.json` is `failed` for that reason only.

## Task
1. Find how the ORIGINAL T156 bench (Codex 003, the draws `023_inputs.t156_rows` reads) handled a draw whose chosen star-sector product has no usable time span (skip and redraw, other product, or excluded from the 2,000). Read 003's code and its saved results; do not guess.
2. Apply exactly that rule to the new T156 draw (seed 2026112202), so the new draw follows the same law as the old one. Report how many new draws it affects per campaign and what happened to them. If 003 had no such case and no rule exists, stop and report the count; do not invent a rule.
3. Re-check that the old T156 records still reproduce, update the source lock honestly (old and new hashes in the report), and resume `031_run.py` from its checkpoints; finished markers stay. Same 3 workers x NUMBA_NUM_THREADS=2. A detached supervisor is fine (it survived your session last time); write progress.json as before.
4. When the bench ends, finish the report exactly as brief 031 asks (rules (a) to (g), duration bands, flags, per-crossing rate, counts only).

## Fixed
Everything in brief 031: the 8 h cut, thresholds 6.5 and 7, seeds, benches, pass rules. Nothing may be adjusted to change an outcome.

## Also report (new, Claude's finding tonight)
For D1 and N1 on the choosing bench: how many planted crossings have NO notch score (a flank without enough data) and are therefore never detected by the short-box path. Counts only. (Claude's detection-level test A12 found 110 of 1,427 crossings, 7.7%, unscored by the notch.)

Branch `astra/031b-duration-notch-continue`; data stays in `data/astra/031/`; usage in `research/astra/USAGE.md`.
