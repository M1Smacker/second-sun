# Lab 2: get the data and look inside

<p class="ss-meta">Lab · at your PC · about 15 min · Level L0 · after Lab 1</p>

!!! plain "In plain words"
    Now you download one month of TESS data for Kepler-16 (one sector, about 2 MB) and open the file. It's a table: one row every 2 minutes, with the time, the brightness, and a "quality" number that warns about bad moments. Every planet search starts from a file like this one.

**Goal:** download a light curve yourself and know what every important column means.

## What you should see

From a real run on your PC (20 October 2026) {{claim:F-037}}:

```text
SearchResult containing 1 data products.

 #     mission     year author exptime target_name distance
--- -------------- ---- ------ ------- ----------- --------
  0 TESS Sector 82 2024   SPOC     120   299096355      0.0

Saved to: D:\second-sun\data\labs\mastDownload\TESS\tess2024223182411-s0082-0000000299096355-0278-s\tess2024223182411-s0082-0000000299096355-0278-s_lc.fits
Header: OBJECT=TIC 299096355  TICID=299096355  SECTOR=82  CAMERA=3  CCD=4  TESSMAG=10.94379997
Columns: TIME, TIMECORR, CADENCENO, SAP_FLUX, SAP_FLUX_ERR, SAP_BKG, SAP_BKG_ERR, PDCSAP_FLUX, PDCSAP_FLUX_ERR, QUALITY, PSF_CENTR1, PSF_CENTR1_ERR, PSF_CENTR2, PSF_CENTR2_ERR, MOM_CENTR1, MOM_CENTR1_ERR, MOM_CENTR2, MOM_CENTR2_ERR, POS_CORR1, POS_CORR2
Cadences: 18619, from BTJD 3533.39 to 3559.25 (25.9 days)
Every 2.0 minutes
Flagged by quality bits: 482 cadences; momentum dumps (bit 32): 16
PDCSAP flux present on 18137 cadences; median 6832 electrons per second
```

## Do it yourself

??? note "The commands, when you are at your PC"

    ```powershell
    cd D:\second-sun
    .\.venv\Scripts\python.exe labs\lab2_get_the_data.py "Kepler-16" 82
    ```

    The `82` is the sector. Downloads go to `D:\second-sun\data\labs` (never C:). If the file is already there, it isn't downloaded again.

## Reading it

**The file name** packs in the facts: `tess2024223182411` is when the data was processed (year 2024, day 223), `s0082` is the sector, `0000000299096355` is the TIC number, and `_lc` means light curve.

**The file format is FITS,** astronomy's standard since 1981. A FITS file has a **header** (labels: which star, which camera) and **tables** (the data).

**The header** says this star fell on camera 3, chip (CCD) 4. Stars on the same chip share spacecraft problems, which is how the QLP fix borrows good time windows from neighbours (Chapter 3).

**The columns you'll use most:**

| Column | Meaning |
|---|---|
| `TIME` | when, in **BTJD**: days since a fixed moment in 2014 (BJD 2457000). BTJD 3533 is August 2024 |
| `SAP_FLUX` | **raw** brightness: all the light in the star's pixels, in electrons per second |
| `PDCSAP_FLUX` | **cleaned** brightness: NASA removed known spacecraft effects. We use this first |
| `..._ERR` | the expected noise on each measurement |
| `QUALITY` | a warning number; 0 means fine (see below) |
| `MOM_CENTR1/2` | where the star's light centre sits on the chip; it moves if the telescope wobbles |
| `SAP_BKG` | the background sky light that was subtracted |

**18,619 cadences.** A cadence is one measurement. 25.9 days × 720 per day (one every 2 minutes) is about 18,650, so almost none are missing.

**PDCSAP is missing on 482 rows:** exactly the 482 flagged ones (checked row by row). NASA blanks the cleaned flux where it doesn't trust the data.

**The QUALITY number** is a set of switches added together. Each switch is a power of 2:

| Value | Name (from lightkurve) | Meaning |
|---|---|---|
| 8 | Earth point | the spacecraft turned toward Earth to send data home |
| 16 | Argabrightening | a sudden glow across the whole camera (cause uncertain) |
| 32 | Desaturation event | **momentum dump**: thrusters fired {{claim:F-028}} |
| 128 | Manual exclude | NASA's team marked these by hand |
| 2048, 4096 | Straylight | scattered light from Earth or Moon (not in this file; common in others) |

This file contains the values 8, 16, 32, 40, 128 and 160 (checked by script). A value of 40 means 32 + 8: a thruster firing *and* an Earth-point moment; 160 is 128 + 32. The 16 momentum-dump cadences matter: on 20 October our first G1 dip turned out to be the telescope wobbling just before one (Chapter 10).

## What can go wrong

| You see | Why | Fix |
|---|---|---|
| `No data found` | That sector has no SPOC 2-minute file for this star | Use a sector from Lab 1's SPOC list |
| A very long wait | MAST is slow today | Wait; it's only 2 MB |
| `PermissionError` | The file is open in another program | Close it and run again |

## Your turn

1. Download a **different sector** of Kepler-16, from 2019. Look at Lab 1's SPOC list and choose 14 or 15.
2. Compare: how many cadences, how many flagged, how many momentum dumps?
3. **Think:** sector 14 was in 2019. Why might its time range in BTJD be much smaller than 3533?

**Tell me:** "Lab 2 done", the sector you picked, and your three numbers.

**Back to:** [Try it yourself, Part 1](../parts/part1/labs.md)
