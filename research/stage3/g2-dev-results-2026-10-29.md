# G2 development slice: first full run of the frozen chain (29 Oct 2026)

DEVELOPMENT USE (G2-PREREGISTRATION.md section 3). The 301 development stars may be searched and used to choose v8. The 594 sealed stars have not been downloaded, searched or looked at. Aggregates only: no star ID and no event time is printed here. Interesting signals are not discoveries.

Code: the v7 search rules with the dataset switch (commit fd0eed2; `SS_SET=g2`). The switch was proved to change nothing on G1: all 5,082 star-sectors, 5,023 events, every field, tiers and flags equal (`zero-diff-dataset-switch.txt`, CONFIRMED). Run folder `data/stage3_g2/dev_73f62615e365` (settings hash 73f62615e365). Not a frozen release: it is a development run.

## 1. What went in
- Audit (`data/g2/audit`): 8,744 files, 8,740 ok, 4 "too little data", 0 errors. Products: QLP 3,352, SPOC 2,711, TESS-SPOC 2,681. 3,425 star-sectors; 3,253 have a usable best product (QLP 1,145, TESS-SPOC 1,107, SPOC 1,001); all 301 stars have at least one. CONFIRMED by counting.
- Cadence of the best product: 2 min 1,001, 3.3 min 898, 10 min 616, 30 min 738 star-sectors.
- QLP good-time windows: own SPOC 2,651, borrowed from 2 or more neighbours 361, one neighbour only 194, none 146. So 340 of 3,352 QLP files (10%) cannot be used safely; 172 of 3,425 star-sectors (5.0%) have no usable product (FIX-QUEUE 26). G1 sat in a dense field; G2 stars are spread over the sky.
- Median 6.5 h noise: SPOC 223 ppm, TESS-SPOC 243, QLP 284. Injected 8 h, 3,000 ppm dip recovered in the audit on 65.8% of best star-sectors.
- Sectors run to 107 (August 2026 files). Five TESS-SPOC files are labelled sector 1751 (FIX-QUEUE 25, UNCERTAIN what that label is).
- Search: 3,425 groups, 2,108 SAP-twin groups, all 2,108 PDCSAP checks done, 0 ERROR lines. 6,666 raw events before the union (3,655 real, 3,011 upside-down).

## 2. The upside-down ratio on this slice (`asymmetry_g2_v5.txt`, `asymmetry_g2_v6sap.txt`; 1,500 random star-sectors each, raw dips, no flags)
- PDCSAP half, upside-down divided by real: 0.89 at SNR 4.5, 0.92 at 5, 0.96 at 6, 0.98 at 7, 1.02 at 8, 1.04 at 10. So on raw dips the two sides are about equal (G1: the control overstated false alarms by 1.3 to 2.5 times).
- SAP twins: 0.50 to 0.56 at every bar: twice as many real dips as upside-down. As in G1 the SAP half has no fair control (FIX-QUEUE 18); its tier-1 list cannot be certified.

## 3. The headline and why it is not a signal
Tier 1 (best product): **90 real against 25 upside-down** (PDCSAP half 78 against 21; with ratio 0.98 the noise-expected real count is 21.4; Poisson chance of 78 or more: below 0.01 at SNR 7, 8, 10 and 12). Under the preregistered rule (section 5, which applies to the sealed slice) this pattern would read as an excess. It is not one:
- The 90 real tier-1 dips sit on only **29 of 301 stars**; 73 of them on 12 stars; the most on one star is 16. The 25 upside-down dips sit on 19 stars (most on one star: 4).
- Of 296 cross-sector pairs of tier-1 real dips on the same star, **238 fall within 0.25 d of the same point of the binary orbit** (chance expects 12; the upside-down set has 3 of 8 pairs). A planet's transits are not locked to the binary's clock; a leftover eclipse is.
- Orbit-locked (any two dips of one star in different sectors within 0.5 d of a whole number of binary periods): **54 of the 90 events on 8 stars.** Their orbital phases are not at 0 or 0.5 (0 of 54 within 0.03 of either), median depth 822 ppm, periods 5.5 to 20.6 d. LIKELY: shallow secondary eclipses of eccentric binaries, which the catalogue test (circular secondary at phase 0.5, and a BJD0 that is not always the primary eclipse; FIX-QUEUE 24) misses. NOT tested directly.
- Without those 54: 36 real on 25 stars against 25 upside-down on 19 stars. This is a post-hoc look and is NOT evidence either way.
- The flags are not the cause: the mirror-bump test (section 5) shows planet-shaped fakes pass about equally on both sides (dip 35% against bump 37% recovered, so the control is, if anything, slightly generous).

Reading: the chain works as designed, but a new rule is needed so that dips locked to the binary's orbit across sectors are flagged on BOTH sides (FIX-QUEUE 30). Until then the G2 sealed run would report a false "excess".

## 4. Split by the labels clause (`g2-by-label-dev.txt`; tier 1 real - upside-down)
(a) in the professionals' table: 178 stars, 44 - 20. (b) not in their table: 123 stars, 46 - 5. (c) TOI hosts: 29 stars, 8 - 7. (d) none of the three: 107 stars, 45 - 4. The (b) and (d) excesses come from the same few orbit-locked stars, so the split shows where the leaks are, not where planets are. No NASA-listed circumbinary host is in the development slice (the one in G2 is sealed).

## 5. Completeness through the whole chain (`chain_recovery_g2dev.txt`; 284 of 300 sampled star-sectors ran, 16 had no prepared product; 13,632 injections; zero-injection identity 284 of 284)
- Share of fake dips that become tier 1, 8 h box: 15% at 6 x the 8 h box noise, 30% at 8 x, 48% at 10 x, 57% at 12 x, 60% at 14 x, 60% at 18 x. 4 h box: 12%, 27%, 43%, 55%, 61%, 63%. 14 h: 9% to 45%. 20 h: 6% to 29%.
- K50 (depth where half come back): about 10.5 x the 8 h noise for 8 h dips, 11.2 for 4 h; not reached up to 18 x for 14 h and 20 h dips. Median 8 h noise 332 ppm, so an 8 h dip needs about 3,500 ppm (0.35%) to be found half the time. Planet size NOT computed: the G2 table has no stellar radius (depth first, size only as a labelled range once a radius exists).
- Where it is lost (dips at 10 x or more, 4,544 injections): not seen 7%, seen but not primary 3%, **tier 2 (flagged) 45%**, tier 1 45%. Flags on those tier-2 fakes (several can apply): flat-baseline step 55%, gap or dump 34%, 1 d ramp 18%, repeater 15%, C5 12%, eclipse overlap 10%, dominated 8%. The ceiling is set by the flags, as in G1 (44 to 64%).
- Mirror-bump test, pooled K 8 to 12: dip 35%, bump 37%, exact p = 0.001 (only dip 253, only bump 336). Small, and in the direction that makes the control generous, not harsh.
- By product family (dips, K 10 or more): SPOC family 49% of 2,832, QLP 38% of 1,712.

## 6. What this changes
1. FIX-QUEUE 30: a symmetric orbit-locked flag (v8 candidate), built from physics and tested on G1 and the development slice before any freeze.
2. FIX-QUEUE 24 (data-derived eclipse phases) gains evidence: the leaks sit at off-center phases.
3. Per-flag ledger (cost per flag from `rows_g2dev.pkl` against benefit from the upside-down ladder) is the next measurement for v8; the flat-baseline step flag alone removes more than half of the flagged fakes.
4. Nothing here is a candidate. No event has been opened or plotted.
