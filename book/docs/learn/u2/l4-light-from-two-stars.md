---
hide: [toc, footer]
title: "2.4 Light from two stars at once"
---

# Light from two stars at once

The planet's second crossing, the one from lessons 1.4 and 2.2. This time, think about the depth.

<div class="tw-plot" data-src="u1-planet-b"></div>

<p class="tw-plot__ask">Lesson 1.4 measured this dip at about 2,655 ppm. The planet is as wide as Jupiter, and Jupiter across the Sun makes about 10,600 ppm. Why is this dip so much shallower?</p>

## One point of light, two stars inside it

TESS cannot see our two stars apart. They are only about 0.19 AU from each other, and from Earth that is far smaller than anything a telescope can separate. So every point on our light curve is the light of **both** stars added together.

When the planet crosses star 2, it blocks part of star 2's light only. Star 1 keeps shining as if nothing happened. The dip is real, but it is measured against the light of both stars, so it looks shallower. Astronomers call this **dilution**: the dip is watered down by light that the planet never touched.

<aside class="tw-mn" markdown>
**Dilution.** Extra light from another star (a partner, or an unrelated star in the same pixels) that makes a dip look shallower than it really is.
</aside>

The rule is one multiplication. If the crossed star gives a fraction \(s\) of all the light we receive:

\[ \text{seen depth} = \left( \frac{R_p}{R_\star} \right)^2 \times s \]

<aside class="tw-mn" markdown>
**The share \(s\).** The crossed star's light divided by the total: 1 if it shines alone, \(\tfrac12\) for two identical twins.
</aside>

## Think it through

<div class="tw-prob" data-answer="0.5|1/2|half" data-tol="0.01" data-why="Two identical stars each give half of the light." markdown>
**a.** Two identical twin stars. What share \(s\) of the light does one of them give? (A number.)
</div>

<div class="tw-prob" data-answer="5000" data-tol="0.01" data-unit="ppm" data-hints='{"10000":"That is the depth if the star shone alone. Its twin adds the same light again.","20000":"Dilution makes a dip shallower, never deeper."}' data-why="10,000 ppm times the share 0.5 gives 5,000 ppm." markdown>
**b.** A planet would block 10,000 ppm of one twin's light. How deep is the dip we see, in ppm?
</div>

<div class="tw-prob" data-answer="smaller|small" data-why="A shallow dip read without dilution gives a small radius ratio, so a small planet." markdown>
**c.** If we forget the twin and read the shallow dip as if the star shone alone, will we think the planet is bigger or smaller than it really is? (One word.)
</div>

!!! example "Worked example: what should the dip be?"
    The paper gives the planet 11.25 Earth radii and star 2 1.3124 Sun radii (one Sun radius is 109.08 Earth radii).

    **Step 1. Radius ratio.** \(11.25 / (1.3124 \times 109.08) = 11.25 / 143.16 = 0.07859\).

    **Step 2. Depth if star 2 shone alone.** \(0.07859^2 = 0.006176\), that is 6,176 ppm.

    **Step 3. Star 2's share of the light.** From lesson 2.3: star 2 gives 1.99 Suns, the pair 4.30. So \(s = 1.99 / 4.30 = 0.463\).

    **Step 4. Seen depth.** \(6{,}176 \times 0.463 = 2{,}860\) ppm.

    Lesson 1.4 measured 2,655 ppm. The simple rule gets within about 8%. The rest is detail this lesson leaves out: a star's disc is darker at its edge than at its centre, our measured average includes some points at the dip's edges, and TESS sees red light, where the two stars' shares are slightly different from their shares of all light (lesson 2.3 counted all colours).

!!! question "Your turn, half done: forgetting the partner"
    Suppose nobody knew star 1 was there. We see 2,655 ppm and think star 2 shines alone. Step 1: \(\sqrt{0.002655} = 0.05153\), so the planet looks 0.05153 times as wide as star 2. Finish: star 2 is 143.16 Earth radii wide; how many Earth radii would we give the planet?

<div class="tw-prob" data-answer="7.38" data-tol="0.02" data-unit="Earth radii" data-hints='{"0.0515":"That is the ratio. Multiply by 143.16 Earth radii.","10.8":"That is with dilution corrected. This step forgets the partner star."}' data-why="0.05153 times 143.16 = 7.38 Earth radii." markdown>
**Your turn.** The planet's size if we forget dilution, in Earth radii:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(0.05153 \times 143.16 = 7.38\) Earth radii: a planet between Neptune (3.9) and Saturn (9.4) in size. Correct for dilution first (divide the depth by 0.463: 5,736 ppm, ratio 0.0757) and it becomes 10.8 Earth radii, close to the paper's 11.25.

