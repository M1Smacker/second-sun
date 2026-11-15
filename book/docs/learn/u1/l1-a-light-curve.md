---
hide: [navigation, toc, footer]
title: "1.1 A light curve"
---

# A light curve

Before any idea, look at the real thing. Below is one star's light, measured by a space telescope for 24 days. Move your finger or mouse along it.

<div class="tw-plot" data-src="u1-sector"></div>

<p class="tw-plot__ask">Find the two deep drops. On which days do they happen, and does one go deeper than the other?</p>

## What you are looking at

This picture is called a **light curve**. It is the simplest thing an astronomer can make from a telescope that stares at one star: how bright the star looked, point after point, as time went on. Time runs from left to right. Brightness runs up and down.

<aside class="tw-mn" markdown>
**Light curve.** Brightness against time for one star. Everything in this project starts from one.
</aside>

The telescope is TESS, a NASA satellite launched in 2018 that watches large patches of sky for about four weeks at a time. One of those four-week stretches is called a **sector**. This plot is sector 44, taken in October and November 2021.

<aside class="tw-mn" markdown>
**Sector.** One stretch of about 27 days when TESS points at the same patch of sky. This one has 24 days of good data because of a gap in the middle, when the data are sent down to Earth.
</aside>

The star is called TIC 172900988. That long number is its entry in the TESS Input Catalog, the telescope's list of stars. You cannot see it with your eyes, but a small telescope would find it easily. And it is not one star. It is two stars, so close together that TESS sees them as one point of light. They circle each other every 19.7 days. Once per orbit, one star passes in front of the other, and from here we see less light. That is what the deep drops are: **eclipses**.

<aside class="tw-mn" markdown>
**Eclipse.** One object passing in front of another and blocking part of its light.
</aside>

There is a third thing in this system, too: a planet as big as Jupiter that circles both stars. Astronomers found it in 2021 from this same kind of light curve. It does not cross the stars in this sector, so you will not see it here. We will come back to it.

## From counts to a percentage

TESS does not measure "brightness" directly. Its camera counts the light that lands in a few pixels around the star, every 2 minutes. For this star the usual count is about 22,437 units each second. That number on its own means little: a brighter star gives a bigger number, a fainter one a smaller number.

So the first thing anyone does with a light curve is to compare every point with the star's normal light. We call a point's light \(F\) and the star's normal light \(F_{\text{normal}}\). Their ratio, \(F / F_{\text{normal}}\), is 1 when the star looks normal and less than 1 when something blocks it. Subtract 1 and multiply by 100, and you have the change in percent:

\[ \text{change (\%)} = \left( \frac{F}{F_{\text{normal}}} - 1 \right) \times 100 \]

<aside class="tw-mn" markdown>
**Normal light.** In practice, the middle value (the median) of all points. A few odd points cannot pull it around.
</aside>

That is the scale on the plot: 0 means normal, minus 10 means 10% fainter than normal.

!!! example "Worked example: how deep is the first eclipse?"
    At the bottom of the first drop, TESS counted about 12,316 units each second. Normal is 22,437.

    **Step 1. The ratio.** \(F / F_{\text{normal}} = 12{,}316 / 22{,}437 = 0.549\). The star pair gave 0.549 of its normal light.

    **Step 2. Subtract 1.** \(0.549 - 1 = -0.451\). The minus sign says "fainter".

    **Step 3. Times 100.** \(-0.451 \times 100 = -45.1\%\).

    So at the deepest moment, almost half of the pair's light was hidden. That is a lot: the two stars are nearly the same size, so one can cover most of the other.

!!! question "Your turn, half done: the second eclipse"
    At the bottom of the second drop the ratio \(F / F_{\text{normal}}\) is 0.642. Step 1 is done for you: the ratio is 0.642. Do steps 2 and 3, then type the change in percent.

<div class="tw-prob" data-answer="-35.8" data-abs="0.15" data-unit="percent" data-hints='{"35.8":"Right size, but the star got fainter: the change is negative.","-0.358":"That is the change as a fraction. Multiply by 100."}' data-why="(0.642 minus 1) times 100 = minus 35.8%." markdown>
**Your turn.** The change in percent at the bottom of the second eclipse:

<details class="tw-sol" markdown><summary>Worked solution</summary>

Step 2: \(0.642 - 1 = -0.358\). Step 3: \(-0.358 \times 100 = -35.8\%\).

The rule behind it: **compare with normal, then turn the difference into percent.** The answer is negative because light was blocked. This eclipse is shallower than the first (36% against 45%). Why the two differ is a question for Unit 3: it depends on which star is hidden and how squarely the two line up.

</details>
</div>

