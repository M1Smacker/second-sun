# Candidate C0 (catalogue eclipse mask): design and sanity test (10 Nov 2026, Opus 5.5 medium, nested session)

PREDICTION (written before work, about 22:20 Kuwait): 1.3 weekly points, about 24 tool calls. Meter at start: weekly 17%, 5-hour 13%.

**Plain verdict: C0 needs the hybrid.**
- **Dips: PASS.** The catalogue windows lose no planet dips. m = 1.00 for every star masked by its catalogue window, in G2 and in G3.
- **Real light: FAIL.** C0 alone leaves recurring eclipse features unmasked: G3 has 77 real-arm events against 29 upside-down, and 43 of those 77 repeat at the same binary phase. The real over upside-down ratio fails its pass mark.
- **The cause** is missing or unlisted secondaries and other recurring features. It is not the phase convention, not drift, and not the pad.
- **G2's 9 to 14% dip loss** comes entirely from the 13% of stars with no catalogue widths, which fall back to the frozen mask.

Recommended next design: C1 = catalogue windows plus a repeat-confirmed lane (mask a phase only where a dip recurs in the sector), with no frozen fold anywhere.

Labels: CONFIRMED = measured by a script on our data that could have contradicted it. Counts only for set stars. Nothing in `pipeline/` was edited. Nothing was committed. Small samples (8 files per bin and family, about 75 usable per set), so every cell carries an error of about 0.1.

## A. Catalogue conventions (evidence `evidence/c0_stepA_catalogue_check.txt`, script `scripts/c0_stepA_check.py`)
| Item | G2 (Prsa 2022, `data/xmatch/ebs.csv`) | G3 (TTC table 3) |
|---|---|---|
| Period, primary epoch | Per, BJD0 (already BTJD), with e_Per and e_BJD0 | Per, T0-pri (BTJD); no errors |
| Widths | Wp-pf, Ws-pf (phase units) | Dur-pri, Dur-sec (hours) |
| Secondary position | Phis-pf (same absolute phase scale as Phip-pf) | T0-sec and Phase (agree within 0.005) |
| Usable primary width | 780 of 895 (87%) | 612 of 612 (100%) |
| Secondary width and phase | 480 of 895 (54%) | 402 of 612 (66%) |
| Secondary off phase 0.5 by more than 0.02 | 295 | 191 |
- **Phase convention, CONFIRMED:**
  - Phip-pf reads 1.000 (meaning phase 0) for 86% of G2. So the primary is at BJD0, and Phis-pf is on the same scale (Phis minus Phip has a median of -0.4997).
  - About 5% have Phip-pf near 0.475. The meaning of that group is UNCERTAIN; C0 ignores Phip-pf and its refit absorbs the shift.
  - Why the old "rule 6" removed almost nothing: NOT TESTED.
- **TOI-1338 (published), CONFIRMED:** the catalogue predicts the sector 98 primary at BTJD 3995.583, against the real 3995.62. Window width 4.9 h, depth 416 sigma, offset -0.09 widths. Prsa gives this star no secondary, so the phase 0.5 fallback is wrong for this eccentric binary.
- **Drift:**
  - The formal 3-sigma drift to sector about 98 is above 0.25 width for 64% of G2. On real data, 14 of 19 primaries sit within 0.25 width.
  - After a per-sector refit (both windows shifted together, by at most the 3-sigma drift or P/4), 18 of 19 do (G2) and 17 of 19 (G3). CONFIRMED on 20 + 20 stars.

## B. C0 (`scripts/c0_catalogue_mask.py`)
- **Windows:** `mask_runs(t, f, periods)` removes PADF x w / 2 around each catalogue primary and secondary. PADF = 1.5 was fixed in advance, not tuned.
- **Refit:** an optional per-sector refit (`C0_REFIT=1`, the default) replaces the drift term with 0.1 width.
- **Fallback flags, each counted:**
  - `no_cat`: the frozen mask is used.
  - `no_sec`: the secondary window goes at phase 0.5 with the primary width.
  - `extra_P`: a second period gets the frozen mask.
  - `no_refit`: no eclipse is covered in this sector.
- The windows are computed once from the real flux and applied to both arms.

## C. Sanity test (harness copy `scripts/c0_mask_loss.py`, which imports the Part A harness unedited; diagnosis `scripts/c0_leak_diag.py`)
Evidence:
- `evidence/c0_mask_loss_g2.txt`, `_g3.txt`: with refit.
- `evidence/c0_mask_loss_g2_norefit.txt`: run by the main session.
- `evidence/c0_leak_diag.txt`.

