# Kepler re-find test (2026-10-23)

*Ahmed: "Do kepler test first." Code: `pipeline/kepler_refind_get.py` (download), `pipeline/kepler_refind.py` (key, score). Data: 52 Kepler long-cadence quarters, 21.4 MB, logged in `research/downloads.csv`.*

**Question:** can `detect_v2` (fixed B1, so 29.4-min data now works) re-find the known transits of Kepler-16 b, 34 b and 35 b in the original Kepler data?

**Answer key (LIKELY, our own measurement):** no per-transit table could be opened, so transits were located with a different method (3-day median flatten, runs of 4+ cadences below 4 sigma, eclipses masked) and confirmed by eye (`key_windows.png`, `key_windows_zoom.png`). Kepler-16: 7 (Davies et al. 2026 Table 2 lists 7). Kepler-34: 7 (Davies 9). Kepler-35: 4 (Davies 7; one more near BKJD 879 sits inside a masked stellar eclipse; 633.96 is a probable crossing of star B, left out). Times in `key.json`. Spacing checks: Kepler-16 about 222 to 230 d (planet period 229 d); Kepler-35 about 126 d (Welsh et al. 2012 give 122 to 127 d intervals).

**Result (VERIFIED, ran):** all **18 of 18** key transits found, in **both** PDCSAP and SAP flux, SNR 13 to 320 (`score.json`).
- Extra events per quarter: Kepler-16 3.6, Kepler-34 0.5 to 0.7, Kepler-35 0.7. For Kepler-16, 52 of 64 extras sit within 0.5 d of a data gap (Kepler paused monthly for downlinks; the existing veto flags these for a human), a few are the shoulders of the planet's own transits, the strongest are quarter-1 glitches (a 13% drop at the very end of Q1). Only 12 are far from both gaps and eclipses.
- A 1% dip at BKJD 1127 appears in both Kepler-16 and Kepler-34: the same moment on two stars, so a spacecraft effect. A real example of why the cross-star "common-time" veto is needed.

**How it compares with Davies et al. (at least 50% per planet, over 75% for 9 of 14): not a fair head-to-head yet.** Our key holds the transits clear enough to find by eye, so 100% on it is an upper bound. The missing 2 (Kepler-34) and 3 (Kepler-35) transits of Davies' counts are probably the hard ones (shallow crossings of star B, or during eclipses).

**Limits:** three bright-signal planets only; the key is not published; eclipse-overlapping transits are unsearchable by design (mask).

**Next (harder cases):** Kepler-47 d (2.4 to 4.8 h transits, below and at our shortest box) and Kepler-64 b (0.11% deep, long); and the review's better test: inject these real Kepler transit shapes into real G1 TESS light curves.
