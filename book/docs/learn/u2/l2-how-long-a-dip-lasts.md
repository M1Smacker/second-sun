---
hide: [toc, footer]
title: "2.2 How long a dip lasts"
---

# How long a dip lasts

The planet's second crossing from lesson 1.4 again. This time, ignore the depth and look only at the time.

<div class="tw-plot" data-src="u1-planet-b"></div>

<p class="tw-plot__ask">Touch where the light starts to fall and where it is back. How many hours apart are they? (Read the days, then multiply by 24.)</p>

## Width of the star, speed of the planet

A planet's dip lasts as long as the planet takes to cross the face of its star. That is a simple travel-time problem, the same as a car crossing a bridge: time = distance / speed.

The distance is about the width of the star, \(2 R_\star\) (a little more, because the planet's own disc must get fully on and off; we will ignore that small extra). The speed comes from the orbit. In one period \(P\) the planet travels once round a circle of radius \(a\), a distance of \(2 \pi a\), so its speed is \(2 \pi a / P\). Divide:

\[ T = \frac{2 R_\star}{2 \pi a / P} = \frac{P}{\pi} \cdot \frac{R_\star}{a} \]

<aside class="tw-mn" markdown>
**Transit duration (\(T\)).** How long a dip lasts. This simple form assumes a circular orbit, a crossing straight through the middle of the star, and a star that stands still.
</aside>

The formula says three things. A longer year (bigger \(P\)) means a longer dip. A bigger star (bigger \(R_\star\)) means a longer dip. A wider orbit (bigger \(a\)) means a shorter one, because the star looks smaller from far away... except that \(P\) also grows with \(a\) (lesson 2.1), and that wins: far-out planets make long dips.

<aside class="tw-mn" markdown>
**Same units.** \(R_\star\) and \(a\) must be in the same unit before you divide. 1 AU is 215 Sun radii.
</aside>

!!! example "Worked example: the Earth crossing the Sun"
    Seen from far away, how long would the Earth's dip across the Sun last?

    **Step 1. The ratio \(R_\star / a\).** The Sun's radius is 1, and 1 AU is 215.0 Sun radii, so \(R_\star / a = 1 / 215.0 = 0.004651\).

    **Step 2. \(P / \pi\).** \(365.25 / 3.1416 = 116.26\) days.

    **Step 3. Multiply.** \(116.26 \times 0.004651 = 0.5407\) days.

    **Step 4. Into hours.** \(0.5407 \times 24 = 13.0\) hours.

    An alien astronomer watching the Sun would see the Earth's 84 ppm dip last about 13 hours, once a year.

!!! question "Your turn, half done: a hot Jupiter"
    A giant planet orbits a Sun-like star every 3 days, at \(a = 0.0407\) AU (from Kepler's law). Step 1: \(a\) in Sun radii is \(0.0407 \times 215.0 = 8.75\), so \(R_\star / a = 1 / 8.75 = 0.1143\). Finish: work out \(P / \pi\), multiply, and give the duration in hours.

<div class="tw-prob" data-answer="2.62" data-tol="0.02" data-unit="hours" data-hints='{"0.109":"That is in days. Multiply by 24 for hours.","0.11":"That is in days. Multiply by 24 for hours."}' data-why="3 / 3.1416 = 0.955 days; times 0.1143 = 0.109 days; times 24 = 2.62 hours." markdown>
**Your turn.** Duration of the hot Jupiter's dip, in hours:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(P / \pi = 3 / 3.1416 = 0.955\) days. Times \(0.1143\): \(0.109\) days. Times 24: 2.62 hours.

The rule: **\(T = (P / \pi)(R_\star / a)\).** Close-in planets make short dips: a few hours, against 13 for the Earth and about 30 for Jupiter (33 if Jupiter's own size is counted).

</details>
</div>

## Around two suns, the clock runs differently

Now try the formula on our planet. From lessons 1.2 and 2.1: \(P \approx 200\) days, \(a \approx 0.90\) AU \(= 193.5\) Sun radii, and the star it crosses in this plot is the smaller one, 1.31 Sun radii. So \(R_\star / a = 1.31 / 193.5 = 0.00677\), \(P / \pi = 63.7\) days, and \(T = 63.7 \times 0.00677 = 0.431\) days, about 10 hours.

But the plot at the top shows a dip lasting only about 6 hours (our rough reading: the light stays more than 1,200 ppm low for about 6 hours). Why so short?

Two of the formula's assumptions can fail here. First, the planet may not cross through the middle of the star: an off-centre path is a shorter chord, and a crossing about 0.8 star radii off-centre would alone turn 10 hours into 6. Second, the star does not stand still. Each star swings round the pair's centre every 19.7 days, at a speed our numbers put near 50 km/s, about as fast as the planet itself travels (also near 50 km/s). If the star happens to move towards the planet as it crosses, their speeds add up and the crossing is quick. If the star moves the same way as the planet, it is almost a race, and the crossing can last much longer. From one dip we cannot tell which effect matters more; the discovery paper fits both with a full model of the three bodies. What is certain is that around two suns every dip has its own length, and its spacing and depth change too. Unit 3 takes this apart, because it is the very thing our search has to cope with.

<aside class="tw-mn" markdown>
**The speeds.** Star: about half of the 0.19 AU separation, once round in 19.7 days. Planet: 0.9 AU, once round in about 200 days. Both come to about 50 km/s.
</aside>

## In a few sentences

A dip lasts as long as the planet takes to cross its star: \(T = (P / \pi)(R_\star / a)\) for a circular orbit straight through the middle of a still star. The Earth would make a 13-hour dip, a hot Jupiter a 2 to 3-hour one. Around two suns the star moves too, so each crossing has its own length.

## Problems

<div class="tw-prob" data-answer="3.95" data-tol="0.02" data-unit="hours" data-hints='{"0.165":"That is in days. Multiply by 24.","0.16":"That is in days. Multiply by 24."}' data-why="a = 0.09 times 215 = 19.35 Sun radii; R/a = 0.0517; P/pi = 3.183 days; T = 0.165 days = 3.95 hours." markdown>
**1.** A planet orbits a star of one Sun radius every 10 days, at \(a = 0.09\) AU. How long is its dip, in hours?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(a = 0.09 \times 215.0 = 19.35\) Sun radii, so \(R_\star / a = 1 / 19.35 = 0.0517\). \(P / \pi = 10 / 3.1416 = 3.183\) days. \(T = 3.183 \times 0.0517 = 0.165\) days \(= 3.95\) hours.

</details>
</div>

<div class="tw-prob" data-answer="2" data-tol="0.01" data-hints='{"4":"Duration grows with the star radius itself, not its square.","0.5":"A bigger star takes longer to cross."}' data-why="T is proportional to the star's radius: twice the radius, twice the time." markdown>
**2.** Same planet, same orbit, but the star is twice as wide. How many times longer is the dip?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(T\) is proportional to \(R_\star\): twice the star, twice the crossing time. (The depth, though, falls to a quarter, because depth goes with \(1 / R_\star^2\).)

</details>
</div>

<div class="tw-prob" data-answer="12" data-tol="0.05" data-unit="points" data-hints='{"6":"Two points per hour for 6 hours.","360":"That is minutes. One point every 30 minutes."}' data-why="6 hours at one point per 30 minutes gives 12 points." markdown>
**3.** Our planet's dip lasts about 6 hours, and the light curve has one point every 30 minutes. How many points does the dip hold? (Why this matters: it is how many points the dip's average uses, the N of lesson 1.4.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(6 \times 60 / 30 = 12\) points. With 2-minute data it would be 180 points, but each would collect 15 times less light and so be noisier by \(\sqrt{15}\); for pure photon noise the two effects cancel and the dip is no clearer. What faster points do give is the dip's shape: ingress and egress become visible instead of blurred.

</details>
</div>

<div class="tw-prob" data-answer="longer|long" data-why="Same direction means a slow relative speed, so the crossing takes longer." markdown>
**4.** Around two suns, the star happens to move in the same direction as the planet during a crossing. Is the dip longer or shorter than the still-star formula says? (One word.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**Longer.** The planet has to catch up with a star that is running away from it, so their relative speed is small and the crossing takes more time.

</details>
</div>

## Sources

- The duration formula and its assumptions (circular orbit, central crossing; the full form also has the planet's own size and the crossing's offset from the centre): Winn 2010, "Transits and Occultations" ([arXiv 1001.2010](https://arxiv.org/abs/1001.2010)).
- 1 AU = 215.03 Sun radii (IAU nominal solar radius 695,700 km; 1 AU = 149,597,871 km).
- Our planet's numbers: Kostov et al. 2021 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614)) for the masses and periods; the orbit size from Kepler's law (lesson 2.1); the 6-hour reading and the speeds of about 50 km/s are our own rough calculations from those numbers (15 Nov 2026), not values from the paper.
