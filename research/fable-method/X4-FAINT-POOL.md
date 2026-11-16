# X4: the "too faint" pool (Fable run, written up by Claude Opus, 2:50 pm, 16 Nov 2026)

**Verdict in one line: found something worth a bench. The too-faint pool is mostly slow wiggles that the frozen 2-day detrending leaves in, not photon noise. The pipeline's own study switch c1a (detrending window 3 x box length, at least 0.5 d) raises planets with a crossing at SNR 7+ from 64.1% to 71.3% (+7.2 points of detection, before vetting), most of all in 5 to 10 day binaries (54% to 70%). But strong events on untouched light rise about 1.6 times on BOTH arms, so it only counts if the tier rules hold those back. Detector level only: NOT yet a P number.**

## Ceiling (CONFIRMED as computed, `data/fable/f2/x4_faint.py`, `x4_summary.py`)
- 4,220 scored planted crossings: SNR 7+ 62.7%, 5 to 7 10.0%, under 5 27.3%.
- Crossings under SNR 7: search noise is 2.59 times what bin-to-bin scatter predicts (1.54 for the ones at 7+); depth kept median 0.76.
- Planets with some crossing at SNR 7+ (equal weight per bin): today 64.1; white-noise bound 78.9; full-depth bound 71.5; both 83.5.

## Prototype: switch c1a against the frozen window (CONFIRMED as computed, `x4_proto.py`, `x4_proto_summary.py`)
| | Frozen (2-day window) | c1a |
|---|---|---|
| Planted crossings at SNR 7+ | 62.7% | 78.3% (690 gained, 29 lost; median SNR x 1.39) |
| Planets with a crossing at 7+ | 64.1% | 71.3% |
| Per bin (5-10, 10-14, 14-20, 20-27.4, 27.4+ d) | 54, 60, 58, 71, 78 | 70, 64, 68, 74, 80 |
| SNR 7+ events on untouched light, per 100 days, real / upside-down | 1.96 / 1.44 | 3.07 / 2.38 |

## Reading
- This is the biggest single lever measured in the whole run, and it hits the named blind spot (short binaries) hardest.
- The cost rises on both arms together (real x 1.57, upside-down x 1.65), so the upside-down meter sees it fully: a fair test is possible.
- Next step (not done): tier-level bench of c1a on the planet bench and untouched background, with the X10 proposal, under the F1 section 5 rule. Expect most of the new events to be caught by step, ramp and dominated flags, but that is NOT TESTED. c1a is a study switch, so it is a new Petrova version, not a fix.
