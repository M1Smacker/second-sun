---
hide: [toc, footer]
title: "3.3 Fingerprints"
---

# Fingerprints

Lesson 3.2 drew a star's glow as a smooth hill. Here is the real thing: the light of one star, split into its colours by an instrument called a **spectrograph**.

<div class="tw-plot" data-src="u3-a0-spectrum"></div>

<p class="tw-plot__ask">The hill is there, but it is full of narrow dark gaps. Before reading on, guess: what could take away exactly one colour of a star's light and leave the colours on both sides?</p>

## A spectrum with gaps

This star is hot, about 9,700 K, so by Wien's law its hill peaks near 299 nm, off the left edge of the plot. What you see is the downhill side, running from violet to red, with dark gaps cut into it. The gaps sit near 656, 486, 434, 410 and 397 nm, and more, crowding closer together toward the blue end.

<aside class="tw-mn" markdown>
**Absorption line.** A narrow range of wavelengths where a star's light is missing. The opposite, a bright line on a dark background, is an **emission line**: the glow of a thin hot gas.
</aside>

Something between the star's hot glowing layers and your telescope is swallowing those exact colours. It is the star's own thin outer gas, and it swallows light in a pattern that depends on what atoms the gas is made of.

## Why only certain colours: the ladder

An electron in an atom cannot have just any amount of energy. It can sit only on certain "rungs", like a ladder with no standing room between the steps. A photon, one packet of light, can lift the electron from one rung to a higher one only if the photon's energy equals the gap between the rungs exactly. Too little or too much and the photon passes by.

A photon's energy comes from its wavelength. For atoms the handy unit is the **electronvolt**.

<aside class="tw-mn" markdown>
**Electronvolt (eV).** A tiny unit of energy, the size used for single atoms and single photons. A photon of wavelength \(\lambda\) carries \(E = 1{,}240 / \lambda\) electronvolts when \(\lambda\) is in nanometres. Visible light, 700 to 400 nm, carries about 1.8 to 3.1 eV.
</aside>

Hydrogen is the simplest atom, one electron, and its rungs are known exactly: rung number \(n\) (1, 2, 3, and so on) sits at \(-13.6 / n^{2}\) eV. Take an electron sitting on rung 2. Lifting it to rung 3 costs \(13.6 \times (1/4 - 1/9) = 1.89\) eV, which is a photon of \(1{,}240 / 1.89 = 656\) nm: red. Lifting it to rung 4 costs 2.55 eV, a photon of 486 nm. Every jump from rung 2 up to a higher rung \(n\) takes one fixed colour, and together they are the **Balmer lines** of hydrogen. Johann Balmer found their pattern in 1885, long before anyone knew about rungs. Written as a rule for the wavelength:

\[ \frac{1}{\lambda} = R \left( \frac{1}{4} - \frac{1}{n^{2}} \right), \qquad R = 1.0968 \times 10^{7} \text{ per metre} \]

(\(R\) is the Rydberg constant for hydrogen.) As \(n\) grows, the lines crowd together and stop at a limit, the end of the series.

## Think it through

<div class="tw-prob" data-answer="2" data-tol="0.02" data-unit="eV" data-hints='{"0.5":"You multiplied by the wavelength. Divide 1,240 by it.","769":"That is 620 times 1.24 times 1,000. Divide 1,240 by 620."}' data-why="E = 1240 / 620 = 2.0 eV." markdown>
**a.** A photon of orange light has a wavelength of 620 nm. Using \(E = 1{,}240 / \lambda\), what is its energy, in eV?
</div>

<div class="tw-prob" data-answer="486|the 486|486 nm" data-hints='{"656":"Shorter wavelength means more energy. 656 nm is the longer one."}' data-why="Energy is 1240 / wavelength, so the shorter wavelength (486 nm, 2.55 eV) carries more than 656 nm (1.89 eV)." markdown>
**b.** A photon of 656 nm light or a photon of 486 nm light: which carries more energy? (Type the wavelength.)
</div>

!!! example "Worked example: the wavelength of the \(n = 3\) line"
    **Step 1. The bracket.** \(1/4 - 1/9 = 9/36 - 4/36 = 5/36 = 0.1389\).

    **Step 2. Multiply by \(R\).** \(1/\lambda = 1.0968 \times 10^{7} \times 0.1389 = 1.523 \times 10^{6}\) per metre.

    **Step 3. Turn it over and convert.** \(\lambda = 1 / 1.523 \times 10^{6} = 6.565 \times 10^{-7}\) m \(= 656.5\) nm.

    This is **H-alpha**, the red line, the first of the Balmer lines.

