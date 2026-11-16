---
hide: [toc, footer]
title: "3.2 Hot things glow"
---

# Hot things glow

Lesson 3.1 ended with a promise: cool stars shine mostly in red and infrared light. Here is a star at 3,300 K, a typical red dwarf, drawn colour by colour.

<div class="tw-plot" data-src="u3-glow-reddwarf"></div>

<p class="tw-plot__ask">The bottom axis is colour again, as in lesson 3.1. Before reading on, guess: at what wavelength is this star brightest? Is that a colour your eye can see?</p>

## Everything warm glows

Push a metal poker into a fire. At first it only feels hot. Then it glows dull red, then orange, then yellow-white. Nothing was added to it. It sends out light because it is hot, and the hotter it gets, the more light it sends and the bluer that light becomes.

A star is a ball of gas far hotter than any poker, and it glows for the same reason. Its surface is close to what physicists call a blackbody.

<aside class="tw-mn" markdown>
**Blackbody.** An object whose light comes only from its own heat. The odd name comes from the cold case: a cold one reflects nothing and looks black. Heat it and it glows, in a pattern set by one number, its temperature.
</aside>

The plot above shows that pattern for 3,300 K. It is a hill: one colour is brightest, and the glow falls away on both sides, quickly on the blue side and slowly on the long-wave side.

## The rule: hotter means bluer

Raise the temperature and the whole hill slides toward shorter wavelengths. The top of the hill, the **peak**, follows a simple rule found by Wilhelm Wien in 1893.

<aside class="tw-mn" markdown>
**Wien's law.** The wavelength where a blackbody glows brightest is a constant divided by its temperature. Twice as hot, half the peak wavelength.
</aside>

\[ \lambda_{\text{peak}} = \frac{b}{T}, \qquad b = 2.898 \times 10^{6} \text{ nm K} \]

Here \(T\) is in kelvin (lesson 2.3) and \(\lambda_{\text{peak}}\) comes out in nanometres. Look at the second plot: the Sun, at 5,772 K.

<div class="tw-plot" data-src="u3-glow-sun"></div>

Its peak is at \(2.898 \times 10^{6} / 5{,}772 = 502\) nm, green. Yet the Sun looks white, not green. The reason is on the plot: at 400 nm the glow is still 0.87 of the peak, and at 700 nm still 0.79. The Sun sends plenty of every colour your eye can see, and the eye adds them up to white.

## Think it through

<div class="tw-prob" data-answer="400" data-tol="0.01" data-hints='{"1600":"Hotter means a shorter peak wavelength, not a longer one. Twice as hot gives half."}' data-why="Twice the temperature halves the peak wavelength: 800 / 2 = 400 nm." markdown>
**a.** One star's glow peaks at 800 nm. A second star is twice as hot. Where does its glow peak, in nm?
</div>

<div class="tw-prob" data-answer="cooler|the cooler|cooler one|the cooler one" data-hints='{"hotter":"Hotter stars have the shorter peak wavelength. The question asks for the longer one.","the hotter":"Hotter stars have the shorter peak wavelength. The question asks for the longer one."}' data-why="The peak wavelength is b / T, so the cooler star, with the smaller T, has the longer peak wavelength." markdown>
**b.** A 3,000 K star and a 6,000 K star. Which one has the longer peak wavelength: the hotter or the cooler? (One word.)
</div>

<div class="tw-prob" data-answer="322" data-tol="0.02" data-hints='{"2898":"That is b divided by one kelvin. Divide by the temperature.","966":"That is the 3,000 K star. The question is about the 9,000 K one."}' data-why="At 3,000 K the peak is 965.9 nm. Three times as hot gives a third: 322 nm. Or directly: 2.898e6 / 9000 = 322 nm." markdown>
**c.** A 3,000 K star peaks at 966 nm. Where does a 9,000 K star peak, in nm?
</div>

