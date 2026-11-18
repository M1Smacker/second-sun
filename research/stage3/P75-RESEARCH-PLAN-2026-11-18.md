# Research plan: can Petrova reach P 75? (RS-039, PLANNED, not started; 18 Nov 2026, 8:45 am)

Ahmed, 18 Nov 2026 morning: "Plan the research only ... we gotta not let the limit of our tool stop us. Improve our chances of finding a planet with our tool." He is considering a restart whose only focus is P to 75+, even if it takes months. Nothing here runs until he says go. Follows `research/RESEARCH-BLUEPRINT.md`.

## Starting facts (our own files, CONFIRMED as computed unless marked)
- P today: 48.1% on all 1,098 planted planets, 48.4% on the 968 possible ones (set B).
- RS-037: if every pool we know of were closed with today's design, the total would be about 71 to 74 (LIKELY). So 75 is at the edge of the CURRENT design. Getting there means raising the ceiling itself, not just tuning the tier rules again.
- Fable X4: under ideal white noise, 78.9% of planets have a crossing at SNR 7 or more (today 64.1%). A single-crossing SNR-7 search cannot go above about 79 on this bench.
- Measured pools still open (points of P, approximate): too faint because of slow wiggles about +11 (X5); never-scored crossings about 9 to 10 (RS-037); detected but held about 12 (RS-037); multi-crossing stacking 2 to 4 (028 says under 1 for its design).
- Blocked by our false-alarm meter, not by physics: dump-by-shape and mask timing M2 (several points) fail rule 4, because the upside-down twin cannot see dip-only artefacts.

## Questions, each tied to a decision
1. **What is the true ceiling on this bench?** Own data: for every planted planet, the best SNR its crossings could reach at the photon or white-noise limit, and how many crossings the TESS data hold. *Decision:* is 75 reachable on all 1,098, only on the 968, or not at all? Is the goal "75" or "X% of the ceiling"?
2. **Where are the 52 lost points today, in one table?** Own data, one fresh accounting on set B: lost at load, outside windows, under the mask, never scored, too faint, and detected but held (by which flag). *Decision:* the order of work.
3. **Can the noise be lowered at the source?** Literature plus our pixels. Ideas: our own photometry from the pixels (TGLC, which uses Gaia to separate neighbours; eleanor); subtracting a model of the binary's eclipses instead of masking them; detrending that follows the wiggles (wotan methods, Gaussian processes, Martin and Fabrycky's variable window); a noise estimate that changes over time inside the SNR. *Decision:* which noise lever gets the first bench test.
4. **Can a second false-alarm meter unlock the rule-4 levers?** Dip-only artefacts (momentum dumps, scattered light, eclipse leftovers) are invisible to the upside-down twin. Ideas: the same dip at the same moment in many stars (cross-star check); pixel and centroid jitter; Kepler DR25's scrambled light curves next to its inverted ones (Thompson 2018, Coughlin). *Decision:* whether DS and M2 can come back honestly.
5. **Can one score replace the hard holds?** Ideas: Kepler's Robovetter, LEO-vetter, ExoMiner-style scores, tuned on planted planets against inverted and scrambled light rather than a list of yes/no flags. *Decision:* is a tier-rule rebuild worth the "detected but held" pool (about 12 points)?
6. **What do professionals reach?** Injection and recovery in published TESS and Kepler circumbinary searches (Kostov and colleagues on TOI-1338 and TIC 172900988; Martin and Fabrycky STANLEY; the mono-cbp work; BEBOP for context). *Decision:* is 75 a fair target or above the field's own level?
7. **Is P the best lever for finding a planet?** Expected planets scale roughly with P times the stars searched (LIKELY). Compare "P 48 to 65 on 1,200 stars" with "P 48 on 1,200 plus 1,400 Census stars". *Decision:* P only, or P first and then more stars.

## Order, size and cap (cheapest first)
- **Part A, own data (Q1, Q2, Q7): about 1.5 weekly points.** Scripts on saved bench outputs (Astra 006, 023, 027, X4). No new runs of the search.
- **Part B, primary sources (Q3 to Q6): about 3 weekly points.** arXiv abstract and HTML pages only; exact sentences pulled out; labels.
- **Part C, synthesis: about 1 weekly point.** A ranked list of levers, each with a measured or sourced ceiling, a cost, and a draft bench brief (Codex runs the heavy tests later).
- **Total cap: 6 weekly points, written before the start.** This week's cap is 15% and 11% is used, so it fits after the weekly reset (Mon 23 Nov, about 1 am) unless Ahmed raises the cap.
- Model: Ahmed's choice. Opus 5.5 high fits judgement work; reading can go cheaper.

## What would change the plan
- If Q1 shows a ceiling under 75 on the 968 possible planets, the goal is restated before any building.
- If Q6 shows that professionals reach well under 75 for similar depths, 75 is kept only as a stretch goal.

## Rules that stay
Planted planets only (no tuning on real events); the upside-down twin stays; a fresh bench confirms every gain; rules 2 and 4 are not lowered without Ahmed's yes; two keys before any freeze.
