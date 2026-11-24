---
hide: [toc, footer]
title: "4.3 Measuring stars from their eclipses"
---

# Measuring stars from their eclipses

Lesson 4.1 read the two eclipses' depths and timing. Here is the third thing an eclipse tells you: its length. These are the same two eclipses of TIC 172900988, hour by hour, each averaged over four TESS sectors.

<div class="tw-plot" data-src="u4-eclipse-primary"></div>

<div class="tw-plot" data-src="u4-eclipse-secondary"></div>

<p class="tw-plot__ask">The shallower eclipse lasts about two and a half times longer than the deeper one. Same two stars, same sizes. Before reading on, guess: what could make one eclipse so much longer?</p>

## How long two stars take to pass

An eclipse starts the moment the two stars' edges first touch, as we see them, and ends when they last touch. In between, the front star's centre moves past the back star's centre. If the centres pass straight through each other, the path from first touch to last touch is twice the two radii added together, \(2(R_1 + R_2)\). If they pass a little off centre, the path is shorter.

<aside class="tw-mn" markdown>
**First and last contact.** The moments an eclipse begins and ends: the two stars' discs, seen from Earth, first touch and last touch. The eclipse's full length is the time between them.
</aside>

So the length depends on two things: the path, and how fast the stars cross the sky. Lesson 4.2 found the speed changes round the orbit. At the deeper eclipse the stars are 0.108 AU apart and cross at 169 km/s; at the shallower one they are 0.266 AU apart and cross at only 68.6 km/s. That is the answer to the question above: same sizes, slower crossing, longer eclipse.

\[ R_1 + R_2 \;\geq\; \frac{v \times T}{2} \]

The sign \(\geq\) is there because an off-centre crossing has a shorter path, so a crossing through the middle gives the **smallest** sizes the eclipse allows. It is lesson 4.4's argument in reverse: there the planet's size was known and the speed was the question.

## Think it through

<div class="tw-prob" data-answer="2.47|2.5|2.469" data-tol="0.03" data-hints='{"0.405":"That is short over long. Divide the longer eclipse by the shorter one."}' data-why="13.25 / 5.37 = 2.47. The speeds, 169 and 68.6 km/s, differ by 169 / 68.6 = 2.46: almost exactly the same factor." markdown>
**a.** Fitting each eclipse, our script finds the deeper one lasts 5.37 hours from first to last contact and the shallower one 13.25 hours. How many times longer is the shallower one?
</div>

!!! example "Worked example: the deeper eclipse"
    The stars cross at 169 km/s for 5.37 hours. The Sun's radius is 695,700 km.

    **Step 1. The time in seconds.** \(5.37 \times 3{,}600 = 19{,}332\) s.

    **Step 2. Half the path.** \(169 \times 19{,}332 / 2 = 1.634 \times 10^{6}\) km.

    **Step 3. In Sun radii.** \(1.634 \times 10^{6} / 695{,}700 = 2.35\). So \(R_1 + R_2\) is **at least 2.35 Sun radii**.

!!! question "Your turn, half done: the shallower eclipse"
    The stars cross at 68.6 km/s for 13.25 hours. Step 1: \(13.25 \times 3{,}600 = 47{,}700\) s. Finish: the smallest \(R_1 + R_2\) this eclipse allows, in Sun radii.

<div class="tw-prob" data-answer="2.35|2.352" data-tol="0.02" data-unit="Sun radii" data-hints='{"4.70":"That is the whole path. The path is twice the radii added together: divide by 2.","1636000":"That is in km. Divide by the Sun radius, 695,700 km."}' data-why="68.6 x 47,700 / 2 = 1.636e6 km; / 695,700 = 2.35 Sun radii." markdown>
**Your turn.** \(R_1 + R_2\) at least, in Sun radii:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(68.6 \times 47{,}700 / 2 = 1.636 \times 10^{6}\) km, and \(1.636 \times 10^{6} / 695{,}700 = 2.35\) Sun radii: the same as the deeper eclipse, to within 0.2%.

