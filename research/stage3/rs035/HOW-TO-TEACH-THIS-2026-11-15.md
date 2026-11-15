# RS-035: how to teach this project's science (Claude, 15 Nov 2026, overnight; Ahmed asked for a real stint, not rushed)

**Cap (written before starting):** about 2.5 weekly points, about 30 tool calls. Node 4.1. Feeds: the lesson template, the unit order, the problem design and the reader tools of the Book 3.0 learning app.

**Reader:** Ahmed. Basic algebra (powers, logs, trig rusty), school physics. Phone and PC equally. Wants a textbook he reads and learns from (conversational, clear), full maths built up, our real stars as worked examples, typed end-of-lesson problems, margin notes and worked examples to clear doubts without asking Claude. Data first.

## Questions, each tied to a decision
1. **Lesson template.** What does the evidence say about worked examples, retrieval practice, spacing, and cognitive load for a self-learner? Decides the order of parts inside one lesson.
2. **Problems.** What kind of practice and feedback works best when the reader checks himself (typed answers, instant check, worked solution)? Decides the problem format.
3. **Unit order, data first.** How do good introductory astronomy courses order light, stars, orbits, binaries, transits and data? Is starting from the data (a light curve on screen) supported? Decides the unit list.
4. **Interactive plots.** When do interactive simulations help learning and when do they distract? Decides where plots and sliders go.
5. **Margin notes and maths.** How should definitions and side explanations be placed so they help rather than split attention? How to build maths just in time from basic algebra? Decides margin notes and the maths layer.
6. **Content facts.** Primary sources for the physics the first units teach (transit depth, light curves, eclipsing binaries, circumbinary planets, TESS). Decides what the first lessons may state as fact.

## Findings (records read 15 Nov 2026, 4:05 to 4:20 am; raw abstracts in `data/rs035_sources_2026-11-15/abstracts.json`)
How read: journal sites (SAGE, PubMed) showed bot checks, which I do not bypass, so each paper's official record and abstract came from Crossref, Europe PMC, OpenAlex or Semantic Scholar, the Fyfe abstract from the Springer page, the astronomy abstracts from arXiv. Abstracts only: full texts were not read, so every label below rests on the authors' own summary.

