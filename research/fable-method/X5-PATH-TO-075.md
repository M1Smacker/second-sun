# X5: the path to 0.75 (Opus 5.5 Extra, 17 Nov 2026, 5:38 pm; bench copies only, nothing frozen)

**Verdict in one line: found something, and it is bad news for the current candidate. Under the new rule 4 (new real minus 2.3 x new upside-down at most 5), mask timing M2 fails on its own (excess 17.1), so every candidate with M2 fails; so do DS (12.1) and R2 (11.0). The best measured change that passes every rule the saved outputs can check is depth cap + the dominated hold released: +1.45 points (95% +0.70 to +2.27) on the 968 possible planets, P 49.85%, fresh seed +1.11. That is under the +2.0 point bar of F1 rule 2, so nothing can be frozen today. Realistic best P for 1.1: about 0.50 to 0.52. 0.75 is not reachable with any measured lever.**

Script: `data/opus-x11/x5_rule4.py` (output `x5_rule4.txt`, `x5_rule4.json`). It reads only Fable's saved scorer outputs (x6 and x10 on the choosing bench, x1 and x1m on the fresh seed 2026111601) and scores all 19 depth-cap configurations, with and without M2, on: (a) paired gain against B, 95% whole-star interval above zero on the 968 AND on the fresh 941; (b) untouched background real at most 174, upside-down at most 79; (c) per-bin dip-gain minus bump-gain, 99% interval contains zero in all five bins, both benches (my reading of the control from saved rows); (e) rule 4, new events matched to B's tier-1 events by the rule of Claude's 027 addendum.

**Checks that could have failed, and did not (CONFIRMED):** B reproduces 174 / 79 and P 48.40 (968); K2 = cap + R2 gives 34 new real, 10 new upside-down, excess 11.0, exactly Codex 027 and Claude's independent recount; every X10 and X1 row (P, change, interval, alarms) reproduces to the second decimal.

## 1. Every candidate against the rules (CONFIRMED as computed)
Change in points against B; possible planets (968); fresh = fresh seed, possible planets (941).

