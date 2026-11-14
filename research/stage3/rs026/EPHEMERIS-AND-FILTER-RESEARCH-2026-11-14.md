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

### Update after Codex 010 (Claude, 14 Nov 2026, 16:35)
- **What 010 measured (CONFIRMED, Codex, saved replays; one key on these numbers, Claude reread the tables):** V1 (timing term off) +25 planets, P 48.37% to 50.68%; V2 (centred on the frozen deepest-point refit, term capped at the catalogue width) +23, 50.54%. On the 112 affected G2 stars: real background 61 to 95 (V1) or 90 (V2), upside-down 3 to 5 or 8. Paired control fails in the two slowest bins for V0 too (pre-OAE baseline). OAE was off.
- **What it means for this design:** V2 is a cheap version of steps 3 and 4 and already gets 23 of V1's 25 planets (92%). So the full template fit (steps 1 and 2) can add at most about 2 planets to P; its value, if any, is cleaner window centres, not more planets. LIKELY: our deepest-point refit wanders on exactly these stars (offset 90th percentile 2.8 d, `rs026_offsets.py`), so a V2 window can sit off the real eclipse and let eclipse light through; that would show up as new real-light events near eclipses. Codex's proxy found none inside eclipse windows, but the proxy itself uses the same refit centres, so it cannot rule this out (UNCERTAIN).
- **Why V2 has more upside-down alarms than V1 (8 against 5):** NOT TESTED. Counts this small are within counting error of each other (Poisson: 5 and 8 overlap easily), so no design choice rests on it yet.
- **Decision rule, written before Codex 011 reports (so it cannot be tuned on 011):**
  1. If V2+OAE passes the 011 pass rule: adopt V2 as the FIX 94 change for Petrova 1.1 (smallest change, already measured); the template fit becomes a later study, not a G1 blocker.
  2. If V2+OAE fails only on upside-down background (rule c) and 011 shows the new events sit within 3 eclipse widths: build steps 1 to 3 (template fit, centres from the fit, not the deepest point) and measure it the same way; this is the case where the full design earns its cost.
  3. If V1+OAE also fails rule c, or the new events sit far from eclipses: the padding is hiding something other than eclipses; stop and research before any fix (root cause first).
  4. If both pass: V2, not V1 (V1 drops the timing term for every star, including any whose catalogue time is truly wrong by more than a width; V2 keeps a capped term).
