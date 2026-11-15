---
hide: [toc, footer]
title: "3.1 What light is"
---

# What light is

Every number in this book so far came from one thing: light from a star, counted by a camera. This plot shows what that camera can count.

<div class="tw-plot" data-src="u3-tess-response"></div>

<p class="tw-plot__ask">The bottom axis is not time this time. It is colour, written as a number. Before reading on, guess: where is TESS blind, and where does it see best?</p>

## Light is a wave

Light is a ripple of electric and magnetic fields travelling through space. Like a ripple on water, it has crests, and the distance from one crest to the next is its **wavelength**.

<aside class="tw-mn" markdown>
**Wavelength (\(\lambda\), "lambda").** The distance from one crest of a wave to the next. For light it is tiny, so we measure it in **nanometres** (nm): one billionth of a metre.
</aside>

Your eye reads wavelength as colour. Light of about 700 nm looks red, about 550 nm green, about 450 nm blue, and about 400 nm violet. That band, roughly 400 to 700 nm, is all your eye can see.

The rainbow does not stop where your eye does. Past red come longer waves, **infrared**, then microwaves and radio. Past violet come shorter ones, **ultraviolet**, then X-rays and gamma rays. All of these are the same thing, light, with different wavelengths. Lined up by wavelength they make the **spectrum**.

## Speed, wavelength and frequency

All light in empty space travels at the same speed, \(c = 299{,}792{,}458\) metres per second. As a wave passes you, crests arrive one after another. How many arrive each second is the **frequency**.

<aside class="tw-mn" markdown>
**Frequency (\(f\)).** How many crests pass a point each second. Unit: the **hertz** (Hz), one per second.
</aside>

If each crest is \(\lambda\) apart and the wave moves \(c\) metres each second, then \(c / \lambda\) crests pass every second:

\[ c = \lambda \times f \]

Long waves, low frequency. Short waves, high frequency. The two always multiply to the same speed.

## Think it through

<div class="tw-prob" data-answer="1000" data-tol="0" data-why="A micrometre is a millionth of a metre and a nanometre a billionth, so one micrometre holds 1,000 nanometres." markdown>
**a.** A micrometre is a millionth of a metre. How many nanometres fit in one micrometre?
</div>

<div class="tw-prob" data-answer="violet" data-hints='{"red":"Red waves are the long ones. Shorter waves mean more crests per second."}' data-why="Violet waves are shorter (about 400 nm against 700 nm), so more crests pass each second: higher frequency." markdown>
**b.** Red light (700 nm) or violet light (400 nm): which has the higher frequency? (One word.)
</div>

<div class="tw-prob" data-answer="1.75" data-tol="0.02" data-hints='{"0.57":"That is violet divided by red. Frequency goes the other way round from wavelength."}' data-why="Frequency is c divided by wavelength, so the ratio is 700 / 400 = 1.75." markdown>
**c.** How many times higher is violet's frequency than red's?
</div>

!!! example "Worked example: the frequency of 1,000 nm light"
    **Step 1. Metres.** \(1{,}000 \text{ nm} = 1{,}000 \times 10^{-9} = 10^{-6}\) m.

    **Step 2. Divide the speed by the wavelength.** \(f = c / \lambda = 3.00 \times 10^{8} / 10^{-6} = 3.00 \times 10^{14}\) Hz.

    Three hundred million million crests every second. That is the reddest light TESS records well.

!!! question "Your turn, half done: 600 nm"
    Step 1: \(600 \text{ nm} = 6.00 \times 10^{-7}\) m. Finish: divide \(3.00 \times 10^{8}\) by it.

<div class="tw-prob" data-answer="5e14" data-tol="0.01" data-unit="Hz" data-hints='{"5e-14":"Divide the speed by the wavelength, not the other way round.","1.8e-15":"Multiplying gives nonsense units: divide."}' data-why="3.00 x 10^8 / 6.00 x 10^-7 = 5.00 x 10^14 Hz." markdown>
**Your turn.** The frequency of 600 nm light, in Hz (you can type 5e14):

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(f = 3.00 \times 10^{8} / 6.00 \times 10^{-7} = 0.5 \times 10^{15} = 5.00 \times 10^{14}\) Hz.

The rule: **\(c = \lambda f\)**, with the wavelength in metres.

</details>
</div>

## Back to the plot