The rule: **divide the seen depth by the share before you work out the planet's size.** Forget dilution and every planet looks too small.

</details>
</div>

## The same trick can fool us

Dilution also works the other way, and it is one of the most common ways a search gets fooled. TESS pixels are large: each one is about 21 arcseconds across, so light from faint stars nearby often lands in the same pixels as our target. Now imagine one of those faint stars is itself an eclipsing binary, with eclipses 50% deep. If that star gives only 1% of the light in our pixels, its eclipse shows up in our light curve as \(50\% \times 0.01 = 0.5\%\): 5,000 ppm, exactly the depth a giant planet would make.

<aside class="tw-mn" markdown>
**Blend.** A dip that comes from another star mixed into the same pixels, not from the target. The checks in Unit 7 exist to catch blends.
</aside>

That is why every candidate dip gets the pixel and neighbour checks in Unit 7: is the dip centred on our star, or on a neighbour? For our pair, the TESS Input Catalog estimates that other stars add only about 0.05% to the light in the pixels, so blends are not a worry here. The partner star is.

## In a few sentences

When two stars share one point of light, a planet crossing one of them makes a dip diluted by the other's light: seen depth = \((R_p/R_\star)^2 \times s\), with \(s\) the crossed star's share. Star 2 gives 46% of our pair's light, which turns a 6,176 ppm dip into about 2,860. Forget dilution and planets look too small; an unseen faint eclipsing binary in the same pixels can, diluted, look just like a planet.

## Problems

<div class="tw-prob" data-answer="2000" data-tol="0.01" data-unit="ppm" data-hints='{"10000":"Multiply by the share, 0.2.","50000":"Multiply by the share, do not divide."}' data-why="10,000 ppm times 0.2 = 2,000 ppm." markdown>
**1.** A planet would block 10,000 ppm of its star's light, but that star gives only 20% of the light we receive. How deep is the dip we see, in ppm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(10{,}000 \times 0.2 = 2{,}000\) ppm.

</details>
</div>

<div class="tw-prob" data-answer="5000" data-tol="0.01" data-unit="ppm" data-hints='{"500000":"The 50% eclipse is diluted by the 1% share: multiply them.","50":"Check: 50% is 500,000 ppm; times 0.01."}' data-why="50% = 500,000 ppm; times the 1% share (0.01) = 5,000 ppm." markdown>
**2.** A faint background star gives 1% of the light in our pixels and has eclipses 50% deep. How deep do they look in our light curve, in ppm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(50\% = 500{,}000\) ppm. Times \(0.01\): 5,000 ppm. A giant planet's depth, made by a star that is not our target at all.

</details>
</div>

<div class="tw-prob" data-answer="4000" data-tol="0.01" data-unit="ppm" data-hints='{"1000":"Divide by the share, do not multiply.","2000":"Twins: each gives half, so double the seen depth."}' data-why="Seen depth / share = 2,000 / 0.5 = 4,000 ppm." markdown>
**3.** Around two identical twin stars we see a 2,000 ppm dip. How deep would it be if the crossed star shone alone, in ppm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

Each twin gives \(s = 0.5\). Undiluted depth \(= 2{,}000 / 0.5 = 4{,}000\) ppm.

</details>
</div>

<div class="tw-prob" data-answer="shallower|shallow" data-why="Its share of the light falls, so the planet's dip is diluted more." markdown>
**4.** In a pair, the planet crosses the fainter star. Compared with crossing an equal-sized but brighter partner, is the dip deeper or shallower? (One word.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**Shallower.** The fainter star's share \(s\) is smaller, so more of the light we see comes from the partner the planet does not touch.

</details>
</div>

## Sources

- Planet and star radii: Kostov et al. 2021 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614)), abstract; the planet first crossed the primary star, then 5 days later the secondary (the crossing in this lesson's plot). Contamination 0.000453 from the paper's table, quoting the TESS Input Catalog (read 15 Nov 2026).
- 1 Sun radius = 109.08 Earth radii (IAU nominal values).
- TESS pixels are about 21 arcseconds across: Ricker et al. 2015, the TESS mission paper ([arXiv 1406.0151](https://arxiv.org/abs/1406.0151)); to be confirmed by the fact-check.
- Dilution and blends as false positives: any vetting guide; for the TESS case see the TESS mission paper above. Neptune 3.9 and Saturn 9.4 Earth radii: NASA planetary fact sheets (equatorial radii, rounded).
- The 2,860 ppm prediction, its 8% gap and the 7.38 and 10.8 Earth-radii figures are our own arithmetic from the paper's numbers (15 Nov 2026).
