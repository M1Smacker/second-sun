# Petrova 1.0 eclipse mask: design note (Fable, 10 Nov 2026, the fix step)

**Status: a design with a tested prototype. Nothing in `pipeline/` was changed. Vesper 0.8.1 stays frozen.** Building this into a new version needs Ahmed's go, a new freeze per `research/stage3/VESPER-VERSIONS.md`, and never re-scores a sealed run.

## The fault being fixed (audit F-01)
`detect_v2.eclipse_mask_auto` masks any phase bin that is low in ONE sector's fold. In slow binaries a phase is seen once, so a planet's dip is masked. Real G2 light: a strong dip in a binary slower than 20 d is found 0 times in 25.

## The rule ("repeat rule"): an eclipse is a dip that comes back
Per STAR, all its sectors together (phase = time mod catalogue period, as now):
1. Flatten each sector (biweight, 2 d), pool all sectors, 600 phase bins.
2. For each bin: the folded median over all cycles, the number of distinct cycles that visit it (a visit = 3 or more points), and each cycle's own median. Centre m0 and robust scatter sig from the folded medians, as now.
3. A bin is an ECLIPSE bin only if its folded median is below m0 minus 4 sig AND
   - 3 or more cycles visit it (a median over 3 cycles is low only if the dip repeats), or
   - exactly 2 cycles visit it and BOTH are low (each below m0 minus the larger of 2 sig and 0.3 of the folded depth).
4. A low bin seen in only one cycle, or in two with only one low, is NOT masked. It is a **single-visit dip**: by repetition alone it cannot be told from an eclipse or a planet.
5. Eclipse runs are padded by 1.5 times their width, as now.
6. **Catalogue window (not in the prototype, needed):** the primary eclipse at the catalogue ephemeris and width (`stage3_core.eb_widths()`; G2 from Prsa 2022, G3 from the TESS Ten Thousand Catalog) is always masked, also when seen once. If a single-visit dip sits at phase 0.5 plus or minus the catalogue secondary width, it is masked as the circular secondary.
7. **Single-visit lane:** every other single-visit dip stays in the light, is searched, and gets the label `single_visit` (its own tier, for example 1S). It is never counted in S1. It goes to the binary-phase duration key (WO-F22) and to the eye. This is where a Kepler-16 like transit and an eccentric secondary eclipse both land; one more sector of light, or the duration key, separates them.
8. **Mirror rule for the control:** the upside-down arm is built from the light kept by rule 3 AND by the same rule applied to the flipped light (bumps that repeat are masked there). Then real and upside-down light have been through the same operation and the control is fair.
9. **Tests move:** every recovery test injects into raw loaded light before step 1.

## Prototype test on real light (`scripts/d01_mask_v1_prototype.py`, output `evidence/d01_mask_v1_prototype.txt`)
G2 SPOC 2-minute light, 10 stars per period bin with 3 or more sectors (up to 6 used), seed 2. Rules 1 to 5 and 8 only (no catalogue window, no lane). Small sample: each share is good to about plus or minus 0.15 to 0.3.

| Binary period | dip K 12 found: frozen / repeat | dip K 25 found: frozen / repeat | events per star-sector, real / upside-down: frozen | same: repeat rule | data kept: frozen / repeat |
|---|---|---|---|---|---|
| 5 to 10 d | 1.00 / 0.90 | 0.90 / 1.00 | 0.15 / 0.11 | 0.15 / 0.13 | 0.858 / 0.840 |
| 10 to 14 d | 0.40 / 1.00 | 0.10 / 1.00 | 0.16 / 0.35 | 0.31 / 0.35 | 0.857 / 0.849 |
| 14 to 20 d | 0.70 / 1.00 | 0.30 / 1.00 | 0.08 / 0.16 | 0.30 / 0.20 | 0.863 / 0.847 |
| 20 to 27 d | 0.30 / 1.00 | 0.00 / 1.00 | 0.17 / 0.35 | 0.65 / 0.44 | 0.914 / 0.912 |
| over 27 d | 0.00 / 0.80 | 0.00 / 0.90 | 0.04 / 0.11 | 0.39 / 0.16 | 0.926 / 0.935 |

Reading (LIKELY, small sample):
- The repeat rule finds the planted dips in every bin (0.8 to 1.0) where the frozen mask finds 0 to 0.7. It keeps the same amount of light.
- Below 20 d the two arms become equal within error (10 to 14 d: 0.31 against 0.35, where the frozen mask gave 0.16 against 0.35). That is the arm asymmetry of F-01 going away.
- Above 20 d the real arm now has MORE events than the upside-down arm (0.65 against 0.44; 0.39 against 0.16). These are eclipses seen only once that the repeat rule cannot confirm (about 3 single-visit bins per star in these bins, 0 below 20 d). That is exactly what rules 6 and 7 are for. Without them 1.0 would flood the real arm with single eclipses in the slowest binaries. So rules 6 and 7 are not optional.

