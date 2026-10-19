# Wave 2: data and archives

*Second Sun research, wave 2. Run inline by the main session (Claude, Opus 5.5) on 2026-10-19, 17:05-17:20 UTC. Claims are numbered D1… in `claims.md`. Wave 1c already covered TESS mission status, the eclipsing-binary catalogues and the brightness limits of each light-curve product; this wave cites that work and doesn't repeat it.*

---

## In plain words (read this first)

**The data is free, open, and works from your PC.** We downloaded every kind of TESS file for two test stars (TOI-1338 and Kepler-16). Every one arrived in seconds to about a minute, and every byte went to D:.

**Light curves are tiny; raw pictures are big.** A ready-made light curve (a star's brightness over one ~27-day sector) is **0.7-2 MB**. A small square of raw pixels around a star, which we'd need to make our *own* light curves for faint stars, is **about 11-50 MB per sector**. So for the main quest's first campaign, ready-made light curves cost tens of GB in total, while do-it-yourself pixels could cost hundreds of GB.

**First precision reading for our first campaign (G1).** On Kepler-16 (a fairly bright Kepler-field star, TESS magnitude 10.9), TESS's noise over one hour is about **240-290 parts per million (0.024-0.029%)**. In plain words: a **Saturn-to-Jupiter-sized planet** (a ~1% dip) would stand out enormously, and a **Neptune-sized** one (~0.13% dip) is catchable on stars this bright but not on the faint ones. Wave 3 measures this across the whole Kepler binary list.

**A hidden problem on your PC, now fixed.** Your **Avast antivirus** intercepts secure web connections, and Python's standard web library didn't trust Avast's certificate, so every data download failed. We fixed it **inside the project only** (a tiny package called `truststore` makes Python use the Windows certificate list, the same one your browser uses). Avast and Windows settings were not touched. Any future machine with antivirus "HTTPS scanning" will need the same fix, so it's written down here.

**Other data sources:**
- **ZTF** (a ground telescope survey) gave us 970 measurements of Kepler-16 spanning 2018-2025, no account needed.
- **ASAS-SN** works via a Python package; no account is mentioned.
- **ATLAS** needs a free registration.
- **Gaia's next big release (DR4) is confirmed for 2 December 2026.** It adds brightness time-series for all its stars, which is directly useful for checking our binaries.

---

## 1. TESS hardware and observing (D1-D6)

| Fact | Value | Label |
|---|---|---|
| Cameras | 4, each 24° × 24°, stacked into a 24° × 96° strip; each camera has 4 CCDs of 2048 × 2048 pixels (plus overscan) | LIKELY (Sullivan+ 2015 via search summary; D1) |
| Pixel size | **~21 arcsec** (21.1″). Big pixels mean light from neighbouring stars mixes in, and that is why "blended" binaries are the #1 false-positive worry (wave 4) | LIKELY (D1) |
| Lens aperture | 10.5 cm per camera (Kepler: 0.95 m). TESS stars are "10-100 times brighter than those surveyed by Kepler" | VERIFIED (Ricker+ 2014 abstract, arXiv:1406.0151; D2) |
| Sector | ~27 days = 2 spacecraft orbits of 13.7 d; one data-downlink gap per orbit (in later years, more frequent but shorter gaps) | VERIFIED orbit (D2); gap pattern LIKELY (D5) |
| FFI cadence history | 30 min (S1-26), 10 min (S27-55), **200 s from S56 (Sept 2022)** | VERIFIED (wave 1c DRN text; D3) |
| Target cadences | 2 min (selected stars) and 20 s (a few thousand per sector, from the first extended mission onward); exposure stacks of 2 s | VERIFIED via files: S98 2-min LC has 40,157 cadences, the 20-s LC 241,046 (D4) |
| Long-stare zones | Stars near the ecliptic poles are watched "from one month to one year" each year | VERIFIED (Ricker+ 2014 abstract; D2) |
| EM3 special sectors | S97-98 double-length; S99-107 overlapping "rolled" sectors for long-period planets | VERIFIED (wave 1c, C2-C3) |

## 2. Light-curve products: measured on this PC (D7-D15)

All downloaded with lightkurve 2.6.0 on 2026-10-19, sizes measured on disk (`handson_results.csv`).

| Product | Made by | Stars | Cadence | **Size per star-sector (measured)** | Download time | Brightness / sector coverage |
|---|---|---|---|---|---|---|
| SPOC 2-min light curve | NASA SPOC | selected targets (~13,000/sector in EM3) | 2 min | **1.9 MB** (normal sector); 4.2 MB (double S98) | 6-12 s | S1-107 (wave 1c) |
| SPOC 20-s light curve | NASA SPOC | ~2,500/sector | 20 s | ~12 MB (24.8 MB double) | 8 s | |
| SPOC target pixel file | NASA SPOC | same as 2-min | 2 min | **~50 MB** (101 MB double) | 20 s | |
| TESS-SPOC FFI light curve | NASA SPOC (HLSP) | ≤ Tmag 13.5 subset | 200 s | **1.15 MB** | 5 s | to S96 (wave 1c) |
| QLP FFI light curve | MIT (HLSP) | Tmag < 13.5 | 200 s | **0.66 MB** | 9 s | to S107 (wave 1c) |
| TGLC FFI light curve | Han & Brandt (HLSP) | Tmag ≤ 16 | 30 min (S10 tested) | 0.05 MB at 30-min cadence (scale ×9 at 200 s ≈ 0.5 MB) | 8 s | S1-65 only (wave 1c) |
| TESScut FFI cutout 15×15 px | MAST | **any star** | 200 s | **50 MB** (110 MB double); ≈ 0.22 MB per pixel per sector, so **7×7 ≈ 11 MB** | 33-71 s | to S108 (wave 1c) |

Older sectors are smaller for FFI-based products: 30-min (S1-26) is ~6× and 10-min (S27-55) ~3× smaller per sector than 200 s.

**Other light-curve products** (eleanor / GSFC-ELEANOR-LITE S1-26, T16 Cycle 1, CDIPS cluster stars S1-55, TASOC, TARS): coverage per wave 1c section 6; not size-tested (not needed for G1).

## 3. Quality flags and systematics (D16-D19)

TESS quality flags as defined in the installed lightkurve 2.6.0 (`TessQualityFlags`, VERIFIED from code):

| Bit | Meaning | In lightkurve's DEFAULT mask? |
|---|---|---|
| 1 | Attitude tweak | yes |
| 2 | Safe mode | yes |
| 4 | Coarse point | yes |
| 8 | Earth point | yes |
| 16 | Argabrightening | yes |
| 32 | Desaturation event (= **momentum dump**) | yes |
| 64 | Cosmic ray in aperture | no |
| 128 | Manual exclude | yes |
| 256 | Discontinuity corrected | no |
| 512 | Impulsive outlier | yes |
| 1024 | Cosmic ray in collateral data | no |
| 2048 / 4096 | Straylight / Straylight2 | no |
| 8192 | Planet search exclude | no |
| 16384 | Bad calibration exclude | yes |
| 32768 | Insufficient targets for error correction | no |

DEFAULT_BITMASK = 17087, HARD = 24319, HARDEST = 65535. **Why it matters for us:** a single circumbinary dip can be faked by a momentum dump or by scattered light, and those are *not all* removed by default. The vetting sheet (wave 4) must show these flags around every candidate dip.

- **Momentum dumps** happen every ~2-6 days. Since Sector 56 they are generally surrounded by ≳0.2-day data gaps (LIKELY; TESSILATOR paper arXiv:2407.18761 via search; D17).
- **Scattered light** from the Earth and Moon causes ramps at orbit ends and a 1-day background oscillation (LIKELY; Sector 1-2 release notes via search; D18).
- **Data Release Notes:** one per sector at `https://archive.stsci.edu/missions/tess/doc/tess_drn/tess_sector_NN_drnNNN_vNN.pdf`; the latest is **DRN 142 = Sector 104** (VERIFIED, index page last modified 2026-09-04; D19). A condensed version lives at HEASARC: <https://heasarc.gsfc.nasa.gov/docs/tess/data_release_notes.html>. **Rule for us: read the DRN for every sector a candidate dip is in.**

## 4. Access routes (D20-D24)

| Route | Works? | Notes |
|---|---|---|
| **lightkurve** (search + download) | **VERIFIED** after the truststore fix | simplest; per-star |
| **astroquery.mast** | installed (0.4.11); underlying MAST API reachable | for bulk queries |
| **TESScut** (via lightkurve) | **VERIFIED** | any star, any sector; heavy files |
| **AWS open data** `s3://stpubdata/tess/` | **VERIFIED** anonymous HTTPS listing (`ffi/`, `tid/`, `hats/`, `staged_cutouts/`, `mast/` …) | public domain, updated monthly, no AWS account (D21). The registry page says nothing about cost; my understanding that AWS Open Data buckets don't bill anonymous readers is UNVERIFIED (memory), so check before any bulk use |
| HLSPs on AWS | `stpubdata/mast/hlsp/` (TESS-SPOC, QLP, TGLC) | LIKELY (registry pages via search; D22) |
| MAST bulk download scripts | per-sector curl scripts | LIKELY; not tested (not needed until batches) |

## 5. Kepler / K2 (D25-D27)
- Kepler stared at one ~100-square-degree field for 4 years with a 0.95 m mirror; its noise on quiet Sun-like stars was ~50% *above* the pre-launch target, but still far better than TESS for the same star (Gilliland+ 2011, arXiv:1107.5207, abstract; LIKELY; D25).
- **Value for us:** Kepler gives (a) the **eclipsing-binary list with precise timings** for G1 (Villanova catalogue, 2,920 EBs; wave 1c C25) and (b) the **4-year baseline** that tells us which planets were *not* crossing during 2009-2013, which is exactly what makes a TESS-era "switched-on" planet meaningful.
- TESS re-observed the Kepler field in Sectors 14-15, 26, 40-41, 53-56, 73-76, 80-83 and has not returned since (VERIFIED via wave 1c ground-truth table; D26).
- K2: no maintained eclipsing-binary catalogue exists (wave 1c C26).

## 6. Gaia (D28-D30)
- **Gaia DR4: 2 December 2026, 12:00 CET** (archive down from 25 Nov). VERIFIED (ESA Gaia news, 8 Oct 2026; D28). DR4 adds epoch (time-series) photometry and astrometry for all sources, 66 months of data (LIKELY; ESA DR4 page via search; D29).
- DR3 tables we'll use (LIKELY from documentation knowledge; links to verify in wave 3/4):
  - `gaia_source`: positions and brightness; **RUWE**, where a high value hints at an unresolved companion
  - `nss_two_body_orbit`: non-single-star orbits, for spectroscopic and astrometric binaries (this is where the **G5 non-eclipsing binaries** live)
  - `vari_eclipsing_binary`: 2.18 M Gaia EB candidates (wave 1c, VERIFIED count)
  - `astrophysical_parameters`: star sizes and temperatures
  - neighbour searches for blends (wave 4). (D30)

## 7. Ground surveys (D31-D33)

| Survey | Tested? | Result |
|---|---|---|
| **ZTF** (IRSA light-curve API) | **VERIFIED**: Kepler-16 query returned **970 g-band points, MJD 58204-60948 (2018-03 to 2025-09)**, 250 KB, ~30 s, **no account** | multiple filters: comma syntax `BANDNAME=g,r` per docs (our first call returned g only; retest); default = latest public release; radius ≤ 0.1667°; >~1,000 stars → use the HATS notebook instead (D31) |
| **ASAS-SN Sky Patrol v2** | not tested | Python client `pip install skypatrol`; 111 M targets; up to 1 M light curves per query; no account mentioned (LIKELY; arXiv:2304.03791; D32) |
| **ATLAS** forced photometry | not tested | **requires free registration + API token** (LIKELY; client docs; D33): add to the account schedule (wave 5) |

## 8. Data budget (measured sizes → estimates)

Per **1,000 star-sectors** at 200-s cadence: QLP **0.7 GB** · TESS-SPOC **1.2 GB** · SPOC 2-min **1.9 GB** · TESScut 7×7 **~11 GB** · TESScut 15×15 **~50 GB**.

| Gap | Star-sectors (estimate) | Ready-made light curves | DIY from cutouts (7×7) | Label |
|---|---|---|---|---|
| **G1** Kepler-field EBs | 2,920 EBs × ~10 sectors ≈ **29,000** (many in smaller 30/10-min sectors) | **~10-30 GB** if all have QLP/TESS-SPOC | up to **~300 GB** if most are fainter than 13.5 | estimate; **the Tmag distribution (wave 3) decides it** |
| **G2** newest sectors, known EBs | ~8,000 EBs × 1.7 ≈ **13,600** (wave 1c C37-C40) | ~5-15 GB (bright third) | ~100 GB (faint two-thirds) | estimate |
| **G3** faint EBs after S65 | ~20,000 (rough) | none exist | **~220 GB** | rough |

**Consequence for the "keep raw data" rule:** ready-made light curves fit easily (keep them all). **Cutouts don't**: G2/G3 would fill a big part of D:. **Proposed (needs Ahmed's OK):** for TESScut cutouts, keep the light curves we extract plus the extraction settings, and delete the cutouts themselves, since they can be re-downloaded any time.

## 9. Environment (VERIFIED)
`D:\second-sun\.venv`: Python 3.12.10, lightkurve 2.6.0, astroquery 0.4.11, astropy 8.0.2, numpy 2.5.4, scipy 1.18.1, truststore 0.10.5 (auto-enabled via `sitecustomize.py`). Install took 190 s. A harmless warning: lightkurve's optional `tpfmodel` needs `oktopus`, which we don't use. Caches: all on D: (`.cache\`); C: checked before and after, with no new caches (`c-cache-before.txt`, `c-cache-after.txt`).
