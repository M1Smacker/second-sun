---
hide: [toc, footer]
title: "5.3 From pixels to light curves"
---

# From pixels to light curves

TESS does not send a light curve. It sends pixels. For a 2-minute star, every 2 minutes, a small square cut-out of the sky around it. Turning those pixels into one number per 2 minutes is the first step of every search, and it has choices in it.

<div class="tw-plot" data-src="u5-raw-sector"></div>

<p class="tw-plot__ask">This is sector 46 of our two-sun star, straight from the pixels, before any correction. Compare it with lesson 5.2's plot, the corrected light. Before reading on, guess: what did the correction change?</p>

## The stamp and the aperture

For our star the cut-out, the **stamp**, is 11 by 11 pixels. Each pixel covers 21 arcseconds of sky (lesson 5.2), so the stamp is about 3.9 arcminutes across. The star's light falls mostly on a few pixels near the middle.

<aside class="tw-mn" markdown>
**Aperture.** The pixels chosen to add up for a star's brightness. Too few, and some of the star's light is left out; too many, and more sky and more neighbouring stars come in.
</aside>

TESS's pipeline (SPOC) chose 20 of the 121 pixels as the aperture and 29 others, away from the star, to measure the sky's own glow, the **background**. Each 2 minutes: add up the 20 aperture pixels, subtract the background, and you have the **simple aperture photometry**, SAP, the plot above. For our star the background subtracted is 2,480 electrons per second, 11.7% as much as the star's own 21,210.

## Two corrections for the level

The pipeline then corrects two things it knows from its model of the sky around the star, both stored in the file:

- Some of the star's light falls outside the 20 pixels. The file's **flux fraction** says the aperture holds 93.508% of it.
- Some light inside the aperture comes from other stars. The file's **crowding** number says 99.878% of it is our star's.

The corrected light (PDCSAP, lesson 5.2's plot) puts both right: take away the neighbours' share, then divide by the share captured. It also removes slow trends that many stars on the same detector share (the method is called MAP; the file says so). For this bright star in this sector the raw light was already smooth, so the visible change is mostly the level.

## Think it through

<div class="tw-prob" data-answer="1.068|1.07" data-tol="0.01" data-hints='{"0.936":"Upside down: divide the crowding by the flux fraction, 0.99878 / 0.93508."}' data-why="0.99878 / 0.93508 = 1.068: the corrected light sits 6.8% above the raw." markdown>
**a.** The corrected light's middle level is the raw level times crowding divided by flux fraction. Using 0.99878 and 0.93508, by what factor is it higher?
</div>

!!! example "Worked example: our file checks out"
    Raw middle level 21,209.7; corrected 22,654.8 electrons per second.

    **Step 1. The measured ratio.** \(22{,}654.8 / 21{,}209.7 = 1.0681\).

    **Step 2. The predicted ratio.** \(0.99878 / 0.93508 = 1.0681\).

    **Step 3.** They agree to four decimals: the file's corrections are exactly the two described above.

!!! question "Your turn, half done: a crowded star"
    A dip removes 1,000 ppm of the raw light of a star whose crowding is 0.80: a fifth of the aperture's light is from neighbours that do not dim. Step 1: only 0.80 of the light belongs to the star that dimmed. Finish: how deep is the dip in the star's own light, in ppm?

<div class="tw-prob" data-answer="1250" data-tol="0.02" data-unit="ppm" data-hints='{"800":"The neighbours make the dip look SHALLOWER. Divide by 0.80, do not multiply.","200":"That is the neighbours share. The dip is 1,000 / 0.80."}' data-why="1,000 / 0.80 = 1,250 ppm: the neighbours' light diluted the dip, as in lesson 2.4." markdown>
**Your turn.** The dip in the star's own light, in ppm:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(1{,}000 / 0.80 = 1{,}250\) ppm. It is lesson 2.4's dilution again, with the neighbours as the second star. The flux fraction does not change a dip's depth in percent: it scales the dip and the level alike.

The rule: **crowding dilutes a dip; the corrected light undoes it, if the crowding number is right**.

</details>
</div>

## Why this matters for Second Sun

Our star is bright and alone: crowding 0.99878, so its dips are only 0.12% too shallow in the raw light. Fainter stars, and stars in crowded fields such as the Milky Way's plane, can have crowding far below 1, and then a dip's depth is only as right as the pipeline's sky model. Full-frame light (QLP and TESS-SPOC images, the Census's source for most slow binaries) is also made by adding up aperture pixels, from the full-frame images. And a planet's dip around two stars is diluted twice: by the other star of the pair (lesson 2.4) and by any neighbours in the aperture.

