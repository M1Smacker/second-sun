# Vesper versions and the before/after record

Numbering (chosen by Claude, 29 Oct 2026): **0.N.0** = the frozen Stage 3 version vN (rules changed, new settings hash). **0.N.x** = a patch that changes no rule and gives identical events on G1 (proved by a zero-difference test). **1.0.0** = the version that runs once on the sealed G2 slice. Stage 2 (the 50-star trial, 23 Oct) is 0.0.0.

| Version | Old name | Settings hash | Date | What changed |
|---|---|---|---|---|
| 0.0.0 | Stage 2 | (data/stage2) | 23 Oct | Box search 3 to 15 h, upside-down control, gap/dump, burst, flip-match and C5 flags, second-product check (rule C8) |
| 0.1.0 to 0.2.0 | v1, v2 | see learnings-2026-10-27 | 27 to 28 Oct | Stage 3 wrapper, tiers; v2 eclipse-overlap and repeater flags |
| 0.3.0 | v3 | 23a74c021d8a | 27 Oct | Flat-baseline (step) flag |
| 0.4.0 | v4 | d5767e66c4d2 | 28 Oct | 1 d ramp flag, dominated flag, measured eclipse widths |
| 0.5.0 | v5 | 5392f864e810 | 28 Oct | 20 h box added |
| 0.6.0 | v6 | f366d3682843 | 28 Oct | SAP twin searched too, union of PDCSAP and SAP |
| 0.7.0 | v7 | fd788be04650 | 28 Oct | Pooled common-moment flag replaces burst; SAP-only dips must show in PDCSAP |
| **0.7.1** | v7 + dataset switch | fd788be04650 rules; G2 dev run 73f62615e365 | 29 Oct | `dataset.py` (G1 or G2 by `SS_SET`); identical on all 5,082 G1 star-sectors. **Baseline of the Vesper study.** |
| 0.8.0 | v8 | (to come) | | Chosen by the study's yardstick (`VESPER-STUDY-PLAN.md` section 3) |

## How Vesper 0.7.1 works (the baseline, in plain steps)
1. **Read** every light curve of a star-sector: SPOC 2 min, TESS-SPOC (FFI), QLP (FFI; raw `sap_flux` before sector 56). QLP is cut to good-time windows from the star's own SPOC file or from 2 or more neighbours; otherwise not used.
2. **Mask** every catalogue binary period: the eclipses are found in the light itself by folding on the period (`eclipse_mask_auto`).
3. **Smooth** with a wotan biweight, 2 d window; bin to 10 minutes.
4. **Search** boxes of 3, 4, 5, 6.5, 8, 10, 12, 15 and 20 h; SNR = box depth over the measured scatter of the box statistic; keep SNR 7 or more. The same on the upside-down copy (2 minus the flux): the control.
5. **Second product:** look up the same time and box in the other products of the star-sector (1A agrees at 4 or more, 1L 3 to 4, 1B no other product, 3 disagrees).
6. **SAP twin:** search the SAP flux of the best SPOC or TESS-SPOC file too; a SAP-only dip must show at SNR 3 or more in the PDCSAP flux of the same file.
7. **Flags (any one sends an event to tier 2, never deleted):** gap edge or momentum dump; common moment (3 or more other stars with an event within 0.1 d, same camera); flip-match; C5 (within 0.35 d of catalogue phase 0 or 0.5); eclipse overlap (catalogue width); repeater (3 or more events of one kind in one product); step (flux before or after the box lifted by more than 0.5 of the depth, or a side with under half its data); ramp (within 1 d after data resumes); dominated (a stronger opposite-kind event in the same light curve).
8. **Tier 1** = primary product, no flag, second product agrees or absent.

## Baseline performance (0.7.1; the numbers every new version is compared with)
| Measure | G1 (549 stars) | G2 development (301 stars) |
|---|---|---|
| Star-sectors with a best product | about 5,064 | 3,253 |
| Tier 1 real / upside-down | 21 / 32 | 90 / 25 (54 real are orbit-locked on 8 stars) |
| Upside-down tier 1 per 1,000 star-sectors (false-alarm yardstick) | about 6.3 | about 7.7 |
| K50, 8 h dips (x the 8 h box noise) | about 11 | about 10.5 (about 3,500 ppm) |
| K50, 14 h and 20 h dips | not reached by 18 x | not reached by 18 x |
| Ceiling of tier-1 recovery (deep dips) | 44 to 64% | 28 to 63% |
| Fake dips at 10 x noise or more lost to flags | (see `chain_recovery_v7.txt`) | 45% |
| Mirror test (dip against bump, pooled) | 32% / 34% | 35% / 37% |
| Raw asymmetry ratio, PDCSAP half, SNR 7 | 1.3 to 2.5 (v4 to v5 files) | 0.98 |
Sources: `aggregate_v7.txt`, `chain_recovery_v7.txt`, `aggregate_g2dev.txt`, `chain_recovery_g2dev.txt`, `g2-dev-results-2026-10-29.md`.

