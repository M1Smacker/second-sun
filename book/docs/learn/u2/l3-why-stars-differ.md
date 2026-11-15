---
hide: [toc, footer]
title: "2.3 Why stars differ"
---

# Why stars differ

The four sectors from lesson 2.1 again. Look only at the bottoms of the drops.

<div class="tw-plot" data-src="u2-four-sectors"></div>

<p class="tw-plot__ask">The two kinds of eclipse do not reach the same depth. Before reading on, guess why: is one star bigger, hotter, or something else?</p>

## Two numbers make a star's light

Our two stars are nearly twins, but not quite. The discovery paper measured them:

- **Star 1:** radius 1.3827 Suns, surface at 6,050 K.
- **Star 2:** radius 1.3124 Suns, surface at 5,983 K.
- **The Sun**, for comparison: radius 1, surface at 5,772 K.

<aside class="tw-mn" markdown>
**Kelvin (K).** Temperature counted from absolute zero. Add 273 to degrees Celsius; at these heats the difference hardly matters.
</aside>

How much light a star sends out in total is called its **luminosity**. It depends on just two things: how much glowing surface the star has, and how hot that surface is.

<aside class="tw-mn" markdown>
**Luminosity (\(L\)).** The total light a star sends out every second, in all directions. Here in Suns: \(L = 1\) is the Sun.
</aside>

The surface is easy: a sphere's area grows with its radius squared, \(R^2\). A star twice as wide has four times the glowing skin.

The heat is the surprise. Every square metre of a hot surface glows, and the glow grows with the temperature to the **fourth power**, \(T^4\). Make a surface twice as hot and each square metre shines \(2 \times 2 \times 2 \times 2 = 16\) times brighter. This is the **Stefan-Boltzmann law**, and it is why a small change in temperature matters far more than a small change in size.

<aside class="tw-mn" markdown>
**Stefan-Boltzmann law.** Light from each square metre of a hot surface grows as \(T^4\). Put together with the area: \(L = R^2 \, T^4\), with \(R\) and \(T\) both measured against the Sun.
</aside>

Put the two together, measuring both against the Sun:

\[ L = R^2 \times T^4 \]

## Think it through

Answer each before moving on. They build the idea one step at a time.

<div class="tw-prob" data-answer="4" data-tol="0.01" data-hints='{"2":"Area grows with the radius squared: 2 times 2."}' data-why="Area goes as R squared, so twice the radius gives 4 times the surface, and at the same temperature 4 times the light." markdown>
**a.** A star has twice the Sun's radius and the Sun's temperature. How many times more light does it give?
</div>

<div class="tw-prob" data-answer="16" data-tol="0.01" data-hints='{"2":"Temperature counts to the fourth power: 2 times 2 times 2 times 2.","4":"That is the square. Light goes with the fourth power of temperature."}' data-why="T to the fourth: 2 x 2 x 2 x 2 = 16." markdown>
**b.** Now a star the Sun's size but twice as hot. How many times more light?
</div>

<div class="tw-prob" data-answer="hotter|the hotter|hotter one|the hotter one" data-why="Each square metre of the hotter star shines more, so hiding the same area of it hides more light." markdown>
**c.** Two stars of the same size. You cover the same patch of each. Covering which one hides more light: the hotter or the cooler? (One word.)
</div>

!!! example "Worked example: how bright is star 1?"
    **Step 1. Radius squared.** \(1.3827^2 = 1.912\).

    **Step 2. Temperature against the Sun.** \(6050 / 5772 = 1.0482\).

    **Step 3. To the fourth power.** \(1.0482^4 = 1.207\). (Square it, then square again: \(1.0482^2 = 1.0987\), \(1.0987^2 = 1.207\).)

    **Step 4. Multiply.** \(L = 1.912 \times 1.207 = 2.31\) Suns.

    Notice what happened: the star is only 5% hotter than the Sun, yet that alone gives 21% more light per square metre. Its larger size gives the rest.

!!! question "Your turn, half done: star 2"
    Step 1: \(1.3124^2 = 1.7224\). Step 2: \(5983 / 5772 = 1.0366\). Finish: raise 1.0366 to the fourth power, then multiply.

<div class="tw-prob" data-answer="1.99" data-tol="0.02" data-unit="Suns" data-hints='{"1.79":"That uses the temperature squared. Square it twice: the fourth power.","1.15":"That is only the temperature part. Multiply by 1.7224 for the area."}' data-why="1.0366 to the fourth is 1.1545; times 1.7224 gives 1.99 Suns." markdown>
**Your turn.** Star 2's luminosity, in Suns:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(1.0366^2 = 1.0745\), \(1.0745^2 = 1.1545\). Then \(1.7224 \times 1.1545 = 1.99\) Suns.

The rule: **\(L = R^2 \, T^4\)**, both measured against the Sun. Together the pair gives \(2.31 + 1.99 = 4.30\) Suns of light, which is what TESS sees as one point of light.

</details>
</div>

## Back to the two eclipses

