---
hide: [toc, footer]
title: "5.2 How TESS watches the sky"
---

# How TESS watches the sky

Every light curve in this course came from TESS. Here is one whole stretch of its watching: about 26 days of our two-sun star, with a hole in the middle.

<div class="tw-plot" data-src="u5-one-sector"></div>

<p class="tw-plot__ask">Why does a space telescope, with no clouds and no daytime, stop watching for two and a half days? Before reading on, guess.</p>

## Four cameras, one strip of sky

TESS carries four cameras pointed side by side. Each sees a square of sky 24 degrees across, about 48 full Moons wide; together they see a strip 24 by 96 degrees. TESS stares at one strip for about 27 days, then turns to the next. Each strip, and each 27-day stare, is a **sector**.

<aside class="tw-mn" markdown>
**Sector.** One of TESS's 27-day stares at a 24 by 96 degree strip of sky. Sectors are numbered in order; our lesson star was seen in sectors 44 to 47.
</aside>

TESS looks at red and near-infrared light, 600 to 1,000 nm (lesson 3.1's spectrum, at its red end and past it). Its pixels are big: each covers 21 arcseconds of sky, so a pixel often holds light from more than one star.

## The hole in the middle

TESS's orbit takes 13.7 days, and it brings TESS closest to Earth once per orbit. There it points its antenna home and sends down everything it has stored: twice per sector. On the plot, the raw time stamps stop for 1.39 days. TESS also marks some measurements next to the gap as unreliable, and when those are left out, as in every lesson plot, the hole grows to 2.74 days. The sending itself takes only a few hours; we have not checked every reason the gap is longer. And a hole can swallow exactly what you are looking for: in this sector, our star's deeper eclipse (43.5%) was due at day 13.65, inside the hole, so the two drops you see are both the shallower kind.

## Think it through

<div class="tw-prob" data-answer="2|two" data-tol="0.01" data-hints='{"1":"A sector is about 27 days and one orbit is 13.7 days. How many orbits fit?"}' data-why="27 / 13.7 = about 2 orbits, and TESS sends its data at the closest point of each: 2 gaps per sector." markdown>
**a.** A sector lasts about 27 days and TESS's orbit takes 13.7. How many times per sector does TESS stop to send its data home?
</div>

!!! example "Worked example: how much of a sector is lost"
    Our sector 46: the usable light spans 25.98 days, with one hole of 2.74 days.

    **Step 1. Days actually watched.** \(25.98 - 2.74 = 23.24\) days.

    **Step 2. As a share.** \(23.24 / 25.98 = 0.895\).

    **Step 3.** About **89%** of the sector is usable light; about 11% is the hole.

!!! question "Your turn, half done: would a dip be missed?"
    A planet's dip lasts 8 hours and could fall at any moment of the sector. The hole covers 11% of it. Step 1: the share of moments that land in the hole is 0.11. Finish: out of 100 such dips, about how many would fall in the hole?

<div class="tw-prob" data-answer="11|10.5" data-tol="0.15" data-hints='{"0.11":"That is the share. Out of 100 dips: multiply by 100.","89":"That is the dips TESS sees. The question asks how many fall in the hole."}' data-why="0.11 x 100 = 11 (a few more if dips that only touch the hole's edges count as lost)." markdown>
**Your turn.** Dips lost in the hole, out of 100:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(0.11 \times 100 = 11\). A few more are partly lost, cut by the hole's edges. For a planet around two stars, which may cross only once in a sector, a hole like this can hide the only crossing there is.

The rule: **a sector has holes; a single dip has a fair chance of falling into one**.

</details>
</div>

## Two ways TESS records a star

TESS cannot send home every pixel every 2 minutes. It does two things:

- For a chosen list of stars, it sends small cut-outs every **2 minutes**. The lists are chosen in advance. From our own copies of the official lists: about 20,000 stars per sector in the early years, 13,000 per sector from sector 56, and 601,177 different stars over sectors 1 to 111.
- For everything else, it sends **full-frame images**: the whole field of all four cameras, added up over longer times. In our own files those are 30 minutes in sectors 1 to 26, 10 minutes in sectors 27 to 55, and 200 seconds from sector 56.

<aside class="tw-mn" markdown>
**Cadence.** How often a measurement is recorded: every 2 minutes for the chosen stars; every 30 minutes, 10 minutes or 200 seconds in the full-frame images, depending on the year.
</aside>

## North, south, and back again

From our own copies of the target lists: in sectors 1 to 13 (the first year) 96% of the 2-minute stars were south of the sky's equator; in sectors 14 to 26 none were. Years three and four repeated the pattern (95% south, then 6%). TESS covers one half of the sky a year, then the other, so most stars are seen only in a few sectors, years apart. Of the 601,177 two-minute stars, the middle one was recorded in just 2 sectors, and 79% in 3 or fewer; only 3% in 13 or more.

## Why this matters for Second Sun

Our hunt lists, G1 to G3, are stars with 2-minute light. The Census needs more stars, and most slow binaries were never 2-minute targets: they exist only in full-frame images, at 30, 10 or 200 seconds' cadence, with more noise. The holes matter too: a planet around two stars may cross only once in a sector, and a single crossing can fall into a hole. Petrova searches each sector's usable light and must never mistake a hole's edge for a dip.

## In a few sentences

TESS's four cameras watch a 24 by 96 degree strip of sky, a sector, for about 27 days, in red and near-infrared light. Twice a sector it sends its data home, leaving a hole: in our sector 46 the usable light stops for 2.74 days, 11% of the sector. Chosen stars are recorded every 2 minutes (about 13,000 to 20,000 per sector); everything else only in full-frame images, every 30, 10 or 3.3 minutes depending on the year. TESS watches the southern sky one year and the northern the next.

## Problems

<div class="tw-prob" data-answer="4" data-tol="0.01" data-hints='{"96":"That is the strip length in degrees. Divide by one camera, 24 degrees."}' data-why="96 / 24 = 4 cameras side by side." markdown>
**1.** Each camera sees 24 degrees and the strip is 96 degrees long. How many cameras sit side by side?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(96 / 24 = 4\). TESS has four identical cameras.

</details>
</div>

<div class="tw-prob" data-answer="9|9.0" data-tol="0.02" data-hints='{"3.3":"That is 200 seconds in minutes. How many 200-second images fit in 30 minutes?"}' data-why="30 minutes = 1,800 s; 1,800 / 200 = 9." markdown>
**2.** How many 200-second full-frame images fit into one 30-minute image of the first two years?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(30 \times 60 = 1{,}800\) s, and \(1{,}800 / 200 = 9\). The newest images are 9 times finer in time.

</details>
</div>

<div class="tw-prob" data-answer="south|southern|the south" data-why="In sectors 1 to 13, 96% of the 2-minute stars were south of the sky's equator." markdown>
**3.** In TESS's first year, which half of the sky did it watch? (North or south.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**South**: 96% of the year's 2-minute stars were south of the sky's equator. The second year was the north.

</details>
</div>

<div class="tw-prob" data-answer="720" data-tol="0.01" data-hints='{"30":"That is the number of 2-minute steps in an hour. A day has 24 hours."}' data-why="60 / 2 = 30 measurements an hour; 30 x 24 = 720 a day." markdown>
**4.** A 2-minute star gets one measurement every 2 minutes. How many per day?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(60 / 2 = 30\) per hour, \(30 \times 24 = 720\) per day: about 18,000 in a sector.

</details>
</div>

## Sources

- The cameras, strip, pixel size, colours and data sending: NASA HEASARC, "TESS Telescope Information" ([page](https://heasarc.gsfc.nasa.gov/docs/tess/telescope_information.html), read 24 Nov 2026): four cameras, "a combined field-of-view (FOV) of 24x96 degrees (known as an observing sector)"; 21 arcsecond pixels; bandpass 600 to 1000 nm; data "downlinked every 13.7 days at orbit perigee", in 4-hour sessions.
- Our own files (`book/tools/lesson_plots_u5b.py`, 24 Nov 2026): sector 46 of TIC 172900988 (SPOC 2-minute light, MAST): 120 s cadence, raw gap 1.39 days, usable gap 2.74 days, usable span 25.98 days. The TESS Science Office 2-minute target lists for sectors 1 to 111 (tess.mit.edu, downloaded 4 Nov 2026): targets per sector, hemispheres, 601,177 distinct stars. Full-frame cadence eras from our own downloads (`research/stage3/Q5-LOST-READS-2026-11-04.md`).
