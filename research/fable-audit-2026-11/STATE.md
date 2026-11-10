# STATE (Fable audit run 1)

Updated 2026-11-10 09:50 Kuwait. Repo read at commit c9b9aca. Model claude-fable-5-2, medium.

## Rules in force
`01-FABLE-BRIEF.md` as changed by `02-AMENDMENT-1-SCALE-DOWN.md` (the amendment wins). Hard stop: Weekly all models 40%. Ladder: 30% core only, 35% work orders only, 38% report now. At most 1 helper, never Fable for reading. No book audit.

## Meters
- 02:49 start: 5-hour 45, bar 7, Fable 0.
- 02:54 stopped by the 5-hour limit: bar 17, Fable 20 (4 Fable helpers reading history).
- 09:48 restart: 5-hour 16, bar 19, Fable 22. Budget left: 21 bar points.

## Done
- Brief, saved answers and amendment read.
- History: `evidence/history/H1-resume-rules.md` and `H2-mistakes-ledger-queues.md` (H3, H4 lost, not redone).
- Core chain read by me: `detect_v2.py`, `stage2_search.py`, `stage3_core.py`, `stage3.py`, `vopts.py`, `g3_run.py`, `audit_all.py`, `dataset.py`.

## Done since restart
- P: `findings-P.md` (F-01 URGENT mask cuts dips in slow binaries, F-02 FIX 84 measured, F-03 to F-06). Evidence in `evidence/p01*.txt`, `p02_fix84.txt`, `p03_flipmatch.txt`.
- N: `findings-N.md` (F-07 to F-10). Evidence `evidence/n01_census_s2.txt`.
- S: `findings-S.md` (F-11 to F-16, ideas, roadmap). Gaia DR4 = 2 Dec 2026 (ESA page).
- R: `findings-R.md` (F-17 privacy leak in watch-data branch history, F-18 to F-21, pending decisions).

