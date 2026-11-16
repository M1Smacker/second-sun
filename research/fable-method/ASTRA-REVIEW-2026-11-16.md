# Claude's review notes on Astra's big-run jobs (for Fable's F1 and F2)

## 023, the candidate matrix (merged 15 Nov, 6:06 pm)
- Fence check: frozen files 0, list-star ids in its output 0; fence-id records are Codex reading RESUME text; bench scoring on development light only, as briefed.
- Verdict: **0 GO candidates.** Best P: B+DS 49.98% [45.70, 54.11], but real 204 (over 174) and upside-down 83 (over 79). B alone 48.11%.
- **The most important finding for F1 (Claude's reading, to verify):** the FIX 96 depth cap costs 4.7 P points on the 1,098-planet bench only because 130 of those planted planets are deeper than a 2 Jupiter-radius planet could make on their host star (50 of the 51 lost dips). On the bench where depths are physical (014 part 3) it costs 0 of 264. So either the reference-planet population in G1-PLANET-BAR.md includes planets that cannot exist on large hosts, or the cap is too tight for diluted or misreported radii. Which is right decides whether C96's freed upside-down budget (26) is real. **F1 must settle this first**; any change to the reference population needs a new dated bar file written before the numbers it judges (the bar file says so).
- The dump-excess window from 014 part 1 did not replicate (G2 to G3), so 023 used a conservative 12-hour screen; DS's 30 new real events all sit inside it.

## 024 (big run A2, short-binary light subtraction), reviewed by Claude 15 Nov 9:12 pm; merged
- Verdict: 0 of 2 configurations pass. B+subtraction P 48.52% [44.30, 52.63] against B 48.11%; background real 180 (B 174), upside-down 78 (B 79). In 5 to 10 day binaries detections rise 131 to 141 (change interval [0.41, 8.11], above zero) but tier 1 only 99 to 103 (interval [-1.64, 5.19], includes zero). Other bins unchanged.
- Scatter in changed stars falls 3,273 to 3,008 ppm (8%), much less than the gap to longer binaries (Codex 003: 3,070 vs 2,221 median): the binary's own repeating light is NOT the main cause of the short-binary noise (LIKELY).
- Worst case: a dip at the same binary phase every cycle keeps a median 24% of its depth (expected; drifting crossings are not phase-locked).
- Coverage: subtraction applied to 2,200 of 9,729 star-sectors; 6,232 had fewer than three binary cycles.
- Fence check since 18:05: fence ids only in RESUME text Codex read; search-code runs are the bench runs briefed; no frozen files changed; no forbidden commands.
- For Fable: the 10 extra detections that stay below tier 1 point to the same tier-2 holds (RS-037: dump, step, ramp, repeater); subtraction plus a better tier rule could add a few short-binary planets, but alone it is not a lever.

## Codex 025, load losses (Claude, 16 Nov 2:36 pm; merged e7cda3fb)
- Ran on GPT-6.1-Sol (runner default); the bench was cut by a PC restart at 2:14 am and resumed by Claude at 9:38 am with 4 workers (results unaffected); finished 2:34 pm.
- Root cause CONFIRMED: of 21 T156 load losses, 14 are the stray-light quality bit 4096 alone, 1 is 128+4096, 3 are the QLP late-sector bit 1073741824; 0 are FIX 101 cases.
- Candidate (admit bit 4096) FAILS its preregistered rule: centre support restored 12 of 21 and identity holds on 50 star-sectors, but R falls 34.21 to 31.52, P 48.11 to 45.24, and upside-down background rises 79 to 172 (real 174 to 254). Stray-light cadences are noisy: admitting them adds alarms and loses planets elsewhere. Not a lever as built.
- Across all 2,000 T156 draws, first losses: quality exclusion 148, other eclipse or repeat mask 118, archive gap 99, catalogue drift mask 94 (FIX 101 pool, Codex 026), no safe windows 50, neighbour intersection 42.
- Note to check: this report's B+C96 row shows P 43.44 (from 48.11), while Codex 014 part 3 said the depth cap costs 0 of 264 planted dips. Fable's X10 uses the cap in its proposal; the denominators differ (all 1,098 trials here vs possible planets in X10). Claude checks this before any freeze.
- Fence check since 15 Nov 9:10 pm: 3 FENCE B hits, all one read-only file listing of data/astra/005; no star light opened, no frozen files changed, no forbidden commands.
