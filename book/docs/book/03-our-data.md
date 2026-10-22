# 3. Our data: from a NASA telescope to your D: drive

<p class="ss-meta">Chapter 3 · about 20 min · Maths: megabytes and gigabytes, ppm</p>

!!! plain "In plain words"
    NASA turns TESS pictures into brightness records and puts them online for free, and our code downloads them to your D: drive. This chapter follows that path so you know what our data is and what can go wrong with it.

**What this chapter answers:** what data do we use, how does it reach your PC, and how good is it?

## 3.1 The intuition

Think of a security camera that photographs a whole car park every few minutes. Later, someone goes through the photos and, for each parked car, writes down how bright its headlights looked in each photo. You get the notebook, not the photos. That notebook is a **light curve**. If you ever need to check something the notebook can't tell you, you can go back to the photos (the **pixels**).

## 3.2 The scientific meaning

TESS has **4 cameras**, each seeing a 24 × 24 degree patch of sky, with 4 detector chips of 2048 × 2048 pixels each. One pixel covers about **21 arcseconds** {{claim:F-024}}. That's a big pixel: several stars can share one, which is why the "neighbour" test in Chapter 10 matters.

TESS circles Earth every **13.7 days** and watches each patch for about 27 days (a sector). Stars near the ecliptic poles get watched for up to a year {{claim:F-025}}.

The data comes in three layers:

| Layer | What it is | Size per star per sector (measured) {{claim:F-026}} | When we use it |
|---|---|---|---|
| **Light curve** (SPOC, QLP, TESS-SPOC) | the brightness notebook, ready-made | 0.7-2 MB | almost always |
| **Target pixel file** | the small stack of pixels around one star, every cadence | ~50 MB | checking where a dip comes from (Chapter 10, C6) |
| **TESScut cutout** | a square of pixels cut from the full-frame images | ~11-50 MB | faint stars with no ready-made light curve |

Your rule from 19 October: we keep light curves, but cutouts are deleted after we extract what we need, because NASA keeps the originals.

## 3.3 The technical explanation

### From pixels to a light curve

TESS doesn't send home "light curves". It sends **pictures**, and teams on the ground turn them into brightness lists:

1. **Postage stamps.** For a limited set of chosen stars, TESS keeps a small square of pixels every 2 minutes (some every 20 seconds). These are **target pixel files**.
2. **Full-frame images (FFIs).** The whole camera view, saved every 30 minutes in the first two years, every 10 minutes later, and every 200 seconds now {{claim:F-041}}. Every star in view is in them, but at a slower rhythm.
3. **Photometry.** A team picks which pixels belong to a star (the **aperture**), adds up their light every cadence, subtracts the background sky, and cleans out spacecraft effects. The result is the light curve you downloaded in Lab 2.

### Who makes the light curves

All of it lives at **MAST** (the Mikulski Archive for Space Telescopes), NASA's public archive. For Kepler-16 alone, MAST holds 94 light curves from six teams {{claim:F-036}}:

| Team | Made from | Rhythm | Notes |
|---|---|---|---|
| **SPOC** (NASA Ames) | postage stamps | 2 min (some 20 s) | the cleanest; our first choice |
| **TESS-SPOC** | FFIs | FFI rhythm | SPOC's method on many more stars |
| **QLP** (MIT Quick-Look Pipeline) | FFIs | FFI rhythm | the widest coverage: every G1 star has it |
| **TARS, CDIPS, TASOC** | FFIs | FFI rhythm | other science teams' versions; useful for second opinions |

In our G1 list, QLP covers all 549 stars, SPOC 275 and TESS-SPOC 312 {{claim:F-043}}. They're made independently, which is why rule C8 (Chapter 10) asks for a dip in at least two of them.

### Where they land on your PC

Every download goes under `D:\second-sun\data\` (never C:), into a `mastDownload` folder that copies MAST's own layout, and gets a line in `research/downloads.csv`. You did this yourself in [Lab 2](../labs/lab2-get-the-data.md).

### How good is the data?

On Kepler-16, a fairly bright star in our G1 field (TESS magnitude 10.94), a quick estimate of one hour's scatter gives **236 ppm** (SPOC), **279 ppm** (TESS-SPOC) or **293 ppm** (QLP) {{claim:F-027}}. Those three numbers are good for **comparing** the products: SPOC is the quietest.

!!! warning "Correction, 20 October 2026"
    That quick estimate flattens the light curve with a window only 3.4 hours long, which removes the slow wobble that matters for our multi-hour transits. Measured the way our detector sees the data, the same hour scatters by about **900 ppm**; NASA's own estimate is 542 ppm {{claim:F-039}}. The optimistic number was one reason for an early overstatement of how small a planet we could find. Chapter 7 explains why the method changes the answer.

### Known troublemakers in the data

- **Momentum dumps:** every 2-6 days TESS fires thrusters; the cadences are flagged (quality bit 32) {{claim:F-028}}. Chapter 8 showed fakes cluster near them.
- **Data gaps:** downlinks to Earth every orbit leave holes; edges of holes are where detrending goes wrong.
- **Scattered light** from the Earth and Moon near the ends of orbits.

## 3.4 Our implementation

- Downloads use **lightkurve** (a Python package), always into `D:\second-sun\data\` or `D:\second-sun\.cache\`, never C:.
- Every download is logged in `research/downloads.csv` (what, from where, size, why).
- Your PC's **Avast** antivirus intercepts secure web connections. Python is told to trust the Windows certificate list (a package called `truststore`), inside the project only. Avast itself is untouched.
- Third-party tools get checked first. On 20 October, STANLEY tried to download to C:; it was caught before any file landed, and now a wrapper forces its downloads onto D: (logged in the mistakes register).

## 3.5 Worked example: what it cost to test STANLEY on TOI-1338

TOI-1338 sits near the south ecliptic pole, so TESS has watched it a lot: **40 sectors** of 2-minute data. At about 2 MB each, that's **78 MB** in total, which is small. The same star as raw cutouts would be roughly 40 × 30 MB ≈ **1.2 GB**. That gap is why we prefer ready-made light curves.

## 3.6 What this lets us conclude, and what it doesn't

- **The data is free and reachable from your PC,** and light curves are small enough that even hundreds of stars fit easily on D:.
- **A light curve hides choices.** Each pipeline cleaned the data its own way. A dip in only one product could be that product's artefact.
- **Big pixels mean blends.** A dip can come from a neighbour inside the same 21-arcsecond pixel. Light curves alone can't rule that out; pixels can.

## 3.7 Check your understanding

The questions for this chapter are on the [Part 1 review page](../parts/part1/review.md).

## Sources
In the [claims register](../claims.md): F-024 to F-028. Full research: `research/wave-2-data/report.md`.
