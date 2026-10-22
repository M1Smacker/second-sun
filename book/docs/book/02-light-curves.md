# 2. Light curves: seeing planets as shadows

<p class="ss-meta">Chapter 2 · about 25 min · Maths: fractions, percentages, ppm, squares, averages</p>

!!! plain "In plain words"
    We cannot photograph these planets, so we watch a star's brightness over time. When a planet passes in front, the star dims a little: that is a transit.

**What this chapter answers:** how does a brightness graph reveal a planet, and how does the TESS telescope collect that graph?

## 2.1 The intuition

Stand at night and look at a distant streetlight. A moth flies across it. You can't see the moth, but for a moment the light looks a touch dimmer. If you'd been measuring the light with a meter every few seconds, you'd see a small notch in the readings. The size of the notch tells you how big the moth is compared with the lamp.

The star is the lamp. The planet is the moth. TESS is the meter.

## 2.2 The scientific meaning

A **[light curve](../glossary.md#light-curve)** is a list of (time, brightness) pairs. For a star with no planet and no partner, it's roughly flat, with random jitter (noise). A **[transit](../glossary.md#transit)** shows as a dip with a flat bottom: the planet slides on, sits fully in front, slides off.

Three numbers describe a transit:

| Number | Meaning | What it tells us |
|---|---|---|
| **Depth** | how much dimmer the star gets | the planet's size compared with the star |
| **Duration** | how long the dip lasts | how fast the planet moves across, and the path it takes |
| **Time** (mid-point) | when it happens | for single-star planets, the period; for two-sun planets, a timing pattern (Chapter 5) |

## 2.3 The technical explanation

### Depth and size

The planet blocks a disc of light. The fraction blocked is the planet's disc area divided by the star's disc area. Area grows with radius squared, so {{claim:F-013}}:

<div class="ss-eq" data-eq="Eq. 2.1 · transit depth" markdown="1">
depth ≈ (*R*<sub>p</sub> / *R*<sub>★</sub>)²
</div>

- *R*<sub>p</sub>: the planet's radius (centre to edge).
- *R*<sub>★</sub>: the star's radius.

Depths are tiny, so we use **ppm** (parts per million): 1% = 10,000 ppm. Earth crossing the Sun: (1/109)² ≈ 0.000084 = **84 ppm**. Jupiter crossing the Sun: about 1% = **10,000 ppm**.

Turning it around gives the planet's size from a measured depth: *R*<sub>p</sub> = *R*<sub>★</sub> × √depth.

### How TESS collects light curves

TESS is a NASA space telescope that stares at one big patch of sky for about **27 days** (a **[sector](../glossary.md#sector)**), then moves on {{claim:F-012}}. It records brightness two ways:

- **Full-frame images** of the whole patch: every 30 minutes (sectors 1-26), every 10 minutes (27-55), every 200 seconds (56 onward) {{claim:F-012}}.
- **2-minute "postage stamps"** for selected stars, which NASA's SPOC pipeline turns into ready-made light curves. Most of our tests use these.

The SPOC light curves come in two versions you'll meet in our code:

- **SAP** (simple aperture photometry): the raw sum of light in the star's pixels.
- **PDCSAP**: SAP with known spacecraft effects removed. Cleaner, but occasionally missing data where SAP is fine. Detector v2 fills those gaps from SAP (Chapter 8).

### Noise

Every measurement jitters. For a star like TOI-1338 (TESS magnitude about 11.5), one hour of 2-minute data scatters by roughly **400 to 550 ppm** in our measurements (overnight test, `pipeline/diag_v2_results.json`). A planet's dip has to stand clearly above that, which is the subject of Chapter 8.

## 2.4 Our implementation

In `pipeline/detect_v2.py`, the function `load(path)`:

1. reads a SPOC light-curve file with lightkurve, dropping cadences flagged as bad ("hard" quality mask);
2. divides by the median so "normal brightness" = 1.0;
3. fills PDCSAP gaps from SAP, scaled to match nearby data;
4. returns `t` (time in BTJD, the TESS day count) and `f` (relative flux).

BTJD = BJD − 2,457,000. For example, BTJD 4025.6 is 16 December 2025.

## 2.5 Worked example: two kinds of dip in TOI-1338

TOI-1338's light curve shows dips of very different sizes:

| Dip | Depth | Cause |
|---|---|---|
| Primary eclipse, every 14.6 days | about **5.1%** (51,000 ppm) | the small star passes in front of the big one |
| Secondary eclipse | about **0.4%** | the big star covers the small one |
| 16 Dec 2025, once | about **0.24%** (2,400 ppm), ~6.4 h | the planet TOI-1338 b {{claim:F-011}} |

Check the planet with the formula: TOI-1338 b is about 6.9 Earth radii {{claim:F-003}}, and the big star is about 1.3 Sun radii (the value used in our injection test). In Earth radii the star is 1.3 × 109 ≈ 142. So depth ≈ (6.9 / 142)² ≈ 0.0024 = **2,400 ppm**. That matches what our search measured.

## 2.6 What this lets us conclude, and what it doesn't

- **A dip is not a planet.** Spacecraft effects, star spots, the other star, or a faint background binary can all make dips. Chapter 8 and the vetting chapter deal with that.
- **Depth gives a size only relative to the star.** If the star's size is wrong, or another star's light dilutes the dip, the planet size is wrong too.
- **One sector is a short window.** Two-sun planets often cross only once per sector or not at all, which is why the next chapter matters.

## 2.7 Check your understanding

The questions for this chapter are on the [Part 1 review page](../parts/part1/review.md).

## Sources
In the [claims register](../claims.md): F-003, F-011 to F-013. Background: Winn 2010, "Transits and Occultations", [arXiv:1001.2010](https://arxiv.org/abs/1001.2010).
