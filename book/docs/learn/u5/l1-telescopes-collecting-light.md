---
hide: [toc, footer]
title: "5.1 Telescopes: collecting light"
---

# Telescopes: collecting light

A telescope is a bucket for light. The bigger the opening, the more light it catches each second, and the more light it catches, the smaller the flicker in its measurements. This plot shows that flicker for our two-sun star, measured in TESS's own data.

<div class="tw-plot" data-src="u5-scatter"></div>

<p class="tw-plot__ask">Averaging the 2-minute measurements over longer blocks makes the spread shrink, fast at first, then more slowly. Before reading on, guess: averaging 4 times as long, by how much does the spread shrink?</p>

## TESS's buckets

Each of TESS's four cameras has an opening, the **entrance pupil**, 10.5 cm across: about the size of a large camera lens, far smaller than a big observatory telescope. Behind it, seven lenses focus the light onto four detectors of 2,048 by 2,048 pixels each, kept at minus 75 degrees Celsius so their own heat does not add noise.

<aside class="tw-mn" markdown>
**Collecting area.** The area of a telescope's opening: \(\pi r^2\). It sets how much light is caught per second. Double the diameter and the area, and the light, grow four times.
</aside>

From our star, TESS's camera collects 21,213 electrons per second in its 20 aperture pixels (lesson 5.3): each electron is one captured particle of light. In one 2-minute measurement that is \(21{,}213 \times 120 = 2.55\) million.

## Why counting gives noise

Light arrives as separate particles, at random moments, like raindrops on a roof. Count them for 2 minutes and the count wobbles from one 2 minutes to the next even if the star is perfectly steady. The size of the wobble is the square root of the count:

\[ \text{photon noise} = \frac{\sqrt{N}}{N} = \frac{1}{\sqrt{N}} \]

<aside class="tw-mn" markdown>
**Photon noise.** The unavoidable random spread in a count of light particles: \(\sqrt{N}\) for a count of \(N\). As a share of the count it is \(1/\sqrt{N}\), so more light means a smaller share.
</aside>

For 2.55 million electrons: \(1/\sqrt{2{,}550{,}000} = 0.000627\), or 627 ppm. That is the best any measurement of this star every 2 minutes could do with TESS's bucket.

## Think it through

<div class="tw-prob" data-answer="86.6|87|86.59" data-tol="0.02" data-hints='{"330":"That used the diameter, 10.5 cm, as the radius. The radius is half: 5.25 cm.","16.5":"That is the circumference formula. The area is pi times r squared."}' data-why="pi x 5.25^2 = 3.1416 x 27.56 = 86.6 square cm." markdown>
**a.** TESS's opening is 10.5 cm across. What is its collecting area, \(\pi r^2\), in square centimetres? (Just the number.)
</div>

!!! example "Worked example: averaging an hour"
    One 2-minute measurement has photon noise 627 ppm. An hour holds 30 of them.

    **Step 1. The count grows 30 times.** \(30 \times 2.55\) million electrons.

    **Step 2. The noise shrinks by the square root of 30.** \(\sqrt{30} = 5.48\).

    **Step 3.** \(627 / 5.48 = 114\) ppm: the best an hour's average could be.

!!! question "Your turn, half done: what we actually get"
    After dividing out the star's own slow changes (it drifts by about 0.1%), our measured 1-hour spread is 159 ppm. Step 1: the photon limit is 114 ppm. Finish: how many times the photon limit is the real spread?

<div class="tw-prob" data-answer="1.39|1.4" data-tol="0.03" data-hints='{"0.72":"Upside down: measured divided by the limit, 159 / 114."}' data-why="159 / 114 = 1.39: the real spread is 1.4 times the photon limit." markdown>
**Your turn.** Measured spread / photon limit:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(159 / 114 = 1.39\). The extra comes from other noise sources; the usual suspects are the sky background's own photons (lesson 5.3 subtracted its level, not its wobble), the detector and the spacecraft's small pointing jitter. We have not split them. On the plot the ratio stays near 1.4 from 2 minutes to 2 hours: the spread shrinks exactly as photon noise does, just 1.4 times larger. (Beyond about 2 hours too few blocks fit in one sector to measure the spread well.)

