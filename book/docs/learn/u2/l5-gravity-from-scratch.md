---
hide: [toc, footer]
title: "2.5 Gravity from scratch"
---

# Gravity from scratch

The two stars' clock from lesson 2.1: an eclipse every 19.7 days, again and again.

<div class="tw-plot" data-src="u2-four-sectors"></div>

<p class="tw-plot__ask">These stars are about 3 billion years old and have kept this beat the whole time. Nothing pushes them. What keeps them going round, and what sets the 19.7 days?</p>

## Falling, and missing

In lesson 2.1 we used Kepler's law, \(P^2 = a^3 / M\), as a rule handed down. Kepler found it in 1619 by staring at tables of planet positions, and he never knew why it worked. Isaac Newton found the why about 70 years later, and you can follow his argument with nothing more than the maths you already have.

Start with a thought experiment Newton drew himself. Stand on a very tall mountain and throw a stone sideways. It curves down and lands. Throw it faster and it lands farther away. Now throw it so fast that, as it falls, the round Earth curves away beneath it just as fast as it drops. It keeps falling and never lands. That is an orbit: **falling all the time, and always missing**. The astronauts on the space station are not floating because gravity is gone up there (it is about 90% as strong as on the ground); they float because they and their station are falling together.

<aside class="tw-mn" markdown>
**Orbit.** A path where an object falls towards another forever but moves sideways fast enough to keep missing it.
</aside>

## The pull: Newton's law of gravity

Newton's second idea: every mass pulls every other mass, and the pull weakens with distance in a very particular way. Twice as far, a quarter of the pull. Three times as far, a ninth. This is the **inverse-square law**, and it is the same square as in lesson 2.3, for the same reason: whatever spreads out from a point is shared over a sphere whose area grows as the distance squared.

<aside class="tw-mn" markdown>
**Inverse-square law.** A pull (or a light) that falls as \(1/r^2\): double the distance, a quarter of the strength.
</aside>

The pull on each kilogram of a planet, at distance \(r\) from a star of mass \(M\), is

\[ g = \frac{G M}{r^2} \]

where \(G\) is Newton's gravitational constant, the same everywhere in the universe. For the Sun, the product \(GM\) is measured very precisely: \(1.3271 \times 10^{20}\) in metres cubed per second squared.

<aside class="tw-mn" markdown>
**\(G\).** Newton's constant, \(6.674 \times 10^{-11}\) in SI units. Tiny: gravity is by far the weakest force, and only matters because stars and planets are so massive.
</aside>

## Think it through

<div class="tw-prob" data-answer="9" data-tol="0.01" data-hints='{"3":"Inverse square: 3 times farther means 3 x 3.","0.111":"The question asks how many times weaker: 9."}' data-why="The pull goes as 1/r squared: 3 x 3 = 9 times weaker." markdown>
**a.** A planet moves to three times its old distance from its star. How many times weaker is the star's pull on it?
</div>

<div class="tw-prob" data-answer="no" data-why="The pull per kilogram, GM/r squared, contains only the star's mass, so a pebble and a planet fall alike." markdown>
**b.** Look at \(g = GM/r^2\). Does the planet's own mass appear in it? (Yes or no.)
</div>

That answer b is Galileo's dropped balls all over again: a heavy and a light ball fall together, and a pebble and a giant planet at the same distance from a star follow the same orbit (as long as they are tiny next to the star).

## The speed an orbit needs

For a circle of radius \(r\), moving at speed \(v\), the pull needed to keep bending the path into the circle is \(v^2 / r\) per kilogram. In an orbit, gravity supplies exactly that pull:

\[ \frac{v^2}{r} = \frac{G M}{r^2} \quad\Longrightarrow\quad v = \sqrt{\frac{G M}{r}} \]

<aside class="tw-mn" markdown>
**Why \(v^2/r\).** Faster means more bending each second, and a tighter circle means sharper bending. Both together give \(v^2/r\), a result Christiaan Huygens and Newton worked out in the 1600s.
</aside>

!!! example "Worked example: how fast is the Earth moving?"
    **Step 1. The numbers.** \(GM_\odot = 1.3271 \times 10^{20}\); \(r = 1\) AU \(= 1.4960 \times 10^{11}\) m.

    **Step 2. Divide.** \(1.3271 \times 10^{20} / 1.4960 \times 10^{11} = 8.871 \times 10^{8}\).

    **Step 3. Square root.** \(\sqrt{8.871 \times 10^{8}} = 29{,}780\) m/s.

    **Step 4. Into km/s.** About 29.8 km/s: the Earth carries you round the Sun at 30 km every second, about 100,000 km every hour.

!!! question "Your turn, half done: the planet around our two stars"
    It feels the pull of both stars, \(M = 2.440\) Suns, at \(r = 0.90\) AU (lesson 2.1). Since \(v = \sqrt{GM/r}\), compared with the Earth the speed changes by \(\sqrt{2.440 / 0.90}\). Step 1: \(2.440 / 0.90 = 2.711\). Finish: take the square root and multiply by 29.78 km/s.

<div class="tw-prob" data-answer="49.0" data-tol="0.02" data-unit="km/s" data-hints='{"1.65":"That is the factor. Multiply by 29.78 km/s.","80.7":"Take the square root of 2.711 first."}' data-why="The square root of 2.711 is 1.647; times 29.78 = 49.0 km/s." markdown>
**Your turn.** The planet's speed, in km/s:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(\sqrt{2.711} = 1.647\), and \(1.647 \times 29.78 = 49.0\) km/s. This is the "about 50 km/s" lesson 2.2 used.