The rule: **eclipse length \(\times\) crossing speed \(= \) path, and the path is at most \(2(R_1 + R_2)\)**.

</details>
</div>

## Two eclipses, one tilt

Why do both eclipses give the same answer? Because of the tilt of the orbit. Seen exactly edge-on, the centres pass straight through each other at both eclipses. Tip the orbit a little and, at mid-eclipse, the centres are offset on the sky by the stars' distance apart times a small number, \(r \cos i\). The far eclipse (big \(r\)) gets a much bigger offset than the near one, so its path shrinks much more.

<aside class="tw-mn" markdown>
**Inclination \(i\).** The tilt of an orbit as we see it: 90 degrees is exactly edge-on, 0 degrees face-on. Eclipses need it very close to 90 degrees.
</aside>

For our pair, \(R_1 + R_2\) is 2.70 Sun radii in Kostov et al. 2021. At a tilt of 88 degrees, the centres would miss by 0.81 Sun radii at the near eclipse and 1.99 at the far one, so the far eclipse would come out clearly shorter than our rule predicts. At 85 degrees the far offset would be 4.98 Sun radii: more than 2.70, so the far eclipse would **not happen at all**, and the pair would show only one eclipse per orbit. Both of ours give the same size, so the offsets must be tiny: the orbit is almost exactly edge-on. The paper's value is 89.42 degrees.

## Why our size comes out small

Our 2.35 Sun radii is 87% of the paper's 2.70. With the paper's tilt, our script predicts full lengths of 6.15 and 14.86 hours; ours are 5.37 and 13.25, both about 12% short. The likely cause: at first and last contact the front star covers only a thin sliver of the back star's edge, and the edge is the darkest part of the disc (limb darkening, lesson 4.1). The first and last half hour of each eclipse barely dims the light, so our straight-sided fitted shape starts late and ends early. We have not tested this; the paper fits the full curved shape, with limb darkening, and so gets the true contact times.

## What professionals add

