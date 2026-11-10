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

## Waiting for Ahmed
Decision rounds (report section "Decisions for Ahmed"). The 14 Nov fix step does ONLY what he approves as "Fable only" (my recommendation: Petrova 1.0 mask design, WO-F01 part B), at most 8 bar points, then he presses the reset.

## For Sonnet after run 1
Update RESUME.md and `research/usage-ledger.md` from this folder; copy RS-015 into `research/research-sessions.md`. Do not file queue items until Ahmed says yes.

## Python
`D:\second-sun\.venv\Scripts\python.exe` has lightkurve 2.6.0, numpy 1.26.4, astropy 7.2.3, wotan. Set PYTHONUTF8=1.