## One eclipse up close

Zoom into the first drop. Here each point is 10 minutes of light, averaged.

<div class="tw-plot" data-src="u1-eclipse"></div>

<p class="tw-plot__ask">Touch the plot where the light first starts to fall, then where it is back to normal. How many hours did the eclipse last?</p>

The shape tells a story. The light does not switch off and on. It slides down as one star moves across the other, reaches a bottom, and slides back up. The shape of that slide holds the sizes of the two stars and the angle we see the orbit from. Later units take that apart, piece by piece.

## In a few sentences

A light curve is a star's brightness against time. We divide every point by the star's normal light so that 1 (or 0%) means normal and anything lower means something blocked some light. This pair of stars blocks up to 45% of its own light once per orbit; a planet blocks far, far less, which is why the next lessons are about small numbers and about noise.

## Problems

<div class="tw-prob" data-answer="-1" data-abs="0.05" data-unit="percent" data-hints='{"1":"The star got fainter, so the change is negative.","-0.01":"That is the change as a fraction. Multiply by 100 for percent."}' data-why="19,800 / 20,000 = 0.99, and (0.99 minus 1) times 100 = minus 1%." markdown>
**1.** A star normally gives 20,000 units of light each second. During a dip it gives 19,800. What is the change in percent?

<details class="tw-sol" markdown><summary>Worked solution</summary>

Ratio: \(19{,}800 / 20{,}000 = 0.99\). Subtract 1: \(-0.01\). Times 100: \(-1\%\). The star was 1% fainter than normal.

</details>
</div>

<div class="tw-prob" data-answer="-3" data-abs="0.05" data-unit="percent" data-hints='{"3":"Fainter means negative.","97":"97% is how much light is left. The change is how much is missing."}' data-why="(0.97 minus 1) times 100 = minus 3%." markdown>
**2.** A point on a light curve has \(F / F_{\text{normal}} = 0.97\). What is the change in percent?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\((0.97 - 1) \times 100 = -0.03 \times 100 = -3\%\).

</details>
</div>

<div class="tw-prob" data-answer="720" data-abs="0" data-hints='{"30":"That is points per hour. A day has 24 hours.","1440":"1,440 is the number of minutes in a day. TESS takes one point every 2 minutes."}' data-why="A day has 24 times 60 = 1,440 minutes, and 1,440 / 2 = 720." markdown>
**3.** TESS takes one measurement of this star every 2 minutes. How many measurements is that in one full day?

<details class="tw-sol" markdown><summary>Worked solution</summary>

A day has \(24 \times 60 = 1{,}440\) minutes. One point every 2 minutes gives \(1{,}440 / 2 = 720\) points.

(This sector has 15,243 good points over 24 days, a little fewer than \(24 \times 720 = 17{,}280\), because some points are flagged as bad and removed.)

</details>
</div>

<div class="tw-prob" data-answer="11.87" data-abs="0.03" data-unit="days" data-hints='{"9.85":"Half of 19.7 days would be 9.85. The real gap is different: read it from the times given."}' data-why="2519.27 minus 2507.40 = 11.87 days." markdown>
**4.** On the TESS clock, the bottoms of the two eclipses are at day 2507.40 and day 2519.27. How many days apart are they?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(2519.27 - 2507.40 = 11.87\) days.

Here is a puzzle to keep: the stars take 19.7 days to go round, so you might expect the two eclipses to be half of that, 9.85 days, apart. They are not. The orbit is not a circle but a stretched oval, so one half of it is travelled faster than the other. Unit 3 shows how astronomers read that from this one gap.

</details>
</div>

<div class="tw-prob" data-answer="dip|eclipse|drop" data-why="A planet passing in front of a star blocks a little light, so the light curve dips." markdown>
**5.** In one word: what shape would a planet crossing in front of a star make in a light curve?

<details class="tw-sol" markdown><summary>Worked solution</summary>

A **dip**: the light falls a little, stays low while the planet crosses, and comes back. It is the same idea as the eclipse above, only much smaller, because a planet is far smaller than a star.

</details>
</div>

## Sources

- The light: TESS sector 44, 2-minute light curve of TIC 172900988 (SPOC pipeline, PDCSAP flux, bad points removed), from the MAST archive. Numbers measured by our own script, `book/tools/lesson_plots.py`.
- The system: Kostov et al. 2021, "TIC 172900988: A Transiting Circumbinary Planet Detected in One Sector of TESS Data" ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614)): binary period 19.7 days, eccentricity 0.45, planet radius about 1.0 Jupiter radius.
- TESS cadence: Ricker et al. 2014 ([arXiv 1406.0151](https://arxiv.org/abs/1406.0151)).
