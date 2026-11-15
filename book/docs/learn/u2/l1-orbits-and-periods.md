---
hide: [navigation, toc, footer]
title: "2.1 Orbits and periods"
---

# Orbits and periods

Same two stars, now watched for four TESS sectors in a row: about 106 days.

<div class="tw-plot" data-src="u2-four-sectors"></div>

<p class="tw-plot__ask">Count the deep drops. Some reach about minus 43%, some only about minus 35%. Do the two kinds take turns?</p>

## A clock in the sky

The drops come back again and again, and they come in two kinds. The deeper ones (about 45% at their 2-minute bottom) happen when one star passes in front of the other; the shallower ones (about 36%) when it is the other way round. Astronomers call the deeper kind the **primary eclipse** and the shallower kind the **secondary eclipse**.

<aside class="tw-mn" markdown>
**Primary and secondary eclipse.** The deeper and the shallower of the two eclipses that a pair of stars makes in each orbit.
</aside>

The time from one primary eclipse to the next is the time the stars take to go once round each other: the **period**, written \(P\). Every orbit, the same lineup repeats, so a period is the most exact clock a star pair can give you.

<aside class="tw-mn" markdown>
**Period (\(P\)).** The time for one full orbit. Here, the time from one primary eclipse to the next.
</aside>

Look closely and you will notice that not every orbit shows both eclipses. Our script finds the middles of five primary eclipses, at days 2507.395, 2527.053, 2546.710, 2586.028 and 2605.685 on the TESS clock. The one that should come between 2546.710 and 2586.028, near day 2566.4, fell in a gap in the data (a 2.8-day pause while TESS sent its data home). One secondary eclipse is lost the same way. Gaps like these are why a single planet crossing can be missed even when the telescope is looking at the right star.

!!! example "Worked example: measuring the period"
    **Step 1. Take the first and the last primary eclipse.** Days 2507.395 and 2605.685.

    **Step 2. Subtract.** \(2605.685 - 2507.395 = 98.290\) days.

    **Step 3. Count the orbits in between.** The gaps between neighbours are about 19.7, 19.7, 39.3 and 19.7 days. The 39.3 is two orbits (the missing eclipse), so the total is \(1 + 1 + 2 + 1 = 5\) orbits.

    **Step 4. Divide.** \(P = 98.290 / 5 = 19.658\) days.

    Why not just subtract two neighbours? Each eclipse time has a small error. Spreading that error over five orbits makes the period five times more exact. The discovery paper gives 19.7 days, the same value rounded.

## How far apart are the stars? Kepler's third law

About 400 years ago Johannes Kepler found a rule linking how long an orbit takes to how big it is. In the form astronomers use for stars:

\[ P^2 = \frac{a^3}{M} \]

<aside class="tw-mn" markdown>
**Kepler's third law.** In these units: period in years, size in astronomical units, mass in Suns. It works for planets around the Sun, for two stars, and for a planet around two stars.
</aside>

Here \(P\) is the period in years, \(M\) is the total mass of everything inside the orbit in Suns, and \(a\) is the size of the orbit in **astronomical units** (AU): 1 AU is the distance from the Earth to the Sun, about 150 million km. For an oval orbit, \(a\) is half of its long axis, the average of the closest and the farthest distance.

<aside class="tw-mn" markdown>
**Astronomical unit (AU).** The Earth's average distance from the Sun, about 150 million km. A ruler for orbits.
</aside>

Check it on the Earth: \(P = 1\) year and \(M = 1\) Sun, so \(a^3 = 1\) and \(a = 1\) AU. Right.

We want \(a\), so we turn the law around: multiply both sides by \(M\) and take the **cube root**, the number that multiplied by itself three times gives what is under the root (the cube root of 8 is 2, because \(2 \times 2 \times 2 = 8\)):

\[ a = \sqrt[3]{M P^2} \]

!!! example "Worked example: the two stars of TIC 172900988"
    The discovery paper gives the stars' masses: 1.238 and 1.202 Suns, so \(M = 2.440\).

    **Step 1. Period in years.** \(19.658 / 365.25 = 0.05382\) years.

    **Step 2. Square it.** \(0.05382^2 = 0.002897\).

    **Step 3. Times the mass.** \(2.440 \times 0.002897 = 0.007069\).

    **Step 4. Cube root.** \(\sqrt[3]{0.007069} = 0.192\) AU.

    The two stars sit about 0.19 AU apart: half of Mercury's distance from the Sun. That is about 41 times the width of the Sun, while each star is only about 1.4 times as wide as the Sun. Close, but far from touching.

!!! question "Your turn, half done: the planet's orbit"
    The planet goes round both stars once in about 200 days (the paper allows six values between 189 and 204). It feels the pull of both stars together, so \(M = 2.440\) again. Step 1: \(200 / 365.25 = 0.5476\) years. Step 2: \(0.5476^2 = 0.2998\). Finish steps 3 and 4.

<div class="tw-prob" data-answer="0.90" data-tol="0.02" data-unit="AU" data-hints='{"0.73":"That is a cubed. Take the cube root as the last step.","0.67":"Did you leave out the mass? Multiply by 2.440 first."}' data-why="2.440 times 0.2998 = 0.7316, and its cube root is 0.90 AU." markdown>
**Your turn.** The size of the planet's orbit, in AU:

<details class="tw-sol" markdown><summary>Worked solution</summary>

