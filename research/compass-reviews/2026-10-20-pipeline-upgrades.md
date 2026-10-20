# Compass review: pipeline upgrades (injection-recovery, contextual vetting, pixel-level validation)

*2026-10-20, Claude (Opus 5.5). Review only; nothing was built during this pass. Method: research/COMPASS.md.*

## Verdict: **REVISE**
The three areas are the right ones, and injection-recovery first is justified by tonight's evidence. Three parts of the proposal need changing before building: odd-even depths don't apply to single circumbinary transits; centroid work must model where the light *should* move; and the injection engine already exists (STANLEY), so building a new one would duplicate it.

## 1. Injection and recovery
| Finding | Label |
|---|---|
| We have injection-recovery: `pipeline/accept_v2.py` (49 batman injections, 7 sizes × 7 times, TOI-1338 S98) and `research/burn-1-science/inject.py`. Injections go in **before** our detrending, so they do test whether detrending eats dips. | VERIFIED (code read, runs logged) |
| Gap: those fakes are strictly periodic, one shape, one 6.4 h duration. Real circumbinary transits shift in time by up to days and vary in duration (TOI-1338 b: 0.3-0.6 d). | VERIFIED (claims F-007, F-008) |
| Gap: injections never fall inside the eclipse mask (11-15% of time), so planets lost to masking are invisible in our recovery rates. | VERIFIED (code read) |
| Gap: 49 trials give recovery fractions with ~±15% binomial uncertainty at 50%; too few for a sensitivity curve. | VERIFIED (arithmetic) |
| Gap: we inject into PDCSAP, so NASA's own PDC step is not tested. Injecting into SAP, or into pixels, would be needed for that. | VERIFIED (code read); impact UNCERTAIN |
| **Duplicate risk:** STANLEY 0.2.8 (MIT, installed, runs on this PC) has `InjectTransits`: N-body timing + batman profile + flux ratio, wired into its detrending (`--injectTransits 1`). Use it rather than writing our own. | VERIFIED (code read) |
| STANLEY's default TESS parameter file (`planet_params.csv`) is not in the installed package; we must supply our own parameter CSV. | VERIFIED (file search) |

## 2. Contextual vetting
| Finding | Label |
|---|---|
| We have: gap/dump warning flags (rule C7, 0.5 d before dumps), flipped-data match rejection, automatic eclipse masks (per sector and global fold), per-sector systematics read from quality bits. | VERIFIED |
| **Incorrect assumption (proposal):** odd-even depth tests assume a periodic planet. A single circumbinary transit has no odd/even pair. Use odd-even only (a) on the binary itself, to catch a "planet" that is really the binary at twice its period, and (b) for periodic candidates. | VERIFIED (logic; SPOC/QLP use it for periodic TCEs: Guerrero+ 2021, claim F-020) |
| **Incorrect assumption (our code):** `load()` drops every cadence in lightkurve's HARD mask, which includes stray-light bits (2048, 4096). That is the blind rejection the proposal warns against; stray-light cadences should be kept and flagged. | VERIFIED (lightkurve bitmask values, wave 2 D16) |
| "Secondary eclipses": for us this means the **binary's** secondary (handled by the masks), plus checking a candidate isn't at an eclipse phase (C5). A planet's own occultation is undetectable at our precision. | VERIFIED (masks) / LIKELY (occultation claim, standard physics) |
| Missing: C2 multi-detrending robustness, C3 model comparison (transit vs step/sine/line), C9 size check for both stars. | VERIFIED (absent from code) |

## 3. Pixel-level validation
| Finding | Label |
|---|---|
| We have one manual script (`research/wave-3-pipeline/toi1338_pixel_check.py`): difference image + flux-weighted centroid shift on one event. | VERIFIED |
| Its centroid error uses out-of-transit scatter / √N_in, which assumes white noise and ignores the out-of-transit mean's own error, so it overstates significance. | VERIFIED (code read) |
| Missing: neighbour positions (Gaia/TIC) projected onto pixels with the file's WCS; the **expected** centroid shift for an on-target dip (dilution by neighbours shifts the centroid even when the target is the source). Kepler's method compares observed vs expected offsets, and uses difference-image centroids: Bryson et al. 2013 (PASP 125, 889) and Twicken et al. 2018 (PASP 130, 064502). | VERIFIED (both papers on ADS; method summary LIKELY, from memory of the papers) |
| Correct principle (proposal): a centroid shift is a warning, not a classification. | agreed |
| Data cost: a target pixel file is ~50 MB per sector (wave 2), so pixel checks only for events that survive steps 1-2. QLP-only stars have no TPF; TESScut cutouts instead (deleted after use, per Ahmed's rule). | VERIFIED (measured sizes) |

## Order (by scientific value)
1. **Injection-recovery with STANLEY's N-body injector** on TOI-1338, smallest version first: decides whether detrending destroys realistic signals, which every later number depends on.
2. Contextual quality flags (keep and flag stray light) + eclipse-phase check (C5) + odd-even on the binary.
3. Pixel tool (difference-image centroid + expected offset + neighbour overlay), only for survivors.

## Single best next step
Run STANLEY's detrending once on TOI-1338 with `--injectTransits 1` and a small parameter file (a few planets of different sizes, realistic periods), then measure how much of each injected transit survives detrending and whether our search finds it.

## Also found (not part of the proposal)
- `book/data/claims.csv` is git-ignored (`data/` rule), so the book's fact register is not in the repo. Fix first; it's 2 lines.
