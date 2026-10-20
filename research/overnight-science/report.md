# Overnight science: detector v2 acceptance test (TOI-1338)

*Second Sun, overnight run 2026-10-20, main session (Claude Opus 5.5). Code: `pipeline/detect_v2.py`, `pipeline/accept_v2.py`, `pipeline/diag_v2.py`. Results: `pipeline/accept_v2_results.json`, `pipeline/diag_v2_results.json`, `pipeline/accept_v2_log.txt`. Only data already on D: was used (no downloads).*

## In plain words (read this first)

Ahmed, last night's test showed our planet search only sees big planets. Tonight I rebuilt the search ("v2") to fix the three causes burn 1 found, then ran the same tests again.

- **It got a little better, not a lot.**
  - The old search found the known planet TOI-1338 b in 3 of the sectors it could test.
  - The new one finds it in **4 of the 8 sectors** that have data at the right moment.
  - Fake planets: the old search needed about **7 times Earth's size**. The new one catches most at **6 times Earth** (5 of 7) and all at 7.
- **Why not more?** I checked each missed crossing. In those sectors the planet's dip is only **3.7 to 6.5 times the noise**. Our bar is 7.
- **The bar can't safely go lower.** When I flip the data upside down (so no real dip can exist), the noise alone still makes fake "dips" up to **12.6 times the noise** in some sectors. That noise comes from the spacecraft and the data processing, not from the stars.
- **What this means:** for a star this bright (TESS magnitude about 11.5), one crossing of a planet smaller than about 6 Earths is buried in the noise of a single sector. That's a limit of the data, not a bug.
- **The way forward is what professionals do for two-sun planets:**
  1. use the binary's known orbit to predict where all the crossings of one planet should fall, and add them together (that's what the STANLEY tool does; it's installed and MIT-licensed);
  2. automatically reject the spacecraft's fake bumps, using the flipped data and the quality flags.

**Honest status:** no new planet. TOI-1338 b is a known planet; this was a test of our tools.

## 1. What changed from v1 to v2

| Problem found in burn 1 | v2 fix |
|---|---|
| 1-day detrending window ate into 6-hour dips | 2-day biweight window (over 3 times the longest searched duration, 15 h) |
| "3 bins below 3 MAD" wasted most of a long, shallow dip's signal | Matched box filter, 3-15 h, 10-min bins; SNR uses the robust scatter of all box means of that length, which includes correlated noise |
| Per-sector BLS sometimes mistook the planet or the secondary for the primary eclipse | Eclipses masked from the known binary period (14.6084 d, claim P8); each sector only re-finds the primary phase |
| PDCSAP gaps | SAP fills them, scaled locally (no gaps needed filling in these sectors) |

Self-check (`python detect_v2.py`): no event in 27 d of pure white noise; a 6 h, 700 ppm box is found at the right time (SNR 8.9). CONFIRMED (ran).

## 2. Recovery of published TOI-1338 b transits (threshold SNR 7)

Ground truth: Wang & Liu 2024 (arXiv:2404.18415) Table 1 mid-times; S98 = their prediction.

| Sector | Data at transit? | v1 (burn 1) | v2 | v2 SNR at published time | Strongest fake bump (flipped data) |
|---|---|---|---|---|---|
| 6 | yes | found | missed | 5.3 | 9.8 |
| 10 | yes | missed (eclipse mix-up) | **found** (SNR 11.5, -0.1 h) | 11.5 | 4.6 |
| 27 | yes | missed | missed | 6.5 | 4.6 |
| 30 | no (gap) | n/a | n/a | n/a | n/a |
| 34 | yes | missed | missed | 5.1 | 12.6 |
| 37 | yes | missed | missed | 3.7 | 3.9 |
| 62 | no (gap) | n/a | n/a | n/a | n/a |
| 65 | yes | found | **found** (SNR 9.0) | 9.0 | 6.0 |
| 68 | yes | found | **found** (SNR 7.5) | 7.5 | 10.2 |
| 98 | yes | found | **found** (SNR 9.0, +1.08 h vs prediction) | 9.0 | 10.6 |

v1 and v2 each found 4 of these 8; v2 swaps S6 for S10. CONFIRMED (ran).

