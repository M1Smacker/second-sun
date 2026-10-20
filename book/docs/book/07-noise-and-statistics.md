# 7. Noise and statistics: when is a dip real?

<p class="ss-meta">Chapter 7 · about 20 min · Maths: averages, square roots, one probability</p>

!!! plain "In plain words"
    Every measurement wobbles. A dip only counts if it's clearly bigger than the wobble, measured over the same length of time as the dip. Averaging many measurements shrinks random wobble, but not slow drifts, and slow drifts are exactly what fakes a planet. And if you look in thousands of places, a few will look like dips by pure chance. This chapter is about those three facts.

**What this chapter answers:** how big is the noise, why doesn't averaging always help, and how do we set a bar that noise rarely crosses?

## 7.1 The intuition

You weigh yourself on a cheap bathroom scale. It says 71.3, then 70.8, then 71.1. Each reading wobbles, but the **average** of 30 readings is much steadier than any one. That's random noise, and averaging beats it.

Now imagine the floor slowly tilts during the morning. All 30 readings drift together. Averaging them doesn't remove the tilt: you get a steady, **wrong** number. That's correlated noise, called **red noise**, and averaging can't beat it.

A planet's dip lasts hours. So the question is never "how much does one reading wobble?" It's "how much does a **few-hour average** wobble?" Slow drifts decide that.

## 7.2 The scientific meaning

### Where the wobble comes from

