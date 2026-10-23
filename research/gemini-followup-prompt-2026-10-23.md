# Follow-up brief for Gemini (one-time), written 2026-10-23

*Purpose: Gemini can open sites and databases that Claude cannot. Ahmed pastes this into the same Gemini chat. Whatever Gemini answers goes through Compass (review only) before anything is built. The review that led to this is `compass-reviews/2026-10-23-gemini-plan.md`.*

---

You are my skeptical research assistant with live web access. This is a one-time brief. Please do three things in order: (A) fact-check your own earlier answer, (B) research my open questions properly, (C) tell me how to improve my work. I am a beginner citizen scientist (Ahmed), so use plain English, but be precise. I need you because my other assistant (Claude, who writes my code) cannot open many websites and databases, and you can.

HOW TO ANSWER (important)
- Tag every factual statement: [OPENED] = you opened the source in this session and it says this; [MEMORY] = from memory, not opened; [UNSURE] = you are guessing. Never invent a citation, URL, quote or number. If you cannot open something, write "could not open" and give the exact search query or page I should check.
- For each source give: authors, year, title, journal or ID (arXiv, DOI or ADS bibcode), URL, the date you accessed it, and the exact table, figure or sentence you relied on (a short quote under 15 words is fine).
- No flattery. Challenge our plan. If something we do is wrong or pointless, say so first.
- Tables are welcome. No code unless I ask. Keep the whole answer under about 2,500 words and do not pad.

WHAT WE ARE BUILDING (Second Sun)
Goal: find a new transiting circumbinary planet (a planet orbiting two stars) in public NASA TESS data. 14 are known to transit: 12 from Kepler and 2 from TESS (TOI-1338 b and TIC 172900988 b) [from our register, citing Davies et al. 2026; please verify the count]. Public repo (MIT): https://github.com/M1Smacker/second-sun . Teaching book: https://m1smacker.github.io/second-sun/ (you may open both).

Campaign "G1": 549 Kepler eclipsing binaries (Villanova Kepler EB catalog, revision 2019-08-08; selected: morphology < 0.5 meaning detached, binary period > 5 d, TESS magnitude <= 13.5) that TESS has re-observed since 2018. The idea: orbital precession may have tipped a planet into view since Kepler. All 549 have QLP light curves, 275 have SPOC 2-minute, 312 have TESS-SPOC. Nothing from the real G1 stars has been searched yet. One dry run on Kepler-16 flagged one dip, and on inspection it was spacecraft wobble before a thruster firing.

Our detector (v2): load PDCSAP flux (gaps filled from scaled SAP), drop cadences with the "hard" quality mask, mask the binary's eclipses (re-found per sector), flatten with a 2-day biweight, bin to 10 minutes, run a matched box filter for durations 3 to 15 hours, estimate noise as the robust spread of box-sized means (so red noise is included), call an event at SNR >= 7, and always run the same search on an upside-down copy of the data as a false-alarm control. For long periods, STANLEY (Martin and Fabrycky 2021, MIT licence) stacks N-body-timed transits; we have not calibrated its score.

What we have measured (VERIFIED by us, mostly on ONE star, TOI-1338, so treat it as thin evidence):
- Re-found the known planet TOI-1338 b in 4 of the 8 sectors where it crosses; the missed crossings had SNR 3.7 to 6.5.
- Injected fakes (realistic transit shape, N-body timing) into 40 TOI-1338 sectors: found 0 of 10 at 4 Earth radii, 8 of 10 at 6, 10 of 10 at 8. The floor is about 6 Earth radii at Tmag about 11.5, and worse for the fainter G1 stars.
- False alarms: on upside-down TOI-1338 data the detector still reports 6 events at SNR >= 7 in 10 sectors (peaks up to SNR 12.6).
- Noise depends hugely on the method. Kepler-16 sector 82, 1-hour scatter: 229 ppm (lightkurve quick estimate), 542 ppm (NASA CDPP in the file header), 573 ppm (0.25-day flatten), 908 ppm (our 2-day flatten).
- SAP versus PDCSAP on TOI-1338: SAP gave a 2 to 3 times smaller noise estimate than PDCSAP in 3 sectors (S6, S34, S37) with the same transit depth, cause unknown. PDCSAP is NaN on cadences with quality bit 4096 (we believe "scattered light") while SAP is finite there; restoring them found two published crossings we had missed but lowered SNR elsewhere.
- Circumbinary transits do not keep time: the gaps differed by days, much longer than a crossing lasts, so folding on one period smears them.

Rules we follow: nothing is announced or sent to anyone until two keys (Ahmed and Claude) agree and a write-up exists; candidate data stays private; ExoFOP is read-only for us until we publish (we recorded that ExoFOP paused uploads on 2026-03-31 and reopened them on 2026-08-19 with a publish-first rule).

