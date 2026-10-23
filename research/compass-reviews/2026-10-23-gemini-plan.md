# Compass review: Gemini's "master plan" for Second Sun (2026-10-23)

*Review only, nothing built. Ahmed asked a fresh Gemini chat "where should I start?" and pasted the answer. Labels: VERIFIED (our own register or run), LIKELY (memory or secondary), UNVERIFIED (not opened by Claude). Claim ids are in `book/data/claims.csv`.*

## Verdict: REVISE
About half of the plan is already done, three points are right, four are wrong or risky for us.

## What is right
- Human plus machine, with Ahmed making the final call: our two-key rule. VERIFIED.
- A blind test with hidden fake planets: this is Eyes mode (practice version published the same day). Gemini reached the same design independently.
- Check ExoFOP and the literature before any claim (B9, B10 rules).
- Validate on known planets and use the Exoplanet Archive census: done for TOI-1338 b (F-014), injections (F-015, F-029), census (F-001). Lightkurve is already used to load data (imported in `detect_v2.py` and five labs).

## What is wrong or risky
1. "Inspect the folded light curves" is wrong for circumbinary planets: transit times shift by days, longer than a crossing lasts, so a single-period fold smears them (F-007; Chapter 5; the Chapter 5 demo shows gaps about 11 crossing-lengths apart). Inspect unfolded, per-sector curves. VERIFIED.
2. "If the code cannot flag the known Kepler planets in TESS data, it will not find new ones" is wrong: a known planet may not transit in the TESS years (precession, F-009 LIKELY: Kepler-453 b about 8% of the time) and many hosts are faint. The count is also off: 14 transiting planets in total, 12 Kepler and 2 TESS (F-001). The valid version is to re-find them in the original Kepler data (NOT TESTED).
3. "Build on Lightkurve's flatten and noise tools" would bring back a mistake we caught: its quick estimate gave 229 ppm for Kepler-16, our 2-day flatten gives 908 ppm (F-039). It does not remove spacecraft jitter; we flag dips near momentum dumps for a human instead.
4. Phase 3 (post to forums, share the pipeline, contact people) conflicts with Ahmed's decisions: hidden until something is worth announcing; contact researchers only for a real candidate (Claude drafts, Ahmed sends); candidate data local until both keys pass. Reading forums to learn is fine; the repo is already public.
- Minor: "V-shaped = binary, U-shaped = planet" is a rule of thumb with exceptions (grazing planets look V-shaped; limb darkening rounds the bottom). Our checks are duration changes with binary phase (F-023) and the pixel test.

## What it misses
- Odds and sensitivity: floor about 6 Earth radii at bright stars (F-015); our estimate of a real candidate from G1 is about 20% (range 5 to 40%). It praises the project without checking novelty or rivals.
- False alarms: "AI filters 99% of noise" is unsupported. Our detector is a matched filter, and on upside-down data at SNR 7 it still reports 6 events in 10 sectors (F-016, about 0.6 per sector).
- Tools we already mapped (wave 4): triceratops, LATTE (LGPL, link only, never copy code into this MIT repo), the pixel check; and the Planet Hunters / Visual Survey Group credit practice (wave 5).

## Unverified (Claude did not open these)
Chandra Interactive Learning as a fit, "NASA's Universe Unplugged" (existence), Planetary Society light-curve guides, Exoplanet Watch "needs data reducers" and "NASA mentors" (LIKELY a small-telescope timing programme for known planets, poor fit), "advanced threads" on Planet Hunters TESS Talk.

## Does it help us?
Modestly: it confirms Eyes mode, adds one new test (re-find known Kepler circumbinary planets in the Kepler data), and reminds us to check ExoFOP and the literature before any claim. The rest duplicates our work or conflicts with Ahmed's rules.

## Best next steps (need Ahmed's go: the hunt and science follow-ups are on hold)
1. Make Eyes mode's fake planets behave like two-sun ones (shifting timing and length, STANLEY-timed injections as in F-029) and draw them from more than one star, so the noise cannot be memorised.
2. Run the detector on Kepler-16, Kepler-34 and Kepler-35 in the original Kepler data and see whether it re-finds them.

## Follow-up
A one-time fact-check and research brief for Gemini is saved as `research/gemini-followup-prompt-2026-10-23.md`. Gemini's answer will be reviewed through Compass again before anything is built from it.
