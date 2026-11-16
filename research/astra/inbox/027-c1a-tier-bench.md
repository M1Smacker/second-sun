# Brief 027: tier-level bench of the detrending switch c1a, the "too faint" lever (Claude, 17 Nov 2026, 1:50 am Kuwait)

You run headless; nobody can answer questions. Choose the safest reading, say so in the report, go on. AGENTS.md wins over this brief. Model: GPT-6-Astra, high effort. Tree node 1.3 (the detector misses the dip; also nodes 1.5 and 1.6).

## Why
Fable's X4 (`research/fable-method/X4-FAINT-POOL.md`, scripts `data\fable\f2\x4_faint.py`, `x4_proto.py`, `x4_proto_summary.py`, `summary-x4-proto.txt`, readable through your `data` link) found that the "too faint" pool (22 points of P, the biggest by RS-037) is mostly slow wiggles that the frozen 2-day detrending leaves in. The pipeline's own study switch **c1a** (`pipeline/stage2_search.py` line 56: detrend window 3 x box length, at least 0.5 d; switched on by adding `c1a` to the `VESPER_OPTS` environment variable, as `x4_proto.py` does with `X4_OPTS="c6,p1,c1a"`) lifts planets with a crossing at SNR 7+ from 64.1% to 71.3% at DETECTOR level (5 to 10 day binaries 54% to 70%). But SNR 7+ events on untouched light rise by about 1.6 times on BOTH arms (real 1.96 to 3.07, upside-down 1.44 to 2.38 per 100 days). Whether the tier rules hold those back, and whether any P is left at equal false alarms, is NOT TESTED. This job measures it. It is the only lever found so far that could move P by more than a few points, so it is worth an honest, careful bench.

## Read first
`research/fable-method/X4-FAINT-POOL.md`, `X10-COMBINED.md` (the candidate K = cap + R2 + M2 and its numbers), `X6-GUARD-FLAGS.md` (rule R2), `F1-PETROVA-1.1-VERDICT.md` sections 1 and 5, `ASTRA-REVIEW-2026-11-16.md`, your reports 013, 023 (harness `research/astra/scripts/023_*.py`), 025 and 026 (the latest, including what a star-wide hold costs), `research/stage3/G1-PLANET-BAR-75-2026-11-15.md`. Fable's tier-level scorer copies are `data\fable\f4\x10_prepare.py`, `x10_score.py`, `x10_summary.py`. If a step of the 023 harness, the 006 and 013 planet and background benches, or the vetting rules is unclear, read the code and its report instead of guessing.

## Configurations (bench copies; frozen pipeline files untouched; M2 is out of this job)
1. **B** = adopted set (must reproduce P 48.105%, T156 R 34.207%, background 174 real / 79 upside-down; if not, say why and report both).
2. **B + c1a.**
3. **K2** = B + C96 depth cap + R2 (dump hold by shape, gap-edge hold released), exactly as X10 (cap + R2: possible-planet P 51.02, 158 real / 63 upside-down). Reproduce that row first.
4. **K2 + c1a.**
M2 stays out because it needs its own mask replays and, with R2, leaves only 2 real alarms of margin; if K2 + c1a passes, say that M2 is the next test, do not run it.

## What to run
The c1a change acts BEFORE the tier rules, so detections change: re-run the search chain with `VESPER_OPTS` plus `c1a` on the same inputs as B, inject into RAW light before every step, then apply the vetting and tier rules of B and of K2 on the new detections. Never run or import pipeline scripts as they are (they write into `D:\second-sun\data`): copy what you need into `research/astra/scripts/` and point it at `data\astra\027\`. Inputs: the 1,098 planet bench (006 drawing), T156's 2,000 single dips and the 222 Saturn-like trials, the untouched design light of both campaigns (013). Report both populations: all 1,098 and the 968 possible planets (F1 section 1: the 130 impossible planets are held by the cap).

## Measures, for each configuration
1. Planet bench P, equal weight on the five binary-period bins, 10,000-draw whole-star bootstrap, seed 2026111523 (as 026); paired change against B and against the same configuration without c1a; planets gained and lost per bin.
2. T156 reference R with interval.
3. Untouched design light, both arms, both campaigns: tier-1 real and upside-down background counts, and the flags that hold the new events at tier 2 (dump, step, gap edge, ramp, repeater, dominated): which flags catch how many of the extra events.
4. Paired dip-against-bump control per bin (99%, 10,000 whole-star bootstraps), pass or fail per bin.
5. Blind-spot checks as in 023 (hours to the nearest momentum dump, within one eclipse width of a catalogue eclipse) for every new real tier-1 event, and the F1 rule: (new real) minus 2.3 x (new upside-down) at most 5.
6. Identity check: with `c1a` off, every number above equals the saved B, K2 results.

## Pass rule (write it into the report BEFORE scoring; nothing tuned after seeing outputs)
A c1a configuration passes only if ALL hold: (a) on the 968 possible planets, P gain against the same configuration without c1a at least +2.0 points, paired 95% interval above zero; (b) untouched upside-down background at most 79 and real at most 174 (the adopted limits, whatever the base reads); (c) paired control passes in every bin; (d) T156 R not below the base; (e) the F1 new-real rule (5) holds. Report each rule, pass or fail, with the number.

## Equal-alarm analysis (preregistered here; this is the only threshold step allowed)
If fixed settings fail rule (b) only, test whether the gain survives at equal false alarms: split the design stars by TIC parity (even = choosing half, odd = held-out half, fixed now). On the choosing half raise the tier-1 SNR floor over the fixed ladder 7.0, 7.5, 8.0, 8.5, 9.0, 10.0 (a new floor applies to every candidate event on both arms) and take the smallest floor at which the choosing half's untouched upside-down count is not above the base's count on that half. Report P, the backgrounds and R on the HELD-OUT half and pooled, labelling the floor "chosen on half the stars, a proposal, not a frozen setting". Do not try other ladders. This is a winner's-curse guard: the number that counts is the held-out half.

## If it passes
Confirm on the fresh-seed planets of Fable's X1 (`research/fable-method/X1-FRESH-SEED.md`, planets and light under `data\astra\fable-fresh`, seed 2026111601, 1,250 planets) if the cap allows; otherwise say that the confirmation is the first job to run next. Say how far it moves P toward the 0.75 bar and what would still be needed.

## Method log, rules and report
Lab-notebook work log `research/astra/reports/027-worklog.md` (files read, scripts, results, the check that could prove the bench wrong, decisions with their evidence, reversals with the result that reversed them). Rules as in 026: branch `astra/027-c1a-tier-bench` from the latest main; CPU up to 4 workers, `NUMBA_NUM_THREADS=2` each; data under `data\astra\027\`; fence A and B never (the stars in the design benches are not fenced, but if any file would open a fenced star, stop and say so); no G1 or sealed data; frozen files untouched; never push. **Run every long job in the FOREGROUND inside your session and wait for it (background jobs die when your process exits: that killed the 026 bench once); write `progress.json` checkpoints so a restart resumes.** Cap 60 five-hour points; never poll. If the full chain cannot finish inside the cap, run in this order and say what was left: planet bench 1,098, untouched background, T156, equal-alarm analysis.

Report `research/astra/reports/027-report.md`: verdict line first (found something / found nothing / passes or fails, in one plain line), then the pass rule as written, the table per configuration with intervals on both populations, rule by rule results, the equal-alarm result, what you did NOT check, usage (honestly: say if the meter is unavailable).