PART A. FACT-CHECK YOUR EARLIER ANSWER
For each claim give: verdict (Correct / Partly / Wrong / Cannot verify), the correction, and a source. My other assistant's note is in brackets.
A1. "Nodal precession means planets invisible to Kepler could be transiting TESS now; use Kepler as a baseline to predict TESS variations." [Plausible in principle (Kepler-453 b transits only about 8% of the time, from memory), but we cannot predict anything for unknown planets. Any real example of a planet appearing years later?]
A2. "AI filters 99% of the baseline noise but struggles with false positives." [Our detector is a matched filter, not AI, and still makes about 0.6 fake dips per sector. Where does 99% come from?]
A3. "Visually inspect the folded light curves." [We think this is wrong for circumbinary planets because timing shifts exceed the transit duration. What do professionals actually inspect when vetting a circumbinary candidate?]
A4. "V-shaped means a binary star, U-shaped means a planet." [Grazing planets can look V-shaped and limb darkening rounds the bottom. How reliable is the rule? Source please.]
A5. Your named resources: Chandra Interactive Learning, "NASA's Universe Unplugged", Planetary Society open guides on light curves. [Do these exist and teach transit photometry? Give working URLs. Chandra is an X-ray mission.]
A6. "Build everything on Lightkurve; it removes spacecraft jitter and is the gold standard for flattening." [We use it only to load data. Its quick noise estimate understated our real noise by about 4 times. Is its flatten or CDPP safe for multi-hour transits?]
A7. "Look up the TIC on ExoFOP to see if a team marked it an eclipsing binary or false positive." [All 549 stars are known eclipsing binaries by construction, so that tells us little. What on ExoFOP is actually useful for a Kepler EB: TOI dispositions, CTOIs, notes? Also verify the 2026 pause and publish-first rule above.]
A8. "Test on the 14 known Kepler circumbinary planets; if the code cannot flag them in TESS it will not find new ones." [We think 14 is the total (12 Kepler plus 2 TESS), and a Kepler planet may not transit in the TESS years, or its host may be too faint. Which known circumbinary planets have TESS data, at what magnitude, and are transits expected in TESS sectors? Any published TESS recovery or non-recovery?]
A9. "Planet Hunters TESS Talk has advanced threads with custom Python and anomalous light curves." [Verify, with links to real threads. What are the rules and norms for posting candidates and for co-authorship?]
A10. "Exoplanet Watch mostly needs data reducers and offers NASA mentors." [Verify. We think it times known transiting planets with small telescopes, so it fits our hunt poorly. Is that right?]
A11. "Have Claude inject a fake planet into a real TESS light curve and find it by eye." [We built exactly this as a practice game. Is there literature on human detection rates versus depth and noise that we can use to calibrate it?]

PART B. RESEARCH THESE PROPERLY (answer each in under 120 words, with sources and a confidence tag)
B1 Novelty and competition: who has searched TESS for circumbinary planets (Kostov and colleagues, Planet Hunters TESS, Visual Survey Group, systematic EB searches)? Has anyone searched Kepler EBs re-observed by TESS, as we plan? List 2022 to 2026 papers and preprints. Are our 549 stars already covered?
B2 Odds: occurrence rates of circumbinary planets around close binaries, predictions for TESS yields, and the effect of precession on visibility. Give numbers with sources so we can sanity-check our own guess (about 20% chance, range 5 to 40%, of one real candidate from G1).
B3 Noise: best practice for detrending eclipsing-binary light curves while keeping multi-hour transits: eclipse masking versus modelling and subtracting the binary, biweight window versus transit duration, Gaussian processes, red-noise-aware SNR (for example Pont et al. 2006), the right choice between SAP and PDCSAP for bright EBs and why PDCSAP might be noisier, and the correct TESS quality-flag definitions (is bit 4096 scattered light? what does bit 2048 mean?) with a recommended mask. Also SPOC versus QLP versus TESS-SPOC for faint stars, and known TESS systematics.
B4 Detection: STANLEY's known limits and calibration; other published circumbinary search methods; how to handle single or two-transit events when the planet period exceeds a 27-day sector; any open-source tool with an MIT-compatible licence.
B5 Vetting: standard tests for circumbinary candidates (odd-even, eclipse-timing variations, centroid shift, duration versus phase, photodynamical fit), and which free tools work with two stars (triceratops, LATTE, DAVE; note which assume a single star). Typical false positives specific to circumbinary signals.
B6 Prioritising targets: could eclipse-timing-variation catalogues, Gaia RUWE, Kepler EB catalogue flags (third light, period changes) or known unconfirmed circumbinary candidates help rank the 549 stars?
B7 Kepler re-find test (our likely next step): where to get Kepler light curves of Kepler-16, Kepler-34 and Kepler-35 (MAST product and cadence to use), published transit times to use as the answer key, how many transits each has, and which cleaning to use. What fraction of known circumbinary transits would a 3 to 15 hour box search catch at Kepler's noise? Any published recovery tests?
B8 Human detection: literature on volunteer recall versus depth and SNR (Planet Hunters), good designs for a training game with hidden known examples, and how many trials give a meaningful hit rate.
B9 Publishing and credit: confirm current ExoFOP rules, the RNAAS route, AI-disclosure rules at MNRAS, A&A and AAS journals, and norms for crediting citizen scientists.
B10 Blind spots: what would a professional circumbinary researcher say is the weakest link in this plan? What is the cheapest experiment that would most reduce our uncertainty?

PART C. HOW DO WE IMPROVE THE WORK
Give a ranked list of at most 10 concrete changes to (1) lower noise and raise sensitivity, (2) cut false alarms, (3) validate honestly, (4) use a human's eyes well. For each: what to change, why (source), expected gain in plain numbers if known, effort (hours or days), and risk. Mark each as [STANDARD PRACTICE] or [YOUR IDEA]. Add a short "do NOT do" list.

END YOUR ANSWER WITH
1. A list of everything you could not open or verify.
2. The single biggest thing you think we have wrong.
3. One sentence: which finding in Parts A and B changed your own earlier advice the most.