!!! question "Your turn, half done: the \(n = 4\) line"
    Step 1: \(1/4 - 1/16 = 3/16 = 0.1875\). Finish: multiply by \(R\), turn it over, and convert to nanometres.

<div class="tw-prob" data-answer="486" data-tol="0.01" data-unit="nm" data-hints='{"2.0565e6":"That is 1/lambda, not lambda. Turn it over: lambda = 1 / (R x 0.1875).","0.486":"That is in micrometres. The question asks for nanometres.","4.86e-7":"That is in metres. Multiply by one billion to get nanometres."}' data-why="1/lambda = 1.0968e7 x 0.1875 = 2.0565e6 per metre, so lambda = 4.863e-7 m = 486.3 nm." markdown>
**Your turn.** The wavelength of the \(n = 4\) Balmer line, in nm:

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(1/\lambda = 1.0968 \times 10^{7} \times 0.1875 = 2.0565 \times 10^{6}\) per metre, so \(\lambda = 4.863 \times 10^{-7}\) m \(= 486.3\) nm. This is H-beta, blue-green.

The rule: **\(1/\lambda = R\,(1/4 - 1/n^{2})\)**, then turn it over.

</details>
</div>

## Back to the plot

Touch the dips on the star's spectrum. The darkest points sit at 656.45, 486.30, 434.21, 410.30 and 397.10 nm. The formula, which knows nothing about this star, says 656.47, 486.27, 434.17, 410.29 and 397.12. For all seven lines from \(n = 3\) to \(n = 9\) the formula and the file agree within 0.05 nm. The dark gaps in a star's light are hydrogen, and an atom's ladder predicts exactly where.

Why does this star show hydrogen so strongly? At about 9,700 K the gas is hot enough that many hydrogen atoms sit on rung 2, the starting rung for the Balmer lines, but not so hot that the atoms lose their electrons altogether. In cooler stars most atoms sit on rung 1, whose lines are in the ultraviolet, and in much hotter stars hydrogen is stripped bare. The strength of the lines is therefore a second thermometer.

## Every atom has its own fingerprint

Each kind of atom has its own ladder, so its own set of wavelengths. Sodium has a pair near 589 nm, the orange-yellow of old street lamps. Helium has a line near 588 nm. Iron has thousands. Match the dark lines in a star's spectrum to the laboratory lines of each atom and you can read what the star's outer gas is made of, from a distance no spacecraft could cross.

In 1925 Cecilia Payne did exactly that, with thousands of spectra and laboratory data, and found that stars are made mostly of hydrogen and helium. The senior astronomer on her thesis committee disagreed, she added a line to her thesis doubting her own result, and later studies confirmed it.

## Why this matters for Second Sun

TESS adds up every colour it can record into a single number each moment (lesson 3.1). The H-alpha dip at 656 nm sits inside TESS's band, but TESS cannot pull it apart from the colours around it. **A light curve has no fingerprints**, only the total brightness. Lines are a different kind of data, and lesson 3.4 uses them to measure speeds.

## In a few sentences

An electron in an atom can sit only on certain rungs, so an atom takes in only photons whose energy (\(E = 1{,}240 / \lambda\) eV, with \(\lambda\) in nm) matches a gap between rungs. That cuts dark absorption lines into a star's spectrum at wavelengths set by its atoms. Hydrogen's Balmer lines follow \(1/\lambda = R\,(1/4 - 1/n^{2})\) and match a real star's spectrum to 0.05 nm. TESS's single brightness number hides all of this.

## Problems