Touch the curve. Below about 580 nm the share is zero: **TESS is blind to green, blue and violet.** It records best from about 600 to 950 nm, red light and the **near infrared** just past it, peaking near 720 nm where it keeps about 0.79 of the light that arrives. By about 1,050 nm it fades out again. Most of what TESS sees, your eye could never see at all.

Why build a camera like that? Small planets are easier to spot around small stars, because they hide a bigger share of the star. Small stars are cool, and cool stars shine mostly in red and infrared light. So TESS's builders made it see red. The smallest common ones, **red dwarfs**, make up about three quarters of the stars near the Sun. Lesson 3.2 shows why cooler means redder.

<aside class="tw-mn" markdown>
**Response curve.** For each wavelength, the share of arriving light an instrument records. It sets which colours a "brightness" number really counts.
</aside>

## In a few sentences

Light is a wave; its wavelength is its colour, and the eye sees only about 400 to 700 nm of a spectrum that runs from radio to gamma rays. All light moves at \(c\), so \(c = \lambda f\): shorter waves have higher frequencies. TESS counts light from about 600 to 1,000 nm, red and near infrared, best near 720 nm, because small planets are easiest to find around small stars, and small stars are cool and red.

## Problems

<div class="tw-prob" data-answer="0.3|0.30|0.29" data-tol="0.15" data-why="Reading the curve at 1,000 nm gives about 0.30: TESS records under a third of the light there." markdown>
**1.** Read the plot: about what share of the light arriving at 1,000 nm does TESS record?

<details class="tw-sol" markdown><summary>Worked solution</summary>

About **0.30**. Touch the curve at 1,000 nm. The camera's sensitivity falls away fast past about 950 nm.

</details>
</div>

<div class="tw-prob" data-answer="no" data-why="The curve is zero at 530 nm: TESS records almost none of green light." markdown>
**2.** A star sends out a strong burst of green light at 530 nm. Would TESS's brightness numbers show it? (Yes or no.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**No.** The response is zero below about 570 nm. TESS's light curves count only red and near-infrared light.

</details>
</div>

<div class="tw-prob" data-answer="3" data-tol="0.02" data-unit="m" data-hints='{"0.33":"Wavelength is the speed divided by the frequency: 3 x 10^8 / 10^8."}' data-why="100 MHz is 10^8 Hz; 3.00 x 10^8 / 10^8 = 3 m." markdown>
**3.** An FM radio station broadcasts at 100 MHz (\(10^{8}\) Hz). What is its wavelength, in metres? Radio is light too.

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(\lambda = c / f = 3.00 \times 10^{8} / 10^{8} = 3\) m. The same kind of wave as starlight, a few million times longer.

</details>
</div>

<div class="tw-prob" data-answer="small stars|small|small cool stars|cool stars|red dwarfs|red dwarf|small red stars" data-why="Small planets are easier to detect around small stars, which are cool and red, so TESS was made to see red." markdown>
**4.** Small planets are easier to find around which kind of star, the reason TESS was made to see red? (Two words.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**Small stars.** A small planet hides a bigger share of a small star, so its dip is deeper. Small stars are cool and shine mostly in red and infrared light, where TESS looks. The smallest common ones are the red dwarfs.

</details>
</div>

## Sources

- The TESS response curve: TESS instrument response function, version 2.0, R. Vanderspek, TESS Payload Operations Center, MIT, 2020, from the NASA TESS Science Support Center (downloaded 15 Nov 2026). Peak 0.785 at 722 nm, half of peak from 580 to 982 nm: our own reading of the file.
- TESS's 600 to 1,000 nm band and why: Ricker et al. 2015, "The Transiting Exoplanet Survey Satellite", JATIS 1, 014003 ([arXiv 1406.0151](https://arxiv.org/abs/1406.0151)), section 3.4: "Enhanced sensitivity to red wavelengths is desired because small planets are more easily detected around small stars, which are cool and red." Red dwarfs (M0 to M5) as about three quarters of nearby stars: the same paper, section 3.3 (read 15 Nov 2026).
- The speed of light, 299,792,458 m/s: exact by the SI definition of the metre (BIPM, SI Brochure, 9th edition).
- Visible light about 400 to 700 nm, the spectrum from radio to gamma rays, \(c = \lambda f\): OpenStax Astronomy 2e, chapter 5 "Radiation and Spectra" ([the book](https://openstax.org/details/books/astronomy-2e), CC BY-NC-SA 4.0), in our own words.
