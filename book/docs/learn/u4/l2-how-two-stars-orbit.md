---
hide: [toc, footer]
title: "4.2 How two stars orbit each other"
---

# How two stars orbit each other

Lesson 4.1 found that this pair's orbit is stretched, because its second eclipse comes late. Here is what the stretch means in space: the distance between the two stars through one orbit.

<div class="tw-plot" data-src="u4-separation"></div>

<p class="tw-plot__ask">The distance swings from about 0.11 AU to about 0.28 AU and back, every 19.66 days. Before reading on, guess: are the stars moving at the same speed all the way round?</p>

## Both stars move

With a planet and a star, lesson 3.4 found that both circle their shared centre of mass, and the heavy star barely moves. With two stars of almost the same mass, both move almost equally. Each star traces its own stretched oval around the balance point, always on opposite sides of it, like the two ends of a see-saw that also spins.

The balance rule from lesson 3.4, \(M_1 v_1 = M_2 v_2\), also fixes the size of each star's oval. If the two stars are a distance \(a\) apart on average, star 1's oval is a share of it set by the **other** star's mass:

\[ a_1 = a \times \frac{M_2}{M_1 + M_2}, \qquad a_2 = a \times \frac{M_1}{M_1 + M_2} \]

<aside class="tw-mn" markdown>
**Semi-major axis \(a\).** Half the long width of an orbit's oval: the stars' average distance apart. Lesson 2.1 found 0.192 AU for this pair from Kepler's third law, using the two stars' total mass.
</aside>

## Fast when close, slow when far

Kepler's second law says a line joining the two stars sweeps out equal areas in equal times. When they are close, the line is short, so it must swing round fast to cover the same area; when they are far apart it is long and swings slowly. For the two ends of the orbit this gives a simple rule: **distance times speed is the same at the nearest and the farthest point**,

\[ r_{\text{near}} \, v_{\text{near}} = r_{\text{far}} \, v_{\text{far}} \]

<aside class="tw-mn" markdown>
**Periastron and apastron.** The points of a two-star orbit where the stars are nearest to and farthest from each other. (For an orbit around the Sun the words are perihelion and aphelion.)
</aside>

## Think it through

<div class="tw-prob" data-answer="2.62|2.6|2.623" data-tol="0.03" data-hints='{"0.38":"That is far over near the wrong way. Speed is larger where the distance is smaller: divide the far distance by the near one."}' data-why="v_near / v_far = r_far / r_near = 0.278 / 0.106 = 2.62." markdown>
**a.** Touch the plot: the stars are 0.106 AU apart at their nearest and 0.278 AU at their farthest. How many times faster do they move at their nearest point than at their farthest?
</div>

!!! example "Worked example: each star's share of the orbit"
    Star 1 has 1.2384 Suns of mass, star 2 has 1.2019, and their average distance apart is 0.192 AU.

    **Step 1. Total mass.** \(1.2384 + 1.2019 = 2.4403\) Suns.

    **Step 2. Star 1's share, set by star 2's mass.** \(1.2019 / 2.4403 = 0.4925\).

    **Step 3. Star 1's oval.** \(a_1 = 0.192 \times 0.4925 = 0.0945\) AU. The heavier star makes the slightly smaller oval.

!!! question "Your turn, half done: star 2"
    Star 2's share is set by star 1's mass: \(1.2384 / 2.4403 = 0.5075\). Finish: the size of star 2's oval, in AU.

<div class="tw-prob" data-answer="0.0974|0.097" data-tol="0.02" data-unit="AU" data-hints='{"0.0945":"That is star 1. Star 2 uses star 1 mass on top: 0.5075 of 0.192 AU.","0.5075":"That is the share. Multiply by the 0.192 AU average distance."}' data-why="0.192 x 0.5075 = 0.0974 AU; the two ovals add up to 0.192 AU." markdown>
**Your turn.** Star 2's oval, in AU:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(a_2 = 0.192 \times 0.5075 = 0.0974\) AU. Check: \(0.0945 + 0.0974 = 0.192\) AU, the distance between them. The balance point sits almost exactly halfway, a hair closer to the heavier star.

The rule: **each star's oval is the distance apart times the other star's share of the mass**.

</details>
</div>

## Back to the plot: why the eclipses differ

The plot is drawn from Kepler's laws, with the paper's period, stretch and masses, and with one number we read from our own light: which way the stretched orbit points. Lesson 4.1's timing gave half the answer; the eclipses' lengths gave the rest. In the folded TESS light the primary eclipse lasts 2.7 hours at half depth and the secondary 7.3 hours. A long eclipse means the stars are crossing slowly, so far apart. That fixes the direction: the primary eclipse happens near periastron, the secondary near apastron.

Touch the plot at day 0: the stars are only 0.108 AU apart during the primary eclipse, sweeping past each other at about 170 km/s. At day 11.88, the secondary eclipse, they are 0.266 AU apart and much slower. Closer stars also line up differently from where we stand, so at the primary eclipse one passes more squarely across the other: that is why the primary is deeper (lesson 4.1).

