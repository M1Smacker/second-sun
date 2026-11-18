# 030d: finish Codex 030 (Claude, 18 Nov 2026, 4:23 pm; continuation of Ahmed's 11:28 am go)

## State
- 030c is merged into main (fence check CLEAN). Claude's resumed `030_run.py` finished every heavy phase at 4:18 pm: planets, fresh and T156 at threshold 6.5 are scored (`data/astra/030/planets-*-floor6.5.json`, `*-fresh-floor6.5.json`, `T156-*-floor6.5.json`, all `.complete.json` markers present).
- `030_summary.py` then stopped on its own assert, as designed: "Rule (g) requires the amended full T109-path result before a final verdict". `progress.json` is `failed` for that reason only.
- **Do not rerun any heavy phase.** Do not launch `030_run.py` from the start.

## Task
1. Rule (g) on the T109 path, per the 030b amendment: run TOI-1338 b (TIC 260128333) with N1 at 6.5 the same way T109 / RS-025 Q5 did for B (`research/stage3/t109/`), all 13 crossing sectors. First reproduce B's 6 of 13 on that path (if B does not give 6, stop and report). Write the N1 count and `pass` (N1 >= 6) into `data/astra/030/known.json`, keeping the design-background counts already there.
2. Run `030_summary.py`, then verify and `030_finish.py`. 3 workers x NUMBA_NUM_THREADS=2 for anything heavy.
3. Report in `research/astra/reports/030-report.md`: every rule (a) to (g) with its number and PASS or FAIL, new-event counts, per-bin dip-vs-bump control, T156 reference R for B and N1. Counts only.

## Fixed
Threshold 6.5, rules (a) to (g) word for word, seeds, benches: unchanged. Claude has written an independent recount of the benches; nothing may be adjusted to change any outcome. If a rule fails, report it as failed.

Branch `astra/030d-notch-finish`; data stays in `data/astra/030/`; usage prediction and actual in `research/astra/USAGE.md`.
