# 6. Our data: from a NASA telescope to your D: drive

<p class="ss-meta">Chapter 6 · about 20 min · Maths: megabytes and gigabytes, ppm</p>

!!! plain "In plain words"
    Ahmed, every number in this book starts as light hitting a camera on NASA's TESS satellite. NASA turns those pictures into brightness records and puts them online for free. Our Python code downloads them to your D: drive, about 1-2 MB per star per month of watching. This chapter follows that path step by step, so you know exactly what our data is, where it comes from, and what can go wrong with it.

**What this chapter answers:** what data do we use, how does it reach your PC, and how good is it?

## 6.1 The intuition

Think of a security camera that photographs a whole car park every few minutes. Later, someone goes through the photos and, for each parked car, writes down how bright its headlights looked in each photo. You get the notebook, not the photos. That notebook is a **light curve**. If you ever need to check something the notebook can't tell you, you can go back to the photos (the **pixels**).

## 6.2 The scientific meaning

TESS has **4 cameras**, each seeing a 24 × 24 degree patch of sky, with 4 detector chips of 2048 × 2048 pixels each. One pixel covers about **21 arcseconds** {{claim:F-024}}. That's a big pixel: several stars can share one, which is why the "neighbour" test in Chapter 5 matters.

TESS circles Earth every **13.7 days** and watches each patch for about 27 days (a sector). Stars near the ecliptic poles get watched for up to a year {{claim:F-025}}.

The data comes in three layers:

| Layer | What it is | Size per star per sector (measured) {{claim:F-026}} | When we use it |
|---|---|---|---|
| **Light curve** (SPOC, QLP, TESS-SPOC) | the brightness notebook, ready-made | 0.7-2 MB | almost always |
| **Target pixel file** | the small stack of pixels around one star, every cadence | ~50 MB | checking where a dip comes from (Chapter 5, C6) |
| **TESScut cutout** | a square of pixels cut from the full-frame images | ~11-50 MB | faint stars with no ready-made light curve |

Your rule from 19 October: we keep light curves, but cutouts are deleted after we extract what we need, because NASA keeps the originals.

## 6.3 The technical explanation

### Who makes the light curves

- **SPOC** (NASA Ames): for stars given 2-minute "VIP" pixels; the cleanest, used for most of our tests.
- **QLP** (MIT Quick-Look Pipeline): for many more stars, from the full-frame images.
- **TESS-SPOC**: SPOC's version made from full-frame images.

They are made independently, which is why rule C8 asks for a dip in at least two of them.

### How good is the data?

On Kepler-16, a fairly bright star in our G1 field (TESS magnitude 10.94), one hour of data scatters by **236 ppm** (SPOC), **279 ppm** (TESS-SPOC) or **293 ppm** (QLP) {{claim:F-027}}. Fainter stars are noisier. In Chapter 4 we measured ~420-540 ppm per hour for TOI-1338 with our own method.

### Known troublemakers in the data

- **Momentum dumps:** every 2-6 days TESS fires thrusters; the cadences are flagged (quality bit 32) {{claim:F-028}}. Chapter 4 showed fakes cluster near them.
- **Data gaps:** downlinks to Earth every orbit leave holes; edges of holes are where detrending goes wrong.
- **Scattered light** from the Earth and Moon near the ends of orbits.

## 6.4 Our implementation

- Downloads use **lightkurve** (a Python package), always into `D:\second-sun\data\` or `D:\second-sun\.cache\`, never C:.
- Every download is logged in `research/downloads.csv` (what, from where, size, why).
- Your PC's **Avast** antivirus intercepts secure web connections. Python is told to trust the Windows certificate list (a package called `truststore`), inside the project only. Avast itself is untouched.
- Third-party tools get checked first. On 20 October, STANLEY tried to download to C:; it was caught before any file landed, and now a wrapper forces its downloads onto D: (logged in the mistakes register).

## 6.5 Worked example: what it cost to test STANLEY on TOI-1338

TOI-1338 sits near the south ecliptic pole, so TESS has watched it a lot: **40 sectors** of 2-minute data. At about 2 MB each, that's **78 MB** in total, which is small. The same star as raw cutouts would be roughly 40 × 30 MB ≈ **1.2 GB**. That gap is why we prefer ready-made light curves.

## 6.6 What this lets us conclude, and what it doesn't

- **The data is free and reachable from your PC,** and light curves are small enough that even hundreds of stars fit easily on D:.
- **A light curve hides choices.** Each pipeline cleaned the data its own way. A dip in only one product could be that product's artefact.
- **Big pixels mean blends.** A dip can come from a neighbour inside the same 21-arcsecond pixel. Light curves alone can't rule that out; pixels can.

## 6.7 Check your understanding

??? quiz "1. Why do we need a dip in two different light-curve products?"
    Each pipeline cleans data differently. A dip in only one could be created by that pipeline's cleaning, not by the star.

??? quiz "2. A light curve is 2 MB. Roughly how much space do 550 stars × 10 sectors take?"
    550 × 10 × 2 MB = **11,000 MB ≈ 11 GB**. Easy for D:.

??? quiz "3. Why are TESS's big pixels a problem for planet hunters?"
    A faint eclipsing binary next to our star can sit in the same pixel and leak its dips into our light curve, faking a small planet.

## Sources
In the [claims register](../claims.md): F-024 to F-028. Full research: `research/wave-2-data/report.md`.