So why are the drops different? Your answer to c says part of it: when the hotter star is hidden, more light goes. But here the two stars are so close in temperature that each square metre of star 1 is only about 5% brighter than star 2's (\((6050 / 5983)^4 = 1.046\)). That cannot by itself turn one eclipse into 45% and the other into 36%.

The rest comes from the orbit. Lesson 2.1 showed it is a stretched oval: the stars are closer together at one eclipse than at the other. Seen from Earth, the front star then passes across the back star along a different line each time, a little more centrally at one eclipse than at the other, so the two discs overlap by different amounts. Star sizes, temperatures and orbit shape all leave their mark in the depths, which is how the discovery paper could measure every one of them from the light curve and the stars' speeds together.

<aside class="tw-mn" markdown>
**Colour.** Hotter stars also look bluer and cooler ones redder. Unit 3 shows why, from how hot things glow.
</aside>

## In a few sentences

A star's total light is \(L = R^2 \, T^4\) in Sun units: the area of its glowing skin times the fourth power of its temperature. Temperature wins: 5% hotter gives 21% more light from each square metre. Our two stars give 2.31 and 1.99 Suns. Their eclipses differ in depth partly because one is a little hotter, but mostly because the stretched orbit makes them overlap by different amounts.

## Problems

<div class="tw-prob" data-answer="0.0029" data-tol="0.05" data-unit="Suns" data-hints='{"0.073":"That is only the temperature part. Multiply by 0.2 squared.","0.0146":"Square the radius: 0.2 x 0.2 = 0.04."}' data-why="T = 3000/5772 = 0.520; to the fourth 0.0730; R squared 0.04; L = 0.0029 Suns." markdown>
**1.** A red dwarf has 0.2 of the Sun's radius and a surface at 3,000 K. Its luminosity, in Suns?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(3000 / 5772 = 0.520\); \(0.520^4 = 0.0730\). \(0.2^2 = 0.04\). \(L = 0.04 \times 0.0730 = 0.0029\) Suns: about 340 of them to match one Sun. Red dwarfs are the commonest stars near the Sun, yet even the nearest star of all, Proxima Centauri, a red dwarf, is far too faint to see without a telescope.

</details>
</div>

<div class="tw-prob" data-answer="2" data-tol="0.02" data-hints='{"16":"The question asks for the temperature, not the light.","4":"Fourth root, not square root: which number times itself four times gives 16?"}' data-why="L = R squared times T to the fourth. Same radius, 16 times the light: T to the fourth = 16, so T = 2." markdown>
**2.** A star the Sun's size gives 16 times the Sun's light. How many times hotter than the Sun is its surface?

<details class="tw-sol" markdown><summary>Worked solution</summary>

Same radius, so \(T^4 = 16\), and \(T = 2\): twice as hot, about 11,500 K. A blue-white star.

</details>
</div>

<div class="tw-prob" data-answer="1.21|1.2" data-tol="0.02" data-why="Same size, so the light ratio is (1.048) to the fourth = 1.207." markdown>
**3.** Two stars of the same size: one at the Sun's 5,772 K, the other at 6,050 K. How many times more light does the hotter one give?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\((6050 / 5772)^4 = 1.0482^4 = 1.21\). Less than 5% hotter, 21% more light.

</details>
</div>

<div class="tw-prob" data-answer="orbit|the orbit|orbit shape|the orbit shape|stretched orbit|the stretched orbit" data-why="The temperatures are nearly equal; the stretched orbit makes the discs overlap differently at the two eclipses." markdown>
**4.** In our pair, what makes most of the difference between the two eclipse depths: the temperatures or the orbit? (One word.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**The orbit.** The temperatures differ by only about 1%, giving about 5% in brightness per square metre. The stretched orbit makes the stars overlap by different amounts at the two eclipses, and that makes most of the difference.

</details>
</div>

## Sources

- Star radii and temperatures: Kostov et al. 2021, the discovery paper ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614)); radii from its abstract, temperatures \(6050 \pm 100\) K and \(5983 \pm 100\) K from its stellar properties table (read 15 Nov 2026).
- The Sun's surface temperature, 5,772 K: IAU 2015 Resolution B3 (nominal solar effective temperature).
- Proxima Centauri is a red dwarf at visual magnitude about 11, far below the naked-eye limit of about 6 (to be confirmed by the fact-check).
- \(L \propto R^2 T^4\) (the Stefan-Boltzmann law): any introductory text, for example OpenStax Astronomy 2e, chapter 5 "Radiation and Spectra" ([the book](https://openstax.org/details/books/astronomy-2e), CC BY-NC-SA 4.0).
- Different overlap at the two eclipses of an oval orbit: Winn 2010, "Transits and Occultations" ([arXiv 1001.2010](https://arxiv.org/abs/1001.2010)), where the crossing offsets of the two eclipses differ by the orbit's shape. That this, and not temperature, explains most of the depth difference here is our own reasoning from the paper's numbers (15 Nov 2026).
