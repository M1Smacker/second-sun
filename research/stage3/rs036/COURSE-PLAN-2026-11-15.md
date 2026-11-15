# RS-036 result: the Twinlight course plan (47 lessons, 11 units)

Claude, 15 Nov 2026, 2:40 pm Kuwait. Node 4.1. Plan and cap: `PLAN-2026-11-15.md` (4 weekly points). Nothing here is built yet: this is the plan that waits for Ahmed's go.

**Plain verdict:** the course can grow from 6 lessons to 47, in two tracks. The core track (Units 1 to 7, 31 lessons) is what the big exam (Keystone) needs. The universe track (Units 8 to 11, 16 lessons) is the wonder part: the Sun, stars' lives, black holes, galaxies, the Big Bang, life. The exam opens only when the whole core track is done and remembered a week later, never after 6 lessons.

## What the research found (each finding turned into a plan line)

**F1. A standard map of what an intro astronomy course covers. CONFIRMED.** OpenStax Astronomy 2e (Rice University) has 30 chapters, from "Science and the Universe" to "Life in the Universe". Its preface says it "is designed to meet scope and sequence requirements of introductory astronomy courses nationwide" ([preface](https://openstax.org/books/astronomy-2e/pages/preface), read 15 Nov 2026). The Test of Astronomy STandards (TOAST, Slater 2014) was built from three expert position statements (AAAS, National Research Council, American Astronomical Society) plus a review by 28 experts ([PhysPort](https://www.physport.org/assessments/TOAST); paper doi 10.19030/jaese.v1i1.9102, abstract not opened, LIKELY). *Plan line:* the universe track follows the OpenStax order (light, the Sun, stars, distances, death of stars, black holes, galaxies, Big Bang, life), so nothing big is missing.

**F2. OpenStax may not be copied into our book as text. CONFIRMED.** The preface: "licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA) license", and derivatives must be distributed "under the same license". Our book text is CC BY 4.0. *Plan line:* lessons are written in our own words; OpenStax chapters are linked as "read more" with credit; no OpenStax text, figures or problems are pasted.

**F3. Interactive reasoning beats reading. CONFIRMED (one research group, so not fully independent).** Wallace and Prather (arXiv [1806.00452](https://arxiv.org/abs/1806.00452), 2018): Lecture-Tutorials "can help students achieve learning gains well beyond what is typically achieved by lecture alone"; the 2004 study (Prather et al., Astronomy Education Review) reports about 50% after lecture and about 70% after the tutorial (from the search summary, paper not opened: LIKELY). *Plan line:* every lesson gets a short **reasoning sheet**: a sequence of small questions that walks him through the idea with his own answers (typed or tapped), before the problems. This replaces passive reading, which is the "school version" he hated.

**F4. Tests and spacing are the two best study methods. CONFIRMED.** Dunlosky et al. 2013, as reported by the Association for Psychological Science: "practice testing and distributed practice ... receiving the highest overall utility rating"; rereading and highlighting rated low ([APS release](https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html)). RS-035 already found worked examples that fade, and help that thins out as he gets better (expertise reversal, Kalyuga 2003). *Plan line:* keep the RS-035 lesson template; Problems due (spaced review) stays; add a **mixed review** after each unit that pulls questions from all earlier units.

**F5. Astronomy has known wrong ideas that good questions target. CONFIRMED.** Concept inventories exist for exactly this: the Light and Spectroscopy Concept Inventory (26 items: the spectrum, Doppler shift, Wien's law; Bardar, Prather, Brecher, Slater) targets "known student alternative conceptions" ([PhysPort LSCI](https://www.physport.org/assessments/LSCI)); others cover lunar phases and star properties. *Plan line:* each unit check uses wrong answers built from real common mistakes (for example "hotter stars are redder", "seasons come from distance to the Sun"), so a right answer means understanding, not luck. We write our own items; we never copy an inventory (they are protected research tools).

**F6. Our exam spec already says which skills are examined. CONFIRMED (our own file).** Keystone (`research/stage3/KEYSTONE-EXAM-SPEC-2026-11-03.md`) examines domains D1 to D8: light curves, noise and statistics, two-sun orbits, our detector, vetting, honest reporting, running the project, judgement. Pass: at least 85% overall and 70% in each domain. Today only D1 and part of D3 are taught by the 6 live lessons. *Plan line:* the readiness rule below.

**F7. Real data is open for every unit. LIKELY** (sources known, each lesson re-checks its own source before use): TESS and Kepler light curves (MAST), Gaia DR3 (stars' colours, brightness, distances), the NASA Exoplanet Archive (all known planets), public spectra. Lesson plots go through `book/tools/lesson_plots.py`, which refuses any hunt-list or fence star unless it is a published system on the allow list (CONFIRMED by reading the file). *Plan line:* one real-data piece per unit (table below); every download is told and logged.

## The course

Each lesson keeps the RS-035 template: see it, the idea, worked example, half-done example, reasoning sheet (new, F3), try it, closing paragraph, problems. Each unit ends with a unit check and a mixed review (F4, F5). "Live" means already in the book.

### Core track: Second Sun (needed for the exam)

| Unit | Lessons | Real data piece |
|---|---|---|
| **1. A star's light on a graph** | 1.1 a light curve (live); 1.2 percent and ppm (live); 1.3 noise (live); 1.4 what a dip looks like (live) | our design system, TESS sector 21 (live) |
| **2. What makes a dip** | 2.1 orbits and periods (live); 2.2 how long a dip lasts (live); 2.3 why stars differ: size, heat, colour; 2.4 light from two stars: dilution; 2.5 gravity from scratch: why Kepler's law works (Newton) | Gaia colours and sizes of the design stars |
| **3. Light itself** | 3.1 what light is: waves, colours, the spectrum; 3.2 hot things glow: why stars have colours (Wien); 3.3 fingerprints: spectral lines and atoms; 3.4 Doppler: weighing stars and finding planets by their wobble | a real stellar spectrum; a published radial-velocity curve |
| **4. Two suns** | 4.1 eclipsing binaries: two eclipses; 4.2 how two stars orbit each other; 4.3 measuring stars from their eclipses; 4.4 planets around two suns: wandering transits (Kepler-16); 4.5 the stability limit and why they are rare | Kepler-16 light curve (published system) |
| **5. The telescope and the data** | 5.1 telescopes: collecting light and sharpness; 5.2 how TESS watches the sky; 5.3 pixels to light curves: apertures and crowding; 5.4 what goes wrong: systematics, momentum dumps, scattered light, flags | a TESS pixel file of a published star |
| **6. Finding dips with a computer** | 6.1 smoothing slow changes; 6.2 the box search and signal-to-noise (why 7); 6.3 false alarms and looking everywhere; 6.4 the upside-down test; 6.5 hiding fake planets to measure what we miss | injected fakes in public light |
| **7. Proving it** | 7.1 what a clean null means; 7.2 blind runs, freezing, rules written first; 7.3 vetting a dip: the checks, pixels and neighbours; 7.4 lead, candidate, claim, and the two keys | planted cases only, never a real private event |

Core: 31 lessons, 6 live, **25 to build**.

### Universe track: the wonder part (not required for the exam, open any time)

| Unit | Lessons | Real data piece |
|---|---|---|
| **8. Our Sun and the lives of stars** | 8.1 the Sun, an ordinary star up close; 8.2 what powers the Sun: fusion and E = mc squared; 8.3 the star census: the HR diagram; 8.4 how stars and planets are born; 8.5 how stars die: white dwarfs, supernovae, neutron stars | Gaia HR diagram of nearby stars |
| **9. Distances, the galaxy, black holes** | 9.1 parallax: measuring distance with Earth's orbit; 9.2 standard candles: Leavitt's Cepheids; 9.3 the Milky Way; 9.4 black holes and curved spacetime, gravitational waves | Gaia parallaxes; a Cepheid light curve |
| **10. The universe** | 10.1 galaxies; 10.2 the expanding universe: Hubble's law; 10.3 the Big Bang and the oldest light; 10.4 dark matter and dark energy | a public redshift and distance table |
| **11. Other worlds and life** | 11.1 the planets we know: what the 6,000 tell us; 11.2 the habitable zone; 11.3 looking for life: atmospheres and JWST | NASA Exoplanet Archive table |

Universe: 16 lessons, all to build. **Total 47 lessons, 41 to build.** (The planet count in 11.1 is checked against the Archive when the lesson is written.)

## When the big exam opens (readiness rule)

1. All 31 core lessons done, every problem answered (wrong answers count as done once the worked solution was opened and the problem came back right in Problems due).
2. Every core unit check passed at **80% or more**, and passed **again at least 7 days later** with different item versions (spacing, F4). Remembering a week later is the test, not finishing.
3. The three eye tests (official, hard, rehearsal) passed, as the Keystone spec already says.
4. The exam page shows these as a checklist and stays locked until all are green. Universe units never block the exam.

This makes the exam weeks away by design, which is what Ahmed asked: 6 lessons can never open it.

## Source policy

- Our own words for every lesson. Facts traced to a primary source (paper, mission page, catalogue) and listed at the lesson's foot.
- OpenStax Astronomy 2e linked as "read more" with credit, never pasted (CC BY-NC-SA, F2).
- Pictures: our own plots from real data first. NASA and ESA images only after checking that image's own credit and licence (UNCERTAIN per image; not checked in this stint).
- Every lesson fact-checked by Codex before publish (as Codex 017 and 018 did for lessons 1.1 to 2.2, which found real errors).

## Build order and cost

1. Finish Unit 2 (2.3 to 2.5), then Unit 3 (light), then Units 4 to 7: the core track in order.
2. One universe lesson may be slotted in after each core unit, for wonder and a break (Ahmed's choice of which).
3. Per unit: Claude writes, the plot generator draws real data, the learn tests run, Codex fact-checks, the release gates run, publish.
4. Exam checklist and unit checks built with Unit 2's finish (so it counts from the start).

**Cost (UNCERTAIN, from the ledger):** the last lesson blocks cost about 0.5 to 0.8 weekly points per lesson including tests and publish (lessons 1.1 to 1.4 with the app about 4 points; 2.1 and 2.2 with fixes and three publishes about 3). So about **2.5 to 3.5 weekly points per unit, about 20 to 30 for all 41 lessons**, spread over several weeks. Codex fact-checks use Codex's own meter.

## Not checked in this stint (honest list)
- The 2004 Lecture-Tutorial numbers (50% and 70%) and the TOAST paper: read from summaries and PhysPort, papers not opened. LIKELY.
- No university syllabus opened; OpenStax's scope statement stands in for it.
- Image licences of NASA and ESA: per image, later.
- Whether the Keystone page and check engine exist yet: the spec says they come after the track; not built (CONFIRMED by grep, no exam code in `learn.js`).
