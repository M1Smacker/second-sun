# RS-033: can TESS's 2-second pointing record see the jitter near dumps? Feasibility on one sector (Claude, 14 Nov 2026, 11:32 pm, Opus 5.5 medium)

**Why:** RS-032 found our light-curve centroids (2 to 30 min averages) cannot separate DS-freed events from planets; the jitter is faster. T164 proposes the spacecraft's 2-second pointing record. Before Fable decides on Monday whether to spend about 46 GB (436 MB per sector, sectors 1 to 106 at MAST), this checks on ONE sector whether the record shows the pre-dump jitter rise at all.
**Cap, written first:** 0.6 weekly points, about 12 tool calls. One download (sector 11, 427 MB, logged). Design stars only.

## Method (written before computing)
- File: `tess2019140185400_sector11-quat.fits`, one table per camera, TIME (BTJD) and quaternion Q1 to Q4 at 2 s.
- Jitter per 30-min window: small-angle pointing error 2 x (Q1, Q2, Q3) in arcsec, minus the window mean; RMS combined over the three axes. Reference: median over windows more than 1 d from any dump (dumps from QUALITY bit 32 of design stars' SPOC files, as RS-031).
- **Q1 (the profile):** median jitter ratio in 1-h bins from 24 h before to 12 h after each dump, per camera. Expected from Vanderburg 2019: a rise before the dump. If none shows, T164 is dead.
- **Q2 (the events, descriptive only):** jitter ratio over the box of each sector-11 DS-freed real event and each planted bench crossing in the dump zone in sector 11, on the star's camera. Three events cannot decide anything; reported only.

## Results (11:33 pm; `rs033_quat.py`, `quat.json`; exploratory `rs033_drift_exploratory.py`)
**Feasible to read, but sector 11 shows nothing that would explain the excess. T164 as a guard: LIKELY not worth 46 GB.**
- **The record exists and is usable:** sectors 1 to 106, one table per camera, 2 s cadence, about 430 MB per sector (CONFIRMED, MAST listing and the sector 11 file). Sector 11: 15 dumps from design stars' files.
- **Fast jitter (Q1, preregistered):** RMS within 30-min windows, relative to windows more than 1 d from a dump, by hour from the nearest dump (all 4 cameras alike, camera 1 shown): 24 h before 1.10, 12 h before 0.95, 8 h 0.95, 6 h 0.96, 4 h 1.01, 2 h 1.01, last hour 1.06, **dump hour 4.5**, 1 h after 1.13, 6 h after 1.28. So the fast jitter barely rises before a dump (up to +7% in the last hour), spikes at the dump, and stays about 10 to 30% high for hours after (as Eisner 2019 says). CONFIRMED for sector 11.
- **Slow drift (exploratory, NOT in the written method):** the pointing walks away from where it was just after the last dump, smoothly, all the way to the next dump (camera 4: 0.25 arcsec 24 h before, 0.32 at 12 h, 0.38 in the last hour; camera 1 about 0.57 flat over the last day), then resets to 0.02. 0.3 to 0.6 arcsec is about 0.02 to 0.03 of a TESS pixel (21 arcsec). A smooth ramp, no feature 6 to 12 h before a dump.
- **Events (Q2, descriptive):** the 3 sector-11 DS-freed real events have box jitter 0.92, 1.07, 1.28 (median 1.07); 8 planted crossings in the dump zone median 0.93. Three events decide nothing.

## What it means
- Claude's dump map (second key for Codex 014 part 1, `rs032/T35-BOX-RULE-2026-11-14.md` side file) shows a real excess 6 to 12 h before dumps (G2 19 / 3). In sector 11 neither the fast jitter nor the slow drift has anything special in that window. So that excess is UNCERTAIN in cause; NOT TESTED alternatives: a counting effect of the dump-rule window (it reaches exactly 12 h before a dump), eclipse leftovers that happen to sit there, or eras other than year 1. Codex 014 part 1 (exposure-normalised, G3 check) is the right next look.
- **For Fable (task 2, T164):** do not download all sectors. If she wants the pointing record, take 2 or 3 sectors from later eras (14 to 26, 27 to 55, 56 on) where dump cadence and pointing changed, and test the same two profiles first (about 1.3 GB).
- One sector only: the profiles are CONFIRMED for sector 11 and UNCERTAIN for other eras.

## Follow-up (11:34 pm): who makes the pre-dump excess? (`rs032/rs032_dumpmap_rows.py`, rows in `data/rs032/dumpmap-rows.csv`). CONFIRMED counts
- 6 to 12 h before a dump (G2 + G3, tier 1 under B with the dump half off): 22 real, 4 upside-down. The 22 real events come from **19 stars and 22 star-sectors, all in different sectors** (sectors 5 to 97, every product). Not a few stars repeating, not one era.
- Their boxes: 9 of 22 are 3 h; 13 are long (8 to 20 h), whose far edge reaches within a few hours of the dump.
- "Box contains a dump": 35 real, 8 upside-down, 31 stars, 35 star-sectors, spread the same way.
- Reading (LIKELY): a widespread instrumental effect tied to the approach of a dump, not a property of a few stars. The pointing record of sector 11 does not show it as jitter or drift, so the cause is still UNCERTAIN (candidates, NOT TESTED: the long boxes picking up the dump's own disturbance at their edge; detrending edge effects near the data gap a dump leaves; era-specific pointing). Codex 014 part 1 (exposure normalised, by product and era) is the next look.
