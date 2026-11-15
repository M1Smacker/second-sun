---
hide: [navigation, toc, footer]
title: "1.4 What a dip looks like"
---

# What a dip looks like

This is the moment the whole project is about. Below is the planet around TIC 172900988, caught by TESS in sector 21 (January and February 2020) as it crossed in front of one of its two suns.

<div class="tw-plot" data-src="u1-planet-b"></div>

<p class="tw-plot__ask">Find the dip. Read its lowest points. How long, in hours, does the light stay low?</p>

## The shape of a planet's dip

Lesson 1.2 said a planet blocks the fraction \((R_p / R_\star)^2\) of its star's light. That is the depth at the deepest part. But the planet does not jump onto the star's face. It slides on, crosses, and slides off, and each part leaves its mark on the light:

<figure class="tw-diagram">
<svg viewBox="0 0 640 210" role="img" aria-label="The shape of a transit: the light is flat, slopes down while the planet moves onto the star, stays flat while it is fully in front, slopes back up as it leaves.">
  <line x1="40" y1="60" x2="620" y2="60" class="tw-d-axis"/>
  <polyline points="40,60 210,60 250,140 410,140 450,60 620,60" class="tw-d-line"/>
  <text x="218" y="118" text-anchor="end" class="tw-d-txt">ingress</text>
  <text x="330" y="184" text-anchor="middle" class="tw-d-txt">flat bottom</text>
  <text x="444" y="118" text-anchor="start" class="tw-d-txt">egress</text>
  <text x="125" y="44" text-anchor="middle" class="tw-d-txt">normal light</text>
  <line x1="600" y1="60" x2="600" y2="140" class="tw-d-dim"/>
  <text x="612" y="178" text-anchor="end" class="tw-d-txt">depth</text>
</svg>
<figcaption>A planet's dip, drawn clean. Real dips are rounder at the corners, because a star's edge is a little darker than its centre.</figcaption>
</figure>

**Ingress** is the slope down: the planet's disc is only partly in front of the star. Once the whole disc is in front, the light stays at its lowest level: the **flat bottom**. **Egress** is the slope back up as the planet leaves. Because a planet is small next to its star, ingress and egress are short and the flat bottom is long. That box-like shape, with short sloping sides, is the signature of a small body crossing a big one.

<aside class="tw-mn" markdown>
**Ingress and egress.** The start and the end of a crossing, while the planet's disc is only partly in front of the star. Both are Latin: "going in" and "going out".
</aside>

Now go back to the eclipse in lesson 1.1. Its bottom is a point, not a flat line: our script finds only 2 of its 10-minute points within 1 percentage point of the lowest one. Two stars of nearly the same size never fit one inside the other, so the hidden part grows and shrinks without ever staying still. A **V shape** usually means two stars; a **U or box shape** with a flat bottom usually means something much smaller than its star. Planet searches use this difference all the time to throw out eclipsing stars that pretend to be planets.

<aside class="tw-mn" markdown>
**V or U.** A rule of thumb, not a law: a planet that only grazes the edge of its star also makes a V. Unit 5 shows how searches handle that.
</aside>

## Seeing a dip through the noise

Look at the plot again. The points outside the dip scatter by a few hundred ppm: our script measures a spread of \(\sigma = 305\) ppm per 30-minute point. A single point 600 ppm low would mean nothing. Yet the dip is plain to see. Why?

Because it is not one low point. It is many low points in a row. Lesson 1.3 showed that averaging \(N\) points shrinks random noise to \(\sigma / \sqrt{N}\). The dip is a stretch of points that all sit low together, and their average is far below normal, with very little noise left. Astronomers compare the two with one number, the **signal-to-noise ratio**:

\[ \text{SNR} = \frac{\text{depth}}{\sigma / \sqrt{N}} \]

<aside class="tw-mn" markdown>
**Signal-to-noise ratio (SNR).** How many times bigger a signal is than the noise left after averaging. Searches usually ask for about 7 or more before they look twice.
</aside>

where depth is the average drop of the points inside the dip, \(\sigma\) is the noise of one point, and \(N\) is how many points the dip holds.

!!! example "Worked example: how clear is the planet's dip?"
    Our script measured this dip (the second one in sector 21) from its 12 points within 3.6 hours of the middle.

    **Step 1. Depth.** Their average is 2,655 ppm below normal.

    **Step 2. Noise of one point.** Outside the dip, \(\sigma = 305\) ppm.

    **Step 3. Noise of the average of 12 points.** \(\sqrt{12} = 3.46\), so \(305 / 3.46 = 88\) ppm.

    **Step 4. Divide.** \(\text{SNR} = 2{,}655 / 88 = 30\).

    The dip is 30 times bigger than the noise left in its average. That is a strong signal: no honest search would miss it. Yet notice: that same planet in a single point would be lost in the noise. All of the power comes from \(\sqrt{N}\).

The depth also matches lesson 1.2. There we worked out 5,560 ppm for this planet in front of the larger star if the other star were not there, and said the second star's light would roughly halve it. 2,000 to 3,000 ppm is what TESS saw.

## The other crossing

Five days earlier the same planet crossed the other star. Here it is:

<div class="tw-plot" data-src="u1-planet-a"></div>

<p class="tw-plot__ask">Is this dip deeper or shallower than the first plot? Does its bottom look flat?</p>

Two dips, 4.9 days apart, from one planet crossing two different suns. With one star, a planet's dips repeat like a clock, every orbit. Around two suns that clock breaks: the stars move while the planet goes round, so the planet meets them at different places each time. The dips change their spacing, their depth and their length. That is what makes planets around two suns so hard to find, and so precious when found. Unit 3 is all about it.

