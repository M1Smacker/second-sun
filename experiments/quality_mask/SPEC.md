# Quality-mask experiment: frozen spec

*Written 2026-10-20 by Claude, before any arm was run. Base commit 0b8e633. Authority: Ahmed, 2026-10-20 ("Go with whatever u recommended"; weekly cap 35%; see RESUME.md). Review: Compass report of 2026-10-20 (REVISE; design adopted below). Anything changed after this file is committed goes under "Amendments" at the bottom, with the reason; nothing above is edited.*

## Question
Does our `HARD` TESS quality filter discard observations that would help recover real circumbinary transits on TOI-1338, and what does it cost to get them back?

## Verified facts the design rests on (read-only checks, 2026-10-20)
- HARD = 24319, DEFAULT = 17087; they differ only in bits 64, 1024, 2048, 4096.
- In the 10 sectors below, DEFAULT restores 45,502 cadences over HARD, all with bit 4096 only. PDCSAP flux is NaN on every one; SAP flux is finite on every one.
- Therefore PDCSAP + HARD and PDCSAP + DEFAULT contain the same finite cadences (a no-op), and the production loader would silently fill the restored cadences from SAP. **The mask can only be tested with SAP flux.**
- Published times near S30 (prediction only: damaged egress) and S62 (measured) fall in PDCSAP-NaN stretches of 2.39 d and 1.38 d; HARD leaves 0 of 180 cadences within +-3 h of either.

## Arms (the only comparison that isolates one change at a time)
| Arm | Flux | Mask | Purpose |
|---|---|---|---|
| **A0** | PDCSAP (with the existing SAP gap-fill) | HARD | the existing baseline, reproduced; must match `pipeline/accept_v2_results.json` |
| **A1** | SAP, normalised by its median over HARD-retained cadences | HARD | A0 vs A1 = effect of the flux choice |
| **A2** | SAP, same normalisation | DEFAULT | A1 vs A2 = effect of the mask (the question) |

## Held fixed across arms
Same TOI-1338 files (the 10 sectors in `accept_v2.py`'s `PUB` table: 6, 10, 27, 30, 34, 37, 62, 65, 68, 98); same published times (Wang and Liu 2024 Table 1; S30 is their prediction); the binary geometry P = 14.6084 d, D1 = 4.7 h, D2 = 6.1 h, secondary phase 0.454, pad 1.5, with the **primary epoch T1 found once per sector from A0 and applied by time to every arm**; `detect_v2.find_events` unchanged (2-day biweight, 10-minute bins, boxes of 3 to 15 h, SNR bar 7); recovery window +-0.3 d for known transits and +-0.25 d for injections; flipped control `2 - f`.

## Measurements
1. **Known transits** (per sector, per arm): cadences within +-3 h of the published time (all, kept after the eclipse mask, restored); whether an event lies within +-0.3 d; its SNR, timing offset, duration, depth; share of its box that is restored cadences; background (SAP_BKG) in the box relative to the sector median.
2. **Injections** (S98, real event removed as in the baseline; multiplicative batman transits, baseline parameters): sizes 5, 6, 7 R_earth at the **baseline's retained 7 times** (taken from A0; not recomputed under DEFAULT). Per trial and arm: recovered or not, SNR, recovered depth over injected centre depth, timing offset. A0 also reruns all 49 baseline trials (sizes 2 to 8) as the reproduction check.
3. **Exploratory restored-region injections** (A1 and A2 only): 6 and 8 R_earth at the centres of up to 6 restored stretches of S98 that are at least 0.6 d long and clear of eclipses; the search is run only when at least 90% of the transit window has data. Judged on depth fidelity and false events, not on recovery rate (HARD has no data there by construction).
4. **False alarms** (all 10 sectors, per arm): flipped-data events with SNR at least 7; exposure in days (retained and restored cadences kept by the eclipse mask); events per 100 days with exact Poisson 95% intervals; for A2, events whose box contains restored cadences vs events that do not.
5. **Restored-cadence quality** (A2): per sector, the robust scatter of 2-minute flattened flux in restored vs retained cadences, and the background level.

## Decision rules (fixed now; none is a universal threshold)
- **Reproduction gate:** A0 must reproduce the saved baseline field by field (event centres to 1e-6 d, SNR to 1e-6, counts exactly). If not, stop and report; nothing else is interpreted.
- **Known transits:** the S62 result in A2 is reported as found / not found (event within +-0.3 d with SNR at least 7, the existing bar). S30 is reported but never counted as recovery evidence by itself. A baseline-recovered transit (S10, S65, S68, S98) that is recovered in A1 but lost in A2 is **harm from the mask**. A change in SNR is attributed to the mask only if |A2 - A1| exceeds |A1 - A0| for that event; otherwise it is labelled "not distinguishable from the flux effect".
- **Injections:** reported as paired per-trial tables (discordant trials listed); the summary is the median SNR change A1 to A2 over trials recovered in both, with the range. No significance tests: 7 trials per size cannot support them.
- **Zero-restored events:** for any event whose box contains no restored cadences, the A1 to A2 SNR change is the pure effect of adding data elsewhere (noise estimate and detrend); it is reported separately.
- **False alarms:** descriptive. **Adverse** only if the rate of flipped events containing restored cadences (per 100 d of restored exposure) exceeds the rate of events without them (per 100 d of retained exposure) with non-overlapping exact 95% intervals. Overlapping intervals mean "inconclusive at this sample size", not "safe". The flipped count is not a calibrated false-alarm probability.
- **Adoption:** this experiment alone never changes the production detector or the target list. At most it characterises restored SAP data on one star.

## What this cannot show (stated in advance)
One star, two new testable transits (one a prediction), 7 injection trials per size, single-digit flipped counts, one sky position (scattered light depends on pointing). Nothing here transfers to the G1 stars without a replication on them.

## Safety
New files only, under `experiments/quality_mask/results/<UTC time>_<commit>/`; the script refuses to write elsewhere or to overwrite. It imports from `pipeline/detect_v2.py` only (never `accept_v2.py` or `diag_v2.py`). No downloads. A manifest records the commit, whether tracked files are modified, versions, and the sha256 of every input FITS file, `detect_v2.py`, `accept_v2.py`, the baseline JSON, this spec and the script.

## Amendments
*(none yet)*
