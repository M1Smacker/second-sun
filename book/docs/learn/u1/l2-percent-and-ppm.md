---
hide: [navigation, toc, footer]
title: "1.2 Percent and parts per million"
---

# Percent and parts per million

In the last lesson one star hid 45% of the other's light. Planets are far gentler. Here is the same pair of stars again, at the scale you will need for planets.

<div class="tw-plot" data-src="u1-quiet-day"></div>

<p class="tw-plot__ask">The points wander between about minus 0.3% and plus 0.3%. Read off a few. How big a dip could hide inside that spread?</p>

## Small numbers need a better unit

A planet blocks only the piece of the star that the planet's disc covers. If a planet's radius is \(R_p\) and the star's radius is \(R_\star\), the fraction of light blocked is the ratio of the two discs' areas. A disc's area is \(\pi R^2\), and the \(\pi\) cancels:

\[ \text{depth} = \frac{\pi R_p^2}{\pi R_\star^2} = \left( \frac{R_p}{R_\star} \right)^2 \]

<aside class="tw-mn" markdown>
**Transit depth.** How much light a planet blocks while it crosses its star, as a fraction of the star's light. The planet must also be in front of the bright disc, not off its edge.
</aside>

<aside class="tw-mn" markdown>
**Why squared?** Area grows with the square of the radius. A planet twice as wide blocks four times the light.
</aside>

That formula is the most important one in this book. It is simple on purpose: it assumes the star is equally bright all over its face, which is not quite true. Real stars are a little darker near their edges, so real dips are slightly rounded. For now the simple form is all we need.

Try it on the Earth crossing the Sun. The Sun is 109 times wider than the Earth, so \(R_p / R_\star = 1/109.08 = 0.00917\). Squared, that is 0.0000840. As a percentage, 0.0084%. Numbers like that are awkward to read, write and compare. So astronomers use a smaller unit: **parts per million**, written ppm.

<aside class="tw-mn" markdown>
**ppm.** Parts per million. 1 ppm is one millionth of the star's light. 1% is 10,000 ppm.
</aside>

\[ \text{ppm} = \text{fraction} \times 1{,}000{,}000 \qquad \text{percent} = \text{fraction} \times 100 \]

So \(1\% = 10{,}000\) ppm, and the Earth's dip across the Sun is \(0.0000840 \times 1{,}000{,}000 = 84\) ppm. That is the size of signal that the hardest planet searches chase.

!!! example "Worked example: the planet in our system"
    The planet around TIC 172900988 is 11.25 times wider than the Earth. The larger star is 1.38 times wider than the Sun. How deep would the dip be if the planet crossed that star, and the second star were not there?

    **Step 1. Same units.** The Sun is 109.08 Earths wide, so the planet is \(11.25 / 109.08 = 0.1031\) Sun widths.

    **Step 2. The ratio.** \(R_p / R_\star = 0.1031 / 1.3827 = 0.0746\).

    **Step 3. Square it.** \(0.0746^2 = 0.00556\).

    **Step 4. Into ppm.** \(0.00556 \times 1{,}000{,}000 = 5{,}560\) ppm, which is 0.56%.

    In the real system the second star adds its light too, so the planet's dip is diluted: it shows up at roughly half that depth. Unit 3 explains dilution properly. Either way, compare it with the eclipse: 0.56% against 45%. The planet's dip is about 80 times smaller.

!!! question "Your turn, half done: Jupiter across the Sun"
    Jupiter is 11.21 Earths wide; the Sun is 109.08. Step 1: \(11.21 / 109.08 = 0.1028\). Steps 2 and 3 are yours: square the ratio and turn it into ppm.

<div class="tw-prob" data-answer="10570" data-tol="0.01" data-unit="ppm" data-hints='{"1.06":"That is percent. Multiply the fraction by 1,000,000 for ppm.","0.0106":"That is the fraction. Multiply by 1,000,000 for ppm.","102800":"You forgot to square the ratio."}' data-why="0.1028 squared = 0.01057, times 1,000,000 = 10,570 ppm, about 1%." markdown>
**Your turn.** Jupiter's dip across the Sun, in ppm:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(0.1028^2 = 0.01057\). Times 1,000,000: about \(10{,}570\) ppm, or 1.06%.

The rule: **depth is the radius ratio squared.** That is why Jupiter's dip (about 1%) is over 100 times deeper than the Earth's (84 ppm), even though Jupiter is only 11 times wider.

