# Petrova 1.0.0 build spec (A2 and A3), 11 Nov 2026

Goal: C2 (catalogue windows + within-sector repeat lane + event-stage cross-sector veto; settings `C0_REFIT=0 C1_PSLOW=1e9 C1_Z=5 C2_TOL_H=1 C2_NMIN=2`) inside the real chain behind ONE switch `p1`, default OFF. Run as `VESPER_OPTS=c6,p1`. With `p1` off the code must give identical events to Vesper 0.8.1 (zero-difference proof), so 0.8.1 stays reproducible. Sources of the logic (verbatim where possible): `research/fable-audit-2026-11/scripts/c0_catalogue_mask.py`, `c1_mask.py`, `c2_event_veto.py`.

## Files
1. `pipeline/petrova_mask.py` (NEW, self-contained, no import from research/): catalogue loader (g1 and g2 from the Prsa table `data/xmatch/ebs.csv`, g3 from TTC table 3), `windows`, `refit` (offset only), within-sector repeat lane (`find_runs`, `complement` with no cross-sector lane), `remove`, `mask_runs(t, f, periods, tic)` with the same return shape as `stage2_search.mask_runs`, `veto_events` (event-stage cross-sector phase veto, P at least 13 d, TOL 1 h, NMIN 2 when 3 or more other sectors else 1, durations within 2.5, depths within 3), `recovered_intervals` (cadences the OLD mask removes on the real arm and the new mask keeps). `selftest()` on synthetic light.
2. `pipeline/vopts.py`: add `p1` to KNOWN and the docstring.
3. `pipeline/stage2_search.py`: `mask_runs` hook (only when `p1` on); `prepare` passes the star and stores `p1` info in `meta` (primary offset, T0, P, recovered intervals) only when `p1` on; `do_group` adds `recovered` (bool) and `p1_off` to each event only when `p1` on.
4. `pipeline/stage3_core.py`: `tier_of` sends `p1_veto` events to tier 2 (key exists only with `p1`).
5. `pipeline/stage3_report.py`: `apply_v7` computes `p1_veto` over the run's events (best product per sector, same arm) when `p1` on.
6. `pipeline/r1_run.py` (NEW, A5, modelled on `g3_run.py`): freeze, go file, refuses without the frozen hash and a clean tree; dry-run and sealed modes read `targets/r1_targets.csv` (`design_seen`).
7. `pipeline/r1_gate.py` (NEW, A3): whole-chain planted-dip test, injection into RAW light before `prepare`, mirror rule on the upside-down arm, per period bin; prints counts only.

## Rules
- Mirror rule: every step treats `f` and `2 - f` alike; windows and repeat-lane cadences are chosen from the real arm and applied to both arms.
- No `pipeline` rule is tuned; all numbers come from the C2 design (see `DESIGN-C2-OPUS-2026-11-10.md`).
- Tests: (1) `petrova_mask.selftest()`; (2) `zero_diff.py` with `p1` off: 300 of 300 identical to 0.8.1; (3) `p1` on, synthetic recurring eclipse is removed, a planted single dip is kept; (4) gate (a) to (d) of `R1-PREREGISTRATION.md` section 5.
- G1 widths: Prsa where the period matches within 2%; otherwise no width, the repeat lane alone (as C1 does), flagged and counted. G1 joins only after the gates pass on it.
