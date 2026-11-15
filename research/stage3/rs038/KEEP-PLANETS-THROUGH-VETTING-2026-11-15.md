# RS-038 findings: how the best searches keep planets through vetting and masking (Claude, Opus 5.5 medium, 15 Nov 2026, 6:55 to 7:05 pm Kuwait)

**Verdict: our biggest single planet loss is a blanket rule the field does not use. We hold every dip that falls 0.25 d after to 0.5 d before a thruster firing (momentum dump) at tier 2; that window covers about 20% of all data in Sectors 1 to 26 and about 7.5% later. mono-cbp instead uses a cross-star coincidence check that costs only "a few per cent" of planted transits, a 4-shape model comparison for steps, and the TOI-1338 b team used a pixel test (jitter makes dips in some pixels and bumps in others). Our files already carry the star-position columns such a test needs.** (CONFIRMED for the papers and our files; LIKELY for the gain.)

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

## TESS documents (lead only, from a search summary of the data release notes, PDFs not opened: UNCERTAIN)
Dumps last about 5 minutes and pointing is stable about 10 minutes after; dumps every 2.5 to 3.1 days in Year 1; bit 5 marks glints and unstable pointing near dumps. Our 0.5 d pre-dump window rests on one Kepler-16 dry-run event (rule C7). To check in the release notes before any change.

## Our data (CONFIRMED, `data/rs037/dumpcover.py`, 443 SPOC and TESS-SPOC files)
- Share of cadences inside our dump window: Sectors 1 to 26 median 20.0% (90th percentile 28.3%); 27 to 55: 7.5%; 56 on: 7.3%.
- Star-position columns MOM_CENTR, POS_CORR, PSF_CENTR present in 443 of 443 files (QLP not checked).
- We already have a cross-star flag ("common", 0.1 d, same sector and camera, `pipeline/stage3_core.py` line 206); the dump flag is an extra blanket on top.

## What this changes
1. F4 (Fable) gains a concrete, fair test: replace the blanket dump hold by (a) the existing cross-star flag plus (b) a jitter test from star-position columns (centroid excursion during the event). Fair bench: a planted dip costs a planet only if the REAL data at that time shows jitter, exactly what a real planet would face. Measure on both arms.
2. Window width: shrinking the pre-dump window from 0.5 d toward what the release notes support is a second, cheaper candidate (needs the notes opened and the upside-down count).
3. Stray-light and "hard" quality cuts may be part of the 13.8-point never-scored pool: add to F2 and Astra 025's checklist (which bits remove planted crossings).
4. Honest benchmark for Ahmed: the best published TESS single-event search sits at 0.41 to 0.61 per transit for planets like ours.