The rule: **\(v = \sqrt{GM/r}\).** More mass, faster orbit; farther out, slower.

</details>
</div>

## Kepler's law falls out

Now the period. One trip round the circle is a distance \(2\pi r\), done at speed \(v\), so \(P = 2\pi r / v\). Put in the speed and square both sides:

\[ P^2 = \frac{4\pi^2 r^2}{v^2} = \frac{4\pi^2 r^2}{G M / r} = \frac{4\pi^2}{G}\,\frac{r^3}{M} \]

That is Kepler's third law: \(P^2\) grows with \(r^3\) and shrinks with \(M\). The only extra piece is the constant \(4\pi^2 / G\). Measure \(P\) in years, \(r\) in AU and \(M\) in Suns, and that constant becomes exactly 1, because those units are defined by the Earth's own orbit. That is why lesson 2.1 could write simply \(P^2 = a^3/M\).

The same law, read backwards, is how astronomers **weigh** things. Measure an orbit's size and period, and the mass inside it follows. The discovery paper weighed our two stars to better than 0.1% this way, from their eclipses and their measured speeds.

## In a few sentences

An orbit is falling while moving sideways fast enough to keep missing. Gravity pulls each kilogram with \(GM/r^2\), weaker as the square of the distance, the same for a pebble and a planet. Making that pull bend the path into a circle gives the orbit speed \(v = \sqrt{GM/r}\): 29.8 km/s for the Earth, 49 km/s for the planet around our pair. Working out the period from that speed gives Kepler's third law, and turns every orbit into a scale for weighing stars.

## Problems

<div class="tw-prob" data-answer="14.9" data-tol="0.02" data-unit="km/s" data-hints='{"7.4":"The speed goes with one over the SQUARE ROOT of the distance: divide by 2, not 4.","59.6":"Farther out is slower, not faster."}' data-why="v goes as 1/sqrt(r): the square root of 4 is 2, so 29.78 / 2 = 14.9 km/s." markdown>
**1.** How fast would a planet orbit the Sun at 4 AU, in km/s?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(v \propto 1/\sqrt{r}\). \(\sqrt{4} = 2\), so \(29.78 / 2 = 14.9\) km/s. (Jupiter, at 5.2 AU, moves at about 13 km/s.)

</details>
</div>

<div class="tw-prob" data-answer="92.4|92" data-tol="0.02" data-unit="minutes" data-hints='{"5545":"That is in seconds. Divide by 60.","1.54":"That is in hours. The question asks for minutes."}' data-why="v = sqrt(3.986e14 / 6.771e6) = 7,673 m/s; P = 2 pi r / v = 5,545 s = 92.4 minutes." markdown>
**2.** The space station flies about 400 km up, so \(r = 6{,}771\) km from the Earth's centre. For the Earth, \(GM = 3.986 \times 10^{14}\). First its speed, then its time for one orbit, in minutes.

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(r = 6.771 \times 10^6\) m. \(v = \sqrt{3.986 \times 10^{14} / 6.771 \times 10^{6}} = \sqrt{5.887 \times 10^{7}} = 7{,}673\) m/s. One orbit: \(2\pi r = 4.254 \times 10^{7}\) m, so \(P = 4.254 \times 10^{7} / 7{,}673 = 5{,}545\) s \(= 92.4\) minutes. The crew sees about 16 sunrises a day.

</details>
</div>

<div class="tw-prob" data-answer="0.5|1/2|half" data-tol="0.02" data-hints='{"0.25":"P squared goes as 1/M, so P goes as one over the SQUARE ROOT of M.","2":"More mass pulls harder: the orbit is quicker, not slower."}' data-why="P squared = r cubed / M: four times the mass makes P squared a quarter, so P is half." markdown>
**3.** A planet orbits at the same distance as the Earth, but around a star four times the Sun's mass. How many times the Earth's year is its year?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(P^2 = r^3/M = 1/4\), so \(P = 1/2\): half a year. A heavier star pulls harder, so the planet has to move faster to keep missing it, and goes round sooner.

</details>
</div>

<div class="tw-prob" data-answer="falling|they are falling|free fall|freefall" data-why="They and the station fall together around the Earth, so nothing presses them against the floor." markdown>
**4.** Astronauts on the space station float. Is gravity missing up there, or are they doing something? Say in one word what they are doing.

<details class="tw-sol" markdown><summary>Worked solution</summary>

**Falling.** Gravity there is about 90% of its pull on the ground. The crew and the station fall around the Earth together, so the floor never pushes back on their feet.

</details>
</div>

## Sources

- \(GM\) of the Sun \(1.32712 \times 10^{20}\) m³/s² and of the Earth \(3.986004 \times 10^{14}\) m³/s²: IAU 2015 Resolution B3 nominal values; 1 AU = 149,597,870,700 m (IAU 2012 Resolution B2). \(G = 6.674 \times 10^{-11}\) (CODATA).
- Kepler's third law, 1619 (Harmonices Mundi); Newton's cannon and law of gravitation, Principia (1687). Any history of astronomy, for example OpenStax Astronomy 2e, chapter 3 "Orbits and Gravity" ([the book](https://openstax.org/details/books/astronomy-2e), CC BY-NC-SA 4.0).
- The stars' age (3.1 billion years) and masses (to better than 0.1%): Kostov et al. 2021 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614)).
- Space station altitude about 400 km, gravity there about 90% of the surface value (\((6371/6771)^2 = 0.885\)): our arithmetic; the station's real height varies, roughly 400 to 420 km.
- All speeds and periods in this lesson: our own arithmetic (15 Nov 2026).
