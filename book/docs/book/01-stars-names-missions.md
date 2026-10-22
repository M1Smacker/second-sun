# 1. Stars, names and missions

<p class="ss-meta">Chapter 1 · about 20 min · Maths: powers of ten, one logarithm (explained)</p>

!!! plain "In plain words"
    Every star we study has several catalogue numbers, a position, a brightness and a distance. Two space telescopes matter to us: Kepler, which stared at one patch of sky, and TESS, which sweeps the whole sky.

**What this chapter answers:** who watched these stars, how do we name them, and how do we read their numbers?

## 1.1 The intuition

Think of a house in Kuwait City. It has a street address, a block number, a civil ID number on the land registry, and maybe a name the family calls it. Four labels, one house. Each label comes from a different office, made for a different job.

Stars are the same. **Kepler-16** is the name its discoverers gave it. **KIC 12644769** is its number in Kepler's catalogue. **TIC 299096355** is its number in TESS's catalogue. **Gaia DR3 2133476355197071616** is its number in the European star map {{claim:F-035}}. One star, four offices.

## 1.2 The scientific meaning

### How planets around other stars are found

| Method | What you see | Who uses it |
|---|---|---|
| **Transit** | the star dims when a planet passes in front | Kepler, TESS, **us** |
| **Radial velocity** | the star wobbles toward and away from us, shifting its colour slightly | big ground telescopes |
| **Timing** | a regular clock (eclipses, a pulsar) runs early and late as a planet tugs on it | used for some two-star planets |
| **Imaging** | a photo of the planet itself | only for big, young planets far from their star |

We use transits because they need only a brightness measurement, which is exactly what TESS gives away for free.

### The two telescopes

**Kepler** (NASA, 2009 to 2013 for its main mission) stared at one patch of sky of 105 square degrees, about 500 times the area of the full Moon, in the constellations Cygnus and Lyra. It watched about 200,000 objects almost without a break {{claim:F-030}}. Because it never looked away, it caught thousands of **eclipsing binaries**: pairs of stars that pass in front of each other. A team at Villanova University keeps the catalogue of them: 2,921 rows in the version we downloaded {{claim:F-038}}.

**TESS** (NASA, launched 2018) does the opposite: it sweeps almost the whole sky, one strip at a time. It circles Earth every 13.7 days, has 4 cameras, and watches each patch for about a month; stars near the poles of its sweep get up to a year {{claim:F-031}} {{claim:F-025}}. Its pixels are big, 21 arcseconds each {{claim:F-024}}, which matters a lot in Chapter 11.

**Why both matter to us:** Kepler found the binaries and timed their eclipses precisely. TESS is now re-watching many of them, years later. Our G1 campaign searches TESS data of Kepler's binaries (Chapter 5 explains why the years in between help).

### The catalogues

| Catalogue | Made by | What it holds | Example |
|---|---|---|---|
| **KIC** (Kepler Input Catalog) | Kepler team | the stars Kepler could watch | KIC 12644769 |
| **Kepler EB catalogue** | Villanova | Kepler's eclipsing binaries, with their periods | our G1 source |
| **TIC** (TESS Input Catalog) | TESS team, built on Gaia {{claim:F-032}} | about every star TESS can see, with brightness, size, distance | TIC 299096355 |
| **Gaia DR3** | European Space Agency | positions and distances of over a billion stars; detailed values for about 470 million {{claim:F-034}} | Gaia DR3 2133... |
| **TOI** (TESS Object of Interest) | TESS team | signals NASA thinks might be planets; 2,241 from the first two years {{claim:F-033}} | TOI-1338 |
| **CTOI** (Community TOI) | anyone, via ExoFOP | candidates found by outside teams, like us one day | none of ours yet |

### How planets get their names

A star system's planets get lowercase letters in order of discovery, starting at **b** ("a" is never used for a planet). TOI-1338 started as **TOI-1338.01**, a "maybe". Once it was confirmed as a planet it became **TOI-1338 b**. In a two-star system the stars are **A** (the brighter one) and **B**, and a planet orbiting both is sometimes written **(AB) b**.

## 1.3 The technical explanation

### Position: RA and Dec

The sky is treated as a giant ball around Earth. **Declination (Dec)** is latitude: +90° is above the North Pole, 0° is above the equator. **Right Ascension (RA)** is longitude, measured eastward, in degrees (0 to 360) or in hours (0 to 24, with 1 hour = 15°). Kepler-16 sits at RA 289.08°, Dec +51.76°.

Small angles use **arcminutes** (′) and **arcseconds** (″): 1° = 60′ = 3,600″. The full Moon is about 30′ across. A TESS pixel is 21″, so about 90 of them fit across the Moon.

### Brightness: magnitudes

Astronomers measure brightness backwards: **bigger numbers mean fainter**. The scale is a logarithm, so each step multiplies:

<div class="ss-eq" data-eq="Eq. 1.1 · magnitudes" markdown="1">
*m*<sub>1</sub> − *m*<sub>2</sub> = −2.5 log<sub>10</sub>(*F*<sub>1</sub> / *F*<sub>2</sub>)
</div>

- *m*: magnitude. *F*: the light we receive (flux).
- A logarithm answers "10 to what power?": log<sub>10</sub>(100) = 2.
- So **5 magnitudes = a factor of 100** in brightness, and 1 magnitude is a factor of about 2.5.

**Worked through:** your eyes reach about magnitude 6 on a dark night. Kepler-16 is 10.94, about 5 magnitudes fainter: roughly **100 times too faint to see**. Our faintest G1 stars are 13.5, about 2.6 magnitudes, or 11 times, fainter than Kepler-16. Fainter means fewer photons, which means more noise (Chapter 7).

**TESS magnitude (Tmag)** is measured through TESS's red filter, so it differs a little from the magnitudes in other catalogues.

### Distance: parsecs

A **parsec** is about 3.26 light years. Gaia measures distances by watching each star shift slightly as Earth goes around the Sun (**parallax**). Kepler-16 is 75 parsecs away {{claim:F-035}}: about 245 light years. The light we measured in 2024 left it around the year 1780.

### Time: BJD and BTJD

Light from a star reaches the Sun and Earth at slightly different moments, up to about 8 minutes apart. So astronomers convert every time to when the light would have reached the **Sun's** centre of mass (the solar system's balance point): the **Barycentric Julian Date (BJD)**, a count of days. Those numbers are huge (2,460,000 and more), so TESS subtracts 2,457,000: **BTJD**. BTJD 0 is 8 December 2014. Kepler's catalogue uses a different offset (BJD − 2,400,000), which is why our G1 list has times like 55002.78.

## 1.4 Our implementation

The G1 list, `targets/g1_targets.csv`, is the catalogue work done once and frozen:

| Column | Meaning | From |
|---|---|---|
| `kic` | Kepler's number | Villanova catalogue |
| `tic` | TESS's number | looked up in the TIC at MAST |
| `tmag` | TESS magnitude | TIC |
| `p_bin_d` | how many days the two stars take to orbit each other | Villanova |
| `bjd0` | the time of one eclipse (BJD − 2,400,000) | Villanova |
| `morph` | 0 = clean, separate eclipses; 1 = stars touching | Villanova |

The selection rule keeps `morph < 0.5` (stars clearly separate), `p_bin_d > 5` days (room for a stable planet, Chapter 4) and `tmag ≤ 13.5` (bright enough to see a planet). That leaves 552 rows: 549 stars, because 3 stars have two binary periods each {{claim:F-038}}.

!!! warning "Found on 20 October: a hole in the rule"
    Kepler's catalogue writes **morph = −1** when it couldn't measure a binary's shape. "−1 < 0.5" is true, so our rule let those stars in: **136 of the 552 rows** {{claim:F-052}}. One of them showed no eclipse at all in TESS data. Lesson: a "missing value" code inside a number column must be handled on purpose. The fix is your decision when the hunt resumes; it's in the decision log.

The top of the file records the fingerprints (sha256) of the source files, so anyone can check the list wasn't changed.

## 1.5 Worked example: Kepler-16's identity card

From [Lab 1](../labs/lab1-name-to-number.md), run on your PC {{claim:F-035}} {{claim:F-036}}:

| | |
|---|---|
| Names | Kepler-16 · KIC 12644769 · TIC 299096355 · Gaia DR3 2133476355197071616 |
| Position | RA 289.08°, Dec +51.76° (Cygnus) |
| Brightness | Tmag 10.94: invisible to the eye, bright for TESS |
| Distance | 75 parsecs (about 245 light years) |
| Neighbours | 15 stars within 1′; 4 bright enough to matter |
| TESS data | 94 light curves from 6 teams, sectors 14 to 83 |
| Famous for | the first transiting planet found orbiting two stars, in 2011 {{claim:F-002}} |

## 1.6 What this lets us conclude, and what it doesn't

- **We can:** find any star's numbers, brightness, distance and available data in under a minute.
- **We can't:** fully trust catalogue values for **binaries**. The TIC treats Kepler-16 as one star of 4018 K, but the light is a blend of two stars. Sizes and temperatures for our G1 stars are blended guesses.
- **Names are pointers, not facts.** A star with a TOI number is not a planet host until confirmed.

## 1.7 Check your understanding

The questions for this chapter are on the [Part 1 review page](../parts/part1/review.md).

## Sources
In the [claims register](../claims.md): F-002, F-024, F-025, F-030 to F-038. Background: magnitude scale, Pogson 1856; Borucki et al. 2010; Ricker et al. 2015; Stassun et al. 2019; Guerrero et al. 2021 (all checked on ADS).