The rule: **noise shrinks as the square root of the light collected; average 4 times longer, and it halves**.

</details>
</div>

## Why this matters for Second Sun

A planet's dip around our star might be 3,000 ppm (lesson 4.4): easy against 159 ppm in an hour. But a planet the size of Earth around a Sun-like star dims it by about 84 ppm, below one hour's noise even for this bright star, and fainter stars collect fewer photons, so their noise is larger. That is why our search adds up many hours of a dip, why bright stars are worth more to us, and why the noise our searches see, 1.6 to 3 times the photon limit for most of our stars (our 22 Nov measurement), is one of the two things that limit how many planets Petrova can find.

## In a few sentences

A telescope collects light in proportion to the area of its opening; TESS's cameras are 10.5 cm across. Light comes as separate particles, so a count of \(N\) wobbles by \(\sqrt{N}\): our star gives 2.55 million electrons per 2 minutes, a photon limit of 627 ppm, and averaging over an hour brings it to 114 ppm. TESS's real spread for this star is about 1.4 times that limit from 2 minutes to 2 hours: 159 ppm in an hour.

## Problems

<div class="tw-prob" data-answer="4" data-tol="0.01" data-hints='{"2":"The area goes as the diameter squared: 2 x 2."}' data-why="Area goes as diameter squared: 2^2 = 4 times the light." markdown>
**1.** A camera with an opening twice as wide as TESS's would collect how many times as much light?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(2^2 = 4\) times. Its photon noise would be half TESS's, since \(1/\sqrt{4} = 1/2\).

</details>
</div>

<div class="tw-prob" data-answer="2" data-tol="0.01" data-hints='{"4":"That is how much more light. The noise shrinks by the square root of that."}' data-why="Averaging 4 times as long collects 4 times the light; the noise shrinks by the square root, 2." markdown>
**2.** Averaging 4 times as long, by what factor does the photon noise shrink?

<details class="tw-sol" markdown><summary>Worked solution</summary>

By \(\sqrt{4} = 2\): it halves. The plot shows it: 858 ppm at 2 minutes, 432 at 8, 223 at 32.

</details>
</div>

<div class="tw-prob" data-answer="76.4|76" data-tol="0.02" data-unit="million" data-hints='{"21213":"That is per second. An hour has 3,600 seconds."}' data-why="21,213 x 3,600 = 76.4 million electrons in an hour." markdown>
**3.** At 21,213 electrons per second, how many million electrons does TESS collect from our star in an hour?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(21{,}213 \times 3{,}600 = 76.4\) million.

</details>
</div>

## Sources

- TESS's cameras: NASA HEASARC, TESS Telescope Information ([page](https://heasarc.gsfc.nasa.gov/docs/tess/telescope_information.html), read 24 Nov 2026): "a 10.5 cm diameter entrance pupil and a focal ratio f/1.4", seven lenses, four 2048 x 2048 CCDs per camera operated at -75 degrees C.
- Our measurements (`book/tools/lesson_plots_u5a.py`, 24 Nov 2026): TESS sector 46 SPOC 2-minute light of TIC 172900988 (MAST), outside the eclipses, quality flags removed, a 12-hour running median divided out: 21,213 electrons per second, photon limit 627 ppm per 2 minutes, measured 858 ppm (2 minutes) to 113 ppm (2 hours), 1.37 to 1.43 times the limit (159 ppm at exactly 1 hour, 1.39 times); the file's own 1-hour noise figure (CDPP) is 195 ppm. The script stops if the scatter is below the photon limit or far from the file's own figure.
- Our noise against the photon floor across our stars: `research/stage3/rs041/P75-REESTIMATE-2026-11-22.md` (1.6 to 1.9 times at Tmag 9 to 11, 2 to 3 times at 12 to 13). An Earth-size planet dims a Sun-like star by about 84 ppm: \((6{,}371 / 695{,}700)^2\).