Step 3: \(2.440 \times 0.2998 = 0.7316\). Step 4: \(\sqrt[3]{0.7316} = 0.90\) AU.

The rule: **\(a = \sqrt[3]{M P^2}\), with \(P\) in years and \(M\) the total mass inside the orbit.** The planet circles both stars at about 0.9 AU, almost five times farther out than the stars are from each other. That is no accident: Unit 3 shows why a planet cannot orbit two suns too closely.

</details>
</div>

## In a few sentences

A pair of stars makes two eclipses each orbit, a deeper primary and a shallower secondary; the time between two primaries is the period. Measure it across many orbits to make it exact; gaps in the data can hide whole eclipses. Kepler's third law, \(P^2 = a^3 / M\), turns a period and a mass into the size of an orbit.

## Problems

<div class="tw-prob" data-answer="20" data-tol="0.005" data-unit="days" data-hints='{"60":"That is the time for all three orbits. Divide by the number of orbits.","15":"From the first to the fourth eclipse is 3 orbits, not 4."}' data-why="From the 1st to the 4th eclipse is 3 orbits: 60 / 3 = 20 days." markdown>
**1.** A star pair's first primary eclipse is at day 100.0 and its fourth at day 160.0, with none missing between. What is the period?

<details class="tw-sol" markdown><summary>Worked solution</summary>

From the first to the fourth eclipse there are 3 orbits (1 to 2, 2 to 3, 3 to 4). \(160.0 - 100.0 = 60.0\) days, and \(60.0 / 3 = 20.0\) days.

</details>
</div>

<div class="tw-prob" data-answer="2625.343" data-abs="0.01" data-hints='{"2615.514":"That is half a period later: the secondary eclipse would come around then, not the next primary (and for this oval orbit, not even exactly halfway)."}' data-why="2605.685 + 19.658 = 2625.343." markdown>
**2.** The last primary eclipse in the plot is at day 2605.685 and the period is 19.658 days. When is the next primary eclipse, on the TESS clock?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(2605.685 + 19.658 = 2625.343\). Predicting eclipses like this is how astronomers plan observations, and how our search masks eclipses out of the light before looking for planets.

</details>
</div>

<div class="tw-prob" data-answer="8" data-tol="0.01" data-unit="years" data-hints='{"64":"64 is P squared. Take the square root.","4":"Square root of 64, not of 16."}' data-why="P squared = 4 cubed / 1 = 64, so P = 8 years." markdown>
**3.** A planet orbits a star of 1 Sun mass at 4 AU. How long is its year?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(P^2 = a^3 / M = 4^3 / 1 = 64\), so \(P = \sqrt{64} = 8\) years. (Jupiter, at 5.2 AU, takes about 12 years.)

</details>
</div>

<div class="tw-prob" data-answer="0.70" data-tol="0.02" data-unit="AU" data-hints='{"0.35":"That is a cubed. Take the cube root.","0.63":"That is the period in years. Square it, multiply by the mass, then take the cube root."}' data-why="P = 229 / 365.25 = 0.627 years; P squared = 0.393; times 0.89 = 0.350; cube root 0.70 AU." markdown>
**4.** Kepler-16 b, the first planet found crossing two suns, orbits stars of 0.69 and 0.20 Sun masses every 229 days. How big is its orbit, in AU?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(M = 0.69 + 0.20 = 0.89\). \(P = 229 / 365.25 = 0.627\) years, \(P^2 = 0.393\). \(M P^2 = 0.89 \times 0.393 = 0.350\). Cube root: \(a = 0.70\) AU, about the distance of Venus from the Sun.

</details>
</div>

<div class="tw-prob" data-answer="2.83" data-tol="0.02" data-hints='{"8":"The period changes with the square root of the mass, not the mass itself.","64":"Inverted: more mass makes the orbit faster, so the period is shorter."}' data-why="P squared = a cubed / M; with a fixed, 8 times the mass gives 1/8 of P squared, so P is the square root of 8 = 2.83 times shorter." markdown>
**5.** Two orbits have the same size \(a\), but one goes round 8 times more mass. How many times shorter is its period?

<details class="tw-sol" markdown><summary>Worked solution</summary>

With \(a\) fixed, \(P^2\) is proportional to \(1 / M\). Eight times the mass makes \(P^2\) eight times smaller, so \(P\) is \(\sqrt{8} = 2.83\) times smaller. More mass pulls harder, so the same orbit is travelled faster.

</details>
</div>

## Sources

- Eclipse times and the period: TESS sectors 44 to 47, 2-minute light curves of TIC 172900988 (MAST); middles of the eclipses (halfway through the time below 90% of normal) and the fitted period 19.658 days measured by our scripts on 15 Nov 2026 (`book/tools/lesson_plots.py` and a check script). Both missing eclipses (days 2566.4 and 2538.9) fall in mid-sector data gaps.
- Masses, period and planet periods: Kostov et al. 2021 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614)): "P = 19.7 days", M1 = 1.2384 and M2 = 1.2019 solar masses, planet period "188.8, 190.4, 194.0, 199.0, 200.4, or 204.1 days".
- Kepler-16: Doyle et al. 2011 ([arXiv 1109.3432](https://arxiv.org/abs/1109.3432)): stars "20% and 69% as massive as the sun", planet on "a nearly circular 229-day orbit".
