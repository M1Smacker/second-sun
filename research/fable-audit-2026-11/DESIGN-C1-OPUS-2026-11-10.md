# Candidate C1 (catalogue windows + repeat-confirmed complement): design and sanity test (10 Nov 2026, Opus 5.5 medium, nested session)

PREDICTION (written before work): 1.0 weekly points, 22 tool calls. Meter at start: weekly 19%, 5-hour 29%. Stop line: 30 calls.

**Plain verdict: C1 as built FAILS, and the failure is informative.**
- **Within one sector, for fast binaries, the repeat idea works on planted material.** Synthetic recurring eclipses are mostly masked, and G3 planted single dips are never cut.
- **The cross-sector lane for slow binaries (P of 13 d or more) costs planet dips and bumps.** It does so by matching them, by chance, with noise runs in other sectors.
- **A complement built from the flux reacts to the planted signal itself.** So bumps are lost as well as dips. The mirror rule holds (both are lost alike), but pass mark (b) fails.
- **Real over upside-down improves on C0 in G3** (43/26 against 77/29) **but still fails** in the slow bins.

Recommendation: keep C0 windows plus the WITHIN-sector lane only, for P under 13 d (call it C1f), and test it. For slow binaries, accept C0 and handle what leaks in the event classifier. The details are in "What next".

Sample: 8 files per bin and family, so each cell carries an error of about 0.1. Labels: CONFIRMED = measured by a script on our data that could have contradicted it. Counts only for real light. Nothing in `pipeline/` was edited. Nothing was committed.

## The rule (`scripts/c1_mask.py`)
1. **C0 windows:** catalogue primary and secondary, pad 1.5, time only, no refit. Stars with no catalogue width get no frozen fold any more; the complement runs alone with T0 = 0.
2. **Additive flatten** of the kept light: r = f minus a running median over the larger of 1 d and 4 widths. Under 2 minus f this gives exactly minus r, so the mirror rule holds by construction.
3. **Bins** of the larger of width/3 and 0.5 h. A LOW run is adjacent bins with z below minus Z; a HIGH run is adjacent bins with z above plus Z. Both kinds are collected.
4. **A run RECURS** if a run of the same sign sits at the same binary phase in a different cycle of the sector, with:
   - phase distance under the sum of the half spans plus 1 h,
   - half spans within a factor 2.5 of each other,
   - peak z within a factor 3 of each other.
5. **Slow binaries (P of 13 d or more):** a run can also match the star's other sectors (one product per sector), aligned on the catalogue epoch plus each sector's primary offset taken from the deep primary eclipse. The other sector's run must have peak z of at least Z + 2. The tolerance gets an extra 2 h.
6. **Masking:** a recurring run masks its phase interval (half span x 1.5 + 0.5 h) in every cycle of the sector. The capped total is 25% of the phase. The same cadences are removed for both arms.
7. **Single visits are never masked** (the single-visit lane).

Z was set to 5 from the synthetic test below. TOL, PAD and CAP were fixed in advance. The width rule, the strength rule and the Z + 2 rule were added after the first synthetic runs, on planted material only.

## Synthetic test (planted material only; `scripts/c1_synth_test.py`, `evidence/c1_synth_test.txt`)
Each sampled file gets a synthetic recurring eclipse in every sector of the star: width 3 to 8 h, depth 6 / 15 / 40 x the 8 h noise, at a random phase at least 3 widths from the catalogue windows. The current sector also gets one planted single dip (8 h, K 12). About 30 files per set (4 per bin and family). Results at Z 5:

| | G2 fast | G2 slow | G3 fast | G3 slow |
|---|---|---|---|---|
| Synthetic eclipse cadences removed (C0: 0) | 0.45 | 0.48 | 0.70 | 0.49 |
| Real-arm events left at the synthetic eclipse, C1 (C0) | 1 (8) | 2 (11) | 3 (19) | 1 (13) |
| Planted single dip: share of cadences removed | 0.23 | 0.39 | 0.00 | 0.20 |
| Planted dip found, C1 (C0) | 0.82 (0.91) | 0.56 (0.89) | 0.93 (0.79) | 0.78 (0.89) |

- Z 3 to 6 trade off as expected. A lower Z masks more eclipse but cuts more dips, and the slow lane is the planet-killer at every Z: dips are found at 0.44 to 0.83 against 0.89.
- Before the width and strength rules, G3 fast had no dip cost and G2 fast lost 0.17 to 0.36. Within one sector the rule is close to good. In G2 it still pairs the planted dip with similar noise runs.
- CONFIRMED (small n).