!!! question "Your turn, half done: the first crossing"
    In the first crossing our script finds a depth of about 1,900 ppm over 14 points. Take the same noise as before, 305 ppm per point. Step 1: \(\sqrt{14} = 3.74\). Finish the other steps and type the SNR.

<div class="tw-prob" data-answer="23.3" data-tol="0.05" data-hints='{"6.2":"You divided the depth by the noise of one point. Divide by the noise of the average: 305 / 3.74 first.","0.04":"Upside down: depth on top, noise below."}' data-why="305 / 3.74 = 81.6 ppm; 1,900 / 81.6 = 23.3." markdown>
**Your turn.** SNR of the first crossing:

<details class="tw-sol" markdown><summary>Worked solution</summary>

Step 2: noise of the average, \(305 / 3.74 = 81.6\) ppm. Step 3: \(\text{SNR} = 1{,}900 / 81.6 = 23.3\).

The rule: **SNR is depth over the noise of the average, \(\sigma / \sqrt{N}\).** Still far above 7: a clear detection.

</details>
</div>

## In a few sentences

A planet's dip has a short slope down (ingress), a flat bottom and a short slope up (egress); two stars eclipsing each other usually make a V instead. A dip is seen through noise because many low points in a row average down the noise: the signal-to-noise ratio, depth over \(\sigma / \sqrt{N}\), says how clear it is. Around two suns, a planet's dips do not repeat like a clock, which is why they are hard to find.

## Problems

<div class="tw-prob" data-answer="20" data-tol="0.02" data-hints='{"5":"Divide by the noise of the average (400 / 4 = 100), not by the noise of one point.","80":"Divide by the square root of 16, which is 4."}' data-why="400 / 4 = 100 ppm, and 2,000 / 100 = 20." markdown>
**1.** A dip is 2,000 ppm deep and holds 16 points. The noise of one point is 400 ppm. What is its SNR?

<details class="tw-sol" markdown><summary>Worked solution</summary>

Noise of the average: \(400 / \sqrt{16} = 400 / 4 = 100\) ppm. SNR: \(2{,}000 / 100 = 20\).

</details>
</div>

<div class="tw-prob" data-answer="12" data-abs="0" data-hints='{"180":"That is minutes over points. One point every 30 minutes means 2 points per hour.","3":"Two points per hour, for 6 hours."}' data-why="6 hours has 360 minutes, and 360 / 30 = 12." markdown>
**2.** A dip lasts 6 hours. The light curve has one point every 30 minutes. How many points fall inside the dip?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(6 \times 60 = 360\) minutes, and \(360 / 30 = 12\) points.

</details>
</div>

<div class="tw-prob" data-answer="7.09" data-tol="0.03" data-unit="Earth widths" data-hints='{"0.05":"That is the planet compared with the star. Multiply by the star size in Earth widths.","0.0025":"That is the depth as a fraction. Take its square root first."}' data-why="The square root of 0.0025 is 0.05; the star is 1.3 times 109.08 = 141.8 Earths wide; 0.05 times 141.8 = 7.09." markdown>
**3.** A dip is 2,500 ppm deep. The star is 1.3 times as wide as the Sun, and no second star dilutes the light. How many times wider than the Earth is the planet?

<details class="tw-sol" markdown><summary>Worked solution</summary>

Run lesson 1.2 backwards. Depth as a fraction: \(2{,}500 / 1{,}000{,}000 = 0.0025\). Since depth is \((R_p / R_\star)^2\), the ratio is its square root: \(\sqrt{0.0025} = 0.05\). The star is \(1.3 \times 109.08 = 141.8\) Earths wide, so the planet is \(0.05 \times 141.8 = 7.09\) Earths wide: between Neptune (3.9 Earths) and Saturn (9.4 Earths) in size.

</details>
</div>

<div class="tw-prob" data-answer="700" data-tol="0.01" data-unit="ppm" data-hints='{"7":"SNR = depth / noise, so depth = SNR times noise.","70":"Use the noise of the average, 100 ppm, times 7."}' data-why="Depth = SNR times the noise of the average = 7 times 100 = 700 ppm." markdown>
**4.** A search only looks twice at dips with SNR of 7 or more. For one star, the noise of the average over a dip's length is 100 ppm. What is the shallowest dip the search will notice?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(\text{SNR} = \text{depth} / \text{noise}\), so \(\text{depth} = \text{SNR} \times \text{noise} = 7 \times 100 = 700\) ppm. Anything shallower is lost, however real it is. Measuring exactly what a search can and cannot see is a whole part of this project (Unit 5).

</details>
</div>

<div class="tw-prob" data-answer="ingress" data-why="Ingress is the slope down at the start of a crossing; egress is the slope back up." markdown>
**5.** In one word: what is the short slope down at the start of a planet's dip called?

<details class="tw-sol" markdown><summary>Worked solution</summary>

**Ingress**, while the planet's disc moves onto the star. The slope up at the end is **egress**.

</details>
</div>

## Sources

- The planet's dips: TESS sector 21, QLP full-frame light curve of TIC 172900988 (30-minute points), from MAST; times, depths and noise measured by our scripts on 15 Nov 2026 (`book/tools/lesson_plots.py` and a check script): dips at day 1883.39 and 1888.31 on the TESS clock, 4.9 days apart; 305 ppm per point outside the second dip.
- The system: Kostov et al. 2021 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614)): "During Sector 21, the planet TIC 172900988b transited the primary star and then 5 days later it transited the secondary star."
- Transit shape (ingress, egress, flat bottom, darker star edges): Winn 2010, "Transits and Occultations" ([arXiv 1001.2010](https://arxiv.org/abs/1001.2010)).
