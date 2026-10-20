# Overnight run 2026-10-20: queue + checkpoint

*Started ~00:58 UTC (03:58 Kuwait; first written as "01:05", an unchecked estimate, corrected) by the main session (Claude Opus 5.5) on Ahmed's go. Any session that resumes this run reads this file first, continues from the first unchecked item, and updates it.*

## Rules for this run
- **Budget:** hard ceiling 30% of the weekly limit (Ahmed). Stop new work at **25% weekly**. The week started 2026-10-19 22:00 UTC at 0%; it was 2% at 00:51 UTC. Check with `get_usage` between tasks. If the 5-hour window is at 90%+, checkpoint and stop.
- **No helpers/subagents** without Ahmed's OK. No outward-facing actions (no ExoFOP, no emails, no posts). Auto-push to github.com/M1Smacker/second-sun is allowed.
- Order: **science first**, then the study bible, then the website.
- Python: `D:\second-sun\.venv\Scripts\python.exe` with cache env vars on D: (see research/WAVE-BRIEF-COMMON.md). Docs: `.venv-docs`. Never write to C:.
- Run `date -u` before every timestamp. Labels: CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED / BLOCKED.
- The morning report goes in `MORNING-REPORT.md` (sections A-I of Ahmed's overnight brief).

## Queue
| # | Task | Done when | Skip/stop if | Status |
|---|---|---|---|---|
| 1 | **Detector v2**: matched-filter single-transit search (box template, durations 3-15 h, SNR on detrended out-of-eclipse flux), eclipse mask from a global ephemeris, SAP fallback where PDCSAP is NaN. Code in `pipeline/` | Unit self-check passes; runs on TOI-1338 S98 and finds the 4025.6 event | Can't beat v1 after 2 bounded attempts → record and move on | DONE (modest gain; see research/overnight-science) |
| 2 | **Acceptance test**: re-run burn 1's recovery (6 testable published TOI-1338 b transits) and injection (2-8 R_earth) with v2; also measure the false-alarm rate on transit-free stretches | Table v1 vs v2; detection floor and false alarms per star-sector stated | — | DONE |
| 3 | **Second known system** (Kepler-16 or TIC 172900988) recovery with v2 | Published transits recovered or misses explained | No TESS data covering a transit | DEFERRED: STANLEY + systematics veto first (report §5) |
| 4 | **Bible chapters 1-3** (stars + two-sun orbits; light curves + transits; why two-sun transits wander), each in the 7-step structure, on real project data/figures | Pages build strict; every claim labelled and sourced | — | DONE |
| 5 | **Bible chapter 4**: our detector, from intuition to code (uses tasks 1-2) | Same | — | DONE |
| 6 | **Website build** phase 1-3 of research/SITE-BLUEPRINT.md at `book/` (repo layout, design tokens, typography, sidebar with chapter progress, mission-control/observatory feel, still professional; not gamey), chapters from 4-5 moved in | `mkdocs build --strict` passes; checked at 390/1280 dark+light in a browser; no overflow; 0 console errors except the known service-worker one in the pane | — | DONE (design layer + chapters live in book/; deploy not enabled) |
| 7 | MORNING-REPORT.md, commit, push | Report has A-I | — | DONE (first version; updated as work continues) |

## Checkpoint log
- ~00:58 UTC: queue written. Burns 1-3 committed (200176c). Next: task 1.
- 01:03 UTC: tasks 1-2 done. v2 = small gain (4/8 sectors, floor ~6 R_E); limit is data noise + systematics (flipped-data bumps up to SNR 12.6). Task 3 deferred. Next: task 4 (bible chapters).
- 01:08 UTC: tasks 4-5 done: book/docs/book/ch1-ch4 (7-step structure), 18 new facts F-001..F-018 in book/data/claims.csv, glossary +10 terms, 3 real-data figures; mkdocs build --strict passes (2.45 s). Next: task 6 (website).
- 01:14 UTC: task 6 done. book/ = prototype + observatory.css (Source Serif 4 / IBM Plex Sans / Plex Mono, self-hosted OFL), sidebar mission-timeline with per-device read marks, mission status panel, chapter index, numbered equation blocks, figure plates. Verified in browser: 13 pages 0 overflow at 390 px, dark+light, 0 console errors, strict build passes. Next: task 7 (morning report).

## Queue, part 2 (added after tasks 1-7; budget still well under 25%)
| # | Task | Done when | Skip/stop if | Status |
|---|---|---|---|---|
| 8 | **Systematics veto** in `pipeline/`: reject events within 0.5 d of a data gap edge, near quality-flagged cadences / momentum dumps, or matched by a flipped-data event; re-run accept_v2 false-alarm + recovery with the veto | false alarms per sector re-measured; recovery of TOI-1338 b not reduced | veto kills real transits → loosen once, then record | DONE (loosened once to flags; report §6) |
| 9 | **STANLEY trial** on TOI-1338 (`.venv-tests`, MIT, imports only) | runs on cached sectors; recovers TOI-1338 b or failure explained | install/API blocks after 2 bounded tries → BLOCKED, record | pending |
| 10 | Update chapter 4 + MORNING-REPORT with 8-9 | build strict passes | — | pending |
- 01:15 UTC: task 7 done (MORNING-REPORT.md). Queue part 2 added (8-10). Next: task 8.
- 01:18 UTC: task 8 done. Strict veto lost 2/4 real transits; loosened once: gap/dump = flags, flipped-match = reject. 4/4 planets kept, 4/6 fakes flagged. Next: task 9 (STANLEY).
- 01:25 UTC: stability calculator added (pipeline/stability.py, self-check vs TOI-1338 passes; ch1 updated). Ch4 gets the veto test. STANLEY: attempt 1 failed (distutils missing under Py3.12 -> installed setuptools in its venv); found it downloads to C: -> stopped before any file landed, wrapper forces D:. Attempt 2 running.
- 01:26 UTC: book ch5 (vetting) added with facts F-019..F-023; strict build passes. STANLEY attempt 2: 40 sectors downloaded to D: (78 MB, logged), detrending running.
- 01:28 UTC: queue item H.3 done: S98 timing +56 +- 5 min (red noise) vs prediction +- 23 min = 2.4 sigma, shape-dependent (report section 7). STANLEY detrending still running (BLS over 40 sectors).
- 01:51 UTC: book ch6 (our data) added, facts F-024..F-028, strict build passes. STANLEY attempt 2 hit the 25-min cap mid eclipse-fit (exit 124, still progressing, no errors); restarted from saved raw data with a 2-h cap (CPU only, little usage).
- 01:53 UTC: G1 targets frozen: targets/g1_targets.csv (552 rows = 549 stars, provenance + checksums; self-check vs wave 3). Report section 8.
- 01:54 UTC: G1 coverage: all 549 stars have QLP (median 9 sectors), 275 SPOC 2-min, 312 TESS-SPOC; full ready-made G1 data ~6.3 GB. Report 8b.
- 01:56 UTC: QLP test: raw SAP swamped by scattered light (fakes to SNR 38.7); det_flux suppresses long transits (~70% depth lost). 2 bounded tries used; QLP support marked NOT READY (report section 9).
- 01:58 UTC: QLP task (2 tries): sys_rm_flux keeps depth (2038 ppm, SNR 6.4) but recurring ~14-d fakes (SNR to 43.8) remain; no gaps to trim. BLOCKED tonight; next steps in report 9b.
- 02:00 UTC: QLP partly fixed: sys_rm_flux + SPOC good-time windows -> only the planet (SNR 10.1), fakes 2 (max 9.7). Report 9c. Next: borrowed windows for QLP-only stars (not done).
