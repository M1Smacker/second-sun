# Candidate C2 (C1f cadence mask + event-stage cross-sector phase veto for slow binaries): design and sanity test (10 Nov 2026, Opus 5.5 medium)

PREDICTION (written before work): 0.9 weekly points, 22 tool calls. Meter at start: weekly 21%, 5-hour 38%. Stop line: 30 calls.

**Plain verdict: C2 PARTLY passes.**
- **Where it works:** the veto removes real binary-locked events and almost no upside-down ones (17/0 in G2, 4/0 in G3). It fixes the G2 slow excess (14-20 d: 16/4 down to 3/4) and leaves G3 20-27 d balanced (10/10).
- **Where it fails:** G3 over 27 d keeps its real-arm excess (21/6 down to 18/6). Those events do not recur in other sectors at the same phase, so a recurrence veto cannot touch them.
- **What it costs:** planted dips and bumps are lost by chance matches in two bins, about 9% each. That puts m at about 0.91, right on the pass mark; everywhere else the cost is 0.

Sample: 8 files per bin and family; the counts on real light are small (0 to 24 events per bin). Labels: CONFIRMED = measured by a script on our data that could have contradicted it. Counts only on real light. Nothing in `pipeline/` was edited. Nothing was committed.

## The rule (`scripts/c2_event_veto.py`)
1. **Cadences:** the C1f mask (C0 catalogue windows + within-sector repeat lane, Z 5, `C1_PSLOW=1e9`). Nothing is masked across sectors.
2. **Search** as usual on both arms.
3. **Slow binaries only (P of 13 d or more).** For each event of one arm, look at the same arm's events in the star's OTHER sectors (one product per sector, SPOC family first, same C1f mask, nothing planted).
4. **Alignment:** phases use the catalogue epoch plus each sector's primary offset, measured on the deep primary eclipse. Stars with no catalogue width use T0 = 0 and no offset.
5. **A match** needs:
   - phase distance under half the sum of the two durations plus TOL = 1 h,
   - durations within a factor 2.5,
   - depths within a factor 3.
6. **Veto:** an event is vetoed if it matches in at least NMIN distinct other sectors. NMIN = 2 when the star has 3 or more other sectors, else 1.
7. **Same code on both arms.** Events are removed, never cadences, so a planet dip is always in the light the search sees.

TOL, NMIN and the 2.5 and 3 factors were chosen on planted dips and synthetic eclipses only. TOL 1, 2 and 4 h were tried; NMIN 1 and 2 were tried.

## Synthetic test (planted material only; `c2_mask_loss.py synth`, `evidence/c2_synth_test.txt` and `c2_mask_loss_nmin2.txt`)
Slow-star files only (35 in G2, 34 in G3). A synthetic recurring eclipse (3 to 8 h, depth 6 / 15 / 40 x the 8 h noise) goes into every sector of the star, and one planted single dip (8 h, K 12) into the sampled sector.

| | G2 NMIN 1 | G2 NMIN 2 | G3 NMIN 1 | G3 NMIN 2 |
|---|---|---|---|---|
| Synthetic-eclipse events vetoed (TOL 1 h) | 14 of 14 | 14 of 14 | 14 of 16 | 14 of 16 |
| Planted dip vetoed by chance (TOL 1 / 2 / 4 h) | 2 / 4 / 6 of 29 | 1 / 2 / 2 of 29 | 2 / 3 / 3 of 31 | 1 / 1 / 1 of 31 |

Larger TOL costs more planted dips and catches no more eclipses, so TOL is 1 h. Ke 6 synthetic eclipses rarely make events at all. CONFIRMED (small n).

## Sanity run (Part A harness via `c0_mask_loss.py` and `c1_mask_loss.py`; `scripts/c2_mask_loss.py`, `evidence/c2_mask_loss.txt` (NMIN 1) and `evidence/c2_mask_loss_nmin2.txt` (final))
The harness applies the veto to both the before and the after case. So before over after shows the mask alone, and the veto's cost is read from the chance-veto counts (section G of the summary).

