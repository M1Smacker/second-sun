---
hide: [toc, footer]
title: "4.5 The stability limit, and why they are rare"
---

# The stability limit, and why they are rare

A planet cannot circle two stars just anywhere. Too close, and the pair's changing pull throws it out. This plot shows how far out the safe zone starts, for a pair with nearly equal masses like ours, in units of the stars' own orbit size.

<div class="tw-plot" data-src="u4-stability"></div>

<p class="tw-plot__ask">The more stretched the stars' orbit, the farther out the edge. Touch the plot at our pair's stretch, 0.448. Before reading on, guess: our planet orbits at 0.9 AU and the stars' orbit is 0.192 AU. Is it safely outside?</p>

## Why there is an edge

Far from the pair, a planet feels the two stars almost as one star of their total mass (lesson 4.4). Close in, it does not: as the stars swing round, the pull on the planet keeps changing direction and strength, every 19.66 days. Each change is a small kick. Far out, the kicks are weak and cancel over time. Close in, they add up, the orbit becomes chaotic, and the planet is thrown out of the system or into a star.

<aside class="tw-mn" markdown>
**Critical orbit \(a_{\text{crit}}\).** The smallest orbit around both stars on which a planet survives for a long time. Inside it, computer simulations lose their planets; outside, they keep them.
</aside>

Holman and Wiegert ran many such simulations in 1999 and fitted a rule for the edge. It depends on two things: the stretch \(e\) of the stars' orbit, and how the mass is shared, \(\mu = M_2 / (M_1 + M_2)\). For two equal stars on a circle the edge sits at about 2.4 times the stars' orbit. A stretched orbit brings the stars closer to the planet at one end, so the edge moves out: at our pair's 0.448, to 3.5 times.

## Think it through

<div class="tw-prob" data-answer="3.52|3.5|3.516" data-tol="0.03" data-hints='{"2.39":"That is a circular orbit. Read the plot at e = 0.448."}' data-why="The plot at e = 0.448 reads 3.516: the edge is 3.5 times the stars' own orbit." markdown>
**a.** Touch the plot at a stretch of 0.448. How many times the stars' orbit is the edge?
</div>

!!! example "Worked example: where the edge is for our pair"
    The stars' orbit is 0.192 AU (lesson 4.2) and the edge is 3.516 times that.

    **Step 1. The edge in AU.** \(3.516 \times 0.192 = 0.675\) AU.

    **Step 2. Compare the planet.** It orbits at 0.901 AU: \(0.901 / 0.675 = 1.34\).

    **Step 3.** The planet is **1.34 times** farther out than the edge: safe, but not by much. Kostov et al. 2021 give the same 1.34.

!!! question "Your turn, half done: the shortest safe period"
    Kepler's third law with the pair's total mass, 2.44 Suns (lesson 2.1): \(P^2 = a^3 / M\), with \(P\) in years and \(a\) in AU. Step 1: \(0.675^3 = 0.3075\), and \(0.3075 / 2.44 = 0.126\). Finish: the period at the edge, in days.

<div class="tw-prob" data-answer="129.7|130|129.6" data-tol="0.02" data-unit="days" data-hints='{"0.355":"That is in years. Multiply by 365.25.","0.126":"That is P squared. Take the square root first."}' data-why="The square root of 0.126 is 0.355 years; 0.355 x 365.25 = 129.7 days." markdown>
**Your turn.** The shortest safe period, in days:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(\sqrt{0.126} = 0.355\) years, and \(0.355 \times 365.25 = 129.7\) days, the value in Kostov et al. 2021. The planet's real period, about 200 days, is 1.55 times longer.

The rule: **the edge is a few times the stars' orbit, more for a stretched orbit**.

</details>
</div>

## Living near the edge

Most planets found around two stars orbit close to this edge, as TIC 172900988 b does (Kostov et al. 2021 show the known ones bunched just outside it). For a planet hunt that is good news and bad news. Good, because the closest orbits give the shortest periods and the most crossings. Bad, because close to the edge the planet feels the stars' pull the most, so its orbit turns fastest and its crossings come and go (lesson 4.4's broken clock).

## Why they are rare around the closest pairs

Kepler found circumbinary planets only around pairs with periods longer than 7 days, although most of Kepler's eclipsing binaries are faster than that (Martin, Mazeh and Fabrycky 2015). Armstrong et al. 2014 confirmed the shortage is real, not a search effect. One proposed explanation: many of the tightest pairs were squeezed into their small orbits by a distant third star, and that slow squeezing also disturbs or prevents planets around them. It is a proposal, not settled.

