# Learning track

<p class="ss-meta">Seven levels and a last step · one or two sittings each · your progress line updates when you finish one</p>

!!! plain "In plain words"
    This is the one path through the book. Start at Level 0 and go in order: each level builds on the one before, from "what is a light curve?" up to being the **second key**, someone who can check a candidate independently. Each level says what to read, in order, which lab to do on your PC (optional), and ends with three questions. When you can answer them, tell me "L2 done, 3/3" (or whatever level), and I'll set the date on your progress line.

<!-- ss:progress-line -->

## The path at a glance

<!-- ss:track -->

The chapter numbers are permanent labels, so the path visits them out of numeric order on purpose. Level 3 comes before Level 4 because you should learn to measure a dip, and to distrust the noise, before you meet the orbits that make our dips hard to predict. If you would rather browse by topic, the Read menu lists the chapters in six Parts, and [How the project unfolded](../start/journey.md) tells the project as a story.

## L0 · What a light curve is { #l0 }

**Read:** [Chapter 1](../book/01-stars-names-missions.md), then [Chapter 2](../book/02-light-curves.md) sections 2.1 to 2.2, then [Chapter 3](../book/03-our-data.md). **Do:** [Lab 0](../labs/lab0-workbench.md), [Lab 1](../labs/lab1-name-to-number.md), [Lab 2](../labs/lab2-get-the-data.md).

??? quiz "L0 check 1. What do the columns TIME, PDCSAP_FLUX and QUALITY hold?"
    When each measurement was taken (BTJD days), the cleaned brightness, and a warning number (0 = fine).

??? quiz "L0 check 2. Kepler-16 is TIC 299096355 and KIC 12644769. Why two numbers?"
    TESS and Kepler each made their own catalogue. The TIC finds the TESS data; the KIC links to Kepler's binary catalogue.

??? quiz "L0 check 3. Magnitude 10 vs magnitude 15: which is brighter, and how much?"
    Magnitude 10, by 5 magnitudes: 100 times.