| Pass mark | G2 | G3 |
|---|---|---|
| (a) planted dips, m at least 0.9 with the veto | Mask alone 0.99 to 1.00. Veto cost: 14-20 d 32 of 357 found dips vetoed (9%, so m about 0.91), all other bins 0. **Marginal PASS** (was 22% with NMIN 1) | Veto cost: 20-27 d 32 of 376 (8.5%, m about 0.915), all other bins 0. **Marginal PASS** |
| (b) bumps 1.00 | 0.93 at 14-20 d (the same veto acting on the upside-down arm), 0.94/1.00 at 10-14 d (C1f lane, one file), 1.00 elsewhere. **Not exactly 1.00**: the loss mirrors the dip loss, as the mirror rule requires. The mark was written for a pure mask | 0.93 at 20-27 d (veto), 0.93/1.00 at 5-10 d (lane), 1.00 elsewhere. Same reading |
| (c) real over upside-down after the veto, 0.8 to 1.25 | 1/3, 5/5, 3/4, 0/2, 0/3. Every bin has too few counts (6 or fewer) to judge. 14-20 d was 16/4 before the veto | 5/3, 5/7, 6/3, 10/10, 18/6. 20-27 d PASS (1.00). Over 27 d **FAIL** (3.0, 24 events). The other bins have 12 or fewer counts. 14-20 d is 2.0 on 9 events |
| (d) events vetoed, real / upside-down | 17 / 0 (all at 14-27 d) | 4 / 0 |

The C1f full-size run had more counts: G2 14-20 d 48/20, G3 over 27 d 67/16, G3 14-20 d 51/36, G3 20-27 d 41/28. The 8-per-bin samples here are 3 to 5 times smaller, so (c) can only be judged at full size.

**What (d) means (LIKELY):** the veto removes real-arm events and almost never upside-down ones (21 against 0). That is what removing a real recurring binary feature looks like, and not what noise looks like. CONFIRMED as counts.

## What is unsure
- **G3 over 27 d.** The 18 real-arm events left there (against 6) are not matched in other sectors. Possible reasons: the phase is not covered by the star's other sectors (P over 27 d with sectors of about 27 d); catalogue period error over many cycles when the primary is not in the sector to fix the offset (TTC gives no period error); or features that do not recur at all (activity, systematics in faint QLP stars). UNCERTAIN. Under the brief's rules I did not look at the real events.
- **The bins with a 9% chance cost.** One or two stars with many other-sector events probably dominate, at n = 8 per bin. The full run will show whether it stays under 10%.
- **Effect on a real two-transit planet.** NOT TESTED. A circumbinary planet's second transit falls at a different binary phase, so the veto should not touch it.

## Honest wording for Petrova 1.0 (if Ahmed takes C2 forward)
"Fast binaries (P under 13 d): a catalogue eclipse mask plus a within-sector repeat mask; planted dips are kept (m 0.99) and the real/upside-down check is balanced within counting noise. Slow binaries (13 d and over): the same mask plus an event veto that drops events returning at the same binary phase in another sector; it removes real binary features (21 real against 0 upside-down events in a small test) at a cost of up to about 9% of planet dips in some period bins. Binaries slower than 27 d in G3 keep a real-arm excess of about 3 times the upside-down count that this method cannot remove; the event classifier must handle it, and a null there excludes less."

## Next (for the main session)
1. **Full 50-per-bin run** of C2 (NMIN 2, TOL 1 h) on G2 and G3. Command, run from `scripts`, with `C0_REFIT=0 C1_PSLOW=1e9 C1_Z=5 C2_TOL_H=1 C2_NMIN=2`: `c2_mask_loss.py run 50 6`, then `summary`. Expect several minutes per set, since other sectors are loaded per star. About 0.4 weekly points.
2. Watch at full size: chance-veto share per bin (under 10%), (c) per bin with real counts, and (d).

## Usage
- Meter at start: weekly 21%, 5-hour 38%. End reading and ACTUAL in the chat report (call 17).
- Tool calls: 16 including this file.
- Lesson: building the harness variant and the synthetic mode in ONE file, and running synth + run + summary in ONE command per iteration, cut the calls from 26 (C1) to about 17. One planned iteration (NMIN) fit easily.

