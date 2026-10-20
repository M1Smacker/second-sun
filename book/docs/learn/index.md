# Learning track

<p class="ss-meta">Seven levels · one or two sittings each · your progress line updates when you finish one</p>

!!! plain "In plain words"
    Seven levels take you from "what is a light curve?" to being the **second key**: someone who can check a candidate independently. Each level says what to read, which lab to do on your PC, and ends with three questions. When you can answer them, tell me "L2 done, 3/3" (or whatever level), and I'll set the date on your progress line.

<!-- ss:progress-line -->

## L0 · What a light curve is

**Read:** [Chapter 1](../book/01-stars-names-missions.md), then [Chapter 2](../book/02-light-curves.md) sections 2.1 to 2.2. **Do:** [Lab 0](../labs/lab0-workbench.md), [Lab 1](../labs/lab1-name-to-number.md), [Lab 2](../labs/lab2-get-the-data.md).

??? quiz "L0 check 1. What do the columns TIME, PDCSAP_FLUX and QUALITY hold?"
    When each measurement was taken (BTJD days), the cleaned brightness, and a warning number (0 = fine).

??? quiz "L0 check 2. Kepler-16 is TIC 299096355 and KIC 12644769. Why two numbers?"
    TESS and Kepler each made their own catalogue. The TIC finds the TESS data; the KIC links to Kepler's binary catalogue.

??? quiz "L0 check 3. Magnitude 10 vs magnitude 15: which is brighter, and how much?"
    Magnitude 10, by 5 magnitudes: 100 times.

## L1 · How big is the dip?

**Read:** the [L1 lesson](l1-dip-depth.md) (or Chapter 2, section 2.3). **Do:** [Lab 3](../labs/lab3-plot-and-read.md).

??? quiz "L1 check 1. A dip goes from 1.000 to 0.998. How deep is it in ppm and in percent?"
    0.002 = **2,000 ppm** = 0.2%.

??? quiz "L1 check 2. In Lab 3, Kepler-16's eclipse was about 10% deep. Could that be a planet?"
    No. √0.10 ≈ 0.32: something a third of the star's size. That's a star (the companion), not a planet.

??? quiz "L1 check 3. Why do we divide the flux by its median before measuring a dip?"
    So 1.0 means "normal" and a dip reads directly as a fraction, whatever the star's raw brightness.

## L2 · From dip depth back to size

**Read:** [Chapter 2](../book/02-light-curves.md) sections 2.3 and 2.5; [Chapter 11](../book/11-pixels-and-neighbours.md) section 11.3 (dilution). **Do:** the "Reading it" part of [Lab 4](../labs/lab4-find-a-dip.md).

??? quiz "L2 check 1. A 1,000 ppm dip on a star the size of the Sun. How big is the planet?"
    √0.001 ≈ 0.032 of the Sun's radius; the Sun is 109 Earths across, so about **3.4 Earth radii**.

??? quiz "L2 check 2. The same dip, but only 80% of the light is from our star. True depth?"
    1,000 ÷ 0.8 = **1,250 ppm**, so the planet is √(1/0.8) ≈ 1.12 times bigger than the first estimate.

??? quiz "L2 check 3. Why is a transit's centre deeper than (planet ÷ star)²?"
    Limb darkening: the star's middle is brighter than its edge, so blocking the middle removes more light.

## L3 · Bright stars, faint stars, noise

**Read:** [Chapter 7](../book/07-noise-and-statistics.md), [Chapter 8](../book/08-our-detector.md). **Do:** [Lab 3](../labs/lab3-plot-and-read.md)'s noise table, [Lab 4](../labs/lab4-find-a-dip.md).

??? quiz "L3 check 1. White noise of 2,000 ppm per 2 minutes. Expected wobble of a 2-hour average?"
    2,000 ÷ √60 ≈ **260 ppm**.

??? quiz "L3 check 2. Lab 3 measured 908 ppm for 1 hour where white noise predicts 368. Name the effect."
    **Red noise**: slow drifts that don't average away.

??? quiz "L3 check 3. In Lab 4 at SNR 5, a second event appeared, 15 hours long, next to a data gap. Trust it?"
    No: it's below our bar, it's at a gap edge, and lowering the bar is exactly how noise gets in (Chapter 7's look-elsewhere effect).

## L4 · Orbits, and why our dips wander

**Read:** [Chapter 4](../book/04-two-suns.md), [Chapter 5](../book/05-wandering-transits.md), [Chapter 6](../book/06-orbits-three-body.md). **Do:** [Lab 5](../labs/lab5-two-suns.md).

??? quiz "L4 check 1. Why do a two-star planet's crossings change length?"
    The star moves too. Moving with the planet: slow pass, long crossing. Against it: quick pass, short crossing.

??? quiz "L4 check 2. A binary's critical period is 60 days. Search for 40-day planets?"
    No: closer than the critical orbit, a planet can't survive.

??? quiz "L4 check 3. Why aren't TOI-1338's eclipses exactly half an orbit apart?"
    The stars' orbit is eccentric (stretched).

## L5 · The fakes

**Read:** [Chapter 9](../book/09-fake-planets.md), [Chapter 10](../book/10-vetting.md) sections 10.1 to 10.2. **Do:** [Lab 6](../labs/lab6-fake-planets.md), [Lab 8](../labs/lab8-read-stanley.md).

??? quiz "L5 check 1. Name three things that can fake a planet's dip."
    Any three of: a thruster firing or pointing jitter, a data-gap edge, scattered light, an eclipsing neighbour (blend), the binary's own eclipse edge, stellar variability, noise.

??? quiz "L5 check 2. Why does our search also run on upside-down data?"
    To count how often noise alone crosses the bar with the same number of tries.

??? quiz "L5 check 3. 28% of STANLEY's orbits scored above 5σ. What does that mean for its 18.4σ peak?"
    Its σ scale isn't calibrated: noise scores high here. The peak is encouraging but needs calibrating before it means anything precise.

## L6 · Two-key vetting

**Read:** [Chapter 10](../book/10-vetting.md) sections 10.3 to 10.6, [Chapter 11](../book/11-pixels-and-neighbours.md), [Chapter 12](../book/12-stanley.md). **Do:** [Lab 7](../labs/lab7-pixels.md), [Lab 9](../labs/lab9-your-star.md).

??? quiz "L6 check 1. A dip appears in SPOC data but not in QLP data at the same time. What does rule C8 say?"
    It fails C8: a real dip should show in a second, independently made product.

??? quiz "L6 check 2. The light's centre shifted 0.10″; the chance spread is 0.01″. On-target expectation 0.001″. Verdict?"
    Suspicious: the shift is 10 times the chance spread and far above the on-target expectation, so a neighbour may be the source.

??? quiz "L6 check 3. What does 'second key' mean?"
    You independently check a candidate and decide whether you agree, before anything is submitted. Both keys must turn.

## Sources
The levels follow the course design in `research/burn-3-book/learning-track.md` (19 October). Facts used here are in the chapters' sources.