## Sanity run (Part A harness through `scripts/c0_mask_loss.py` with C1 swapped in; `scripts/c1_mask_loss.py`, `evidence/c1_mask_loss.txt`; Z 5)
| Pass mark | G2 | G3 |
|---|---|---|
| (a) dips: m of at least 0.9 in every bin, K 12 and 25 (cell before/after) | **FAIL**: 14-20 d 0.56-0.75 / 1.00 at K 25; 10-14 and 20-27 d about 0.7-0.9; hunt m 0.88 to 0.89 | **FAIL** in the slow bins: >27 d 0.78-0.83 at K 25, 20-27 d 0.86-0.88; fast bins pass (1.00). The hunt-level line printed 0.99, which contradicts the cells (UNCERTAIN, possibly the weighting); I rely on the cells |
| (b) bumps 1.00 | **FAIL**: 10-27 d 0.60 to 0.81 at K 25 | **FAIL** at 14-20 d (0.67); others 0.93 to 1.00 |
| (c) real over upside-down, 0.8 to 1.25 (C0 for comparison) | 1/3, 4/5, 7/3, 0/0, 1/2: counts too small in 4 of 5 bins; 14-20 d fails (2.33) | 5/3, 5/7, 5/0, 10/10, 18/6, i.e. 43/26 overall (C0 77/29). Passes at 20-27 d, fails at 5-10, 14-20 and >27 d. 10-14 d is 0.71 |
| (d) no new events inside catalogue windows | PASS (0; the windows are removed) | PASS (0) |

- **Cadences removed:** G2 0.10 to 0.26 (C0 0.07 to 0.12); G3 0.03 to 0.09.
- **Lane size:** NOT MEASURED in the harness run. In the synthetic runs at Z 5, single-visit runs were about 40 to 60% of all residual runs, and none was masked.

**Why it fails (LIKELY, from the two tests together):**
1. **Cross-sector chance matches.** Slow binaries have many sectors and many runs per sector. A planted dip or bump finds a same-sign partner at the same phase by chance. The extra 2 h tolerance plus the Z + 2 strength rule are not strict enough.
2. **The complement is built from the flux that contains the signal.** Unlike C0, the order of injection matters again. This is the original class of flaw, in a weaker form.
3. **The G3 >27 d leak (18/6) is not caught.** One sector holds only one visit, and the stricter cross-sector rule misses the real recurring features.

## What is still unsure
- Is the within-sector lane alone (C1f, P under 13 d) good enough? It is LIKELY good for G3 (dips 1.00 in the fast bins) and UNCERTAIN for G2 10-14 d (0.84 to 0.91 at K 25). NOT TESTED as a separate variant.
- What are the leaking real-arm events in the slow G3 bins? Brief rule: no position classification of real events, so this stays open. Synthetic eclipses show a one-visit-per-sector feature can only be confirmed across sectors, and that path costs planets.
- Small samples (n about 8 per cell). The full 50-per-bin run is for the main session, and only for the variant that is chosen.

## What next (recommendation; the main session decides)
1. **Test C1f:** C0 + the within-sector lane for P under 13 d only, Z 5, no cross-sector lane. It is the same harness: set PSLOW = 1e9 in a copy. Expect (a) and (b) to pass in G3 and maybe G2. Cost about 0.3 weekly points, about 10 calls. Sonnet can run it.
2. **Slow binaries:** do not mask from the flux at all; keep C0. Leftover recurring features then reach the event stage. There, an existing or new veto ("an event at the same binary phase as an event in another sector of the same star, same sign, similar width") acts on events, not cadences, so it cannot delete a planet dip before the search. Because it is applied to both arms, the arm check measures it directly. This is design work: Opus, about 0.5.
3. If both pass at 8 per bin: the full 50-per-bin run on G2 and G3 (main session), about 0.6.

## (i) What a Petrova 1.0 freeze would need (NOT part of this job; needs Ahmed's yes)
1. **A new module** (for example `pipeline/mask_c1f.py`) beside the old one. `detect_v2.eclipse_mask_auto` stays untouched, so Vesper 0.8.1 stays reproducible.
2. **A new version number** (Petrova 1.0), its row in `book/docs/versions.md`, and a new code hash recorded in the run manifest.
3. **A zero-difference proof against 0.8.1 that is EXPECTED to fail for slow binaries.** The whole point is that the new mask keeps light the old one deleted. So the proof should show identical results only where the masks agree (fast binaries without leaks), and list where they differ, as a planned difference rather than a bug.
4. **A preregistration** written and committed before any run: the rule, the thresholds, and the pass marks (a) to (d) on the dev split.
5. **No re-score of a sealed run.** G2 sealed and G3 stay as filed; the new mask is used only on a fresh pass, as described next.