**Next:** [Level 1](#l1).

## L1 · How big is the dip? { #l1 }

**Read:** the [L1 lesson](l1-dip-depth.md) (or Chapter 2, section 2.3). **Do:** [Lab 3](../labs/lab3-plot-and-read.md).

??? quiz "L1 check 1. A dip goes from 1.000 to 0.998. How deep is it in ppm and in percent?"
    0.002 = **2,000 ppm** = 0.2%.

??? quiz "L1 check 2. In Lab 3, Kepler-16's eclipse was about 10% deep. Could that be a planet?"
    No. √0.10 ≈ 0.32: something a third of the star's size. That's a star (the companion), not a planet.

??? quiz "L1 check 3. Why do we divide the flux by its median before measuring a dip?"
    So 1.0 means "normal" and a dip reads directly as a fraction, whatever the star's raw brightness.

**Next:** [Level 2](#l2).

## L2 · From dip depth back to size { #l2 }

**Read:** [Chapter 2](../book/02-light-curves.md) sections 2.3 and 2.5, and one section from further on, [Chapter 11](../book/11-pixels-and-neighbours.md) section 11.3 (dilution). That is a short look ahead: read only that section now, and the rest of Chapter 11 when you reach Level 6. **Do:** the "Reading it" part of [Lab 4](../labs/lab4-find-a-dip.md).

??? quiz "L2 check 1. A 1,000 ppm dip on a star the size of the Sun. How big is the planet?"
    √0.001 ≈ 0.032 of the Sun's radius; the Sun is 109 Earths across, so about **3.4 Earth radii**.

??? quiz "L2 check 2. The same dip, but only 80% of the light is from our star. True depth?"
    1,000 ÷ 0.8 = **1,250 ppm**, so the planet is √(1/0.8) ≈ 1.12 times bigger than the first estimate.

??? quiz "L2 check 3. Why is a transit's centre deeper than (planet ÷ star)²?"
    Limb darkening: the star's middle is brighter than its edge, so blocking the middle removes more light.

**Next:** [Level 3](#l3), which starts with Chapter 7.

## L3 · Bright stars, faint stars, noise { #l3 }

**Read:** [Chapter 7](../book/07-noise-and-statistics.md) (newest part: "Noise is lopsided"), then [Chapter 8](../book/08-our-detector.md) (newest part: "Flags, tiers and frozen settings"). For the story behind both, read [The first real search](../start/first-search.md). **Do:** [Lab 3](../labs/lab3-plot-and-read.md)'s noise table, [Lab 4](../labs/lab4-find-a-dip.md).

??? quiz "L3 check 1. White noise of 2,000 ppm per 2 minutes. Expected wobble of a 2-hour average?"
    2,000 ÷ √60 ≈ **260 ppm**.

??? quiz "L3 check 2. Lab 3 measured 908 ppm for 1 hour where white noise predicts 368. Name the effect."
    **Red noise**: slow drifts that don't average away.

??? quiz "L3 check 3. In Lab 4 at SNR 5, a second event appeared, 15 hours long, next to a data gap. Trust it?"
    No: it's below our bar, it's at a gap edge, and lowering the bar is exactly how noise gets in (Chapter 7's look-elsewhere effect).

??? quiz "L3 check 4. Why does an upside-down light curve find MORE false dips than a real one would from noise alone?"
    Noise is lopsided: flares and glitches jump up more than down, and upside-down they become dips. At signal-to-noise 7 we measured 2.3 times as many (see Chapter 7).

??? quiz "L3 check 5. Why is a scrambled control the wrong control for a search for single dips?"
    Scrambling moves big blocks of time but keeps the order inside each block, so a single dip survives it. It only destroys repeating signals.

??? quiz "L3 check 6. We froze all settings before reading any result. What does that protect us from?"
    From quietly tuning the rules until the answer looks good. Every number can be traced to the exact rules that made it.

**Next:** [Level 4](#l4), which starts with Chapter 4.

## L4 · Orbits, and why our dips wander { #l4 }

**Read:** [Chapter 4](../book/04-two-suns.md), then [Chapter 5](../book/05-wandering-transits.md), then [Chapter 6](../book/06-orbits-three-body.md). **Do:** [Lab 5](../labs/lab5-two-suns.md).

??? quiz "L4 check 1. Why do a two-star planet's crossings change length?"
    The star moves too. Moving with the planet: slow pass, long crossing. Against it: quick pass, short crossing.

??? quiz "L4 check 2. A binary's critical period is 60 days. Search for 40-day planets?"
    No: closer than the critical orbit, a planet can't survive.

??? quiz "L4 check 3. Why aren't TOI-1338's eclipses exactly half an orbit apart?"
    The stars' orbit is eccentric (stretched).

**Next:** [Level 5](#l5), which starts with Chapter 9.

## L5 · The fakes { #l5 }

**Read:** [Chapter 9](../book/09-fake-planets.md) (newest part: "Completeness"), then [Chapter 10](../book/10-vetting.md) sections 10.1 to 10.2 (the rest of Chapter 10 waits for Level 6). **Do:** [Lab 6](../labs/lab6-fake-planets.md), [Lab 8](../labs/lab8-read-stanley.md).

??? quiz "L5 check 1. Name three things that can fake a planet's dip."
    Any three of: a thruster firing or pointing jitter, a data-gap edge, scattered light, an eclipsing neighbour (blend), the binary's own eclipse edge, stellar variability, noise.

??? quiz "L5 check 2. Why does our search also run on upside-down data?"
    To count how often noise alone crosses the bar with the same number of tries.

??? quiz "L5 check 3. 28% of STANLEY's orbits scored above 5σ. What does that mean for its 18.4σ peak?"
    Its σ scale isn't calibrated: noise scores high here. The peak is encouraging but needs calibrating before it means anything precise.

??? quiz "L5 check 4. What is completeness, and how do we measure it?"
    The share of real planets a search would catch. We hide fake planets in real data and count how many come back through every rule: 82.7% of strong ones got through the flag chain.

??? quiz "L5 check 5. Name two things our completeness number does NOT cover."
    Faint planets, and planets that cross near the edge of the data. (Also: the second-product check and some flags are not in the number.)

??? quiz "L5 check 6. A new filter idea catches 3 points more fake planets. Why is that not enough to adopt it?"
    It must also stay inside the false-alarm budget written before the test (here at most 8 upside-down first-tier dips per 1,000 star-sectors). Catching more fakes while letting through more noise is moving the bar, not improving.

??? quiz "L5 check 7. Most false alarms were found by the 3 hour box. We removed it, and they were found by the 4 hour box. What does that teach?"
    Where something is found is not what causes it. The cause was short glitches; the shortest box simply caught them first.

**Next:** [Level 6](#l6), which starts with the rest of Chapter 10.

## L6 · Two-key vetting { #l6 }

**Read:** [Chapter 10](../book/10-vetting.md) sections 10.3 to 10.6, then [Chapter 11](../book/11-pixels-and-neighbours.md), then [Chapter 12](../book/12-stanley.md). **Do:** [Lab 7](../labs/lab7-pixels.md), [Lab 9](../labs/lab9-your-star.md).

??? quiz "L6 check 1. A dip appears in SPOC data but not in QLP data at the same time. What does rule C8 say?"
    It fails C8: a real dip should show in a second, independently made product.

??? quiz "L6 check 2. The light's centre shifted 0.10″; the chance spread is 0.01″. On-target expectation 0.001″. Verdict?"
    Suspicious: the shift is 10 times the chance spread and far above the on-target expectation, so a neighbour may be the source.

??? quiz "L6 check 3. What does 'second key' mean?"
    You independently check a candidate and decide whether you agree, before anything is submitted. Both keys must turn.

??? quiz "L6 check 4. Why can a dip within 1 day after data resumes not be trusted?"
    TESS is settling and scattered light is strongest there, which fakes slow dips. The price of the rule is about 14% of the time.

??? quiz "L6 check 5. Why can a planet around two stars not make three transits in one 27-day sector?"
    It must orbit beyond the stability limit, at least about 3.7 binary periods, so for a binary of 5 days or more it needs about 15 days per lap. At most two transits fit.

??? quiz "L6 check 6. A dip sits on a star that is a TESS Object of Interest. What do you do first?"
    Look the star up: TOIs, known hosts and catalogued eclipsing binaries are known objects, so a dip there is probably the known thing and not a discovery.

??? quiz "L6 check 7. Two dips on one star, in different sectors, are exactly 12 binary orbits apart with the same length and depth. Planet?"
    Probably not. A leftover eclipse keeps the binary's clock; a planet keeps its own. v8's orbit-locked flag moves such dips to tier 2.

??? quiz "L6 check 8. Why is it a good sign that a published candidate says 'no statistical validation is claimed' and gives its predicted dip times in advance?"
    It tells readers exactly what is and is not shown, and it lets new data judge the claim fairly: if the star does not dim on time, the claim fails in public. That is the same idea as our preregistration and sealed stars.

??? quiz "L6 check 9. Why does the sealed run go through a wrapper file that sits outside the frozen code?"
    Changing any frozen file changes the version fingerprint. A wrapper outside that list can check the fingerprint, refuse to start if it differs, and still be edited, so the guard and the frozen rules cannot get in each other's way.

**Next:** [After Level 6](#after): how the project runs.

## After Level 6 · Running the project { #after }

These three chapters are not part of the readiness bar. They are how a careful project is run, and you can read them any time after Level 6.

**Read:** [Chapter 13](../book/13-your-workshop.md), then [Chapter 14](../book/14-credit-and-publishing.md), then [Chapter 15](../book/15-mistakes-as-lessons.md).

??? quiz "After L6, check 1. In 2026 NASA's candidate site started wanting something published before it takes a candidate. What?"
    The write-up (a paper or note) comes first. So the order is: find a dip, check it with both keys, publish, and only then submit the candidate.

??? quiz "After L6, check 2. Where would you look to find out why we made a decision, and where to find a mistake we logged?"
    Decisions are in `research/decisions.md` and mistakes in `research/mistakes.md`. Results, with their labels and sources, are on the facts page (the claims register).

??? quiz "After L6, check 3. Chapter 15 groups fifteen mistakes into five patterns and keeps a rule for each. Why write a rule instead of just fixing the mistake?"
    A fix repairs one case. A written rule stops the same pattern coming back, anywhere in the work.

That is the end of the track. The Hunt tab shows where the project stands now.

## Sources
The levels follow the course design in `research/burn-3-book/learning-track.md` (19 October). On 27 October 2026 the track became the book's one reading order (see the Compass review `research/compass-reviews/2026-10-27-learning-spine.md`). Facts used here are in the chapters' sources.
