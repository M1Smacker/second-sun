# RS-038 findings: how the best searches keep planets through vetting and masking (Claude, Opus 5.5 medium, 15 Nov 2026, 6:55 to 7:05 pm Kuwait)

**Verdict: our biggest single planet loss is a blanket rule the field does not use. We hold every dip that falls 0.25 d after to 0.5 d before a thruster firing (momentum dump) at tier 2; that window covers about 20% of all data in Sectors 1 to 26 and about 7.5% later. mono-cbp instead uses a cross-star coincidence check that costs only "a few per cent" of planted transits, a 4-shape model comparison for steps, and the TOI-1338 b team used a pixel test (jitter makes dips in some pixels and bumps in others). Our files already carry the star-position columns such a test needs.** (CONFIRMED for the papers and our files; LIKELY for the gain.)

**Tasks A to C (7:13 to 7:40 pm, Ahmed's go):** (A) star-position jitter separates dump false alarms from planted dips only partly (J 12+: 12% of false alarms, 3% of dips), so it is one signal to combine, not the fix; (B) of 1,271 never-scored crossings, about 600 had good data, away from eclipses, in prepared sectors, and were cut for an unnamed reason: the biggest silent loss found, now F2's first target; (C) TESS release notes put dump disturbance at tens of minutes, not half a day; from Sector 56 one dump per orbit, at the start of data collection.

## Full paper read: mono-cbp (Davies, Brown, Gill, French 2026, [arXiv 2604.09435](https://arxiv.org/html/2604.09435v1)), sections 2 to 8 and Appendix A
- Eclipses are masked by phase (±width/2), not modelled: modelling "can create transit-like features" and eclipse depths change between sectors. Ephemeris decay left eclipse residue and false alarms; they refit ephemerides (BLS plus PDM). Same lesson as our RS-027 and Codex 012/014.
- Detrending: cosine plus 21 biweight windows (1 to 3 d); an event must appear in 18 of 21 ("detrending-independent"). This cut is their biggest planet killer: up to 67% of injected long shallow transits lost; it is what removes long-duration transits.
- Cross-star check (Skye metric, from Kepler DR25): group events within 0.1 d across targets per sector; flag groups that are 3-sigma outliers. Cost to planted transits: "of order a few per cent across the grid". Removes, with the other cuts, over 70% of false alarms on inverted light curves.
- Steps: a fitted model comparison (transit, sinusoid, line, two-polynomial step) by AIC (difference 2 or more), not a flag. Long transits distorted by detrending get misread as steps.
- Inverted light curves for injection (same idea as our upside-down arm). False alarms: 0.84 per light curve raw; 0.007 per light curve for clean "T" class.
- Data loss: TOI-1338 b crossed in Sectors 30, 62 and 68, but all three were removed by the lightkurve "hard" quality cut (stray light) before the search. Data cuts cost known planets.
- Benchmark: per-transit detection efficiency 0.41 to 0.61 for 0.32% to 0.46% deep transits (our reference planets are 0.3% to 0.6%). Our P 0.48 per planet is in the same range; 0.75 would be beyond the published state of the art for TESS single-event searches (LIKELY).
- They prefer SAP flux: PDCSAP showed spurious transit-like features and higher scatter for many eclipsing binaries.

## Paper read (method sections): TOI-1338 b discovery (Kostov and co-workers 2020, [arXiv 2004.07783](https://ar5iv.labs.arxiv.org/html/2004.07783))
- Found by eye (Planet Hunters TESS). Non-planet events were "artifacts caused by pointing jitter (mainly before reaction wheel momentum dumps)"; the test that separated them: per-pixel light curves where artefacts look "transit-like in some of the core pixels and anti-transit-like in others", and the star's image shape changing. CONFIRMED.
- Our own code notes the same history: on TOI-1338 dump distance did NOT separate real from fake (real 0.17 d from a dump), so the dump rule was meant as a flag for a human, never a reject (`pipeline/detect_v2.py` line 243 on). In the tier system it now acts as a hold.

## TESS data release notes (task C, CONFIRMED: PDFs downloaded to `data/tess-drn/`, read as text)
- Sector 1 (DRN 1): momentum dumps "take approximately 5 minutes", and "nominal pointing stability returns after 10 minutes"; flags cover the dump with "a 20 minute buffer". Dumps every 2.5 days. Manual excludes cover "a subset of cadences just before and during each momentum dump"; bit 5 flags are "caused by the unstable pointing at times near momentum dumps".
- Sector 14 (DRN 19): dumps every 4.4 days; excludes for pointing excursions over 21 arcsec. SPOC's own search de-emphasises "epochs with excess TCEs" (a cross-star check, like Skye).
- Sector 56 (DRN 80): "One momentum dump was performed in each orbit, at the end of each data downlink just before data collection resumed: because of this, the impact of the momentum dump on science should be minimal."
- Meaning: the documents support a disturbance of tens of minutes around a dump, not half a day. Our 0.5 d pre-dump window rests on one Kepler-16 dry-run event and the TOI-1338 team's note that jitter came "mainly before" dumps in Year 1 (when the wheels speed up). In Sectors 56 on, the window mostly duplicates the gap-edge flag. LIKELY: the window can shrink a lot in later sectors; Year 1 needs the jitter test.

## Task A: does star-position jitter separate dump false alarms from planted dips? (CONFIRMED as computed, `data/rs037/jitter.py`, metric fixed before the run)
J = largest combined star-position (MOM_CENTR) excursion during the event, in units of the sector's robust spread, after removing a 0.5-day running median. SNR 7+ events flagged near a dump. Planted dips use the REAL star-position data at the planted time, which is what a real planet there would face.

| Group | n | median J | J 5+ | J 8+ | J 12+ |
|---|---|---|---|---|---|
| Background, real arm | 879 | 5.5 | 0.55 | 0.28 | 0.13 |
| Background, upside-down arm | 815 | 5.3 | 0.52 | 0.27 | 0.12 |
| Planted planet dips | 744 | 3.9 | 0.34 | 0.11 | 0.03 |
| Planted, planets lost after detection | 103 | 3.9 | 0.33 | 0.09 | 0.02 |

- Both arms agree (the test treats them alike). Jitter separates, but only partly: a veto at J 12+ removes about 12% of dump false alarms for about 3% of planted dips; releasing the dump hold when J is under 5 frees about two thirds of planted dump dips but also about 45% of dump false alarms.
- Rerun with QLP included (QLP files carry SAP_X and SAP_Y positions, plus small and large aperture fluxes KSPSAP_FLUX_SML and _LAG): background real n 1,534 (J 8+ 0.25, J 12+ 0.12), upside-down n 1,513 (0.25, 0.12), planted dips n 1,255 (0.11, 0.03), planted lost n 178 (0.08, 0.02). Same picture across all products. The aperture-size pair in QLP is an untested extra signal (a dip on the target has the same depth in both apertures). It CANNOT be benched with today's injection, which changes only the searched flux column: a fair test must inject into the small and large aperture columns too (scaled by each aperture's share of target light). Same rule for any pixel test.
- Verdict: jitter alone is NOT the fix. It is one of three signals to combine (cross-star coincidence about 2 to 1, jitter about 3 to 1 at the tail, orbit vouching); F4 should measure the combination under Tree rule 1.

