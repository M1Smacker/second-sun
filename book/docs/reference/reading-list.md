# Reading list

<p class="ss-meta">Reference · the papers behind this book, each in one plain sentence</p>

!!! plain "In plain words"
    Every paper this book leans on, grouped by topic, with one sentence on what it says and how deeply we've read it. "Abstract" means we read the summary on NASA's ADS index; "title" means we only confirmed it exists and is what we say it is. Start with the ones marked ★ if you want to read real papers yourself.

| Read depth | Meaning |
|---|---|
| **abstract** | summary read on ADS (LIKELY-level facts) |
| **title** | confirmed to exist with these authors; content from other reading |
| **used** | we ran its method or tool ourselves |

## Two-star planets

| Paper | In one sentence | Depth | Chapter |
|---|---|---|---|
| ★ Doyle et al. 2011, *Science* 333, 1602 | Kepler-16 b: the first planet seen crossing two stars | title | 1, 4 |
| ★ Kostov et al. 2020, *AJ* 159, 253 | TOI-1338 b, TESS's first two-star planet: three crossings of similar depth but different lengths | abstract | 6, 12 |
| Holman and Wiegert 1999, *AJ* 117, 621 | how close to two stars a planet can orbit and survive, from thousands of simulations | used (`stability.py`) | 4, 6 |
| ★ Martin and Fabrycky 2021, *AJ* 162, 84 | STANLEY: stacking crossings that don't keep time, using simulated orbits | abstract, used | 12 |
| Wang and Liu 2024, arXiv:2404.18415 | predicted TOI-1338 b's 16 December 2025 crossing, which our search found | used (prediction scored) | 8 |
| Davies et al. 2026, *MNRAS* 548, arXiv:2604.09435 | mono-cbp: a semi-automated single-transit search of 512 detached eclipsing binaries, one weak candidate (claims F-001, F-021) | abstract, Table 2 | [prior work](prior-work.md) |
| Thornton et al. 2026, *MNRAS* 548, arXiv:2512.07934 | 27 candidate two-star planets from the slow turning of binary orbits, found by timing eclipses rather than transits | title | [prior work](prior-work.md) |
| Oddo et al. 2026, arXiv:2610.22625 | how common planets are around red-dwarf eclipsing binaries in TESS | title | [prior work](prior-work.md) |

## Missions and catalogues

| Paper | In one sentence | Depth | Chapter |
|---|---|---|---|
| Borucki et al. 2010, *Science* 327, 977 | the Kepler mission and its first results; 156,000 stars in its first weeks | abstract | 1 |
| ★ Ricker et al. 2015, *JATIS* 1, 014003 | the TESS mission: 4 cameras, a 13.7-day orbit, each star watched 1 month to 1 year | abstract | 1, 3 |
| Kirk et al. 2016, *AJ* 151, 68 | the final catalogue of Kepler's eclipsing binaries, the source of our G1 list | abstract | 1 |
| Stassun et al. 2019, *AJ* 158, 138 | the TESS Input Catalog, rebuilt on Gaia data | abstract, used (Lab 1) | 1 |
| Guerrero et al. 2021, *ApJS* 254, 39 | the TESS Objects of Interest catalogue: 2,241 candidates from the first two years | abstract | 1 |
| Gaia Collaboration 2023, *A&A* 674, A1 | Gaia's third data release: positions, distances and properties for hundreds of millions of stars | abstract | 1 |

## Finding dips honestly

| Paper | In one sentence | Depth | Chapter |
|---|---|---|---|
| ★ Pont, Zucker and Queloz 2006, *MNRAS* 373, 231 | slow, correlated (red) noise makes transits much harder to find than random-noise maths suggests | title | 7 |
| Hippke et al. 2019, *AJ* 158, 143 | wotan: the toolkit that flattens our light curves (the biweight filter) | title, used | 7, 8 |
| Kreidberg 2015, *PASP* 127, 1161 | batman: draws realistic transit shapes, used for our fake planets | title, used | 9 |
| Christiansen et al. 2013, *ApJS* 207, 35 | how Kepler measured its own search by injecting fake transits | title | 9 |
| Rein and Liu 2012, *A&A* 537, A128 | REBOUND: the N-body code inside STANLEY | title, used (via STANLEY) | 6, 12 |

## Is it real?

| Paper | In one sentence | Depth | Chapter |
|---|---|---|---|
| Bryson et al. 2013, *PASP* 125, 889 | how Kepler caught background stars faking planets, with pixel-level checks | title | 11 |
| Twicken et al. 2018, *PASP* 130, 064502 | Kepler's validation tests, including difference images and centroid offsets | title | 11 |

All were checked on NASA's ADS index on 20 October 2026. Links and exact facts are in the [claims register](../claims.md).