Eclipses give sizes and the tilt. Spectra give the speeds of both stars directly (lesson 3.4's Doppler shifts), and with the tilt known, Kepler's laws turn those speeds into masses, not just lower limits. For pairs measured both ways, the masses and radii of both stars are known to 3% or better: 95 such systems in Torres, Andersen and Giménez 2010. They are the best measurements of stars we have, and models of how stars live are tested on them.

## Why this matters for Second Sun

Before searching a pair for a planet, our filter hides each eclipse with a window in time. The window's width comes from the eclipse's length in a catalogue. Catalogues measure that length in different ways, the Census list records which way each one used, and this lesson shows why it matters: a straight-sided fit gives lengths about 12% shorter than first-to-last contact. A window that is too narrow leaves the faint edges of an eclipse in the light, where they can look like a planet's dip.

## In a few sentences

An eclipse lasts as long as the stars take to cross from first to last contact, so its length times the crossing speed is a path no longer than \(2(R_1 + R_2)\). For TIC 172900988 the eclipses last 5.37 and 13.25 hours at 169 and 68.6 km/s, and both give \(R_1 + R_2\) of at least 2.35 Sun radii. That they agree means the orbit is almost exactly edge-on (the paper: 89.42 degrees). Our straight-sided fit misses the faint first and last moments, so the true size, 2.70 Sun radii, is 15% larger.

## Problems

<div class="tw-prob" data-answer="0.58|0.578" data-tol="0.05" data-unit="Sun radii" data-hints='{"57.1":"That is the distance itself. Multiply by cos(89.42 degrees), about 0.0101.","0.235":"That is the near eclipse. Use the far one, 57.1 Sun radii."}' data-why="57.1 x cos(89.42 degrees) = 57.1 x 0.0101 = 0.58 Sun radii." markdown>
**1.** At the shallower eclipse the stars are 0.266 AU apart, which is 57.1 Sun radii. With the paper's tilt of 89.42 degrees (\(\cos i = 0.0101\)), how far apart are their centres on the sky at mid-eclipse, in Sun radii?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(57.1 \times 0.0101 = 0.58\) Sun radii, far less than the 2.70 Sun radii needed to touch. The path is barely shorter than a crossing through the middle.

</details>
</div>

<div class="tw-prob" data-answer="no" data-hints='{"yes":"Work out the offset first: 57.1 x cos(85 degrees) = 57.1 x 0.087."}' data-why="57.1 x 0.087 = 4.98 Sun radii, more than R1 + R2 = 2.70: the discs never touch, so no eclipse." markdown>
**2.** Tip the same orbit to 85 degrees (\(\cos i = 0.087\)). Does the shallower eclipse still happen? (Yes or no.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**No.** The offset would be \(57.1 \times 0.087 = 4.98\) Sun radii, more than the 2.70 Sun radii at which the discs touch. The near eclipse would still happen (offset \(23.2 \times 0.087 = 2.02\)), so the pair would show one eclipse per orbit.

</details>
</div>

<div class="tw-prob" data-answer="0.87|0.873|87" data-tol="0.02" data-hints='{"1.15":"Upside down: our length divided by the predicted one."}' data-why="5.37 / 6.15 = 0.87: our fitted length is 87% of the true first-to-last-contact length." markdown>
**3.** The paper's sizes and tilt predict the deeper eclipse lasts 6.15 hours. Ours is 5.37 hours. What share of the true length did our fit catch?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(5.37 / 6.15 = 0.87\). The missing 13% is the faint first and last part of the eclipse, when only a sliver of the darker edge is covered.

</details>
</div>

<div class="tw-prob" data-answer="spectra|spectrum|doppler|doppler shifts|speeds|radial velocities|radial velocity" data-hints='{"eclipses":"Eclipses give sizes and tilt. What gave the speed of 51 Pegasi in lesson 3.4?"}' data-why="Spectra: their Doppler shifts give both stars' speeds, and with the tilt from the eclipses Kepler's laws give the masses." markdown>
**4.** Eclipses give the stars' sizes and the tilt. What else do you need to weigh both stars? (One word.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**Spectra**: their Doppler shifts give each star's speed, and with the tilt from the eclipses, Kepler's laws give each star's mass.

</details>
</div>

## Sources

- The light: TESS sectors 44 to 47, SPOC 2-minute light curves of TIC 172900988, from MAST, as in lessons 4.1 and 4.2. Our script `book/tools/lesson_plots_u4c.py` (24 Nov 2026) fits each folded eclipse with a straight-sided shape (a trapezoid): full lengths 5.37 and 13.25 hours. It takes the speeds from Kepler's laws with the paper's period, stretch and masses and lesson 4.2's orientation, and stops if the two eclipses' size limits differ by more than 5% (they differ by 0.2%) or if the limit is not between 75% and 100% of the paper's size (it is 87%).
- The system: Kostov et al. 2021, AJ 162, 234 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614), HTML tables read 24 Nov 2026): binary inclination 89.4182 degrees (or the mirror value 90.59), star 1 radius 1.3846 Sun radii and radius ratio 1.0527, so \(R_1 + R_2 = 2.70\) Sun radii; the orbit's orientation 69.6 degrees, within 1 degree of the 70.6 degrees lesson 4.2 read from our own eclipses.
- Masses and radii to 3%: Torres, Andersen and Giménez 2010, "Accurate masses and radii of normal stars", A&ARv 18, 67 ([arXiv 0908.2624](https://arxiv.org/abs/0908.2624), abstract read 24 Nov 2026): 95 detached binaries, 94 of them eclipsing, with both stars' mass and radius known to 3% or better.
- 1 AU = 215.0 Sun radii and the Sun's radius 695,700 km: IAU 2015 nominal values.
