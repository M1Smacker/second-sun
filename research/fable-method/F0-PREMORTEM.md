# F0 pre-mortem: how this run could produce a FALSE breakthrough (Fable, 16 Nov 2026, 9:55 am Kuwait)

Written before any F1 number was computed. P is the planet-level recovery on the fixed 1,098 reference planets (bar file `research/stage3/G1-PLANET-BAR-75-2026-11-15.md`). Today: adopted set B, P 48.1% (43.9 to 52.2).

## 1. Winner's curse: the best of eight on the bench that chose it
- **How it fakes a win:** 023 scored eight combinations on one planet bench. The top row is partly top by luck. With a 95% interval of about plus or minus 4 points, the pick can sit 1 to 2 points above its true value, enough to cross 0.50 (B+DS missed by 0.02 points) and it would look like progress toward 0.75.
- **Check that catches it:** (a) choose the combination from mechanism and a rule written before looking at the fresh numbers; (b) score it on a FRESH planet bench (new seed, new planets, same rules) and judge only the fresh number; (c) judge the PAIRED change against B on the same planets (interval of the difference), never two separate P values.
- **Stop sign:** any sentence "X reaches P of ..." that uses the choosing bench.

## 2. A better P from a changed denominator, not from more planets found
- **How it fakes a win:** 130 of the 1,098 planted planets are deeper than a planet of 2 Jupiter radii could be on their host star (023). Dropping them, or re-drawing their depths, moves P by composition alone. The same holds for dropping "bench capture gap" crossings (RS-038: best-product table has no entry for 192 crossings) or for counting planets on a new definition of "found" (looser match window, novelty rule changed).
- **Check that catches it:** every P is reported on the ORIGINAL fixed 1,098 with the 023 novelty definition. A sensitivity on another population is printed beside it, labelled, and never compared with the 0.75 bar unless a dated bar file defined that population first. For each claimed gain, list the planets gained and lost by id (a gain is a count of the same planets changing from missed to found).

## 3. Planets freed by opening a door the upside-down meter cannot see
- **How it fakes a win:** Tree rule 1 counts upside-down alarms. Some false alarms only exist as DIPS (eclipse leftovers at wrong catalogue times, pre-dump pointing dips, stray light ramps down). A change that releases them shows "more planets, no more upside-down alarms" while real-arm false alarms rise: DS adds 30 real events, all near dumps, and only 4 upside-down; mask-timing variants add 24 to 29 real and 3 upside-down (023). In G1 those extra real events are the cost: each one is a false lead.
- **Check that catches it:** real background is a gate too (not above B's 174, or new real events classified one by one); per-bin real against upside-down counts on the untouched background; for any mask or window change, a residue control (new real events within 0.3 d of predicted eclipses against the upside-down arm) and the zero-planet identity check (untouched star-sectors give the same events).

## Smaller traps, same family
- **Ceiling quoted as gain.** "Up to 64 planets", "11.6 points held" are pools, not gains. Only a bench-measured paired gain counts; a pool is quoted with the word ceiling and its realistic share.
- **Injection after the step under test.** A fix to load, windows or mask can only be judged with planets put into RAW light before that step, and with both arms rerun; a saved-event replay cannot see it (lesson F-01, 10 Nov).
- **Old chain against new chain.** RS-037 pools come from the 006 captures (older chain) joined to B. A pool can be partly already recovered by B. Re-count on B before sizing a lever.
- **Too narrow intervals.** Star-sectors of one star are correlated; only whole-star bootstrap intervals are used. A number inside its interval of the bar is "borderline".
- **A prototype that passes its own test only.** Each fix shows a failing-first test, a mutation check, and a zero-difference identity on untouched star-sectors.
