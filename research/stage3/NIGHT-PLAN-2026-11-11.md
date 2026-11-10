# Night plan, 11 Nov 2026 (written 02:35 Kuwait; Ahmed asleep from about 02:30; morning report is the deliverable)

**His words (2:21 a.m.):** "Go with your default" (option A, Amendment 2), push the Search window card now, write the Search window blueprint, "plan how things go after the G2 test finishes", use the limit (30% is better, 35% is fine), and a detailed morning report that says clearly whether anything was found in the stars searched again, how good this is for the app, and what to lead forward to. I read this as the go for the whole plan including the ONE sealed run, with the stop rules below. The go file quotes his words.

**Meter at 02:30:** weekly 26%, 5-hour 11%. Target 30%, hard ceiling 35%, new work stops at 34%, never cross 35%.

## Steps and branches (times are guesses, UNCERTAIN)
| # | Step | When | Branch if it goes wrong |
|---|---|---|---|
| 1 | Card and book 2.11.0 pushed and published (done or running) | 02:30 | publish check fails: fix, republish, one line to him |
| 2 | G2 planted-dip gates finish (r1_gates_run.sh, log data\r1_gates.log) | about 03:10 | (a) or (b) FAIL in any bin: nothing frozen, the Opus repair (one try), then stop and write the morning report as "not frozen" |
| 3 | Start the three p1-off proofs again on the final code (about 10 min, 6 workers) | right after 2 | a difference: stop, report, nothing frozen |
| 4 | Nested Opus 5.5 medium check (brief R1-OPUS-CHECK-BRIEF-2026-11-11.md, 30 calls, no edits) | 03:15 to 03:40 | "Do not freeze": no freeze, no sealed run, report. "Freeze after N fixes": do the fixes (new commit, proofs again) if they are not rule changes; a rule change = new amendment, and I stop if it touches what the sealed run reads |
| 5 | Freeze: `r1_run.py freeze` (needs clean tree, proofs, both gate files), rename Vesper to Petrova in versions.md and the book, freeze field note | about 04:00 | freeze refuses: read why, fix the cause, else stop |
| 6 | Re-push the prepared card with the frozen version, then write the go file (his words) and start `pipeline\r1_go.ps1 6`: G3 unseen (328 stars) then G2 unseen (475 stars), each followed by the readout; then S4 completeness on both lists | about 04:15, run about 1.5 h plus S4 about 1.5 h | a crashed run resumes with the same hash; a bug found afterwards = fixed version runs again and BOTH results are reported (preregistration section 3) |
| 7 | Plain verdict from R1-RESULT-g3.txt and -g2.txt (counts only), notes, field note, Census spec note, book text, publish | as each result lands | an excess: leads stay private; nothing opened; I report "N leads under check" and wait for his yes |
| 8 | Morning report (below), ledger, RESUME, push | when the readouts and S4 are in, or at the 34% line | |

## Cap handling
Machine time is free; my calls are not. I wait on background tasks (no polling), read logs at most every 30 to 60 minutes, and write the morning report when the readouts are in. Expected cost from here: about 4 weekly points (Opus 0.5, freeze and proofs 0.4, run supervision 0.4, readout and notes 0.8, book and field note 0.5, morning report 0.4, slack 1). Leftover before 30%: nothing new is started except the next learning piece (units foundation) if the run is still going and the meter is under 30%. If the meter reaches 34% the machine keeps going and I only write the report.

## The morning report (short outline; the report itself is detailed)
1. **Plain verdict first:** found something / found nothing / N leads under check, for the stars searched again (the unseen G2 and G3 binary stars of 5 days or longer, in the light the old filter deleted).
2. Numbers first: stars, star-sectors, how much light was recovered, events real and upside-down, S1 by the new rule and as written, the control, S2, S4 completeness by period bin, what was skipped.
3. What the null means and what it does NOT mean (power, the Amendment 2 limit, G1 not covered).
4. What went wrong or was risky overnight, in plain words (the design problem, anything found by Opus, anything not tested).
5. How good this is for the app and the project, and what leads forward (Census, G1, Gaia DR4 on 2 Dec, a better filter 1.1.0 if the imbalance is eclipse leftovers, the learning screens).
6. Usage: meter at start, now, per step vs prediction; what is committed, pushed and published; what waits for him.
Files: `research/stage3/MORNING-REPORT-2026-11-11.md`, also sent to him.

## Added by Ahmed at about 02:50 (before he slept): what happens AFTER the morning report
Order, each step only if the meter is under 34% (30% preferred, 35% is the ceiling, never crossed):
1. **(DONE 02:52 at his request, before the other steps: watchdog v2 follows the exact python process trees by CPU time, detects STUCK / ENDED_UNMARKED / RUNNING-but-quiet, chains of scripts, low disk and memory, time jumps; tested with a sleeper, an exiter and a spinner; configs watch_g2_gates.json and watch_sealed_chain.json). Original note:** Watchdog review and improvement (`research/fable-audit-2026-11/scripts/watchdog.py`). Known weaknesses to look at first: it counts ANY python.exe, so an unrelated python process hides an idle job; STALL uses log file times only (a long step that logs rarely looks stuck, the Search window feed JSON updated each minute is a better liveness signal); it exits on the first done condition and cannot chain stages; it does not check disk space, free memory or a sleeping PC; no log of its own decisions.
2. **Light audit of the scripts and pages I made** with the second-sun-auditor skill (Python, JS, CSS, HTML, PowerShell; the book changes of today, `r1_gate.py`, `r1_readout.py`, `r1_reference_counts.py`, `watch_export.py` additions, `r1_go.ps1`, `watchdog.py`, `push_star_check.py`). Minimum usage: a cap of about 15 tool calls, scripts first (a small script that could contradict a belief), no deep audit. **Never edit the hashed Petrova files** (`stage2_search.py`, `stage3_core.py`, `stage3_report.py`, `stage3.py`, `vopts.py`, `petrova_mask.py`) or anything the sealed run reads; findings there go to FIX-QUEUE only. Small safe fixes are made at once with the test shown; the rest are filed.
3. **The fix list** (`research/stage3/FIX-QUEUE.md`), one item at a time, bugs only, Sonnet 5.5 Extra.
4. **The build list** (`research/stage3/BUILD-QUEUE.md`), only items that need no input from him, one task each.
Ahmed's words: do this after everything is done, then the fix list, then the build list, "only if you have usage".
