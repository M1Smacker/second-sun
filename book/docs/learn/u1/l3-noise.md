---
hide: [toc, footer]
title: "1.3 Noise: the spread of the points"
---

# Noise: the spread of the points

One quiet day of our star pair, every 2-minute point. No eclipse happens on this day.

<div class="tw-plot" data-src="u1-quiet-day"></div>

<p class="tw-plot__ask">If no eclipse is happening, why are the points not all on one line? Read the highest and the lowest point.</p>

## Where the spread comes from

Every measurement has a little error in it. Light arrives as single particles, photons, and in any 2 minutes a few more or a few fewer land on the camera, just by chance. The camera adds its own small errors. The spacecraft wobbles very slightly. The stars themselves flicker a little. All of this together is called **noise**.

<aside class="tw-mn" markdown>
**Noise.** Changes in the measured light that are not the signal we are looking for.
</aside>

To compare noise between stars we need one number for "how spread out are the points". The usual one is the **standard deviation**, written \(\sigma\) (the Greek letter sigma). In words: how far, on a typical day, a point lies from the average.

<aside class="tw-mn" markdown>
**Standard deviation (\(\sigma\)).** Roughly, the typical distance of the points from their average. For the bell-shaped noise most measurements have, about two thirds of the points lie within one \(\sigma\) of it.
</aside>

The recipe has four steps. Find the average. Subtract it from every point. Square those differences (so minus and plus both count, and big misses count extra). Average the squares, then take the square root to get back to the original units:

\[ \sigma = \sqrt{ \frac{ (x_1 - \bar{x})^2 + (x_2 - \bar{x})^2 + \dots + (x_N - \bar{x})^2 }{ N } } \]

<aside class="tw-mn" markdown>
**\(\bar{x}\).** Read "x bar": the average of the values. \(N\) is how many values there are. Some books divide by \(N - 1\) instead of \(N\); for many points the difference is tiny.
</aside>

!!! example "Worked example: five points"
    Five points of a light curve, as \(F / F_{\text{normal}}\): 1.0010, 0.9990, 1.0005, 0.9995, 1.0000.

    **Step 1. Average.** They add up to 5.0000, so \(\bar{x} = 1.0000\).

    **Step 2. Differences.** +0.0010, -0.0010, +0.0005, -0.0005 and 0.

    **Step 3. Squares.** 0.000001, 0.000001, 0.00000025, 0.00000025 and 0. Their sum is 0.0000025.

    **Step 4. Average, then square root.** \(0.0000025 / 5 = 0.0000005\), and \(\sqrt{0.0000005} = 0.000707\).

    So \(\sigma = 0.000707\), which is 707 ppm.

For the quiet day in the plot above, our script does the same sum over all 720 points and gets \(\sigma \approx 930\) ppm. (A slow drift across the day, which you will meet below, is part of that number.) A single point can easily be 930 ppm off. Compare that with the dips from the last lesson: an Earth-sized planet around a star like these makes a dip far under 100 ppm. In one point, it would be lost.

## Averaging beats noise

Here is the way out. If the errors are random and independent (each point's error has nothing to do with its neighbours'), they partly cancel when you average several points: some are too high, some too low. Average \(N\) points and the noise of the average shrinks by the square root of \(N\):

\[ \sigma_{\text{average}} = \frac{\sigma}{\sqrt{N}} \]

<aside class="tw-mn" markdown>
**Why a square root?** Random errors add up more slowly than the points do. Four points do not cancel four times the noise, only twice: \(\sqrt{4} = 2\).
</aside>

Look at the same day again, now with every 15 points (30 minutes) averaged into one:

<div class="tw-plot" data-src="u1-quiet-day-30"></div>

<p class="tw-plot__ask">How much tighter is this than the plot at the top? Compare the highest and lowest points.</p>

!!! example "Worked example: what averaging should give"
    **Step 1.** Noise of one 2-minute point: about 930 ppm.

    **Step 2.** A 30-minute average holds \(N = 15\) points, and \(\sqrt{15} = 3.87\).

    **Step 3.** Expected noise of the average: \(930 / 3.87 = 240\) ppm.

    Our script measured the real 30-minute averages of this day: 357 ppm. Bigger than the 240 the rule promised.

Why bigger? Because not all of the change is independent from one point to the next. Across this day the light drifts slowly, by about 940 ppm from start to end, almost a tenth of a percent. Averaging 15 neighbouring points cannot cancel a drift that all 15 share. Watch what happens when our script first removes a straight-line drift from the day: the 30-minute averages then scatter by 233 ppm, and the rule, applied to the same drift-free points, predicts 231 ppm. Once the shared drift is gone, averaging works exactly as promised.

<aside class="tw-mn" markdown>
**White and red noise.** Noise that changes independently from point to point is called white noise. Slow wobbles shared by neighbouring points are called red noise. Averaging cleans the first quickly and the second only slowly.
</aside>

That slow, shared part has a name: **red noise**. What causes this day's drift (the stars themselves, the spacecraft, or both) we have not measured. Red noise was one of the reasons early planet searches from the ground found fewer planets than simple counts predicted, and it is why, in Unit 5, our search first takes slow changes out of the light before it looks for dips.