<div class="tw-prob" data-answer="h-beta|hbeta|h beta|beta|h-b|hb|hβ|h-β|h β" data-hints='{"h-alpha":"H-alpha is the red line at 656 nm. This dip is at 486 nm, the next one.","halpha":"H-alpha is the red line at 656 nm. This dip is at 486 nm, the next one.","alpha":"Alpha is the red line at 656 nm. This dip is at 486 nm, the next one.","h-gamma":"H-gamma is the next one, at 434 nm. 486 nm comes before it.","gamma":"Gamma is the next one, at 434 nm. 486 nm comes before it."}' data-why="The n = 4 line is at 486 nm: H-beta, the second Balmer line after H-alpha at 656 nm." markdown>
**1.** Touch the plot near 486 nm. Which Balmer line is that dip? (H-alpha, H-beta, H-gamma, and so on.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**H-beta**, the \(n = 4\) line, at 486 nm. The series goes H-alpha (656 nm), H-beta (486), H-gamma (434), H-delta (410).

</details>
</div>

<div class="tw-prob" data-answer="434" data-tol="0.01" data-unit="nm" data-why="1/4 - 1/25 = 0.21; 1/lambda = 1.0968e7 x 0.21 = 2.303e6; lambda = 434.2 nm." markdown>
**2.** Predict the \(n = 5\) Balmer line. What wavelength, in nm?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(1/4 - 1/25 = 0.21\), \(1/\lambda = 1.0968 \times 10^{7} \times 0.21 = 2.303 \times 10^{6}\) per metre, \(\lambda = 4.342 \times 10^{-7}\) m \(= 434.2\) nm. On the plot, the dip is at 434.21 nm: H-gamma.

</details>
</div>

<div class="tw-prob" data-answer="365|364.7" data-tol="0.01" data-unit="nm" data-hints='{"3.647e-7":"That is in metres. The question asks for nanometres: multiply by one billion."}' data-why="For huge n, 1/n^2 is almost 0, so 1/lambda = R/4 and lambda = 4/R = 4 / 1.0968e7 = 3.647e-7 m = 364.7 nm." markdown>
**3.** As \(n\) gets very large, \(1/n^{2}\) shrinks to almost nothing. Where do the Balmer lines pile up, in nm? (Use \(\lambda = 4 / R\).)

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(\lambda = 4 / (1.0968 \times 10^{7}) = 3.647 \times 10^{-7}\) m \(= 364.7\) nm, the **series limit**. Every Balmer line lies between 656 nm and this limit, and they bunch up toward it. That is why the left edge of the plot is crowded with dips.

</details>
</div>

<div class="tw-prob" data-answer="1.89|1.9" data-tol="0.02" data-unit="eV" data-why="E = 1240 / 656.5 = 1.889 eV, the same as 13.6 x (1/4 - 1/9) = 1.89 eV." markdown>
**4.** Find the energy of an H-alpha photon (656.5 nm) two ways: from the wavelength, \(E = 1{,}240 / \lambda\). Does it match the rung gap \(13.6 \times (1/4 - 1/9) = 1.89\) eV? Give the first answer, in eV.

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(E = 1{,}240 / 656.5 = 1.889\) eV. Both routes give 1.89 eV. That agreement is the whole idea: the colour of a line and the size of the gap between two rungs are the same fact written two ways.

</details>
</div>

<div class="tw-prob" data-answer="no" data-why="TESS adds all the colours it can record into one brightness number, so the narrow dips cannot be seen." markdown>
**5.** Could a TESS light curve of this star show you its hydrogen dips? (Yes or no.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**No.** TESS records one brightness number for all the colours it sees at once. The H-alpha dip is a tiny gap in one colour, so it is lost in the total. To see lines you must first split the light by colour, which a spectrograph does and TESS does not.

</details>
</div>

## Sources

- The spectrum: SDSS DR17 spectrum of an A0 star, plate 2938, MJD 54526, fibre 518, from the Sloan Digital Sky Survey (Abdurro'uf et al. 2022, ApJS 259, 35; [the survey](https://www.sdss.org/dr17/)); chosen from the survey catalogue as a bright A0 star whose motion is too small to move its lines (redshift 2.6e-6, 0.8 km/s). File downloaded 17 Nov 2026 (`research/downloads.csv`). The star is not cross-matched against our hunt lists, and no TESS light of it is used. SDSS wavelengths are in vacuum, and so are the formula's.
- The check against the formula, our own script `book/tools/lesson_plots_u3b.py` (17 Nov 2026): the darkest point of the file near each predicted line sits within 0.05 nm of it for \(n = 3\) to \(9\) (656.45 against 656.47, 486.30 against 486.27, 434.21 against 434.17, 410.30 against 410.29, 397.10 against 397.12 nm).
- The Rydberg constant \(R_H = 1.0967758 \times 10^{7}\) per metre: the NIST CODATA value for infinite mass, \(10{,}973{,}731.568\) per metre, corrected for the proton's finite mass. The ladder, photon energy, Balmer series, absorption and emission lines: OpenStax Astronomy 2e, chapter 5 "Radiation and Spectra" ([the book](https://openstax.org/details/books/astronomy-2e), CC BY-NC-SA 4.0), in our own words. Balmer 1885 is the textbook date.
- The star's temperature, about 9,700 K, from the type A0 dwarf row of Mamajek's table (lesson 3.2 sources). That Balmer lines are strongest in A stars near this temperature: OpenStax, same chapter.
- Cecilia Payne's 1925 thesis, its result, and her committee's doubt: Science History Institute, "Cecilia Payne-Gaposchkin" ([biography](https://www.sciencehistory.org/education/scientific-biographies/cecilia-payne-gaposchkin/), read 17 Nov 2026). The thesis is "Stellar Atmospheres" (Harvard, 1925).