The average relative speed is \(2\pi a / P\): \(2\pi \times 0.192\) AU in 19.66 days, about 106 km/s. At periastron it reaches about 172 km/s, at apastron it falls to about 66 km/s. Each star carries about half of that. A spectrograph (lesson 3.4) would see each star's lines swing by tens of kilometres per second: about a thousand times 51 Pegasi's wobble.

## Why this matters for Second Sun

A planet around this pair circles both stars at about 0.9 AU (lesson 2.1's planet orbit), while the two stars underneath it swing around their balance point on 0.09 AU ovals every 19.66 days. When the planet crosses in front, each star is somewhere different on its oval each time, moving in a different direction. So the planet's dips do not come at a steady beat like a planet around one star: their timing and their length wander. Lesson 4.4 is about exactly that, and it is why our search looks for single dips instead of a repeating period.

## In a few sentences

Two stars orbit their shared centre of mass; each traces an oval whose size is the stars' distance apart times the other star's share of the mass, so this near-equal pair swings on ovals of 0.0945 and 0.0974 AU. By Kepler's second law they move fastest when closest: distance times speed is equal at the nearest and farthest points, so 0.106 AU and 0.278 AU mean a 2.62 times change in speed. The primary eclipse happens near the nearest point (short, 2.7 hours), the secondary near the farthest (long, 7.3 hours).

## Problems

<div class="tw-prob" data-answer="0.278|0.28" data-tol="0.02" data-unit="AU" data-why="The highest point of the plot is 0.278 AU, near day 9.4." markdown>
**1.** Touch the plot. How far apart are the stars at their farthest, in AU?

<details class="tw-sol" markdown><summary>Worked solution</summary>

**0.278 AU**, near day 9.4 of the orbit. The nearest, 0.106 AU, comes just before the primary eclipse.

</details>
</div>

<div class="tw-prob" data-answer="0.106|0.11" data-tol="0.03" data-unit="AU" data-hints='{"0.0864":"That is 0.192 times (1 - 0.55). The stretch is 0.448: use 1 - 0.448."}' data-why="a (1 - e) = 0.192 x (1 - 0.448) = 0.106 AU." markdown>
**2.** For a stretched orbit the nearest distance is \(a(1 - e)\). With \(a = 0.192\) AU and \(e = 0.448\), what is it, in AU? Does it match the plot?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(0.192 \times (1 - 0.448) = 0.192 \times 0.552 = 0.106\) AU, the bottom of the plot. The farthest is \(a(1 + e) = 0.192 \times 1.448 = 0.278\) AU, the top.

</details>
</div>

<div class="tw-prob" data-answer="66|65.6|65" data-tol="0.04" data-unit="km/s" data-hints='{"450":"Multiply by the ratio the other way: far means slow. 172 divided by 2.62."}' data-why="v_far = v_near x r_near / r_far = 172 x 0.106 / 0.278 = 65.6 km/s." markdown>
**3.** At periastron the stars move at 172 km/s relative to each other. Using distance times speed, how fast do they move at apastron, in km/s?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(v_{\text{far}} = 172 \times 0.106 / 0.278 = 65.6\) km/s.

</details>
</div>

<div class="tw-prob" data-answer="secondary|the secondary" data-hints='{"primary":"The primary is the short one: 2.7 hours. The stars are close and fast then."}' data-why="The secondary eclipse happens near apastron, where the stars are far apart and slow, so it lasts longer (7.3 hours against 2.7)." markdown>
**4.** Which eclipse lasts longer, the primary or the secondary?

<details class="tw-sol" markdown><summary>Worked solution</summary>

The **secondary**: 7.3 hours at half depth against 2.7. It happens near apastron, where the stars cross each other slowly.

</details>
</div>

<div class="tw-prob" data-answer="0.5|0.50|half" data-tol="0.03" data-hints='{"1":"That would put the whole oval on one star. With equal masses the shares are equal."}' data-why="With equal masses each share is M / (M + M) = 1/2." markdown>
**5.** If the two stars had exactly equal masses, what share of the distance apart would each star's oval be?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(M / (M + M) = 0.5\): half each. The balance point sits exactly in the middle, and the two stars trace identical ovals on opposite sides of it.

</details>
</div>

## Sources

- Period 19.658173 d, eccentricity 0.4479, masses 1.2384 and 1.2019 Suns: Kostov et al. 2021, AJ 162, 234 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614), Tables 5 and 6, read 23 Nov 2026).
- The orbit's direction, omega = 70.6 degrees, is our own estimate, not the paper's: e cos(omega) = 0.149 from the eclipse timing (lesson 4.1) and the sign from the eclipse lengths (2.74 and 7.27 hours at half depth in TESS sectors 44 to 47 folded), `book/tools/lesson_plots_u4b.py` (23 Nov 2026). The script stops if the semi-major axis from Kepler's third law (0.1919 AU) differs from lesson 2.1's 0.192 AU or if the two eclipse lengths are too similar to tell.
- Kepler's second law, centre of mass and two-body orbits: OpenStax Astronomy 2e, chapter 3 "Orbits and Gravity" ([the book](https://openstax.org/details/books/astronomy-2e), CC BY-NC-SA 4.0), in our own words.
