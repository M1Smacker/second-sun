# RS-039: can Petrova reach P 75? Strong, broad version (18 Nov 2026; plan 8:45 am, strengthened and STARTED 9:15 am)

Ahmed, 18 Nov 2026, 9:09 am: make the research "stronger and broader", using **5 weekly points or more**, taking hours. **New weekly cap 25%** (it does not have to be reached). Model: **Opus 5.5 high**. After improving the plan, start. Project otherwise stays on hold: research only, no Codex jobs, no hunts, no freezes.

Follows `research/RESEARCH-BLUEPRINT.md`. **Cap written before the start: at least 5 weekly points, target about 8, hard stop at 25% weekly (meter 12% at 9:09 am).** Findings file: `research/stage3/rs039/P75-RESEARCH-2026-11-18.md`. Scripts in `data/rs039/`.

## What is already known (do not redo; build on it)
- P 48.1% (1,098 planted planets), 48.4% (968 possible), set B.
- RS-037: missed planets: 11.6 points detected but held at tier 2, 13.8 never scored, 22.4 too faint. Ceiling of every known lever about 71 to 74.
- Fable X4: planets with a crossing at SNR 7+: today 64.1; white-noise bound 78.9; full-depth bound 71.5; both 83.5. For weak crossings the search noise is 2.59 times the bin scatter; median depth kept 0.76.
- RS-016, RS-024 to RS-038, Fable F1 to F4 and X1 to X11 covered: eclipse masks, dumps, vetting flags, cross-star checks (mono-cbp), jitter, tier rules, c1a, the orbit search.
- **Not yet studied anywhere in the project:** (1) the photon-noise ceiling (how far our light sits above what TESS physically allows); (2) detrending methods that keep transit depth (fitting the trend and the dip together); (3) a red-noise-aware SNR; (4) our own pixel photometry or other light-curve products for our stars; (5) the Kepler DR25 machinery (inverted and scrambled light, Skye, Robovetter scores) as a model for our meters and tiers; (6) machine-learning vetting for single transits; (7) whether our test planets look like real circumbinary planets; (8) what P buys in expected planets compared with searching more stars.

## Part A: our own data (scripts that could contradict me)
- **A1 Ceiling, per planet.** From Fable's X4 rows (per-crossing SNR, depth kept, red-noise factor, bin scatter): what fraction of planets could pass SNR 7 with (a) full depth, (b) white noise, (c) both, (d) stacking all crossings. *Decision:* is 75 reachable on this bench at all, and by which kind of change?
- **A2 Photon floor.** Our bin scatter against a TESS noise model for each star's brightness (the constants come from a primary source). *Decision:* is the noise in the light products (better photometry would help), or in what is left after detrending (better detrending helps)?
- **A3 Loss table.** One table of the 52 lost points on set B, from saved outputs (023, RS-037, X4, X6, X7, F2). *Decision:* the order of work.
- **A4 Bench realism.** Depth, duration and period of our test planets against the known transiting circumbinary planets. *Decision:* does P weight the planets that matter?
- **A5 Value of P.** Expected visible planets as P and the number of stars change. *Decision:* P alone, or P then more stars (Census).

## Part B: primary sources (arXiv abstract and HTML pages; exact sentences; labels)
- **B1 Detrending that keeps depth:** wotan's benchmark (Hippke 2019), the notch filter (Rizzuto 2017), Gaussian-process detrending, Martin and Fabrycky's variable window, fitting the trend with a transit model.
- **B2 Binary light:** subtracting an eclipse model or phase template instead of masking eclipses (Kepler circumbinary searches, the TOI-1338 and TIC 172900988 papers, Windemuth 2019).
- **B3 Red-noise SNR:** Pont, Zucker and Queloz 2006, the beta factor, time-local noise, TLS and BLS false-alarm calibration.
- **B4 Photometry:** TGLC (Han and Brandt), eleanor, QLP precision papers, the TESS noise model (Sullivan 2015, Vanderspek), 200 s FFIs.
- **B5 False-alarm meters:** Kepler DR25 inverted and scrambled light and Skye (Thompson 2018, Coughlin 2017, Christiansen), cross-star and pixel tests for TESS.
- **B6 One vetting score:** Robovetter design and its completeness/reliability trade, LEO-vetter, ExoMiner and Astronet-Triage on TESS, machine learning for single transits.
- **B7 Professional completeness:** what mono-cbp, STANLEY, Windemuth, Kostov's searches and Planet Hunters TESS recover in their own injection tests.
- **B8 Detection beyond one crossing:** CB-BLS (Ofir), QATS-style and photodynamical searches; when stacking pays once the noise is lower.

## Part C: synthesis
- A ranked list of levers, each with a ceiling (measured or sourced), a cost, a risk to false alarms and how our meters would see it.
- A roadmap to 75 (or to the true ceiling) in phases with checkpoints every couple of weeks, and a stop-or-rethink rule.
- Draft bench briefs for the top three levers (Codex runs them later, only on Ahmed's go).

## Rules that stay
No tuning on real events; the upside-down twin stays; every gain is confirmed on a fresh bench; rules 2 and 4 are not lowered without Ahmed's yes; two keys before any freeze; no Codex job, hunt or freeze during this research.