## Before and after (filled as the study accepts or rejects options)
| Option | Version | 8 h K50 | 14 to 20 h K50 | False alarms per 1,000 | Mirror test | Verdict |
|---|---|---|---|---|---|---|
| Baseline | 0.7.1 | about 10.5 (G2 dev) | over 18 | 6.3 (G1), 7.7 (G2 dev) | pass | reference |
| C2: no data-cover rule in the step flag | 0.7.2 candidate (switch `c2`) | paired: never loses a fake; +1.7 to +4.4 points of dip recovery | long dips +53 (G1), +139 (G2 dev) net | 9.3 (G1), 12.6 (G2 dev) | pass | NOT ACCEPTED: false alarms over 8; at a bar that restores 8, net loss (-360, -138) |
| C1b+C2: re-smoothed step test | 0.7.2 candidate (switch `c1b,c2`) | 8 h about equal; 4 h +14, +35 | long dips +90 (G1), +195 (G2 dev) net, loses 67 and 51 | 9.3 (G1), 12.3 (G2 dev) | pass | NOT ACCEPTED: same reason (at the budget bar net -441, -164) |
| C4-lite: reweigh the nine flags | (no switch; analysis `flag_patterns.py`) | train G1 to G2 dev: +377 dips, 0 lost | n/a | 15.4 on G2 dev (train G1); +1 point in-sample (train G2) | n/a | NOT ACCEPTED: budget does not transfer between sets |
| C4: calibrated score (logistic, boosting) | (analysis `score_c4.py`) | -518 to +312 net depending on split | n/a | 3.1 to 17.1 per 1,000 on the held-out part | pass in design | NOT ACCEPTED: cannot calibrate on about 25 survivors |
| C1a: smoothing window 3 x box for every box | 0.7.2 candidate (switch `c1a`) | 8 h dips net -73 (G1), -163 (G2 dev); 4 h +54 (G1), -3 (G2 dev) | 14 and 20 h about even (-14, -8) | 6.3 (G1), 9.8 (G2 dev) | G1 pass (+2.2), G2 dev fail (+5.6) | NOT ACCEPTED: the short window eats 25% of an 8 h dip on a quiet star; step flag fires 30 to 95% more often |
| C1c: smoothing window 5 x box, long boxes only (10 to 20 h) | 0.7.2 candidate (switch `c1c`) | 8 h dips net -16 (G1, p 0.0001), -2 (G2 dev); 4 h about even | 14 and 20 h: +18 (G1, p 0.22), -34 (G2 dev, p 0.012) | not measured (stopped: sensitivity already failed) | pass (+0.6, +1.9) | NOT ACCEPTED: no gain on long dips, a net loss on G2 dev; deeper dips kept but more slow noise let through |
| C6: orbit-locked flag, tier-1 partners with matched box and depth | v8 candidate (switch `c6`, built 30 Oct; `V8-DESIGN.md`) | cost 0.81% of injected tier-1 dips (14 of 1,731, G2 dev); G1 none | none above 20 d binary period | G2 dev 25 to 23; G1 unchanged | not affected | PURITY OPTION, candidate for v8: removes 47 locked real tier-1 events on 7 stars; real minus upside-down excess on G2 dev +65 to +20 (bar 7), 0 (bar 12) |
| C5a: box floor, drop the 3 h box (switch `bf4`) | 0.7.2 candidate (switch `bf4`) | 8 h dips +1 (G1), +5 (G2 dev), p 0.3 to 1.0; 4 h dips -85, -87 (p<0.0001, the declared price) | 14 and 20 h: +6 (G1, p 0.03), +5 (G2 dev, p 0.06) | 6.9 (G1), 6.8 (G2 dev) | pass (+1.3, +2.5) | NOT ACCEPTED: no significant gain; the survivors move to the 4 h box (3 h and 4 h survivors together: G1 17 before, 17 after; G2 dev 20 before, 16 after), so little false-alarm room was freed |
| C5a + C2 (`bf4,c2`) | 0.7.2 candidate | 8 h dips +15 (G1), +31 (G2 dev); 4 h dips -72, -56 | 14 and 20 h: +59, +150, lost 0 | 10.1 (G1), 11.7 (G2 dev) | pass (+1.5, +2.2) | NOT ACCEPTED: above the budget of 8 on both sets; c2 alone was 9.3 and 12.6, so the floor freed nothing |
| C5a + C1b + C2 (`bf4,c1b,c2`) | 0.7.2 candidate | 8 h dips +13, +12; 4 h dips -76, -67 | 14 and 20 h: +93 net (160 gained, 67 lost, G1), +203 net (254, 51; G2 dev) | 9.3 (G1), 11.7 (G2 dev) | pass (+2.0, +2.9) | NOT ACCEPTED: above the budget on both sets |

Known weak spots of 0.7.1 found by the study's phase A (details in `VESPER-STUDY-PLAN.md` section 6): flags lose 38 to 45% of planet-shaped fakes; the step flag is the largest cost (alone 5.8 to 11.3% of fakes) and the largest guard; for 8 h dips it fires only through its data-cover rule near gaps; for 20 h dips the 2 d smoothing leaves raised shoulders (median +0.21 of the depth) and keeps only 68% of the depth.

## Benchmark baseline: Vesper 0.8.0 on G2 sealed (30 Oct 2026)
Run sealed_5f73692944aa, option c6, fingerprint 5f73692944aa. S1 NO EXCESS (real 26, upside-down 59, noise-expected 41.8 at bar 7). S2 8.91 per 1,000 (mark 8, FAIL on the mark; interval 6.80 to 11.47). S3 PASS (gap +0.1 points). S4 planted-dip recovery 4 h 41.0%, 8 h 46.8%, 14 h 34.1%, 20 h 28.0% (K 8 to 14). S5 13 events moved to tier 2, 0.51% cost. S6 TOI-1338 b: 1 of 7 strong tests (preregistered window). Full scorecard: research/stage3/benchmark-g2-sealed.txt. Later Vesper versions are compared against these numbers.
