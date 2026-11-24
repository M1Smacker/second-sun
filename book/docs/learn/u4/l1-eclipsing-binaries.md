---
hide: [toc, footer]
title: "4.1 Eclipsing binaries"
---

# Eclipsing binaries

Unit 1 opened with this star's light and its deep drops. Here are four TESS sectors of it, about five orbits, laid on top of each other by folding them on the pair's period, 19.66 days.

<div class="tw-plot" data-src="u4-eb-folded"></div>

<p class="tw-plot__ask">Two dips per orbit, not one, and they are not the same depth. And the second one is not halfway round. Before reading on, guess: what makes two dips, and what could push the second one late?</p>

## Two stars taking turns

TIC 172900988 is two stars, a little larger and hotter than the Sun, circling each other every 19.66 days. We happen to see their orbit almost edge-on, so once per orbit the first star passes in front of the second, and once per orbit the second passes in front of the first. Each passage blocks some light: an **eclipse**. So an orbit gives two eclipses.

<aside class="tw-mn" markdown>
**Eclipsing binary.** Two stars orbiting each other, seen so nearly edge-on that they take turns passing in front of each other. Most binaries are tilted and never eclipse; we only see eclipses when the orbit lines up with us.
</aside>

The deeper one is called the **primary eclipse**, the shallower the **secondary eclipse**. On this plot the primary is at day 0 and removes 43.5% of the light; the secondary, at day 11.88, removes 35.8%.

## How deep an eclipse is

TESS sees the two stars as one point, so an eclipse removes the light of whatever part of the back star is covered. Lesson 2.3 measured the two stars' light: the first gives 2.31 Suns, the second 1.99, together 4.30. If the front star covers a share \(s\) of the back star's disc, and the back star's surface is evenly bright:

\[ \text{depth} = s \times \frac{L_{\text{back}}}{L_1 + L_2} \]

<aside class="tw-mn" markdown>
**Limb darkening (a correction we ignore here).** A real star's disc is a little darker at its edge than at its centre, so covering the middle blocks more light than covering the edge. Our rule treats the disc as evenly bright, which is good enough to read the plot.
</aside>

## Think it through

<div class="tw-prob" data-answer="46.3|46" data-tol="0.02" data-unit="percent" data-hints='{"53.7":"That is star 1 left over. When star 2 is fully covered, the missing light is star 2: 1.99 out of 4.30.","0.463":"That is the share. Give it in percent: multiply by 100."}' data-why="1.99 / 4.30 = 0.463, so 46.3% of the light." markdown>
**a.** Star 1 is the bigger one (1.38 Sun radii against 1.31), so it can hide star 2 completely. What is the deepest that eclipse could be, in percent?
</div>

!!! example "Worked example: depth from the share covered"
    Two identical stars, each giving half the light. The front one covers 60% of the back one's disc.

    **Step 1. The back star's share of the light.** \(L_{\text{back}} / (L_1 + L_2) = 1/2\).

    **Step 2. Multiply by the share covered.** \(0.60 \times 0.5 = 0.30\).

    **Step 3.** The eclipse is **30%** deep. Covering more of the disc, or covering the brighter star, makes it deeper.

!!! question "Your turn, half done: our two stars"
    Star 2 passes in front of star 1 and covers 80% of its disc. Step 1: star 1's share of the light is \(2.31 / 4.30 = 0.537\). Finish: how deep is the eclipse?

<div class="tw-prob" data-answer="43|43.0" data-tol="0.02" data-unit="percent" data-hints='{"0.43":"That is the share. Give it in percent.","37":"You used star 2. Star 1 is the one being covered: 2.31 out of 4.30."}' data-why="0.80 x 0.537 = 0.430, so 43% deep: close to the primary eclipse on the plot." markdown>
**Your turn.** The depth, in percent:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(0.80 \times 0.537 = 0.430\), so **43%**. The real primary eclipse is 43.5% deep, so star 2 covers roughly 80% of star 1 at that moment.

The rule: **depth = share covered \(\times\) the back star's share of the light**.