!!! example "Worked example: where does a 3,300 K star peak?"
    **Step 1. Divide the constant by the temperature.** \(\lambda_{\text{peak}} = 2.898 \times 10^{6} / 3{,}300 = 878\) nm.

    **Step 2. Where is that?** Beyond red. Your eye stops at about 700 nm, so this star's brightest light is **infrared**, but it sits well inside the band where TESS keeps at least half of its best response (580 to 982 nm, lesson 3.1).

!!! question "Your turn, half done: a 3,000 K star"
    Step 1: divide \(2.898 \times 10^{6}\) by \(3{,}000\). Finish, and say whether TESS sees that colour.

<div class="tw-prob" data-answer="966" data-tol="0.01" data-unit="nm" data-hints='{"0.00104":"You divided the temperature by the constant. Divide the constant by the temperature.","9660":"Check the zeros: 2,898,000 divided by 3,000 is 966, not 9,660."}' data-why="2,898,000 / 3,000 = 966 nm." markdown>
**Your turn.** The peak wavelength of a 3,000 K star, in nm:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(\lambda_{\text{peak}} = 2.898 \times 10^{6} / 3{,}000 = 966\) nm, infrared. TESS still records at least half of its best response there, so a star this cool is bright to TESS even though it looks dim to your eye.

The rule: **\(\lambda_{\text{peak}} = b / T\)**, with \(T\) in kelvin.

</details>
</div>

## One curve, two rules

Lesson 2.3 gave you the brightness rule: each square metre of a hot surface sends out light in proportion to \(T^4\). It is the same hill. The total light is the **area under the curve**, and when the temperature doubles the hill gets higher everywhere, with an area 16 times larger. Hotter means brighter, and Wien's law says hotter also means bluer. Both rules come from one curve, written down by Max Planck in 1900, and the plots here are drawn from it.

You can run Wien's law backwards, and astronomers do. Measure where a star's glow peaks and you know its temperature, without going near it. A star's colour is its temperature in disguise.

## Back to the plots

Touch the red dwarf's hill. It peaks at 878 nm, exactly where Wien's law says. Red dwarfs run from about 3,850 K (type M0) to 3,060 K (type M5), so their peaks fall between about 753 and 947 nm. All of them sit inside the colour band TESS records best.

Now the Sun. Its peak, 502 nm, falls where TESS is blind. TESS still sees the Sun's long-wave tail, the glow at 600 to 1,000 nm, but on the plot that tail is only 0.41 to 0.93 of the peak. For a red dwarf the same colours are the top of the hill. That is the plain meaning of lesson 3.1's last paragraph: **a red-seeing camera is a camera tuned to the colours cool stars glow in.**

## In a few sentences

Anything hot glows, and a blackbody's glow is a hill whose peak wavelength is \(b / T\) (Wien's law, \(b = 2.898 \times 10^{6}\) nm K): hotter means a shorter peak, so bluer. The same curve gives the \(T^4\) brightness rule of lesson 2.3 as its area. Red dwarfs, 3,060 to 3,850 K, peak at 750 to 950 nm, inside TESS's band; the Sun peaks at 502 nm, in the colours TESS cannot see.

## Problems

<div class="tw-prob" data-answer="0.41|0.4" data-tol="0.15" data-why="Touching the Sun's curve at 1,000 nm gives a glow of about 0.41 of the peak." markdown>
**1.** Read the second plot, the Sun: about what share of the peak glow is there at 1,000 nm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

About **0.41**. Touch the curve at 1,000 nm: the glow has fallen to a bit under half of its value at 502 nm.

</details>
</div>

