# 12. STANLEY: the professionals' tool

<p class="ss-meta">Chapter 12 · about 20 min · Maths: square roots, a grid of guesses</p>

!!! plain "In plain words"
    Each crossing of a small two-star planet is too faint to see alone, and they do not arrive on a timetable. STANLEY guesses a whole orbit, predicts every crossing, and adds up the light at those moments.

**What this chapter answers:** what is STANLEY, why does it need a real orbit calculation, what did it say about TOI-1338 on your PC, and why don't we trust its scores yet?

## 12.1 The intuition

You're listening for a faint drummer in a noisy room. Each beat is too quiet to hear. If the drummer kept perfect time, you could add up the sound at every beat and the rhythm would appear. That's how normal planet searches work: they stack dips that repeat on a timetable.

Our drummer doesn't keep time: the beats come early and late, some long, some short (Chapter 6). But if you knew the drummer's **pattern**, you could still add the sound at exactly the right moments. STANLEY tries thousands of possible patterns and checks which one makes the rhythm appear.

## 12.2 The scientific meaning

- **The problem.** No two-star planet smaller than 3 Earth radii had been found, though such planets make up over 75% of discoveries around single stars. They're not necessarily rare: they're hard to find, because their timing shifts are bigger than their crossings are long {{claim:F-044}}.
- **The idea.** For each guessed orbit (period, starting position, and optionally eccentricity), run an N-body simulation (Chapter 6), get every predicted crossing time and length, and stack the light curve at those moments.
- **The authors.** David Martin and Daniel Fabrycky described STANLEY in 2021. Run on Kepler's two-star systems, it found every known planet, including all three of Kepler-47's, and showed planets under 3 Earth radii could have been found in half of them {{claim:F-044}}. The software is published under the MIT licence by Martin's group at Tufts University; version 0.2.8 is installed on your PC.
- **The three stages.**
    1. **Detrending:** fits the binary, removes the eclipses, flattens the light curve.
    2. **Search:** the grid of guessed orbits, each given a score in σ.
    3. **Analysis:** reads the grid, ranks the best orbits, and checks them.

## 12.3 The technical explanation

### Why stacking helps

If each of *N* crossings has SNR *s* on its own, and the noise is white, the stack has SNR ≈ *s* × √*N*. Four crossings of SNR 3 make an SNR-6 stack; nine make 9. That's how STANLEY reaches planets our one-dip-at-a-time search can't.

### The grid

Every guess is an orbit. Our TOI-1338 run tried {{claim:F-045}}:

| Setting | Values |
|---|---|
| Planet period | 173 steps from 90.05 to 100.03 days |
| Starting angle (where on its orbit the planet starts) | up to 123 steps around the full circle |
| Eccentricity | 0 only (circular): a quick test |
| Total | **20,482 orbits**, in 33 minutes |

A full search would add eccentricities and orientations, and many more periods. Grids grow fast: that's the price of not knowing the orbit.

### Scores and the look-elsewhere problem

Each orbit gets a score in σ: how much darker the stacked crossings are than normal, compared with the noise. But with 20,482 tries, high scores happen by chance (Chapter 7). On your PC, the **typical** score was 4.2σ and **28%** of all orbits scored above 5σ {{claim:F-045}}. So here "5σ" doesn't mean "rare". The scale must be **calibrated**: run the same grid on data with no planet (flipped, or shuffled), see how high pure noise scores, and set the bar above that.

## 12.4 Our implementation

STANLEY needed six fixes to run on your PC. Each one is in our wrapper scripts, not in STANLEY's own code:

| Problem | Fix | Where |
|---|---|---|
| Python 3.12 dropped a module (`distutils`) that `batman` needs | installed `setuptools` | STANLEY's environment |
| It downloaded data to C: | wrapper forces the cache to D: before anything downloads | `pipeline/stanley/run_detrend.py` |
| `np.product` removed in newer numpy | one-line stand-in | `run_search.py` |
| The fake-planet maker used a 1-second time limit | raised to 600 s | `inject_cbp.py` |
| The fake-planet maker kept only crossings that already showed a dip, so it injected **zero** | take crossing times straight from the N-body step | `inject_cbp.py` |
| A one-item list passed where a number is needed | return a plain number | `inject_cbp.py` |

The last two were found by calling STANLEY's pieces one at a time (field note, 20 October).

## 12.5 Worked example: STANLEY on TOI-1338

From [Lab 8](../labs/lab8-read-stanley.md), run on your PC {{claim:F-045}}:

<figure markdown>
![Left: best score per trial period with a sharp peak of 18.4 sigma at 96.1 days, near the dashed line at 95.2 days. Right: histogram of all scores, peaking around 4 to 5 sigma](../labs/img/lab8-stanley-toi1338.png){ width="100%" loading="lazy" }
<figcaption>STANLEY's search of TOI-1338 (40 sectors, circular orbits). Left: the best score at each trial period; red dashed line: the real planet's 95.2 days {{claim:F-047}}. Right: every orbit's score.</figcaption>
</figure>

- **The peak: 18.4σ at 96.11 days**, the next-best 16.3σ at 96.16 days. The real planet's period is 95.2 days.
- **Why not exactly 95.2?** Our grid only tried circular orbits (the real one has e ≈ 0.09, Kostov et al. 2020), and STANLEY's own fit gave the stars slightly different masses (1.2 and 0.325 Suns, against the published 1.1 and 0.3). A slightly wrong model shifts the best guess.
- **The histogram:** most orbits score 2 to 8σ just from noise and leftover wiggles. 18.4σ is far out on its own, which is encouraging. But until the scale is calibrated, it's a pointer, not a result.

!!! warning "Corrected, 20 October 2026"
    Our overnight report first said the peak was at 93.8 days. The search log prints the period range from high to low, but the results file runs low to high. Lab 8 now reads the periods from STANLEY's saved grid file and checks that its row lengths match. Logged in the mistakes register.

## 12.6 What this lets us conclude, and what it doesn't

- **We can:** run STANLEY on your PC, and it points close to the real planet's period with a strong score.
- **We can't yet:** say how significant 18.4σ is (no calibration), or claim a "recovery" (circular grid, uncalibrated): still uncertain.
- **Not done yet (not tested):** STANLEY's analysis stage, a calibrated run, and any G1 star.
- **Where it fits:** our fast detector screens all 549 G1 stars for single strong dips; STANLEY is the slow, deep search for small planets on the most promising binaries.

## 12.7 Check your understanding

The questions for this chapter are on the [Part 5 review page](../parts/part5/review.md).

## Sources
In the [claims register](../claims.md): F-044, F-045, F-047. Martin and Fabrycky 2021, "Searching for Small Circumbinary Planets. I." (AJ 162, 84); Rein and Liu 2012 (REBOUND); both checked on ADS.
