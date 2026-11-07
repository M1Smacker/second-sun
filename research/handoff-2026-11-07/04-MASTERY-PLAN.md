# Second Sun mastery plan: Checker, Engineer, Inventor

*Written 7 Nov 2026 by Claude (claude.ai, Opus 5.5) for Ahmed. Every link below was opened and checked on 7 Nov 2026 unless the row says otherwise. Hours are rough estimates for a focused hour, not clock time with a phone nearby.*

## How to read this plan

There are three tiers. Each one has a clear finish line, a list of exact topics, the depth you need for each, and where to learn it.

**Checker** means you can independently vet a candidate dip and say yes or no with reasons. This is what the book's learning track already trains (the book calls this role the second key; you call it the first key; same job, pick one name and tell Claude Code).

**Engineer** means you can open any core file in the pipeline, explain what it does line by line, change it safely, and prove the change with a test. This is your definition of the key you want to hold.

**Inventor** means you can design a new method, test it fairly, and defend it against a sceptical expert. This is where original work comes from.

Every topic carries one of three depth labels:

| Label | Meaning | How you know you have it |
|---|---|---|
| **Master** | you can do it without notes and explain it to someone else | you can write it on a blank page, and you can spot a wrong version |
| **Confident** | you can use it correctly with a reference open | you can follow a paper's equation or a library's docs and apply it |
| **Aware** | you know it exists, what it is for, and where to look | you can say "this needs X" and find X |

## The timeline (named phases)

Your HSSC-II boards (March to May 2027) come first. Your school maths, physics and computer science are not a distraction from this plan; they are its foundation. FBISE 12th-grade maths covers functions, limits, differentiation and integration, which is most of the Engineer maths (my reading of the syllabus, LIKELY).

| Phase | When | Second Sun study | What gets done |
|---|---|---|---|
| **Exam Week** | now until your physics improvement exam | none | the exam |
| **Checker Season** | after the exam until about end of January 2027 | about 3 hours a week, two sittings | Checker tier finished |
| **Board Sprint** | February to the end of boards | 0 to 1 hour a week (Second Sun keeps running with Claude Code; you approve decisions only) | boards |
| **Engineer Summer** | June to mid-November 2027 | 1.5 to 2 hours a day, 5 days a week | Engineer tier finished |
| **Inventor Year** | late November 2027 onwards, 12 to 18 months, alongside your ML roadmap | 1 to 2 hours a day | Inventor tier, first original method tested |

A word on pacing, because plans like this usually die in week two, not month six. Each phase is built from small units of one to two hours with a visible checkpoint at the end. If a week is missed, you do not restart the plan; you do the next unit. Two missed weeks in a row means the plan is too big, and it gets cut, not abandoned.

## Tier 1: Checker (Checker Season, about 30 to 40 hours)

**Finish line:** pass every check in the book's learning track Levels 0 to 6, do all ten labs (they are marked optional; for you they are not), then pass a blind test: Claude Code prepares 10 events (real dips, planted fakes, eclipse leftovers, gap fakes, mixed and unlabelled), and you write a verdict and one paragraph of reasons for each. Pass mark: 8 of 10 right, with reasons that name the evidence.

