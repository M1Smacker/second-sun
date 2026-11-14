# RS-034: why Codex 014 part 2 (eclipse times v2) failed its controls (Claude, 15 Nov 2026, 12:02 am, Opus 5.5 medium)

**Cap, written first:** 0.3 weekly points, about 5 tool calls; Codex's own output table only (`D:\second-sun-astra\data\astra\014\ephemerides-v2.csv`, seed-12 controls, primary tracks). Fence check of branch 014 clean (11:44 pm run; part 2 commits add report text and data under data\astra only).

## What Codex reported (commit 249b0ad, preregistered at 11:45 pm before fitting)
FAIL: seed-12 period within 3 combined sigma 15 / 60 (54 needed), epoch 9 / 60; seed-14 hold-out 11 / 40 and 6 / 40. Alias resolution PASSED: synthetic trap 30 / 30; all 100 controls chose the catalogue band. Calibrated reduced chi-square still 4.69 (seed 12). Codex did not iterate after the hold-out (as the brief requires).

## Root cause (CONFIRMED on Codex's table, one key)
- **The periods are good.** Against the catalogue, 50 of 58 fitted seed-12 primary periods agree within 0.001 d and 56 within 0.01 d (012: 38 and 44). The alias fix worked.
- **The scoring fails them through the error model.** 39 of 58 tracks carry the large-residual flag (status "timing variations"), so they are unusable and count as failures; **33 of those 39 agree with the catalogue period within 0.001 d.** Of the 19 usable tracks, 15 pass 3 sigma.
- Why the flag trips: per-eclipse time errors remain about 2 times too small after the one-scale-per-product calibration (reduced chi-square 4.7; fitted period errors median 2.5e-6 d against catalogue 3.6e-5 d). Normal eclipse-to-eclipse scatter (spots, detrending, cadence) looks like timing variations.
- Even ignoring the flag, 3-sigma passes 37 of 58 (median distance 1.6 sigma): the formal errors are too tight for a strict sigma test.

## What it means (for Fable's task 1, FIX 94)
- The eclipse-time measurement is close to usable; the failing parts are the per-eclipse error model and the residual flag that depends on it.
- Design direction (NOT TESTED, for Fable, not for Codex to retune on the spent hold-out): a per-star extra scatter term added in quadrature (fitted from the star's own residuals), a residual flag on robust scatter in widths rather than formal sigmas, and agreement judged against the catalogue's own spread (quarter width) as well. Any v3 needs a NEW hold-out (seed 16); seed 14 is spent.
- Epoch failures (9 / 60) NOT examined here.