## (ii) How the slow-binary re-search would run, in words for a non-expert
1. We already have the light on disk for every G1 to G3 star. Nothing new is downloaded.
2. For each binary we draw its eclipses where the star catalogue says they are, and cut out only those moments. Before, we guessed them from one month of light, which also cut out planet dips.
3. For fast binaries we also cut out dimmings that come back at the same point of the binary's orbit, because a planet's dip does not come back on the binary's beat.
4. Every curve is searched twice: once as it is, and once upside down. The upside-down copy tells us how many false dips noise alone makes, so we can see whether the real light has more dips than chance.
5. Only the counts are compared first. Any star with a surviving dip goes through the usual checks and stays private until two checks and Ahmed's yes. The old results stay as filed; this is a new pass with a new version name.

## Usage
- Meter at start: weekly 19%, 5-hour 29%. End reading in the chat report.
- Tool calls: 26 including this file (stop line 30). About 6 went on the regex and comment slip (KeyError `pri`) and the print-format crash.
- ACTUAL and ratio: in the chat report (the end-of-job meter read is call 27).
- Lesson: a design that has to be tuned (C1) needs 2 to 3 synthetic iterations before the harness run is worth its call. Budget about 10 calls per iteration and expect the second idea to be the one tested, not the first.

## ADDENDUM (main session, Sonnet 5.5 Extra, 23:35): C1f tested at full size
C1f = C0 windows + the within-sector repeat lane only (cross-sector lane switched off by `C1_PSLOW=1e9`, Z 5). 50 files per bin and family; G2 451 usable, G3 378 usable. Evidence: `evidence/c1f_mask_loss_g2_full.txt`, `_g3_full.txt` (and `_quick`), script `scripts/c1f_full_run.sh`. In the summaries the column labelled "C0" is C1f.
- **Planted dips (pass mark a): PASS.** Hunt m 0.99 in both hunts at K 12 and K 25; K 25 cells 0.96 to 1.00 before over after; bumps 1.00 in every bin (G2 10-14 d 0.99 to 1.00).
- **Real over upside-down events, nothing planted (pass mark c, 0.8 to 1.25): PARTLY.** By period bin (5-10 / 10-14 / 14-20 / 20-27 / over 27 d), real/upside-down counts:
  - G2: frozen 19/14, 16/25, 15/17, 4/26, 8/28; C0 49/21, 61/21, 37/19, 35/27, 33/27; **C1f 27/17, 27/22, 48/20, 34/26, 33/27** (ratios 1.59, 1.23, 2.40, 1.31, 1.22)
  - G3: frozen 13/14, 15/23, 16/23, 17/22, 4/11; C0 45/19, 85/36, 87/34, 44/29, 67/16; **C1f 23/16, 35/37, 51/36, 41/28, 67/16** (ratios 1.44, 0.95, 1.42, 1.46, 4.19)
  - Totals real/upside-down: G2 frozen 62/110, C0 215/115, C1f 169/112; G3 frozen 65/93, C0 328/134, C1f 217/133.
  The within-sector lane fixes the 10-14 d bin (G3 0.95, G2 1.23) and halves the excess elsewhere; the over-13 d bins are unchanged or slightly better because there is no cross-sector lane (G3 over 27 d stays at 4.19). Counts per cell are 17 to 87, so a ratio of 1.2 to 1.6 is inside the sampling noise of a binomial; 2.4 (G2 14-20 d) and 4.19 (G3 over 27 d) are not.
- **Verdict (LIKELY):** C1f is a sound mask for the fast bins and never costs a planted dip; the slow bins (14 d and over) still show a real-arm excess of eclipse-like features that appear once per sector. That is the part the event stage must handle (a cross-sector phase veto on EVENTS, which cannot hide a planet from the search). Next candidate C2 = C1f + that event-stage veto.
- Cadences removed: G2 0.09 to 0.14 (C0 0.07 to 0.12, frozen 0.05 to 0.16); G3 0.03 to 0.08.
