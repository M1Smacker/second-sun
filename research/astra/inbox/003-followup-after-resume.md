# Brief 003 follow-up: Claude resumed and finished your run; you write the reading (13 Nov 2026)

**From:** Claude. **Branch:** `astra/003-recovery-sprint` (main is merged in: read `research/TREE.md` and AGENTS rule 13 first).

## What Claude did while you were stopped (do NOT rerun anything)
- Fence check clean. Archived your budget `STOP.json` to `data\astra\003\archive-stop\`. No unfinished trial folders needed moving.
- Ran your own command: `003_supervise.py --start 20 --limit 2000 --g2 2 --g3 2 --resume`, then `003_finishrun.py`. All exit 0, no tracebacks. Your resume path worked (first resumed runtime test: 1,011 new pairs, no duplicates).
- Outputs now complete: `recovery-summary.json` / `follow-summary.log` (R 0.2747, interval 0.2072 to 0.3371, FIX FIRST), `diagnosis-g2.json`, `study-summary.json` (multi-window), plus G3 diagnosis from before.
- Claude re-counted R, the reference counts per bin and the stage counts from the raw journals: identical to your summary. Filed in `research/stage3/G1-RECOVERY-BAR.md` (Result section) with the reference-band split: found but held below tier 1 53, outside windows 45, not found 41, mask 15, no safe windows 7, tier 1 61 (of 222).
- Your bug is filed as FIX 91 on Tree node 1.1.

## What only you still need to do (the judgement, not the machine work)
Budget: what is left of brief 003's 25-point cap (your USAGE says about 14 used). Astra High.
1. **Finish `reports/003-recovery-sprint.md`:** replace the RESUME HERE block with the final verdict line, the full tables (per bin, product, era, depth and duration cells, the paired dip/bump test with discordant pairs), and the usage.
2. **Why each stage loses planets, with file and line,** ordered by the Tree's branch 1 nodes: 1.1 tier-1 flags (which flags, alone and in overlap, on the reference band; the repeater flag first), 1.2 windows, 1.3 detection, 1.4 mask. Label CONFIRMED / LIKELY / UNCERTAIN.
3. **Node 1.5, the 5 to 10 day blind spot** (reference R 0.13, 6 of 48): what makes that bin lose more. Use only the existing trial journals and traces; no new injections unless a check is cheap and predeclared in the report first.
4. **The multi-window study, read honestly:** 41 dips gained but bump alarms 22 to 55. Is there any version that gains dips without raising bumps, or is it a no?
5. **"What I would do next and why"**, as a ranked list of Petrova 1.1 candidate changes, each naming its Tree node, the planets it should free on THIS bench, the false-alarm risk, and how to test it on the same 2,000 trials. Claude and Ahmed decide; you advise. Do not edit frozen files.

Stop signs and fences as before. Commit on your branch; Claude reviews and merges.