## Done (run 1 complete)
- L: skill installed at `C:\Users\hanzl\.claude\skills\second-sun-auditor\` (SKILL.md, examples.md). Blind bug test in `data\fable_audit_bugtest\` (4 bugs), key and generator in `data\fable_audit_private\`.
- Work orders: `work-orders/WO-F01.md`, `WO-F02-F04-F05-F06.md`, `WO-F09-to-F22.md` (includes WO-BUGTEST).
- `REPORT.md` written. Local commit made, not pushed.

## Fix step (done 10 Nov, on Ahmed's word "do whatever's left ... so that I can use the reset")
- His answers to both rounds: `03-AHMED-ANSWERS-ROUNDS.md`.
- `design/PETROVA-1.0-MASK-DESIGN.md` (repeat rule, tested prototype `scripts/d01_mask_v1_prototype.py`, `evidence/d01_mask_v1_prototype.txt`).
- `design/SLOW-BINARY-RESEARCH-PREREG-DRAFT.md` (draft only).
- `work-orders/RESEARCH-ORDERS.md` (RS-013 to RS-021 for Sonnet or Opus).
- Committed locally, not pushed. Ahmed may press the Fable reset.

## For Sonnet after run 1
Approved by Ahmed on 10 Nov: shorten RESUME; push local commits after a check that no file names a star; the outside-check rule; WO-F18 (tidy rules and queues, file the audit findings with tag [FABLE-Fnn]); all Sonnet-ok work orders (he may use Opus). NOT approved: rewriting the watch-data history ("Leave it").
Update RESUME.md and `research/usage-ledger.md` from this folder; copy RS-015 into `research/research-sessions.md`. Do not file queue items until Ahmed says yes.

## Python
`D:\second-sun\.venv\Scripts\python.exe` has lightkurve 2.6.0, numpy 1.26.4, astropy 7.2.3, wotan. Set PYTHONUTF8=1.




## Extension (Ahmed 10 Nov: do not reset yet, use Fable to 49% or bar 38%, then tell him to reset; auto-continue after the 5-hour reset)
Plan in order: (1) d02: mask prototype with catalogue window and single-visit lane, G2 SPOC, 30 stars per bin; (2) known planets on real light, old and new mask; (3) RS-021 and RS-016 research; (4) whole-chain mask loss m per hunt; (5) expand FABLE-TAKE-AND-IDEAS.md with detail per idea (how to tackle, traps, which is best, which to scrap); then the most important leftover. Progress lines are appended below.

- 11:5x (5-hour 86%, bar 28, Fable 38): step 1 `scripts/d02_mask_v1_catalogue_lane.py 20 5` is RUNNING in the background; its output goes to `evidence/d02_mask_v1_catalogue_lane.txt`. If the session stopped, read that file; if it is empty or partial, rerun the same command from `scripts/` with SS_SET=g2 (about 30 to 40 min).
- Step 2 DONE: `scripts/k01_known_planets_two_masks.py`, output `evidence/k01_known_planets.txt`. TIC 172900988 (SPOC 2-min S44 to 47 plus TESS-SPOC S21): 0 events with either mask, so the two S21 transits are NOT found by either mask at SNR 7 (NOT TESTED why: check the S21 file is 30-min data and whether the transits sit inside masked phases). TOI-1338 (40 SPOC sectors): frozen mask 11 events, repeat rule 16; 5 NEW events the frozen mask removed 28% to 100% of (BTJD 1422.20, 2047.86, 2156.20, 2185.60, 2199.93). The S10 event at 1579.04 (10 h, 2,112 ppm) has planet b's expected depth. OPEN QUESTION K1: events cluster near binary phase 0.06 to 0.14 and 0.55 to 0.70; either planet b's transits (period about 6.5 binary periods gives two alternating phases) or a binary-locked feature (a narrow secondary eclipse) that the POOLED fold missed because phase smears over 7 years. If the second, the repeat rule must count repeats per cycle with a phase tolerance, not through one global fold: DESIGN AMENDMENT A, to be written into `design/PETROVA-1.0-MASK-DESIGN.md` after d02. Sonnet check: compare the event list with the transit table of Kostov et al. 2020.
- Still to do, in order: read d02 result and write Amendment A; expand `FABLE-TAKE-AND-IDEAS.md` (detail per idea, traps, ranking, which to scrap); step 3 research (RS-021, RS-016) only if Fable judges it must be Fable; step 4 whole-chain m. Stop at Fable 49% or bar 38%, commit, tell Ahmed to press the reset.
- 12:0x (5-hour 89%, bar 28, Fable 39): IDEAS-PLAYBOOK.md written and committed (9cb7f29). d02 still running: first two period bins printed (5 to 10 d and 10 to 14 d), three to come. NEXT when it ends: read evidence/d02_mask_v1_catalogue_lane.txt, write Amendment A into the design note, commit; then steps 3 and 4 as budget allows.
- d02 DONE (`evidence/d02_mask_v1_catalogue_lane.txt`, 20 stars per bin): planted dips K 12 / K 25 found, frozen against pooled repeat rule: 5-10 d 0.90/1.00 and 0.80/1.00; 10-14 d 0.55/0.75 and 0.25/0.95; 14-20 d 0.35/1.00 and 0.05/1.00; 20-27 d 0.20/0.75 and 0.05/1.00; over 27 d 0.05/0.79 and 0.00/0.79. BUT with nothing planted the real arm outside the lane exceeds the upside-down arm in EVERY bin (0.28/0.15, 0.38/0.23, 0.46/0.22, 0.39/0.17, 0.13/0.06; frozen was 0.12/0.13, 0.24/0.30, 0.36/0.21, 0.15/0.14, 0.04/0.10). So the POOLED fold leaks eclipses (period drift over years smears them) and the catalogue window as coded did not help (single bins 3.0 -> 2.2; the Prsa phase convention is unverified). The pooled version must NOT be built.
- AMENDMENT A under test: `scripts/d03_mask_v1_hybrid.py 20 5` RUNNING in the background -> `evidence/d03_mask_v1_hybrid.txt`. Hybrid = the frozen per-sector runs, each kept as an eclipse only if it is low in 2 or more cycles anywhere in the star's sectors (phase tolerance width + 0.02); unconfirmed runs are not masked and form the lane. Pass marks: planted dips at least 0.9 in every bin, real over upside-down outside the lane within 0.8 to 1.25 or no worse than frozen. NEXT: read it, write Amendment A (with both results, honest) into `design/PETROVA-1.0-MASK-DESIGN.md`, commit.
- d03 DONE (evidence/d03_mask_v1_hybrid.txt). Amendment A written into the design note: pooled rule leaks, hybrid is balanced under 14 d but does not recover at 10 to 14 d; design NOT settled; next steps for Opus listed there. Meters: 5-hour 96, bar 29, Fable 41. REMAINING for Fable if resumed (stop at Fable 49 or bar 38): diagnose the 10 to 14 d failure of d03 (step 1 and 2 of Amendment A), then tell Ahmed to press the reset.

## FINAL STOP (2026-11-10 15:43 Kuwait): Fable 48%, bar 33%, 5-hour 25%. Stop line (Fable 49%) reached. Ahmed may press the reset.
Why the jump from 41 to 48 with no work: resuming this session after the 5-hour pause re-read its whole 400K context uncached (about 7 Fable points, 4 bar points). Lesson for the skill: never resume a large context after a long pause; save state, start a FRESH session, read STATE.md.
Nothing is running. All work is committed locally through d09c0ee plus this commit; nothing pushed.
REMAINING, for Opus 5.5 or Sonnet 5.5 Extra in a fresh session (read in this order: REPORT.md, FABLE-TAKE-AND-IDEAS.md, IDEAS-PLAYBOOK.md, design/PETROVA-1.0-MASK-DESIGN.md with Amendment A, 03-AHMED-ANSWERS-ROUNDS.md):
1. Mask design, Amendment A steps 1 to 4 (why the hybrid rule fails at 10 to 14 d; tighter tolerance and depth match; catalogue phase convention; rerun on 50 stars per bin). Opus, about 1.5 points.
2. WO-F01 part A: whole-chain mask loss m per hunt. Sonnet, about 1.5.
3. Known planets: match evidence/k01_known_planets.txt with the published transit tables; why TIC 172900988 S21 transits are not found. Sonnet, about 0.6.
4. Research orders RS-016 (first), RS-021, RS-018, RS-017, RS-013, RS-014, RS-020; RS-019 after 2 Dec. work-orders/RESEARCH-ORDERS.md.
5. Housekeeping Ahmed approved: shorten RESUME, push after the star-name check, outside-check rule, WO-F18 (tidy and file findings as [FABLE-Fnn]). Update RESUME.md, research/usage-ledger.md, research-sessions.md (RS-015).
