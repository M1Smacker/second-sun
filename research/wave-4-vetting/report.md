# Wave 4: vetting and false positives

*Second Sun research, wave 4. Run inline by the main session (Claude, Opus 5.5) on 2026-10-19, ~17:20-17:40 UTC. Claims are numbered V1… in `claims.md`. Reading-only wave.*

---

## In plain words (read this first)

**Most dips are not planets.** In TESS's first two years, about **1 in 4** official planet candidates later turned out to be something else (V1). Our job in vetting is to kill fakes before anyone else has to.

**The usual suspects:**
1. **Two stars eclipsing each other**: either our own binary, or another binary *hiding in the same pixels*. TESS's pixels are huge (~21″), so a faint background binary can sit inside our star's pixel and fake a small dip.
2. **The spacecraft**: TESS fires thrusters every few days (momentum dumps). Just before those, it wobbles slightly, and that wobble can draw a perfect fake dip. This exact thing fooled people for a moment during the TOI-1338 b discovery (V8).
3. **Scattered light** from the Earth and Moon, and **asteroids** drifting across the pixels.
4. **The star itself**: spots, pulsations, flares.
5. **Our own software**: cleaning a light curve badly can carve a dip that isn't there. That's why the Warwick team re-cleaned every light curve 21 different ways and kept only dips that survived at least 18 of them (V5).

**The circumbinary "smoking gun".** A real planet orbiting two stars leaves a fingerprint no fake has: its crossings are **shorter near one eclipse of the binary and longer near the other**, and they come at irregular times that a computer model of the three bodies can predict (V9). Two dips that fit that pattern are worth more than ten that don't.

**Our bar is strict on purpose.** A clean record is how an independent citizen scientist earns trust. Below are numeric pass/fail rules (section 4), and a design for a one-page vetting sheet you can read on your iPhone (section 5).

---

## 1. Catalogue of fakes

| Fake | What it looks like | Why it fools you | Main test | Source |
|---|---|---|---|---|
| Eclipsing binary (our target) | V-shaped dip, often a secondary dip at another phase; odd/even depth differences | Grazing eclipses are shallow like planets | Shape, odd/even, secondary search | TOI dispositions "EB: V-shaped" (V2) |
| **Blended background binary** | Planet-like dip, diluted by our star's light | Sits inside the same 21″ pixel | Centroid / difference image; depth vs aperture; Gaia neighbours | V2, V3 |
| Hierarchical triple | Extra dips from a third star | Same as a planet in timing chaos | Depth and duration physically too large; RVs | Davies: 4 "stellar tertiaries" in Oddo+ 2026 (wave 1b) |
| Stellar variability (spots, pulsations) | Sinusoidal or ramp-like dips | Detrending turns a wave into a dip | Model comparison (transit vs sinusoid/step/line); detrending robustness | V5, V6 |
| Flares, spot crossings | Brief brightenings or bumps inside eclipses | Distort the shape | Visual + model residuals | general (LIKELY) |
| **Momentum dumps / pointing jitter** | Sharp, transit-like dips, often just *before* a dump | PSF changes shape | Quality flag 32; dump times; PSF / pixel-level check | **TOI-1338 b paper (V8)**; wave 2 D16-D17 |
| Scattered light (Earth/Moon) | Ramps at orbit ends; 1-day background ripples | Background over- or under-subtraction | Hard quality mask; background flux plot; DRNs | wave 2 D18 |
| Asteroids | A short dip *or* bump as a rock crosses the aperture or background region | Moves through pixels in sequence | Per-pixel time series; background aperture | Davies (V5) |
| Cosmic rays / single-cadence events | One-point outliers | Pass a simple threshold | Require ≥3 consecutive cadences (30-min bins) | V4 |
| Detrending artefacts | Dips carved near gaps or sector edges | Filter edge effects | 18-of-21 detrending rule | V5 |
| **Circumbinary-specific:** eclipse residuals | Leftover bits after masking or subtracting eclipses | Imperfect eclipse model | Phase-of-binary check: ≥3 events at the same binary phase = eclipse, not planet | V6 |
| **Circumbinary-specific:** wrong stellar radius | A "planet" whose implied size is a star | Catalogue radius wrong for a binary | Implied radius for *both* stars as host; reject > 2 R_J | Davies on TIC 319011894 (V7) |
| **Circumbinary-specific:** third light | Dilution changes all depths | Unresolved companion | Gaia RUWE / NSS; high-resolution imaging (later) | V7, V8 |

## 2. The professionals' tests and thresholds

