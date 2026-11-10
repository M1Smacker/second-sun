# The plan for the next job: freeze Petrova, search the hidden light, improve the learning screens (agreed with Ahmed, 11 Nov 2026, 7 ask-tool rounds)

## In ten lines (read this if nothing else)
1. **Order:** A) write the rules and freeze Petrova 1.0.0, B) run the hunt (machine does the work), C) build the learning quick wins while it runs, then read the hunt totals.
2. **Money:** weekly meter was 22% at 00:12 on 11 Nov. Target: work until the meter reads **30%**. If the planned work is not done by then, continue to a hard ceiling of **35%**. New work stops at 34%; the last point is for wrap-up. Never cross 35%.
3. **Who:** Sonnet 5.5 Extra does the main work. A nested Opus 5.5 medium (30-call stop) checks the pass marks and the freeze list, and gets one repair attempt if the whole-chain test fails. No Fable.
4. **Name:** Petrova 1.0.0. The rename from Vesper happens at the freeze. Vesper 0.8.1 stays untouched as the old reference. A later rule change would be 1.1.0.
5. **What the hunt searches:** every star of the three lists with a binary period of 5 d or more (about 2,056 stars on disk, no download). Both arms, real and upside-down.
6. **What counts as evidence:** only events in the light the OLD mask deleted and the NEW mask keeps ("the recovered light"). Other events are reported but never count, because 0.8.1 already judged that light.
7. **Split:** dry run on the 704 stars I already looked at while designing the mask (34% of 2,056: G2 420, G3 284, G1 none), bugs only. Then one sealed run on the 1,352 unseen stars. The pass or fail comes from the sealed stars; the seen stars are reported apart. (Built in step A1; list `targets/r1_targets.csv`.)
8. **Pass marks (set after I saw the C2 counts, which the preregistration says plainly):** planted dips kept at least 0.95 per bin; bumps at least 0.95; real over upside-down 0.67 to 1.5 where a bin has 20 or more events; vetoed events reported. G3 binaries over 27 d are a known limit: that bin's null is worded "excludes less".
9. **If something shows up:** counts first, no star named in the repo or the book; I run the two private checks, push a notification, and wait for your yes.
10. **PC:** hunt always at 70% (normal priority, numba threads capped). Short note to you after each step.

## Steps, models, predictions (UNCERTAIN, to be compared with the real cost)
| Step | What | Model and stop line | Predicted weekly points |
|---|---|---|---|
| A1 | Preregistration: update Fable's draft (`research/fable-audit-2026-11/design/SLOW-BINARY-RESEARCH-PREREG-DRAFT.md`) with these decisions, the star list with its SHA-256, the gates R1 (dips kept) and R2 (exchangeability), the leads stage rules; commit BEFORE any light is read | Sonnet 5.5 Extra | 0.5 |
| A2 | Put C2 (catalogue windows, within-sector repeat lane, event-stage cross-sector veto) into the real filter as a NEW module; Vesper files untouched | Sonnet | 1.0 to 1.5 |
| A3 | Whole-chain test on planted dips injected into RAW light before every step (veto, flags and tiers included; this was NOT TESTED), plus R2 on synthetic light | Sonnet | 0.5 to 1.0 |
| A4 | Outside check of pass marks and freeze list; one repair attempt if A3 fails | Opus 5.5 medium nested, 30-call stop | 0.5 (+1 if the repair is used) |
| A5 | Freeze: settings file, hash, versions rows, rename to Petrova, field note for the day | Sonnet | 0.5 |
| B1 | Build the seen and unseen split; Search window page (a "Re-search 1" card, counts-only blind feed, version label, archive link); book publish and live check | Sonnet | 0.5 |
| B2 | Dry run on the seen stars (bugs only, written down; a fix means 1.0.x with a zero-difference proof) | machine, cheap | 0.2 |
| B3 | Sealed run on unseen stars (one shot, refuses without the frozen hash and a clean tree) | machine | 0.1 |
| B4 | Totals-first readout (S1 excess, S2 false alarms without a pass mark, S3 single-visit lane), plain verdict, note, ledger; Census spec note (period, epoch, widths, secondary phase columns) | Sonnet | 0.8 |
| C | Learning quick wins: Back and "where was I", hide the 125 evidence chips, dashboard-lite on today's chapters (design from `LEARNING-SPACE-PROPOSAL-2026-11-03.md` sections B and C, approved as written); tested at 375 px in the browser pane only, NOT TESTED on his phone | Sonnet | 1.5 to 2.0 |
| Total | | | about 6.5 (range 5.7 to 8.3); meter should end near 28 to 30% |

If the planned work ends before 30%, the leftover goes to the next learning piece in order: units foundation, then the reader screen. The 30 to 35% band is only for finishing planned work, the Opus repair, or a lead check.

## Not this week
Units foundation and full reader, the full dashboard, the 8-page chapter on the filter (`BOOK-COVERAGE-AUDIT-2026-11-10.md`), the check engine, recomputing reach maps, Census build, FFI door v2 and G5 (Gaia DR4 on 2 Dec 2026). First thing after the 17 Nov reset: units foundation, dashboard, the chapter.

## Rules that stay
Counts only on real light; tune only on planted dips and synthetic eclipses; no star ids, event times or lead details in the repo or the book; `pipeline/` frozen files never edited (new module, new version); nothing outward without his yes except the already approved book publish and the push after the star-name check; unverified is not fixed; times read from `Get-Date`.

## Honest notes
- **G1 (549 Kepler-field stars) is not ready for the new mask:** its target list has an epoch and a period but no eclipse width. The widths must come from the Villanova catalogue and the same gates must be measured on G1. Default (found in A1): G1 is searched only after that check passes, otherwise it follows later. This may add about 0.3 points to A2/A3.
- Fable's draft names this hunt G4a. Census replaced G4, so we call it **Re-search 1**.
- The exchangeability mark in Fable's draft was 0.8 to 1.25. I loosen it to 0.67 to 1.5 because 1.25 on 40 events is inside one standard error, and I saw the C2 table first. The preregistration must say this.
- Part A found the old mask also loses 27 to 34% of strong dips at 5 to 10 d, so the draft's 10 d cut is replaced by 5 d.
- The whole chain (veto, flags, tiers) on top of the new mask has never been measured. A3 is the first time. If it fails, nothing is frozen and the Opus repair gets one try; then I stop and ask.
