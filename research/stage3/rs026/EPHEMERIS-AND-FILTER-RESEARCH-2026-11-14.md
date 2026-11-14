# RS-026: TESS-era eclipse times (FIX 94) and a wide scan for filter improvements (started 14 Nov 2026, 13:56 Kuwait, Opus 5.5 medium)

**Why:** RS-025 found the biggest fixable loss: the mask's timing padding blanks light curves of binaries with poor catalogue timing (up to about 64 planets). Codex 010 measures it; this stint prepares the fix design for Fable's round on Monday. Ahmed (14 Nov): also search widely for anything that improves the filter, with full control.

**Cap, written before the start:** 8 weekly points, about 150 tool calls. No helpers. Own data first.

## Questions
| # | Question | Decision it feeds |
|---|---|---|
| Q1 | Where do our eclipse times and their errors come from (G2 and G3 catalogues), and why are some errors so large? | which source to replace |
| Q2 | Do our own light curves already pin the eclipse times? (each light curve's stored Petrova offset across sectors) | can we fit TESS-era ephemerides at zero download cost |
| Q3 | Which published TESS-era eclipse ephemerides exist, how precise, for which stars (Prsa 2022 TESS EB catalogue, IJspeert, Gaia DR3, others)? | external source or our own fit |
| Q4 | How do professionals fit eclipse times and handle timing variations (apsidal motion, third bodies)? | fit design and its safety margin |
| Q5 | The weak pool (205, mostly QLP): does another product of the same sectors have lower noise? | product choice rule |
| Q6 | Wide scan: what else in recent single-transit and EB-planet work could improve the filter (detrending, vetting, ML triage)? | new Tree items |

## Findings

### Q1. Where our timing comes from. CONFIRMED (code and own data)
- G2 (and G1): Prsa et al. 2022 TESS EB catalogue, sectors 1 to 26 (`data/xmatch/ebs.csv`, `petrova_mask.load_catalogue`): P, BJD0 and their errors e_Per, e_BJD0. G3: TESS Ten Thousand Catalog table 3, which carries no timing errors (the loader sets them to NaN, so G3 windows get no timing term at all).
- `rs026_offsets.py`: 110 of 420 G2 design stars (26%) have a 3-sigma timing term over 0.5 d at some sector (median 1.9 d); **706 of the 711 blanked light curves belong to them**; no G2 light curve with a smaller term is blanked. On those stars our own measured per-sector offsets have median 0.28 d but a long tail (90% 2.8 d: the deepest-point refit wanders inside the huge search range); on the other stars offsets are near zero (90% 0.064 d).
### Q2. Do our own light curves pin the timing? PARTLY. CONFIRMED (own data)
A straight line through each star's per-sector offsets (373 G2 stars with 3+ searched sectors): median scatter 0.011 d; 306 under a quarter of the eclipse width. Of the 76 big-term stars with a fit, 33 are clean. The rest need a proper eclipse-time measurement (template fit), not the deepest-point refit.
### Q3. Published TESS-era ephemerides. CONFIRMED (primary pages)
- TESS Ten Thousand Catalog (Kostov et al. 2025, [arXiv 2506.05631](https://arxiv.org/abs/2506.05631)), sectors 1 to 82: table 4 updates 2,065 known EBs with TESS periods and T0, no errors given; **covers 2 of our 420 G2 design stars and none of the 110 big-term stars** (`rs026_ttc.py`). Not a source for G2.
- Villanova live catalogue ([tessebs.villanova.edu](https://tessebs.villanova.edu/)): lists sectors up to 88, but the entry checked (a public star on the front page, last modified Feb 2025) still has its epoch at BTJD 1516 (sector 7 era) with the same kind of period error. LIKELY not refit with later sectors (one entry checked).
- **Oddo et al. 2026** ([arXiv 2610.22625](https://arxiv.org/html/2610.22625v1), III.1), the newest TESS CBP search, met the same problem: "occasionally, the ephemeris becomes 'stale' or slightly incorrect in the final two years of TESS data. To account for this, we split the light curve into individual sectors, and in sectors beyond Sector 55, we manually recalculate the phase of both the primary and secondary eclipse, and mask according to the new phase center." They also mask data within 0.5 d of sector gaps and use SNR 10 with LEO-Vetter.
### Q4. How professionals time eclipses. CONFIRMED (Marcadon and Prsa 2024, [arXiv 2403.07694](https://arxiv.org/html/2403.07694v2))
Each eclipse time from a template fit (handles asymmetric eclipses; Kwee-van Woerden assumes symmetry), then an ephemeris fit and an eclipse-timing-variation check: about 20% of close binaries have a third body (light-travel time), and eccentric binaries show apsidal motion (primary and secondary drift in opposite directions). So a single straight line is not always enough; each sector must still be checked.
### Q5. Weak pool and product choice. CONFIRMED (code)
`audit_all_summary.py` already picks, per star-sector, the product where a test injection was found and, among those, the lowest 6.5 h noise. The 205 weak planets are a data limit, not a product-choice bug.
### Q6. Wide scan (decision-relevant only)
- Our gap-edge half (0.5 d) matches the field (Oddo 2026 masks data within 0.5 d of gaps; LEO-Vetter 2 durations). Our momentum-dump distance rule has no counterpart in Oddo, LEO-Vetter or mono-cbp (they rely on shape tests); RS-025 found it holds 23 planets. Supports a shape-based dump rule (RS-025 DS) over a distance rule.
- Oddo 2026 uses SNR 10, stricter than our 7; our looser threshold is a deliberate completeness choice, kept.

## Fix design draft for FIX 94 (for Fable's round on Monday and Codex's measurement; NOT adopted, NOT tested)
1. **Measure our own eclipse times:** for every catalogue star, every sector we hold: primary and secondary times by a template fit to the star's own folded eclipse (not the deepest point), with an error; real flux only.
2. **Fit a TESS-era ephemeris** per eclipse type (primary, secondary separately, so eccentric offsets and apsidal drift are caught); keep the residual scatter.
3. **Place windows per sector** at the fitted prediction; half-width = 1.5 x catalogue width / 2 + 3 x max(fit prediction error, residual scatter), never the catalogue's growing term. Where a sector's own measured eclipse disagrees with the line by more than a quarter width (third bodies, apsidal motion), centre on the measured time (Oddo's per-sector recentring).
4. **Fallback** when a star has too few eclipses to fit: cap the timing term at the catalogue width and record the star as "timing uncertain", so its coverage loss is counted, never silent.
5. **Arm symmetry:** one mask from the real flux, applied to both arms (as now). A planted dip must not move a fitted eclipse time: check by injection (Codex harness).
6. **Side benefit:** the measured secondary positions also cover RS-024's missed eclipses (secondaries without catalogue geometry) and FIX 24 (G2 ephemeris for c5 and ecl_overlap).
7. **Judged by:** Codex 010's V1 (upper bound) and V2 numbers first; then this design on the planet bench, T156 and both background meters.
