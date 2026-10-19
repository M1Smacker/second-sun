# Wave 4 claims (V-numbers)

| # | Claim | Source | Label | Checked |
|---|---|---|---|---|
| V1 | SPOC TPS: MES > 7.1 and ≥ 2 transits. QLP: SNR > 9 and BLS significance > 9. Odd/even flag > 5σ (QLP). Centroid offset ≥ 1 px suggests a background EB; SPOC offsets < 7.5″ not significant at 3σ. Depth rising with aperture → nearby source. 3-5 vetters per target. TOIs with SNR < 11 = priority 2. 565 of 2,241 prime-mission TOIs (~25%) were later flagged as false positives. Ephemeris match within 155″. | Guerrero+ 2021, arXiv:2103.12538 (ar5iv, first 100k chars) | VERIFIED | 2026-10-19 |
| V2 | TOI dispositions: PC U-shaped, EB V-shaped, V sinusoidal, IS ramp/transit-shaped, U ambiguous; EB/V/IS excluded from the catalogue | same | VERIFIED | 2026-10-19 |
| V3 | Blends are the main TESS false positive because of ~21″ pixels | wave 2 D1 + V1 logic | LIKELY | 2026-10-19 |
| V4 | Davies+ 2026 single-event detection: 30-min bins, 3 consecutive points < 3 × MAD of a 4-d window; candidate SNR > 5 | arXiv:2604.09435 (HTML) | VERIFIED | 2026-10-19 |
| V5 | Davies+ 2026 automated vetting: kept if found in ≥ 18/21 biweight detrendings (1-3 d windows); duration < 1 d; transit preferred if ΔAIC ≤ −2 vs sinusoid/step/linear; RMSE ≤ 1.2 → ambiguity flag; systematics = > 3σ outlier groups of events within 0.1 d; HARD quality mask; asteroid/background and per-pixel checks | same | VERIFIED | 2026-10-19 |
| V6 | Davies: events rejected as stellar eclipses if ≥ 3 share the same binary phase or coincide with a visible eclipse; 138 events rejected as nearby short-period EBs | same | VERIFIED | 2026-10-19 |
| V7 | TIC 319011894: one sector (S7), 2.2% eclipses at 8.3 d, event at BTJD 1495.8, ~0.2% deep; TIC radius 2.86 R☉ → ~4 R_J (implausible); RUWE 1.03, not in Gaia NSS; event in SPOC, QLP, eleanor, less clear in TGLC; no centroid shift | same | VERIFIED | 2026-10-19 |
| V8 | TOI-1338 b vetting: SPOC + DAVE centroids; Gaia: 6 sources within ΔT ~7 in a 13×13-px area, none in the aperture; P_unresolved ~10⁻³; background EB would need T > 18; FPP ~10⁻⁸; Sector 3 fakes = pointing jitter before momentum dumps (PSF analysis); eleanor vs SPOC consistent; durations vary with binary phase; intervals ~93 vs ~95 d; RVs single-lined; SOAR speckle: nothing within 3″ | Kostov+ 2020, arXiv:2004.07783 (ar5iv, first 100k chars) | VERIFIED | 2026-10-19 |
| V9 | CBP "smoking gun": transit durations near primary eclipse shorter than near secondary | same | VERIFIED | 2026-10-19 |
| V10 | TRICERATOPS: validated if FPP < 0.015 and NFPP < 10⁻³; likely planet if FPP < 0.5 and NFPP < 10⁻³; likely nearby false positive if NFPP > 10⁻¹ | Giacalone+ 2021, arXiv:2002.00691 (abstract) | VERIFIED | 2026-10-19 |
| V11 | Kepler DR25 Robovetter: fully automated vetting with measured completeness and reliability | Thompson+ 2018, arXiv:1710.06758 (abstract) | VERIFIED (abstract) | 2026-10-19 |
| V12 | Tool status: triceratops 1.1.0 (PyPI 2026-09-02, MIT); exovetter 0.0.16 (2026-04-27, BSD-3); LEO-Vetter (push 2026-07-29, GPL-3.0); LATTE (push 2024-06-21, LGPL-3.0, not on PyPI as tess-latte); DAVE (push 2020-01-27, MIT) | GitHub API + PyPI JSON | VERIFIED | 2026-10-19 |