## In a few sentences

TESS sends pixels; a light curve is the sum of the aperture pixels minus the sky's background (SAP). The pipeline then corrects for the star's light outside the aperture and for neighbours' light inside it, and removes trends shared by many stars (PDCSAP). For our star, 20 of 121 pixels make the aperture, the background is 11.7% of the star's light, and the two corrections raise the level by exactly 0.99878 / 0.93508 = 1.068. Crowding is what changes a dip's depth: a dip of 1,000 ppm in raw light with crowding 0.80 is really 1,250 ppm deep.

## Problems

<div class="tw-prob" data-answer="3.85|3.9" data-tol="0.03" data-unit="arcminutes" data-hints='{"231":"That is in arcseconds. One arcminute is 60 arcseconds."}' data-why="11 x 21 = 231 arcseconds = 3.85 arcminutes." markdown>
**1.** The stamp is 11 pixels wide and each pixel is 21 arcseconds. How wide is the stamp, in arcminutes?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(11 \times 21 = 231\) arcseconds, and \(231 / 60 = 3.85\) arcminutes: about an eighth of the full Moon's width.

</details>
</div>

<div class="tw-prob" data-answer="0.117|11.7" data-tol="0.03" data-hints='{"8.55":"Upside down: background divided by the star, 2,480 / 21,210."}' data-why="2,480 / 21,210 = 0.117: the background was 11.7% of the star's own light." markdown>
**2.** The background is 2,480 and the star's raw light 21,210 electrons per second. What share of the star's light is the background?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(2{,}480 / 21{,}210 = 0.117\), about 12%. Getting it wrong by even a tenth would shift every dip's depth by about 1%.

</details>
</div>

<div class="tw-prob" data-answer="0.12|0.122" data-tol="0.05" data-unit="percent" data-hints='{"99.88":"That is the crowding itself. The dip is too shallow by the neighbours share: 100 minus 99.878."}' data-why="1 - 0.99878 = 0.00122: dips in the raw light are 0.12% too shallow." markdown>
**3.** With crowding 0.99878, by how many percent are our star's dips too shallow in the raw light?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(1 - 0.99878 = 0.00122\), so **0.12%**: far too little to matter for this star.

</details>
</div>

<div class="tw-prob" data-answer="no" data-hints='{"yes":"The flux fraction scales the dip and the level by the same factor."}' data-why="Dividing everything by the flux fraction scales the dip and the level alike, so the dip's depth in percent does not change." markdown>
**4.** Does the flux-fraction correction change a dip's depth in percent? (Yes or no.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**No.** It divides the whole light curve by the same number, dip and level alike. Only the crowding correction changes depths.

</details>
</div>

## Sources

- Our file (`book/tools/lesson_plots_u5c.py`, 24 Nov 2026): TESS sector 46 SPOC 2-minute light curve of TIC 172900988 from MAST. Header and columns read directly: 11 by 11 stamp, 20 aperture and 29 background pixels, CROWDSAP 0.99878 ("Ratio of target flux to total flux in op. ap."), FLFRCSAP 0.93508 ("Frac. of target flux w/in the op. aperture"), PDCMETHD MAP, median SAP 21,209.7 and PDCSAP 22,654.8 electrons per second, background 2,479.7. The script stops unless the PDCSAP to SAP ratio equals CROWDSAP / FLFRCSAP within 0.5% (they agree to 0.001%).
- The corrections and their purpose: Stumpe et al. 2012, "Kepler Presearch Data Conditioning I" ([arXiv 1203.1382](https://arxiv.org/abs/1203.1382), read 24 Nov 2026): corrections "for incompletely captured target flux (the flux fraction ...), and for excess light from neighboring stars into the aperture (crowding metric)", while "preserving planet-transits". The MAP method: Smith et al. 2012, "Kepler Presearch Data Conditioning II" ([arXiv 1203.1383](https://arxiv.org/abs/1203.1383)). Our TESS file names the same MAP method.
- Pixel size: NASA HEASARC TESS Telescope Information (lesson 5.2).