</details>
</div>

## Why the two eclipses differ

The two stars are almost the same temperature (6,050 K and 5,983 K in Kostov et al. 2021), so square metre for square metre they shine almost equally: \((6050 / 5983)^{4} = 1.05\), only 5% apart. That cannot turn 35.8% into 43.5%. The difference comes from **how much** of the back star is covered, and that comes from the shape of the orbit.

## Why the second eclipse is late

In a circular orbit the stars move at a steady speed, so the second eclipse comes exactly half an orbit after the first: day 9.83 here. It comes at day 11.88 instead, 60.4% of the way round.

The orbit is **stretched**. Its eccentricity is 0.448 (lesson 2.1 found the distance between the stars swinging from about 0.11 to 0.28 AU). The stars move fast when they are close together and slowly when they are far apart, as Kepler's second law says (equal areas in equal times). The two eclipses happen at two fixed points of the orbit, the two moments when the stars line up with us, and the time from one to the other depends on whether that stretch of the orbit is a near, fast part or a far, slow part. Here one stretch takes 11.88 days and the other only 7.78.

The same stretch changes the depths. At one eclipse the stars are closer together than at the other, so seen from Earth they overlap differently: one passes more squarely across the other's face.

<aside class="tw-mn" markdown>
**Eccentricity \(e\).** How stretched an orbit is: 0 for a circle, close to 1 for a long thin ellipse. Earth's is 0.017; this pair's is 0.448.
</aside>

A rule of thumb from the timing alone: the shift away from half an orbit, as a share of the orbit, is about \(\frac{2}{\pi}\, e\cos\omega\), where \(\omega\) is the angle saying which way the stretched orbit points. Here the shift is \(0.604 - 0.5 = 0.104\), so \(e\cos\omega \approx 0.104 \times \pi / 2 = 0.16\). Our exact calculation with Kepler's equation gives 0.15. The timing therefore says the orbit is stretched by **at least** 0.15; the full 0.448 also needs the eclipses' lengths and, in the paper, the planet's own pull.

## Why this matters for Second Sun

Every star on our hunt lists is a pair like this one. Their eclipses are 100 times deeper than a planet's dip, so the search must hide them first, using a table of when each eclipse happens. When that table's times are wrong, the hiding windows slide off the real eclipses or swell to cover the whole sector, and planets are lost (this week's eclipse-timing work, FIX 94, measures those times from TESS's own eclipses, exactly as this lesson did). A planet around such a pair circles both stars, outside this 19.66-day dance.

## In a few sentences

An eclipsing binary is a pair of stars seen nearly edge-on, so each orbit brings two eclipses: the primary (deeper) and the secondary. An eclipse's depth is the share of the back star covered times that star's share of the total light. For TIC 172900988 the eclipses are 43.5% and 35.8% deep; the stars are nearly equally hot, so the difference comes from how much they overlap. The secondary comes 11.88 days after the primary, not 9.83, because the orbit is stretched (e = 0.448), and the timing alone shows a stretch of at least 0.15.

## Problems

<div class="tw-prob" data-answer="11.88|11.9" data-tol="0.01" data-unit="days" data-why="The shallower dip sits at day 11.88 of the 19.66-day orbit." markdown>
**1.** Touch the plot. On which day of the orbit does the shallower (secondary) eclipse fall?

<details class="tw-sol" markdown><summary>Worked solution</summary>

Day **11.88**. The next primary comes at day 19.66, 7.78 days later.

</details>
</div>

<div class="tw-prob" data-answer="9.83" data-tol="0.01" data-unit="days" data-hints='{"19.66":"That is a full orbit. A circular orbit puts the second eclipse halfway round."}' data-why="Half of 19.66 days is 9.83 days." markdown>
**2.** If the orbit were a circle, on which day would the secondary eclipse fall?

<details class="tw-sol" markdown><summary>Worked solution</summary>

Halfway round: \(19.66 / 2 = 9.83\) days. The real one is 2.05 days later than that.

