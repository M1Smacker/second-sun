# 030: tier-level bench of the lower-flank notch statistic (Petrova 2.0 candidate N1)

Written by Claude, 18 Nov 2026, 11:25 am. **GO: Ahmed, 11:28 am ("Sure, launch it").** Project restarted 18 Nov 2026 with planet recovery P as the only focus (Ahmed). Background: `research/stage3/rs039/P75-RESEARCH-2026-11-18.md` (Claude's RS-039), especially A8b to A8d, and `research/stage3/rs039/DRAFT-BENCH-BRIEFS.md` brief N.

## What Claude measured (detection level only, 160 design stars; read it, do not trust it)
- Statistic N1: light detrended with a 5-day wotan biweight; for every box centre and box length D (the frozen ten lengths), baseline = the LOWER of the two flank means (each flank 1.5 D wide, starting 0.25 D outside the box); depth = baseline - box mean; SNR = (depth - median depth) / (1.4826 x MAD of depths), per star-sector and D. Reference code: `D:\second-sun\data\rs039\a8b_notchmin.py` (function `notch_scores`).
- At equal untouched alarms on both arms (N1 at SNR 5 against frozen at 7): planted crossings detected 0.741 vs 0.664, star-bootstrap 95% +4.0 to +11.1 points; planets detected 81.1 vs 69.7; dip-against-bump gap -0.1 (every bin within 0.03).
- Unknown: what the tier rules (step, ramp, gap edge, dump, dominated, mirror, repeater, eclipse overlap, OAE, FIX 95) do to events at SNR 5 to 7. That is this job.

## Task
1. Add N1 to a BENCH COPY of the chain as a study switch (never edit frozen files). With the switch off, the copy must reproduce set B exactly (P 48.105% on 1,098, 48.404% on 968; T156 reference R 34.207%; untouched 174 real / 79 upside-down). Stop and report if it does not.
2. Mirror rule for N1: an upside-down match counts only if it overlaps the box itself (centres within 0.25 x the box), not its flanks (A8 showed flank matches are an artefact of flank statistics).
3. Threshold: run N1 at detection thresholds 4.5, 5, 5.5, 6, 6.5 and 7. The **chosen** threshold is fixed by this rule, written now: the lowest threshold at which the TIER-1 untouched background on the choosing bench is at most 174 real AND at most 79 upside-down. No other choice is allowed.
4. Score the chosen N1 on the choosing bench (968 possible planets), then once on the fresh bench (seed 2026111601, Fable's X1 set), equal weight per binary-period bin, whole-star bootstrap 10,000 draws, seed 2026111830.
5. Report also: per-crossing tier-1 rate; alarm curves (tier 1, both arms) at every threshold in step 3; which flags hold the new detections (counts per flag); T156 reference R; TOI-1338 b tier-1 transits (count, as under B: 6 of 13).

## Pass rule (F1 section 5, written before any result; Claude and Ahmed may not change it after)
(a) paired gain against B on the FRESH bench at least +2.0 points of P on possible planets, 95% interval above zero; (b) untouched tier-1 background at most 79 upside-down and at most 174 real; (c) dip-against-bump control passes in every bin (planted dips vs planted bumps scored on the upside-down copy, 99% interval contains zero); (d) zero-planet identity: switch off reproduces B, and untouched light with N1 changes only through N1; (e) rule 4: new real minus 2.3 x new upside-down tier-1 events against B at most 5; (f) T156 reference R not below B's 34.207; (g) TOI-1338 b tier-1 transits not fewer than 6.
Passing all = N1 becomes the first part of Petrova 2.0 (freeze later, with the other levers). Failing (b) or (e) alone: report the flag counts; do not tune.

## Rules
Design stars and planted light only; no real-event lists in reports (counts only); 3 workers x NUMBA_NUM_THREADS=2; foreground runs; data in `data/astra/030/`; branch `astra/030-notch-tier-bench`; predict Codex weekly use before starting and log actual in `research/astra/USAGE.md`. Pre-create any shared output folders before parallel workers start (the 028 folder race).
