# X11 lever 1: combined rule-4-safe releases (Opus 5.5 Extra, 17 Nov 2026; bench copies, a proposal, nothing frozen)

**Verdict in one line: found something. C3 = depth cap + ramp hold released + gap-edge hold released PASSES every rule preregistered for this lever, including the new rule 4: +2.66 points on the 968 possible planets (95% +1.65 to +3.78, P 51.07%), confirmed on the fresh seed at +1.56 (+0.76 to +2.45, P 53.74%), alarms 173 real / 73 upside-down, rule 4 excess 3.0, T156 R 34.81 against 34.21. It is the first candidate above +2.0 points that passes rule 4. Two cautions: under F1 section 5 rule 2 as Fable wrote it (+2.0 on the FRESH bench) it falls short (1.56); and its gap-edge part carries about 13 unmirrored real events. Far from 0.75 either way.**

Pass rule preregistered in `WORK-LOG-X11.md` (5:40 pm, amended 5:41 pm before any score). Scorer: Fable's X10 scorer copied to `data/opus-x11/` (`x11_score_orig.py`, `_fresh.py`, `_freshm2.py`; writes only to `data/opus-x11/out`), summary `x11_summary.py`; copies in `research/fable-method/opus-x11/`. Checks that could have failed and did not: identity against Codex 013 on all 1,098 choosing-bench trials and all 2,000 T156 trials (B and DS trial by trial); B reproduces 174 / 79, P 48.40 (968) and T156 reference R 34.21; every single-release row reproduces X5 exactly.

## Table (CONFIRMED as computed)
All with the depth cap. Change in points against B, paired, 95% whole-star. Alarms on the untouched background. R = T156 reference R (B 34.21).

| Configuration | P 968 | Change 968 | Change 1,098 | Fresh change | Real / upside-down | New real / new upside-down | Rule 4 excess | R | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| C1 dominated + ramp | 51.17 | +2.77 (+1.72 to +3.88) | -2.12 | +1.65 (+0.88 to +2.51) | 168 / **89** | 44 / 36 | -38.8 | 34.37 | fails (b) |
| C2 dominated + gap edge | 50.67 | +2.27 (+1.37 to +3.23) | -2.58 | +1.65 (+0.88 to +2.53) | 169 / **84** | 45 / 31 | -26.3 | 32.06 | fails (b), (d) |
| **C3 ramp + gap edge** | **51.07** | **+2.66 (+1.65 to +3.78)** | -2.23 | **+1.56 (+0.76 to +2.45)** | **173 / 73** | **49 / 20** | **3.0** | **34.81** | **PASSES the preregistered rule** |
| C4 all three | 52.41 | +4.01 (+2.78 to +5.31) | -1.03 | +2.67 (+1.67 to +3.75) | 208 / **101** | 84 / 48 | -26.4 | 34.81 | fails (b) |

Per-bin own dip-minus-bump control (rule c, 99%): passes for all four on the 968 and the 1,098; fresh: passes for all four (fresh B reproduces 52.18; the single releases reproduce X5's fresh rows).
M2 rows were scored for information only and cannot pass (preregistered). They would fail anyway: C3 + M2 gives 193 / 77, new 78 / 24, excess 22.8 (real over 174 and rule 4); C1, C2, C4 + M2 give 189 / 93, 187 / 88, 230 / 106 (upside-down over 79).

## Which rule wins where (said plainly, for the second key)
- Preregistered rule of this lever (Codex 027's five plus X1's fresh rule): (a) +2.0 on the 968 with the interval above zero: 2.66, PASS; (a2) fresh interval above zero and point at least half: 1.56 against 1.33, PASS; (b) PASS; (c) PASS; (d) PASS; (e) PASS.
- F1 section 5 rule 2, read literally ("paired change on the fresh bench ... at least +2.0 points"): 1.56, FAIL. I wrote the lever's rule from the brief ("same five rules as Codex 027"); the stricter reading is the main session's and Ahmed's call, not mine. Winner's curse is visible: three to four configurations were scored and the fresh gain is 59% of the choosing gain (Fable's releases shrank about a third, X1).

## What C3 is, in plain words
B plus the depth cap, plus two holds switched off: the ramp hold (a dip sitting on a slow slope) and the gap-edge hold (a dip near the start or end of a data gap). The dump hold stays as it is. It is R1 of X6 without the dump-shape rule (DS), which is the part that broke rule 4.

## Honest reading
- C3 is the first candidate above +2.0 that passes every freeze rule measurable on saved outputs, including the new rule 4. Its margins are thin: real alarms 173 against 174, rule 4 excess 3.0 against 5, and the gain point +2.66 against the +2.0 bar.
- **The gap-edge part carries an unmirrored pile (UNCERTAIN, same trap as F1 section 3):** 34 of the 49 new real events sit near a data-gap edge against 9 of the 20 new upside-down ones; at the usual 2.3 ratio about 21 would be expected, so about 13 real gap-edge events have no mirror. Rule 4 passes overall only because the ramp release adds upside-down events too. Gap edges after downlinks carry thermal settling that is not sign-symmetric; a pixel look at the 34 is the check (NOT RUN).
- The cap alone lowers R (34.21 to 32.06); the ramp release gives it back (34.81). So in C3 the T156 pass comes from the ramp part.
- On the bar's current 1,098 bench C3 reads -2.23 (the cap holds the 130 impossible planets, F1 section 1). Under today's bar file it is not better than B; under a physical bar file it is. The bar-file decision is still Ahmed's first.

## Not tested
TOI-1338 b under C3 (F1 rule 8); zero-planet identity on class A star-sectors (expected: tier rules only, the light is unchanged); the pixel check of the 34 gap-edge real events; a narrower gap-edge release.