| Configuration (all with depth cap) | Change 968 (95%) | Fresh | Real / upside-down | New real / new upside-down | Rule 4 excess | Fails |
|---|---|---|---|---|---|---|
| cap only | -0.10 | 0.00 | 124 / 53 | 0 / 0 | 0.0 | (a) no gain |
| **dominated released** | **+1.45 (+0.70 to +2.27)** | **+1.11 (+0.48 to +1.85)** | **150 / 77** | **26 / 24** | **-29.2** | **none of a, b, c, e; under +2.0** |
| ramp released | +1.23 (+0.55 to +2.01) | +0.54 (+0.11 to +1.04) | 139 / 64 | 15 / 11 | -10.3 | none; under +2.0, fresh under half |
| gap edge released | +0.73 (+0.18 to +1.35) | +0.53 (+0.10 to +1.06) | 138 / 58 | 14 / 5 | 2.5 | none; small |
| DS (dump by shape) | +1.79 (+0.95 to +2.73) | +1.22 | 143 / 56 | 19 / 3 | **12.1** | rule 4 |
| R2 (DS + gap edge) | +2.61 (+1.60 to +3.71) | +1.75 | 158 / 63 | 34 / 10 | **11.0** | rule 4 |
| R1 (R2 + ramp) | +4.55 | +2.74 | 193 / 78 | 69 / 25 | 11.5 | real 193, rule 4 |
| step released | +2.29 | +1.76 | 279 / 166 | 155 / 113 | -104.9 | alarms; control on fresh |
| M2 alone | +1.36 (+0.43 to +2.44) | +2.19 | 139 / 56 | 24 / 3 | **17.1** | rule 4 |
| DS + M2 (F1 candidate) | +3.26 | +3.41 | 156 / 59 | 41 / 6 | 27.2 | rule 4 |
| **R2 + M2 (Fable's proposal)** | **+4.08** | **+3.94** | **172 / 66** | **57 / 13** | **27.1** | **rule 4** |
| ramp released + M2 | +2.58 (+1.46 to +3.87) | +2.84 | 158 / 68 | 43 / 15 | 8.5 | rule 4 (near) |
| dominated released + M2 | +3.71 (+2.14 to +5.57) | +4.00 | 167 / 81 | 52 / 28 | -12.4 | upside-down 81 |

Readings:
- **M2 is the problem, not only R2.** Its 24 new real events against 3 new upside-down give 17.1 alone (F1 section 3 already read at least 14 of them as eclipses the catalogue cannot place). Rule 4 is therefore a rule against M2 until a leftover-eclipse check exists that works (M4 failed on planets, Codex 026).
- DS, R2 and "dump text released" all fail for the same reason: their new real events carry the momentum-dump flag (19 of 19, 20 of 34, 46 of 46) with almost no upside-down mirror. Narrowing R2's dump release to nothing leaves "gap edge released": it passes but gives +0.7.
- The passing releases (dominated, ramp, gap edge) pass rule 4 because they add upside-down events as fast as real ones: they are noise-like, which the rule tolerates. Rule 4 rewards a fair release, not a clean one; rule (b) is what limits them.
- Rule (c), my per-bin control, fails for R3 on the 968 and for step on the fresh bench only.

## 2. Best candidate that passes (LIKELY as a freeze candidate; its parts CONFIRMED as computed)
- **Single measured: cap + dominated released**, P 49.85% on the 968 (paired change +1.45, +0.70 to +2.27), 44.8 on all 1,098 (change -3.30 there: the cap holds the impossible planets, as in F1 section 1), fresh +1.11 (+0.48 to +1.85, above half of 1.45), alarms 150 / 77 (two under the upside-down limit).
- It fails F1 rule 2 (+2.0 points), so it cannot be frozen alone.
- **Not yet measured, and the obvious next step:** combinations of the three passing releases (dominated, ramp, gap edge). Single prices sum to +3.4 points, but upside-down 53 + 24 + 11 + 5 = 93 would break 79, and flags overlap (X6 learned that the sum understates both sides). This is X11 lever 1.
- NOT TESTED for any candidate here: T156 R (no T156 rescore of these configurations exists), zero-planet identity under the new rule (expected to hold: these are tier rules only, the light is untouched), TOI-1338 b.

## 3. Realistic best P with its interval (LIKELY)
- Without M2, the passing set can at best approach cap + dominated + ramp + gap edge, bounded by rule (b): about +2 to +3 points, so **P about 50 to 51.5% on possible planets (whole-star 95% roughly 46 to 56)**. With an M2 that passes rule 4 (needs a new leftover-eclipse design), about 52 to 53.
- **0.75 lower bound 0.65: out of reach. Gap: about 23 to 25 points.** Even the fresh-seed P of the failing proposal (56.1, 51.6 to 60.5) is 19 points short.

## 4. The single change most likely to close the gap, with its measured ceiling
**The slow-wiggle noise in the too-faint pool (X4), with a tier rule that does not throw the new detections away.** Measured ceiling (Fable X4, CONFIRMED as computed): planets with a crossing at SNR 7+ rise from 64.1% today to 78.9% under white noise, +14.8 points of detection; B keeps about three quarters of detected planets at tier 1, so about +11 points of P. No other measured pool is that large: guard flags behind all soft holds +6.0 (X2 last row, at 139 more real and 58 more upside-down alarms), never-scored crossings about 9 to 10 (RS-037), stacking 2 to 4 (Codex 028 owns it).
- What we know fails: c1a (shorter detrending window) gains the detections (+7.2 points of detection) but loses them at tier 1 (Codex 027: 57.8% to 44.3% of found dips reach tier 1, losses concentrated at 6 to 12 h dips) and adds 84 real and 62 upside-down alarms. So the change is not "shorter window"; it is a noise estimate that follows the wiggles (per-sector, time-local noise in the SNR) plus knowing which flag eats the 6 to 12 h dips. **The second part is a measurement, not a design: attribute the tier-1 losses in 027's saved rows to flags.** That is cheap and decides whether any faint-pool lever can work.
- Honest size: even with this pool half closed, P lands near 0.60 to 0.65 (UNCERTAIN). 0.75 needs nearly every pool closed (RS-037 ceiling 0.71 to 0.74).

## 5. What stays UNCERTAIN or NOT TESTED
- UNCERTAIN: whether the 34 to 57 dump-adjacent and eclipse-like new real events are artefacts or wrongly held signal (no pixel or pointing check run); the per-bin control is my reading of rule (c) from saved rows, not Codex's code.
- NOT TESTED: T156 R and TOI-1338 b for every candidate above; combinations of the passing releases; any M2 variant that passes rule 4.
- The bar-file decision (physical reference planets) still changes every "all 1,098" reading by about 4.5 points; all gains above are on possible planets.

## Plan change
X11 starts with lever 1 = combined rule-4-safe releases (cheap: Fable's scorer, minutes of machine time), then lever 2 = flag attribution of c1a's lost dips if the meter allows.