| Test | Threshold used by professionals | Source | Label |
|---|---|---|---|
| SPOC detection | MES > **7.1**, ≥ **2 transits** | Guerrero+ 2021 (V1) | VERIFIED |
| QLP detection | SNR (pink noise) > **9** and BLS significance > **9** | V1 | VERIFIED |
| TOI follow-up priority | SNR < **11** → priority 2 | V1 | VERIFIED |
| Odd/even | QLP flags > **5σ** depth difference | V1 | VERIFIED |
| Centroid | Offset to a star ≥ **1 pixel** suggests a background EB; SPOC offsets < **7.5″** not significant at 3σ | V1 | VERIFIED |
| Depth vs aperture | Depth rising with aperture → nearby source | V1 | VERIFIED |
| Human vetting | **3-5 independent vetters** per target; any planet vote → group review | V1 | VERIFIED |
| Single-dip detection (CBP) | 3 consecutive 30-min points < **3 × MAD** (4-day window); SNR > **5** | Davies+ 2026 (V4) | VERIFIED |
| Detrending robustness | Kept if found in ≥ **18 of 21** biweight detrendings (1-3 d windows) | V5 | VERIFIED |
| Duration (CBP single dip) | < **1 day** | V5 | VERIFIED |
| Model comparison | Transit preferred if ΔAIC ≤ **−2** vs sinusoid, step and line; RMSE ≤ 1.2 → "ambiguous" flag | V5 | VERIFIED |
| Systematics clustering | Events within 0.1 d grouped; > **3σ** outlier groups = systematics | V5 | VERIFIED |
| Statistical validation | TRICERATOPS **FPP < 0.015 and NFPP < 0.001** = validated; FPP < 0.5 and NFPP < 0.001 = likely planet; NFPP > 0.1 = likely nearby false positive | Giacalone+ 2021 (V10) | VERIFIED |
| Kepler-era automated vetting | Robovetter metrics with measured completeness and reliability | Thompson+ 2018 (V11) | VERIFIED (abstract) |

## 3. How the circumbinary planets were vetted

**TOI-1338 b (V8, VERIFIED from the paper):**
- **Centroids:** SPOC centroid offsets plus DAVE's photocenter module showed the eclipses come from the target. Per-pixel light curves exposed the fake events as artefacts.
- **Neighbours:** Gaia found only 6 sources within 7 magnitudes in the 13×13-pixel area, none inside the aperture. The odds of a hidden neighbour were ~10⁻³, and a background binary would need to be fainter than T ≈ 18 to fit the depths.
- **Overall false-positive probability:** ~10⁻⁸.
- **Fake dips:** the Sector 3 fakes were traced to **pointing jitter just before momentum dumps**, using PSF-shape fitting.
- **Two independent light curves** (eleanor FFI and SPOC 2-min) agreed once the background was redone.
- **The smoking gun:** transit durations varied with the binary's phase (shorter near primary eclipse), and the intervals between transits differed (~93 vs ~95 days).
- **Follow-up:** radial velocities showed a single-lined binary with no sign of extra stars; speckle imaging found no source within 3″.