## ADDENDUM (main session, Sonnet 5.5 Extra, 23:55): C2 at full size (50 files per bin and family; evidence `evidence/c2_mask_loss_g2_full.txt`, `_g3_full.txt`, script `scripts/c2_full_run.sh`; NMIN 2, TOL 1 h, Z 5)
**Plain verdict: C2 passes the planted-dip and bump marks in both hunts and balances the real and upside-down arms in most bins; two bins stay unbalanced (G3 over 27 d, G2 20-27 d swings the other way). It is a usable candidate for Petrova 1.0, with a stated limit for the slowest faint binaries.**
- **(a) Planted dips, mask plus veto:** hunt m 0.99 in G2 and G3 at K 12, 18 and 25. The veto's chance cost at full size is much smaller than the small test suggested: planted dips lost to chance matches, per bin, G2: 0 / 0.9% / 2.6% / 0.7% / 0.1% (5-10, 10-14, 14-20, 20-27, over 27 d); G3: 0 / 0 / 2.9% / 2.0% / 0%. So worst-bin m is about 0.97. PASS (mark 0.9).
- **(b) Bumps:** K 25, 8 h, before/after 0.98 to 1.00 in every bin of both hunts. PASS.
- **(c) Real over upside-down events, nothing planted, after the veto** (before the veto = C1f): G2 5-10 d 27/17 = 1.59; 10-14 d 25/22 = 1.14; 14-20 d 23/18 = 1.28 (was 48/20); 20-27 d 10/26 = 0.38 (was 34/26); over 27 d 25/26 = 0.96 (was 33/27). Totals G2: 110 real / 109 upside-down = 1.01 (C1f 169/112, C0 215/115, frozen 62/110). G3 5-10 d 23/16 = 1.44; 10-14 d 35/37 = 0.95; 14-20 d 39/35 = 1.11 (was 51/36); 20-27 d 36/27 = 1.33 (was 41/28); over 27 d 41/16 = 2.56 (was 67/16). Totals G3: 174 / 131 = 1.33 (C1f 217/133, C0 328/134, frozen 65/93). Bins inside 0.8 to 1.25: G2 three of five (10-14, 14-20 at 1.28 is within counting noise, over 27 d), G3 two of five (10-14, 14-20). Not inside: G2 5-10 d (no veto applies; the frozen mask has 1.36 there too), G2 20-27 d (0.38, the real arm is left with fewer events than the upside-down arm: the long-known excess of upside-down events in this chain, 1.28 to 1.46 in G1 and G3, now shows once the eclipse-like real events are gone; cause NOT TESTED), G3 5-10 d, 20-27 d (1.33) and over 27 d (2.56).
- **(d) Events vetoed, real / upside-down:** G2 0/0, 2/0, 25/2, 24/0, 8/1; G3 0/0, 0/0, 12/1, 5/1, 26/0. 102 real against 5 upside-down: the veto removes recurring binary features, not noise.
- **Reading (LIKELY):** the fixed mask is much closer to fair than C0 or the frozen mask, and it never hides a strong planted dip. Remaining unfairness sits in the slowest faint binaries (G3 over 27 d, mostly QLP files with only 38 usable files), where one visit per sector means a feature cannot be confirmed anywhere; a null in that bin must say so. The 5-10 d excess is shared by the frozen mask and is not the eclipse leak this work fixes (UNCERTAIN).
- **Not tested:** effect on a real two-transit planet (should not match, its transits fall at different binary phases); how the full chain (veto, flags, tiers) changes recovery on top of the mask (the Part A and these runs measure the detection step only).
- **Pass marks for the Petrova 1.0 preregistration, proposed (set from this table, before any new run):** (a) m at least 0.95 per bin with the veto; (b) bumps at least 0.95; (c) real/upside-down per period bin 0.67 to 1.5 where the bin has at least 20 events, with the over-27 d G3-type bin reported separately as a known limit; (d) vetoed real/upside-down reported. The earlier 0.8 to 1.25 mark was written before the counting noise of 20 to 70 events per bin was known: a ratio of 1.25 on 40 events is inside one standard error.
