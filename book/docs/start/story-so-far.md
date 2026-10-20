# The story so far

<p class="ss-meta">Start here · about 12 min · no maths</p>

!!! plain "In plain words"
    We're hunting for planets that orbit **two stars at once**, using free public data from NASA's TESS telescope. So far we've built a search tool, tested it honestly on a planet that's already known, and chosen 549 two-star systems to search. **No new planet yet**, and we haven't searched the 549 yet. The search is paused while you catch up with this book.

**What this page answers:** what happened, in order, and where we stand today. Each day has a longer lesson in the [Field notes](../field-notes/index.md).

## The idea in one paragraph

Some stars come in pairs, two suns orbiting each other. A planet can orbit the **pair**, like Tatooine. When it passes in front of one of the suns, that sun dims a little: a **transit** ([Chapter 2](../book/02-light-curves.md)). With two moving suns, the transits don't arrive on a timetable ([Chapter 5](../book/05-wandering-transits.md)), so the usual search methods miss them. That's our opening. NASA's Kepler telescope found thousands of two-star systems between 2009 and 2013 {{claim:F-030}}. TESS has been watching many of them again since 2018. A planet whose orbit has slowly tilted into view could be crossing now, in TESS data nobody has searched this way. That campaign is called **G1**.

## Day 1: Sunday 19 October 2026, the founding

- **25 rounds of questions** set the rules: what we hunt, how sure we must be, what you decide and what I decide. They're in `RESEARCH-PLAN.md`.
- **Research waves.** I read what's known: only 14 transiting two-sun planets exist {{claim:F-001}}. I measured how big TESS files are on your PC {{claim:F-026}} and checked who else searches.
- **G1 chosen.** From your phone you said: "your searches are great. Follow it."
- **This book was founded,** with a quiet, professional look (your rule: not gamey).
- **Accounts:** you made ORCID and ADS accounts, so later we can sign work and read papers through the official index.

## Night 1: 19 to 20 October, the overnight run

1. **A better detector.** Version 2 of our search re-found the known planet TOI-1338 b in 4 of the 8 sectors where it crossed {{claim:F-014}}. It sees planets down to about 6 Earth sizes in one sector {{claim:F-015}}. Noise alone still makes fake dips {{claim:F-016}}. [Chapter 8](../book/08-our-detector.md)
2. **A prediction came true.** A 2024 paper predicted TOI-1338 b would cross on 16 December 2025. Our search found it that night {{claim:F-011}}, about 56 minutes late. That's interesting, but not proof of anything.
3. **Cleaning fakes automatically failed.** Rejecting dips near spacecraft events also threw away real ones. So now we flag those dips for a human instead.
4. **The G1 list was frozen:** 549 stars from Kepler's catalogue {{claim:F-038}}, with fingerprints of the source files.
5. **QLP data was fixed.** Half of G1 only has QLP light curves (Chapter 3), and they were full of fake dips from scattered light. The fix borrows NASA's good time windows.
6. **Our first real G1 star, Kepler-16:** one dip flagged, and on inspection it was the telescope wobbling before a thruster firing. Nothing survived. [Chapter 10](../book/10-vetting.md)
7. **STANLEY** (the professionals' search tool, Part 5) was installed and run on TOI-1338. It pointed near the right period, but its scores aren't calibrated yet.

## Morning 20 October

- **Compass** was born: your review system that checks every big idea before we build it. Its first verdict on our upgrade plans was **REVISE**.
- **Realistic fake planets** finally worked after I found a bug in STANLEY. Our cleaning keeps 90 to 100% of each dip. We find 6-Earth-size planets 8 times in 10, and about 1 crossing in 11 is lost inside the stars' eclipses {{claim:F-029}}.
- **NASA's candidate site now wants papers first** {{claim:B9}}. That's a decision for you, later.
- **Afternoon: the Bible Overhaul.** Writing the labs caught three of our own errors (a noise number, STANLEY's best period, and a hole in the G1 list), all corrected and logged. The [field note](../field-notes/2026-10-20.md) has the details.
- **Evening: the quality-filter test** (a seventh test in [Chapter 8](../book/08-our-detector.md)). A milder data filter finds the two crossings we couldn't see before, but costs sensitivity elsewhere; and the raw flux gave a quieter noise estimate than the cleaned flux in several sectors. One star only; nothing in the detector changed. [Field note](../field-notes/2026-10-20.md).
- **You paused the hunt** to start this overhaul: "I can't let an AI do all the work while I just sit and say yes or no."

## The honest scoreboard

| Question | Answer today |
|---|---|
| New planets found | **0** |
| Stars searched from G1 | 1 (Kepler-16), as a dry run |
| Smallest planet we can see in one sector | about 6 Earth radii (TOI-1338) |
| Known planet re-found | yes, TOI-1338 b, in 4 of 8 sectors |
| Anything sent to NASA or published | no |

## What's left before the real hunt

1. **Smarter quality flags:** warn about scattered light instead of deleting it.
2. **A pixel check:** is the dip on our star, or on a neighbour? (Chapter 11)
3. **A bigger fake-planet test** (hundreds of planets), so "nothing found" has a measured meaning.
4. **Decide the 136 unmeasured stars:** a quarter of the G1 list has no measured binary shape {{claim:F-052}}. Your call (decision log).
5. **Run G1:** 549 stars, about 6.3 GB of light curves.

## Where to go next

Read [How to read this book](how-to-read.md), then set up your workbench in [Lab 0](../labs/lab0-workbench.md).