**TIC 319011894 (Warwick's single-dip candidate; V7):**
- No centroid shift; the dip appears in SPOC, QLP and eleanor, but is less clear in TGLC.
- **But:** the catalogue radius (2.86 R☉) makes the "planet" ~4 R_J, which is not planetary unless that radius is wrong. Gaia RUWE is 1.03, and the star is not in Gaia's non-single-star catalogue.
- No secondary eclipse was found.
- They asked for ground photometry and spectroscopy.
- **Lesson:** the host's radius can kill a candidate. Check it first.

TIC 172900988 b: the discovery-paper vetting wasn't read in this wave (open question).

## 4. Our "very strict" bar (proposal; numbers sourced or marked as OUR choice)

### 4a. Normal periodic candidate (training quest)

| # | Rule | Threshold | Basis |
|---|---|---|---|
| N1 | Detection strength | SNR ≥ **11** | OUR choice: above the TOI priority-2 line (V1) |
| N2 | Number of transits | ≥ **3** | OUR choice (SPOC needs 2) |
| N3 | Odd/even depths | differ by < **3σ** | OUR choice (QLP flags at 5σ) |
| N4 | Secondary eclipse | none > **3σ** at any phase | OUR choice |
| N5 | Centroid / difference image | no offset significant at 3σ; no offset toward a neighbour ≥ 1 pixel | V1 |
| N6 | Depth vs aperture | consistent within 2σ across apertures | V1 (test); 2σ is OUR choice |
| N7 | Neighbours | no Gaia source within 2 pixels (~42″) bright enough to make the dip if it were fully eclipsed | standard logic; OUR radius |
| N8 | Shape and size | U-shaped, or a grazing fit with radius < **2 R_J** | V2, V7 |
| N9 | Systematics | no transit within **0.5 d before** a momentum dump unless pixel/PSF checks clear it; no HARD-mask cadences in transit | TOI-1338 lesson (V8); 0.5 d is OUR choice |
| N10 | Independent products | seen in ≥ **2** light-curve products | V7, V8 |
| N11 | Statistical validation | TRICERATOPS **NFPP < 0.001** and **FPP < 0.1** | V10 for NFPP; FPP 0.1 is OUR choice (stricter than "likely planet" at 0.5) |
| N12 | Not already known | not a TOI/CTOI/known EB within 155″ with matching ephemeris | V1 (QLP ephemeris match) |

### 4b. Circumbinary single-dip candidate (main quest)

| # | Rule | Threshold | Basis |
|---|---|---|---|
| C1 | Event | ≥ 3 consecutive 30-min bins below 3 × MAD; SNR ≥ **7** | Davies method (V4); SNR 7 is OUR choice (stricter than their 5) |
| C2 | Detrending robustness | ≥ **18/21** detrendings | V5 |
| C3 | Shape | transit model preferred with ΔAIC ≤ −2 vs sinusoid, step and line; not "ambiguous" | V5 |
| C4 | Duration | < 1 d, **and** within the range allowed for a circumbinary orbit outside the stability limit (P_p ≥ ~4 × P_bin) | V5; orbit range = OUR analysis using wave 1a physics |
| C5 | Not an eclipse | not at a binary phase shared by ≥ 3 events; not overlapping a visible eclipse | V6 |
| C6 | Not a neighbour | per-pixel light curves show no correlated anti-dips; no centroid shift; no nearby EB with matching timing | V5, V7 |
| C7 | Not the spacecraft | no HARD-mask cadences; not within 0.5 d before a momentum dump unless pixel/PSF checks clear it; DRN for the sector read | V8; wave 2 |
| C8 | Independent products | seen in ≥ **2** of SPOC / QLP / TESS-SPOC / eleanor / TGLC | V7 |
| C9 | Physical size | implied radius < **2 R_J** whether it crosses the primary *or* the secondary star; host radius sanity-checked (Gaia, RUWE, NSS) | V7 |
| C10 | Smoking gun (if ≥ 2 events) | timing and duration pattern consistent with a circumbinary orbit (duration shorter near primary-eclipse phase) | V8 |
| C11 | Submission | **Two keys** (Claude's analysis + Ahmed agrees). Prefer ≥ 2 consistent events; a single event is submitted only if C1-C9 all pass with margin | founding decision |

Open: TRICERATOPS needs a period, so single-dip use is unclear (wave 5 / wave 3).

## 5. Phone vetting sheet: specification

One tall page, **390 px wide** (iPhone), dark "night observatory" style, one panel per row, traffic-light ✅ / ⚠️ / ❌ beside each rule. Panels, top to bottom:

1. **Header:** SS-ID + nickname, TIC, Tmag, binary period, sector(s), product(s), date vetted, Claude's verdict + confidence (also logged to the prediction scoreboard).
2. **Whole sector:** light curve with eclipses shaded, the candidate highlighted, momentum dumps as ticks, flagged cadences greyed.
3. **Zoom ±1 day:** data + transit model, with sinusoid/step alternatives faint; residuals underneath; ΔAIC printed.
4. **Same window in other products,** stacked (rule C8 / N10).
5. **Detrending robustness:** "found in 19 / 21" plus a mini strip of the 21 versions.
6. **Pixels:** per-pixel light-curve grid around the event + difference image with the target and Gaia neighbours plotted.
7. **Centroid** row/column time series around the event.
8. **Binary phase:** where the event sits relative to the eclipses (rule C5).
9. **Physics box:** implied radius on primary vs secondary; duration vs the allowed circumbinary range (C4, C9).
10. **Context:** Gaia neighbours (within 2′), RUWE, NSS flag, any TOI/CTOI/EB nearby, and the sector's DRN notes.
11. **Beginner checklist,** ten yes/no questions in plain words, e.g. "Is the dip in at least two different light curves?", "Is it nowhere near a thruster firing?", "Would the 'planet' be smaller than Jupiter ×2?". Ahmed answers, and that's the second key.

## 5b. Tools for wave 3 to test
| Tool | Licence | Last activity | Use |
|---|---|---|---|
| triceratops 1.1.0 | MIT | 2026-09-02 | FPP/NFPP (V10) |
| exovetter 0.0.16 | BSD-3 | 2026-04-27 | odd/even, secondary, centroid metrics |
| LEO-Vetter | **GPL-3.0** | 2026-07-29 | automated TOI-style vetting (used by Oddo+ 2026); install as a tool only |
| LATTE | LGPL-3.0 | 2024-06-21 | Planet Hunters' interactive vetting; not on PyPI |
| DAVE | MIT | 2020-01-27 | stale; photocenter idea only |