- **Photon noise.** Light arrives as separate particles (photons). Counting them is like counting raindrops in a bucket: the count naturally varies by about its square root. Brighter stars give more photons, so relatively less noise.
- **The telescope.** Pointing jitter, heating, thruster firings, scattered light from Earth and Moon (Lab 2's quality flags).
- **The star itself.** Stars have spots, flares and boiling surfaces (granulation) that change their brightness slowly.

### White and red noise

**White noise:** each measurement's wobble is independent of the last one. Averaging *N* of them shrinks the wobble by √*N*.

**Red noise:** neighbouring measurements wobble together. Averaging helps much less. Real TESS data always has some, and red noise makes transit searches much harder than white-noise maths suggests {{claim:F-042}}.

### Signal-to-noise ratio

The **signal-to-noise ratio (SNR)** compares the dip's depth with the wobble of an average over the dip's length. SNR 7 means the dip is 7 times bigger than a typical few-hour wobble. NASA's planet search uses a bar of 7.1 {{claim:F-017}}; ours is 7.

### The look-elsewhere effect

If you check one spot, a 7-times wobble is incredibly rare. But a search checks **every** time and **every** dip length: thousands of tries per sector. Rare things happen when you try often enough. That's why our search also runs on **upside-down data** (Chapter 8): it counts how many fakes noise produces with the same number of tries.

## 7.3 The technical explanation

### Measuring the wobble robustly

The **standard deviation** (σ) is the usual measure of spread, but one wild point can inflate it. We use a **robust** version that ignores a few outliers:

<div class="ss-eq" data-eq="Eq. 7.1 · robust spread" markdown="1">
σ ≈ 1.4826 × median( | *x* − median(*x*) | )
</div>

- Take each value's distance from the middle value, then the middle of those distances (the **MAD**, median absolute deviation).
- The factor 1.4826 makes it equal σ for well-behaved (bell-curve) noise.

### Averaging

<div class="ss-eq" data-eq="Eq. 7.2 · white-noise averaging" markdown="1">
σ<sub>*N*</sub> = σ<sub>1</sub> / √*N*
</div>

- σ<sub>1</sub>: the wobble of one measurement. σ<sub>*N*</sub>: the wobble of an average of *N* measurements.
- Example: 2,015 ppm per 2-minute point, averaged over 1 hour (*N* = 30): 2,015 / √30 ≈ **368 ppm**, **if** the noise were white.

### SNR

<div class="ss-eq" data-eq="Eq. 7.3 · signal-to-noise" markdown="1">
SNR = depth / σ<sub>*D*</sub>
</div>

- σ<sub>*D*</sub>: the wobble of an average over the dip's duration *D*, **measured**, not computed with Eq. 7.2.
- Our detector measures σ<sub>*D*</sub> directly: it takes every possible *D*-hour average in the sector and measures their robust spread. Red noise is automatically included.

### How rare is 7σ?

For pure bell-curve noise, the chance of one average falling 7σ below normal is about **1 in 780 billion**. A sector gives our search tens of thousands of tries (thousands of ten-minute positions × 8 box lengths). Pure white noise would almost never cross the bar. Yet on upside-down TOI-1338 data, noise crossed it **6 times in 10 sectors** {{claim:F-016}}. That's the strongest evidence that real TESS noise isn't white or bell-shaped: it has slow drifts and sudden jumps.

## 7.4 Our implementation

In `pipeline/detect_v2.py`:

| Function | What it does | Why |
|---|---|---|
| `detrend()` | flattens slow trends with a 2-day "biweight" filter (from the `wotan` toolkit) | removes star spots and drifts, but keeps dips up to 15 hours (Chapter 9 measured 90 to 100% kept) |
| `bin10()` | averages into 10-minute bins | fewer, steadier points |
| `box_scores()` | for each length *D*, measures the robust spread of all *D*-hour averages: σ<sub>*D*</sub> | red-noise-aware SNR |
| `find_events()` | keeps boxes with SNR ≥ 7 | the bar |

**A trade-off to understand:** a shorter flattening window removes more red noise, but it also eats long dips. Version 1 of our detector used a 1-day window and lost real transits. Version 2 uses 2 days (Chapter 8).

## 7.5 Worked example: one star, four noise numbers

Kepler-16, sector 82, one hour of data, measured on your PC {{claim:F-039}} (and in [Lab 3](../labs/lab3-plot-and-read.md)):

| Method | One-hour noise |
|---|---|
| lightkurve's quick estimate (flattens with a 3.4-hour window) | **229 ppm** |
| NASA's own estimate, stored in the file header ("CDPP") | **542 ppm** |
| our binned scatter after a 0.25-day flatten | **573 ppm** |
| our binned scatter after a 2-day flatten (what our detector sees) | **908 ppm** |
| what white noise would give (Eq. 7.2) | 368 ppm |

**Same data, a factor of 4 apart.** The quick estimate flattens so hard that it removes most of the slow wobble. It even lands *below* the white-noise value, which is a warning sign by itself. Our own 19 October report used that quick number (236 ppm), and it fed an early claim that we could find planets of 2 to 5 Earth radii. Injection tests later measured the real floor: about 6 {{claim:F-015}}. **Corrected and logged.**

The lesson: a noise number means nothing without the method. Quote the one that matches how your search sees the data, and check it against the file's own CDPP.

## 7.6 What this lets us conclude, and what it doesn't

- **We can:** measure the noise our search actually faces, and set a bar whose false-alarm rate we've measured (upside-down data).
- **We can't** assume bell-curve maths. 7σ is not "one in 780 billion" in real TESS data.
- **Not yet known (NOT TESTED):** how much of Kepler-16's extra hour-scale noise is the stars themselves and how much is the spacecraft. Comparing quiet and noisy sectors would tell us.

## 7.7 Check your understanding

??? quiz "1. One point wobbles by 1,000 ppm. With white noise, what does a 4-hour average (120 points) wobble by?"
    1,000 / √120 ≈ **91 ppm**.

??? quiz "2. You measure 400 ppm for that 4-hour average instead. What does that tell you?"
    The noise is **red**: slow drifts that don't average away. A dip must be judged against 400 ppm, not 91.

??? quiz "3. Why does running the search on upside-down data help?"
    It makes the same number of tries on data with no real dips. Whatever it finds shows how often noise alone crosses the bar: the look-elsewhere effect, measured.

??? quiz "4. Why not just flatten with a 3-hour window to get rid of red noise?"
    It would also flatten the planet: a 6-to-15-hour two-star transit would be partly removed.

**Next:** [Chapter 8: our detector](08-our-detector.md).

## Sources
In the [claims register](../claims.md): F-015, F-016, F-017, F-027, F-039, F-042. Background: Pont, Zucker and Queloz 2006 (red noise); Hippke et al. 2019 (wotan detrending), both checked on ADS.
