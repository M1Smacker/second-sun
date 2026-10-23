# Detector fixes and data-path audit pilot (2026-10-23)

*Ahmed: "Apply all of the ordered changes... make sure nothing breaks." Order from `research/compass-reviews/2026-10-23-deep-review.md`. Labels: VERIFIED (ran here), LIKELY, NOT TESTED.*

## 1. Fixes in `pipeline/detect_v2.py`
| Bug | Fix | Test that failed before and passes now |
|---|---|---|
| B1: no events on 30-min data | `bin_width()`: bins are 10 min, or the data's own spacing when that is slower; `bin10()` and `box_scores()` take `bin_d` (default unchanged) | `test_detect_v2_paths.py::test_cadences`: dip found at 2, 3.3, 10, 29.4 and 30 min; 30-min white noise gives no event. Old code: nothing at 29.4 min. VERIFIED |
| B2: pre-56 QLP used `kspsap_flux` | QLP uses `sys_rm_flux` from S56, raw `sap_flux` before; `needs_windows` is set for every QLP file | `test_qlp_pre56_column` on our Kepler-16 S54 file. VERIFIED |
| B5: all-NaN PDCSAP returned nothing | SPOC file with no finite PDCSAP falls back to SAP | `test_spoc_all_nan_pdcsap` (copy of Kepler-16 S82 with PDCSAP blanked, written to `D:\second-sun\.cache`). VERIFIED |
| Record the column | `load(path, info=True)` also returns product, sector, column, cadence, needs_windows; default return unchanged | used by the audit |

Not changed (outside the order, noted for next): B3 (mask from ALL catalogue periods: KIC 4150611, KIC 7622486), B4 (flipped-match auto-reject should become a flag; it changes what Lab 9 shows, so it needs its own check).

## 2. Nothing else broke (VERIFIED)
`pipeline/regress_detect_v2.py` ran the committed detector (e66aac4) and the fixed one on every light curve on disk: **50 identical** (same cadences, same flux, same events), **1 different by design** (Kepler-16 S54 QLP: column `kspsap_flux` → `sap_flux`; events 3 → 2). Three files (eleanor, TGLC, a pixel file) cannot be read by either version, as before. The original `_selfcheck()` still passes. Only `look_event.py` (a one-off plot from the Kepler-16 dry run) ever read a pre-56 QLP file; its plot would now show SAP; its conclusion came from SPOC and stands.

## 3. Audit pilot (`pipeline/audit_paths.py`, `audit_summary.py`; 29 unique star-sectors, 7 G1 stars on disk)
Output: `pilot.csv`, `pilot_summary.txt`. This is not a search: real-data events are not recorded.
- **Injection works where it should:** a hidden 8 h, 3,000 ppm dip came back in every star-sector whose noise allowed it, and in none where 7 × noise exceeds 3,000 ppm (0 unexpected misses). VERIFIED
- **Red-noise factor beta on real G1 stars (SPOC, 27 star-sectors): median 1.76, quartiles 1.32 to 2.59.** Per-star medians: 1.15, 1.22, 1.29, 1.40, 1.94 (Kepler-16), 2.96, and 58.7 (outlier below). The "2.8 for Kepler-16" used in the odds discussion came from a 1-hour scatter with a different estimator; measured the way the search measures, Kepler-16 is about 1.9. VERIFIED (small sample: 7 bright-ish stars with SPOC data).
- **Pre-56 QLP is now depth-safe but noisy:** Kepler-16 S54 QLP `sap_flux` inside its own SPOC windows: 2,160 ppm at 6.5 h, against 362 ppm from SPOC the same sector (about 6x). The injected dip was not recoverable. Post-56 QLP `sys_rm_flux` (S82): 185 ppm, as good as SPOC. VERIFIED (one star, one sector each). So the B2 fix stops depth loss but does not make those sectors useful; prefer SPOC, then TESS-SPOC, and treat pre-56 QLP-only star-sectors as low sensitivity until a better recipe exists.
- **Poor-match stars are flagged automatically:** TIC 48507019 (KIC 11285625, 3.1 Rsun, noise 4,000 to 7,800 ppm; LIKELY a pulsating star, from memory) and TIC 158278417 (a 12.5 Rsun giant: smallest detectable planet about 84 Earth radii).
- **Smallest planet at SNR 7 in one 6.5 h transit** (no dilution correction): Kepler-16 2.7 to 5.5 Earth radii per sector; TIC 63071165 4.7; TIC 121277143 9.7; TIC 159443078 10.3.
- **False-alarm proxy:** 0.28 flipped events per star-sector (in line with F-016/F-058's 0.25 to 0.6).

## 4. What it changes
- Odds: the measured beta (about 1.2 to 2.0 for most stars) sits between the two cases in the Compass review (1.4 → about 29%, 2.0 → about 22%). Claude's estimate stays **about 20% (5 to 45%)** until the full audit, because the pilot stars are brighter and better covered than typical G1 stars; it leans up, not down.
- The full audit needs the G1 light curves (about 6.3 GB, under the 20 GB rule; to be logged in `research/downloads.csv`). Not run today (usage cap).
