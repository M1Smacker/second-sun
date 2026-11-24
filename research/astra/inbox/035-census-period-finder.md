# 035: Census period finder (find a binary's period from its own TESS light)

Written by Claude, 24 Nov 2026, 11:17 pm Kuwait. GO: Ahmed, 23 Nov ("Both in parallel": Census build beside P) and 24 Nov 11:05 pm. Runs AFTER 034b, in whichever worktree codex_run gives you (read its note). Tree node 2.1 (T139 follow-up).

## Why
Claude merged the public EB lists (`research/stage3/census_union/T139-UNION-RESULT-2026-11-24.md`). The catalogues hold only about 580 bright unsearched binaries with an epoch and width. The Census's real pool is CALNet: 10,531 new bright binaries, 8,814 with no period anywhere. Your eclipse timer v3 (032) times eclipses once a period is known; it does not find one. This brief builds the missing front end.

## Build
1. `035_period.py`: for one star's TESS 2-minute light (all sectors given), find the binary period: an eclipse search (box or similar; your choice, say why), then the half-period and double-period check you already have (014/032 alias functions, imported unchanged and AST-checked as in 032b): odd and even eclipse depths, secondary phase. Output period, epoch (BTJD), primary width, secondary phase, number of eclipses seen, and a quality flag. Never output a period supported by fewer than 3 eclipses; flag single-eclipse stars instead (they matter: long periods).
2. Validation, preregistered here before you run anything: stars where the answer is known, from `data/census_union/eb_union.csv` with `source` prsa2022 or ttc_t3, P from 1 to 30 d, Tmag 13.5 or brighter, **excluding every G1 star (fence A) and every design_seen == 0 star of G2 and G3 (fence B)** (check against `targets/` lists; report the check). Pick 150 stars with a fixed seed 2026112501, stratified by period (1 to 5, 5 to 10, 10 to 30 d), using light already on disk if it exists for them; if not, download their SPOC 2-minute light from MAST into `data/astra/035/lc/` (log every file count and size in your report; Claude tells Ahmed).
3. Pass marks (written now, not tuned later): period within 0.1% of the catalogue for at least 85% of stars with 3 or more eclipses in the data; half or double period errors under 5%; every single-eclipse star flagged, none given a period. Report per period band. A mutation test: break the alias check and show the half-period rate rises.

## Rules
AGENTS.md applies. No pipeline edits, no frozen files, no search for planets in this light (period finding only). At most 2 workers and NUMBA_NUM_THREADS=1 (the D1 bench may still be running). Data only under `data/astra/035/`. Report `research/astra/reports/035-report.md` with a plain verdict line first (PASS, FAIL or PARTIAL, per band), labels CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED, meter before and after in `research/astra/USAGE.md`.
