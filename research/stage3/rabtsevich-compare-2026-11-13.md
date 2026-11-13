# Rabtsevich against Second Sun: are we over-engineering? (RS-023, 13 Nov 2026, Ahmed's question, Sonnet 5.5)

Method: `research/RESEARCH-BLUEPRINT.md`. Cap 1.5 weekly points, written before the start (about 12 tool calls). Builds on `rabtsevich-deep-2026-11-03.md` (RS-007), which already read his Note, preregistration and later papers. New pages opened today in the browser pane (HTML only).

## Questions and the decision each feeds
1. Is his candidate circumbinary, and is his problem the same as ours? Decides whether the comparison is fair.
2. Did other people (professional or amateur) use the same tools we built (injection tests, upside-down copies, preregistration)? Decides whether our depth is excess.
3. Is a lone circumbinary search normally easy? Decides how to read our nulls and our pace.
4. Is there anything he does that we should copy? Decides plan changes.

## Answers
**Q1. CONFIRMED (own files):** TIC 4206066 is a late-K dwarf, a 3.18 d signal of 500 ppm, 1.4 Earth radii if on the target (`data/rabtsevich_zenodo/manuscript_note.txt`, abstract). The word "circumbinary" appears 0 times in his Note, both later papers and the Sector 110 preregistration. Its main alternative is a planet transiting an unresolved bound companion. So it is a single-star small-planet candidate, NOT a circumbinary one. It was found by box least squares on Sector 98 QLP light curves of 126,246 stars plus LEO-Vetter, post hoc below his own shortlist threshold (multiple-event statistics 10.6 and 11.0 against 15); the post hoc significance test is about 3 sigma for the weaker signal. TRICERATOPS FPP 0.03 to 0.04 sits above the 0.015 validation line, so he claims no validation. A periodic planet is the problem box least squares was built for: 23 transits in three sectors at 3.18 d. A circumbinary planet transits once or twice a sector, at irregular times, in front of a binary whose eclipses are far deeper.

**Q1b. LIKELY (Gizmodo, a secondary source, opened today):** he is 28, a product manager living in Spain, no astronomy training, about two weeks, 126,000 stars, then dozens of tests on one star; he says he decided which tests to run. https://gizmodo.com/did-claude-help-an-amateur-astronomer-discover-a-new-planet-2000824393 . The count of 74 tests is from other press (UNCERTAIN in detail). An earlier pass (RS-007) noted a TESS-team member saying professional filters had already flagged the signal (LIKELY, secondary).

**Q1c. CONFIRMED (our DDT notes):** TESS Sector 110 runs 31 Oct to 26 Nov 2026 (there is no 31 Nov). DDT program 100 predicts nine transits of the 3.18 d signal and three of the 11.13 d one; no result exists before 26 Nov (T60). A search today found no Sector 110 result and no published critique.

**Q2. CONFIRMED (abstracts opened today):**
- Kepler's catalogue paper measured completeness by running its Robovetter on simulated data and gave reliability above 98% for periods under 100 days; its low-S/N long-period slice was only 50.5% reliable. https://arxiv.org/abs/1710.06758 . The Kepler documentation describes inverted light curves for the false-alarm count (LIKELY: search summary of the Robovetter document, not opened).
- Davies et al. 2026 (professionals) searched TESS eclipsing binaries for circumbinary planets with mono-cbp, "yielding one candidate transit event", tested it on the known circumbinary planets (14, recovery at least 50% each) and injected simulated transits with varying depth and duration. https://arxiv.org/abs/2604.09435
- Martin and Fabrycky's circumbinary search algorithm STANLEY is titled "...and No New Planets in Existing Systems" (ADS title, https://ui.adsabs.harvard.edu/abs/2021AJ....162...84M/abstract).
- Rabtsevich himself, for a later Kepler candidate (KOI-5005.01), found dips as strong as the real one in 16 of 34 upside-down copies and wrote "not established" (RS-007, his later paper, CONFIRMED). He reached our control the hard way.
- Beyond Kepler, Davies and Rabtsevich I found no other TESS group reporting upside-down copies (UNCERTAIN: one search, not exhaustive).

**Q3. CONFIRMED (abstract):** only two transiting circumbinary planets have come out of TESS so far, TOI-1338 b and TIC 172900988 b; the second was "detected in one sector of TESS data" by the professional team. https://arxiv.org/abs/2105.08614 (the NASA Exoplanet Archive composite table holds 14 transiting circumbinary planets in all, Codex 003 query of 13 Nov, the same 14 as in Davies). A team search of 512 binaries gave one candidate event. Clean nulls are the normal outcome.

**Q4. What to copy (plan changes):** nothing new in the checking: T125 to T130 already cover his follow-up habits. One idea he has and we lack: a deliberate, labelled exploratory lane for events just below the bar, kept apart from the sealed confirmatory run and confirmed only on new data (his Sector 110 test; our Vigil, T120). Filed as T162, not decided.

## What changes
- T162 exploratory lane (idea) on Tree node 3.3, WAITS for Ahmed.
- Tree note: our first checks on real circumbinary planets (T109) stay BEFORE G1, because G1 is one shot.
- Correction recorded: his candidate is not circumbinary (memory and the book must say so).

## Open
Sector 110 result (after 26 Nov); the TESS-team quote not re-opened; whether any other TESS group publishes upside-down controls; the exact count of his tests.