</details>
</div>

<div class="tw-prob" data-answer="35.8|36" data-tol="0.03" data-unit="percent" data-hints='{"64.2":"That is the light left over at the bottom. The depth is the light missing: 1 minus 0.642."}' data-why="The bottom of the secondary eclipse sits near 0.642 of normal, so 35.8% of the light is missing." markdown>
**3.** Touch the bottom of the secondary eclipse. How deep is it, in percent?

<details class="tw-sol" markdown><summary>Worked solution</summary>

The bottom is near 0.642 of normal brightness, so **35.8%** of the light is gone.

</details>
</div>

<div class="tw-prob" data-answer="1.05|1.045" data-tol="0.02" data-hints='{"1.011":"That is the temperature ratio. The glow per square metre goes as the fourth power: 1.011 x 1.011 x 1.011 x 1.011."}' data-why="(6050 / 5983)^4 = 1.0112^4 = 1.045." markdown>
**4.** Star 1 is at 6,050 K and star 2 at 5,983 K. How many times brighter is each square metre of star 1? (Use the \(T^4\) rule of lesson 2.3.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

\((6050 / 5983)^{4} = 1.0112^{4} = 1.045\): only about 5% brighter. Far too little to explain eclipses of 43.5% and 35.8%; the overlap must differ.

</details>
</div>

<div class="tw-prob" data-answer="0.16|0.164" data-tol="0.05" data-hints='{"0.104":"That is the shift itself. The rule says shift = (2/pi) x e cos(omega), so multiply the shift by pi/2.","0.066":"Multiply by pi/2, do not multiply by 2/pi."}' data-why="0.104 x pi / 2 = 0.163." markdown>
**5.** Another pair has its secondary eclipse at 0.604 of the orbit too. Using the rule of thumb, what is \(e\cos\omega\)?

<details class="tw-sol" markdown><summary>Worked solution</summary>

Shift \(= 0.604 - 0.5 = 0.104\); \(e\cos\omega \approx 0.104 \times \pi / 2 = 0.163\). The rule of thumb is best for nearly round orbits. The timing alone cannot give an exact answer: the exact value also depends on the stretch \(e\). (For our own pair, with its measured \(e = 0.448\), it came out at 0.149.)

</details>
</div>

## Sources

- The light: TESS sectors 44 to 47, SPOC 2-minute light curves of TIC 172900988 (PDCSAP flux, quality flags removed), from MAST, as in lessons 1.1 and 2.1.
- The system: Kostov et al. 2021, "TIC 172900988: A Transiting Circumbinary Planet Detected in One Sector of TESS Data", AJ 162, 234 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614), abstract and HTML tables read 23 Nov 2026): binary period 19.658173 d (Table 5), eccentricity 0.4479 (Table 6), star radii 1.384 and 1.312 Sun radii (Table 5), temperatures 6,050 and 5,983 K (Table 3); TESS-only eclipse depths "about 40% and 35%" (section 2.1).
- Our checks, `book/tools/lesson_plots_u4.py` (23 Nov 2026): 5 primary and 4 secondary eclipses; median depths 43.5% and 35.8%; secondary at 0.6043 of the orbit (11.879 d); with e = 0.4479 the exact edge-on timing (Kepler's equation) reproduces that separation at e cos(omega) = 0.149, the first-order rule gives 0.164. A failure of the depth or timing check stops the plot.
- The first-order timing rule (the secondary's shift from half an orbit is about (2/pi) e cos(omega) for a nearly edge-on orbit): the standard result found in eclipsing-binary texts, for example Kallrath and Milone, "Eclipsing Binary Stars: Modeling and Analysis" (Springer). Eclipses, primary and secondary, and Kepler's second law: OpenStax Astronomy 2e, chapters 3 and 18 ([the book](https://openstax.org/details/books/astronomy-2e), CC BY-NC-SA 4.0), in our own words.
- Earth's eccentricity 0.0167: NASA Earth fact sheet ([nssdc.gsfc.nasa.gov](https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html)).