Private rows are in `data\fable_audit_mask\rows_<set>_c0.pkl`. Both sessions wrote to the same file, so the summaries were made right after each run.

**Dips, before/after (K 12 and 25, all durations), by period bin 5-10 | 10-14 | 14-20 | 20-27.4 | >27.4 d:**
| Group | 5-10 | 10-14 | 14-20 | 20-27.4 | >27.4 | all |
|---|---|---|---|---|---|---|
| G2, catalogue window (62 files) | 1.00/1.00 | 0.92/0.92 | 0.99/0.99 | 0.97/0.97 | 0.94/0.94 | m 1.00 |
| G2, no_cat with the frozen fallback (18 files) | 0.83/0.83 | 0.17/1.00 | 0.28/0.90 | 0.12/0.97 | 0.04/0.96 | m 0.30 |
| G3, catalogue window (74 files) | 0.90/0.90 | 0.94/0.94 | 0.96/0.96 | 0.96/0.96 | 0.94/0.94 | m 1.00 |

- **Hunt-level m (weighted):** G2 0.91 (K 12) and 0.87 (K 25). G3 1.00 at every K. The frozen mask in Part A gave 0.60/0.40 and 0.69/0.40. CONFIRMED.
- **Refit:** turning it off changes G2 m by at most 0.01 (0.90 and 0.86). The refit does not pull windows onto planet dips, at least at the depths injected.
- **Bumps:** before = after in every bin (0.87 to 1.00). The proof test passes.
- **Cadences removed (whole file):** C0 removes 0.02 to 0.11, against 0.04 to 0.16 for the frozen mask. C0 removes less in most bins.
- **Syzygy cost:** not measured. The harness puts injections in light the mask keeps, so dips that overlap a true eclipse are not in the sample. NOT TESTED. Expected to be about the masked share (2 to 11%).

**Real light, no injection, events real arm / upside-down arm (pass mark 0.8 to 1.25):**
| Bin (d) | G2 frozen | G2 C0 | G3 frozen | G3 C0 |
|---|---|---|---|---|
| 5-10 | 7/3 | 8/5 | 2/3 | 15/5 |
| 10-14 | 4/2 | 7/5 | 1/5 | 14/7 |
| 14-20 | 1/5 | 2/5 | 3/0 | 17/2 |
| 20-27.4 | 1/1 | 7/1 | 5/8 | 10/10 |
| >27.4 | 1/3 | 1/3 | 0/4 | 21/5 |

The counts are small (n about 15 files per bin). G3 under C0 fails clearly, at 77 against 29 overall. G2 under C0 is 25 against 19, failing in one bin.

**Where C0's real-arm events sit (CONFIRMED, `c0_leak_diag.txt`):**
| | G2 real / upside-down | G3 real / upside-down |
|---|---|---|
| Within 1.5 widths of the primary (edge leak) | 3 / 1 | 3 / 4 |
| Within 1.5 widths of the catalogue secondary | 0 / 1 | 5 / 2 |
| Away from both windows, star with no catalogue secondary | 10 / 6 | 37 / 6 |
| Away from both windows, star with a catalogue secondary | 10 / 11 | 32 / 17 |
| Events that REPEAT at the same binary phase in one file | 7 of 23 (3 files) | 43 of 77 (16 of 34 files) |
| The same, upside-down arm | 4 of 19 | 6 of 29 |

Reading:
- Edge leaks are rare, so the pad and drift are fine.
- The excess is recurring features at phases the catalogue does not list: unlisted or eccentric secondaries, and possibly other periodic dips. These are typical of the TTC stars, which are fainter and found by machine learning. A planet transit cannot repeat at the binary phase within one sector unless its period matches the binary's.
- These features are exactly what the frozen fold catches, and it catches them at the cost of planet dips.

## D. Decision
**C0 alone: NO.** It passes on dips but fails the real/upside-down check, and G3 would read a false excess.

**Failure attribution:**
| Candidate cause | Verdict |
|---|---|
| Phase convention | not the cause (CONFIRMED) |
| Ephemeris drift | not the cause after the refit (CONFIRMED) |
| Pad | not the cause (edge leaks 3/1 and 3/4) |
| Secondaries the catalogue does not list, or lists only partly | **the cause** (LIKELY; the 43 repeats point there; which feature each is: NOT TESTED) |
| Frozen fallback for no_cat stars | separately, the whole G2 dip loss (CONFIRMED) |

