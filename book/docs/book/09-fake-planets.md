# 9. Fake planets: injection and recovery

<p class="ss-meta">Chapter 9 · about 20 min · Maths: fractions, one square root</p>

!!! plain "In plain words"
    How do you know what your search can find? You hide fake planets of known sizes in real data, run the search, and count how many it finds. That's **injection and recovery**. It turns "we found nothing" into "nothing bigger than about 6 Earth sizes crossed here". Without it, an empty result means nothing at all.

**What this chapter answers:** how do we measure a search, what makes the test honest, and what have our tests shown so far?

## 9.1 The intuition

A teacher wants to know whether a metal detector works on the school field. She doesn't just walk around and say "nothing beeped, so there's no metal". She buries coins of different sizes at places she's marked, walks the field, and counts which coins beeped. Now "nothing beeped" means something: no coin bigger than the smallest one it reliably finds.

Our coins are fake planets. The field is real TESS data.

## 9.2 The scientific meaning

- **Injection:** add a computer-made transit to the real light curve. It must go in **before** any cleaning, so the test includes everything that could damage a real dip.
- **Recovery:** run the complete search and check whether an event appears at the right time.
- **Recovery fraction:** found ÷ hidden, for each planet size. Plotted against size, it shows the search's **floor**: the smallest planet it finds most of the time.
- **Professionals do this.** NASA's Kepler pipeline measured its own efficiency by injecting fake transits into its real pixel data {{claim:F-051}}. Every claimed "no planets here" in the literature leans on a test like this.

### What makes the test honest

Compass (20 October) listed what a weak injection test gets wrong. Our first test had all five:

| Weakness | Why it matters | Fixed? |
|---|---|---|
| Fakes on a perfect timetable, all the same length | real two-star crossings wander and change length (Chapter 6) | **yes**: STANLEY-timed fakes |
| Fakes never placed inside the eclipse mask | planets lost to masking were invisible in the counts | **yes**: now counted separately |
| Too few trials | a recovery fraction from 7 trials is very uncertain (9.3) | **not yet** |
| Injected into already-cleaned NASA data (PDCSAP) | NASA's own cleaning isn't tested | **not yet** |
| One star, one sector | another star's noise is different | **not yet** |

## 9.3 The technical explanation

### Making a realistic dip

A planet blocks a fraction of the star's light: about (planet radius ÷ star radius)² (Chapter 2). But a star's edge looks darker than its centre (**limb darkening**), so a planet crossing the middle blocks a brighter patch, and the dip's centre is **deeper** than that simple formula. The `batman` toolkit (Kreidberg 2015) draws the full shape: a curved bottom and gradual edges.

### How sure is a recovery fraction?

If the true recovery rate is *p* and you try *N* times, the count you get wobbles:

<div class="ss-eq" data-eq="Eq. 9.1 · uncertainty of a fraction" markdown="1">
σ<sub>*p*</sub> = √( *p* (1 − *p*) / *N* )
</div>

- 8 found out of 10: *p* = 0.8, σ = √(0.8 × 0.2 / 10) = 0.13, so **80% ± 13%**.
- 1 found out of 4: 25% ± 22%. Four trials can't tell 25% from 50%.
- For ± 3%, you need about 200 trials per size. That's why the next test is "hundreds of planets".

### Timing the fakes like real ones

STANLEY's N-body code (Chapter 6) gives each fake planet real crossing times and lengths. Our wrapper takes those times, and STANLEY's injector adds a `batman` shape at each one. Getting it working took finding a bug: its injector threw away every crossing (Chapter 12).

## 9.4 Our implementation

| Script | What it does |
|---|---|
| `pipeline/accept_v2.py` | the first test: 49 fakes on a timetable, TOI-1338 sector 98 |
| `pipeline/stanley/inject_cbp.py` | STANLEY-timed fakes into all 40 TOI-1338 sectors |
| `pipeline/recover_cbp.py` | runs our search on each, scores every crossing: found, missed, in a gap, or inside the eclipse mask; measures how much depth survives cleaning |
| `labs/lab6_fake_planets.py` | your version: 20 fakes, 5 sizes, 4 times |

## 9.5 Worked example: three tests, one answer

| Test | Fakes | Found at 6 Earth radii | Found at 4 | Depth kept |
|---|---|---|---|---|
| Timetable fakes, sector 98 {{claim:F-015}} | 49 | 5 of 7 | none | not measured |
| STANLEY-timed, 40 sectors {{claim:F-029}} | 33 crossings | 8 of 10 | 0 of 10 | 90 to 100% |
| Your Lab 6, sector 98 {{claim:F-048}} | 20 | 4 of 4 | 0 of 4 | 92 to 96% |

**Three different tests agree:** our search reliably finds single crossings of planets about **6 Earth radii** and bigger around a star like TOI-1338, and almost never smaller than 5. The 2-day cleaning keeps over 90% of a real dip's depth, even for 15-hour crossings.

And one new loss: **3 of 33** realistic crossings fell inside the stars' eclipses, so they were cut out before the search looked {{claim:F-029}}. About 1 crossing in 11 is invisible to us whatever its size.

## 9.6 What this lets us conclude, and what it doesn't

- **We can say:** "for TOI-1338-like stars, nothing bigger than about 6 Earth radii crossed in the searched data, apart from the known planet, with about 1 crossing in 11 hidden by eclipses".
- **We can't** say anything about planets smaller than 5 Earth radii from single crossings. That's what stacking (STANLEY, Chapter 12) is for.
- **We can't** yet give these numbers for fainter G1 stars. Each brightness level needs its own test.

## 9.7 Check your understanding

??? quiz "1. Why must fakes go in before cleaning, not after?"
    Cleaning can flatten part of a real dip. Injecting after cleaning would skip that damage, so the test would look better than reality.

??? quiz "2. 3 of 4 fakes found. What's the uncertainty?"
    √(0.75 × 0.25 / 4) ≈ 0.22: **75% ± 22%**. Four trials are far too few.

??? quiz "3. Why count fakes inside the eclipse mask separately?"
    They show a loss no detector improvement can fix. Mixing them into "missed" would blame the detector for what the mask did.

??? quiz "4. A dip's centre is deeper than (radius ratio)². Why?"
    **Limb darkening:** the star's edge is dimmer, so a planet over the bright middle blocks more light than the average.

**Next:** [Lab 6: hide your own fake planets](../labs/lab6-fake-planets.md), then Part 4, [Chapter 10](10-vetting.md).

## Sources
In the [claims register](../claims.md): F-015, F-029, F-048, F-051. Background: Kreidberg 2015 (batman, PASP 127, 1161); Christiansen et al. 2013 (Kepler injection); both checked on ADS.
