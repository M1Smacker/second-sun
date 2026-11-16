# X7: the never-scored pool, in-chain losses (Fable, 16 Nov 2026)

**Verdict in one line: answered by the F2 census, no new run. The "about 600 unnamed crossings" have names now. The largest real cause is the QLP safe-window rule (511 crossings), not "no finite score": that pool shrinks from 248 to 103 once all ten box lengths are tried, as the search does. The one fix that is clean at detector level is the one-neighbour window rule; the tier-level bench for it is the open step.**

Source: `F2-SILENT-LOSSES.md` and `data/fable/f2/` (`census.py`, `summary.py`, `prototype.py`). The census differs from the RS-038 replay in three ways that matter here: it starts from raw cadences (no quality mask), it follows every product instead of the table's best one, and it asks for a finite score at ANY of the ten box lengths.

## The split asked for (planted planet crossings that have raw cadences: 5,914)
| Cause named in the task | RS-038 replay | F2 census | What it is |
|---|---|---|---|
| No finite score | 248 | **103** | 145 of the 248 were a replay artefact (one box length tested). Of the 103: 29 within half a day of the end of the light, 69 inside gaps (a box needs 80% of its bins), 5 between. Mostly physics. Ceiling 0.6 point. |
| Safe windows (QLP) | 235 | **511** | Bigger than the replay saw, because the replay stopped at the first product. Three different rules inside: windows taken from the star's own SPOC file (175: the scattered-light bit again), the intersection of all SPOC neighbours (168), and "no safe windows" when fewer than two neighbours exist (168). Ceiling 3.7 points. |
| Product table has no entry; capture mismatch | 192 + 60 | not a loss | Bench artefacts, confirmed: followed through every product, 58 crossings that 006 called unobserved do reach a score. The real search scans every product. |
| Gap trimming | not split | inside the two rows above | The half-day trim after each window start is part of the neighbour rule; a no-trim intersection would keep 155 of the 336 neighbour-rule losses. |
| Load (quality mask) | 31 | **404** | Invisible to the replay and to the planet bench: 006 only lists crossings that survive the quality mask (F2 section 1). 269 are the scattered-light bit. Ceiling 2.7 points. |
| Eclipse mask | 526 | 507 | 241 in sectors where the mask removed over half the light (FIX 94 = FIX 101, already benched as M2), 159 truly at an eclipse time. |

## Prototype for the largest real cause (from F2 section 4, detector level)
| Rule changed | Crossings rescued (clean SNR 7+) | Strong events per 100 days in the new light, real / upside-down | Today's light |
|---|---|---|---|
| QLP windows from own SPOC file read without the scattered-light bit | 63 of 175 | 13.3 / 12.0 | 2.2 / 1.9 |
| One SPOC neighbour is enough (was: star-sector dropped) | 24 of 126 | 2.3 / 3.1 | about 2 / 1.7 |
| Neighbour intersection replaced by a majority rule | not built (rebuilding windows opens other stars' files: fence) | | |

Failing-first: with the planet planted, the frozen chain scores 0 of these crossings. Reading: the first row is a real rescue at a price nobody should pay unguarded; the second is clean and small (about 0.1 to 0.6 point of P).

## Open step
Tier-level bench of the one-neighbour rule (both arms, adopted set B with the depth cap, untouched background and planted planets in the 94 affected QLP star-sectors, plus every other one-neighbour star-sector of the design set). Pass rule: Tree rule 1 as F1 reads it (upside-down not above 79, real not above 174 after the X10 proposal's 172 / 66, so at most 13 and 2 more), planets up. Not run by me: the planet bench cannot credit it today (its denominator ignores star-sectors the frozen chain drops), so it needs the raw-observable denominator first.

## Labels
CONFIRMED: the counts. LIKELY: ceilings in points and the gain of the one-neighbour rule. NOT TESTED: tier level; the majority rule.
