# 031: duration-aware notch D1 (notch for short boxes, frozen box for long boxes), tier-level bench

Written by Claude, 22 Nov 2026, 9:35 pm Kuwait. **GO: Ahmed, 22 Nov 2026, 9:30 pm ("Go ... I hereby give you every permission required").** This file is the preregistration: it is committed before any D1 number exists. Background: `research/astra/reports/030-report.md` (your 030), `research/stage3/rs039/RECOUNT-030-2026-11-18.md` (Claude's recount), `data/rs039/t156_breakdown_030.txt`.

## Why
030's N1 (lower-flank notch at 6.5) passed six rules and failed (f): T156 reference R 34.207 to 31.653. Exploratory breakdown on all 2,000 T156 planets: N1 gains on 3 to 6 h (+0.023) and 6 to 9 h (+0.013) dips, loses on 9 to 12 h (-0.039) and 12 h+ (-0.028). LIKELY cause: the notch spans 4.5 D (box plus two gaps of 0.25 D and two flanks of 1.5 D) inside a 5-day detrend, so long boxes have too short a baseline.

## The design (fixed now, no free choice left)
- **D1 = for box lengths D <= 8 h use N1 exactly as in 030** (5-day wotan biweight, lower-flank notch, threshold 6.5, box-overlap mirror rule); **for D > 8 h use the frozen B statistic exactly** (2-day biweight, frozen box SNR, threshold 7, frozen mirror rule). With the frozen grid (3, 4, 5, 6.5, 8, 10, 12, 15 h), N1 owns 3 to 8 h and B owns 10 to 15 h. If the grid on the bench path differs, the same rule applies: N1 for D <= 8 h.
- The 8 h cut is set by a rule, not by results: wotan's best window is 3 x the transit duration (Hippke et al. 2019); the notch's whole span 4.5 D must fit 3 times in the 5-day window, so 4.5 D <= 40 h, D <= 8.9 h; the largest grid length below that is 8 h. Claude saw the 030 duration breakdown before writing this, so the judging benches below are NEW and unseen.
- Merging: one candidate list per arm from both statistics; sort by SNR divided by its own threshold; keep the existing non-overlap rule (centres further apart than 0.5 x the longer box + 0.1 d). Each kept event then goes through the tier rules as it does under its own statistic (N1 events: the 030 N1 path; long-box events: the B path). Thresholds 6.5 and 7 are not tuned.

## Benches
1. **Identity (rule d), mandatory stop if either fails:** cut below 3 h (all boxes frozen) reproduces B exactly (P 48.105 on 1,098, 48.404 on 968; untouched 174 / 79; T156 R 34.207); cut above 15 h (all boxes N1) reproduces 030's N1 at 6.5 exactly (choosing-bench possible 51.34; untouched 165 / 77; T156 R 31.653). Reuse 030's stored events where they are pre-tier and complete; otherwise regenerate.
2. **Choosing bench and old benches (reported, not judged):** D1 on the 968 possible planets of the 006 bench, the old fresh bench (seed 2026111601) and the old T156. Label them exploratory.
3. **New fresh bench (judges rule a):** `data/fable/x1/fresh_draws.py` logic (Codex 006's `006_draws.py`) with **seed 2026112201**, same pools, same rules, 1,250 draws; same "possible" rule (no radius, or depth <= 1e6 x min(1, (0.2009/R)^2), radii `targets/host_radii_g2_g3.csv`). Score B and D1 on it.
4. **New T156 draw (judges rule f):** the same draw rules as the T156 bench (Codex 003 draws, read by `023_inputs.t156_rows`), **seed 2026112202**, same count as the original (2,000); reference subset 3,000 to 6,000 ppm and 6 to 12 h, equal weight per bin. Score B and D1 on it. If the 003 draw code cannot be re-seeded cleanly, stop and report before scoring anything.
5. **TOI-1338 b on the T109 path (rule g):** as in 030d (`030_t109.py`), B must reproduce 6 of 13 first.
6. Untouched tier-1 background on the design stars, both arms, as in 030.

## Pass rules (F1, word for word as in 030, judged on the NEW benches)
(a) paired gain against B on the NEW fresh bench at least +2.0 points of P on possible planets, whole-star 95% interval above zero (10,000 draws, seed 2026112230); (b) untouched tier-1 background at most 174 real and 79 upside-down; (c) dip-against-bump control passes in every bin (99% interval contains zero); (d) identity as in bench 1; (e) new real minus 2.3 x new upside-down tier-1 events against B at most 5; (f) R on the NEW T156 draw not below B's R on that same draw (B is re-measured there; report its interval); (g) TOI-1338 b at least 6 of 13 on the T109 path.
Passing all = D1 becomes the first part of Petrova 2.0 (not frozen yet). Failing any rule: report it as failed; nothing is tuned, no cut or threshold is changed.

## Also report (counts only)
P per bin and per duration band (3 to 6, 6 to 9, 9 to 12, 12 h+) for B, N1 and D1 on every bench; which flags hold D1's new detections; per-crossing tier-1 rate; T156 R on old and new draws.

## Rules
Never edit frozen files (bench copy and study switch, as in 030); design stars and planted light only; counts only in reports; 3 workers x NUMBA_NUM_THREADS=2; pre-create shared folders before workers start (the 028 race); checkpoints and markers so a stopped run resumes without redoing finished phases; data in `data/astra/031/`; branch `astra/031-duration-notch`. Read your meter (last `rate_limits` in your rollout file) before and after; predict and log in `research/astra/USAGE.md`. Claude recounts independently before any merge.
