# Vesper v8 design (30 Oct 2026, Opus 5.5 medium; Ahmed: "start the work")

Rules unchanged: settings frozen per version and never tuned on results; v8 is chosen on G1 and the G2 development slice only (G2-PREREGISTRATION.md allows this); the 594 sealed stars stay untouched until v8 is frozen under a hash with the regressions re-proved AND Ahmed says go.

## 1. The three forks: defaults I used (Ahmed can overrule any of them before the freeze)
| Fork | Default used | Why this default |
|---|---|---|
| False-alarm budget | **Hold at 8 upside-down tier-1 per 1,000 star-sectors** | It was written before any option was run. Raising it now, after seeing which options sit just above it, would be choosing a rule from the results. If Ahmed wants more planets for more false alarms, the cleanest buy is c2 alone (no dip lost in any box; G2 dev 7.7 to 12.6 per 1,000 for +2.4 to +6.1 points). |
| Price of the short end | **Keep the 3 h box** | The floor bought nothing (false alarms moved to 4 h) and cost 7 to 8 points at 4 h. |
| Yardstick weight | **Keep equal weights for v8** | Same reason as the budget: a weight chosen now would be chosen after the results. A physical weight (known transits about 6 to 12 h) can be written for v9 before any v9 run. |

## 2. What v8 is
**v8 = Vesper 0.7.1 + the orbit-locked flag (`c6`).** Nothing else passed the yardstick; every sensitivity option traded about 1 point of recovery for 1 false alarm per 1,000 (VESPER-VERSIONS.md).

`c6`: a tier-1 event goes to tier 2 if a tier-1 partner of the same kind on the same star, in another sector, sits a whole number of catalogue binary periods away (within 0.5 x the longer box + 0.1 d), with box length within x1.6 and depth within x2. Code: `stage3_core.orbit_locked`, applied in `stage3_report.apply_v7` after the v7 tiers.

## 3. Evidence (CONFIRMED on our own data; aggregates only, no real event opened)
- Built-in switch reproduces the offline C6 variant C exactly (`c6_chain_check.py`, `c6-orbit-lock.txt`): G2 dev tier-1 real 90 to 43, upside-down 25 to 23 (49 locked events on 7 stars); G1 21 and 32 unchanged (nothing locked). Switch off: no new column, every tier as before.
- False alarms with c6: G1 6.32, G2 dev 7.07 per 1,000 (budget 8: pass).
- Real minus upside-down excess on G2 dev, before to after: bar 7 +65 to +20; bar 12 +10 to 0.
- Cost on injected dips: 14 of 1,731 tier-1 fakes (0.81%) flagged by chance on G2 dev; none on G1 (offline, `c6_orbit_lock.py`).
- Tests: `test_vopts.py` 7 of 7 PASS (new `test_c6_lock`); `test_stage3_prep.py` PASS (dry runs identical to Stage 2).

## 4. Known limit (filed, not hidden)
The injection harness (`chain_recovery.py`) judges one star-sector against the real events of the same sector, so it cannot see a partner in another sector: run with c6 on, it would show no c6 cost. v8 completeness must therefore be quoted as the harness number minus the offline c6 cost (0.81% of tier-1 fakes on G2 dev). LIKELY small; the exact share at the sealed stars is NOT TESTED until the sealed run.

## 5. FROZEN 30 Oct 2026 (Ahmed: "You have my approval")
Vesper 0.8.0 = 0.7.1 + c6, frozen in `SETTINGS_FROZEN_V8.json`, hash 5f73692944aa (rules and code only; each run records its own data hashes), commit 12733c2, pipeline clean. Regression re-proved with c6 on (`v8-regression-zero-diff.txt`): zero-difference 300 of 300 star-sectors on G1, 0 errors, mutation caught 7 of 15; `test_vopts.py` 7 of 7; `test_stage3_prep.py` 20 of 20 (c6 off and on). Book: chapters 9 and 10 and learning-track checks updated; Vesper rename and F-090 update still open. NOT done: the sealed run (step 4 below), which needs Ahmed's separate go and a sealed-run mode that refuses to run unless the code hash equals the frozen one.

### Freeze recipe (as planned)
1. Make `c6` part of the frozen setting (VESPER_OPTS=c6 recorded in the run file, or default on in v8 code) and record the code hash.
2. Re-prove: zero-difference on G1 (300 star-sectors, whole chain), Stage 2 dry runs, `test_vopts.py`, mutation check.
3. Book: Vesper rename, F-090 update, v8 page.
4. Then, only on Ahmed's go: download and search the 594 sealed stars once.
