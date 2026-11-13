# G1 recovery bar (preregistered, written BEFORE any T156 result)

**Written by:** Claude, 13 Nov 2026, Kuwait 16:42, before Codex brief 003 starts. **Status:** filed before results. Ahmed may change it only BEFORE the first T156 result is read; after that it stands as written, and a changed rule needs a new dated file.

## Why this exists
G1 is our last unseen list (fence A, 552 rows). It can be searched only once. Codex's 10-trial raw pilot (brief 002, part C) recovered 0 at tier 1, which is too few to be a rate, but it is the first test of the path a real planet takes. Brief 003 (T156) measures that path properly. This file says, in advance, what each answer makes us do, so the bar cannot be tuned after the numbers are seen.

## The number that decides
**R = unconditional tier-1 recovery** of single raw-light injections in the **reference band**: depth 3,000 to 6,000 ppm, duration 6 to 12 hours, on the design-seen stars, with every trial counted in the denominator (including trials whose time falls outside every searched window, in a gap, or in a file with no safe windows). R is the pooled rate over the five binary-period bins, each bin weighted equally. The 95% interval is computed by star-clustered bootstrap (trials of one star are correlated).

Also reported, but not deciding: R per period bin (5 to 10, 10 to 14, 14 to 20, 20 to 27.4, over 27.4 days), R per product (SPOC, TESS-SPOC, QLP), the conditional rate R_c (given the injection lands inside a searched window), and the loss at each stage.

The reference band is a choice made now, not derived from data: it brackets a roughly Saturn-sized planet around a Sun-like primary after dilution by the companion. It is not tuned to any of our results.

## What each answer makes us do
1. **R at least 0.50 and its lower 95% bound at least 0.40: GO.** G1 preparation goes ahead with Petrova 1.0.x (Amendment 4 and the frozen 1.0.1 build). The measured R and every per-bin R go into the G1 preregistration as its stated sensitivity.
2. **R from 0.20 to under 0.50 (or the lower bound under 0.40): FIX FIRST.** G1 waits. The stage with the largest measured loss is fixed in a new Petrova version (1.1.0), which is frozen and tested on design data with injections and the upside-down control before it is used. Then T156 is rerun on the new version, and this bar is applied again.
3. **R under 0.20: CHAIN BROKEN.** No G1 and no Census search until the cause is found and fixed. Everything goes to the largest loss stage.

**In every case:** any period bin with R under 0.20 is named as a blind spot in the G1 preregistration, and the book says it plainly. If the upside-down (bump) control recovers very differently from dips at the same depth (outside the counting error), that is a bug, filed before any decision.

## What this bar is not
It is not a claim about planets in the sky. It measures only our chain on our stars. A clean null with a known R is still the win (rule of 29 Oct 2026).

## Result (added 13 Nov 2026, Kuwait 19:14; the rule above is unchanged)
T156 finished (Codex's design and scripts; Codex stopped at its five-hour limit at 989 of 2,000 trials and Claude resumed the same frozen run with its resume option). 2,000 paired trials on 510 design-seen stars, 222 in the reference band.
**R = 0.27, 95% star-clustered interval 0.21 to 0.34. Decision under this bar: FIX FIRST.** G1 waits; the largest loss stage gets fixed in a new Petrova version, tested, and T156 is rerun.
Reference R per period bin: 5 to 10 d 0.13 (6 of 48, interval 0.04 to 0.23: a named blind spot), 10 to 14 d 0.26, 14 to 20 d 0.26, 20 to 27.4 d 0.40, over 27.4 d 0.33.
Where all 2,000 dips stop (whole depth and duration range): no safe windows 59 (3%), centre outside every searched window 316 (16%), too little left after the eclipse mask 218 (11%), **not found at any tier 570 (29%)**, found but not tier 1 443 (22%), recovered 394 (20%). Bumps recovered 400: the two arms agree in every bin (paired 99% intervals include zero).
Claude re-counted R, the reference counts per bin and the stage counts directly from the raw result journals: identical. Codex's final report and its reading of the losses are still to come.
