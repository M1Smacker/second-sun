# Compass review: Gemini's fact-check and research answer (2026-10-23)

*Review only, nothing built. Every citation was looked up in ADS by Claude (API, key not printed). Our own code was read (`pipeline/detect_v2.py`) and the TESS quality bits were decoded with lightkurve. Labels: VERIFIED (ADS record or abstract read, or our own code/run), LIKELY, UNVERIFIED, WRONG, INVENTED.*

## Verdict: REVISE (keep five things, reject the rest)

## Citation check (12 checked)
| Citation as given | Result |
|---|---|
| Welsh et al. 2015, ApJ 809, 26 (Kepler-453 b) | VERIFIED. Abstract: precession about 103 years, transits visible about 8.9% of the time, about 11.5 hidden systems per one seen. |
| Davies et al. 2026, MNRAS 548 (mono-cbp) | VERIFIED. Real, and we already had it (wave 1, A21: 512 detached Prša 2022 EBs, P > 7 d, through Sector 79; 1 weak candidate). New to us from its abstract: on Kepler long-cadence data it recovered at least 50% of transits for every known planet and over 75% for 9 of 14. |
| Eisner et al. 2021, MNRAS 501, 4669 (Planet Hunters TESS II) | VERIFIED. Abstract: volunteers plus clustering recovered 85% of TOIs larger than 4 Earth radii and 51% at 3 to 4. |
| Seager and Mallen-Ornelas 2003; Doyle et al. 2011 | VERIFIED (records exist; cited for general points). |
| Pont et al. 2006 | Real paper (2006MNRAS.373..231P) but the DOI given belongs to a galaxy-groups paper. |
| Martin and Fabrycky 2021 (STANLEY) | Real paper (2021AJ....162...84M) but the arXiv id given is a string-theory paper. |
| Kostov et al. 2020 (TOI-1338) | Real (2020AJ....159..253K); the DOI given did not resolve in ADS. |
| Fischer et al. 2012 | Real, but it is the first two Planet Hunters candidates; its abstract has none of the "95% at SNR 8, under 50% at SNR 5" numbers. Numbers UNSUPPORTED. |
| Conroy et al. 2014 | Real, but about close (short-period) binaries; G1 has binary periods over 5 days. Wrong population. |
| Oddo and Dragomir 2026 | Real, but a catalogue of M-dwarf eclipsing binaries, not a circumbinary occurrence-rate search. |
| "Popcorn et al. 2024, PASP 136, 024401" | INVENTED: no such author or page in ADS. |

Tally: 5 clean, 6 real papers with a wrong identifier or wrong content, 1 invented. Its [OPENED] tags and "Confidence: High" labels are not reliable (generic domains such as harvard.edu were tagged as opened sources; it also called our public repo "private").

## Keep (useful, now checked)
1. **A benchmark for the Kepler re-find test**: Davies et al. recovered at least 50% of known transits per planet in Kepler long-cadence data, over 75% for 9 of 14 (VERIFIED abstract). Our test can be scored against that. Their abstract also says recovery depends strongly on transit duration, so the test should include durations below our 3-hour lower limit.
2. **A benchmark for Eyes mode**: Planet Hunters TESS recovered 85% of TOIs above 4 Earth radii and 51% at 3 to 4 (VERIFIED abstract; note this is many volunteers plus clustering, not one person).
3. **Eclipse wings as a false-alarm source** (Gemini's B10, NOT TESTED). Claude's addition: our upside-down control cannot see this, because flipping turns eclipse residuals into bumps. Cheap check: plot our events against binary phase; a pile-up near eclipses means leakage.
4. **Do not mask quality bit 4096 blindly**: consistent with our own experiment (restoring those cadences found two missed crossings but lowered SNR elsewhere). Bits decoded with lightkurve: 2048 "Straylight", 4096 "Straylight2" (VERIFIED).
5. **Kepler-453 b numbers** confirm our F-009 (8.9% of the time, 103-year cycle).

## Reject or correct
- **"The biggest thing you have wrong: a fixed-width linear-period box filter and folding"** is false about us. `detect_v2.py` searches every crossing on its own with boxes of 3 to 15 hours; it uses no period and no folding (VERIFIED, code). Gemini could not open the repo and misread the brief.
- **Rank 1 "velocity-aware variable window, +35%"**: our box widths already span 3 to 15 hours; the 35% is unsourced. The real, smaller gap is short durations (point 1 above).
- **Rank 4 "red-noise-aware SNR, false alarms from 0.6 to under 0.05 per sector"**: already done (our noise is the spread of box-sized means, which includes red noise); the 0.05 is invented.
- **Rank 6 "drop high-RUWE stars as unstable triples"**: not standard, and PH1 b orbits in a four-star system (F-059). At most a ranking flag, never a filter.
- **B10 "calibrate on 100 normal stars"**: the wrong control for the risk it names; normal stars have no eclipses. The phase check (point 3) is the right one.
- **B2 "1 to 2% occurrence, so 5 to 15% odds"**: the 1 to 2% is not in the cited paper. Not usable as evidence.
- **B7 "a box search misses over 60% of transits", "Kepler-34/35 chaotic"**: unsourced.
- **B9 "the pipeline author is entitled to first authorship"**: not a rule; overconfident.
- **B3 "PDCSAP eats transits (Davies 2026)" and Rank 2 "2 to 3 times lower noise"**: the 2 to 3 times is our own number repeated back; no source shown. Our SAP result stays one star, cause unknown.

## Decisions taken in this review (Claude)
1. Filed this review. No code, book or register changes.
2. Nothing from Gemini enters the claims register unless Claude checks it first. Proposed new claims (not yet added): Davies et al. 2026 Kepler recovery rates; Eisner et al. 2021 volunteer recall (both LIKELY: abstracts).
3. Odds: no new evidence from Gemini, but re-reading Davies' result (1 weak candidate from 512 comparable binaries) moves Claude's estimate from about 20% to about 15% (range 4 to 35%) for at least one real candidate from G1. It goes up if most G1 stars turn out to be outside the Davies sample or our extra sectors add many crossings; down if the Tufts/Martin TESS project covers the Kepler field.

## Effect on the next steps (Ahmed's go needed)
- Kepler re-find test on Kepler-16, 34 and 35: stronger case now; score against Davies' 50% / 75% benchmark, and add short durations.
- Add the eclipse-phase false-alarm check to the same run (cheap).
- Eyes mode upgrade (two-sun-like fakes, several stars): unchanged; Planet Hunters TESS gives a yardstick.

## Lesson
A research assistant that can open more sites still needs checking: 7 of 12 citations had a problem, and 1 was invented. The Compass step caught all of them in one ADS pass.
