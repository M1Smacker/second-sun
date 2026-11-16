# X1: fresh-seed confirmation (Fable run, written up by Claude Opus at 2:31 pm, 16 Nov 2026)

**Verdict in one line: CONFIRMED. On a new planet bench (seed 2026111601, 1,250 new planets, same drawing rules, never used to choose anything), the proposal cap + R2 + M2 gains +3.94 points over B (95% +2.18 to +6.04) on planets that can exist, against +4.08 on the choosing bench. P = 56.1% (51.6 to 60.5). Every candidate passes the rule written before the run.** Still far from 0.75; the lower bound 51.6 is far under 0.65.

Rule (in `WORK-LOG-X1.md`, written 11:36 am before any fresh number): paired change against fresh B on planets that can exist, 95% interval above zero AND point estimate at least half the original-bench estimate.

| Candidate (all with depth cap) | Original bench | Fresh bench (95%) | Half of original | Verdict |
|---|---|---|---|---|
| DS | +1.79 | +1.22 (+0.55 to +1.97) | 0.90 | CONFIRMED |
| R2 | +2.61 | +1.75 (+0.94 to +2.66) | 1.31 | CONFIRMED |
| R1 | +4.55 | +2.74 (+1.71 to +3.86) | 2.28 | CONFIRMED (fails the real-alarm limit, X6) |
| DS + M2 | +3.26 | +3.41 (+1.71 to +5.46) | 1.63 | CONFIRMED |
| **R2 + M2 (proposal)** | **+4.08** | **+3.94 (+2.18 to +6.04)** | 2.04 | **CONFIRMED** |
| R1 + M2 | +5.92 | +5.24 (+3.20 to +7.58) | 2.96 | CONFIRMED (over both alarm limits) |

- Fresh B on possible planets: 52.18% (original 48.40): the new draw is easier by chance, which is why only paired changes are judged.
- The vetting releases shrink by about a third on fresh planets (winner's curse, as F0 predicted); the mask timing part does not shrink.
- Alarms are unchanged by the seed (same stars, same light): proposal 172 real / 66 upside-down against B's 174 / 79.
- On ALL fresh planets (bar's current definition, impossible planets included) the proposal reads -1.43 (-4.68 to +1.76): the depth cap again holds the 123 impossible planets. The bar-file decision (F1) still comes first.

Files: `data/fable/x1/` (draws, generator copies, `chain.sh`, `summary-x1.txt`, `summary-x1m.txt`), outputs under `D:\second-sun-astra\data\astra\fable-fresh` and `fable-fresh-m2`.
Not done: T156 and the known planets under the proposal; the leftover-eclipse check for M2 (F1 section 4).
