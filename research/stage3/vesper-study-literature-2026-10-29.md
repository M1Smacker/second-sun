# Vesper study, phase B: what published work says (29 Oct 2026)

Research by Claude (Opus 5.5) with web search, about 15 minutes, stopped when each question had an answer that feeds a decision. Labels: CONFIRMED = stated in the source's own abstract or documentation as returned by the search; LIKELY = stated by a secondary page or my reading; UNCERTAIN = not checked at the primary source. I did not open full papers (PDF links are not opened in the browser pane); where a number matters for a decision, the primary text is marked "to open".

## Q1. How big are the known transiting circumbinary planets, and what does that mean for TESS?
- About a dozen to fifteen transiting circumbinary planets are known (LIKELY; a talk abstract says "a dozen", Davies et al. 2026 test on 14 known planets).
- The smallest is Kepler-47 b at 3.0 Earth radii; Kepler-38 b is 4.35 (CONFIRMED, discovery abstracts: [Kepler-47, arXiv:1208.5489](https://arxiv.org/abs/1208.5489), [Kepler-38, arXiv:1208.3712](https://arxiv.org/abs/1208.3712)). Transiting circumbinary planets sit mostly at large radius (LIKELY, figure in [Kostov et al. 2021, arXiv:2105.08614](https://arxiv.org/abs/2105.08614)).
- Their periods are much longer than a TESS sector; TIC 172900988 b was found from two transits 5 days apart in ONE sector, one over each star (CONFIRMED, same paper).
- **Decision fed:** "smaller" for Vesper means from about Jupiter size down to Saturn, and Neptune size (about 4 Earth radii) only on quiet stars; 3 Earth radii needs Kepler-length data and stacking. Our own loss ledger: a planet of period 100 d gives a median 1.5 transits per G2 dev star; 16 transits (halving the radius by stacking) is reached by no star at 100 d.

## Q2. How to smooth without eating long transits?
- Wotan (Hippke et al. 2019): the biweight is the best general choice; a window about 3 times the transit duration keeps the transit; the documentation says 2 to 3 times (CONFIRMED in the [wotan documentation](https://wotan.readthedocs.io/en/stable/Interface.html); the 3 x result is from the paper, [arXiv:1906.00966](https://arxiv.org/abs/1906.00966), LIKELY, to open).
- For searches over many durations the window must follow the duration being tested (LIKELY, [PLATO TLS survey IV, arXiv:2206.02071](https://arxiv.org/abs/2206.02071)).
- Even a good biweight lowers transit SNR on active stars; fitting the transit and the variability together does better ([nuance, Garcia et al., arXiv:2402.06835](https://arxiv.org/abs/2402.06835); LIKELY).
- **Decision fed (H2, C1):** Vesper's 2 d window is 2.4 x a 20 h box (inside the 2 to 3 x band) but 6 x a 8 h box. Phase A found that detection itself is fine for long dips (about 90% seen at 10 x noise); the loss comes from the flags, so C1 should test a duration-scaled window TOGETHER with the step test, not alone.

## Q3. How do circumbinary searches handle single transits?
- mono-cbp (Davies et al. 2026, [arXiv:2604.09435](https://arxiv.org/abs/2604.09435)): removes eclipses, detrends, vets single events in TESS eclipsing binaries; recovers each of 14 known planets at 50% or more of its transits, over 75% for 9 of them; one new candidate (CONFIRMED by a secondary summary; we already hold this paper's numbers).
- Circumbinary transits are NOT periodic: they shift by days and their durations change by hours with the binary phase (CONFIRMED, Kepler-47 abstract; mechanism in [STANLEY, Martin and Fabrycky 2021, arXiv:2101.03186](https://arxiv.org/abs/2101.03186)). A planet can transit two or three times within one conjunction (Kostov et al. 2020, "multiple transits during a single conjunction", LIKELY).
- Small planets are found by STACKING many shallow transits of varying interval and duration with N-body predictions: STANLEY could have found planets under 3 Earth radii in about half of the Kepler circumbinary systems, using 4 years of Kepler data (CONFIRMED, abstract).
- A 2026 TESS search of M-dwarf eclipsing binaries reports one candidate and an occurrence upper limit (Oddo et al., said to be arXiv:2610.22625; UNCERTAIN: the arXiv entry was not found; to open). It is the closest published model of our "clean measured null".
- **Decisions fed:** (a) the repeater flag (3 or more events in one product and sector) and any stacking must allow 2 to 3 genuine transits within one conjunction; (b) the orbit-locked flag must only fire on dips that recur at the same binary phase in DIFFERENT sectors, which a planet does not do; (c) injections should include duration changes of several hours (FIX-QUEUE 28); (d) stacking in TESS helps only short-period planets on many-sector stars (H4 stands).

## Q4. How to vet without blunt yes/no vetoes, and how to calibrate false alarms?
- Kepler DR25: the pipeline was re-run on inverted light curves (our upside-down control) and on scrambled ones to measure false alarms, and these sets were used to tune the Robovetter's pass/fail thresholds; a Disposition Score lets users trade completeness for reliability (CONFIRMED, [KSCI-19114-002](https://exoplanetarchive.ipac.caltech.edu/docs/KSCI-19114-002.pdf) and [DR25 KOI companion](https://exoplanetarchive.ipac.caltech.edu/docs/Q1Q17-DR25-KOIcompanion.html), via search summary).
- At long period and low SNR the metric values of false alarms and real signals overlap, so no clean cut exists; reliability must be corrected statistically ([Bryson et al. 2020, arXiv:2006.15719](https://arxiv.org/abs/2006.15719); LIKELY).
- **Decision fed (H1, C4):** a single calibrated score (positives = injected planets through the whole chain; negatives = upside-down events), with the operating point chosen at the yardstick false-alarm rate, is the established approach. Our scrambled control was withdrawn (FIX-QUEUE 6) because single dips survive scrambling; the inverted control alone is what Kepler also relied on for single-event false alarms.

## Q5. How long is a circumbinary transit?
- The duration depends on the binary phase at the time of transit (the star's own motion adds to or subtracts from the planet's); STANLEY uses a simple formula for circular orbits and zero impact parameter (CONFIRMED, abstract-level). Kepler-47 durations vary by several hours; a single Kepler-47 transit of about 4.15 h is discussed in a later paper (LIKELY).
- **Decision fed (H5, C5):** a physical box-length range per star is possible (planet speed from Kepler's law around the total mass, plus or minus the star's orbital speed, over the star's size), but G2 has no stellar radius or mass; the range would need TIC radii (a MAST query, a download that needs Ahmed's yes) or a wide default. Priority: below C1 to C4.

## What changes in the plan
1. Phase C order: C2 (fair step test) together with C1 (duration-scaled smoothing) first; then C3 (gap rule); then C4 (calibrated score); C6 (orbit-locked) with the same-conjunction exception; C5 last.
2. FIX-QUEUE 28 (injected shape) moves up: injections with durations changed by up to a few hours, and pairs of transits within one conjunction, before judging the repeater or orbit-locked rules.
3. Stacking (phase D) stays second: it can only help planets with periods of about 50 d or less on stars with many sectors.