## What the builder must still measure (work order: extend WO-F01 part B)
1. Add rules 6 and 7 to the prototype; rerun on 50 stars per bin, G2 and G3, SPOC family and QLP (QLP needs the windows applied first, as `stage2_search.prepare` lines 150 to 159).
2. Pass marks: planted-dip recovery at least 0.9 of the after-mask recovery in every period bin; real over upside-down event ratio between 0.8 and 1.25 in every bin for events outside the single-visit lane; events inside catalogue eclipse windows not higher than with the frozen mask.
3. Period accuracy: pooling sectors assumes the catalogue period keeps phase over years. Measure the phase drift of the primary eclipse between a star's first and last sector; if it exceeds 1 bin (1/600 of the period), refit the period from the eclipse times first (this also gives the TESS-derived ephemerides the FFI door v2 needs).
4. Stars with a second catalogue period: apply the rule once per period, as `mask_all_periods` does now.
5. The 2-visit rule's thresholds (2 sig, 0.3 of depth) are first guesses. Tune them ONLY on injected dips and synthetic eclipses, never on real events.
6. Eccentric binaries: the secondary is not at phase 0.5. With 2 or more cycles the repeat rule finds it wherever it is; with one cycle it goes to the lane. Count how many G2 and G3 stars have a lane dip that repeats at the same phase once a later sector is added (those are secondaries; this is the T145 question answered for free).

## Traps for the builder
- Do not edit `detect_v2.py`. New function, new module, new version, new freeze.
- Do not drop rule 8. Without the mirror, the control arm is biased again, in the other direction.
- Do not tune on the real-arm events that appear when the mask is loosened. Anyone looking at those events before a preregistration spends the blind light of the slow-binary re-search (`SLOW-BINARY-RESEARCH-PREREG-DRAFT.md`). The prototype printed counts only.
- The zero-difference proof against 0.8.1 will and must FAIL for slow binaries. The proof for 1.0 is the injection table, not sameness.
- 30-minute data: a "visit" of 3 points is 1.5 hours; check the rule on Sector 1 to 26 full-frame light separately.

## Cost (UNCERTAIN)
Finish the prototype and measure: Sonnet 1.5 to 2. Review and thresholds: Opus 1. Build into a version with tests, freeze: 3 to 5 (the ledger's "new frozen version plus full bug hunt").

## Amendment A (10 Nov 2026, after two more prototype runs): the design is NOT settled. Read this before building anything.
Two versions were tested on the same 20 G2 stars per period bin (seed 3). Columns: planted dip found at K 12 / K 25; events per star-sector with nothing planted, real / upside-down, outside the lane.

| Binary period | Frozen 0.8.1 | Pooled repeat rule (d02) | Hybrid (d03) |
|---|---|---|---|
| 5 to 10 d | 0.90 / 0.80; 0.12 / 0.13 | 1.00 / 1.00; 0.28 / 0.15 | 0.85 / 0.75; 0.12 / 0.12 |
| 10 to 14 d | 0.55 / 0.25; 0.24 / 0.30 | 0.75 / 0.95; 0.38 / 0.23 | 0.45 / 0.25; 0.23 / 0.23 |
| 14 to 20 d | 0.35 / 0.05; 0.36 / 0.21 | 1.00 / 1.00; 0.46 / 0.22 | 0.60 / 0.55; 0.32 / 0.12 |
| 20 to 27 d | 0.20 / 0.05; 0.15 / 0.14 | 0.75 / 1.00; 0.39 / 0.17 | 0.65 / 0.85; 0.11 / 0.05 |
| over 27 d | 0.05 / 0.00; 0.04 / 0.10 | 0.79 / 0.79; 0.13 / 0.06 | 0.65 / 0.70; 0.02 / 0.03 |

(Frozen and hybrid differ a little from run to run in the planted column because the dip time is drawn differently; each share is good to about plus or minus 0.2.)
- **Pooled rule (the text above, rules 1 to 5): best recovery, but it LEAKS.** With nothing planted the real arm has 1.6 to 2.3 times the upside-down arm in every bin, also under 10 d where the frozen mask is balanced. LIKELY cause: folding several years at the catalogue period smears eclipses that a per-sector fold catches (TOI-1338 shows binary-locked events under this rule too, `evidence/k01_known_planets.txt`). The catalogue window as coded removed almost nothing (the Prsa phase convention `Phip-pf`, `Phis-pf` is unverified). Do NOT build the pooled rule as written.
- **Hybrid (frozen per-sector runs, kept as eclipses only if low in 2 or more cycles; `scripts/d03_mask_v1_hybrid.py`): balanced arms under 14 d (0.12 / 0.12, 0.23 / 0.23), and it frees dips in slow binaries (0.55 to 0.85 found over 14 d, 77% to 100% of them in the single-visit lane). But at 10 to 14 d it recovers no more than the frozen mask (0.45 / 0.25), and the lane has a real-arm excess (0.25 against 0.08 over 20 d: eclipses seen once).** NOT TESTED why 10 to 14 d fails: first suspect, the planted dip's run is "confirmed" by an unrelated run within the phase tolerance (0.02 is 0.2 to 0.3 d at these periods), or the padding of a neighbouring confirmed run covers it.
- **What a builder should do next (Opus, about 1.5 points):** (1) print, for the 10 to 14 d failures of d03, whether the dip's run was confirmed and by which episode; (2) tighten the phase tolerance to the run width plus 2 bins and require the confirming episode to have a similar depth (within a factor 2); (3) verify the catalogue phase convention on 10 stars and add the catalogue window to the hybrid; (4) rerun on 50 stars per bin. Pass marks unchanged: planted recovery at least 0.9 of after-mask recovery in every bin, real over upside-down outside the lane between 0.8 and 1.25.
- **What is solid:** the fault (F-01), the principle (an eclipse is a dip that comes back; a dip seen once is a lane case, not a deletion), the mirror rule, and planting before the mask. What is not: the exact rule.
