# 5. Why two-sun transits wander

<p class="ss-meta">Chapter 5 · about 25 min · Maths: averages, rough speeds, percentages</p>

!!! plain "In plain words"
    Around one star, a planet's dips arrive like a clock: same gap, same length, every time. Around two stars, they **don't**. The stars are moving, so the planet meets them at different places each time. Its dips come early or late, last longer or shorter, and can even stop for years and come back. This makes two-sun planets hard to find with normal tools, and it's exactly why our hunt has a chance.

**What this chapter answers:** why are circumbinary transits irregular, and how does that create our G1 opportunity?

## 5.1 The intuition

Imagine a lighthouse on a boat, and the boat is circling in the harbour. You walk around the harbour on a path. Each time you pass in front of the lighthouse beam, the boat is somewhere different on its circle. Sometimes you meet it early, sometimes late. If the boat is moving the same way you are, you stay in its beam longer; if it moves the opposite way, you flash past.

The boat is the star being crossed. You're the planet.

## 5.2 The scientific meaning

Three effects make circumbinary transits irregular:

1. **Timing shifts.** Each star swings around the pair's centre. The planet crosses the star wherever the star happens to be, so the gaps between transits vary. These shifts can be **days**, longer than a transit lasts, so the usual trick of folding the data at one period fails. Every Kepler circumbinary discovery was made **by eye** {{claim:F-007}}.
2. **Duration changes.** If the star moves the same direction as the planet, the crossing is slow and long; the opposite direction makes it short. TOI-1338 b's first three TESS transits came about 93 and 95 days apart and lasted about **0.3, 0.4 and 0.6 days** {{claim:F-008}}.
3. **Switching on and off.** The planet's orbit slowly tilts around (it **precesses**). For part of each cycle it's lined up to cross the stars; for the rest it misses them completely. Kepler-453 b crosses only about 8% of the time: for every one like it we see, about 12 are hidden right now {{claim:F-009}}.

## 5.3 The technical explanation

### Precession and transit windows

The two stars aren't a perfect point mass, so they pull the planet's orbit plane round in a slow circle. Call the time for one full turn the **precession period**. For TOI-1338 b it's **21.4 years** {{claim:F-010}}. Transits are only possible while the planet's orbit plane cuts across the stars, so they come in **windows** separated by long silences.

Kostov et al. (2020) worked out that TOI-1338 b's transits would become unlikely, with at most about a 30% chance per crossing, after **12 September 2025** {{claim:F-010}}. Yet a 2024 model by Wang and Liu predicted one specific crossing on **16 December 2025**, and our search found a dip that same night {{claim:F-011}}. The "30%" was a chance, not a ban: this was one of the crossings that happened.

### Why normal searches miss them

NASA's SPOC pipeline flags a planet only after it sees **at least two transits** and a detection score above **7.1** {{claim:F-017}}. Its multi-transit method assumes a fixed period. A two-sun planet with shifting timing, changing durations, and one transit per sector can slip through.

## 5.4 Our implementation: the G1 idea

From 2009 to 2013 the Kepler telescope stared at one patch of sky and catalogued about 2,900 eclipsing binaries. Kepler's planets were found in that window. But precession means some planets that were **not crossing back then could be crossing now**. A 2017 study estimated Kepler's binaries hold about **17 to 30 more** such planets that will start transiting someday, possibly during TESS {{claim:F-018}}.

TESS has re-observed the Kepler field. G1 is the search of those binaries in the newer TESS data. In code this means:

- take the Kepler binary's period and eclipse times from the catalogue;
- mask its eclipses (Chapter 8);
- search what's left for single dips, and later for groups of dips that fit a circumbinary orbit.

## 5.5 Worked example: TOI-1338 b's timeline

| When | What happened | Source |
|---|---|---|
| 2018-2019 (sectors 3, 6, 10) | first three transits, 93 and 95 days apart, 0.3-0.6 d long | {{claim:F-008}} |
| 2020 | planet announced; precession period 21.4 yr; transits predicted to become rare after Sep 2025 | {{claim:F-010}} |
| 2024 | Wang and Liu predict a crossing on 16 Dec 2025, 02:13 UTC, 6.31 h | {{claim:F-011}} |
| 16 Dec 2025 | our search finds a 0.24% dip that night, about 1 hour after the predicted time | {{claim:F-011}} |

That one-hour difference is bigger than the paper's stated error (±23 min). It could be real wobble, or our timing error could be bigger than it looks. We haven't measured our error carefully yet (UNCERTAIN, on the task list). A known planet's crossing that nobody has published yet is a nice result for practice, but it is **not a discovery**.

## 5.6 What this lets us conclude, and what it doesn't

- **It explains why there's room for us:** standard tools are built for clockwork planets.
- **It doesn't promise planets.** The 17-30 estimate is a model, and many of those planets could be small or faint.
- **Irregular timing cuts both ways.** It hides planets from NASA's pipeline, but it also means one dip alone is weak evidence. A strong case needs dips that fit a physical orbit around the two stars.

## 5.7 Check your understanding

??? quiz "1. Why can't we fold a two-sun planet's light curve at one period?"
    Its transit times shift by up to days, so the dips don't line up at any single period.

??? quiz "2. TOI-1338 b's transits lasted 0.3, 0.4 and 0.6 days. What causes the difference?"
    The crossed star's own motion. Moving with the planet makes a long transit; moving against it makes a short one.

??? quiz "3. In one sentence, what is G1?"
    Searching Kepler's eclipsing binaries in newer TESS data for planets that weren't crossing during Kepler but have **switched on** since, because their orbits precessed.

**Next:** [Chapter 8](08-our-detector.md): how our search actually finds dips, and how good it is.

## Sources
In the [claims register](../claims.md): F-007 to F-011, F-017, F-018.
