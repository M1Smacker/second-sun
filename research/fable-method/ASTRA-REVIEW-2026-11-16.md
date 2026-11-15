# Claude's review notes on Astra's big-run jobs (for Fable's F1 and F2)

## 023, the candidate matrix (merged 15 Nov, 6:06 pm)
- Fence check: frozen files 0, list-star ids in its output 0; fence-id records are Codex reading RESUME text; bench scoring on development light only, as briefed.
- Verdict: **0 GO candidates.** Best P: B+DS 49.98% [45.70, 54.11], but real 204 (over 174) and upside-down 83 (over 79). B alone 48.11%.
- **The most important finding for F1 (Claude's reading, to verify):** the FIX 96 depth cap costs 4.7 P points on the 1,098-planet bench only because 130 of those planted planets are deeper than a 2 Jupiter-radius planet could make on their host star (50 of the 51 lost dips). On the bench where depths are physical (014 part 3) it costs 0 of 264. So either the reference-planet population in G1-PLANET-BAR.md includes planets that cannot exist on large hosts, or the cap is too tight for diluted or misreported radii. Which is right decides whether C96's freed upside-down budget (26) is real. **F1 must settle this first**; any change to the reference population needs a new dated bar file written before the numbers it judges (the bar file says so).
- The dump-excess window from 014 part 1 did not replicate (G2 to G3), so 023 used a conservative 12-hour screen; DS's 30 new real events all sit inside it.
