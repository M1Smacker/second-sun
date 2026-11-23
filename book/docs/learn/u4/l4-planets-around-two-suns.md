---
hide: [toc, footer]
title: "4.4 Planets around two suns"
---

# Planets around two suns

Lesson 1.4 showed these two dips and said Unit 4 would explain them. Here they are again: the same planet crossing in front of the first star, and then, 4.9 days later, in front of the second.

<div class="tw-plot" data-src="u1-planet-a"></div>

<div class="tw-plot" data-src="u1-planet-b"></div>

<p class="tw-plot__ask">One planet, two dips, five days apart, and the first one lasts longer. Before reading on, guess: with one star, could a planet ever make two dips five days apart?</p>

## The planet circles the pair

The two stars of TIC 172900988 swing round each other every 19.66 days (lessons 4.1 and 4.2). The planet goes round both of them together, much farther out: about 0.9 AU, once in about 200 days (lesson 2.1). From that far away the pair pulls like one star of 2.44 Suns, which is why Kepler's third law with the total mass gives the planet's orbit.

<aside class="tw-mn" markdown>
**Circumbinary planet.** A planet that orbits both stars of a binary, outside their own orbit. Its name comes from "around" (circum) and "the binary". The other kind, a planet around just one star of a pair, is called circumstellar.
</aside>

The planet takes a long time to cross the pair: while it passes, the stars below keep moving on their small ovals. So the planet can pass in front of one star, and a few days later in front of the other, which has moved into its path. That is what TESS saw in January 2020.

## Why the two dips have different lengths

A dip lasts as long as the planet takes to cross the star's disc, and what matters is the **relative** speed: the planet's speed minus the star's speed in the same direction. If the star moves the same way as the planet, the planet overtakes it slowly and the dip is long; if the star moves the other way, they pass quickly and the dip is short.

\[ T \approx \frac{\text{chord across the star}}{v_{\text{planet}} - v_{\text{star}}} \]

<aside class="tw-mn" markdown>
**Chord.** The length of the planet's path across the star's disc: the full diameter \(2R_\star\) for a crossing through the middle, shorter for one near the edge.
</aside>

The planet moves at about \(2\pi \times 0.9\) AU in 200 days, about 49 km/s. The stars, each on its own 0.09 AU oval, move between about 32 and 85 km/s (lesson 4.2), in directions that keep changing. So from one crossing to the next, the relative speed changes a lot, and so does the dip's length. With one star, every transit of a planet on a round orbit lasts the same time.

## Think it through

<div class="tw-prob" data-answer="49|48.9" data-tol="0.03" data-unit="km/s" data-hints='{"0.028":"That is AU per day. Turn AU into km (1 AU = 149.6 million km) and days into seconds (86,400 s)."}' data-why="2 pi x 0.901 x 149.6e6 km = 8.47e8 km; 200 days = 1.728e7 s; 8.47e8 / 1.728e7 = 49 km/s." markdown>
**a.** The planet's orbit is about 0.901 AU in radius and takes 200 days. Its speed, \(2\pi a / P\), in km/s? (1 AU = 149.6 million km.)
</div>

!!! example "Worked example: the fastest the planet could pass the first star"
    The first dip lasts about 0.4 days (Kostov et al. 2021). Star 1's radius is 1.384 Suns, and the Sun's radius is 696,000 km.

    **Step 1. The longest possible chord.** \(2 \times 1.384 \times 696{,}000 = 1.93 \times 10^{6}\) km, the full diameter.

    **Step 2. The time in seconds.** \(0.4 \times 86{,}400 = 34{,}560\) s.

    **Step 3. The relative speed.** \(1.93 \times 10^{6} / 34{,}560 = 56\) km/s. A crossing off the middle has a shorter chord, so this is the **largest** relative speed the dip allows.

!!! question "Your turn, half done: the second star"
    The second dip lasts about 0.27 days; star 2's radius is 1.312 Suns. Step 1: \(2 \times 1.312 \times 696{,}000 = 1.83 \times 10^{6}\) km. Finish: the largest relative speed, in km/s.

<div class="tw-prob" data-answer="78|78.3" data-tol="0.04" data-unit="km/s" data-hints='{"0.078":"You kept metres and kilometres mixed. The chord is in km and the time in seconds: the answer is in km/s.","6.8":"The time must be in seconds: 0.27 x 86,400 = 23,328 s."}' data-why="0.27 x 86,400 = 23,328 s; 1.83e6 / 23,328 = 78 km/s." markdown>
**Your turn.** The relative speed, in km/s:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(0.27 \times 86{,}400 = 23{,}328\) s, and \(1.83 \times 10^{6} / 23{,}328 = 78\) km/s.

The planet passed the second star at up to 78 km/s and the first at up to 56 km/s, with the planet itself moving at about 49 km/s. If both crossings went near the middle of the stars, star 2 was moving against the planet at the second crossing and star 1 almost with it at the first. We do not know the chords, so this is a reading of the numbers, not a measurement.

The rule: **dip length = chord / relative speed**.

</details>
</div>

## The broken clock

