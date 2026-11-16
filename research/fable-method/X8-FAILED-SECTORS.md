# X8: star-sectors that fail to prepare (Fable, 16 Nov 2026)

**Verdict in one line: answered from the F2 census and from Codex 010's replays, no new run. The two failure messages have two different causes. "Too little data after masking" is the eclipse-mask padding (FIX 94 = FIX 101): reclaimable, already benched as M2 (+1.4 points), and it does let eclipse leftovers in. "No safe windows" is a counting rule about SPOC neighbours: three quarters of it is reclaimable cleanly by accepting one neighbour.**

## 1. "Too little data after masking" (143 crossings in RS-038; 166 in my census with over 90% of the sector masked, 75 more with 50 to 90%)
- Why it fails: `pipeline/petrova_mask.py` `windows()` widens every eclipse window by `3 x sqrt(eT0^2 + (n x eP)^2)`. On stars with a bad catalogue period error the windows grow until they cover the orbit; fewer than 200 points survive and the star-sector is dropped (F1 section 4; RS-038).
- Is a safe change available? Partly. M2 (window at the sector's own measured offset, padding capped at the eclipse width) is benched: +1.36 points of P (+0.43 to +2.44) with the depth cap, background 139 real / 56 upside-down against 124 / 53.
- The eclipse-residue count the task asks for: counting new real events "within 0.3 d of catalogue eclipses" cannot work here, because on these stars the catalogue time and period are the thing that is wrong. Codex 023 found only 1 to 2 of M2's new events near a catalogue eclipse. Read row by row, at least 14 of the 24 new real events are eclipses at times the catalogue does not predict (F1 section 3), against 3 new upside-down events. So the honest residue count is 14 or more of 24, not 1.
- What makes it safe: the leftover-eclipse check of F1 section 4 (hold a star when a leftover dip is deeper than a planet can make, or when three or more similar events fit one strict period), with the fallback radius for stars with no catalogue radius. NOT BUILT.

## 2. "No safe windows" (165 crossings in RS-038; 168 in my census)
- Why it fails: a QLP light curve is searched only inside windows borrowed from SPOC stars on the same sector, camera and CCD. `stage2_search.prepare` drops the star-sector when the star has no SPOC file of its own and fewer than TWO such neighbours exist in the campaign's files. 126 crossings sit in star-sectors with exactly one neighbour, 42 with none.
- It is a rule about which files happen to be in the campaign, not about the light: a bigger campaign has more neighbours (and then the intersection rule bites instead, F2 rank 4).
- Safe change, prototyped at detector level (F2 section 4): accept one neighbour. 106 of the 126 crossings get a score, 24 are clean detections, and the 1,600 days of light that come back show a normal rate of strong events (2.3 real and 3.1 upside-down per 100 days against about 2 and 1.7). Catalogue eclipses are still masked by the same mask as everywhere else, so this change adds no new eclipse-residue path of its own.
- The 42 crossings with no neighbour at all: no safe change proposed. QLP's own quality flag is the only guard left there, and raw QLP outside SPOC windows is known to be dirty (the reason the rule exists).

## 3. Size
- Planets: mask padding about 1.4 points (measured, inside the X10 proposal already); one-neighbour rule about 0.1 to 0.6 point (LIKELY, detector level).
- Neither is visible in today's P for the second case: a star-sector the frozen chain drops is not in the bench's "observed" list (F2 section 1).

## Open steps
1. Build the leftover-eclipse check for M2 and rerun its controls (F1 section 4).
2. Tier-level bench of the one-neighbour rule (see `X7-NEVER-SCORED.md`).

## Labels
CONFIRMED: causes (code read, counts from the census). LIKELY: the gains in points. NOT TESTED: tier level for the one-neighbour rule; the leftover-eclipse check.