<div class="tw-prob" data-answer="241.5" data-tol="0.02" data-unit="nm" data-hints='{"0.000414":"You divided the temperature by the constant. Divide the constant by the temperature."}' data-why="2.898e6 / 12000 = 241.5 nm: ultraviolet, shorter than violet (about 400 nm)." markdown>
**2.** A hot blue star has a surface at 12,000 K. Where does its glow peak, in nm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(2.898 \times 10^{6} / 12{,}000 = 241.5\) nm. That is **ultraviolet**, shorter than violet (about 400 nm), so neither your eye nor TESS sees the top of its hill. Only the long-wave tail reaches us, and that tail is blue-white to the eye.

</details>
</div>

<div class="tw-prob" data-answer="947" data-tol="0.02" data-unit="nm" data-why="2.898e6 / 3060 = 947 nm, still inside TESS's best band (580 to 982 nm)." markdown>
**3.** The coolest star in the red dwarf range of lesson 3.1 is type M5, at 3,060 K. Where does it peak, in nm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(2.898 \times 10^{6} / 3{,}060 = 947\) nm. Even the coolest red dwarfs on the list peak inside the 580 to 982 nm band where TESS keeps at least half its best response.

</details>
</div>

<div class="tw-prob" data-answer="4000|4,000" data-tol="0.02" data-unit="K" data-hints='{"0.00025":"You divided the wavelength by the constant. Divide the constant by the wavelength.","3.6e-4":"Divide the constant by the wavelength."}' data-why="Run Wien's law backwards: T = b / wavelength = 2.898e6 / 725 = 3,997 K, about 4,000 K." markdown>
**4.** A star's glow peaks at 725 nm. What is its temperature, in K? (Run the rule backwards: \(T = b / \lambda_{\text{peak}}\).)

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(T = 2.898 \times 10^{6} / 725 = 3{,}997\) K, about **4,000 K**. That is a cool orange-red star, a little warmer than an M0 red dwarf.

</details>
</div>

<div class="tw-prob" data-answer="9348" data-tol="0.02" data-unit="nm" data-why="Skin at about 310 K: 2.898e6 / 310 = 9,348 nm, about 9.3 micrometres, deep infrared." markdown>
**5.** You glow too. Your skin is about 310 K. Where does your glow peak, in nm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(2.898 \times 10^{6} / 310 = 9{,}348\) nm, about 9.3 micrometres: far into the infrared. Your eye cannot see it, but a thermal camera is built to, which is why it shows warm bodies glowing in the dark.

</details>
</div>

## Sources

- The shape of the curves: Planck's law, computed by our own script (`book/tools/lesson_plots_u3b.py`) with the exact SI values of h, c and k (BIPM, SI Brochure, 9th edition). The script checks that the top of each curve lands where Wien's law puts it: 878.1 nm at 3,300 K and 502.0 nm at 5,772 K (read 17 Nov 2026).
- Wien's law and its constant \(b = 2.897771955 \times 10^{-3}\) m K: NIST CODATA 2018 value of the Wien wavelength displacement law constant; the idea, blackbodies, Planck's law and the area under the curve: OpenStax Astronomy 2e, chapter 5 "Radiation and Spectra" ([the book](https://openstax.org/details/books/astronomy-2e), CC BY-NC-SA 4.0), in our own words. The dates 1893 (Wien) and 1900 (Planck) are the textbook dates.
- The Sun's 5,772 K: the IAU 2015 nominal solar effective temperature (Resolution B3, Prsa et al. 2016, AJ 152, 41); the 5,770 K in Mamajek's table below agrees.
- Star temperatures by type, M0 dwarf 3,850 K, M5 dwarf 3,060 K, G2 dwarf 5,770 K: E. Mamajek, "A Modern Mean Dwarf Stellar Color and Effective Temperature Sequence", version 2022.04.16 ([table](https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt), downloaded 17 Nov 2026, based on Pecaut and Mamajek 2013, ApJS 208, 9). The 3,300 K red dwarf is a made-up mid-range example, not a named star.
- TESS band and red dwarfs: lesson 3.1 and Ricker et al. 2015 ([arXiv 1406.0151](https://arxiv.org/abs/1406.0151)).
