# Wave 3: methods and tools (PARTIAL)

*Second Sun research, wave 3. Run inline by the main session (Claude, Opus 5.5) on 2026-10-19, 17:20-17:35 UTC. Hands-on wave. Claims P1… in `claims.md`. Status: **partial**; see "Not done yet".*

---

## In plain words (read this first)

**1. Our first campaign (G1) is feasible, for half the sample.** The Kepler eclipsing binaries are mostly faint for TESS: the median TESS magnitude is **13.6**. About **half (552) of the 1,112 binaries that matter** (detached, binary period > 5 days) are bright enough for ready-made light curves. For those, TESS can catch a planet from a **single crossing** down to:

| TESS magnitude | Smallest planet |
|---|---|
| 10 | ~2 × Earth |
| 11 | ~3 × Earth |
| 12 | ~3.7 × Earth |
| 13 | ~5 × Earth |

The known two-sun planets are 3-12 × Earth, so this is the right size range. The faint half needs do-it-yourself light curves, and there only Saturn/Jupiter-size planets will show.

**2. Our pipeline found a real-looking transit on its first try.** Practice target: TOI-1338 (the first TESS two-sun planet). In NASA's newest data for it (Sectors 97-98, Sep 2025 - Jan 2026), the search found **one dip, about 0.25% deep and ~6-7 hours long, around 16 December 2025** (BTJD ≈ 4025.5-4025.8):
- It survived **21 of 21** cleaning methods.
- It appears in **three independent light curves** (NASA's processed and raw fluxes, and MIT's QLP).
- No spacecraft warnings or thruster firings were nearby.
- Its depth matches TOI-1338 b.

**It's most likely a transit of the already-known planet TOI-1338 b, not a new planet.** Even so, it's useful: the discovery paper gave only a ≲30% chance per pass of transits continuing after Sept 2025, and nobody has published on these sectors (wave 1c). The next step is comparing it with the published predictions of TOI-1338 b's transit times. It is an internal result for now: no claims, no submission.