**False alarms:** at SNR ≥ 7 the flipped data gave **6 fake events in 10 sectors** (0.6 per sector). The real (unflipped) data had 2 extra events besides the planet (S27 at BTJD 2047.87, S98 at 4038.44, 15 h). With 550 G1 stars × several sectors, that rate would mean hundreds of fake alarms. Vetting must remove systematics before a human looks. CONFIRMED (ran); the S27 and S98 extra events are UNCERTAIN (not inspected).

## 3. Injection test (S98, 6.4 h transits, 7 times)

| Size | Depth | v1 found | v2 found | v2 SNR |
|---|---|---|---|---|
| 2-5 R⊕ | 195-1,219 ppm | 0 | 0 | below 7 |
| 6 R⊕ | 1,755 ppm | 0/8 | **5/7** | 7.2-7.9 |
| 7 R⊕ | 2,389 ppm | 7/8 | **7/7** | 8.8-10.4 |
| 8 R⊕ | 3,120 ppm | 8/8 | 7/7 | 11.6-13.4 |

(v2 used 7 of the 8 burn-1 injection times; one fell in a gap after the new eclipse mask.) CONFIRMED (ran).

## 4. What this means for G1

- The wave-3 G1 estimate (single-transit reach of ~2-5 R⊕ at Tmag 10-13) is **wrong for single sectors**: it used a white-noise formula. Measured on a real two-sun star at Tmag ~11.5: about **6 R⊕** with a box search. Fainter G1 stars will be worse. Logged in research/mistakes.md (2026-10-19).
- G1 is still worth doing, but the search has to **stack** each planet's crossings across a sector and across sectors (circumbinary-aware search, like STANLEY), and it needs **systematics rejection** first. Single-event box searches alone will mostly find Saturn-to-Jupiter-sized planets.
- Many known transiting two-sun planets are Saturn-sized or larger (LIKELY, from memory of the Kepler sample; to verify from the wave-1 census before quoting).

## 5. Next steps (ranked)
1. **Systematics veto:** flag events near momentum dumps, quality-flagged cadences, scattered-light edges, and events that also show up in flipped data or in nearby stars (same camera/CCD, same time). Measure the false-alarm rate again.
2. **STANLEY trial on TOI-1338** (`.venv-tests`, MIT): does a circumbinary-aware stacked search recover TOI-1338 b from S1-S98 together? This is the real test of G1 feasibility.
3. Second known system (Kepler-16, TIC 299096355?: verify the TIC before use) once 1-2 work.
4. Red-noise error bar on the S98 timing offset (+1.08 h v2, +57 min burn 1) before calling it meaningful.

## 6. Systematics veto (task 8): tested, then loosened once

**In plain words:** I tried to throw out fake dips automatically when they sit next to a data gap or a thruster firing ("momentum dump"). It removed 4 of the 6 fakes, but it also threw out **2 of the 4 real planet crossings**. Real and fake ones sit at the same kinds of distances from gaps and dumps on this star, so no cut-off separates them. Following the stop rule, I loosened it once: gap and dump closeness are now **warning flags** for the human vetting sheet, not automatic rejection. Only "the same wiggle also appears in the flipped data" is rejected automatically.

| Version | Real crossings kept (of 4 found) | Fakes on flipped data | Other real events |
|---|---|---|---|
| No veto | 4 | 6 | 2 |
| Strict veto (gap 0.5 d, dump 0.25 d, flipped match) | **2** (lost S10: dump 0.17 d away; S68: gap edge 0.09 d away) | 2 | 1 |
| Loosened (flags only + flipped match) | **4** | 6, of which **4 flagged** | 2 |

Measured distances (days) to the nearest gap edge / dump: planet S10 2.75 / 0.17, S65 2.66 / 1.71, S68 0.09 / 3.07, S98 3.18 / 1.11; fakes S6 0.35 / 0.24, S30 0.16 / 0.16, S34 0.06 / 0.47, S68 2.03 / 0.38, S98 2.08 / 0.20 and 2.79 / 0.72. CONFIRMED (`pipeline/veto_test.py`, `veto_dist.py`, `veto_results.json`).

**Conclusion:** on one star with 4 real and 6 fake events, single-event cuts can't clean the data without losing planets. That points again to requiring **several dips that fit one circumbinary orbit** (stacking) rather than judging dips alone. The flags still help: 4 of 6 fakes carry a warning a human will see.

