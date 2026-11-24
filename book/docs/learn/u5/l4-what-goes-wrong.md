---
hide: [toc, footer]
title: "5.4 What goes wrong"
---

# What goes wrong

A light curve looks like a clean record of a star. Behind it is a spacecraft that turns, fires thrusters, and sometimes looks almost straight at Earth and the Moon. This is the sky behind our star in sector 46: the background light in its 20 aperture pixels.

<div class="tw-plot" data-src="u5-background"></div>

<p class="tw-plot__ask">Most of the time the background sits near 2,500 electrons per second. Then it leaps more than tenfold. Before reading on, guess: what could light up the sky behind a star for hours?</p>

## Light that should not be there

TESS's cameras look out into space, but parts of each orbit bring Earth and the Moon close to where they point. Their light bounces inside the camera hoods and spreads across the images: **scattered light**. On the plot it is the surges, up to 29,166 electrons per second at day 0.45, about twelve times the usual sky. The pipeline subtracts the background, but when the background is huge and changing fast, small errors in it become large errors in the star's light.

<aside class="tw-mn" markdown>
**Quality flag.** A marker stored beside each 2-minute measurement, saying what was going on: pointing at Earth, scattered light, a thruster firing, a bad calibration. Measurements with any flag set are usually left out.
</aside>

## What the file admits

Every TESS light curve carries a quality flag for every measurement. In sector 46 of our star, 2,825 of 19,542 measurements are flagged, 14.5%:

| Flag | Measurements | Hours | What it means |
|---|---|---|---|
| Earth point | 1,004 | 33.5 | pointing at Earth to send the data home (lesson 5.2's hole): no light recorded at all |
| Scattered light | 1,102 | 36.7 | the surges on the plot |
| Manual exclude | 376 | 12.5 | marked bad by the mission team |
| Bad calibration | 306 | 10.2 | the pixels could not be calibrated |
| Too few stars to correct | 177 | 5.9 | the trend removal (lesson 5.3) lacked reference stars |
| Argabrightening | 25 | 0.8 | a brief brightening of the whole image |
| Momentum dump | 22 | 0.7 | thrusters fired to slow the pointing wheels |
| Pointing tweaks | 8 | 0.3 | small corrections of the pointing |

(Some measurements carry two flags, so the rows add up to more than 2,825.)

## Think it through

<div class="tw-prob" data-answer="11.8|12|11.75" data-tol="0.04" data-hints='{"0.085":"Upside down: the surge divided by the usual level, 29,166 / 2,482."}' data-why="29,166 / 2,482 = 11.8: the background rose almost twelvefold." markdown>
**a.** The usual background is 2,482 and the highest surge 29,166 electrons per second. How many times the usual level is that?
</div>

!!! example "Worked example: how much is left out"
    Sector 46 has 19,542 measurements, of which 2,825 are flagged.

    **Step 1. The share flagged.** \(2{,}825 / 19{,}542 = 0.145\).

    **Step 2. In days.** Each measurement is 2 minutes: \(2{,}825 \times 2 = 5{,}650\) minutes, or 3.9 days.

    **Step 3.** About **15%**, nearly 4 days of a 27-day sector, is set aside before any search.

!!! question "Your turn, half done: the momentum dumps"
    TESS fired its thrusters to unload momentum at days 0, 6.5, 14.5 and 20.7 of the sector. Step 1: the gaps between them are 6.5, 8.0 and 6.2 days. Finish: the average gap, in days.

<div class="tw-prob" data-answer="6.9" data-tol="0.03" data-unit="days" data-hints='{"20.7":"That is the total. Divide by the 3 gaps."}' data-why="(6.5 + 8.0 + 6.2) / 3 = 6.9 days." markdown>
**Your turn.** The average gap between dumps, in days:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\((6.5 + 8.0 + 6.2) / 3 = 20.7 / 3 = 6.9\) days. A dump comes roughly once a week, and each one nudges the pointing a little, which can leave a small step in a star's light.

The rule: **every sector has holes, surges and steps, and the flags say where**.

</details>
</div>

## Why this matters for Second Sun

These are exactly the places where Petrova's false alarms live. Next to the holes, the dumps and the steps, a search sees more fake dips than fake bumps, and the upside-down test (Unit 6) cannot catch them, because flipping the light turns a fake dip into a fake bump that the search then ignores. Our measurements (22 Nov) found this is the main thing blocking the next gain in how many planets Petrova catches. Leaving out flagged measurements removes much of the trouble, but not all: the unflagged edges just beside a flagged stretch are where it lingers.

## In a few sentences

A TESS light curve hides a busy spacecraft: it points at Earth to send data, it fires thrusters about once a week, and scattered light from Earth and the Moon floods the images for hours. Each measurement carries a quality flag; in our sector 46, 14.5% are flagged, nearly 4 days, mostly the data-sending hole and scattered light that raised the background twelvefold. Searches leave flagged data out, but fake dips still gather next to the holes, dumps and steps.

## Problems

<div class="tw-prob" data-answer="33.5|33" data-tol="0.03" data-unit="hours" data-hints='{"2008":"That is in minutes. Divide by 60."}' data-why="1,004 x 2 = 2,008 minutes = 33.5 hours." markdown>
**1.** The Earth-point flag covers 1,004 measurements, one every 2 minutes. How many hours is that?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(1{,}004 \times 2 = 2{,}008\) minutes, and \(2{,}008 / 60 = 33.5\) hours: lesson 5.2's 1.39-day hole.

</details>
</div>

<div class="tw-prob" data-answer="85.5|85" data-tol="0.02" data-unit="percent" data-hints='{"14.5":"That is the share flagged. The question asks for the share kept."}' data-why="100% - 14.5% = 85.5% kept." markdown>
**2.** 14.5% of the sector's measurements are flagged. What share is kept for the search, in percent?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(100 - 14.5 = 85.5\%\).

</details>
</div>

<div class="tw-prob" data-answer="bump|a bump|bumps" data-hints='{"dip":"Flip the light upside down: what does a dip become?"}' data-why="Flipping the light turns a dip into a bump, which the dip search ignores." markdown>
**3.** The upside-down test flips the light. A fake dip next to a hole becomes what? (One word.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**A bump**, which a search for dips ignores. So the upside-down copy cannot show how many fake dips the holes make.

</details>
</div>

## Sources

- Our file (`book/tools/lesson_plots_u5d.py`, 24 Nov 2026): TESS sector 46 SPOC 2-minute light curve of TIC 172900988 from MAST: QUALITY and SAP_BKG columns read directly; flag names from the installed lightkurve 2.6 (TessQualityFlags). The script stops unless the flagged share is 5% to 30%, the Earth-point measurements hold no light, and the background's peak sits on a scattered-light flag.
- Scattered light from Earth and the Moon, and the hoods that reduce it: NASA HEASARC, TESS Telescope Information (read 24 Nov 2026). Argabrightenings among the errors a pipeline must handle: Stumpe et al. 2012 ([arXiv 1203.1382](https://arxiv.org/abs/1203.1382)).
- Fake dips next to gaps, dumps and steps outnumbering fake bumps: our own measurement, `research/stage3/rs041/P75-REESTIMATE-2026-11-22.md`.
