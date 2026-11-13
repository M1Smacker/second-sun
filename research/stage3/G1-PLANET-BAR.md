# G1 planet-level bar (preregistered, written BEFORE any planet-level measurement)

**Written by:** Claude, 13 Nov 2026, Kuwait 23:31, after Ahmed's question round on Codex 005, before Codex brief 006 starts and before any planet-level number exists. **This file decides G1 from now on.** The single-transit bar (`G1-RECOVERY-BAR.md`, 13 Nov 16:42) stays on record unchanged, with its result (FIX FIRST at R 27.5%, baseline now 33.3%). A change to this file needs a new dated file, written before the numbers it would judge.

## Why a second bar, and why it is not moving the goalposts
The single-transit bar measures whether one transit reaches tier 1. A real circumbinary planet usually transits several times across the sectors a star was watched, so the question that matters for G1 is whether **the planet** is found. That number has never been measured, so a rule written now cannot be tuned on it. Codex 005 also showed that single-transit repairs probably cannot reach 50% (ceilings of about 15 points against 17 needed), which is why Ahmed chose to measure planets.

## The number that decides
**P = planet-level recovery**: the fraction of **reference planets** for which the search method that G1 will use flags **at least one transit at tier 1** (1A, 1L or 1B, SNR 7 or more, same matching rule as T156), counting only planets that transit at least once inside the star's observed data (a planet that never transits in the data can be found by no method; that geometric share is reported separately, not in P).

**Reference planets** (fixed now): transit depth 3,000 to 6,000 ppm (log-uniform), planet period log-uniform from 4 to 8 times the binary period (Kepler's circumbinary planets cluster just outside the stability limit, a few times the binary period: LIKELY, Welsh et al. 2014; Codex checks the primary source and reports the exact sentence), transit duration and transit times from a predeclared circumbinary orbit model that includes the binary's motion (Codex designs it and commits it before any trial), on the design-seen stars only, using all of each drawn star's observed sectors, injected into raw light before windows, masks and detrending, equal weight for the five binary-period bins, 95% interval by star-cluster bootstrap.

**Method:** P is measured for the current chain (Petrova 1.0.0 plus the adopted repeater rule b and FIX 91). If a multi-transit combination method is built, its P is measured the same way, with its own upside-down control, and only a method frozen before G1 can be used for G1.

## What each answer makes us do (same thresholds as the first bar)
1. **P at least 0.50 and its lower 95% bound at least 0.40: GO** to G1 preparation with that method (Amendment 4, freeze, outside audit at the freeze).
2. **P from 0.20 to under 0.50, or the lower bound under 0.40: FIX FIRST.**
3. **P under 0.20: CHAIN BROKEN.**
Any period bin with P under 0.20 is a named blind spot in the G1 preregistration. The upside-down control must still pass the 004 acceptance conditions for whatever method is used.

## What this bar is not
Not a planet occurrence rate and not a claim about the sky. A clean null with a known P is still the win.