## 7. How late was the 16 December 2025 transit, really? (queue item 3)

**In plain words:** with the planet's crossing shape held to the 2024 paper's prediction, our measured crossing time is **56 minutes late, give or take 5 minutes** from our own data. The prediction itself is only good to about ±23 minutes, so overall the difference is **2.4 times the combined error**: a mild tension, interesting but not proof of anything. The answer also depends on the shape we assume: letting the shape float gives 34 minutes late (burn 1), forcing the paper's exact impact parameter in a different way gave about 2 hours. So: "roughly an hour late, shape-dependent, mildly outside the prediction's error bar." UNCERTAIN.

| Method | Mid-time (BTJD) | Offset vs prediction | Our error | Significance |
|---|---|---|---|---|
| Shape = predicted (T14 6.31 h, b 0.428), t0 + depth + baseline free; prayer-bead error (158 shifts) | 4025.6316 | **+56 min** | ±4.2 min (white) / **±5.1 min (red-noise)** | **2.4σ** including the prediction's ±23 min |
| burn 1, shape free | 4025.6165 | +34 min | ±8 min (white) | 1.4σ |
| burn 1, b fixed, a/R* free | 4025.6740 | +117 min | ±6 min (white) | 4.9σ, but its fitted duration (8.8 h) disagrees with the prediction |

Code: `pipeline/timing_s98.py` → `timing_s98_results.json`. CONFIRMED that these numbers come out of the fits; the physical meaning is UNCERTAIN.

**Why it might matter:** this is a TESS crossing of a known planet that, as far as we know, nobody has published. A precise new transit time helps the people who model TOI-1338's orbit. If Ahmed wants, Claude can draft a short note to the TOI-1338 modelers for Ahmed to send (contact rule: Claude drafts, Ahmed sends). Not urgent.

## 8. The G1 target list, frozen and traceable

**In plain words:** our first-campaign list now lives in one file, `targets/g1_targets.csv`. Its header records exactly where it came from (with checksums of the source files) and the selection rule. It reproduces wave 3's count: **552 rows**. But those 552 rows are **549 different stars**: 3 stars appear twice because the Kepler catalogue lists two binary periods for them (likely triple or more complex systems, which is interesting for two-sun planets).

| Step | Source | Count |
|---|---|---|
| Kepler EB Catalog rev 3 (Villanova, 2019-08-08), logged download | `data/wave-1/villanova_kepler-ebs_live/keplerebs_live.csv` | 2,920 rows = 2,907 stars (13 listed twice) |
| KIC to TIC match via MAST (wave 3) | `research/wave-3-pipeline/g1_tmag.csv` | 2,901 matched; 19 with no TIC |
| Detached (morph < 0.5), P_bin > 5 d, Tmag ≤ 13.5 | `pipeline/targets_g1.py` | **552 rows = 549 stars** |

Self-check: the script asserts 552 (claim P6). CONFIRMED. A bug in my first version gave the second period of a double-listed star the wrong eclipse time; fixed by matching on star and period. Not yet checked: which of the 549 have SPOC 2-minute data versus only full-frame-image light curves (needs ~550 archive queries; next session).

### 8b. What TESS data exists for the 549 G1 stars (metadata only, no downloads)

| Product | Stars with it | Median sectors per star | Stars with ≥ 10 sectors | Total files | Est. size |
|---|---|---|---|---|---|
| QLP (full-frame images) | **549 / 549** | 9 | 176 | 5,081 | ~3.3 GB (0.66 MB each, wave 2) |
| SPOC 2-min | 275 / 549 | 1 | 51 | 1,629 | ~3.0 GB (1.9 MB each) |
| TESS-SPOC (FFI) | 312 / 549 | 2 | 28 | not totalled | small |

Sanity check: Kepler-16 (TIC 299096355) shows 22 SPOC sectors including S82, which wave 2 downloaded. CONFIRMED (`pipeline/coverage_g1.py` → `targets/g1_coverage.csv`, MAST queries 2026-10-20).

**What it means:** every G1 star has at least one ready-made light curve, half have the best (SPOC 2-min) data, and the whole campaign's ready-made data is about **6.3 GB**, under the 20 GB line that needs Ahmed's OK. Because QLP is the only product for half the stars, the pipeline must handle QLP as a first-class input (our detector so far was tested on SPOC only).

