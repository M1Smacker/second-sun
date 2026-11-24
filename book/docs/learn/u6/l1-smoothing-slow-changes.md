---
hide: [toc, footer]
title: "6.1 Smoothing out slow changes"
---

# Smoothing out slow changes

Stars wander. Our two-sun star drifts by about 0.1% over days (lesson 5.1), more than a small planet's whole dip. Before searching for dips, every search first divides out these slow changes. This plot shows what that does, done with a window half a day wide.

<div class="tw-plot" data-src="u6-smoothed"></div>

<p class="tw-plot__ask">The slow drift is gone, but look at the two eclipses: they used to remove 36% of the light. Touch their bottoms now. Before reading on, guess: where did the rest of the eclipse go?</p>

## The running median

The simplest way to follow a slow change: at each moment, take the **median** of all the measurements within a window around it, and divide by it. A slow drift is the same across the window, so it divides away. A short dip is only a small part of the window, so the median ignores it, and the dip survives.

<aside class="tw-mn" markdown>
**Running median.** For each moment, the middle value of the measurements in a window of fixed width centred on it. It follows changes slower than the window and ignores changes much shorter than it.
</aside>

The catch is in "much shorter". When a dip lasts as long as the window, the median falls into the dip and divides most of it away. The smoothing cannot tell a slow change from a long dip: it only knows how long each one lasts.

## Measured on our star

In sector 46 both visible eclipses are secondaries, each about 13 hours long (lesson 4.3). Our script divides the light by running medians of five widths and measures how much of each eclipse's depth survives:

| Window | Depth kept |
|---|---|
| 6 hours | 17% |
| 12 hours | 48% |
| 1 day | 91% |
| 2 days | 100% |
| 3 days | 100% |

A window shorter than the eclipse eats most of it; a window about twice as long as the eclipse keeps nearly all of it.

## Think it through

<div class="tw-prob" data-answer="48" data-tol="0.03" data-unit="percent" data-hints='{"52":"That is the part eaten. The question asks for the part kept."}' data-why="The 12-hour window keeps 48% of the eclipse's depth." markdown>
**a.** With the half-day (12-hour) window of the plot, what share of the eclipse's depth is kept, in percent?
</div>

!!! example "Worked example: the depth you would measure"
    The secondary eclipse is 35.8% deep. A 12-hour window keeps 48% of it.

    **Step 1. Multiply.** \(0.358 \times 0.48 = 0.172\).

    **Step 2.** After smoothing, the eclipse looks only **17% deep**: less than half its real depth.

!!! question "Your turn, half done: a planet's dip"
    A planet's dip 3,000 ppm deep, smoothed with a window that keeps 91% of a dip that long. Step 1: kept share 0.91. Finish: the depth after smoothing, in ppm.

<div class="tw-prob" data-answer="2730" data-tol="0.02" data-unit="ppm" data-hints='{"270":"That is the part lost. Multiply 3,000 by the kept share, 0.91."}' data-why="3,000 x 0.91 = 2,730 ppm." markdown>
**Your turn.** The depth after smoothing, in ppm:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(3{,}000 \times 0.91 = 2{,}730\) ppm. A shallower dip is harder to find, and a dip that seems shallower than it is would give a planet that seems smaller than it is.

The rule: **the smoothing window must be much longer than the dips you hope to find**.

</details>
</div>

## Why this matters for Second Sun

A planet around two stars can make long dips: crossing a star slowly takes many hours (lesson 4.4's 0.4-day dip lasted almost 10 hours). Petrova smooths with a 2-day window. Our filed measurement (FIX 11) found it keeps about 57% of a 20-hour dip's depth and 68% of a 15-hour dip's. A longer window would keep more, but follow the star's slow changes less well, leaving more of them to look like dips. Choosing the window is a trade, and like every Petrova setting it is fixed before a search and never tuned on its results.

## In a few sentences

Searches divide out a star's slow changes first, often with a running median: the middle value in a window around each moment. Changes slower than the window vanish; dips much shorter than it survive; dips as long as the window are eaten. On our star's 13-hour eclipses, windows of 6 hours, 12 hours, 1 day and 2 days keep 17%, 48%, 91% and 100% of the depth. The window must be much longer than the dips we hope to find.

## Problems

<div class="tw-prob" data-answer="26" data-tol="0.02" data-unit="hours" data-hints='{"13":"That is the eclipse itself. Keeping nearly all of it needed about twice its length."}' data-why="About twice the dip: 2 x 13 = 26 hours (our 1-day window kept 91%, the 2-day window 100%)." markdown>
**1.** As a rule of thumb from the table, a window about twice a dip's length keeps nearly all of it. For a 13-hour dip, about how many hours?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(2 \times 13 = 26\) hours. Our 1-day (24-hour) window kept 91%.

</details>
</div>

<div class="tw-prob" data-answer="no" data-hints='{"yes":"How deep did the eclipse look after a 6-hour window? 17% of its depth."}' data-why="A 6-hour window keeps only 17% of a 13-hour eclipse: most of the dip is divided away." markdown>
**2.** Would a 6-hour window be a good choice for finding 13-hour dips? (Yes or no.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**No.** It keeps only 17% of their depth.

</details>
</div>

## Sources

- Our measurement (`book/tools/lesson_plots_u6a.py`, 24 Nov 2026): TESS sector 46 SPOC 2-minute light of TIC 172900988 (MAST), divided by centred running medians 0.25, 0.5, 1, 2 and 3 days wide; depth kept 0.17, 0.48, 0.91, 1.00, 1.00 for the two 13-hour secondary eclipses. The script finds eclipses by their depth and stops unless the kept share rises with the window, a 6-hour window keeps under half and a 2-day window over 90%. (Its first version wrongly took the deepest visible dip for the primary eclipse; in sector 46 the primary falls inside the data-sending hole of lesson 5.2.)
- Petrova's 2-day window and the 57% and 68% kept for 20-hour and 15-hour dips: our fix queue, FIX 11 (`research/stage3/FIX-QUEUE.md`).