**Q1 Lesson template.**
- Dunlosky et al. 2013 (Psychological Science in the Public Interest, doi 10.1177/1529100612453266): "Practice testing and distributed practice received high utility assessments"; rereading and highlighting do not consistently help, so use "practice testing instead of rereading". CONFIRMED (authors' conclusion).
- Sweller and Cooper 1985 (Cognition and Instruction, doi 10.1207/s1532690xci0201_3): worked examples "require considerably less time to process than conventional problems", and later similar problems were solved faster with fewer errors. CONFIRMED for novices.
- Renkl 2013 (Cognitive Science, doi 10.1111/cogs.12086): "Learning from examples is a very effective means of initial cognitive skill acquisition." CONFIRMED.
- Atkinson, Renkl and Merrill 2003 (Journal of Educational Psychology, doi 10.1037/0022-0663.95.4.774): fading worked-out steps plus prompts to name the principle behind each step gave "medium to large effects on near and far transfer without requiring additional time on task". CONFIRMED.
- Kalyuga et al. 2003 (Educational Psychologist, doi 10.1207/S15326985EP3801_4), expertise reversal: methods that help beginners "can lose their effectiveness" for more experienced learners. CONFIRMED: help must thin out as units go on.

**Plan change:** each lesson = real thing on screen, the idea built step by step, a fully worked example on our own star, a second example with the last steps left open and a prompt to name the principle, then problems. Later units give fewer steps.

**Q2 Problems and feedback.**
- Rowland 2014 (Psychological Bulletin, doi 10.1037/a0037559): "initial recall tests yielding larger testing benefits than recognition tests". CONFIRMED.
- Adesope et al. 2017 (Review of Educational Research, doi 10.3102/0034654316689306): practice tests beat restudying and all other comparison conditions. CONFIRMED.
- Shute 2008 (Review of Educational Research, doi 10.3102/0034654307313795): formative feedback "should be nonevaluative, supportive, timely, and specific"; types include explanation of the correct answer, hints, worked examples. Hattie and Timperley 2007 (doi 10.3102/003465430298487): feedback can help or harm depending on its type. CONFIRMED.
- Cepeda et al. 2006 (Psychological Bulletin, doi 10.1037/0033-2909.132.3.354): spacing helps; the best gap grows with how long you need to remember. CONFIRMED.

**Plan change:** problems are typed (numbers or short words: recall, not multiple choice where avoidable), checked at once, with a specific explanation and the full worked solution. A wrong or skipped problem goes to "Problems due" on the home screen (spaced practice without forced re-asking). Highlights and notes stay because Ahmed asked for them, but home leads with Continue and Problems due, since the evidence ranks practice above highlighting.

**Q3 Unit order, data first.**
- Fyfe, McNeil, Son and Goldstone 2014 (Educational Psychology Review, doi 10.1007/s10648-014-9249-3): "we recommend beginning with concrete materials and then explicitly and gradually fading to the more abstract." CONFIRMED as a review recommendation.
- OpenStax Astronomy 2e (read 15 Nov 2026) orders theory first: orbits and gravity (ch. 3), radiation and spectra (5), instruments (6), exoplanets only in ch. 21. Our data-first order is a deliberate departure, backed by concreteness fading and by the goal (understand and check this project); general basics are taught when needed.

**Plan change:** units start from a light curve on screen and pull physics in as each idea needs it.

**Q4 Interactive plots.**
- Wieman, Adams and Perkins 2008 (Science, doi 10.1126/science.1161948): students learn better when they construct their own understanding, and "Interactive computer simulations can meet both of these needs". CONFIRMED as the PhET project's summary of its research.

**Plan change:** a plot appears where touching it answers a question the lesson just asked (question written beside it), never as decoration.

**Q5 Margin notes and maths.** Ginns 2006 (Learning and Instruction, contiguity meta-analysis): no abstract reachable in any open record, so "explanations placed beside what they explain help" is NOT READ tonight and stays LIKELY (the contiguity principle, widely cited). Maths is built just in time from basic algebra (powers, roots, ratios, logs) inside the lesson that first needs it, each time with a worked numeric example (Sweller 1985, Renkl 2013).

**Q6 Content facts (first units).**
- Winn 2010, "Transits and Occultations" (arXiv 1001.2010): eclipses give "the relative dimensions of the planet and its host star". CONFIRMED; the depth relation of the dip lesson comes from this review.
- Doyle et al. 2011, Kepler-16 (arXiv 1109.3432): transits across both stars; planet comparable to Saturn in mass and size on a nearly circular 229-day orbit; stars 20% and 69% as massive as the Sun on an eccentric 41-day orbit. CONFIRMED.
- Welsh et al. 2012, Kepler-34 and -35 (arXiv 1204.3955): "Most Sun-like stars in the Galaxy reside in gravitationally-bound pairs". CONFIRMED as the authors' statement.
- Ricker et al. 2014, TESS (arXiv 1406.0151): target stars every 2 min, full-frame images every 30 min in the original mission (later 10 min, then 200 s; already in claims F-041). CONFIRMED.

## The lesson template
1. **See it:** a real plot from our design stars first.
2. **The idea:** built step by step in plain conversational text; new words get a margin note beside the sentence; maths just in time.
3. **Worked example:** every step shown, real numbers from our stars.
4. **Your turn, half done:** a second example with the last steps open and a prompt to name the principle.
5. **Try it** (only where it answers a question): an interactive plot with the question beside it.
6. **Closing paragraph:** the lesson in a few sentences, quiet, no bold banner.
7. **Problems:** three to five typed answers, instant check, specific explanation, full worked solution; wrong or skipped ones go to Problems due.

Later units fade the help: fewer worked steps, more problems.

## Unit outline (data first; the hunt resumes after Units 1 to 6, Ahmed's milestone)
1. **A star's light on a graph:** light curves; brightness, flux, percent and parts per million; noise and spread; what a dip looks like.
2. **What makes a dip:** shadow size and depth; orbits and periods (Kepler's third law); how long a dip lasts; why stars differ.
3. **Two suns:** eclipsing binaries and their two eclipses; how two stars orbit; planets around two suns and their wandering transits (Kepler-16); why they are rare and hard to find.
4. **The telescope and the data:** how TESS watches the sky; pixels to light curves; what goes wrong (systematics, momentum dumps, scattered light).
5. **Finding dips with a computer:** smoothing slow changes; box search and signal-to-noise; false alarms and the upside-down test; hiding fake planets to measure what we miss.
6. **Proving it:** what a clean null means; blind runs and rules written first; from a dip to a claim (checks, two keys).
7. **Beyond the project (later):** gravity, light and stars in general.