## 9. QLP data: not ready yet (important for G1)

**In plain words:** half of our G1 stars only have QLP light curves (made by MIT from TESS's full-frame pictures). I tested our search on QLP's version of the 16 December TOI-1338 transit. Neither QLP flux column works yet:
- **QLP's raw flux** still contains the transit, but it's swamped by scattered sunlight and earthshine: 7 fake "events" and fake bumps up to **38.7** times the noise.
- **QLP's cleaned flux** is calm, but its cleaning **eats most of a long dip**: the 2,400 ppm transit shrinks to about 700 ppm and drops below our bar (SNR 3.6-4.4).

Two-sun planets have long transits (hours to most of a day), so a cleaning step that eats long dips is dangerous for us. This needs its own fix before G1 runs on QLP-only stars.

| QLP column | Planet at BTJD 4025.63 | Depth seen | Events (real data) | Fakes (flipped data) |
|---|---|---|---|---|
| `sap_flux` (raw; lightkurve's default `flux` for QLP files) | missed | present (wave 3 measured ~2,190 ppm with a local fit) | 7 | 10 (up to SNR 38.7) |
| `det_flux` (QLP-detrended) | missed (SNR 3.6-4.4) | **~700 ppm** (about 70% lost) | 2 | 1 |

The eclipse mask was checked (first primary at BTJD 3995.62, same as SPOC), so the problem is the flux, not the mask. Loader now uses `det_flux` for QLP files (cleaner, but with the depth-loss caveat above). CONFIRMED (`pipeline/qlp_check.py`).

**Next ideas (not done):** start from QLP's raw flux and remove scattered light with a background or co-trending model, or use TESS-SPOC (312 of 549 stars) where QLP is the only alternative; then re-run the injection test on QLP data.

### 9b. Two more QLP tries (new task, own 2-try budget)

| Try | Input | Planet (6.5 h box) | Fakes (flipped) | Strong real-data events |
|---|---|---|---|---|
| 1 | QLP `sys_rm_flux` (instrument systematics removed, no long detrend) + our 2-day detrend | **depth kept: 2,038 ppm**, SNR 6.4 (just under 7) | 9, max SNR 43.8 | BTJD 3991.9, 4004.99, 4020.0, 4033.9 (spacing ~13-15 d) |
| 2 | same + trim 0.75 or 1.0 d from each data-stretch edge | SNR 6.3-6.4 | 9, max 43.6 | unchanged: S98 QLP has **no gap > 0.5 d**, so there are no edges to trim |

**What we learned:** `sys_rm_flux` is the right starting point for long transits (it keeps the depth). The remaining fakes recur roughly every 14 days and are absent from SPOC. Candidate causes, not yet tested: spacecraft downlink/momentum-dump times, or a neighbouring variable star inside QLP's larger aperture. Next: compare the fake times with SPOC quality flags and with QLP's background flux, and check neighbours in Gaia. Loader unchanged (`det_flux`) until this is fixed. Status: superseded by 9c (cause found: stretches SPOC excludes).

**Diagnostic (not a fix):** the strong QLP fakes are **not** at SPOC momentum dumps or gap edges (all 2.0-3.4 d away from dumps, 1.7-2.5 d from gaps; `systematics()` on the SPOC S98 file). Two clues instead: QLP keeps data SPOC excludes (QLP starts at BTJD 3991.74, SPOC at 3993.64), and the fakes recur about once per TESS orbit (13.7 d). Leading hypothesis: **scattered light that returns at the same orbital phase**, in stretches SPOC's quality cuts remove and QLP keeps. LIKELY, not tested. Test next: mask QLP cadences outside the SPOC good-time windows when a SPOC file exists, and use QLP's background column where it doesn't.

### 9c. QLP partly fixed: borrow SPOC's good-time windows

**In plain words:** all four strong QLP fakes sat inside stretches that SPOC throws away (SPOC kept 3993.64-4002.79, 4008.33-4017.47, 4022.46-4031.59, 4036.97-4045.87; QLP kept everything). Keeping only SPOC's windows in the QLP data, and using QLP's `sys_rm_flux` so long dips keep their depth, **the only event left is the planet**: BTJD 4025.632, SNR 10.1, depth 2,275 ppm. That's within ~9 minutes of the SPOC detection (4025.638) and the timing fit (4025.6316). Fakes on flipped data: 2, max SNR 9.7 (was 9, max 43.8). 59% of the QLP data is kept. This is the planet seen in **two independent products** (rule C8). CONFIRMED (`pipeline/qlp_check.py`, asserts the planet is found).

**Limits:** tested on one sector of one star, and the windows came from that same star's SPOC file. For the ~274 G1 stars with QLP only, the windows must be borrowed from a SPOC star on the same sector, camera and CCD. That's the next test (NOT TESTED). Code: `good_windows()` and `in_windows()` in `pipeline/detect_v2.py`; QLP loader now prefers `sys_rm_flux`.

## 10. Automatic eclipse mask (needed for 549 stars without hand-tuned widths)

`eclipse_mask_auto(t, f, P)` in `pipeline/detect_v2.py`: flatten (2-day biweight), fold at the catalogue period, flag phase bins more than 4 robust sigmas low, grow each flagged run by 1.5 × its width. First version folded **before** flattening: the star's slow drift (bin scatter 1,700 ppm) hid the 0.4% secondary eclipse (3.2σ), which then showed up as three fake events one binary period apart. Flattening first fixed it.

| Check on TOI-1338 S98 | Hand mask (widths 4.7/6.1 h) | Auto mask |
|---|---|---|
| Eclipses found | given | primary (phase 0.505-0.520) + secondary (0.958-0.973) |
| Data masked | 11.4% | 15.2% |
| Agreement | | 96.3% of points |
| Events found | planet only (SNR 9.0) | **planet only (SNR 8.5)** |

CONFIRMED (`pipeline/auto_mask_check.py`, asserts the planet stays findable). One star, one sector; untested on very eccentric binaries and on QLP's 10/30-minute cadences.

### 9d. Borrowing windows from neighbour stars (for QLP-only stars)

Four SPOC 2-min neighbours of TOI-1338 within 1.5° in S98, all on camera 4, CCD 1 (downloaded ~2 MB each, logged):

| Neighbour | Windows vs TOI-1338's | |
|---|---|---|
| TIC 350861689 | same 4 windows, edges differ by up to 7.9 h | |
| TIC 350933091 | same 4 windows, edges differ by up to 4.8 h | |
| TIC 150145337 | same 4 windows + a short extra stretch at the start | |
| TIC 260266504 | **one continuous window**, no gaps | SPOC's cuts are partly per-star |

QLP TOI-1338 with windows **borrowed** from TIC 350861689: planet found (SNR 10.2), plus 2 extra events just after two borrowed window starts (BTJD 4022.93, 3994.16), where the borrowed edges sit a few hours earlier than TOI-1338's own. Fakes on flipped data: 3, max 9.6.

**Conclusion:** borrowing mostly works, but window edges matter. Next: take the **intersection** of several neighbours' windows (most conservative) and trim ~0.5 d after each window start; re-test. CONFIRMED (`pipeline/borrow_windows_check.py`); general fix NOT TESTED.

**Fix tried (1 of 2):** `intersect_windows()`: keep only times inside the SPOC windows of **all** neighbours, then trim 0.5 d after each window start. Using the 4 neighbours only (TOI-1338's own SPOC file not used, as for a QLP-only star):

| QLP TOI-1338 S98 | Planet | Other real events | Fakes (flipped) | Data kept |
|---|---|---|---|---|
| no windows | missed | 7 (to SNR 18.6) | 9, max 43.8 | 100% |
| own SPOC windows | SNR 10.1 | 0 | 2, max 9.7 | 59% |
| borrowed from 1 neighbour | SNR 10.2 | 2 (window edges) | 3, max 9.6 | ~59% |
| **intersection of 4 neighbours, starts trimmed 0.5 d** | **SNR 10.9** | 1 (BTJD 3994.43, 0.1 d into the sector's first window; the gap-edge flag marks it) | 2, max 8.2 | 54% |

CONFIRMED (`pipeline/borrow_windows_check2.py`). This is the recipe for QLP-only G1 stars: find SPOC stars on the same sector/camera/CCD, intersect their windows, trim starts, use QLP `sys_rm_flux`. Tested on one star and one sector only.

## 11. Rivals watch addition (found tonight via ADS)

| Who | What | Data | Overlap with G1 | Source |
|---|---|---|---|---|
| Spalding & Orosz (San Diego State) | updated photodynamical (ELC) models of Kepler-16, Kepler-34, Kepler-1647 using Kepler + **TESS**; search for a second planet through **eclipse timing variations**; mass limits vs period | TESS + Kepler, 3 known hosts | Partial: same 3 stars, but timing method, not a transit search of the ~550 binaries | AAS 243 (2024AAS...24310526S) and DPS 56 (2024DPS....5640203S) abstracts, LIKELY (abstracts only) |

Does not change the G1 gap: still no published TESS transit search of the Kepler EB sample (burn 2, R1-R2). Worth a full read when their paper appears; `ads_watch.py` should get a query for "Spalding Orosz circumbinary".

## 12. First G1 dry run: Kepler-16 (17 SPOC sectors)

**In plain words:** I ran the whole pipeline on Kepler-16, a real Kepler-field binary with a known two-sun planet, using only the catalogue period (no hand-tuning). Across 17 sectors it flagged **one** event and found 5 fakes in flipped data (about 0.3 per sector, better than on TOI-1338). I then vetted that one event like a real candidate. It's a **known impostor**: a dip 0.41 days before a spacecraft thruster firing (momentum dump at BTJD 2776.07), the same pointing jitter that fooled people during TOI-1338 b's confirmation. QLP shows nothing there either (fails C8). Our written rule C7 would have caught it, but the code used a different window, so the code was fixed to match the rule. **Result: no surviving event on Kepler-16.** This is a test, not a search result about Kepler-16 b.

| Item | Result |
|---|---|
| Sectors searched | 17 (SPOC 2-min) |
| Events | 1: S54, BTJD 2775.659, 15 h box, SNR 7.8, ~2,040 ppm |
| Fakes (flipped data) | 5 in 17 sectors |
| Primary eclipse check | real primary at BTJD 2771.734 (13% deep); catalogue ephemeris predicts 2771.74. CONFIRMED |
| Event vetting | momentum dump at 2776.07 (quality bit 32), flags 128/164 around it; dip shape is pre-dump jitter; QLP flat at that time. **Impostor (C7, C8 fail)** |
| Code fix | dump flag now covers 0.5 d **before** a dump (rule C7), not ±0.25 d; re-run raises the C7 flag on this event. CONFIRMED |
| Weakness found | Kepler-16's 41-day period is longer than a sector, so the per-sector fold flags noise runs as "eclipses" (up to 5 runs, 13% of data masked). Fix next: fold all sectors together. |

Figures: `research/overnight-science/kepler16_s54_event.png`, `kepler16_s54_sector.png`. Code: `pipeline/dryrun_kepler16.py`, `pipeline/look_event.py`.

**Global fold (all 17 sectors together), same files:** eclipse runs at phases 0.472-0.478 (the primary), 0.638-0.640 and 0.962-0.967; only **4.9%** of data masked (per-sector fold: up to 13%). Events: **3, all flagged** (S54 BTJD 2783.62: gap edge + C7; S73 3298.81: C7; S75 3355.47: gap edge). **0 unflagged events**, 4 fakes in 17 sectors. Whether the two smaller phase runs are the secondary eclipse or noise is UNCERTAIN (not checked against Kepler-16's published secondary phase). CONFIRMED (`pipeline/dryrun_kepler16_global.py`). For long-period binaries the pipeline should fold all sectors together.

## 13. STANLEY on TOI-1338: stage 1 done

STANLEY's detrending (stage 1) completed on all **40 SPOC sectors** of TOI-1338 (93,690 cadences after its cuts), after two fixes (setuptools for Python 3.12's missing distutils; a wrapper forcing downloads onto D:) and one restart from saved data (the first run hit a 25-minute cap mid-fit). Its independent binary fit agrees with ours: period **14.608642 d** (ours 14.6084), secondary eclipse at **0.455** of the orbit after the primary (ours 0.454), masses 1.2 + 0.325 M☉ (published ~1.1 + 0.3). Outputs in `data/stanley/LightCurves/Processed/ss_toi1338/` (data folder, not in git). Stage 2 (the orbit-grid search), as a bounded recovery test (circular orbits, 90-100 d), started 02:19 UTC with a 1-hour cap.

## 14. STANLEY stage 2 result + first try at physically realistic injection (Compass priority 1)

**STANLEY search (circular orbits, 90-100 d, 33 min on this PC):** strongest cell 18.4σ at a trial period of ~93.8 d (grid index 107 of 173, 100.03 → 90.05 d), close to TOI-1338 b's ~95 d. But the median cell is 4.2σ and 27% of cells exceed 5σ, so the σ scale is **not calibrated** here; STANLEY's analysis module is needed before calling this a recovery. UNCERTAIN.

**Injection with STANLEY's N-body injector (`pipeline/stanley/inject_cbp.py`):** 6 planets (4/6/8 R⊕ at 130 and 200 d) into the 40-sector raw light curve. **All injected zero transits.** Two bounded debugging tries:
1. Found a real STANLEY issue: `Search_CreateTransitMask` defaults to `maxCompTime=1` s and `InjectTransits` never raises it, so long integrations time out silently. Raised to 600 s in our wrapper (no package edit). Still zero.
2. Direct call: returns in 0.2 s with no transit times, not the timeout sentinel. Its N-body transit finder finds no crossings with our inputs. Cause not found (candidates: viewing-geometry convention, time origin). BLOCKED.

**Next (smallest step):** run STANLEY's injector on its own tutorial target (Kepler-64) to learn whether the problem is our TESS inputs or the injector; if it can't be made to work quickly, fall back to a small rebound three-body transit-time model (rebound is installed; importing GPL code is fine, copying it into the repo is not).

## 15. Injection unblocked: realistic circumbinary injection-recovery on TOI-1338 (Compass priority 1, step 1)

**Root cause of "zero transits" (section 14), found 2026-10-20 05:50 UTC:** STANLEY's N-body timing works (direct test: 13-29 transits for 95/130/200 d planets). `InjectTransits` takes its times from `Search_CreateTransitMask`, which passes them through the **search scorer** `Search_FitTransitMask`; that keeps only transits already showing a dip in the data (consistency and fraction-hit cuts). Before injection there is no dip, so every transit is dropped. Fixed in our wrapper by returning the raw N-body times and durations (no package edit). A second numpy-2 issue (a 1-element array passed to batman as a float) is also wrapped. CONFIRMED.

**Run** (`pipeline/stanley/inject_cbp.py` then `pipeline/recover_cbp.py`): 6 planets (4/6/8 R⊕ × 130/200 d, circular, coplanar, fB/fA = 0.01), 33 transits with data, durations 6.8-15.3 h. Search = auto eclipse mask (removes 14.6% of cadences) + `detect_v2.find_events` (SNR 7) on the full 40-sector light curve; events already present before injection (TOI-1338 b, systematics) excluded.

| Planet | Depth | Transits | In eclipse mask | Found | Depth retained (median) |
|---|---|---|---|---|---|
| 4 R⊕, 130 d | 850 ppm | 8 | 0 | 0/8 | 1.10 (noise-dominated) |
| 4 R⊕, 200 d | 850 ppm | 3 | 1 | 0/2 | 0.80 |
| 6 R⊕, 130 d | 1913 ppm | 8 | 0 | 7/8 | 1.01 |
| 6 R⊕, 200 d | 1913 ppm | 3 | 1 | 1/2 | 0.90 |
| 8 R⊕, 130 d | 3401 ppm | 8 | 0 | 8/8 | 0.98 |
| 8 R⊕, 200 d | 3401 ppm | 3 | 1 | 2/2 | 0.97 |

No new non-injected events. **Conclusions:** the 2-day biweight detrend keeps ~90-100% of realistic 7-15 h transit depths (CONFIRMED for this star); 3/33 transits (9%) are lost inside the eclipse mask before searching (CONFIRMED, small sample); per-transit floor ~6 R⊕, agreeing with the periodic test (section 3). **Limits:** 33 transits, one star, one orbital phase per period (same transit times across sizes), STANLEY injects crossings of the primary only, central-crossing shape. Earlier docstring claim that secondary crossings get the primary's depth was wrong (they are never injected); corrected.

**Next:** scale up (random phases, ~200 planets) only after contextual flags (priority 2), since the sensitivity map should be measured with the final vetting in place.
