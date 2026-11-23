# 032: eclipse times v3 (honest error model), then the mask bench with our own TESS ephemerides (FIX 94)

Written by Claude, 23 Nov 2026, 10:52 am Kuwait. **GO: Ahmed, 22 Nov 2026, 9:30 pm ("I hereby give you every permission required") and 23 Nov 10:43 am (work the queues without waiting).** This file is the preregistration: committed before any v3 number exists. Runs beside the 031 bench (do not touch `data/astra/031/` or its processes).

## Background (read first)
- Your 014 part 2 (branch `astra/014-dumps-ephemerides`, unmerged; data in `data/astra/014/`): alias resolution PASSED (trap 30/30); controls FAILED (period 3 sigma 15/60). Claude's root cause `research/stage3/rs034/CODEX-014-PART2-ROOT-CAUSE-2026-11-15.md`: periods are good (50 of 58 within 0.001 d), but per-eclipse errors are about 2x too small (reduced chi-square 4.7), so the large-residual flag makes 39 of 58 tracks unusable (33 of those agree within 0.001 d).
- Why it matters: FIX 94 (mask padding blanks whole light curves on 112 G2 stars; your 010: up to +25 planets) and Census (`research/stage3/census_gaia/C1-C2-RESULT-2026-11-23.md`: Gaia EB periods are unusable for timing, so Census ephemerides must come from this fit).

## Part A: error model v3 (design fixed now; nothing below is tuned on results)
Reuse 014's per-eclipse time measurement and alias resolution unchanged (copy the 014 scripts to `research/astra/scripts/032_*`; your 014 `eclipse-times-v2.csv` may be reused for the stars it covers). Change only the error model and the flags:
1. **Extra scatter:** per track, s >= 0 added in quadrature to every per-eclipse error, solved so the reduced chi-square of the linear ephemeris fit is 1 (s = 0 if already at or below 1). One robust pass first: drop eclipses whose residual exceeds 5 x 1.4826 x MAD (at most 10% of a track's eclipses; report how many). Period and epoch errors come from the fit with the inflated errors.
2. **Usable flag:** a track is usable if it has 3 or more eclipse times in 2 or more sectors AND its robust residual scatter (1.4826 x MAD) is at most 0.1 x the eclipse width. The old large-residual flag in formal sigmas is dropped.
3. **Agreement with the catalogue (controls only):** a control track AGREES if, at the mid-time of every sector the star has, the v3 predicted primary eclipse centre is within 0.25 x the catalogue eclipse width of the catalogue prediction. Report separately (calibration, not a pass rule): share of usable controls with period within 3 combined sigma using v3 errors.

## New controls (judging sample)
Seeds 12 and 14 are spent. Draw a NEW control sample with seed **2026112316** using 014's eligibility rule exactly (design-seen G2, not affected, catalogue padding under 0.05 d in every sector), excluding the 100 stars of seeds 12 and 14, stratified as before (5 period bins), 60 stars, or all remaining eligible stars if fewer (state the count before fitting). Synthetic twin-eclipse trap: rerun as in 014 (must stay 30/30).

## Part A pass rules (judged on the seed-2026112316 controls only)
(A1) usable: at least 80% of control primary tracks that have 3 or more eclipse times; (A2) agreement: at least 90% of usable control primary tracks agree (rule 3); (A3) trap 30/30. Seeds 12 and 14 may be reported as development numbers (labelled seen). If A fails: report, stop, no tuning, no Part B.

## Part B (only if Part A passes): the mask with our own ephemerides on the benches
- **V3 mask:** Petrova 1.0 mask path exactly (bench copy plus study switch, as in your 010/011), except that for a star whose primary track is usable under v3 the window centres come from the v3 ephemeris and the timing padding is 3 x the v3 predicted-centre error at that sector (secondary from the measured secondary track if usable, else the catalogue phase with the same padding); every other star keeps the frozen catalogue windows. The same mask on both arms.
- Benches and rules: F1 rules (a) to (g) word for word as in brief 031, against frozen B, on a NEW fresh bench (seed **2026112301**, 1,250 draws, 006 draw code) and a NEW T156 draw (seed **2026112302**, 2,000 draws; draws whose selected product loads no times are excluded from both sides, as in 031c), identity at both ends (V3 with zero usable tracks reproduces B exactly), untouched tier-1 background both arms, TOI-1338 b on the T109 path. Also report, exploratory: P change on the 112 affected stars alone, and how many of RS-027's deep wrong-time eclipse events (your 011) are removed.

## Rules
Never edit frozen files; design stars and planted light only; counts only in reports; **2 workers x NUMBA_NUM_THREADS=2** (the 031 bench uses 3 workers; the machine cap is about 70%); pre-create shared folders before workers start; checkpoints so a stopped run resumes; data in `data/astra/032/`; branch `astra/032-eclipse-times-v3`. If Part B will take more than 3 hours of machine time, start it detached (as you did for 031) and hand back with a progress file. Read your meter before and after; predict and log in `research/astra/USAGE.md`. Claude recounts independently before any merge.