</details>
</div>

## Reading a light curve in ppm

The same conversion works on any point of a light curve. If a point sits at \(F / F_{\text{normal}} = 0.9988\), it is \(1 - 0.9988 = 0.0012\) below normal: 0.12%, or 1,200 ppm.

Now look again at the quiet day at the top of this lesson. Nothing is crossing either star, yet the points scatter by a few thousand ppm. A dip from an Earth-sized planet (under 100 ppm around a star this size) would be invisible in any single point. Finding planets is the art of seeing small dips through that scatter. That is the next lesson.

## In a few sentences

A planet blocks the fraction \((R_p / R_\star)^2\) of its star's light. For planets that fraction is tiny, so we write it in parts per million: 1% is 10,000 ppm. Jupiter across the Sun is about 10,600 ppm, the Earth only 84 ppm.

## Problems

<div class="tw-prob" data-answer="2500" data-tol="0.005" data-unit="ppm" data-hints='{"25":"Percent is per hundred. To go to per million, multiply by 10,000.","250":"Check the factor: 1% is 10,000 ppm."}' data-why="0.25 times 10,000 = 2,500 ppm." markdown>
**1.** A dip is 0.25% deep. How deep is it in ppm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(1\% = 10{,}000\) ppm, so \(0.25\% = 0.25 \times 10{,}000 = 2{,}500\) ppm.

</details>
</div>

<div class="tw-prob" data-answer="0.03" data-tol="0.01" data-unit="percent" data-hints='{"3":"Divide by 10,000, not by 100.","0.0003":"That is the fraction. Multiply by 100 for percent."}' data-why="300 / 10,000 = 0.03%." markdown>
**2.** A dip is 300 ppm deep. How deep is it in percent?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(300 / 10{,}000 = 0.03\%\).

</details>
</div>

<div class="tw-prob" data-answer="1200" data-tol="0.005" data-unit="ppm" data-hints='{"9988":"That is how much light is left. How much is missing?","0.12":"That is percent. Convert to ppm."}' data-why="1 minus 0.9988 = 0.0012, times 1,000,000 = 1,200 ppm." markdown>
**3.** A point on a light curve has \(F / F_{\text{normal}} = 0.9988\). How far below normal is it, in ppm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(1 - 0.9988 = 0.0012\). Times 1,000,000: 1,200 ppm.

</details>
</div>

<div class="tw-prob" data-answer="10000" data-tol="0.005" data-unit="ppm" data-hints='{"100000":"Remember to square: 0.1 squared is 0.01.","1":"That is percent. Convert to ppm."}' data-why="0.1 squared = 0.01 = 10,000 ppm." markdown>
**4.** A planet is one tenth as wide as its star. How deep is its dip, in ppm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\((R_p / R_\star)^2 = 0.1^2 = 0.01\), and \(0.01 \times 1{,}000{,}000 = 10{,}000\) ppm (1%).

</details>
</div>

<div class="tw-prob" data-answer="336" data-tol="0.02" data-unit="ppm" data-hints='{"84":"84 ppm is for a star as wide as the Sun. This star is half as wide.","168":"Halving the star doubles the ratio, and squaring makes that four times the depth."}' data-why="The ratio doubles to 0.01834; squared, 0.000336 = 336 ppm, four times the Earth-Sun dip." markdown>
**5.** An Earth-sized planet crosses a star half as wide as the Sun. How deep is the dip, in ppm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

The star is \(0.5 \times 109.08 = 54.54\) Earths wide, so \(R_p / R_\star = 1 / 54.54 = 0.01834\). Squared: \(0.000336\), which is 336 ppm.

Shortcut: halving the star doubles the ratio, and squaring turns "twice" into "four times": \(4 \times 84 = 336\) ppm. This is why small planets are easiest to find around small stars.

</details>
</div>

## Sources

- Depth as the radius ratio squared: Winn 2010, "Transits and Occultations" ([arXiv 1001.2010](https://arxiv.org/abs/1001.2010)), which also explains the darker star edges (limb darkening) left out here.
- Planet and star sizes: Kostov et al. 2021 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614)): planet 11.25 Earth radii, larger star 1.3827 Sun radii.
- The Sun is 109.08 Earth radii wide (IAU nominal values); Jupiter's equator is 11.21 Earth radii (71,492 km against 6,378 km).
- The plotted day: TESS sector 44, our script `book/tools/lesson_plots.py`.
