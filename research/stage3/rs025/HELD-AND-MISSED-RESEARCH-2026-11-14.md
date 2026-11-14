# RS-025: why found planets are held and why 4 in 10 are never found (started 14 Nov 2026, 12:34 Kuwait, Opus 5.5 medium)

**Why:** RS-024 showed "dominated" cannot lift P to 0.50 (best +2 planets). Road to G1 step 5. Started unasked (memory: research root cause first).

**Cap, written before the start:** 8 weekly points, about 150 tool calls. No helpers. Own data first, then primary sources, then preregistered tests.

**Where the planets go (planet bench, 1,098 planets that cross; `006-check/p-flags.json`):** found at SNR 7+ in at least one crossing 690; at tier 1 529 to 531; found but held about 159 (flags on the best held event: step 78, gap/dump 76, ramp 45, dominated 21, c5 17, p1_veto and orbit_lock about 19); **never found at SNR 7: about 408**. To reach P 0.50 we need about +20 planets (equal weight).

## Questions (each tied to a decision)
| # | Question | Decision it feeds |
|---|---|---|
| Q1 | What does each holding flag cost and buy on its own (planets gained, upside-down and real background) if cleared alone? | which flag to research first |
| Q2 | What exactly makes step, gap/dump and ramp fire on a real transit (shape, distance to gaps and dumps, product)? | design of a fairer test |
| Q3 | Why are about 408 planets never found at SNR 7 (too shallow for the noise, in gaps, masked, detrending eats them)? | whether the bigger gain is in detection, not flags |
| Q4 | How do Kepler (Rubble, Marshall, Skye), LEO-Vetter and mono-cbp treat transits next to gaps, momentum dumps and steps? | replacement design |
| Q5 | Do the same flags hold the real known planets (TOI-1338 b transits, the second system)? | a check that fixes help real planets, not only planted ones |

## Findings
(filled below)

### Q1. Price of each holding flag, cleared alone (`rs025_price.py`, identity baseline 529 / 486 exact; 12:43). CONFIRMED (one key)
| Flag cleared | Planets (new) | P equal weight | Background real / upside-down | Extra upside-down per planet gained |
|---|---:|---:|---|---:|
| none | 529 | 0.4845 | 176 / 83 | |
| step | 559 (+30) | 0.5121 | 406 / 188 | 3.5 |
| gap or dump | 560 (+31) | 0.5132 | 259 / 97 | **0.45** |
| ramp | 543 (+14) | 0.4970 | 202 / 95 | 0.86 |
| all three | 631 (+102) | 0.5783 | 1,178 / 878 | 7.8 |
**Meaning:** gap/dump is by far the cheapest planets per upside-down alarm, and clearing it alone would cross 0.50. But it adds 83 REAL background events against 14 upside-down: near data gaps the false dips far outnumber false bumps, so the upside-down meter would hide most of the cost there (the same sign asymmetry as RS-024). A gap fix must be judged on the real background too, not only on the upside-down count. Step is expensive (3.5 alarms per planet) and stays.

### Q4 (gaps). What professionals do. CONFIRMED (primary text, LEO-Vetter, arXiv 2509.10619 III.11 to III.13)
- Data Gap Test: a transit is "near a gap" if its mid-time is within 2 transit durations of a gap of at least 0.3 d; a TCE fails only if 50% or more of its transits are near gaps (scattered light at TESS orbit starts is the stated reason).
- Missing Data (Kepler's Rubble): count points within 2 durations of the centre; flag if more than 25% of the expected cadences are missing.
- No momentum-dump distance test; dumps are handled by shape tests (step, asymmetry, single-event domination).
- Ours: within 0.5 d of a gap edge (any gap over 0.25 d) or from 0.25 d before to 0.5 d after a momentum dump, any duration, any coverage (`detect_v2.py` 246 to 281; its own comment: "FLAG (for the human vetting sheet, never auto-reject)"; Stage 3 made it a tier-2 hold). The step flag already holds events with too little data on a side (`stage3_core.step_flag`, cover under STEP_COVER).

### Q2 (dumps). Where and what the dump-held dips are. CONFIRMED (own data, `rs025_gapsplit.py`, `rs025_dumps.py`, `rs025_dumpshape.py`)
- Split of gap/dump: switching off the momentum-dump half frees +23 planets (P 0.506) for +7 upside-down and +64 real background; switching off the gap-edge half frees +9 (P 0.493) for +5 and +18.
- Dump times read from one SPOC/TESS-SPOC file per sector (108 sectors; second file agrees in 97 of 107). Near dumps, events held only by the dump rule: 154 real against 49 upside-down (3 to 1: dumps make false DIPS, so the upside-down meter misses most of them). Distance does NOT separate them from planted planets: fakes median 5.9 h (real) and 4.7 h (upside-down) from the dump, freed planted crossings median 4.0 h; both peak at 3 to 6 h.
- Shape does: freed planted dips have median SNR 30 and a flat baseline (largest side lift median 0.10 of the depth); the dump-zone fakes have median SNR about 9 and uneven baselines (median lift 0.21 real, 0.33 upside-down). The SNR difference is partly the bench's depth range (3,000 to 6,000 ppm), so a rule on baseline shape is safer than one on SNR.

## Test plan 2, written BEFORE running (14 Nov 2026, 13:00 Kuwait)
- **DS, dump zone judged by shape:** an event in the momentum-dump zone is held only if its baseline is uneven: the larger side lift is above 0.25 of the dip depth (half of STEP_LIFT, the step rule's limit), or a lift is unmeasured. The gap-edge half is unchanged. Honest note: 0.25 was chosen after seeing the design-bench shapes above (bench data, not search results); Codex must check it on the T156 bench, and Fable's design round may replace it.
- Judged by the Tree rule (P up, upside-down background not up), and **also reported: the real background**, because near dumps the upside-down meter is blind to most false dips.

### Result of test plan 2 (`rs025_dumpshape_test.py`, 13:09; identity baseline exact). CONFIRMED (one key)
| Rule | Planets (new) | P equal weight | Background real / upside-down | Paired control |
|---|---:|---:|---|---|
| frozen | 529 | 0.4845 | 176 / 83 | fails 2 bins (dominated, RS-024) |
| dump half off | 552 (+23) | 0.5060 | 240 / 90 | fails |
| **DS, dump zone judged by shape** | 548 (+19) | **0.5024** | 213 / 88 | fails (dominated not changed here) |
**Not adopted under the Tree rule** (+5 upside-down). DS keeps 19 of the 23 planets and cuts the extra real background from +64 to +37. No rule tested today frees planets with zero extra false alarms.

## Where RS-025 stands (13:10)
- Answered: Q1 (prices), Q2 for dumps (distance does not separate, shape partly does), Q4 for gaps (LEO-Vetter, Kepler Rubble).
- Open: Q2 for step and ramp; **Q3, the about 408 planets never found at SNR 7 (the biggest pool)**; Q5 (real known planets under these rules).
- **Plain conclusion so far:** P 0.50 is within reach (DS alone gives 0.502; DS plus OAE not yet run), but every route found so far costs a few false alarms. The next decision is a trade-off rule (how many extra false alarms per planet gained is acceptable, judged on BOTH meters, since the upside-down meter is blind near dumps and gaps), not another single fix. That is the design task for Fable's round on Monday, with Codex's T156 second key.
- Used: about 2 weekly points of the 8 cap (meter 3% to 5%).