**Recommend C1 = C0 windows + a repeat-confirmed lane, replacing the frozen fallback everywhere:**
- Fold the sector at P and mask a phase interval only where a dip is seen in at least 2 separate cycles at the same phase (within 1.5 primary widths). One visit is never masked, so a single planet dip survives.
- For no_cat stars, the repeat lane runs alone.

This is Amendment A's repeat rule, but now only as an addition to the catalogue windows, so most stars barely depend on it.

C1 has a known blind spot: binaries with P over about 13.7 d show each phase at most twice per sector, and for P over 27 d about once, so the repeat lane cannot act there. For those stars, C1 equals C0 plus whatever the catalogue lists. The G3 slow bins (20-27 d and >27 d: 10/10 and 21/5) show this matters. The likely way to cover them is to confirm repeats across sectors (the same phase in two sectors). UNCERTAIN, and it needs design.

## E. Rest of the plan (weekly points; who runs it)
1. **C1 design and code** (repeat lane within a sector and across sectors, at most P/4 masked per period) plus the same harness at 8 per bin for G2 and G3: about 1.0. Opus judgment on the repeat thresholds, chosen only from injected dips and synthetic eclipses: inject a fake secondary at a random phase into real light, check that C1 masks it, and check that a single dip survives.
2. **Syzygy cost:** a harness variant that also injects inside eclipses (the share of the orbit masked) gives the "planets we cannot see" number for the book: about 0.3. Sonnet.
3. **Full test at 50 per bin, G2 and G3** (main session, step 4): about 0.6. Sonnet.
4. **Petrova 1.0 freeze** (NOT part of this job; needs Ahmed's yes): a new module (`mask_c1.py`, not an edit of `detect_v2`), a new version and hash, a preregistration, and no re-score of the sealed G2 or G3 runs. About 1.5 to 2.
5. **Book wording** waits for C1's numbers and Ahmed's call on the Part A stop sign. A safe sentence even now: "a catalogue-based mask keeps every injected dip that does not overlap an eclipse, but alone it leaves recurring eclipse features that look like planet events, so it needs a repeat check".

## Usage
Weekly meter: 17% at the start, 18% at the end (it moves in whole points). 5-hour meter: 13% to 22%, which is 9 points, or about 1.2 weekly points at 7 to 8 per point. Tool calls: about 47 over three turns. About 13 were lost to stops and re-sends, the wrong Python, two pandas name clashes, and a PowerShell pipe error.
- ACTUAL about 1.2 against the 1.3 PREDICTED, a ratio of 0.9, for the full job.
- Lesson: code plus machine runs again landed near 1.0 of the guess. About a quarter of the calls went on environment friction (interpreter, pandas `.flags`). Writing the known Python path and the "no `.flags` attribute" rule into the brief would save about 0.2 points next time.

## ADDENDUM (main session, Sonnet 5.5 Extra, 10 Nov 22:40): C0 was run; verdict "C0 alone is not enough"
Opus stopped at the whole-point meter tick before running C0, so the main session ran it. Configuration of the test: time-only mask (per-sector refit OFF, `C0_REFIT=0`), the catalogue's two-Gaussian width divided by 1.44 as fallback where the polyfit width is missing (G2 only), pad 1.5 widths, 50 files per period bin and product family. G2: 451 usable files (49 skipped, same reasons as Part A); G3: 378 usable files. Evidence: `evidence/c0_mask_loss_g2_full.txt`, `c0_mask_loss_g3_full.txt` (counts only; rows are private in `data\fable_audit_mask\`), plus the 8-per-bin runs `c0_mask_loss_g2.txt` (refit), `_g2_norefit.txt`, `_g2_2g.txt`, `_g3_quick.txt`, and `c0_conv_check.txt`. Scripts: `c0_catalogue_mask.py`, `c0_mask_loss.py`, `c0_conv_check.py`, `c0_full_run.sh`.

**Plain verdict: C0 fixes the planted-dip loss completely and breaks the control arm. Dips pass; the real-over-upside-down check fails by a wide margin (real eclipses leak through the catalogue windows). So C0 alone cannot be Petrova 1.0's mask.**

| Check (pass mark) | G2 frozen 0.8.1 | G2 C0 | G3 frozen | G3 C0 |
|---|---|---|---|---|
| Hunt-level m, K 12 / 18 / 25, all durations (at least 0.9) | 0.60 / 0.48 / 0.40 (Part A) | 0.99 / 0.98 / 0.98 | 0.69 / 0.54 / 0.40 | 1.00 / 1.00 / 1.00 |
| Cell-level m at K 25, every period bin | 0.01 to 0.66 | 0.92 to 1.00 | 0.00 to 0.45 | 1.00 |
| Bumps before/after, K 25 | 1.00 | 1.00 | 1.00 | 1.00 |
| Real over upside-down events, nothing planted, 5 to 10 / 10 to 14 / 14 to 20 / 20 to 27 / over 27 d (0.8 to 1.25) | 1.36 / 0.64 / 0.88 / 0.15 / 0.29 | 2.33 / 2.90 / 1.95 / 1.30 / 1.22 | 0.93 / 0.65 / 0.70 / 0.77 / 0.36 | 2.37 / 2.36 / 2.56 / 1.52 / 4.19 |
| Same, totals (real / upside-down events over the sample) | 62 / 110 | 215 / 115 | 65 / 93 | 328 / 134 |
| Share of cadences removed, 5 to 10 ... over 27 d | 0.164 / 0.140 / 0.113 / 0.079 / 0.050 | 0.117 / 0.124 / 0.087 / 0.118 / 0.074 | 0.128 ... 0.077 | 0.072 / 0.065 / 0.045 / 0.033 / 0.033 |
Reading (CONFIRMED as counts; the cause is LIKELY, NOT TESTED):
- The injection result is exactly what a time-only mask must give: before and after are the same set of cadences, so m is 1 wherever the catalogue gives widths. The remaining G2 loss (m 0.98) comes from 18 of 451 files with no usable width, where C0 falls back to the frozen mask (those files: dips found 0.21 before the mask against 1.00 after). 38 files used the two-Gaussian fallback and behaved like the rest.
- The control arm is broken the other way: the frozen mask starves the real arm of dips (ratio below 1 in slow bins), C0 floods it (ratio 1.2 to 4.2, about 100 extra real events in G2 and 190 in G3 over the sample). Eclipses the catalogue windows do not cover appear only on the real arm. LIKELY causes: the secondary window is guessed at phase 0.5 for 37% of G2 and 35% of G3 files (no catalogue secondary) while about a third of binaries are eccentric; widths smaller than first-to-fourth contact; ephemeris drift. Which one: NOT TESTED. I did NOT look at the individual events (blind-light rule of the slow-binary re-search); any fix must be tuned on injected dips and synthetic eclipses.
- The per-sector refit was dropped: it changed nothing in the injection test (8-per-bin run, same m) and it reads the flux (a flux-dependent step is how the original flaw arose).
- Phase convention, CONFIRMED on real light (counts only): the primary sits at BJD0, ignoring the catalogue phase column, including for the 2g-only stars (eclipse seen in 27 of 27 and 13 of 17 stars with Phip away from 0 and 1, against 17 and 4 if the phase column is added; control 27 of 28 either way). This reverses the earlier suspicion that the old "rule 6" removed little because of a missing offset: it is NOT the cause.
- Coverage: G2 780 of 895 stars have a polyfit primary width, 864 with the two-Gaussian fallback (ratio Wp-2g/Wp-pf: median 1.44, IQR 1.39 to 1.54, flat in period), 31 have none; G3 612 of 612. Secondary width and phase: 54% (G2), 66% (G3).

**Decision (LIKELY, for Ahmed):** build candidate C1 = C0 plus a data-driven complement that masks only residual dips that REPEAT (same phase relative to the catalogue ephemeris in at least 2 cycles of the star's light, pooling its sectors, with a tolerance set on synthetic eclipses), with the mirror rule so both arms go through the same operation, and a lane for single-visit dips that are not masked. Pass marks unchanged: m at least 0.9 in every bin at K 12 and 25, bumps 1.00, real over upside-down 0.8 to 1.25 in every bin, no new events inside catalogue windows. Budget: Opus design and first test about 1.5, Sonnet full test about 0.5. A Petrova 1.0 freeze needs Ahmed's yes and is separate.

## Usage record for this job (lesson for the next one)
- Opus: PREDICTED 1.3 weekly points and 24 calls; ACTUAL about 1 point (17% to 18%, 5-hour 13% to 17%) and about 32 calls over two turns, but only about 55% of the job done because the whole-point meter tick (18%) fired first. LESSON: never give a stop line as a whole-point weekly reading; use the 5-hour meter (about 7 to 8 points per weekly point) or a call count.
- Main session step 4 (run C0, debug the summary, refit test, fallback split, two-Gaussian fallback, convention check, G3 quick check, full run, write-up): PREDICTED 0.5; ACTUAL about 0.9 (weekly 18% to 19%, 5-hour 17% to 24%); ratio about 1.8. LESSON: a test that returns a surprise (the fallback files, then the arm ratio) multiplies the calls by 2 to 3; the machine runs were free (G2 full 99 s, G3 full 49 s).