## Task B: why are 24% of planted crossings never scored? (CONFIRMED as computed, `data/rs037/neverscored.py`, `phase.py`; Astra 006 planted run)
Of 1,271 crossings that fall inside observed data but never got a score:

| Cause | Crossings |
|---|---|
| No cadence in any file (archive gap) | 0 (the bench counts only crossings inside data) |
| Only quality-flagged cadences (bit 13 stray light 32, bit 16 7, bit 8 manual exclude 5, others few) | 76 |
| Star-sector failed to prepare: "no safe windows" 165, "too little data after masking" 143 | 308 |
| Good cadences, sector prepared, crossing removed inside the chain (eclipse mask, windows, or the scored product lacked it) | **887** |

- Eclipse share: 29% of never-scored crossings overlap an eclipse time (phase 0 or 0.5), against 12% of scored ones, so about 220 crossings (17 points of the 1,292) are lost to eclipse masking, mostly in binaries under 15 days (39% and 33%). Part of this is physics (a crossing during an eclipse is hard for anyone: mono-cbp loses the same "syzygys"). Secondary assumed at phase 0.5 (rough for eccentric binaries).
- The rest, about **600 crossings with good data, prepared, not near an eclipse, still never scored**, is the largest unexplained silent loss in the project. Candidates: the safe-windows rule, the choice of the single scored product (another product had data), gap-edge trimming. This is F2's first target and the most promising "second F-01".
- 308 crossings sit in star-sectors that fail to prepare: "no safe windows" (165) is a rule we chose, not physics. Overlaps Astra 025 (load losses on T156).
- Stray light (bit 13) removes 32 crossings; small here, but mono-cbp lost three TOI-1338 b crossings this way.

## Our data (CONFIRMED, `data/rs037/dumpcover.py`, 443 SPOC and TESS-SPOC files)
- Share of cadences inside our dump window: Sectors 1 to 26 median 20.0% (90th percentile 28.3%); 27 to 55: 7.5%; 56 on: 7.3%.
- Star-position columns MOM_CENTR, POS_CORR, PSF_CENTR present in 443 of 443 files (QLP not checked).
- We already have a cross-star flag ("common", 0.1 d, same sector and camera, `pipeline/stage3_core.py` line 206); the dump flag is an extra blanket on top.

## What this changes
1. F4 (Fable) gains a concrete, fair test: replace the blanket dump hold by (a) the existing cross-star flag plus (b) a jitter test from star-position columns (centroid excursion during the event). Fair bench: a planted dip costs a planet only if the REAL data at that time shows jitter, exactly what a real planet would face. Measure on both arms.
2. Window width: shrinking the pre-dump window from 0.5 d toward what the release notes support is a second, cheaper candidate (needs the notes opened and the upside-down count).
3. Stray-light and "hard" quality cuts may be part of the 13.8-point never-scored pool: add to F2 and Astra 025's checklist (which bits remove planted crossings).
4. Honest benchmark for Ahmed: the best published TESS single-event search sits at 0.41 to 0.61 per transit for planets like ours.