Around slower pairs, planets are not rare at all. Armstrong et al. 2014 measured that about 10% of binaries have a planet bigger than 6 Earth radii with an orbit under 300 days (somewhere between 3.5% and 28%, if the planets' orbits lie flat with the stars', as the known ones do). That is about as common as around single stars.

## Why this matters for Second Sun

Our hunt lists keep only pairs with periods over 5 days (G3 over 7), and the Census plan does the same: the closest pairs, which are most of the catalogues, are where Kepler found none. And every planet we hope to find must live outside its pair's edge, at a few times the stars' orbit, which sets the shortest planet period worth searching for each star.

## In a few sentences

A planet around two stars survives only outside a critical orbit, where the pair's changing pull is weak: about 2.4 times the stars' orbit for an equal circular pair, 3.5 times for our stretched one. TIC 172900988 b orbits 1.34 times outside its edge (period 200 days against 130), like most known circumbinary planets, which sit near the edge. Kepler found none around pairs faster than 7 days, and about 10% around slower pairs, which is why our searches keep only the slower pairs.

## Problems

<div class="tw-prob" data-answer="0.239|0.24" data-tol="0.03" data-unit="AU" data-hints='{"2.39":"That is the edge in units of the stars orbit. Multiply by 0.1 AU."}' data-why="2.39 x 0.1 AU = 0.239 AU." markdown>
**1.** Two equal stars on a circle, 0.1 AU apart. The edge is 2.39 times their orbit. Where is it, in AU?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(2.39 \times 0.1 = 0.239\) AU. Any planet must orbit farther out than that.

</details>
</div>

<div class="tw-prob" data-answer="no" data-hints='{"yes":"Compare it with the edge, 0.675 AU."}' data-why="0.5 AU is inside the 0.675 AU edge: the pair's changing pull would throw the planet out." markdown>
**2.** Could a planet survive around our pair at 0.5 AU? (Yes or no.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**No.** 0.5 AU is inside the edge at 0.675 AU, where simulated planets do not last.

</details>
</div>

<div class="tw-prob" data-answer="140" data-tol="0.03" data-hints='{"14":"10% is a tenth: 1,400 / 10."}' data-why="10% of 1,400 = 140." markdown>
**3.** If 10% of slow binaries have a planet bigger than 6 Earth radii with an orbit under 300 days, how many of 1,400 such binaries would?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(0.10 \times 1{,}400 = 140\). Only a small share of those cross their stars as seen from Earth, and only some of the time (lesson 4.4), which is why a hunt needs many stars.

</details>
</div>

<div class="tw-prob" data-answer="7" data-tol="0.01" data-unit="days" data-why="Kepler's circumbinary planets all orbit pairs with periods longer than 7 days (Martin, Mazeh and Fabrycky 2015)." markdown>
**4.** Kepler found circumbinary planets only around pairs slower than how many days?

<details class="tw-sol" markdown><summary>Worked solution</summary>

**7 days**: none around the many faster pairs, which is why our hunts skip them.

</details>
</div>

## Sources

- The edge: Holman and Wiegert 1999, "Long-term stability of planets in binary systems", AJ 117, 621 to 628 ([arXiv astro-ph/9809315](https://arxiv.org/abs/astro-ph/9809315)): the fitted rule for the critical orbit. Our script `book/tools/lesson_plots_u4d.py` (24 Nov 2026) draws it for mass share 0.4925 and stops unless it reproduces Kostov et al.'s numbers below (it gives 1.335 and 129.6 days).
- The system: Kostov et al. 2021, AJ 162, 234 ([arXiv 2105.08614](https://arxiv.org/abs/2105.08614), HTML read 24 Nov 2026): the planet is close to the critical radius, "a/a_crit = 1.34 (P/P_crit = 1.55)", using Holman and Wiegert's approximation; the critical period 129.7 days; the known circumbinary planets bunched near their critical orbits (their Figure 27).
- None around the tightest pairs: Martin, Mazeh and Fabrycky 2015, "No circumbinary planets transiting the tightest Kepler binaries" ([arXiv 1505.05749](https://arxiv.org/abs/1505.05749), abstract read 24 Nov 2026): the Kepler circumbinary systems are "all found around eclipsing binaries with periods greater than 7 d"; the third-star explanation is theirs.
- How common: Armstrong et al. 2014, "On the abundance of circumbinary planets" ([arXiv 1404.5617](https://arxiv.org/abs/1404.5617), abstract read 24 Nov 2026): 10.0% (+18, -6.5; 95% limits) for planets bigger than 6 Earth radii with periods under 300 days if they orbit flat with their stars; the shortage around shorter-period binaries "a real effect".
