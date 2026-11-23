# 033: D2 = depth cap (FIX 96) plus a detection threshold set by the alarm budget, tier-level bench

Written by Claude, 23 Nov 2026, 10:55 am Kuwait, **before any D1 (031) result exists**. GO: Ahmed, 22 Nov 9:30 pm and 23 Nov 10:43 am. This file is the preregistration. **Launch only after the 031 bench has finished** (it uses the same benches and machine).

## Why
FIX 96 / Codex 014 part 3: a per-star depth cap at a 2 Jupiter-radius planet on the most generous host radius (smallest of TIC header, TIC 8.2, Gaia DR3 GSP-Phot, FLAME; `research/stage3/fix96/FIX96-RADIUS-CHECK-2026-11-15.md`) holds 50 of 174 real and 26 of 79 upside-down untouched tier-1 background events and loses 0 of 264 planted deep dips. That frees alarm budget. D2 spends it on a lower detection threshold, by a rule fixed here.

## Base
- If 031 PASSES all seven rules: base = D1 (notch for boxes <= 8 h, frozen B above). The threshold that moves is the notch's (6.5); B's 7 stays.
- If 031 FAILS any rule: base = frozen B; the threshold that moves is B's 7.
Either way the base itself is not changed in any other way.

## The design (fixed now)
1. **Cap:** the FIX 96 cap, both arms, applied to tier-1 candidates exactly as Codex 014 part 3 priced it (event depth above the cap's depth on that star = held, not tier 1). Stars with no usable radius: no cap.
2. **Threshold ladder:** the moving threshold takes the values (notch) 6.5, 6.25, 6.0, 5.75, 5.5 or (B) 7.0, 6.75, 6.5, 6.25, 6.0, in that order.
3. **Alarm-budget rule (chooses the threshold, on background only):** on the untouched design-star background of the choosing bench (both arms, after the cap), pick the LOWEST ladder value at which untouched tier-1 background is at most 174 real AND at most 79 upside-down. Planet benches are not looked at for this choice. If even the top value exceeds the budget, D2 = base plus cap at the base threshold.
4. **One-neighbour windows (A14 nn1), counted, not adopted:** report on the new fresh bench how many extra QLP crossings and extra background events the A14 nn1 window rule would add under D2. Exploratory only.

## Benches and pass rules
- Identity (rule d): cap disabled and threshold at the base value reproduces the base exactly (B: P 48.404 on 968, 174 / 79; or D1's own 031 numbers).
- **NEW fresh bench seed 2026112401** (1,250 draws, 006 draw code, same possible-planet rule) and **NEW T156 draw seed 2026112402** (2,000; empty-span draws excluded from both sides as in 031c); TOI-1338 b on the T109 path; untouched background both arms.
- F1 rules (a) to (g) word for word as in brief 031, against frozen B on the NEW benches. Also report D2 against the base (if base is D1) as exploratory.
- Report: the chosen threshold and the full ladder table of untouched background (real, upside-down) per value, P per bin and per duration band, which flags hold D2's new detections, how many held events the cap removes on each bench.

## Rules
Never edit frozen files; bench copy plus study switches; design stars and planted light only; counts only; 3 workers x NUMBA_NUM_THREADS=2 (2 workers if 032 is still running); checkpoints; data in `data/astra/033/`; branch `astra/033-d2-cap-budget`. Meter before and after, logged in `research/astra/USAGE.md`. Claude recounts independently before any merge. Nothing is tuned after a result.
