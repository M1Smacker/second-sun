---
hide: [toc, footer]
title: "3.4 Doppler"
---

# Doppler

Lesson 3.3 showed that a star's light carries dark lines at exact wavelengths. Here is what happens when you measure those lines night after night for one star, 51 Pegasi, and turn each night's tiny shift into a speed.

<div class="tw-plot" data-src="u3-51peg-rv"></div>

<p class="tw-plot__ask">The star swings toward us and away from us, about 55 metres per second each way, every 4.23 days. Before reading on, guess: what could push a whole star back and forth like that?</p>

## Moving sources change colour

Stand by a road as an ambulance passes. The siren sounds higher as it comes toward you and lower as it goes away. The siren never changed; its motion did. A source moving toward you squeezes its waves closer together, and one moving away stretches them apart. This is the **Doppler effect**, and light does it too.

<aside class="tw-mn" markdown>
**Blueshift and redshift.** Light from a source moving toward you arrives at a slightly shorter wavelength (shifted toward blue); from a source moving away, at a slightly longer one (toward red). The words describe the direction of the shift, not the colour you see.
</aside>

For speeds far below the speed of light \(c\), the shift is simple:

\[ \frac{\Delta \lambda}{\lambda} = \frac{v}{c} \]

where \(\lambda\) is the wavelength the line has at rest (from the atom's ladder, lesson 3.3), \(\Delta\lambda\) is how far it moved, and \(v\) is the speed **along the line of sight**, toward or away from us. Sideways motion does not shift the line at all.

<aside class="tw-mn" markdown>
**Radial velocity.** The part of a star's motion straight toward us or straight away from us, measured from the Doppler shift of its lines. Away counts as positive, toward as negative.
</aside>

## How small the shift is

The speed of light is 299,792 km/s. A star moving away at 30 km/s shifts every line by \(30 / 299{,}792 = 0.0001\) of its wavelength: the red hydrogen line at 656.28 nm moves to 656.35 nm. A good spectrograph sees that easily.

51 Pegasi's swing is 55 **metres** per second, about 550 times smaller. Its H-alpha line moves by about 0.00012 nm, far less than the width of the line itself. Nobody measures that from one line. The Lick team that took the data above passed the starlight through a glass cell of iodine gas, which prints thousands of its own sharp lines on top of the star's, a ruler that travels with the light. Comparing the star's thousands of lines against the iodine ruler, they measured speeds to a few metres per second.

## Think it through

<div class="tw-prob" data-answer="0.0328|0.033" data-tol="0.03" data-unit="nm" data-hints='{"32.8":"You used 15,000 for the speed but 299,792 in km/s. Use the same unit for both: 15 km/s and 299,792 km/s.","0.0000500":"That is v/c alone. Multiply it by the wavelength, 656.28 nm."}' data-why="v/c = 15 / 299,792 = 5.00e-5; times 656.28 nm gives 0.0328 nm." markdown>
**a.** A star moves away from us at 15 km/s. How far does its H-alpha line (656.28 nm at rest) move, in nm?
</div>

<div class="tw-prob" data-answer="red|redshift|red shift|longer|toward red" data-hints='{"blue":"Moving away stretches the waves. Longer wavelength is toward red."}' data-why="Moving away stretches the waves, so the wavelength gets longer: a redshift." markdown>
**b.** Is that a redshift or a blueshift? (Type red or blue.)
</div>

!!! example "Worked example: a speed from a shift"
    A line that sits at 500.000 nm in the laboratory is measured at 499.990 nm in a star.

    **Step 1. The shift.** \(\Delta\lambda = 499.990 - 500.000 = -0.010\) nm. Negative: shorter, a blueshift.

    **Step 2. The ratio.** \(\Delta\lambda / \lambda = -0.010 / 500 = -2.0 \times 10^{-5}\).

    **Step 3. The speed.** \(v = c \times (-2.0 \times 10^{-5}) = 299{,}792 \times (-2.0 \times 10^{-5}) = -6.0\) km/s. The star moves **toward** us at 6 km/s.

!!! question "Your turn, half done"
    The same line is measured at 500.0015 nm. Step 1: \(\Delta\lambda = +0.0015\) nm, a redshift. Finish: the ratio, then the speed, in metres per second.

<div class="tw-prob" data-answer="900|899" data-tol="0.01" data-unit="m/s" data-hints='{"0.9":"That is in km/s. The question asks for metres per second: multiply by 1,000.","3e-6":"That is the ratio. Multiply it by the speed of light."}' data-why="0.0015 / 500 = 3.0e-6; times 299,792,458 m/s = 899 m/s, about 900 m/s away from us." markdown>
**Your turn.** The star's speed, in m/s (away from us is positive):

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(\Delta\lambda/\lambda = 0.0015 / 500 = 3.0 \times 10^{-6}\), so \(v = 299{,}792{,}458 \times 3.0 \times 10^{-6} = 899\) m/s, about 0.9 km/s, **away** from us.

The rule: **\(v = c\,\Delta\lambda / \lambda\)**, and the sign says the direction.

</details>
</div>

## Why a star wobbles

A planet does not simply circle its star. The star and the planet both circle their shared **centre of mass**, the balance point between them, the way two dancers holding hands spin around a point between them. The heavy star sits close to that point and makes a small circle; the light planet makes a huge one. The balance gives the rule:

\[ M_\star \, v_\star = m_p \, v_p \]

The star's mass times its speed equals the planet's mass times its speed. Jupiter, about 1/1,048 of the Sun's mass, moves at 13.1 km/s, so it swings the Sun around at \(13{,}100 / 1{,}048 = 12.5\) m/s with a 12-year period. Earth, 1/333,000 of the Sun's mass, swings it at only 9 centimetres per second.

<aside class="tw-mn" markdown>
**Centre of mass.** The balance point of two bodies, closer to the heavier one. Each body circles it; neither stays still.
</aside>

## Back to the plot

Touch the plot. Near day 0 the star comes toward us at about 55 m/s (the dots sit near \(-55\)); a quarter of the orbit later it is moving sideways, so the measured speed passes through zero; near day 2.1 it moves away at about 55 m/s. The 354 measurements, taken over 16 years, fall on one smooth wave when folded on 4.23 days. Our own fit gives a period of 4.230799 days (the published value is 4.2307966) and a swing, called the **semi-amplitude** \(K\), of 55.5 m/s (published: 55.77 m/s). The dots scatter about 8 m/s around the wave: the measurement error plus the star's own restless surface. One dot near the top, at +111 m/s, is far off the wave. It stays in the plot, because real data has such points and hiding them would be dishonest.

From \(K\), the period and the star's mass (1.07 Suns), the balance rule gives the planet's mass. For a circular orbit and a planet much lighter than its star:

\[ m_p \sin i = K \left( \frac{P}{2\pi G} \right)^{1/3} M_\star^{2/3} \]

Put in \(K = 55.5\) m/s, \(P = 4.2308\) days and \(M_\star = 1.07\) Suns, and out comes 0.46 Jupiter masses, matching the published 0.46 to 0.47. A planet half as heavy as Jupiter, going around its star in four days. Kepler's law (lesson 2.5) puts it at 0.052 AU, about seven times closer than Mercury is to the Sun. Nothing like it was known in 1995.

<aside class="tw-mn" markdown>
**Why "sin i".** Doppler sees only the part of the motion along our line of sight. If the orbit is tilted by an angle \(i\) from face-on, we see the speed times \(\sin i\). So the method gives a **minimum mass**: the planet is at least this heavy, and heavier if the orbit is closer to face-on.
</aside>

## The first planet around a Sun-like star

Michel Mayor and Didier Queloz found 51 Pegasi b this way in 1995, with a spectrograph at the Haute-Provence Observatory in France. It was the first planet found around an ordinary star like the Sun, and it was so strange, a giant planet in a four-day orbit, that many astronomers doubted it at first. Other teams, Lick among them, confirmed it within weeks. The two discoverers shared half of the 2019 Nobel Prize in Physics.

## Why this matters for Second Sun

A transit, our kind of signal, gives a planet's **size** (lesson 1.4) but not its mass. A Doppler wobble gives its **mass** (or a minimum) but not its size. Together they give its density: rock, water or gas. For eclipsing binaries, Doppler measured on both stars gives both stars' masses, which Unit 4 uses. TESS records only brightness, so it cannot see a wobble. A single dip we find someday would not give the planet's mass on its own. Spectrograph speeds are the usual route; around a binary there is a second one: a planet's pull shifts the binary's eclipse times a little, and modelling those shifts can weigh it too (Doyle et al. 2011 did this for Kepler-16).

## In a few sentences

A source moving toward or away from us shifts its spectral lines by \(\Delta\lambda / \lambda = v / c\): toward blue when it approaches, toward red when it recedes. A planet and its star both circle their centre of mass, so the star wobbles with \(M_\star v_\star = m_p v_p\). 51 Pegasi's lines swing by 55.5 m/s every 4.23 days in 354 real Lick measurements, which gives a planet of at least 0.46 Jupiter masses, the first found around a Sun-like star.

## Problems

<div class="tw-prob" data-answer="55|-55|56|-56" data-tol="0.12" data-unit="m/s" data-why="The dots near day 0 sit around -55 m/s, and near day 2.1 around +55 m/s: a swing of about 55 m/s each way." markdown>
**1.** Touch the plot near day 0. About how fast does 51 Pegasi move toward us at that point in the orbit, in m/s?

<details class="tw-sol" markdown><summary>Worked solution</summary>

About **55 m/s** toward us (the dots sit near \(-55\)). Half an orbit later, near day 2.1, it moves away at about the same speed. The fitted swing is 55.5 m/s.

</details>
</div>

<div class="tw-prob" data-answer="111|110|111.0" data-tol="0.03" data-unit="m/s" data-hints='{"27.75":"More mass pulls the star harder, not less. With the same period, K grows in step with the planet mass.","55.5":"That is the real planet. Double its mass and the swing doubles."}' data-why="With the period and star fixed, K is proportional to the planet mass: 2 x 55.5 = 111 m/s." markdown>
**2.** Suppose 51 Pegasi b were twice as heavy, with the same period. What would the star's swing \(K\) be, in m/s?

<details class="tw-sol" markdown><summary>Worked solution</summary>

From \(M_\star v_\star = m_p v_p\) with the same orbit, the star's speed grows in step with the planet's mass: \(2 \times 55.5 = 111\) m/s.

</details>
</div>

<div class="tw-prob" data-answer="12.5|12.48" data-tol="0.03" data-unit="m/s" data-hints='{"0.0125":"That is in km/s. The question asks for metres per second.","13728000":"Divide by 1,048, do not multiply: the Sun is the heavy one."}' data-why="v_sun = 13,100 m/s / 1,048 = 12.5 m/s." markdown>
**3.** Jupiter moves at 13.1 km/s and has 1/1,048 of the Sun's mass. How fast does Jupiter swing the Sun, in m/s?

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(v_\odot = v_J \times m_J / M_\odot = 13{,}100 / 1{,}048 = 12.5\) m/s. An alien astronomer with Lick's instrument could find Jupiter, given 12 years of patience.

</details>
</div>

<div class="tw-prob" data-answer="1.2e-4|0.00012|1.2×10^-4|0.000121" data-tol="0.05" data-unit="nm" data-hints='{"0.12":"That is the shift for 55.5 km/s. The swing is 55.5 metres per second, a thousand times smaller."}' data-why="55.5 / 299,792,458 = 1.85e-7; times 656.28 nm = 1.21e-4 nm." markdown>
**4.** How far does 51 Pegasi's H-alpha line (656.28 nm) move when the star moves at 55.5 m/s? Give the answer in nm.

<details class="tw-sol" markdown><summary>Worked solution</summary>

\(\Delta\lambda = 656.28 \times 55.5 / 299{,}792{,}458 = 1.21 \times 10^{-4}\) nm. That is far smaller than the line's own width, which is why the measurement needs thousands of lines and an iodine ruler.

</details>
</div>

<div class="tw-prob" data-answer="yes" data-why="Doppler gives m sin i, a minimum mass. If the orbit is tilted toward face-on, sin i is smaller and the true mass larger." markdown>
**5.** Could 51 Pegasi b be heavier than 0.46 Jupiter masses? (Yes or no.)

<details class="tw-sol" markdown><summary>Worked solution</summary>

**Yes.** Doppler measures \(m_p \sin i\). Unless the orbit is seen exactly edge-on, \(\sin i\) is less than 1 and the true mass is larger. A transit would settle it, because a planet can only transit when its orbit is nearly edge-on; 51 Pegasi b has never been seen to transit.

</details>
</div>

## Sources

- The velocities: Lick Observatory planet search, Fischer, Marcy and Spronck 2014, "The Twenty-five Year Lick Planet Search", ApJS 210, 5 ([abstract](https://ui.adsabs.harvard.edu/abs/2014ApJS..210....5F/abstract)); table 2, star HD 217014 (51 Pegasi), 354 rows, from VizieR J/ApJS/210/5 ([catalogue](https://cdsarc.cds.unistra.fr/viz-bin/cat/J/ApJS/210/5)), downloaded 23 Nov 2026 (`research/downloads.csv`). Each CCD dewar's own mean is removed before fitting (the table's note on dewars).
- Our checks, `book/tools/lesson_plots_u3c.py` (23 Nov 2026): a period search over 1 to 10 days finds 4.230799 d; the sine fit at the published period gives K = 55.50 m/s; the minimum mass comes out 0.462 Jupiter masses for a 1.07 solar-mass star. A failure of any of these stops the plot.
- Published orbit: NASA Exoplanet Archive, Planetary Systems table, 51 Peg b, read 23 Nov 2026 ([archive](https://exoplanetarchive.ipac.caltech.edu/)): default solution (Cont et al. 2026) P = 4.2307966 d, K = 55.77 m/s, star 1.07 solar masses; minimum mass 0.464 (Rosenthal et al. 2021) and 0.472 (Butler et al. 2006) Jupiter masses.
- The discovery: Mayor and Queloz 1995, Nature 378, 355 ([abstract](https://ui.adsabs.harvard.edu/abs/1995Natur.378..355M/abstract)). The 2019 Nobel Prize in Physics, half to James Peebles and half shared by Michel Mayor and Didier Queloz: [nobelprize.org](https://www.nobelprize.org/prizes/physics/2019/summary/).
- The iodine-cell method: Butler et al. 1996, "Attaining Doppler Precision of 3 m/s", PASP 108, 500 ([abstract](https://ui.adsabs.harvard.edu/abs/1996PASP..108..500B/abstract)).
- Jupiter's mass ratio (1/1,047.6) and orbital speed (13.07 km/s), Earth's (1/332,946, 29.78 km/s): NASA planetary fact sheets ([Jupiter](https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html), [Earth](https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html)). The Doppler effect, centre of mass and minimum mass: OpenStax Astronomy 2e, chapters 5 and 21 ([the book](https://openstax.org/details/books/astronomy-2e), CC BY-NC-SA 4.0), in our own words.