Around one star, a planet's dips repeat like a clock: same spacing, same length, same depth, every orbit. Around two suns, each time the planet comes round the stars are somewhere else on their ovals. The next dip may come days early or late, may cross only one star, may be longer or shorter, or may not happen at all, because the stars may both be outside the planet's path at that moment. Over years there is a deeper reason the dips can stop: the stars' pull slowly turns the tilt of the planet's orbit, so for long stretches its path misses both stars.

That broken clock is the reason for one of our project's biggest design choices. The standard way to find planets folds the light on a trial period and looks for dips that line up. A planet around two suns does not line up, so our search looks for **single dips** one at a time, and judges each one on its own.

## How deep: the same rule as lesson 2.4

The planet's radius is about 11.25 Earth radii, about 0.103 Sun radii (Kostov et al. 2021). Crossing star 1 alone it would block \((0.103 / 1.384)^{2} = 0.55\%\) of that star's light; but TESS also collects star 2's light, so the dip is diluted to star 1's share of the total, 0.537 (lesson 4.1): about 0.30%, or 3,000 ppm. The paper reports dips of about 3,000 ppm. Our lesson 1.4 measurements are smaller for the first dip (about 1,900 ppm), which a crossing near the star's edge, where it is darker, can explain; we have not tested that.

## In a few sentences

A circumbinary planet circles both stars of a pair, far outside their own orbit, while the stars swing round each other underneath. Its dips last chord divided by relative speed, so they change length as the stars move with or against it: 0.4 and 0.27 days for TIC 172900988, meaning relative speeds of at most 56 and 78 km/s for a planet moving at 49 km/s. The dips do not repeat like a clock, which is why our search judges single dips instead of folding on a period.

## Problems

<div class="tw-prob" data-answer="0.25|0.249" data-tol="0.04" data-hints='{"4.0":"Upside down: 4.9 days divided by the 19.66-day binary orbit."}' data-why="4.9 / 19.66 = 0.249: a quarter of the binary's orbit." markdown>
**1.** The two dips are 4.9 days apart. What share of the binary's 19.66-day orbit is that?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(4.9 / 19.66 = 0.25\). In a quarter of their orbit the two stars swung round enough for the second one to move into the planet's path.

</details>
</div>

<div class="tw-prob" data-answer="3000|2970|2967" data-tol="0.04" data-unit="ppm" data-hints='{"5530":"That is the share of star 1 alone. TESS also sees star 2: multiply by star 1 share of the light, 0.537."}' data-why="(0.103 / 1.384)^2 = 0.00554; x 0.537 = 0.00297, about 2,970 ppm." markdown>
**2.** Use the dilution rule: a planet of 0.103 Sun radii crossing star 1 (1.384 Sun radii), which gives 0.537 of the pair's light. How deep is the dip, in ppm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\((0.103 / 1.384)^{2} = 0.00554\), and \(0.00554 \times 0.537 = 0.00297\): about **2,970 ppm**, the size the paper reports.

</details>
</div>

<div class="tw-prob" data-answer="no" data-why="The stars are somewhere else on their orbits each time, so the timing, length and even the existence of the next dip change." markdown>
**3.** The planet's orbit takes about 200 days. Will its next dip come exactly 200 days after one of these? (Yes or no.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**No.** After 200 days the stars are at a different point of their 19.66-day dance (200 is not a whole number of 19.66-day orbits: \(200 / 19.66 = 10.17\)), so the planet meets them in different places, and the dip comes early, late, or not at all.

</details>
</div>

<div class="tw-prob" data-answer="single|single dips|one at a time|single dip" data-hints='{"fold":"Folding on a period lines up repeating dips. These do not repeat on a steady period."}' data-why="The dips do not repeat on a steady period, so folding cannot stack them; each dip is judged alone." markdown>
**4.** Our search does not fold the light on trial periods. What does it look for instead? (Two words.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**Single dips**, each judged on its own, because a circumbinary planet's dips do not line up on any steady period.

</details>
</div>

## Sources

- The two dips: TESS sector 21, QLP full-frame light of TIC 172900988 (30-minute points), MAST; the same plots and measurements as lesson 1.4 (`book/tools/lesson_plots.py`). Our 30-minute points stay below half depth for about 7.5 and 6.0 hours.
- The system and the dips: Kostov et al. 2021, AJ 162, 234 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614), read 23 Nov 2026): the planet "transited the primary star and then 5 days later it transited the secondary star"; dip depths "about 3,000 ppm" and lengths "about 0.4 days and about 0.27 days" (section 2.1); planet radius 11.25 Earth radii (abstract); orbit about 189 to 204 days (abstract); star radii 1.384 and 1.312 Suns (Table 5).
- The Sun's radius 696,000 km and 1 AU = 149.6 million km: IAU nominal values (the IAU 2015 resolution B3 gives 695,700 km; we round). Circumbinary transits that change in timing and length, and an orbit whose tilt slowly turns: Doyle et al. 2011, "Kepler-16: A Transiting Circumbinary Planet", Science 333, 1602 ([abstract](https://ui.adsabs.harvard.edu/abs/2011Sci...333.1602D/abstract)), in our own words.