!!! question "Your turn, half done: one hour"
    One hour of 2-minute points holds \(N = 30\) points, and \(\sqrt{30} = 5.48\). Finish it: with 930 ppm per point, what noise does the rule predict for a one-hour average?

<div class="tw-prob" data-answer="170" data-tol="0.02" data-unit="ppm" data-hints='{"31":"Divide by the square root of 30, not by 30.","27900":"Averaging makes noise smaller, not bigger: divide."}' data-why="930 / 5.48 = 170 ppm, if the noise were all white." markdown>
**Your turn.** The rule's prediction for a one-hour average, in ppm:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(930 / \sqrt{30} = 930 / 5.48 = 170\) ppm.

The rule: **noise of an average is \(\sigma / \sqrt{N}\)**, but only for independent noise. Our script finds the real one-hour averages of this day scatter by about 320 ppm, far above 170, because of the slow drift.

</details>
</div>

## In a few sentences

Every light curve scatters, even when nothing happens; we measure the scatter with the standard deviation \(\sigma\). Averaging \(N\) points shrinks independent noise by \(\sqrt{N}\), which is how tiny dips become visible. Slow, shared wobbles (red noise) average away only slowly, so searches usually take them out first.

## Problems

<div class="tw-prob" data-answer="200" data-tol="0.01" data-unit="ppm" data-hints='{"40":"Divide by the square root of 25 (that is 5), not by 25.","1000":"Averaging helps: divide by the square root of N."}' data-why="The square root of 25 is 5, and 1,000 / 5 = 200 ppm." markdown>
**1.** The noise of one point is 1,000 ppm. What is the noise of an average of 25 points, if the noise is all random?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(\sqrt{25} = 5\), so \(1{,}000 / 5 = 200\) ppm.

</details>
</div>

<div class="tw-prob" data-answer="16" data-abs="0" data-hints='{"4":"Averaging 4 points only halves the noise. You need it four times smaller.","8":"Noise falls with the square root: to divide it by 4 you need 4 squared points."}' data-why="To shrink noise 4 times you need the square root of N to be 4, so N = 16." markdown>
**2.** How many points must you average to bring 1,200 ppm of random noise down to 300 ppm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

You need the noise 4 times smaller (\(1{,}200 / 300 = 4\)). Noise falls as \(\sqrt{N}\), so \(\sqrt{N} = 4\) and \(N = 4^2 = 16\) points.

Notice the price: halving the noise costs four times the points. That is why faint signals need so much data.

</details>
</div>

<div class="tw-prob" data-answer="1414" data-tol="0.02" data-unit="ppm" data-hints='{"1633":"You divided by N minus 1. This problem divides by N, as the formula above does."}' data-why="Average 1.000; squares of the differences 0.000004, 0.000004, 0, 0; their average 0.000002; square root 0.001414 = 1,414 ppm." markdown>
**3.** Four points: 0.998, 1.002, 1.000, 1.000. What is their standard deviation, in ppm? (Divide by \(N\).)

<details class="tw-sol" markdown><summary>Worked solution</summary>

Average: \(4.000 / 4 = 1.000\). Differences: -0.002, +0.002, 0 and 0. Squares: 0.000004, 0.000004, 0 and 0, sum 0.000008. Divide by 4: \(0.000002\). Square root: \(0.001414\), which is 1,414 ppm.

(Dividing by \(N - 1 = 3\) instead gives 1,633 ppm. That version is used when the points are a sample and you want to estimate the spread of everything they came from; with only four points the two differ a lot, with hundreds hardly at all.)

</details>
</div>

<div class="tw-prob" data-answer="red" data-why="Slow, shared wobbles are red noise; averaging neighbouring points cannot cancel them." markdown>
**4.** A light curve drifts slowly up and down over several hours. Averaging neighbouring points barely reduces it. In one word, what colour of noise is it?

<details class="tw-sol" markdown><summary>Worked solution</summary>

**Red.** Red noise is slow and shared by neighbouring points, so averaging them together hardly cancels it; only averages over much longer stretches, or taking the slow change out, help. White noise changes independently from one point to the next, and averaging cancels it quickly.

</details>
</div>

## Sources

- Noise numbers: one quiet day (720 points) of TIC 172900988, TESS sector 44, 2-minute light curve; measured by our script `book/tools/lesson_plots.py` and a check script run on 15 Nov 2026 (930 ppm per point; 357 ppm for 30-minute averages; drift about 940 ppm across the day; 233 ppm for 30-minute averages after removing a straight line, against 231 ppm predicted; 320 ppm for one-hour averages). Every number re-derived independently by Codex (brief 017, 15 Nov 2026), which also caught that the first version of this lesson averaged with medians while comparing against the rule for plain averages.
- Red noise and planet searches: Pont, Zucker and Queloz 2006, "The effect of red noise on planetary transit detection" ([arXiv astro-ph/0608597](https://arxiv.org/abs/astro-ph/0608597)): survey yield predictions "assume uncorrelated noise", and red noise effects "cannot be neglected in typical ground-based surveys".
