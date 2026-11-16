# X10: the combined candidate for Petrova 1.1 (Fable, 16 Nov 2026; bench copy, a proposal, nothing frozen)

**Verdict in one line: the best combination that stays under B's alarm counts on BOTH arms is: depth cap (FIX 96) + release rule R2 (dump hold by shape, gap-edge hold released) + mask timing M2. On planets that can exist it reaches P 52.5% (95% 47.8 to 56.9), +4.1 points over B (+2.7 to +5.6), with 172 real / 66 upside-down alarms against B's 174 / 79. That is the Petrova 1.1 proposal number on the choosing bench. It is 22.5 points short of the 0.75 bar and its lower bound (47.8) is far under 0.65. The fresh-seed check of its parts is in `X1-FRESH-SEED.md`.**

## The table (CONFIRMED as computed)
Scorer: the F4 and X6 copy of Codex 023's scorer, now also run in mask mode M2 on Codex 010's replays (`data/fable/f4/x10_prepare.py`, `x10_score.py`, `x10_summary.py`). Checks that could have failed: the M2 rows reproduce 023 exactly (B + cap + M2: 44.80% on the full bench, 139 / 56; B + cap + DS + M2: 46.49%, 156 / 59), and the no-M2 rows keep the trial-by-trial identity with the saved B and DS outcomes.

Planets that can exist (968). Change is paired against B, whole-star bootstrap.

| Combination (all with the depth cap) | P % | Change against B (95%) | Real | Upside-down | Under 174 / 79? |
|---|---|---|---|---|---|
| B today (no cap) | 48.40 | | 174 | 79 | |
| cap + DS | 50.20 | +1.79 (+0.95 to +2.73) | 143 | 56 | yes |
| cap + R2 | 51.02 | +2.61 (+1.60 to +3.71) | 158 | 63 | yes |
| cap + R1 | 52.95 | +4.55 (+3.19 to +6.03) | 193 | 78 | real over |
| cap + M2 | 49.76 | +1.36 (+0.43 to +2.44) | 139 | 56 | yes |
| cap + DS + M2 (F1's candidate) | 51.67 | +3.26 (+2.01 to +4.66) | 156 | 59 | yes |
| **cap + R2 + M2** | **52.49** | **+4.08 (+2.71 to +5.56)** | **172** | **66** | **yes, real by 2** |
| cap + R1 + M2 | 54.33 | +5.92 (+4.32 to +7.65) | 211 | 82 | both over |
| cap + R3 + M2 | 54.55 | +6.14 (+4.52 to +7.86) | 215 | 82 | both over |

On the bar's own bench of 1,098 the proposal reads 47.2% (change -0.9, interval -3.5 to +1.5), because 130 of those test planets cannot exist and the depth cap holds them (F1 section 1). Under today's bar file the proposal is therefore "no better than B"; under a physical bar file it is +4.1. That is why the bar file is the first decision.

Per binary-period bin (possible planets, B to proposal, % of planets found): 5 to 10 d 41 to 43; 10 to 14 d 44 to 47; 14 to 20 d 43 to 47; 20 to 27.4 d 50 to 54; over 27.4 d 64 to 71. No bin loses; the short binaries gain least.

## What is in and what is out
- **In:** depth cap; R2; M2.
- **Out by price:** the ramp release (R1): +1.9 more points but real alarms 211 and upside-down 82, over both limits once M2 is on. Step and dominated (F4).
- **Out as untested or failed:** binary-light subtraction (Codex 024, failed its rule); scattered-light bit (F2: admitted light is about 8 times dirtier); one-neighbour QLP windows (F2: clean at detector level, tier bench not run; expected +0.1 to +0.6 point).
- **Slot left open:** FIX 101 is the same code line as M2 (F1 section 4), so it adds nothing on top of M2 unless Codex 026 finds stars that 010's list missed.

## Conditions before anyone calls this 1.1 (unchanged from F1 section 5)
1. Fresh-seed bench: the gain must hold on new planets (`X1-FRESH-SEED.md` covers the parts without M2 today).
2. M2 needs its leftover-eclipse check (F1 section 4): 14 of its 24 new real events are eclipses the catalogue cannot place.
3. The real-alarm margin is 2 events (172 against 174): any added lever breaks it.
4. Zero-planet identity, T156 on possible planets, and the known planets (TOI-1338 b) under the frozen copy.

## Honest size
+4.1 points is the sum of everything measured today that passes on both arms. With the ramp release (Ahmed's call, real alarms up by 37) it would be +5.9. Neither is near 0.75. The remaining distance is the "too faint" pool (22 points in RS-037) and the crossings lost before the search (F2: ceiling 9.7 points, of which the mask part is already inside M2).