| Topic | Depth | Where to learn it (exact) | Hours |
|---|---|---|---|
| The whole Second Sun method | Master | The book's learning track, Levels 0 to 6, in order: [m1smacker.github.io/second-sun/learn/](https://m1smacker.github.io/second-sun/learn/) | 15 |
| Running the labs (terminal, Python, files) | Confident | Labs 0 to 9 from the book; for the Python inside them, [CS50P](https://cs50.harvard.edu/python/) Weeks 0 to 2 (Functions and variables, Conditionals, Loops) | 8 |
| Light curves and TESS data files | Confident | [Lightkurve tutorials](https://lightkurve.github.io/lightkurve/tutorials/index.html), section 1.1 (all three) and 1.2 ("Searching & downloading Kepler, K2, and TESS data", "Using Light Curve Files with Lightkurve", "Using Target Pixel Files with Lightkurve") | 4 |
| TESS cadences, FFIs, light-curve files | Confident | [TESS Data Products Information](https://heasarc.gsfc.nasa.gov/docs/tess/data-products.html) (NASA TESS Science Support Center) | 1 |
| Instrumental fakes (gaps, quality flags, scattered light) | Master | Lightkurve tutorials section 2.2, the four "Instrumental Noise in Kepler and K2" notebooks, then book Chapter 10 again | 3 |
| How the transit method works | Confident | [OpenStax Astronomy 2e, section 21.4](https://openstax.org/books/astronomy-2e/pages/21-4-planets-beyond-the-solar-system-search-and-discovery), "Transiting Planets" | 1 |
| Binary stars and their masses | Confident | [OpenStax Astronomy 2e, section 18.2](https://openstax.org/books/astronomy-2e/pages/18-2-measuring-stellar-masses) (does not cover eclipsing binaries; the book's Chapter 4 does) | 1 |
| Gravity and Kepler's laws | Confident | [OpenStax University Physics Vol. 1, Chapter 13](https://openstax.org/books/university-physics-volume-1/pages/13-introduction), sections 13.1, 13.4, 13.5, 13.6 | 3 |
| The two real discoveries you are trying to repeat | Confident (read, not derive) | [Kepler-16, Doyle et al. 2011](https://arxiv.org/abs/1109.3432) abstract and figures; [TOI-1338, Kostov et al. 2020](https://arxiv.org/abs/2004.07783) abstract, introduction and the light-curve figures | 3 |

## Tier 2: Engineer (Engineer Summer, about 220 to 240 hours; at 2 hours a day, 5 days a week, that is June to about mid-November)

**Finish line, two tests:** (1) Claude Code plants three bugs in a sandbox copy of the core pipeline (a mutation test, the same method the project already uses on its own tests), and you find and explain at least two in one sitting. (2) You make one real improvement from the build queue yourself, end to end: plan, change, test, compare against the frozen run event by event, write it up. Claude reviews it as a stranger would.

### Python and tools

My recommendation for the main Python course is **CS50P, Harvard's "Introduction to Programming with Python"**, free at [cs50.harvard.edu/python](https://cs50.harvard.edu/python/). Ten weeks: functions and variables, conditionals, loops, exceptions, libraries, unit tests, file I/O, regular expressions, object-oriented programming, and a final project. Why this one over the others: it has real problem sets that are checked automatically, it teaches unit tests and exceptions (Second Sun lives on tests), and it assumes nothing. Do every problem set; watching without the problem sets does not count. If a week feels too steep, read the matching chapter of [Python for Everybody](https://www.py4e.com/lessons), which is gentler and covers the same ground, then go back. Make your CS50P final project something Second Sun related (for example, a small tool that reads a TESS light curve and reports the deepest dip).

| Topic | Depth | Where to learn it (exact) | Hours |
|---|---|---|---|
| Core Python (variables, loops, functions, files, exceptions, tests, classes) | Master | [CS50P](https://cs50.harvard.edu/python/), Weeks 0 to 9 plus final project | 60 |
| NumPy arrays (the language every pipeline file speaks) | Master | [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html), then [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/), Chapter 2 "Introduction to NumPy" | 12 |
| pandas tables (target lists, results, CSVs) | Confident | Python Data Science Handbook, Chapter 3 "Data Manipulation with Pandas" | 8 |
| Plotting | Confident | [Matplotlib quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html), then Python Data Science Handbook, Chapter 4 | 5 |
| Git and GitHub (reading history, branches, diffs) | Confident | [Software Carpentry, Version Control with Git](https://swcarpentry.github.io/git-novice/), episodes 1 to 9 | 6 |
| Writing careful scientific code (defensive programming, debugging) | Confident | [Software Carpentry, Programming with Python](https://swcarpentry.github.io/python-novice-inflammation/), episodes 10 "Defensive Programming" and 11 "Debugging" | 3 |
| The official reference, for looking things up | Aware | [The Python Tutorial](https://docs.python.org/3/tutorial/) (python.org); not for beginners, but the place to check how something really works | as needed |

### Astronomy Python

| Topic | Depth | Where to learn it (exact) | Hours |
|---|---|---|---|
| Lightkurve, end to end | Confident | [Lightkurve tutorials](https://lightkurve.github.io/lightkurve/tutorials/index.html), sections 2.1 to 2.3 (creating light curves, noise, CBV, regression and PLD correctors) and 3.1 (all five exoplanet examples) | 12 |
| Fitting a line and a model by code | Master | [Python for Astronomers](https://prappleizer.github.io/), tutorial "Linear regression: fitting a line to data" | 3 |
| Astropy (units, FITS, time) | Confident | [Learn Astropy](https://learn.astropy.org/) (the site loads its list dynamically; search it for "FITS", "units" and "time series") | 6 |

### Maths

Most of this is your 12th-grade maths, used for real. Revise it with Second Sun examples in mind once boards are done.

| Topic | Depth | Where to learn it (exact) | Hours |
|---|---|---|---|
| Algebra: powers, roots, rearranging formulas | Master | [Khan Academy, Algebra 2](https://www.khanacademy.org/math/algebra2) | 10 |
| Logarithms and exponentials (magnitudes, noise falling as 1 over the square root of N) | Master | [Khan Academy, Precalculus](https://www.khanacademy.org/math/precalculus), the exponential and logarithm units (I could confirm the page loads, not its unit list) | 6 |
| What a derivative and an integral mean | Confident | [3Blue1Brown, Essence of calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr) (12 videos), first 8 | 4 |

### Statistics (the part that decides whether a dip is real)

| Topic | Depth | Where to learn it (exact) | Hours |
|---|---|---|---|
| Probability and distributions, visually | Confident | [Seeing Theory](https://seeing-theory.brown.edu/), chapters 1 to 4 (basic and compound probability, distributions, frequentist inference) | 5 |
| Gaussian, Poisson and binomial distributions; mean, standard deviation, averaging noise | Master | [MIT 18.05 Introduction to Probability and Statistics](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/), the readings and problem sets on random variables and distributions (with solutions) | 15 |
| Confidence intervals, hypothesis tests, p-values, false alarms, the look-elsewhere effect | Master | MIT 18.05 readings on hypothesis testing and confidence intervals, then book Chapter 7 again; you should be able to recompute the project's false-alarm intervals by hand | 12 |
| Practice drills | Confident | [Khan Academy, Statistics and probability](https://www.khanacademy.org/math/statistics-probability) | as needed |
| Fitting a model to data, done honestly | Confident | [Hogg, Bovy and Lang 2010, "Data analysis recipes: Fitting a model to data"](https://arxiv.org/abs/1008.4686), sections 1 to 4 | 6 |
| Why red noise makes small dips hard | Confident | [Pont, Zucker and Queloz 2006, "The effect of red noise on planetary transit detection"](https://arxiv.org/abs/astro-ph/0608597) | 2 |

### Transit and two-sun physics

| Topic | Depth | Where to learn it (exact) | Hours |
|---|---|---|---|
| Transit shapes, depth, duration, limb darkening | Confident (Master for depth and duration formulas) | [Winn 2010, "Transits and Occultations"](https://arxiv.org/abs/1001.2010), sections 1 and 2 | 8 |
| How box searches work | Confident | [Kovács, Zucker and Mazeh 2002, "A box-fitting algorithm in the search for periodic transits" (BLS)](https://arxiv.org/abs/astro-ph/0206099) | 3 |
| Why two-sun planets transit often but irregularly | Confident | [Martin and Triaud 2015, "Circumbinary planets: why they are so likely to transit"](https://arxiv.org/abs/1501.03631) | 4 |
| The stability limit (stability.py) | Confident | [Holman and Wiegert 1999, "Long-Term Stability of Planets in Binary Systems"](https://arxiv.org/abs/astro-ph/9809315), introduction and results | 2 |
| The big picture of planets around binaries | Confident | [Martin 2018, "Populations of planets in multiple star systems"](https://arxiv.org/abs/1802.08693), introduction and the circumbinary sections | 4 |
| How professionals vet and validate | Confident | [Sagan Summer Workshop 2018, "Did I Really Just Find an Exoplanet?"](https://nexsci.caltech.edu/workshop/2018/) (the page links the workshop's YouTube channel with talks since 2014; I did not open individual videos) | 6 |

### The Engine Room (the new book Part, the core of Tier 2)

About 25 to 30 hours. Described in full in the last section of this plan.

## Tier 3: Inventor (Inventor Year, about 200 hours of study below, plus 200 to 400 hours building and testing your own method)

**Finish line:** a two-page method proposal of your own (what it does, why nobody has done exactly this, how it will be tested fairly), which survives a hostile review by a separate AI session and by one outside reader; then the method is built, frozen and run as a preregistered test on data it has never seen. A null result passes this tier as long as the test was fair.

| Topic | Depth | Where to learn it (exact) | Hours |
|---|---|---|---|
| Linear algebra (least squares in matrix form, the core of every detrending fit) | Confident | [3Blue1Brown, Essence of linear algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) (16 videos), then Hogg et al. 2010 again, the matrix sections | 15 |
| Bayesian inference | Master | [Seeing Theory](https://seeing-theory.brown.edu/), chapter 5; MIT 18.05 Bayesian readings | 15 |
| MCMC (how fitted numbers get honest error bars) | Master | [Hogg and Foreman-Mackey 2017, "Data analysis recipes: Using Markov Chain Monte Carlo"](https://arxiv.org/abs/1710.06068); then write your own sampler with [Python for Astronomers](https://prappleizer.github.io/), tutorials "Markov Chain Monte Carlo" and "Writing a Metropolis-Hastings sampler"; then [emcee tutorials](https://emcee.readthedocs.io/en/stable/) "Quickstart" and "Fitting a model to data" | 30 |
| Gaussian processes (modelling red noise instead of fighting it) | Confident | [Foreman-Mackey et al. 2017, celerite](https://arxiv.org/abs/1703.09710); background in [Rasmussen and Williams, Gaussian Processes for Machine Learning](https://gaussianprocess.org/gpml/), chapter 2 (the site offers the book for download) | 25 |
| Orbits by computer | Master | [Python for Astronomers](https://prappleizer.github.io/), "Building an RK4 orbit integrator"; then make it integrate a planet around two stars and watch its transit times drift | 20 |
| Physics of orbits and tides | Confident | [OpenStax University Physics Vol. 1, Chapter 13](https://openstax.org/books/university-physics-volume-1/pages/13-introduction) properly, plus a first-year mechanics course of your choice when you get there | 40 |
| Modern transit search | Confident | [Hippke and Heller 2019, Transit Least Squares](https://arxiv.org/abs/1901.02015) | 4 |
| What the state of the art already does | Master | [Martin et al. 2021, STANLEY](https://arxiv.org/abs/2101.03186); [Davies et al. 2026, mono-cbp](https://arxiv.org/abs/2604.09435); [Thornton et al. 2026, apsidal precession](https://arxiv.org/abs/2512.07934). You should know these three better than anyone you will talk to, because "new" means "not in these" | 30 |
| Eclipsing-binary catalogues (where targets come from) | Confident | [Prsa et al. 2021, TESS EBs in Sectors 1 to 26](https://arxiv.org/abs/2110.13382); [TESS Ten Thousand Catalog](https://arxiv.org/abs/2506.05631); [CALNet, arXiv:2504.15875](https://arxiv.org/abs/2504.15875) | 8 |
| Machine learning for vetting (bridges to your ML roadmap) | Confident | [Shallue and Vanderburg 2018, Identifying Exoplanets with Deep Learning](https://arxiv.org/abs/1712.05044) | 8 |
| Statistical methods for planet searches, as professionals teach them | Confident | [Sagan Summer Workshop 2016, "Is There a Planet in My Data?"](https://nexsci.caltech.edu/workshop/2016/) (MCMC, Bayesian inference, noise; videos on the workshop's YouTube channel) | 10 |
| Transit maths in depth | Aware | [Seager and Mallén-Ornelas 2003, unique solution of planet and star parameters from a transit](https://arxiv.org/abs/astro-ph/0206228) | 3 |

Your ML roadmap and Tier 3 overlap heavily (Python, statistics, fitting, Gaussian processes, neural networks for vetting). Count those hours once, for both.

## The Engine Room: what it is and how it avoids clutter

You asked whether a lesson per pipeline file would bury you in 111 explainer files. It would, which is why it should not be built that way.

**The real size of the code.** Of the 111 Python files in `pipeline/`, only about a dozen are the core chain that every search runs through: `dataset.py`, `detect_v2.py`, `stage3_core.py`, `stage3.py`, `vopts.py`, `audit_all.py`, `chain_recovery.py`, `scorecard_plus.py`, `horizon_reach.py`, `stability.py`, `leads_export.py`, plus the tests. That is roughly 2,000 lines. The other 7,000 lines are one-off studies and checks that answered a question once. You need to master the core, be confident reading the tests, and only be aware of the studies.

**Where it lives.** One new Part in the book, called **Engine Room** (not "Workshop", because Chapter 13 is already "Your workshop"), in `book/docs/engine-room/`. Nothing is added next to the code, so the pipeline folder stays exactly as clean as it is. The learning track gets one new level after Level 6, "L7 · Engine Room", which points to it.

**What is in it.** One map page and ten lessons that follow the data from download to lead:

| Lesson | Covers | Files |
|---|---|---|
| Map | every file classed as core, test, study or retired, one line each; this page replaces 111 explainers | all |
| ER1 Getting the light | where data comes from, paths, quality flags | `dataset.py` and the fetch scripts |
| ER2 Cleaning and safe windows | detrending, gaps, borrowed windows | `stage3_core.py` |
| ER3 The detector | box scores, signal-to-noise | `detect_v2.py` (box scores) |
| ER4 The flags and tiers | why a dip is kept or thrown out | `detect_v2.py` (veto), `vopts.py` |
| ER5 The upside-down control and the scorecard | false-alarm counting | `scorecard_plus.py` |
| ER6 Planting fakes | completeness by injection | `chain_recovery.py` |
| ER7 Freezing and fingerprints | versions, hashes, the sealed wrapper | `audit_all.py`, the frozen settings files |
| ER8 Horizon | expected planets and ceilings (including the F2 fix) | `horizon_reach.py`, `stability.py` |
| ER9 Leads | from a dip to the Search window | `leads_export.py` |
| ER10 Tests | how the project proves it did not break itself | the `test_*.py` files |

**How each lesson works.** Five steps, about two to three hours: (1) **Read**, an annotated excerpt of the real code, pinned to the frozen version's fingerprint; (2) **Predict**, a question like "if the box limit drops from 3 hours to 2, what happens to false alarms?", answered in writing before you run anything; (3) **Change**, make that change on a sandbox copy, never the real files; (4) **Check**, run the test and compare with your prediction; (5) **Explain back**, five plain sentences on what the file does, which Claude marks. Being wrong at step 2 is the most useful thing that can happen.

**How it stays honest.** A small guard test checks that every code excerpt quoted in an Engine Room lesson still matches the real file. When the pipeline changes, the guard fails and the lesson gets updated, so the book never teaches you old code.

**Why this is the right home.** The book is already where you learn; the track is already the one path; the levels already end in checks. The Engine Room is the same idea, one level deeper. It is not too much for the learning track, because it is a single new level with its own Part, not changes scattered through Levels 0 to 6.

## Checkpoints at a glance

| Tier | Finish test | Expected by |
|---|---|---|
| Checker | track L0 to L6 checks, all ten labs, blind 10-event vetting test at 8 of 10 | end of January 2027 |
| Engineer | CS50P final project, Engine Room L7 checks, mutation hunt (2 of 3 bugs), one real improvement end to end | about mid-November 2027 |
| Inventor | method proposal survives hostile review, method frozen and run as a preregistered test | 2028 |

## What could go wrong with this plan

The most likely failure is not difficulty; it is the plan being too big for the week you actually have. So the rule is small units, a checkpoint at the end of each, and cutting rather than abandoning. The second risk is studying Second Sun instead of board subjects between February and May. The boards decide where you study next, and the maths in them is the Engineer maths anyway. The third is reading without doing: every row above has an exercise, a problem set, a lab or a test, and those are the only parts that count.