**3. The tools work on Windows (mostly).**
- The professional circumbinary search code **STANLEY installs**, and so does the binary-star model **ellc**.
- **Warwick's mono-cbp doesn't** (it needs an old library that Windows can't build). We can borrow its *method*, which is published, without its code.
- So far **we don't need Linux (WSL).**

**4. Two hiccups on this PC, both fixed and written down:**
- One of our tools (triceratops) quietly **downgraded** the core science libraries (numpy 2.5 → 1.26, scipy 1.18 → 1.13, astropy 8.0 → 7.2). Everything still works together, but it's recorded so nobody is surprised later.
- My Avast fix from wave 2 clashed with pip (an endless loop); it now skips pip.

---

## 1. Compatibility matrix (Windows 11 + Python 3.12.10, measured)

| Tool | Version | Installs? | Time | Notes | Licence (from package metadata) |
|---|---|---|---|---|---|
| lightkurve | 2.6.0 | ✅ | (wave 2) | needs the truststore fix behind Avast | MIT |
| astroquery | 0.4.11 | ✅ | (wave 2) | | BSD |
| wotan | 2.0 | ✅ | 24 s | detrending (Davies' method uses biweight) | MIT |
| transitleastsquares | 2.0.1 | ✅ | 5 s | pulls in numba 0.68 | MIT |
| batman-package | 2.5.3 | ✅ | 2 s | transit model (C extension: prebuilt wheel OK) | GPL-3.0 |
| rebound | 5.2.2 | ✅ | 2 s | N-body (needed by STANLEY) | GPL-3.0 |
| triceratops | 1.1.0 | ✅ | 119 s | **downgrades numpy → 1.26.4, scipy → 1.13.1, astropy → 7.2.3** | MIT |
| exovetter | 0.0.16 | ✅ | 8 s | | BSD-3 |
| PyTransit | 2.2.0 | ✅ (as a dependency) | | | GPL-2.0 |
| **stanley_cbp** | 0.2.8 | ✅ (separate venv) | 183 s | Tufts' CBP pipeline; MIT | MIT |
| **mono-cbp** | 0.1.9 | ❌ | 106 s | "Compiler cython cannot transpile": its `scipy<1.13` pin forces a source build; Windows has no compiler | GPL-3.0 |
| **ellc** | 1.8.15 | ✅ (separate venv) | 62 s | EB light-curve model | GPL-3.0 |
| PHOEBE 2 | (PyPI latest) | ✅ (separate venv) | 511 s | Claude's memory said Linux/Mac-only: WRONG, it installs on Windows | GPL-3.0 (not metadata-checked) |
| LEO-Vetter | git | ❌ | 55 s | build error installing from GitHub (subprocess error in the build hooks); revisit | GPL-3.0 |

All tools import together in `D:\second-sun\.venv` (VERIFIED: one import line with all of them succeeded, MAST reachable).

**WSL verdict: not needed** (STANLEY, ellc and PHOEBE 2 all install natively on Windows). STANLEY (CBP search) and ellc (EB modelling) run natively. Revisit only if PHOEBE is needed *and* fails.

**Licence note:** batman, rebound, ellc, PyTransit and mono-cbp are GPL. Using them as installed tools is fine; never copy their code into our MIT repo.

## 2. G1 feasibility (measured)

Source: Villanova Kepler EB catalogue (2,920 rows), cross-matched by KIC → TIC through MAST: **2,888 matched**.

| Sample | n | Median Tmag | ≤ 13.5 (ready-made light curves likely) |
|---|---|---|---|
| All Kepler EBs | 2,901 | 13.58 | 1,378 (48%) |
| **Detached (morph < 0.5) and P_bin > 5 d** | **1,112** | 13.51 | **552 (50%)** |

Tmag bins for the detached subset: <10: 28 · 10-11: 61 · 11-12: 114 · 12-13: 198 · 13-13.5: 151 · 13.5-14: 116 · 14-15: 264 · 15-16: 146 · >16: 34.

Noise, one detached EB per magnitude step: one sector each, eclipses masked from the Kepler ephemeris, 12-h flatten, 1-hour CDPP. Smallest planet for a 6-h single transit at SNR 7 around a 1 R☉ star:

| Tmag | KIC | Product / sector | 1-h CDPP | Smallest planet |
|---|---|---|---|---|
| 10.0 | 2697935 | SPOC 2-min, S81 | 120 ppm | 2.0 R⊕ |
| 11.0 | 10274244 | SPOC 2-min, S82 | 267 ppm | 3.0 R⊕ |
| 12.0 | 7887124 | SPOC 2-min, S15 | 412 ppm | 3.7 R⊕ |
| 13.0 | 6762188 | SPOC 2-min, S81 | 716 ppm | 4.9 R⊕ |
| 14.0 | 9164836 | none found | | DIY needed |
| 15.0 | 4940438 | none found | | DIY needed |

Caveats:
- Some of these hosts are evolved: TIC radii of 3.2, 2.2 and 12.5 R☉. Planets around those are much harder to see than the "1 R☉" column suggests.
- SPOC 2-min was available for these four; FFI-only stars at the same magnitude are ~15-25% noisier (wave 2, D34).
- One sample star per bin.

**Verdict: G1 is feasible** for Neptune-size-and-up circumbinary planets around the ~550 brighter detached Kepler EBs, and for giants among the fainter half (with DIY photometry). The ready-made-light-curve half costs roughly 10-20 GB (wave 2 budget).

## 3. Practice target: TOI-1338, Sectors 97-98 (PRELIMINARY INTERNAL CHECK)

Scripts: `toi1338_s97_98.py` (search) and `toi1338_event_check.py` (vetting). Picture: `toi1338_event_check.png`.

- **Binary, measured from the data:** P = 14.6084 d; primary eclipse T0 = BTJD 3937.1450, 4.7 h long, 5.13% deep; secondary at phase 0.454, 6.1 h, 0.40%. The off-0.5 phase matches the binary's known eccentricity of 0.16 (wave 1a).
- **Search:** HARD quality mask (27% of S97 and 37% of S98 cadences removed), eclipses masked (±1.5 durations), wotan biweight 1 d, 30-min bins. 30-min scatter = 594 ppm. Events = ≥3 consecutive bins < 3 MAD.
- **Result:** one event at **BTJD ≈ 4025.55-4025.72** (detection core; the visible dip spans ~4025.5-4025.8, ~6-7 h). Depth ~2,250-2,500 ppm; SNR ~7.6-8.4.
- **Checks against the wave 4 rules:**

| Rule | Check | Result |
|---|---|---|
| C2 | Detrending robustness | **21/21** biweight windows (1-3 d); depth 2,326-2,532 ppm |
| C7 | Spacecraft | no quality flags of any kind in BTJD 4024.6-4026.6; nearest momentum dump 4024.52, ~1 d **before** the event (outside the 0.5-d-before window) |
| C8 | Independent products | SPOC SAP 2,635 ppm; SPOC 20-s 2,216 ppm; **QLP 2,192 ppm**; TESS-SPOC not available for S98 |
| C5 | Not an eclipse | 0.76 d after the primary eclipse at 4024.795; outside the eclipse mask |
| C9 | Physical size | 0.22-0.25% on a ~1.3 R☉ primary ≈ 6-7 R⊕, matching TOI-1338 b (6.85 R⊕) |
| C6 | Neighbours (centroid, pixels) | **PASS**: difference image shows the dimming on the target's core pixels inside the SPOC aperture; a neighbour star (px 1,8) shows none; centroid shift 0.0-0.2σ (`toi1338_pixel_check.py/.png`) |

- **Calendar date:** BTJD 4025.6 = JD 2461025.6 ≈ **2025-12-16**.
- **Interpretation (Claude, logged in predictions.md): ~70% this is a TOI-1338 b transit.** Alternatives: another body, or a blend (pixel check pending).
- **Next:** compare with published TOI-1338 b transit-time predictions (Kostov+ 2020; the 2024 photodynamical reanalysis, arXiv:2404.18415) and run the pixel/centroid check.

## Not done yet (carry over)
1. PHOEBE 2 and LEO-Vetter install results (tests still running at write time).
2. Recovery of TOI-1338 b's *published* transits (S3, S6, S10): the formal ground-truth test.
3. Injection-recovery smoke test.
4. Processing time per star → batch sizes.
5. Comparison of the S98 event with the published TOI-1338 b ephemeris (the pixel/centroid check is done: PASS).
6. Reading for plan questions 1-6: the detrending literature, EB-removal methods, CBP algorithms (wave 1b covers most), anomaly methods.
