# 8. Our detector: finding a dip in the noise

<p class="ss-meta">Chapter 8 · about 30 min · Maths: averages, square roots, ratios · Code: <code>pipeline/detect_v2.py</code></p>

!!! plain "In plain words"
    This program scans a light curve and points at dips that might be planets. It finds the known planet TOI-1338 b in half the sectors where it crossed {{claim:F-014}}, and it catches fake planets about 6 Earth sizes and up {{claim:F-015}}.

**What this chapter answers:** how does our search decide "this might be a planet", and how good is it?

## 8.1 The intuition

You're listening for a quiet whistle in a noisy room. A single loud clap could fool you, so you don't react to one instant. Instead you ask: "is it consistently a bit different for a few seconds?" A long, steady change is easier to pick out than a single blip, even if it's quiet.

A transit is that steady change: a small dip lasting hours. Our detector averages the light over a few hours at a time and asks whether any stretch is unusually dim compared with how much stretches normally wobble.

## 8.2 The scientific meaning

The method is a **matched filter** with a **box** shape: we slide a box-shaped template of a given length along the data and measure how dim each stretch is. The key number is the **signal-to-noise ratio (SNR)**:

<div class="ss-eq" data-eq="Eq. 8.1 · signal-to-noise ratio" markdown="1">
SNR = (how much dimmer this stretch is) ÷ (how much stretches of this length normally vary)
</div>

An SNR of 7 means "seven times bigger than a normal wobble". We use 7 as the bar, close to NASA's 7.1 {{claim:F-017}}. But a bar only means something if we **measure** how often noise alone crosses it. That's why we also run the search on flipped data (section 8.5).

## 8.3 The technical explanation

The steps, with every symbol:

1. **Mask the eclipses.** The stars eclipse each other every binary period *P*<sub>bin</sub>. We use the known *P*<sub>bin</sub> (14.6084 days for TOI-1338) and find where in that cycle the deep eclipse falls in each sector. Data within 1.5 eclipse-lengths of either eclipse is set aside. A star with more than one catalogue period (two of ours have) gets every period masked, one after the other.
2. **Flatten (detrend).** Stars and the spacecraft cause slow drifts. We fit a smooth curve with a moving window of **2 days** (a "biweight", which ignores outliers) and divide it out. The window must be much longer than a transit, or the flattening eats the dip. v1 used 1 day, which was too short for 6-hour dips.
3. **Bin.** Average the 2-minute points into **10-minute bins**. When the data itself is spaced wider (30 minutes in TESS's first two years and in Kepler), each bin is one data point wide instead.
4. **Slide boxes.** For each length *D* in 3, 4, 5, 6.5, 8, 10, 12 and 15 hours, compute the average brightness *m* of every *D*-long stretch.
5. **Score.** For each length, SNR = (*median* − *m*) ÷ *σ*<sub>D</sub>, where *σ*<sub>D</sub> is the **robust spread of all the box averages of that length** (1.4826 × the median absolute deviation, a version of the standard deviation that isn't thrown off by a few odd values).
6. **Keep peaks** with SNR ≥ 7 and merge overlapping ones into one event.

Why step 5 measures the spread from the box averages themselves: if the noise were purely random ("white"), averaging *N* points would shrink it by √*N*. Real data has slow wiggles ("red noise") that don't average away. Measuring the spread of real box averages includes those wiggles, so the SNR stays honest.

## 8.4 Our implementation (the code)

All of this is in `pipeline/detect_v2.py`, about 130 lines. The important functions:

| Function | Input | Output | What can go wrong |
|---|---|---|---|
| `load(path)` | a SPOC or QLP light-curve file | time `t`, flux `f`, number of gaps filled (and, if asked, which column it used) | missing PDCSAP data (filled from SAP); QLP needs SPOC's good stretches |
| `eclipse_mask(t, f, P, ...)` | data + binary period and eclipse lengths | which points to keep | wrong period or eclipse lengths leave eclipse edges in |
| `detrend(t, f, window_d=2.0)` | kept data | flattened flux | gaps create edge effects (Figure 8.2) |
| `box_scores(bt, bf, dur_h)` | 10-min bins, one length | box centres, SNR, box averages | too few bins → no score |
| `find_events(t, f, thr=7)` | kept data | list of events (time, length, SNR, depth) | noise bumps above 7 (false alarms) |

Running `python detect_v2.py` runs a **self-check**: 27 days of pure random noise must give no event, and a hidden 6-hour, 700 ppm dip must be found at the right time. Both pass (VERIFIED, ran on 2026-10-20).

## 8.5 Worked example: TOI-1338, sector 98

<figure markdown>
![TOI-1338 sector 98 light curve: deep eclipses every 14.6 days, and the planet transit marked near day 4025.6](img/fig4-1-s98-raw.png){ width="100%" loading="lazy" }
<figcaption>Figure 8.1. The raw light curve. The black streaks are the stars eclipsing each other (masked before searching). The amber band is TOI-1338 b's transit on 16 Dec 2025. Data: NASA TESS via MAST.</figcaption>
</figure>

<figure markdown>
![Top: flattened brightness in 10-minute bins. Bottom: box SNR for 6.5-hour boxes, crossing the threshold of 7 only at the planet transit](img/fig4-2-s98-snr.png){ width="100%" loading="lazy" }
<figcaption>Figure 8.2. After masking and flattening (top), the 6.5-hour box score (bottom) crosses 7 only at the planet. Look at the sharp swings beside gaps (near days 4024.5 and 4038.5): edges of gaps cause fake signals, one of our known weaknesses.</figcaption>
</figure>

The search finds the transit with SNR **9.0**, depth about **2,100 ppm**, about **1.1 hours** after Wang and Liu's predicted time {{claim:F-011}}.

### How good is it? Three honest tests

**1. Re-finding the known planet.** TOI-1338 b crossed in 8 sectors where we have data at the right moment. v2 finds it in **4** {{claim:F-014}}. In the 4 it misses, the dip is only 3.7 to 6.5 times the noise: below our bar.

**2. Fake planets.** We hid computer-made transits of known sizes in sector 98 and ran the search {{claim:F-015}}:

<figure markdown>
![Bar chart: v1 finds nothing below 7 Earth radii; v2 finds 6 Earth radii 5 times in 7 and everything at 7 and 8](img/fig4-3-injection.png){ width="100%" loading="lazy" }
<figcaption>Figure 8.3. Fake planets found, by size. v2 (amber) reaches about 6 Earth radii; neither version finds 5 or smaller in this star.</figcaption>
</figure>

**3. False alarms.** Turn the light curve upside down (2 − flux). Now any real dip becomes a bump, so anything the search finds is **noise or spacecraft effects**. At SNR 7, v2 still finds **6 fake events in 10 sectors**, some as strong as SNR 12.6 {{claim:F-016}}. That's why we can't just lower the bar.

### A fourth test: can we clean up the fakes automatically?

Many fake dips sit next to a **data gap** (where the spacecraft paused) or a **momentum dump** (a short thruster firing that jolts the pointing). So I tried rejecting any dip close to one. It removed 4 of the 6 fakes, but it also threw away **2 of the 4 real crossings** of TOI-1338 b: one sat 0.17 days from a thruster firing, the other 0.09 days from a gap. On this star, real and fake dips sit at the same kinds of distances, so no cut-off separates them.

So the rule became gentler. Closeness to a gap or a firing is now a **warning flag** shown to a human, not an automatic rejection. Only a dip that also appears in the flipped data is thrown out. Result: all 4 real crossings kept, and 4 of the 6 fakes carry a warning (`pipeline/veto_test.py`, VERIFIED). The lesson: with one dip at a time, you can't clean this data without losing planets. You need several dips that fit **one orbit**.

### A fifth test: the same dip in a second, independent product

Half of your G1 stars only have **QLP** light curves (made by MIT from TESS's full-frame pictures, Chapter 3). So I ran the search on QLP's version of sector 98.

- **First try: a mess.** QLP's raw light had fake dips up to **44 times the noise**, and QLP's own cleaned version shrank the planet's 2,400 ppm dip to about 700 ppm (its cleaning eats long dips). The planet was missed both ways.
- **The clue:** every strong fake sat inside stretches of time that NASA's SPOC pipeline **throws away** (scattered light that comes back at the same point in each TESS orbit). QLP keeps those stretches.
- **The fix:** use QLP's flux that keeps long dips (`sys_rm_flux`) and keep only SPOC's good stretches. Result: **one event, the planet**, at SNR 10.1 and 2,275 ppm, within about 9 minutes of where SPOC put it. Fakes dropped from 9 to 2.

That's rule C8 from Chapter 10 in action: the same dip, at the same time, in two products made by different teams. VERIFIED for this one sector; borrowing SPOC's good stretches for stars that have no SPOC file is still untested.

**Found later by an outside review (23 October):** two holes this test could not see. Before sector 56, QLP has no `sys_rm_flux`, and the loader quietly took the cleaned column that eats long dips; and data spaced 30 minutes apart filled only one 10-minute bin in three, so every box failed the coverage rule and the search returned **nothing**, with no error. Both are fixed, with checks that hide a dip at five spacings and in our real files (`pipeline/test_detect_v2_paths.py`, VERIFIED). Old QLP sectors now keep their dips, and across 650 comparisons their raw light is only about 1.2 times noisier than SPOC's (I first took one bad Kepler-16 sector, six times noisier, as typical). The lesson: a search that silently finds nothing looks exactly like a quiet star.

### A seventh test: every star, every sector (the audit)

Before searching anything, we ran the detector over all 8,100 light-curve files of all 549 stars, hiding one standard dip (8 hours, 0.3% deep) in each star-sector and checking that it came back. Nothing in it is a search.

- **Noise:** the box-averaged noise is a median of **2.5 times** what a perfectly quiet camera would give (quartiles 1.7 and 4.0). The first seven stars said 1.8; they were brighter than most.
- **What it means for planet size:** in one 6.5-hour crossing, the smallest planet we could see is below 10 Earth radii for 143 of the 549 stars and below 15 for 269. For the other 239 stars no sector gets below 15, which is bigger than any known two-sun planet (the largest is about 12). The hidden dip came back in 73% of sectors for stars brighter than magnitude 11, but in only 8% at magnitude 12 to 13.
- **False alarms:** upside down, the search made 869 fake events at SNR 7 (0.17 per star-sector). 41% of them fell at moments when three or more other stars also showed one, which points to the spacecraft; the same-moment filter flags those for a person. About 520 fakes would still be left at our bar of 7.

These are VERIFIED on the audit files (`research/audit-2026-10-23/summary.txt`), with one standard dip rather than realistic wandering crossings, so they are best cases.

### A sixth test: fake planets that move like real ones

Test 2 had a weakness: its fake planets crossed on a perfect schedule, always lasting 6.4 hours. A real planet around two suns doesn't do that (Chapter 5). So I used **STANLEY**'s own fake-planet maker, which works out each crossing with a real three-body orbit calculation. First, two bugs in STANLEY itself had to be found and worked around:

- It checked its planned crossings against the data **before** adding them, and kept only the ones that already showed a dip. With no dip there yet, it kept none. So for hours it made "fake planets" with zero crossings.
- A number was passed as a list of one item, which newer Python maths libraries refuse.

Then 6 fake planets (4, 6 and 8 Earth radii, orbits of 130 and 200 days) went into all 40 sectors of TOI-1338, giving **33 crossings** that last anywhere from 6.8 to 15.3 hours {{claim:F-029}}:

| Planet size | Dip depth | Crossings found |
|---|---|---|
| 4 Earth radii | 850 ppm | 0 of 10 |
| 6 Earth radii | 1,900 ppm | 8 of 10 |
| 8 Earth radii | 3,400 ppm | 10 of 10 |

- **Good news:** our 2-day flattening kept about **90 to 100%** of every dip's depth, even the 15-hour ones. So the cleaning step isn't eating realistic, long, irregular crossings.
- **Hidden loss:** 3 of the 33 crossings landed **inside the binary's eclipses**, which we cut out before searching. Those planets were lost before the search even looked. That's about 1 crossing in 11.
- **Same floor as before:** about 6 Earth radii, now measured with realistic crossings. No false alarms appeared.

Limits (honest): only 33 crossings, one star, one orbit angle per planet, and STANLEY never makes crossings of the **smaller** star. A proper sensitivity map needs hundreds of fake planets.

### A seventh test: does the quality filter, or the kind of flux, matter?

Our search throws away every measurement NASA flags as possibly bad (the **HARD** filter). Two published crossings of TOI-1338 b, in sectors 30 and 62, fall where that leaves **no data at all**. So we asked: would a milder filter (**DEFAULT**) let us see them?

There was a catch, found by reading the files first: in every one of those restored stretches NASA's cleaned flux (PDCSAP) is blank, and only the raw flux (SAP) exists. So the test needed three versions, changing one thing at a time:

| Arm | Flux | Filter | Compares |
|---|---|---|---|
| A0 | cleaned (PDCSAP) | HARD | our baseline, rerun and matched exactly to the saved results |
| A1 | raw (SAP) | HARD | A0 vs A1: the flux alone |
| A2 | raw (SAP) | DEFAULT | A1 vs A2: the filter alone |

The rules for reading the result were written down before anything ran (`experiments/quality_mask/SPEC.md`). Results, all on this one star:

- **The milder filter finds both missing crossings.** In sectors 62 (a measured time) and 30 (only a prediction), an event appears within 0.3 days of the published time, at 12.1 and 10.5 times the noise {{claim:F-056}}.
- **But it costs sensitivity everywhere else.** Transits that don't touch the restored data got weaker by a median of 0.5 noise units, up to 2.2. Fake 6-Earth-radius planets went from 2 found of 7 to 0 of 7, and 7-Earth-radius ones from 7 of 7 to 3 of 7 {{claim:F-057}}. Restored data is noisier and has up to 8 times the background light.
- **False alarms: undecided.** In upside-down data, events containing restored data came at about 6.8 per 100 days against about 1 per 100 days without, but with so few events the ranges overlap, so the rule we set in advance was not triggered. "Not triggered" is **not** the same as "safe" {{claim:F-058}}.
- **A surprise about the flux, not the filter.** With the same cadences, raw SAP flux found the published crossing in 7 of 8 sectors; our cleaned PDCSAP baseline found 4 {{claim:F-054}}. A follow-up check (not planned in advance, so weaker evidence) showed the transit depth is the same in both. What differs is the detector's noise estimate: in sectors 6, 34 and 37 it is 2 to 3 times larger in the cleaned flux {{claim:F-055}}. **Why is not known.**

!!! warning "What this does to earlier numbers"
    The "mostly the data" conclusion below was drawn from the cleaned flux only. On this star, part of the limit comes from how noisy the cleaned flux looks to our detector. Nothing is changed in the production detector: this is one star, two new crossings (one of them a prediction), and a few injections. The next steps are in `RESUME.md`.

## 8.6 What this lets us conclude, and what it doesn't

- **We can conclude:** the code works as designed (self-check), it finds a real planet transit when the transit is strong enough, and for a star like TOI-1338 its single-sector floor is about **6 Earth radii**.
- **We can't conclude:** that "nothing found" means "no planet". It means "nothing bigger than about 6 Earths crossed in this sector", and only for stars this bright or brighter.
- **The limit is partly the data.** The planet's missed dips are weak in the cleaned flux, and spacecraft effects make bumps as strong as real dips. But the seventh test shows that, for the same cadences, the raw flux gave the detector a quieter noise estimate in several sectors, so "mostly the data" was too strong.
- **What came next:** the gap and thruster rules became warning flags (test 4); fake planets that move like real ones were tested (test 6, and [Chapter 9](09-fake-planets.md)); and the stacked search, STANLEY, was run on TOI-1338 ([Chapter 12](12-stanley.md)). Smarter quality flags and a pixel tool are still to build.

!!! warning "Not a discovery"
    TOI-1338 b has been known since 2020. Everything in this chapter is a test of our tools on a known planet.

## 8.7 Check your understanding

The questions for this chapter are on the [Part 3 review page](../parts/part3/review.md).

## Sources
In the [claims register](../claims.md): F-011, F-014 to F-017. Full test report: `research/overnight-science/report.md`. Code: `pipeline/detect_v2.py`, `pipeline/accept_v2.py`, `pipeline/diag_v2.py`, `pipeline/book_figures.py`.
