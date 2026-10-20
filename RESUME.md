# RESUME: how to pick Second Sun up again (read this first)

*Created 2026-10-20 21:55 UTC by Claude. Keep the "Status" table below current; it is the single source of truth for what is done and what is next. If the weekly limit stops work, anyone (including a fresh session a week later) can continue from here.*

## When can work continue?
- **Ahmed's weekly cap: 35%** of the weekly limit (his words, 2026-10-20: "Weekly limit cap is 35% and that's it"). Work stops at 35%, finished or not.
- The weekly window resets **2026-10-26 22:00 UTC** (27 October, 01:00 Kuwait). After that, say **"resume Second Sun"** in a new session. Nothing restarts by itself (timed tasks froze before: they need the PC and Auto mode).
- Check usage between tasks with the `get_usage` tool before starting each new step.

## What Ahmed approved (2026-10-20, in his words: "Go with whatever u recommended")
- **A. Bounded autonomy: yes.** Claude runs the frozen quality-mask experiment without asking at each step, writes the Field Note, and reports confirmed results, uncertainties and the next decision. **Stop and tell Ahmed if:** (1) the baseline reproduction does not match the saved results; (2) a step would change a tracked result or production file; (3) the usage cap is reached.
- **B. Weekly cap 35%.**
- **C. Labels: option 1.** The register keeps VERIFIED / LIKELY / UNVERIFIED. Test progress is written as plain words ("not tested yet"). CONFIRMED in the book becomes VERIFIED. (Compass reports to Ahmed may still say CONFIRMED; it means VERIFIED.)
- **Unchanged rules:** the star hunt stays paused (no G1 run, no 549 targets); the 136 unmeasured-morphology rows stay as they are (default: keep them and measure their eclipses ourselves, decide before a larger search); no helper sessions without asking; nothing outward-facing; no tokens or keys in the repo; nothing written to C:; every download logged in `research/downloads.csv` (this experiment needs none); same-day Field Note for every block of work; no dashes in book text.
- **Ahmed reads the book tonight (20/21 Oct) for the first time.** He will report "Lab N done" with results, or "LN done, 3/3". When he does: check it, then set the date in `book/progress/levels.yml`. Any friction he reports is the top fix.

## Status (update as you go)
| # | Task | Status |
|---|---|---|
| 1 | Save approvals and this file | done 2026-10-20 |
| 2 | Fix stale text and label vocabulary in the book | done 2026-10-20 (logged in mistakes.md) |
| 3 | Experiment manifest tool and frozen spec (`experiments/quality_mask/`) | done 2026-10-20 (SPEC.md + qmask.py, commits 03cbfbe, e4b1eb0; smoke-tested) |
| 4 | Reproduce the baseline (arm A0) against `pipeline/accept_v2_results.json`; stop if it does not match | done 2026-10-20: matched exactly |
| 5 | Run the SAP arms A1 (SAP + HARD) and A2 (SAP + DEFAULT) | done 2026-10-20: results in `experiments/quality_mask/results/20261020T215121Z_e40982b/` (summary.md); post-hoc diagnostics in `post_hoc/` |
| 6 | Field Note, publish book, update this file | done 2026-10-20 (Field Note evening section; Chapter 8 seventh test; claims F-054 to F-058) |
| 7 | Later: guard `accept_v2.py` (`__main__` guard, never overwrite tracked results); make `recover_cbp.py` save timestamped output | not started |
| 8 | Later: QLP recipe automation (OVERNIGHT.md task 12), then scale-up injection tests (about 200 trials per size, random timings, SPOC vs QLP, real fainter stars) | not started |
| 9 | Later, Ahmed's decisions: the 136 morph = -1 rows; ExoFOP publish-first path; STANLEY calibration | pending Ahmed |
| 10 | **Next scientific question (my recommendation, needs Ahmed's go because it changes the plan):** the experiment says (a) restored SAP cadences find S62 and S30 but add noise and maybe false alarms; (b) SAP gave a quieter noise estimate than PDCSAP in several sectors. Smallest follow-ups: (i) search restored stretches separately with their own noise estimate instead of pooling; (ii) run PDCSAP and SAP both and require agreement (rule C8) instead of choosing; (iii) replicate on a second star (Kepler-16, 94 light curves) before any production change; (iv) find out why PDCSAP's noise estimate is higher (e.g. S6) | proposed |

## Result of the experiment (2026-10-20, one star; read `experiments/quality_mask/results/20261020T215121Z_e40982b/summary.md`)
Baseline reproduced exactly. Milder filter (SAP + DEFAULT) found both missing crossings (S62 SNR 12.1, S30 SNR 10.5) but lowered SNR elsewhere (median -0.54) and 6 R_earth injections went 2/7 to 0/7; flipped-data events inconclusive (restored 6.8 vs 1.0 per 100 d, intervals overlap). Separately, SAP + HARD found 7 of 8 published transits vs PDCSAP's 4, because PDCSAP's noise estimate is larger (depths equal; cause unknown). Nothing in production changed.

## The experiment in one paragraph
The question: does our HARD quality filter throw away useful cadences? Facts already verified (2026-10-20, read-only): HARD (24319) and DEFAULT (17087) differ only in bits 64, 1024, 2048 and 4096; across the 10 TOI-1338 sectors DEFAULT would restore 45,502 cadences, all bit 4096 only; **PDCSAP flux is NaN on every one of them**, SAP is finite. So PDCSAP + HARD vs PDCSAP + DEFAULT is identical (a no-op), and the old loader would silently turn DEFAULT into SAP. Valid design: **A0** = existing PDCSAP + HARD (reproduce), **A1** = SAP + HARD, **A2** = SAP + DEFAULT. A0 vs A1 isolates the flux choice; A1 vs A2 isolates the mask. Same sectors, published times (Wang and Liu 2024), hand-tuned eclipse mask geometry (held fixed from A0), 2-day detrend, SNR 7 bar, flipped (2 - f) control, S98 injections at the baseline's retained 7 times. Full review text: Compass report of 2026-10-20 (to be filed as `research/compass-reviews/2026-10-20-quality-mask.md`).

## Where things live
- Experiment code, spec, results: `experiments/quality_mask/` (new; results in timestamped folders, never overwritten).
- Frozen baseline (never touch): `pipeline/accept_v2_results.json`, `pipeline/accept_v2_log.txt`, other `pipeline/*_results.json`.
- Never import or run `pipeline/accept_v2.py` or `pipeline/diag_v2.py` (they overwrite or write to the current folder when imported or run).
- Detector (read only, import from it): `pipeline/detect_v2.py`. Book: `book/`; publish with `research/burn-3-book/tools/publish_book.ps1`. "Is the book behind?": `.venv-docs\Scripts\python.exe book\tools\teach_check.py`.
- Python for everything: `D:\second-sun\.venv\Scripts\python.exe` (caches forced to D: by `labs/_env.py` for lab-style scripts).

## Resume checklist (a fresh session)
1. Read this file, then `research/decisions.md` (last entries) and `OVERNIGHT.md`.
2. `git log --oneline -8` and `git status --short`; the book should say "0 commits behind" from `teach_check.py`.
3. Check usage; confirm the weekly figure is under 35% (after the reset it will be near 0).
4. Continue with the first task above that is not done. Update the table and write the Field Note as you finish each one.
