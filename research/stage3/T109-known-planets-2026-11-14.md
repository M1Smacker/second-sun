# T109 early run: the two real circumbinary planets TESS has seen, through Petrova (14 Nov 2026, night, Claude)

**Plain verdict: Petrova finds one of the two real planets at tier 1 (TOI-1338 b) and misses the other (TIC 172900988 b), and both misses come from the same place the fake-planet bench says is the biggest loss: real dips that are found but held below tier 1 by data-edge flags. The real planets agree with the bench.**

This is an EARLY run of T109 (the road ahead puts T109 after brief 006 and its fixes). It is a baseline on Petrova 1.0.0 and on the bench (binary-locked repeater, rule b, plus FIX 91), so the same scripts can be rerun after the fix rounds and show what each fix bought on real planets. n = 2 planets: a reality check, not a rate. Both planets are published, so their names and transit times are public; nothing else is named. Nothing in `pipeline/` was edited; scripts import the frozen code read-only. Data: already on disk (TOI-1338 in the design-seen G2 files, TIC 172900988 in `data\known`, downloaded 29 Oct); no new download. No fenced star read (neither star is in fence A or B).

## Why only two planets
Of the 14 transiting circumbinary planets known, only TOI-1338 b and TIC 172900988 b have been seen transiting in TESS data (Davies et al. 2026, arXiv:2604.09435, introduction: "TESS has detected two transiting CBPs"; CONFIRMED, read verbatim). The Kepler planets' transits have mostly drifted out of view or fall outside the TESS sectors (an Orosz conference talk reports none clearly seen for Kepler-1647 in sector 41, UNCERTAIN, slides only). So the Kepler systems cannot test detection; they stay a later injection job (WO-F06 step 4).

## TOI-1338 b (binary 14.6 d; depth about 2,000 to 3,000 ppm, shallower than our reference band)
Times: Wang and Liu 2024 (arXiv:2404.18415) Table 1, 9 observed TESS transits (BTJD), read verbatim; plus their Table 3 forecast for sectors 89, 93, 96 and 98 (published before those sectors were observed). Stored events of the Petrova 1.0.0 development run, re-tiered exactly as Codex's 005 replay does. Script `research/stage3/t109/t109_toi1338_bench.py`.

| Sector | Result (1.0.0 and bench identical) | What held it |
|---|---|---|
| 3 | no light file (QLP sector 3 absent, SPOC 2-min starts at sector 4) | no data |
| 6 | **tier 1**, SNR 14.1 | |
| 10 | found, tier 2, SNR 14.4 | near momentum dump (every product) |
| 27 | found, tier 2, SNR 7.3 (SAP only) | ramp (within 1 d after data resumes) |
| 34 | **tier 1**, SNR 13.7 | |
| 37 | **tier 1**, SNR 11.3 | |
| 62 | not found | |
| 65 | found, tier 2, SNR 14.3 | **dominated** (an upside-down event in the same light curve is as strong) |
| 68 | found only in a non-primary product | gap edge, step, dominated |
| 89 (forecast) | found, tier 2, SNR 8.7 | dominated |
| 93 (forecast) | found, tier 2, SNR 10.9 | dominated (QLP copy: step) |
| 96 (forecast) | found, tier 2, SNR 15.1 | gap edge, step |
| 98 (forecast) | **tier 1**, SNR 10.0 | |

**Planet level: FOUND** (at least one transit at tier 1). Single transits at tier 1: 4 of 13 (31%), the same as the fake-planet bench (R 27 to 33%). 11 of 13 are found at some SNR of 7 or more; 7 of those are held at tier 2. The repeater fix changes nothing here (no transit carried the repeater flag). Comparison: the professional mono-cbp search found 6 of TOI-1338 b's transits and also lost sectors 3, 62 and 68, there to missing files and a stray-light cut (Davies et al. 2026, from the extracted summary, UNCERTAIN until the table is read verbatim).

## TIC 172900988 b (binary 19.66 d, e = 0.45; two transits 5 days apart in sector 21)
Times: Kostov et al. 2021 (arXiv:2105.08614) section 2, BTJD 1883.37 and 1888.30; binary ephemeris from their section 5 (P = 19.658025 d, primary BTJD 1878.3386); secondary phase from their Figure 1 eclipse times. This star is in no catalogue the Petrova mask reads, so the catalogue entry was built from the paper; the eclipse widths (not in the paper) were measured from the binary's own eclipses and tested at 0.75, 1 and 1.5 times. Scripts `t109_tic172900988.py` (mask and detection) and `t109_tic172900988_tier.py` (full event chain replicated step by step from `do_group`, `add_step` and `enrich_group`).

- **Mask: fixed.** The old 0.8.1 mask deleted 100% of both transit windows (Fable audit, 10 Nov). The Petrova 1.0.0 catalogue mask removes 0% of both, at every width tried, and the detector finds both in QLP: SNR 8.3 and 15.7, with zero upside-down events. CONFIRMED.
- **Without a catalogue entry** the eclipses stay in (the repeat lane needs two cycles in one sector) and the first transit falls to SNR 7.0. Petrova depends on the catalogue entry; Census stars come from catalogues, so this matters only for stars outside them.
- **Tiers: both held at tier 2.** The SNR 15.7 transit sits 0.64 d after data resume from the mid-sector downlink, so the ramp rule (1 d) holds it. The SNR 8.3 transit sits 0.25 d after a gap: gap edge, step (one side has too little data) and ramp. **Planet level: MISSED.**
- **Second product.** The TESS-SPOC 30-minute copy of the same sector is about 20 times noisier (per-cadence scatter about 6,000 to 8,500 ppm against 265 to 460 in QLP) and shows the transits at SNR 1.5 and 2.4. Under the tier rules a second product below SNR 3 "disagrees", so even with no flag the strong transit would be tier 3. A noisy copy that could not have seen the dip is counted as evidence against it: filed as FIX 92.
- **Negative control:** sectors 44 to 47 hold no forecast transit (Kostov et al. 2021 Table 7). With the catalogue mask: 0 to 3 real and 0 to 1 upside-down events per product and sector at SNR 7 (detection only, tiers not computed).
- Not replicated (stated, not hidden): QLP borrowed windows (no neighbour table for this star, so this is the best case), burst and common-moment flags (need other stars, assumed 0), the cross-sector p1 veto (no other sector has events at the same phase), the SAP twin pass.

## What this means for the filter
1. **The bench tells the truth on real planets.** 4 of 13 real transits at tier 1 (31%) against R 27 to 33% on planted ones. CONFIRMED for this one planet; LIKELY in general.
2. **Planet level matters.** TOI-1338 b is caught because it transits many times; TIC 172900988 b has only two chances, both beside a data gap, and loses both. This is exactly the question brief 006 (P) measures.
3. **The real losses are flags, not detection.** 9 of the 13 TOI-1338 b transits and both TIC 172900988 b transits are found at SNR 7 or more; what holds them is momentum dump, gap edge, ramp, step and "dominated". These are the node 1.1 flags the bench already blames (Codex 003: step 18, gap or dump 17, ramp 9, dominated 5 of the 53 held reference planets). New from the real planets: "dominated" costs 4 of 13 real transits on one eclipsing binary (FIX 93), and the second-product rule can sink a dip using a copy that is too noisy to see it (FIX 92).
4. **The Petrova mask works on a real planet.** The F-01 fix did what it was built for.

Labels: CONFIRMED = measured by these scripts on our data. Rerun after each fix round: the three scripts, unchanged. Outputs (event-level, private): `data\t109\`.
