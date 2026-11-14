# RS-030: why Codex 012's eclipse-time fits fail the catalogue controls (Claude Opus 5.5 high, 14 Nov 2026, 9:27 pm Kuwait)

**Question (decision it feeds):** Codex 012's fitted TESS periods agree with the catalogue for only 28 of 60 control stars (54 needed). Is the timing method wrong, or something narrower? This decides what Fable's FIX 94 design round on Monday must fix. Cap written first: 0.5 weekly points, about 8 tool calls. Own data only (Codex's private rows, data/astra/012/ephemerides.csv in the astra worktree).

## Findings
### 1. The main failure is the half-period alias. CONFIRMED (Codex's rows, counted by Claude)
Of 60 control primary tracks, 58 have a fitted period. **13 of the 58 locked onto half the catalogue period (alias 0.5), and 0 of those 13 agree.** With near-equal primary and secondary eclipses, a box search at P/2 stacks both eclipses and wins. Codex's discovery table shows the same in the affected sample (18 half-period, 15 double-period, 10 no discovery out of 112).
### 2. On the right period the timing is good. CONFIRMED
45 control fits sit on the catalogue period: **38 of 45 agree within 0.001 d**, 33 of 45 within 3 combined sigma; median |difference| 0.00006 d, 90th percentile 0.0014 d. Median reduced chi-square 0.1, so the fitted errors look too LARGE, not too small (UNCERTAIN why; the error floor of a quarter cadence is a likely cause).
### 3. The remaining 12 of 45 outside 3 sigma: NOT TESTED
The catalogue errors are formal fits to sectors 1 to 26 (median 0.000035 d); extrapolated over 6 years they may be understated, or these stars may have real timing drifts. Codex itself says the catalogue is a check, not truth.

## What it changes (for Fable's FIX 94 round, Mon 16 Nov)
1. The fit method is close; the missing piece is **alias resolution**: when the half-period band wins, compare odd and even eclipse depths (and the catalogue's secondary phase) before accepting P/2; prefer the catalogue band when it has support in three or more cycles. Rough upper bound from the counts: up to about 51 of 60 controls (38 within 0.001 d plus up to 13 recovered aliases) if alias resolution works, near the 54 needed. NOT TESTED.
2. The validation should also report agreement in days (for example within a quarter eclipse width), beside the strict sigma test, since the catalogue's errors are themselves uncertain.
3. The deep events Codex 011 let through line up with Codex's flagged tracks (18 of 21 V1, 14 of 18 V2): this supports RS-027 (wrong catalogue times), and no change is made on it until a validated method exists.
Codex 012 report: `D:\second-sun-astra\research\astra\reports\012-own-eclipse-ephemerides.md` (branch astra/012-own-ephemerides, fence check: frozen files 0, fence ids 0).
